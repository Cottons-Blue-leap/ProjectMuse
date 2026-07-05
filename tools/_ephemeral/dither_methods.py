"""
디더 방식 비교 (scratch · 2026-06-22).
코튼 질문: "1픽셀 단위 미세 변동으로 자연스러운 연결 가능할 텐데, 이게 최선? Remotion 한계?"
→ 8bit 양자화를 어떻게 디더하느냐의 문제. 4방식을 인코딩 통과 후 비교.
  A. plain         : 단순 round (밴딩 baseline)
  B. random 1LSB   : 랜덤(triangular) 디더 ±1 — 우리 grain의 정밀 최소판
  C. ordered(Bayer): 8x8 정렬 디더 1LSB — 규칙적 미세 패턴, grain 거의 안 보임
  D. random strong : 랜덤 ±3 — 우리 Remotion grain류(강함=grain 보임)
"""
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 2560, 1440
OUT = Path(__file__).parent
FF = r"C:\Users\user\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffmpeg.exe"
STOPS = ["#181614", "#6F6A60", "#D8D2C4"]

def hexrgb(h):
    h = h.lstrip("#"); return np.array([int(h[i:i+2],16) for i in (0,2,4)], np.float64)

def gradient_float():
    c0,c1,c2 = (hexrgb(s) for s in STOPS)
    t = np.linspace(0,1,H); col = np.empty((H,3)); lo = t<=0.5
    col[lo]  = c0*(1-(t[lo]/0.5)[:,None]) + c1*((t[lo]/0.5)[:,None])
    a = ((t[~lo]-0.5)/0.5)[:,None]; col[~lo] = c1*(1-a) + c2*a
    return np.repeat(col[:,None,:], W, axis=1)

BAYER8 = np.array([
    [ 0,32, 8,40, 2,34,10,42],[48,16,56,24,50,18,58,26],
    [12,44, 4,36,14,46, 6,38],[60,28,52,20,62,30,54,22],
    [ 3,35,11,43, 1,33, 9,41],[51,19,59,27,49,17,57,25],
    [15,47, 7,39,13,45, 5,37],[63,31,55,23,61,29,53,21]], np.float64)

def to8(a): return np.clip(np.round(a),0,255).astype(np.uint8)

def tri(amp, seed):
    r = np.random.default_rng(seed)
    return (r.random((H,W,1))-r.random((H,W,1)))*amp

def bayer_threshold():
    ty = (BAYER8+0.5)/64.0 - 0.5   # -0.5~+0.5
    tiled = np.tile(ty, (H//8+1, W//8+1))[:H,:W]
    return tiled[:,:,None]

g = gradient_float()
methods = {
    "A plain (round)":     to8(g),
    "B random 1LSB":       to8(g + tri(1.0, 1)),
    "C ordered Bayer 1LSB":to8(g + bayer_threshold()),
    "D random strong 3":   to8(g + tri(3.0, 2)),
}

def encode_metric(u8, tag):
    src=OUT/f"_d_{tag}.png"; mp4=OUT/f"_d_{tag}.mp4"; dec=OUT/f"_dd_{tag}.png"
    Image.fromarray(u8).save(src)
    subprocess.run([FF,"-y","-loop","1","-i",str(src),"-frames:v","1","-c:v","libx264",
                    "-crf","16","-pix_fmt","yuv420p",str(mp4)],check=True,capture_output=True)
    subprocess.run([FF,"-y","-i",str(mp4),"-frames:v","1",str(dec)],check=True,capture_output=True)
    return np.array(Image.open(dec).convert("RGB"))

# 어두운 상단 크롭 (밴딩 최악)
y0,y1,x0,x1 = 120, 760, 80, 470
crops={}
for name,u8 in methods.items():
    enc = encode_metric(u8, name.split()[0])
    c = enc[y0:y1,x0:x1]; crops[name]=c
    rm = c.reshape(c.shape[0],-1,3).mean(1).mean(1)
    print(f"{name}: 인코딩후 행밴딩 계단강도={np.abs(np.diff(rm,2)).sum():.1f}")

# 4-way 크롭 비교
h,wd,_=next(iter(crops.values())).shape; gap=6; top=46
im=Image.fromarray(np.full((h+top, wd*4+gap*3,3),18,np.uint8)); d=ImageDraw.Draw(im)
f=ImageFont.truetype(r"C:\Windows\Fonts\malgunbd.ttf",19)
for i,(k,c) in enumerate(crops.items()):
    x=i*(wd+gap); im.paste(Image.fromarray(c),(x,top)); d.text((x+5,13),k,fill=(255,255,255),font=f)
im.save(OUT/"dither_methods_compare.png"); print("saved", im.size)
