"""
Banding vs dither test (scratch · s-current 2026-06-22).
실제 letterbox 그라디언트를 한 프레임으로 재현 → H.264 한 프레임 인코딩을 통과시켜
'현재(노이즈 없음)' vs '미세 노이즈 디더' 를 좌/우로 비교한 PNG 한 장 생성.
"""
import subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 2560, 1440
OUT = Path(__file__).parent
FFMPEG = r"C:\Users\user\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffmpeg.exe"

# ⑩ 헨델 무채 ivory — 밴딩 최악 케이스
STOPS = ["#181614", "#6F6A60", "#D8D2C4"]
DITHER_AMP = 2.5   # ±2.5 LSB triangular ≈ 1% 그레인 (인코딩 통과 목적)

def hexrgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i+2], 16) for i in (0, 2, 4)], dtype=np.float64)

def gradient_float():
    c0, c1, c2 = (hexrgb(s) for s in STOPS)
    t = np.linspace(0.0, 1.0, H)            # 세로 위치 0..1 (180deg)
    col = np.empty((H, 3), np.float64)
    lower = t <= 0.5
    a = (t[lower] / 0.5)[:, None]
    col[lower] = c0 * (1 - a) + c1 * a
    a = ((t[~lower] - 0.5) / 0.5)[:, None]
    col[~lower] = c1 * (1 - a) + c2 * a
    return np.repeat(col[:, None, :], W, axis=1)   # (H,W,3)

def to8(arr):
    return np.clip(np.round(arr), 0, 255).astype(np.uint8)

def triangular_noise(shape, amp):
    # triangular PDF (두 uniform의 합) = 정석 디더 노이즈
    rng = np.random.default_rng(7)
    return (rng.random(shape) - rng.random(shape)) * amp

def h264_roundtrip(img_u8, tag):
    """PNG → H.264 단일프레임(yuv420p) → PNG 추출. 압축 밴딩 증폭 재현."""
    src = OUT / f"_src_{tag}.png"
    mp4 = OUT / f"_enc_{tag}.mp4"
    dec = OUT / f"_dec_{tag}.png"
    Image.fromarray(img_u8).save(src)
    subprocess.run([FFMPEG, "-y", "-loop", "1", "-i", str(src), "-frames:v", "1",
                    "-c:v", "libx264", "-crf", "23", "-pix_fmt", "yuv420p",
                    str(mp4)], check=True, capture_output=True)
    subprocess.run([FFMPEG, "-y", "-i", str(mp4), "-frames:v", "1", str(dec)],
                   check=True, capture_output=True)
    return np.array(Image.open(dec).convert("RGB"))

grad = gradient_float()
plain   = to8(grad)
dithered = to8(grad + triangular_noise(grad.shape, DITHER_AMP))

A = h264_roundtrip(plain, "plain")       # 현재
B = h264_roundtrip(dithered, "dither")   # 디더

# 좌측 절반 = A, 우측 절반 = B (같은 세로위치 비교)
half = W // 2
combo = np.empty((H, W, 3), np.uint8)
combo[:, :half] = A[:, :half]
combo[:, half:] = B[:, half:]

im = Image.fromarray(combo)
d = ImageDraw.Draw(im)
d.line([(half, 0), (half, H)], fill=(255, 80, 80), width=3)
try:
    font = ImageFont.truetype(r"C:\Windows\Fonts\malgunbd.ttf", 46)
except Exception:
    font = ImageFont.load_default()
def label(x, txt):
    tw = d.textbbox((0, 0), txt, font=font)[2]
    d.rectangle([x, 24, x + tw + 36, 92], fill=(0, 0, 0))
    d.text((x + 18, 32), txt, fill=(255, 255, 255), font=font)
label(40, "현재 (노이즈 없음)")
label(half + 40, "미세 노이즈 디더")

out = OUT / "banding_compare.png"
im.save(out)
print("saved", out)
