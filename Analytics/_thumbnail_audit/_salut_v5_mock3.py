# -*- coding: utf-8 -*-
"""scratch v5 mock #3 — 코튼의 3-정보 스펙 충족.
정보 ③ = '하츠네 미쿠가 A Cappella한 곡' → 初音ミク + アカペラ 둘 다 (Mincho 코히전 유지).
정보 ② = 악곡(아래 Didot) 유지 · 정보 ① = 명화 배경 유지.
JP 인식 = 상단 初音ミク アカペラ(가나·한자) / EN 측 = 하단 워드마크 'Atelier Miku Acappella'가 커버."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

V4 = Path(r"C:\Users\user\Desktop\myProject\Project_Muse\works\elgar_salut_damour\video\thumbnail_v4.jpg")
MINCHO = r"C:\Windows\Fonts\yumindb.ttf"
OUT = Path(r"C:\Users\user\Desktop\myProject\Project_Muse\Analytics\_thumbnail_audit")
W, H = 1280, 720
WARM_WHITE = (236, 233, 224)
SOFT_TEAL  = (151, 214, 201)

def jp(sz): return ImageFont.truetype(MINCHO, sz, index=0)

def top_scrim(img, end=300, amax=170):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    for y in range(H):
        a = int(amax * max(0, (end - y) / end))
        od.line([(0, y), (W, y)], fill=(6, 9, 13, a))
    return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")

def soft(d, xy, t, f, fill, off=4):
    x, y = xy
    d.text((x + off, y + off), t, font=f, fill=(0, 0, 0))
    d.text((x, y), t, font=f, fill=fill)

def build(miku_fill, aca_fill, tag):
    img = top_scrim(Image.open(V4).convert("RGB"))
    d = ImageDraw.Draw(img)
    soft(d, (54, 26), "初音ミク", jp(112), miku_fill)         # ③ who
    soft(d, (58, 26 + 122), "アカペラ", jp(58), aca_fill)      # ③ format
    out = OUT / f"_salut_v5_{tag}.jpg"
    img.save(out, quality=92)
    print(tag, out)

if __name__ == "__main__":
    build(WARM_WHITE, WARM_WHITE, "info3_white")
    build(SOFT_TEAL,  WARM_WHITE, "info3_teal")   # 初音ミク=틸 accent · アカペラ=흰
