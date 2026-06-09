#!/usr/bin/env python3
"""Pre-render blending gate for Project Muse (WS1).

The channel is acapella-only on a single Miku voicebank, so we cannot fix
blend problems by separating timbres. Defects (Lead poking out, voice
collision, loudness/stereo drift) used to surface *after* render+publish via
코튼's ears, forcing remix/re-render (Chopin Lead spike, Boccherini 4 cycles).
This script moves an objective measurement gate to *before* the render commit.

It measures two layers:

  - FULL MIX (always)   — LUFS / True-Peak / LRA via ffmpeg loudnorm, plus
                          Mid/Side RMS and L/R correlation via numpy.
                          Compared against the live-catalog baseline.
                          This is the strong, absolute gate → failure mode (d).

  - STEMS (if --stems)  — arrangements follow the score, so stem track names
                          are free-form (e.g. "Miku Violin 1", "Miku Viola left").
                          The lead (the part Miku actually sings the melody on)
                          is identified by --lead <substring> (or a lead_ prefix
                          fallback). Everything else is treated as accompaniment.
                          Measures Lead-vs-rest balance overall and over a short
                          window (failure mode a = Lead 튐), pairwise spectral
                          overlap + low-mid mud across tracks (failure mode b),
                          and a Lead harshness probe (failure mode c).

Honesty note: (d) and (a) are reliable, threshold-backed gates. (b) and (c)
are reported as measurements + flag candidates whose absolute thresholds are
deliberately loose until calibrated against 코튼's listening over the first
few gated songs (헨델 onward). 코튼's ear stays the final gate for those.

Dependencies: ffmpeg on PATH, numpy, scipy. (muse_audio.py stays stdlib-only;
this heavier module is imported lazily by it.)
"""

from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

LEAD_PREFIX_FALLBACK = "lead"  # used only when --lead is not given

# --- Gate thresholds (failure mode d — absolute, backed by live-catalog baseline) ---
# Channel target is the -16 LUFS centre band (코튼 s394). Live catalog measured
# -15.5..-18.0. We hard-flag only clearly-out-of-family values and advise inside.
LUFS_ADVISE = (-17.0, -15.0)   # inside = on-target for new songs
LUFS_HARD = (-18.5, -13.5)     # outside = re-export almost certainly needed
TRUE_PEAK_CEILING = -1.0       # dBTP ceiling (코튼 baseline doctrine)
CORRELATION_MIN = 0.2          # L/R correlation floor (below = possible phase problem)

# --- Stem thresholds (failure mode a — Lead 튐; calibratable) ---
LEAD_VS_REST_ADVISE_DB = 3.0   # Lead RMS above (rest sum) by more than this = advise
LEAD_VS_REST_HARD_DB = 6.0     # ... clearly poking out
LEAD_TRANSIENT_WINDOW_S = 0.20 # short-window for time-localized Lead spikes
LEAD_TRANSIENT_FLAG_DB = 9.0   # if Lead exceeds rest by this in a window = spike flag
LEAD_TRANSIENT_MAX_PCT = 2.0   # ...and that happens in >2% of active windows


def db(x: float) -> float | None:
    return round(20 * math.log10(x), 2) if x > 0 else None


# --------------------------------------------------------------------------- #
# WAV loading (numpy, supports 16/24/32-bit PCM; scipy can't read int24)
# --------------------------------------------------------------------------- #
def load_wav(path: Path) -> tuple[np.ndarray, int]:
    with wave.open(str(path), "rb") as w:
        ch, sw, sr, n = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
        raw = w.readframes(n)
    if sw == 1:
        data = (np.frombuffer(raw, dtype=np.uint8).astype(np.float64) - 128.0) / 128.0
    elif sw == 2:
        data = np.frombuffer(raw, dtype="<i2").astype(np.float64) / 32768.0
    elif sw == 3:
        b = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 3).astype(np.int32)
        ints = b[:, 0] | (b[:, 1] << 8) | (b[:, 2] << 16)
        ints = np.where(ints & 0x800000, ints - 0x1000000, ints)
        data = ints.astype(np.float64) / 8388608.0
    elif sw == 4:
        data = np.frombuffer(raw, dtype="<i4").astype(np.float64) / 2147483648.0
    else:
        raise ValueError(f"Unsupported sample width: {sw}")
    data = data.reshape(-1, ch)
    return data, sr


