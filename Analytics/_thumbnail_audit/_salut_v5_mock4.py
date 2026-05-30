# -*- coding: utf-8 -*-
"""scratch v5 mock #4 — 텍스트를 *한 구역(좌하단)*으로 통합 (시선 분산 해소).
상단 텍스트/스크림 제거 → 회화·미쿠 얼굴은 위쪽서 숨 쉬고, 정보는 하단 한 블록.
운영 효율 = 기존 make_thumbnail의 하단 ink-bbox 스택에 ③ 한 줄만 더 얹는 구조.

블록 위계(위→아래): 初音ミク アカペラ(틸·③) / 작곡가(소) / 곡명(大 hero·②) / 워드마크(옵션)."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE = Path(r"C:\Users\user\Desktop\myProject\Project_Muse")
DIDOT = str(BASE / "assets/fonts/gfs_didot/GFSDidot-Regular.ttf")
MINCHO = r"C:\Windows\Fonts\yumindb.ttf"
COVER = BASE / "works/elgar_salut_damour/video/cover/Miku_waterhouse_soul_of_the_rose.png"
BOX = (0.00, 0.04, 1.00, 0.80)
COMPOSER, PIECE = "Edward Elgar", "Salut d'Amour"
OUT = Path(r"C:\Users\user\Desktop\myProject\Project_Muse\Analytics\_thumbnail_audit")
W, H = 1280, 720
SOFT_TEAL = (151, 214, 201)
WARM_WHITE = (236, 233, 224)

_probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
def didot(sz): return ImageFont.truetype(DIDOT, sz)
def mincho(sz): return ImageFont.truetype(MINCHO, sz, index=0)
def tw(t, f): return _probe.textlength(t, font=f)
def fit(text, maxw, start=118, lo=58):
    for sz in range(start, lo - 1, -2):
        if tw(text, didot(sz)) <= maxw:
            return didot(sz)
    return didot(lo)

def sub_then_fill(img, b):
    x0, y0, x1, y1 = b
    sub = img.crop((int(x0*img.width), int(y0*img.height), int(x1*img.width), int(y1*img.height)))
    s = max(W/sub.width, H/sub.height)
    r = sub.resize((int(sub.width*s+0.5), int(sub.height*s+0.5)), Image.LANCZOS)
    x, y = (r.width-W)//2, (r.height-H)//2
    return r.crop((x, y, x+W, y+H))

def bottom_scrim(bg, start):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    for y in range(H):
        a = int(210 * max(0, (y-start)/(H-start)))
        od.line([(0, y), (W, y)], fill=(6, 9, 13, a))
    return Image.alpha_composite(bg.convert("RGBA"), ov).convert("RGB")

def tsh(d, xy, t, f, fill, off=4):
    x, y = xy
    d.text((x+off, y+off), t, font=f, fill=(0, 0, 0))
    d.text((x, y), t, font=f, fill=fill)

def wordmark(d, x, y, sz=36):
    f = didot(sz)
    for t, c in [("Atelier ", WARM_WHITE), ("M", (120, 224, 224)), ("iku Acappella", WARM_WHITE)]:
        d.text((x+2, y+2), t, font=f, fill=(0, 0, 0)); d.text((x, y), t, font=f, fill=c)
        x += tw(t, f)

def build(with_wm, tag):
    bg = sub_then_fill(Image.open(COVER).convert("RGB"), BOX)
    id_f, comp_f, big_f, wm_f = mincho(50), didot(44), fit(PIECE, W-150), didot(36)
    idt = "初音ミク  アカペラ"
    ib = _probe.textbbox((0,0), idt, font=id_f)
    cb = _probe.textbbox((0,0), COMPOSER, font=comp_f)
    pb = _probe.textbbox((0,0), PIECE, font=big_f)
    wb = _probe.textbbox((0,0), "Atelier Miku Acappella", font=wm_f)
    G = 16
    # 아래→위 스택
    if with_wm:
        wm_y = (H-28) - wb[3]
        big_y = (wm_y + wb[1]) - G - pb[3]
    else:
        big_y = (H-30) - pb[3]
    comp_y = (big_y + pb[1]) - 10 - cb[3]
    id_y = (comp_y + cb[1]) - 20 - ib[3]
    scrim_start = id_y - 40
    bg = bottom_scrim(bg, max(280, scrim_start))
    d = ImageDraw.Draw(bg)
    tsh(d, (70, id_y), idt, id_f, SOFT_TEAL)          # ③ 미쿠+아카펠라 (틸)
    tsh(d, (72, comp_y), COMPOSER, comp_f, (216,212,198))
    tsh(d, (66, big_y), PIECE, big_f, (255,255,255))
    if with_wm:
        wordmark(d, 72, wm_y)
    out = OUT / f"_salut_v5_{tag}.jpg"
    bg.save(out, quality=92); print(tag, out)

if __name__ == "__main__":
    build(True, "unified_wm")
    build(False, "unified_nowm")
