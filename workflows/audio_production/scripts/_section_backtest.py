#!/usr/bin/env python3
"""Backtest for proposed blend-gate failure mode (b'): time-localized section anomaly.

Question: 코튼/Fable proposed adding a 5th gate mode — flag 10s windows whose
band-energy profile deviates (z-score) from the whole-track mean — to catch the
"one section sounds off" defects (⑥/⑨2차/⑩) that whole-track QC misses.

But the ⑨ 2차 defect was logged as "구간RMS로는 안 잡힘 · null test 잔차 -31.6dB".
If RMS couldn't localize it, can band-energy z-score? This backtest answers it
against ground truth: the known-defective published version vs the fixed master.

  defect = renders/_published_s410_063cf16.wav  (0:50–1:40 balance defect)
  fixed  = masters/Miku_boccherini_minuet_master.wav

Three measurements:
  (1) Direct A/B diff per 10s window → does the difference localize to 0:50–1:40?
      (This is the null-test, resolved on the time axis. Ground-truth check.)
  (2) On the DEFECT file alone, run the proposed (b') detector: per-band log-energy
      z-score vs whole-track. Does window 0:50–1:40 flag as an outlier?
  (3) Same detector on the FIXED file → does the flag disappear after the fix?

If (1) localizes but (2) does NOT flag the defect window above the musical-variation
floor, the proposed (b') detector cannot catch ⑨-class defects → report the limit.
"""
import sys
from pathlib import Path
import numpy as np

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))
from blend_gate import load_wav, to_mono  # reuse loaders

