# -*- coding: utf-8 -*-
import numpy as np, glob, os
from scipy.io import wavfile
from scipy.signal import welch

files = sorted(glob.glob('Project_Muse/works/*/video/visualizer/public/audio.wav'))

def wname(p):
    parts = p.replace(os.sep, '/').split('/')
    return parts[parts.index('works') + 1][:13]

def load(p):
    sr, a = wavfile.read(p)
    a = a.astype(np.float64)
    if a.ndim > 1:
        a = a.mean(axis=1)
    return a, sr

print(f'{"song":<14}{"peak":>7}{"roll85":>8}{"roll95":>8}{"roll99":>8}{"-40dB hi":>10}{"-60dB hi":>10}')
for p in files:
    a, sr = load(p)
    f, P = welch(a, sr, nperseg=16384)
    Pn = P / P.max()
    db = 10 * np.log10(Pn + 1e-20)
    c = np.cumsum(P) / P.sum()
    peak = f[np.argmax(P)]
    r85 = f[np.searchsorted(c, 0.85)]
    r95 = f[np.searchsorted(c, 0.95)]
    r99 = f[np.searchsorted(c, 0.99)]
    hi40 = f[db >= -40][-1]
    hi60 = f[db >= -60][-1]
    print(f'{wname(p):<14}{peak:>7.0f}{r85:>8.0f}{r95:>8.0f}{r99:>8.0f}{hi40:>10.0f}{hi60:>10.0f}')

# octave-band energy share for mozart (coloratura highs)
mz = [x for x in files if 'mozart' in x][0]
a, sr = load(mz)
f, P = welch(a, sr, nperseg=16384)
print('\nmozart octave-band energy share:')
edges = [20, 160, 320, 640, 1280, 2560, 5120, 10240, 22050]
tot = P.sum()
for lo, hi in zip(edges[:-1], edges[1:]):
    m = (f >= lo) & (f < hi)
    print(f'  {lo:>6}-{hi:<6} Hz : {100*P[m].sum()/tot:5.1f}%')
