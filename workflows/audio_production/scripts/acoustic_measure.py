#!/usr/bin/env python3
"""
acoustic_measure.py — Muse MOKA 측정 패스 표준 도구

매 곡 test render 음향분석 (LUFS/TP/LRA + 포맷 + 클리핑/DC + head/tail 무음
+ 스테레오 side-mid·상관 + 스펙트럼 밴드 + crest factor).

방법론 정본 = works/haydn_trumpet_concerto_finale/notes/acoustic-analysis.md
도구: ffmpeg loudnorm(summary) + numpy/soundfile.

usage: python acoustic_measure.py <wav> [--label LABEL]
"""
import argparse
import json
import re
import subprocess
import sys

import numpy as np
import soundfile as sf

FFMPEG = "ffmpeg"

BANDS = [
    ("sub 20-80", 20, 80),
    ("low 80-250", 80, 250),
    ("lowmid 250-500", 250, 500),
    ("mid 500-2k", 500, 2000),
    ("himid 2-6k", 2000, 6000),
    ("high 6-12k", 6000, 12000),
    ("air 12-20k", 12000, 20000),
]


def ffmpeg_loudnorm(path):
    """ffmpeg loudnorm 1st-pass summary → integrated/TP/LRA/threshold."""
    cmd = [FFMPEG, "-hide_banner", "-i", path,
           "-af", "loudnorm=I=-16:TP=-1.0:LRA=11:print_format=json",
           "-f", "null", "-"]
    p = subprocess.run(cmd, capture_output=True, text=True)
    out = p.stderr
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", out, re.S)
    if not m:
        return None
    d = json.loads(m.group(0))
    return {
        "integrated": float(d["input_i"]),
        "true_peak": float(d["input_tp"]),
        "lra": float(d["input_lra"]),
        "threshold": float(d["input_thresh"]),
    }


def spectrum_bands(mono, sr):
    """RMS-power 분포를 밴드별 비중(%)으로."""
    n = len(mono)
    # 윈도우 처리 FFT (단일 큰 FFT)
    win = np.hanning(n)
    spec = np.abs(np.fft.rfft(mono * win)) ** 2
    freqs = np.fft.rfftfreq(n, 1.0 / sr)
    total = spec.sum()
    out = []
    for name, lo, hi in BANDS:
        mask = (freqs >= lo) & (freqs < hi)
        frac = spec[mask].sum() / total * 100 if total > 0 else 0.0
        out.append((name, frac))
    return out


def silence_edges(mono, sr, thresh_db=-60):
    """head/tail 무음 길이(초). thresh 이하를 무음으로."""
    amp = np.abs(mono)
    thr = 10 ** (thresh_db / 20.0)
    above = np.where(amp > thr)[0]
    if len(above) == 0:
        return len(mono) / sr, 0.0
    head = above[0] / sr
    tail = (len(mono) - 1 - above[-1]) / sr
    return head, tail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wav")
    ap.add_argument("--label", default="")
    args = ap.parse_args()

    data, sr = sf.read(args.wav, always_2d=True)
    nframes, nch = data.shape
    dur = nframes / sr

    info = sf.info(args.wav)
    subtype = info.subtype

    # 클리핑 / DC
    peak = float(np.max(np.abs(data)))
    clip_samps = int(np.sum(np.abs(data) >= 0.999))
    dc = float(np.mean(data))

    # mono mix
    mono = data.mean(axis=1)

    # head/tail 무음
    head, tail = silence_edges(mono, sr)

    # crest factor (peak / rms, dB)
    rms = np.sqrt(np.mean(mono ** 2))
    crest = 20 * np.log10(peak / rms) if rms > 0 else float("inf")

    # 스테레오
    stereo = {}
    if nch == 2:
        L, R = data[:, 0], data[:, 1]
        mid = (L + R) / 2
        side = (L - R) / 2
        rms_mid = np.sqrt(np.mean(mid ** 2))
        rms_side = np.sqrt(np.mean(side ** 2))
        side_mid_db = 20 * np.log10(rms_side / rms_mid) if rms_mid > 0 else float("-inf")
        denom = np.sqrt(np.sum(L ** 2) * np.sum(R ** 2))
        corr = float(np.sum(L * R) / denom) if denom > 0 else 0.0
        stereo = {"side_mid_db": side_mid_db, "corr": corr}

    # 스펙트럼
    bands = spectrum_bands(mono, sr)

    # 라우드니스
    loud = ffmpeg_loudnorm(args.wav)

    # ---- 출력 ----
    lbl = f" [{args.label}]" if args.label else ""
    print(f"=== 음향 측정{lbl} ===")
    print(f"file: {args.wav}")
    print(f"\n[포맷]")
    print(f"  {sr} Hz / {subtype} / {nch}ch / {dur:.1f}s ({int(dur//60)}:{dur%60:04.1f})")
    print(f"  peak={peak:.4f} ({20*np.log10(peak):.2f} dBFS) · clip(|x|>=.999)={clip_samps} · DC={dc:+.2e}")
    print(f"  head silence={head:.2f}s · tail silence={tail:.2f}s")
    if loud:
        print(f"\n[라우드니스] (ffmpeg loudnorm)")
        print(f"  Integrated : {loud['integrated']:+.1f} LUFS")
        print(f"  True Peak  : {loud['true_peak']:+.1f} dBTP")
        print(f"  LRA        : {loud['lra']:.1f} LU")
        print(f"  Threshold  : {loud['threshold']:+.1f} LUFS")
    print(f"\n[다이내믹]")
    print(f"  Crest factor: {crest:.1f} dB (peak/rms)")
    if stereo:
        print(f"\n[스테레오]")
        print(f"  Side-Mid: {stereo['side_mid_db']:.1f} dB · L/R 상관: {stereo['corr']:.3f}")
    print(f"\n[스펙트럼] (power 분포)")
    for name, frac in bands:
        bar = "#" * int(frac / 2)
        print(f"  {name:<16} {frac:5.1f}%  {bar}")
    print()


if __name__ == "__main__":
    main()