CENTERS = [63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
WORKS = SCRIPTS.parents[2] / "works"

import argparse
import math
from scipy.signal import welch

CASES = {
    "boccherini": {  # ⑨ — null test -31.6dB, "구간RMS로는 안 잡힘", ~micro
        "defect": WORKS / "boccherini_minuet/music/renders/_published_s410_063cf16.wav",
        "fixed": WORKS / "boccherini_minuet/music/masters/Miku_boccherini_minuet_master.wav",
        "start": 50.0, "end": 100.0,
    },
    "handel": {  # ⑩ — 1:45-2:00 passage ~2dB recessed, larger defect
        "defect": WORKS / "handel_lascia_chio_pianga/music/renders/Miku_handel_lascia_chio_pianga_test4.wav",
        "fixed": WORKS / "handel_lascia_chio_pianga/music/masters/Miku_handel_lascia_chio_pianga_master.wav",
        "start": 105.0, "end": 120.0,
    },
}


def band_energy(x, sr):
    nper = min(8192, len(x)) if len(x) >= 256 else max(1, len(x))
    f, psd = welch(x, fs=sr, nperseg=nper)
    out = []
    for c in CENTERS:
        lo, hi = c / math.sqrt(2), c * math.sqrt(2)
        out.append(float(np.sum(psd[(f >= lo) & (f < hi)])))
    return np.array(out)


def windows(x, sr, win_s=10.0, hop_s=5.0):
    w, h = int(sr * win_s), int(sr * hop_s)
    starts = list(range(0, max(1, len(x) - w + 1), h))
    return [(s / sr, band_energy(x[s:s + w], sr)) for s in starts]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("case", choices=list(CASES))
    a = ap.parse_args()
    c = CASES[a.case]
    DEFECT, FIXED = c["defect"], c["fixed"]
    DEFECT_START, DEFECT_END = c["start"], c["end"]
    print(f"### CASE: {a.case} ###")
    xd, sr = load_wav(DEFECT)
    xf, _ = load_wav(FIXED)
    md, mf = to_mono(xd), to_mono(xf)
    n = min(len(md), len(mf))
    md, mf = md[:n], mf[:n]
    dur = n / sr
    print(f"defect={DEFECT.name}  fixed={FIXED.name}  sr={sr}  dur={dur:.1f}s")
    print(f"defect window of interest: {DEFECT_START:.0f}-{DEFECT_END:.0f}s\n")

    wd = windows(md, sr)
    wf = windows(mf, sr)
    m = min(len(wd), len(wf))
    wd, wf = wd[:m], wf[:m]
    tstarts = np.array([t for t, _ in wd])
    Bd = np.array([b for _, b in wd])  # (m, 9) defect band energies
    Bf = np.array([b for _, b in wf])

    # log domain (energy spans orders of magnitude)
    Ld = np.log10(np.maximum(Bd, 1e-12))
    Lf = np.log10(np.maximum(Bf, 1e-12))

    in_defect = (tstarts >= DEFECT_START - 5) & (tstarts < DEFECT_END)

    # ---- (1) Direct A/B diff per window: how different is defect vs fixed, in dB per band ----
    diff_db = 10.0 * (Ld - Lf)  # dB difference per band per window
    win_diff = np.sqrt(np.mean(diff_db ** 2, axis=1))  # RMS-across-bands dB diff per window
    print("(1) DIRECT A/B DIFF per 10s window (dB, RMS across bands) — ground truth of where the fix changed things:")
    order = np.argsort(-win_diff)
    for i in order[:8]:
        mark = "  <-- in defect window" if in_defect[i] else ""
        print(f"    t={tstarts[i]:5.0f}s  diff={win_diff[i]:.3f} dB{mark}")
    print(f"    mean diff inside  0:50-1:40 = {win_diff[in_defect].mean():.3f} dB")
    print(f"    mean diff outside 0:50-1:40 = {win_diff[~in_defect].mean():.3f} dB")
    print(f"    localization ratio (in/out) = {win_diff[in_defect].mean()/max(win_diff[~in_defect].mean(),1e-9):.2f}x\n")

    # ---- (2)/(3) Proposed (b') detector: per-band z-score vs whole-track, on EACH file alone ----
    def detector(L, label):
        mean = L.mean(axis=0)
        std = L.std(axis=0) + 1e-9
        Z = (L - mean) / std
        score = np.max(np.abs(Z), axis=1)  # max-band |z| per window = "section anomaly score"
        print(f"(b') DETECTOR on {label}: per-window max-band |z| (higher = more anomalous vs track avg)")
        order = np.argsort(-score)
        flagged_top = set(order[:5].tolist())
        for i in order[:8]:
            mark = "  <-- in defect window" if in_defect[i] else ""
            print(f"    t={tstarts[i]:5.0f}s  score={score[i]:.2f}{mark}")
        print(f"    mean score inside  0:50-1:40 = {score[in_defect].mean():.2f}")
        print(f"    mean score outside 0:50-1:40 = {score[~in_defect].mean():.2f}")
        # Does the defect window rank among the top anomalies?
        defect_idx = np.where(in_defect)[0]
        ranks = [int(np.where(order == di)[0][0]) + 1 for di in defect_idx]
        print(f"    defect-window ranks among {m} windows (1=most anomalous): {sorted(ranks)}")
        print(f"    → would (b') point 코튼 at 0:50-1:40? top-5 windows include defect window: "
              f"{bool(set(defect_idx.tolist()) & flagged_top)}\n")
        return score

    sd = detector(Ld, "DEFECT file")
    sf = detector(Lf, "FIXED file")

    print("VERDICT INPUTS:")
    print(f"  - If (1) localization ratio >> 1: the fix really was concentrated at 0:50-1:40 (ground truth holds).")
    print(f"  - If (b') defect-window does NOT rank top-few on the DEFECT file: the proposed detector")
    print(f"    cannot distinguish the ⑨ defect from normal musical variation → it would not have caught it.")
    print(f"  - Compare defect-file score vs fixed-file score at 0:50-1:40: "
          f"defect={sd[in_defect].mean():.2f} vs fixed={sf[in_defect].mean():.2f} "
          f"(near-equal = detector blind to the change).")


if __name__ == "__main__":
    main()
