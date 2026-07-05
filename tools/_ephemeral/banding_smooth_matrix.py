"""
밴딩 제거 강도 매트릭스 (scratch · 2026-06-22).
디더 강도 × 인코딩 품질(8bit/10bit, crf) 조합을 1:1 크롭으로 비교.
"""
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 2560, 1440
OUT = Path(__file__).parent
FFMPEG = r"C:\Users\user\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffmpeg.exe"
STOPS = ["#181614", "#6F6A60", "#D8D2C4"]   # ⑩ 헨델 무채 (밴딩 최악)

def hexrgb(h):
    h = h.lstrip("#"); return np.array([int(h[i:i+2],16) for i in (0,2,4)], np.float64)

def gradient_float():
    c0,c1,c2 = (hexrgb(s) for s in STOPS)
    t = np.linspace(0,1,H); col = np.empty((H,3))
    lo = t<=0.5
    col[lo]  = c0*(1-(t[lo]/0.5)[:,None])      + c1*((t[lo]/0.5)[:,None])
    a = ((t[~lo]-0.5)/0.5)[:,None]
    col[~lo] = c1*(1-a) + c2*a
    return np.repeat(col[:,None,:], W, axis=1)

def tri_noise(shape, amp, seed):
    r = np.random.default_rng(seed)
    return (r.random(shape)-r.random(shape))*amp

def to8(a): return np.clip(np.round(a),0,255).astype(np.uint8)

def encode(u8, tag, crf, tenbit):
    src=OUT/f"_m_{tag}.png"; mp4=OUT/f"_m_{tag}.mp4"; dec=OUT/f"_md_{tag}.png"
    Image.fromarray(u8).save(src)
    px = "yuv420p10le" if tenbit else "yuv420p"
    args=[FFMPEG,"-y","-loop","1","-i",str(src),"-frames:v","1","-c:v","libx264",
          "-crf",str(crf),"-pix_fmt",px]
    if tenbit: args+=["-profile:v","high10"]
    args.append(str(mp4))
    subprocess.run(args,check=True,capture_output=True)
    subprocess.run([FFMPEG,"-y","-i",str(mp4),"-frames:v","1",str(dec)],check=True,capture_output=True)
    return np.array(Image.open(dec).convert("RGB"))

grad = gradient_float()
panels = [
    ("현재: 디더 없음 · 8bit crf23", encode(to8(grad), "p1", 23, False)),
    ("디더 2% · 8bit crf23",        encode(to8(grad+tri_noise(grad.shape,5.1,1)), "p2", 23, False)),
    ("디더 2% · 10bit crf18",       encode(to8(grad+tri_noise(grad.shape,5.1,2)), "p3", 18, True)),
    ("디더 3% · 10bit crf18",       encode(to8(grad+tri_noise(grad.shape,7.6,3)), "p4", 18, True)),
]

# 어두운 미드톤 1:1 크롭
y0,y1, x0,x1 = 300, 1200, 900, 1600   # 700x900
cw, ch = x1-x0, y1-y0
gap, top = 8, 70
canvas = np.full((ch+top, cw*len(panels)+gap*(len(panels)-1), 3), 18, np.uint8)
font = ImageFont.truetype(r"C:\Windows\Fonts\malgunbd.ttf", 30)
im = Image.fromarray(canvas); d = ImageDraw.Draw(im)
for i,(label,img) in enumerate(panels):
    x = i*(cw+gap)
    im.paste(Image.fromarray(img[y0:y1, x0:x1]), (x, top))
    d.text((x+12, 20), label, fill=(255,255,255), font=font)
im.save(OUT/"banding_matrix.png")
print("saved", im.size)