def to_mono(data: np.ndarray) -> np.ndarray:
    return data.mean(axis=1) if data.ndim == 2 and data.shape[1] > 1 else data.reshape(-1)


def rms_db(x: np.ndarray) -> float | None:
    if x.size == 0:
        return None
    return db(float(np.sqrt(np.mean(x.astype(np.float64) ** 2))))


# --------------------------------------------------------------------------- #
# ffmpeg loudness (K-weighted LUFS / true-peak / LRA — gated measurement)
# --------------------------------------------------------------------------- #
def ffmpeg_loudness(path: Path) -> dict:
    try:
        proc = subprocess.run(
            ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
             "-af", "loudnorm=print_format=summary", "-f", "null", "-"],
            capture_output=True, text=True,
        )
    except FileNotFoundError:
        return {"error": "ffmpeg not found on PATH"}
    out = proc.stderr

    def grab(label: str) -> float | None:
        m = re.search(rf"Input {label}:\s*(-?[0-9.]+)", out)
        return float(m.group(1)) if m else None

    return {"lufs": grab("Integrated"), "true_peak": grab("True Peak"), "lra": grab("LRA")}


# --------------------------------------------------------------------------- #
# Full-mix analysis → failure mode (d)
# --------------------------------------------------------------------------- #
def analyze_full_mix(path: Path) -> dict:
    data, sr = load_wav(path)
    ch = data.shape[1]
    loud = ffmpeg_loudness(path)

    if ch >= 2:
        L, R = data[:, 0], data[:, 1]
        mid = (L + R) / 2.0
        side = (L - R) / 2.0
        mid_db, side_db = rms_db(mid), rms_db(side)
        denom = float(np.std(L) * np.std(R))
        corr = round(float(np.mean((L - L.mean()) * (R - R.mean())) / denom), 3) if denom > 0 else None
        width_db = round(side_db - mid_db, 2) if (side_db is not None and mid_db is not None) else None
    else:
        mid_db = rms_db(to_mono(data))
        side_db = None
        corr = 1.0
        width_db = None

    mono = to_mono(data)
    return {
        "file": path.name, "channels": ch, "sample_rate": sr,
        "duration_s": round(data.shape[0] / sr, 3) if sr else None,
        "lufs": loud.get("lufs"), "true_peak_dbtp": loud.get("true_peak"), "lra": loud.get("lra"),
        "mid_rms_db": mid_db, "side_rms_db": side_db,
        "stereo_width_db": width_db, "lr_correlation": corr,
        "rms_db": rms_db(mono), "band_energy_mono": octave_band_energy(mono, sr) if sr else None,
        "ffmpeg_error": loud.get("error"),
    }


def eval_full_mix(m: dict, baseline: dict | None) -> list[dict]:
    findings: list[dict] = []
    lufs, tp, corr = m.get("lufs"), m.get("true_peak_dbtp"), m.get("lr_correlation")

    if tp is not None and tp > TRUE_PEAK_CEILING:
        findings.append({"mode": "d", "severity": "hard",
                         "msg": f"True peak {tp} dBTP exceeds ceiling {TRUE_PEAK_CEILING} dBTP "
                                f"(clipping/IS-peak risk). Lower output gain / engage TP limiter."})
    if lufs is not None:
        if not (LUFS_HARD[0] <= lufs <= LUFS_HARD[1]):
            findings.append({"mode": "d", "severity": "hard",
                             "msg": f"Integrated {lufs} LUFS is outside family band "
                                    f"[{LUFS_HARD[0]}, {LUFS_HARD[1]}]. Re-export with gain correction."})
        elif not (LUFS_ADVISE[0] <= lufs <= LUFS_ADVISE[1]):
            findings.append({"mode": "d", "severity": "advise",
                             "msg": f"Integrated {lufs} LUFS is off the -16 target band "
                                    f"[{LUFS_ADVISE[0]}, {LUFS_ADVISE[1]}]. OK if intentional (intimate→-16.5~-17, lively→-15~-16)."})
    if corr is not None and corr < CORRELATION_MIN:
        findings.append({"mode": "d", "severity": "advise",
                         "msg": f"L/R correlation {corr} is low (<{CORRELATION_MIN}); check phase/mono-compatibility."})

    if baseline:
        for key, label in (("lufs", "LUFS"), ("side_rms_db", "Side RMS dB")):
            rng = baseline.get(key)
            v = m.get(key)
            if rng and v is not None and not (rng["min"] - 1.0 <= v <= rng["max"] + 1.0):
                findings.append({"mode": "d", "severity": "advise",
                                 "msg": f"{label} {v} sits outside live-catalog range "
                                        f"[{rng['min']}, {rng['max']}] (+/-1 tol). Will stand out in Non-Stop autoplay."})
    return findings


