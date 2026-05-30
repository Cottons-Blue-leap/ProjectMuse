# -*- coding: utf-8 -*-
# Focused low-frequency analysis: is there real energy below C1/C2/C3?
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

# note refs
C1, C2, C3 = 32.70, 65.41, 130.81
print(f'{"song":<14}{"-40dB lo":>9}{"-60dB lo":>9}{"%<C1":>8}{"%<C2":>8}{"%<C3":>8}{"%<200":>8}')
for p in files:
    a, sr = load(p)
    # fine low-freq resolution: nperseg 65536 -> bin width ~0.67 Hz
    f, P = welch(a, sr, nperseg=65536)
    Pn = P / P.max()
    db = 10 * np.log10(Pn + 1e-20)
    tot = P.sum()
    # lowest freq exceeding -40 / -60 dB
    lo40 = f[db >= -40][0]
    lo60 = f[db >= -60][0]
    def share(hz):
        return 100 * P[f < hz].sum() / tot
    print(f'{wname(p):<14}{lo40:>9.1f}{lo60:>9.1f}{share(C1):>8.3f}{share(C2):>8.3f}{share(C3):>8.3f}{share(200):>8.3f}')

# show the raw low-end spectrum (sub-200Hz) for the song with most low energy
print('\nsub-200Hz fine spectrum (peak-normalized dB) per song, every ~10Hz:')
for p in files:
    a, sr = load(p)
    f, P = welch(a, sr, nperseg=65536)
    db = 10 * np.log10(P / P.max() + 1e-20)
    pts = []
    for hz in [20, 30, 40, 50, 65, 80, 100, 130, 160, 200]:
        i = np.searchsorted(f, hz)
        pts.append(f'{hz}:{db[i]:.0f}')
    print(f'  {wname(p):<14} ' + ' '.join(pts))
