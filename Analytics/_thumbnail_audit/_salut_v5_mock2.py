# -*- coding: utf-8 -*-
"""scratch v5 mock #2 — 初音ミク 마크를 *아래 Didot와 조화*되게 재설계.
- 폰트: Yu Mincho (明朝 세리프) → 아래 Didot 세리프와 같은 결 (gothic 클릭베이트 X)
- 처리: 두꺼운 외곽선 제거 → 아래 텍스트와 동일한 *은은한 그림자*
- 가독: 두꺼운 stroke 대신 *상단 스크림*(아래 스크림의 거울상)으로 확보
- 팔레트: 회화의 뮤트톤에 맞춘 warm-white / soft-teal 2안
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

V4 = Path(r"C:\Users\user\Desktop\myProject\Project_Muse\works\elgar_salut_damour\video\thumbnail_v4.jpg")
MINCHO = r"C:\Windows\Fonts\yumindb.ttf"   # Yu Mincho Demibold (우아한 세리프 · 가독 weight)
OUT = Path(r"C:\Users\user\Desktop\myProject\Project_Muse\Analytics\_thumbnail_audit")
W, H = 1280, 720

WARM_WHITE = (236, 233, 224)
SOFT_TEAL  = (151, 214, 201)

def jp(sz): return ImageFont.truetype(MINCHO, sz, index=0)

def top_scrim(img, end=250, amax=165):
    """상단에서 아래로 사라지는 어두운 그라데이션 (하단 스크림의 거울상)."""
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    for y in range(H):
        a = int(amax * max(0, (end - y) / end))
        od.line([(0, y), (W, y)], fill=(6, 9, 13, a))
    return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")

def soft(d, xy, t, f, fill, off=4):
    x, y = xy
    d.text((x + off, y + off), t, font=f, fill=(0, 0, 0))   # 은은한 그림자 (아래 텍스트와 동일 결)
    d.text((x, y), t, font=f, fill=fill)

def build(fill, tag):
    img = top_scrim(Image.open(V4).convert("RGB"))
    d = ImageDraw.Draw(img)
    soft(d, (54, 30), "初音ミク", jp(118), fill)
    out = OUT / f"_salut_v5_{tag}.jpg"
    img.save(out, quality=92)
    print(tag, out)

if __name__ == "__main__":
    build(WARM_WHITE, "mincho_white")
    build(SOFT_TEAL,  "mincho_teal")