# --------------------------------------------------------------------------- #
# Spectral helpers
# --------------------------------------------------------------------------- #
def octave_band_energy(x: np.ndarray, sr: int) -> dict[str, float]:
    from scipy.signal import welch
    nper = min(8192, len(x)) if len(x) >= 256 else max(1, len(x))
    f, psd = welch(x, fs=sr, nperseg=nper)
    centers = [63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
    out = {}
    for c in centers:
        lo, hi = c / math.sqrt(2), c * math.sqrt(2)
        mask = (f >= lo) & (f < hi)
        out[str(c)] = float(np.sum(psd[mask]))
    return out


def windowed_rms(x: np.ndarray, sr: int, win_s: float) -> np.ndarray:
    w = max(1, int(sr * win_s))
    n = (len(x) // w) * w
    if n == 0:
        return np.array([])
    return np.sqrt(np.mean(x[:n].reshape(-1, w) ** 2, axis=1))


# --------------------------------------------------------------------------- #
# Stem analysis → failure modes (a), (b), (c)
# score-following arrangements → free-form track names; lead identified by match
# --------------------------------------------------------------------------- #
def classify_stems(stem_dir: Path, lead_match: str | None) -> tuple[list[Path], list[Path], list[Path]]:
    wavs = sorted(stem_dir.glob("*.wav"))
    lead, rest = [], []
    for w in wavs:
        name = w.stem.lower()
        is_lead = (lead_match.lower() in name) if lead_match else name.startswith(LEAD_PREFIX_FALLBACK)
        (lead if is_lead else rest).append(w)
    return lead, rest, wavs


def analyze_stems(stem_dir: Path, lead_match: str | None) -> dict:
    lead_paths, rest_paths, wavs = classify_stems(stem_dir, lead_match)
    report: dict = {
        "stem_dir": str(stem_dir),
        "lead_match": lead_match,
        "lead_tracks": [p.name for p in lead_paths],
        "accompaniment_tracks": [p.name for p in rest_paths],
        "findings": [],
    }
    if not wavs:
        report["findings"].append({"mode": "stem", "severity": "hard",
                                   "msg": "No WAV stems found in --stems dir."})
        return report

    # Load every track as mono; check sample-rate & duration consistency
    tracks: dict[str, np.ndarray] = {}
    srs, durs = set(), []
    for p in wavs:
        data, sr = load_wav(p)
        mono = to_mono(data)
        tracks[p.name] = mono
        srs.add(sr)
        durs.append(len(mono) / sr if sr else 0)
    if len(srs) > 1:
        report["findings"].append({"mode": "stem", "severity": "advise",
                                   "msg": f"Mixed sample rates across stems: {sorted(srs)}."})
    sr_common = sorted(srs)[0]
    if durs and max(durs) - min(durs) > 0.25:
        report["findings"].append({"mode": "stem", "severity": "advise",
                                   "msg": f"Stem durations differ by {round(max(durs)-min(durs),3)}s (>0.25s). "
                                          f"Check same-start / same-length export."})

    n = min(len(s) for s in tracks.values())
    tracks = {k: v[:n] for k, v in tracks.items()}
    report["track_rms_db"] = {k: rms_db(v) for k, v in tracks.items()}

    lead_sig = np.zeros(n)
    for p in lead_paths:
        lead_sig += tracks[p.name]
    rest_sig = np.zeros(n)
    for p in rest_paths:
        rest_sig += tracks[p.name]

    # --- (a) Lead 튐 ---
    if lead_paths:
        lead_db, rest_db = rms_db(lead_sig), rms_db(rest_sig)
        report["lead_balance"] = {
            "lead_rms_db": lead_db, "rest_rms_db": rest_db,
            "lead_minus_rest_db": round(lead_db - rest_db, 2) if (lead_db is not None and rest_db is not None) else None,
        }
        if lead_db is not None and rest_db is not None:
            diff = lead_db - rest_db
            if diff > LEAD_VS_REST_HARD_DB:
                report["findings"].append({"mode": "a", "severity": "hard",
                                           "msg": f"Lead is {round(diff,1)} dB above the accompaniment "
                                                  f"(> {LEAD_VS_REST_HARD_DB} dB) — Lead poking out. Pull Lead fader down."})
            elif diff > LEAD_VS_REST_ADVISE_DB:
                report["findings"].append({"mode": "a", "severity": "advise",
                                           "msg": f"Lead sits {round(diff,1)} dB above the accompaniment "
                                                  f"(> {LEAD_VS_REST_ADVISE_DB} dB). Check it doesn't dominate."})
        if rest_paths:
            lw = windowed_rms(lead_sig, sr_common, LEAD_TRANSIENT_WINDOW_S)
            rw = windowed_rms(rest_sig, sr_common, LEAD_TRANSIENT_WINDOW_S)
            m = min(len(lw), len(rw))
            if m:
                with np.errstate(divide="ignore"):
                    series = 20 * np.log10(np.maximum(lw[:m], 1e-9) / np.maximum(rw[:m], 1e-9))
                active = rw[:m] > (np.max(rw) * 0.05 if np.max(rw) > 0 else 0)
                spikes = int(np.sum((series > LEAD_TRANSIENT_FLAG_DB) & active))
                denom = max(1, int(np.sum(active)))
                pct = round(100.0 * spikes / denom, 2)
                report["lead_balance"]["spike_window_pct"] = pct
                if pct > LEAD_TRANSIENT_MAX_PCT:
                    report["findings"].append({"mode": "a", "severity": "advise",
                                               "msg": f"Lead spikes >{LEAD_TRANSIENT_FLAG_DB} dB above accompaniment in "
                                                      f"{pct}% of active windows (>{LEAD_TRANSIENT_MAX_PCT}%) — localized Lead 튐 "
                                                      f"(cf. Chopin). Inspect those passages."})
    else:
        report["findings"].append({"mode": "a", "severity": "advise",
                                   "msg": "No lead track identified (pass --lead <substring of the melody track name>). "
                                          "Lead-balance check skipped; only collision/loudness measured."})

    # --- (b) voice collision: pairwise spectral overlap + low-mid mud ---
    bands = {name: octave_band_energy(sig, sr_common) for name, sig in tracks.items()}
    report["band_energy"] = bands
    names = list(tracks.keys())
    overlaps = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            va = np.array(list(bands[names[i]].values()))
            vb = np.array(list(bands[names[j]].values()))
            denom = float(np.linalg.norm(va) * np.linalg.norm(vb))
            cos = round(float(np.dot(va, vb) / denom), 3) if denom > 0 else None
            overlaps.append({"pair": [names[i], names[j]], "spectral_cosine": cos})
    overlaps.sort(key=lambda o: (o["spectral_cosine"] is not None, o["spectral_cosine"]), reverse=True)
    report["spectral_overlap_top"] = overlaps[:5]

    full = lead_sig + rest_sig
    fb = octave_band_energy(full, sr_common)
    report["stem_sum_band"] = fb        # for bus-effect diagnosis vs full mix
    report["stem_sum_rms_db"] = rms_db(full)
    total = sum(fb.values()) or 1.0
    mud = round(100.0 * (fb["250"] + fb["500"]) / total, 1)
    report["low_mid_mud_pct"] = mud
    top_pairs = "; ".join(f"{o['pair'][0]}~{o['pair'][1]}:{o['spectral_cosine']}" for o in overlaps[:3])
    report["findings"].append({"mode": "b", "severity": "info",
                               "msg": f"Collision probes (calibrating): low-mid (250-500Hz) share = {mud}%; "
                                      f"highest spectral overlap pairs = {top_pairs or 'n/a'}. "
                                      f"No absolute threshold yet — compare to 코튼 listening over 헨델+."})

    # --- (c) Lead harshness probe ---
    if lead_paths:
        lb = octave_band_energy(lead_sig, sr_common)
        tot = sum(lb.values()) or 1.0
        hf = round(100.0 * (lb["8000"] + lb["16000"]) / tot, 1)
        report["lead_hf_share_pct"] = hf
        report["findings"].append({"mode": "c", "severity": "info",
                                   "msg": f"Melisma/legato distortion probe (calibrating): Lead HF (8k+16kHz) share = {hf}%. "
                                          f"Digital harshness on sustained vowels stays 코튼's listening call."})
    return report


# --------------------------------------------------------------------------- #
# Bus-effect diagnosis (lets 코튼 export with master bus ON; gate self-checks)
# --------------------------------------------------------------------------- #
def diagnose_bus_effect(full_mix: dict, stem_report: dict) -> dict | None:
    """Compare stem-sum tone vs full-mix tone. If the master bus landed
    differently on the stems than on the full mix, the per-track balance reads
    could be skewed — so the gate flags it instead of forcing 코튼 to toggle the
    bus on/off every export."""
    fb_full = full_mix.get("band_energy_mono")
    fb_stem = stem_report.get("stem_sum_band")
    if not (fb_full and fb_stem):
        return None
    keys = list(fb_full.keys())
    va = np.array([fb_full[k] for k in keys])
    vb = np.array([fb_stem[k] for k in keys])
    denom = float(np.linalg.norm(va) * np.linalg.norm(vb))
    cos = round(float(np.dot(va, vb) / denom), 4) if denom > 0 else None
    return {"tone_cosine": cos}


# --------------------------------------------------------------------------- #
# Verdict assembly
# --------------------------------------------------------------------------- #
def assemble_verdict(full_findings: list[dict], stem_report: dict | None) -> dict:
    all_findings = list(full_findings)
    if stem_report:
        all_findings += stem_report.get("findings", [])
    hard = [f for f in all_findings if f.get("severity") == "hard"]
    advise = [f for f in all_findings if f.get("severity") == "advise"]
    verdict = "FAIL" if hard else ("REVIEW" if advise else "PASS")
    return {"verdict": verdict, "hard": len(hard), "advise": len(advise),
            "note": "PASS/REVIEW/FAIL is the measurement layer only — 코튼 listening is the final gate."}


# --------------------------------------------------------------------------- #
# Commands
# --------------------------------------------------------------------------- #
def run_gate(args: argparse.Namespace) -> int:
    master = Path(args.master)
    if not master.exists():
        print(f"master not found: {master}", file=sys.stderr)
        return 2
    baseline = json.loads(Path(args.baseline).read_text(encoding="utf-8")) if args.baseline and Path(args.baseline).exists() else None
    base_ranges = baseline.get("ranges") if baseline else None

    full = analyze_full_mix(master)
    full_findings = eval_full_mix(full, base_ranges)
    stem_report = analyze_stems(Path(args.stems), args.lead or None) if args.stems and Path(args.stems).exists() else None
    if stem_report:
        diag = diagnose_bus_effect(full, stem_report)
        if diag and diag.get("tone_cosine") is not None:
            stem_report["bus_diagnosis"] = diag
            cos = diag["tone_cosine"]
            if cos < 0.97:
                stem_report["findings"].append({"mode": "bus", "severity": "advise",
                    "msg": f"Stem-sum tone vs full-mix tone cosine = {cos} (<0.97): the master bus seems to land "
                           f"differently on stems vs the full mix, so Lead-balance reads may be skewed. If a balance "
                           f"flag looks wrong, bypass only the bus comp/limiter and re-export this song."})
            else:
                stem_report["findings"].append({"mode": "bus", "severity": "info",
                    "msg": f"Stem-sum vs full-mix tone cosine = {cos} (>=0.97): bus processing is consistent across "
                           f"stems and mix → Lead-balance reads are trustworthy. No need to toggle the bus."})
    verdict = assemble_verdict(full_findings, stem_report)

    report = {"master": full, "full_mix_findings": full_findings, "stems": stem_report, "verdict": verdict}
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"=== Blend gate: {master.name} ===")
    print(f"  LUFS {full['lufs']} | TP {full['true_peak_dbtp']} dBTP | LRA {full['lra']} | "
          f"Side {full['side_rms_db']} dB | corr {full['lr_correlation']}")
    if stem_report and stem_report.get("lead_balance"):
        lb = stem_report["lead_balance"]
        print(f"  Lead {stem_report['lead_tracks']} vs accompaniment: {lb.get('lead_minus_rest_db')} dB | "
              f"spike windows {lb.get('spike_window_pct')}%")
    elif stem_report:
        print(f"  stems: {len(stem_report.get('accompaniment_tracks', []))+len(stem_report.get('lead_tracks', []))} tracks, "
              f"no lead identified (pass --lead)")
    elif not args.stems:
        print("  (no --stems given → full-mix layer only; Lead/collision checks skipped)")
    print(f"  VERDICT: {verdict['verdict']}  (hard={verdict['hard']} advise={verdict['advise']})")
    for f in full_findings + (stem_report.get("findings", []) if stem_report else []):
        sev = f.get("severity")
        if sev in ("hard", "advise", "info"):
            print(f"   [{sev}] ({f['mode']}) {f['msg']}")
    if args.out:
        print(f"  report → {args.out}")
    if args.strict and verdict["verdict"] == "FAIL":
        return 1
    return 0


def run_calibrate(args: argparse.Namespace) -> int:
    root = Path(args.works) if args.works else Path(__file__).resolve().parents[3] / "works"
    masters = sorted(root.glob("*/music/masters/Miku_*_master.wav"))
    if not masters:
        print(f"no masters under {root}", file=sys.stderr)
        return 2
    rows = []
    for m in masters:
        info = analyze_full_mix(m)
        info["work"] = m.parent.parent.parent.name
        rows.append(info)
        print(f"  {info['work']:26} LUFS {info['lufs']} | TP {info['true_peak_dbtp']} | "
              f"LRA {info['lra']} | Side {info['side_rms_db']} | corr {info['lr_correlation']}")

    def rng(key):
        vals = [r[key] for r in rows if r.get(key) is not None]
        return {"min": min(vals), "max": max(vals), "mean": round(sum(vals) / len(vals), 2)} if vals else None

    baseline = {
        "source": "live catalog full-mix masters",
        "n": len(rows),
        "works": [r["work"] for r in rows],
        "ranges": {k: rng(k) for k in ("lufs", "true_peak_dbtp", "lra", "side_rms_db", "mid_rms_db", "lr_correlation")},
        "per_work": rows,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(baseline, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nbaseline ({len(rows)} works) → {out}")
    print(f"  LUFS range {baseline['ranges']['lufs']}")
    print(f"  Side range {baseline['ranges']['side_rms_db']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Project Muse pre-render blending gate")
    sub = p.add_subparsers(dest="command", required=True)

    g = sub.add_parser("gate", help="Run the blending gate on a master (+ optional stems)")
    g.add_argument("--master", required=True, help="Full-mix master WAV")
    g.add_argument("--stems", default="", help="Dir of stem WAVs (free-form track names ok)")
    g.add_argument("--lead", default="", help="Substring of the melody/lead track name(s), e.g. 'Soprano' or 'Violin 1'")
    g.add_argument("--baseline", default="", help="baseline JSON (from calibrate)")
    g.add_argument("--out", default="", help="Write JSON report here")
    g.add_argument("--strict", action="store_true", help="Exit 1 when verdict is FAIL")
    g.set_defaults(func=run_gate)

    c = sub.add_parser("calibrate", help="Build baseline from live-catalog masters")
    c.add_argument("--out", required=True, help="Output baseline JSON path")
    c.add_argument("--works", default="", help="works/ root (default: repo works/)")
    c.set_defaults(func=run_calibrate)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
