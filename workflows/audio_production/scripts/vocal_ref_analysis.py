# -*- coding: utf-8 -*-
"""Vocal reference measurement for V6 tuning targets (s417 · ⑩ Handel).
Extracts: sustained-note vibrato (rate/depth/onset delay), attack scoop,
breath gaps, phrase dynamic arcs, register. Run on python 3.9 (parselmouth).
"""
import sys, json
import numpy as np
import soundfile as sf
import parselmouth
from scipy import signal

def main(path, fmin=180.0, fmax=1200.0):
    snd = parselmouth.Sound(path)
    sr_audio = snd.sampling_frequency
    x, _sr = sf.read(path)
    if x.ndim > 1:
        x = x.mean(axis=1)

    dt = 0.005
    pitch = snd.to_pitch_ac(time_step=dt, pitch_floor=fmin, pitch_ceiling=fmax)
    f0 = pitch.selected_array['frequency']
    t = pitch.xs()
    voiced = f0 > 0

    # intensity envelope on the same grid
    n_hop = int(_sr*dt)
    m = len(x)//n_hop
    rms = np.sqrt(np.mean(x[:m*n_hop].reshape(m, n_hop)**2, axis=1))
    rms_db = 20*np.log10(np.maximum(rms, 1e-12))
    # align lengths
    L = min(len(rms_db), len(f0))
    grid_t = np.arange(L)*dt

    # ---- voiced runs ----
    runs = []
    i = 0
    while i < L:
        if voiced[i]:
            j = i
            while j < L and voiced[j]:
                j += 1
            runs.append((i, j))
            i = j
        else:
            i += 1

    # ---- breath gaps between voiced runs (0.12-1.2 s) ----
    gaps = []
    for k in range(1, len(runs)):
        g0, g1 = runs[k-1][1], runs[k][0]
        dur = (g1-g0)*dt
        if 0.12 <= dur <= 1.2:
            gaps.append({"t": round(g0*dt, 2), "dur_s": round(dur, 2)})

    # ---- sustained notes: stable plateaus inside runs ----
    notes = []
    cents_all = np.full(L, np.nan)
    cents_all[voiced[:L]] = 1200*np.log2(f0[:L][voiced[:L]]/440.0)
    for (a, b) in runs:
        if (b-a)*dt < 0.5:
            continue
        seg = cents_all[a:b]
        # sliding stability: median filter, then split where jump > 80 cents
        med = signal.medfilt(seg, kernel_size=min(31, (len(seg)//2)*2+1))
        cut = [0] + list(np.where(np.abs(np.diff(med)) > 80)[0]+1) + [len(seg)]
        for c0, c1 in zip(cut[:-1], cut[1:]):
            if (c1-c0)*dt < 0.55:
                continue
            note_c = seg[c0:c1]
            center = np.nanmedian(note_c)
            dev = note_c - center
            if np.nanstd(dev) > 120:   # unstable / gliss
                continue
            # detrend slow drift (>0.7s)
            k_smooth = min(int(0.7/dt)//2*2+1, (len(dev)//2)*2+1)
            if k_smooth < 5:
                continue
            trend = signal.medfilt(dev, kernel_size=k_smooth)
            vib = dev - trend
            vib = np.nan_to_num(vib)
            # vibrato band 3.5-8.5 Hz
            fs = 1/dt
            sos = signal.butter(2, [3.5/(fs/2), 8.5/(fs/2)], btype='band', output='sos')
            vb = signal.sosfiltfilt(sos, vib)
            env = np.abs(signal.hilbert(vb))
            steady = np.median(env[len(env)//3:])
            if steady < 8:   # < 8 cents = no real vibrato
                continue
            # rate from FFT peak
            F = np.fft.rfft(vb*np.hanning(len(vb)))
            fr = np.fft.rfftfreq(len(vb), dt)
            band = (fr >= 3.5) & (fr <= 8.5)
            rate = float(fr[band][np.argmax(np.abs(F[band]))]) if band.any() else None
            # onset delay: first time env > 0.5*steady for >=0.1s
            th = 0.5*steady
            onset = None
            run_len = 0
            for ii, e in enumerate(env):
                run_len = run_len+1 if e > th else 0
                if run_len >= int(0.1/dt):
                    onset = (ii-run_len+1)*dt
                    break
            # attack scoop: mean of first 50 ms vs center
            scoop = float(np.nanmean(dev[:max(int(0.05/dt),1)]))
            t0 = (a+c0)*dt
            f_center = 440*2**(center/1200)
            notes.append({
                "t": round(t0, 2), "dur_s": round((c1-c0)*dt, 2),
                "f0_Hz": round(float(f_center), 1),
                "vib_rate_Hz": round(rate, 2) if rate else None,
                "vib_halfdepth_cents": round(float(np.median(env)*1.0), 1),
                "vib_onset_delay_s": round(onset, 2) if onset is not None else None,
                "attack_scoop_cents": round(scoop, 1),
            })

    # ---- phrase dynamics: voiced spans between breath gaps ----
    phrases = []
    bounds = [0] + [int(g["t"]/dt) for g in gaps] + [L]
    for p0, p1 in zip(bounds[:-1], bounds[1:]):
        vmask = voiced[p0:p1]
        if vmask.sum()*dt < 1.0:
            continue
        pd = rms_db[p0:p1][vmask[:len(rms_db[p0:p1])]]
        if len(pd) < 10:
            continue
        phrases.append({
            "t": round(p0*dt, 2), "dur_s": round((p1-p0)*dt, 2),
            "dyn_span_dB": round(float(np.percentile(pd, 95)-np.percentile(pd, 10)), 1),
        })

    voiced_f0 = f0[:L][voiced[:L]]
    out = {
        "file": path.split("\\")[-1],
        "register": {
            "f0_median_Hz": round(float(np.median(voiced_f0)), 1),
            "f0_p5_Hz": round(float(np.percentile(voiced_f0, 5)), 1),
            "f0_p95_Hz": round(float(np.percentile(voiced_f0, 95)), 1),
        },
        "n_sustained_notes": len(notes),
        "vibrato_summary": {
            "rate_Hz_median": round(float(np.median([n["vib_rate_Hz"] for n in notes if n["vib_rate_Hz"]])), 2) if notes else None,
            "halfdepth_cents_median": round(float(np.median([n["vib_halfdepth_cents"] for n in notes])), 1) if notes else None,
            "onset_delay_s_median": round(float(np.median([n["vib_onset_delay_s"] for n in notes if n["vib_onset_delay_s"] is not None])), 2) if notes else None,
            "attack_scoop_cents_median": round(float(np.median([n["attack_scoop_cents"] for n in notes])), 1) if notes else None,
        },
        "breath_gaps": {"count": len(gaps), "dur_s_median": round(float(np.median([g["dur_s"] for g in gaps])), 2) if gaps else None},
        "phrase_dyn_span_dB_median": round(float(np.median([p["dyn_span_dB"] for p in phrases])), 1) if phrases else None,
        "longest_notes": sorted(notes, key=lambda n: -n["dur_s"])[:12],
        "breath_gap_list_first20": gaps[:20],
    }
    print(json.dumps(out, indent=1, ensure_ascii=False))

if __name__ == "__main__":
    main(sys.argv[1])
