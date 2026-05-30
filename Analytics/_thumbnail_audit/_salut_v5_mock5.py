# -*- coding: utf-8 -*-
"""scratch v5 mock #5 — NoWM + 初音ミク / アカペラ 2줄·확대 (코튼 지정).
블록(위→아래): 初音ミク(大·틸) / アカペラ(大·틸) / Edward Elgar(소) / Salut d'Amour(hero).
워드마크 제거. id 사이즈 = 80."""
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

_probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
def didot(sz): return ImageFont.truetype(DIDOT, sz)
def mincho(sz): return ImageFont.truetype(MINCHO, sz, index=0)
def tw(t, f): return _probe.textlength(t, font=f)
def fit(text, maxw, start=112, lo=58):
    for sz in range(start, lo-1, -2):
        if tw(text, didot(sz)) <= maxw: return didot(sz)
    return didot(lo)

def sub_then_fill(img, b):
    x0, y0, x1, y1 = b
    sub = img.crop((int(x0*img.width), int(y0*img.height), int(x1*img.width), int(y1*img.height)))
    s = max(W/sub.width, H/sub.height)
    r = sub.resize((int(sub.width*s+0.5), int(sub.height*s+0.5)), Image.LANCZOS)
    x, y = (r.width-W)//2, (r.height-H)//2
    return r.crop((x, y, x+W, y+H))

def bottom_scrim(bg, start):
    ov = Image.new("RGBA", (W, H), (0,0,0,0)); od = ImageDraw.Draw(ov)
    for y in range(H):
        a = int(212 * max(0, (y-start)/(H-start)))
        od.line([(0,y),(W,y)], fill=(6,9,13,a))
    return Image.alpha_composite(bg.convert("RGBA"), ov).convert("RGB")

def tsh(d, xy, t, f, fill, off=4):
    x, y = xy
    d.text((x+off, y+off), t, font=f, fill=(0,0,0)); d.text((x,y), t, font=f, fill=fill)

def build(id_sz, tag):
    bg = sub_then_fill(Image.open(COVER).convert("RGB"), BOX)
    id_f, comp_f, big_f = mincho(id_sz), didot(44), fit(PIECE, W-150)
    mb = _probe.textbbox((0,0), "初音ミク", font=id_f)
    ab = _probe.textbbox((0,0), "アカペラ", font=id_f)
    cb = _probe.textbbox((0,0), COMPOSER, font=comp_f)
    pb = _probe.textbbox((0,0), PIECE, font=big_f)
    big_y = (H-34) - pb[3]
    comp_y = (big_y + pb[1]) - 12 - cb[3]
    aca_y = (comp_y + cb[1]) - 26 - ab[3]
    miku_y = (aca_y + ab[1]) - 8 - mb[3]
    bg = bottom_scrim(bg, max(250, miku_y - 38))
    d = ImageDraw.Draw(bg)
    tsh(d, (70, miku_y), "初音ミク", id_f, SOFT_TEAL)
    tsh(d, (70, aca_y), "アカペラ", id_f, SOFT_TEAL)
    tsh(d, (72, comp_y), COMPOSER, comp_f, (216,212,198))
    tsh(d, (66, big_y), PIECE, big_f, (255,255,255))
    out = OUT / f"_salut_v5_{tag}.jpg"
    bg.save(out, quality=92); print(tag, out)

if __name__ == "__main__":
    build(80, "2line_80")
    build(92, "2line_92")
