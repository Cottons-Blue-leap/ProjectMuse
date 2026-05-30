# -*- coding: utf-8 -*-
# Detect the highest sung fundamental per song. Guard against harmonics:
# a peak f is treated as a fundamental only if f/2 does NOT carry comparable energy.
import numpy as np, glob, os
from scipy.io import wavfile
from scipy.signal import welch, find_peaks

files = sorted(glob.glob('Project_Muse/works/*/video/visualizer/public/audio.wav'))
NAMES = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

def wname(p):
    parts = p.replace(os.sep, '/').split('/')
    return parts[parts.index('works') + 1][:13]

def load(p):
    sr, a = wavfile.read(p)
    a = a.astype(np.float64)
    if a.ndim > 1: a = a.mean(axis=1)
    return a, sr

def hz_to_note(f):
    if f <= 0 or np.isnan(f): return '-'
    midi = 69 + 12*np.log2(f/440.0); m = int(round(midi))
    cents = round((midi - m)*100)
    return f'{NAMES[m%12]}{m//12-1}{cents:+d}c'

print('Highest sung fundamental per song (peaks >-30dB, 300-2500Hz; harmonic-guarded):')
glob_hi = (0, None, None)
for p in files:
    a, sr = load(p)
    f, P = welch(a, sr, nperseg=32768)
    Pn = P / P.max(); db = 10*np.log10(Pn + 1e-20)
    band = (f >= 300) & (f <= 2500)
    fb, dbb = f[band], db[band]
    peaks, _ = find_peaks(dbb, height=-30, prominence=5)
    hi_f = float('nan'); hi_db = float('nan')
    # go from highest peak downward; accept first that is NOT a mere harmonic
    for pk in peaks[::-1]:
        pf = fb[pk]
        # energy near pf/2
        sub = (f >= pf/2*0.97) & (f <= pf/2*1.03)
        sub_db = db[sub].max() if sub.any() else -99
        if sub_db < dbb[pk] + 3:   # f/2 not clearly stronger -> pf is a fundamental
            hi_f, hi_db = pf, dbb[pk]; break
    print(f'  {wname(p):<14} highest fundamental = {hi_f:7.1f} Hz  ({hz_to_note(hi_f)})  @ {hi_db:.0f} dB')
    if hi_f > glob_hi[0]:
        glob_hi = (hi_f, wname(p), hi_db)
print(f'\n=> GLOBAL highest note across catalog: {glob_hi[0]:.1f} Hz ({hz_to_note(glob_hi[0])}) in {glob_hi[1]}')
