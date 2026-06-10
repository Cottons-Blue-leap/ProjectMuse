# -*- coding: utf-8 -*-
"""One-off reverb/space diagnosis for ⑩ Handel test1 (s417).
Measures proxies for 'sacredness': tail RT estimate, gap fill, per-band
stereo width, spectral balance, tail brightness. Compares against
published masters (Pachelbel = baroque sibling, Chopin = slow/intimate).
"""
import sys, json
import numpy as np
import soundfile as sf
from scipy import signal

BANDS = [(20,60),(60,120),(120,250),(250,500),(500,1000),
         (1000,2000),(2000,4000),(4000,8000),(8000,16000)]

def band_filter(x, sr, lo, hi):
    ny = sr/2
    hi = min(hi, ny*0.99)
    sos = signal.butter(4, [lo/ny, hi/ny], btype='band', output='sos')
    return signal.sosfilt(sos, x)

def db(x):
    return 20*np.log10(np.maximum(x, 1e-12))

def envelope_db(x, sr, hop=0.05):
    n = int(sr*hop)
    m = len(x)//n
    e = np.sqrt(np.mean(x[:m*n].reshape(m, n)**2, axis=1))
    return db(e), hop

def analyze(path):
    x, sr = sf.read(path)
    if x.ndim == 1:
        x = np.stack([x, x], axis=1)
    L, R = x[:,0], x[:,1]
    mid, side = (L+R)/2, (L-R)/2
    mono = mid
    out = {"file": path.split("\\")[-1], "sr": sr, "dur_s": round(len(mono)/sr,1)}

    # ---- per-band energy balance + width ----
    bands = {}
    tot = np.sqrt(np.mean(mono**2))
    for lo, hi in BANDS:
        bm = band_filter(mid, sr, lo, hi)
        bs = band_filter(side, sr, lo, hi)
        rm = np.sqrt(np.mean(bm**2)); rs = np.sqrt(np.mean(bs**2))
        bands[f"{lo}-{hi}"] = {
            "level_rel_dB": round(float(db(rm) - db(tot)), 1),
            "side_minus_mid_dB": round(float(db(rs) - db(rm)), 1),
        }
    out["bands"] = bands

    # ---- envelope / gaps ----
    env, hop = envelope_db(mono, sr)
    body = env[env > env.max()-60]
    p50 = float(np.percentile(body, 50)); p5 = float(np.percentile(body, 5))
    out["gap_floor_p5_minus_p50_dB"] = round(p5 - p50, 1)

    # ---- final tail RT estimate (Schroeder on last decay) ----
    # find end of signal (last frame above max-55dB)
    above = np.where(env > env.max()-55)[0]
    end_i = above[-1] if len(above) else len(env)-1
    # last local max within 8 s before end
    start_search = max(0, end_i - int(8/hop))
    seg = env[start_search:end_i+1]
    pk = int(np.argmax(seg)) + start_search
    tail = mono[int(pk*hop*sr):int((end_i+1)*hop*sr)]
    rt = None
    if len(tail) > sr//2:
        e2 = tail.astype(np.float64)**2
        sch = np.cumsum(e2[::-1])[::-1]
        sch_db = 10*np.log10(np.maximum(sch/sch[0], 1e-12))
        t = np.arange(len(sch_db))/sr
        # fit -5..-25 dB region (T20 x3)
        i5 = np.argmax(sch_db <= -5); i25 = np.argmax(sch_db <= -25)
        if i25 > i5 > 0:
            slope = (sch_db[i25]-sch_db[i5])/(t[i25]-t[i5])
            rt = round(float(-60/slope), 2)
    out["tail_RT60_est_s"] = rt

    # ---- tail brightness vs body brightness (spectral centroid) ----
    def centroid(seg_x):
        f, P = signal.welch(seg_x, sr, nperseg=8192)
        m = (f>50)&(f<16000)
        return float(np.sum(f[m]*P[m])/np.sum(P[m]))
    n_body = int(min(len(mono)*0.5, 60*sr))
    out["centroid_body_Hz"] = round(centroid(mono[int(len(mono)*0.2):int(len(mono)*0.2)+n_body]), 0)
    if len(tail) > sr//2:
        # use latter half of tail = mostly reverb
        out["centroid_tail_Hz"] = round(centroid(tail[len(tail)//2:]), 0)

    # ---- mid-piece decay after offsets: how fast do gaps dry out ----
    # find frames where env drops >= 12 dB within 0.4 s
    drops = []
    w = int(0.4/hop)
    for i in range(len(env)-w):
        d = env[i] - env[i+w]
        if d > 0 and env[i] > p50 - 10:
            drops.append(d)
    if drops:
        out["fastest_offset_drop_dB_per_0.4s"] = round(float(np.percentile(drops, 99)), 1)

    return out

if __name__ == "__main__":
    results = [analyze(p) for p in sys.argv[1:]]
    print(json.dumps(results, indent=1, ensure_ascii=False))
