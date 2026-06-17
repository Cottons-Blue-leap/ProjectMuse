#!/usr/bin/env python3
"""muse_captions.py — timed lyric-line cues from a VOCALOID6 .vpr project.

Phase 2 of the CC caption pipeline. Reads vocal (Soprano/Lead) note onsets +
phonemes from a .vpr, segments them into lyric lines, and emits cues.json
(timed, language-neutral, one cue per sung line occurrence). cues.json x
lyrics.json -> locale VTTs (Phase 3, muse_captions.py vtt).

Handles: tempo map (ticks->seconds incl. ritardando), L/R panning-duplicate
vocal tracks (dedup), da capo / internal repeats (a region's note-index map is
reused for identical material), wordless vocalise tails (auto-skipped).

Segmentation source = a per-work sidecar  lyrics/cue_map.json  whose note-index
ranges are derived from (and verifiable against) the .vpr phoneme stream. Use
`dump` to print that stream when building a map for a new song.

Usage:
  python muse.py captions dump <work_id>           # phoneme timeline (build a map)
  python muse.py captions cues <work_id>           # write lyrics/cues.json
  python muse.py captions vtt  <work_id>           # write lyrics/captions.<lang>.vtt x N
  python muse.py captions all  <work_id>           # cues + vtt
"""
from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[3]          # Project_Muse/
TPQ = 480                                            # VOCALOID ticks per quarter
FILLER_PH = {"-", "", "4 M", "M", "Sil", "sil", "br"}  # melisma/continuation/filler


def work_dir(work_id: str) -> Path:
    d = ROOT / "works" / work_id
    if not d.exists():
        sys.exit(f"work 없음: {d}")
    return d


def load_map(wd: Path) -> dict:
    p = wd / "lyrics" / "cue_map.json"
    if not p.exists():
        sys.exit(f"cue_map.json 없음: {p}  (먼저 `dump`로 phoneme 확인 후 작성)")
    return json.loads(p.read_text(encoding="utf-8"))


def tempo_fn(seq: dict):
    te = sorted(seq["masterTrack"]["tempo"]["events"], key=lambda e: e["pos"])

    def t2s(tick: int) -> float:
        sec = 0.0
        for i, e in enumerate(te):
            start, bpm = e["pos"], e["value"] / 100.0
            end = te[i + 1]["pos"] if i + 1 < len(te) else None
            if end is not None and tick > end:
                sec += (end - start) / TPQ * (60.0 / bpm)
            elif tick >= start:
                sec += (tick - start) / TPQ * (60.0 / bpm)
                break
        return round(sec, 3)

    return t2s


def vocal_parts(seq: dict, name_contains: str):
    """Return de-duplicated vocal parts: list of (track_name, part_notes[]).
    L/R panning copies are identical -> keep one per (start_tick, note_count)."""
    seen, parts = set(), []
    for t in seq["tracks"]:
        if name_contains.lower() not in t.get("name", "").lower():
            continue
        for p in t.get("parts", []):
            notes = p.get("notes", [])
            if not notes:
                continue
            poff = p.get("pos", 0)
            key = (poff, len(notes), notes[0].get("phoneme", ""))
            if key in seen:
                continue
            seen.add(key)
            abs_notes = [
                {"pos": poff + n["pos"], "dur": n["duration"], "ph": n.get("phoneme", "")}
                for n in notes
            ]
            parts.append((t["name"], poff, abs_notes))
    parts.sort(key=lambda x: x[1])
    return [(nm, ns) for nm, _, ns in parts]


def classify_region(notes, signatures: dict) -> str | None:
    """Return region type key whose signature phoneme appears in the first
    ~8 phonemes, or None if wordless (only filler/nasal hum)."""
    head = [n["ph"] for n in notes[:8]]
    for rtype, sigs in signatures.items():
        if any(s in head for s in sigs):
            return rtype
    # wordless if every phoneme is a single nasal/filler (e.g. 'N\\')
    uniq = {n["ph"] for n in notes}
    if uniq and all(p in FILLER_PH or p.strip() in {"N\\", "N"} for p in uniq):
        return None
    return None


def build_cues(seq, cmap, t2s):
    lines_meta = cmap["maps"]
    sigs = cmap["region_signatures"]
    merge = cmap.get("merge_consecutive_same_line", True)
    parts = vocal_parts(seq, cmap.get("vocal_track_name_contains", "Soprano"))
    cues = []
    for nm, notes in parts:
        rtype = classify_region(notes, sigs)
        if rtype is None:
            continue  # wordless vocalise tail -> no caption
        amap = lines_meta[rtype]
        for lo, hi, line in amap:
            if lo >= len(notes):
                continue
            hi = min(hi, len(notes) - 1)
            start = t2s(notes[lo]["pos"])
            nxt = notes[hi + 1]["pos"] if hi + 1 < len(notes) else notes[hi]["pos"] + notes[hi]["dur"]
            end = t2s(nxt)
            cues.append({"start": start, "end": end, "line": line, "region": rtype, "track": nm})
    cues.sort(key=lambda c: c["start"])
    if merge:
        merged = []
        for c in cues:
            if merged and merged[-1]["line"] == c["line"] and abs(merged[-1]["end"] - c["start"]) < 0.6:
                merged[-1]["end"] = c["end"]
            else:
                merged.append(dict(c))
        cues = merged
    for i, c in enumerate(cues, 1):
        c["idx"] = i
    return cues


