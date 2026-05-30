# -*- coding: utf-8 -*-
# Detect the lowest actual sung note (lowest prominent fundamental peak) per song.
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
    if a.ndim > 1:
        a = a.mean(axis=1)
    return a, sr

def hz_to_note(f):
    if f <= 0: return '-'
    midi = 69 + 12*np.log2(f/440.0)
    m = int(round(midi))
    cents = round((midi - m)*100)
    name = NAMES[m % 12]; octave = m//12 - 1
    return f'{name}{octave}{cents:+d}c'

print('Lowest prominent fundamental per song (threshold -40 dB rel. peak, search 50-500 Hz):')
glob_lo = (1e9, None, None)
for p in files:
    a, sr = load(p)
    f, P = welch(a, sr, nperseg=32768)   # ~1.35 Hz bins
    Pn = P / P.max()
    db = 10*np.log10(Pn + 1e-20)
    # restrict to 50-500 Hz, find peaks above -40 dB
    band = (f >= 50) & (f <= 500)
    fb, dbb = f[band], db[band]
    peaks, props = find_peaks(dbb, height=-40, prominence=6)
    if len(peaks):
        lo_f = fb[peaks[0]]; lo_db = dbb[peaks[0]]
    else:
        lo_f, lo_db = float('nan'), float('nan')
    print(f'  {wname(p):<14} lowest fundamental = {lo_f:6.1f} Hz  ({hz_to_note(lo_f)})  @ {lo_db:.0f} dB')
    if lo_f < glob_lo[0]:
        glob_lo = (lo_f, wname(p), lo_db)
print(f'\n=> GLOBAL lowest note across catalog: {glob_lo[0]:.1f} Hz ({hz_to_note(glob_lo[0])}) in {glob_lo[1]}')
