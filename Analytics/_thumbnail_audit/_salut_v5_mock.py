# -*- coding: utf-8 -*-
"""scratch: v5 썸네일 mockup — 初音ミク 마크 오버레이 (salut · 코튼 승인용).
현 thumbnail_v4.jpg 위에 大 初音ミク 마크를 얹어 before/after를 즉시 비교.
승인되면 make_thumbnail.py 본체에 정식 흡수."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

V4 = Path(r"C:\Users\user\Desktop\myProject\Project_Muse\works\elgar_salut_damour\video\thumbnail_v4.jpg")
JP_FONT = r"C:\Windows\Fonts\YuGothB.ttc"   # Yu Gothic Bold (가나·한자 OK)
OUT = Path(r"C:\Users\user\Desktop\myProject\Project_Muse\Analytics\_thumbnail_audit")

TEAL = (84, 226, 214)     # 미쿠 시그니처 틸
DARK = (8, 10, 14)

def jp(sz):
    return ImageFont.truetype(JP_FONT, sz, index=0)

def mark(d, xy, text, sz, fill=TEAL, stroke=10):
    x, y = xy
    f = jp(sz)
    # 깊이용 그림자 + 굵은 외곽선 → 회화 위에서도 또렷
    d.text((x + 6, y + 7), text, font=f, fill=DARK, stroke_width=stroke, stroke_fill=DARK)
    d.text((x, y), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=DARK)
    return f

def variant_a():
    img = Image.open(V4).convert("RGB")
    d = ImageDraw.Draw(img)
    mark(d, (52, 34), "初音ミク", 132)
    out = OUT / "_salut_v5a_miku.jpg"
    img.save(out, quality=92)
    print("A", out)

def variant_b():
    img = Image.open(V4).convert("RGB")
    d = ImageDraw.Draw(img)
    f = mark(d, (52, 34), "初音ミク", 132)
    # 아카펠라 보조(작게) — 初音ミク 바로 아래
    w = d.textlength("初音ミク", font=f)
    mark(d, (56, 34 + 150), "アカペラ", 64, fill=(238, 236, 228), stroke=7)
    out = OUT / "_salut_v5b_miku_acappella.jpg"
    img.save(out, quality=92)
    print("B", out)

if __name__ == "__main__":
    variant_a()
    variant_b()