def cmd_dump(work_id: str):
    wd = work_dir(work_id)
    cmap = load_map(wd) if (wd / "lyrics" / "cue_map.json").exists() else {}
    vpr = wd / cmap.get("vpr", "music/renders") if cmap else None
    if not cmap:
        cand = list((wd / "music" / "renders").glob("*.vpr"))
        vpr = cand[0] if cand else None
    if not vpr or not Path(vpr).exists():
        sys.exit(f".vpr 없음: {vpr}")
    seq = json.loads(zipfile.ZipFile(vpr).read("Project/sequence.json"))
    t2s = tempo_fn(seq)
    nc = cmap.get("vocal_track_name_contains", "Soprano") if cmap else "Soprano"
    for nm, notes in vocal_parts(seq, nc):
        print(f"\n=== {nm}  ({len(notes)} notes  {t2s(notes[0]['pos'])}s–{t2s(notes[-1]['pos']+notes[-1]['dur'])}s) ===")
        for i, n in enumerate(notes):
            print(f"{i:3} {t2s(n['pos']):7.2f}-{t2s(n['pos']+n['dur']):7.2f}  {n['ph']}")


def cmd_cues(work_id: str):
    wd = work_dir(work_id)
    cmap = load_map(wd)
    vpr = wd / cmap["vpr"]
    seq = json.loads(zipfile.ZipFile(vpr).read("Project/sequence.json"))
    t2s = tempo_fn(seq)
    cues = build_cues(seq, cmap, t2s)
    lyr = json.loads((wd / "lyrics" / "lyrics.json").read_text(encoding="utf-8"))
    by_idx = {l["idx"]: l for l in lyr["lines"]}
    for c in cues:
        c["original"] = by_idx[c["line"]]["original"]
        c["section"] = by_idx[c["line"]]["section"]
    out = {
        "work_id": work_id,
        "vpr": cmap["vpr"],
        "sync_offset_sec": 0.0,
        "note": "Timed line cues from .vpr note onsets. sync_offset_sec is a global shift applied at VTT build (cotton listen-gate). end of last cue must be <= audio duration.",
        "cue_count": len(cues),
        "cues": cues,
    }
    p = wd / "lyrics" / "cues.json"
    p.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    # report
    print(f"cues.json 작성: {len(cues)} cues")
    last = cues[-1]["end"] if cues else 0
    print(f"마지막 cue end = {last}s")
    overlaps = sum(1 for a, b in zip(cues, cues[1:]) if b["start"] < a["end"] - 0.01)
    print(f"겹침(overlap) = {overlaps}")
    for c in cues:
        print(f"  {c['idx']:2} {c['start']:7.2f}-{c['end']:7.2f} [{c['section']}{c['line']}] {c['original']}")


def fmt_ts(s: float) -> str:
    s = max(0.0, s)
    h = int(s // 3600); m = int((s % 3600) // 60); sec = s % 60
    return f"{h:02d}:{m:02d}:{sec:06.3f}"


def cmd_vtt(work_id: str):
    wd = work_dir(work_id)
    cues = json.loads((wd / "lyrics" / "cues.json").read_text(encoding="utf-8"))
    lyr = json.loads((wd / "lyrics" / "lyrics.json").read_text(encoding="utf-8"))
    by_idx = {l["idx"]: l for l in lyr["lines"]}
    off = cues.get("sync_offset_sec", 0.0)
    original_lang = lyr.get("source", {}).get("original_lang")  # e.g. 'it'; usually absent from our 10
    dur = None
    audio = wd / "video" / "visualizer" / "public" / "audio.wav"
    written = []
    for lang in lyr["locales"]:
        out_lines = ["WEBVTT", ""]
        for c in cues["cues"]:
            line = by_idx[c["line"]]
            orig = line["original"]
            trans = line.get(lang, "")
            body = orig if lang == original_lang else f"{orig}\n{trans}"
            out_lines.append(f"{fmt_ts(c['start']+off)} --> {fmt_ts(c['end']+off)}")
            out_lines.append(body)
            out_lines.append("")
        p = wd / "lyrics" / f"captions.{lang}.vtt"
        p.write_text("\n".join(out_lines), encoding="utf-8")
        written.append(p.name)
    print(f"VTT {len(written)}개 작성 (offset {off}s): {', '.join(written)}")


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    sub, work_id = argv[0], argv[1]
    if sub == "dump":
        cmd_dump(work_id)
    elif sub == "cues":
        cmd_cues(work_id)
    elif sub == "vtt":
        cmd_vtt(work_id)
    elif sub == "all":
        cmd_cues(work_id)
        cmd_vtt(work_id)
    else:
        sys.exit(f"알 수 없는 서브커맨드: {sub}")


if __name__ == "__main__":
    main(sys.argv[1:])
