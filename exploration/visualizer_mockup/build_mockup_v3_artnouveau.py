# -*- coding: utf-8 -*-
"""
Project Muse — v3 "Art Nouveau Ensemble" mockup (s356, Gemini-direction, MOKA-filtered).
Hero arched panel (per-song painting + Miku, ~52% width) + 6 stained-glass voice panels
(glow per active part) + paper-texture overlay + GFS Didot / cream / teal.
Hero Miku = placeholder (current cover); real version = official Miku art.
"""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = r"C:/Users/user/Desktop/myProject/Project_Muse"
FONT = BASE + "/assets/fonts/gfs_didot/GFSDidot-Regular.ttf"
COVER = BASE + "/works/vivaldi_spring_1_allegro/video/visualizer/public/cover.png"
OUT_DIR = BASE + "/exploration/visualizer_mockup"
os.makedirs(OUT_DIR, exist_ok=True)
OUT = OUT_DIR + "/artnouveau_ensemble_v3.png"

W, H = 1920, 1080
CREAM = (232, 224, 200)
TEAL = (40, 180, 175)
GOLD = (201, 169, 106)
MUTED = (140, 138, 146)

def font(sz):
    return ImageFont.truetype(FONT, sz)

# ---------- palette from painting ----------
cov_full = Image.open(COVER).convert("RGB")
small = np.asarray(cov_full.resize((90, 90))).reshape(-1, 3).astype(float)
lum = small @ np.array([0.299, 0.587, 0.114])
order = np.argsort(lum)
dark = small[order[: len(order)//4]].mean(0)
mid = small[order[len(order)//2-250: len(order)//2+250]].mean(0)
def cap(c, mx, fl=8):
    c = np.array(c, float); m = c.max()
    if m > mx: c = c*(mx/m)
    return np.clip(c, fl, 255)
g_dark, g_mid, g_acc = cap(dark, 52), cap(mid, 92), cap(dark*0.8+mid*0.2, 64)

# gradient bg
yy, xx = np.mgrid[0:H, 0:W]
t = (((xx/W)+(yy/H))/2.0)[..., None]
bg = np.where(t < 0.5, g_dark+(g_mid-g_dark)*(t/0.5), g_mid+(g_acc-g_mid)*((t-0.5)/0.5))
img = Image.fromarray(np.clip(bg, 0, 255).astype("uint8")).convert("RGBA")

def D():
    return ImageDraw.Draw(img)

# ---------- HERO arched panel ----------
ax0, ay0, ax1, ay1 = 70, 96, 1060, 1004
r = (ax1-ax0)/2
spring = ay0 + r
cx = (ax0+ax1)/2

# fill = cover, cropped to arch bbox aspect
bb_w, bb_h = ax1-ax0, ay1-ay0
cv = Image.open(COVER).convert("RGB")
s = max(bb_w/cv.width, bb_h/cv.height)
cv = cv.resize((int(cv.width*s), int(cv.height*s)), Image.LANCZOS)
l = (cv.width-bb_w)//2; tp = (cv.height-bb_h)//2
cv = cv.crop((l, tp, l+bb_w, tp+bb_h))
# arch mask
mask = Image.new("L", (W, H), 0)
md = ImageDraw.Draw(mask)
md.rectangle([ax0, spring, ax1, ay1], fill=255)
md.ellipse([ax0, ay0, ax1, ay0+2*r], fill=255)
cv_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cv_layer.paste(cv, (ax0, ay0))
img.paste(cv_layer, (0, 0), mask)

# gold double border on arch
d = D()
for off, wd in ((0, 5), (13, 2)):
    d.line([(ax0+off, spring), (ax0+off, ay1-off)], fill=GOLD+(235,), width=wd)
    d.line([(ax1-off, spring), (ax1-off, ay1-off)], fill=GOLD+(235,), width=wd)
    d.line([(ax0+off, ay1-off), (ax1-off, ay1-off)], fill=GOLD+(235,), width=wd)
    d.arc([ax0+off, ay0+off, ax1-off, ay0+2*r-off], 180, 360, fill=GOLD+(235,), width=wd)

# simple Art-Nouveau flourishes (springline curls + apex motif)
def curl(cxp, cyp, sgn, scale=1.0):
    bb = 34*scale
    d.arc([cxp-bb, cyp-bb, cxp+bb, cyp+bb], 0 if sgn > 0 else 90, 110 if sgn > 0 else 200,
          fill=GOLD+(220,), width=3)
    d.arc([cxp-bb*0.5, cyp-bb*0.5, cxp+bb*0.5, cyp+bb*0.5], 200, 360,
          fill=GOLD+(180,), width=2)
curl(ax0+8, spring, +1); curl(ax1-8, spring, -1)
# apex small lily motif
d.ellipse([cx-5, ay0+22, cx+5, ay0+34], outline=GOLD+(220,), width=2)
d.line([(cx, ay0+34), (cx, ay0+60)], fill=GOLD+(200,), width=2)
d.arc([cx-22, ay0+30, cx, ay0+62], 270, 360, fill=GOLD+(180,), width=2)
d.arc([cx, ay0+30, cx+22, ay0+62], 180, 270, fill=GOLD+(180,), width=2)

# ---------- 6 stained-glass voice panels (2 col x 3 row) ----------
roles = [
    ("I", "Ah", (216, 184, 120), True),
    ("II", "Ah", (201, 143, 143), False),
    ("III", "Oo", (95, 185, 179), True),
    ("IV", "Oo", (159, 185, 143), False),
    ("V", "Oo", (210, 160, 96), True),
    ("VI", "Mm", (176, 168, 196), True),
]
gx0, gy0 = 1120, 118
cw, ch, gap = 348, 232, 26
f_num, f_vow, f_mk = font(40), font(18), font(15)
for i, (num, vowel, color, active) in enumerate(roles):
    cxx = i % 2
    ryy = i // 2
    x0 = gx0 + cxx*(cw+gap)
    y0 = gy0 + ryy*(ch+gap)
    x1, y1 = x0+cw, y0+ch
    # glass fill (glow if active)
    a_fill = 150 if active else 55
    gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gl)
    gd.rounded_rectangle([x0, y0, x1, y1], radius=8, fill=color+(a_fill,))
    if active:
        glow = gl.filter(ImageFilter.GaussianBlur(18))
        img.alpha_composite(glow)
    img.alpha_composite(gl)
    d = D()
    # lead-came border (dark) + gold inner line
    d.rounded_rectangle([x0, y0, x1, y1], radius=8, outline=(20, 18, 16, 235), width=6)
    d.rounded_rectangle([x0+6, y0+6, x1-6, y1-6], radius=6,
                        outline=(GOLD if active else MUTED)+(210,), width=2)
    # placeholder Miku mark (teal twin-tail suggestion) + numeral
    mcx, mcy = (x0+x1)/2, (y0+y1)/2
    tcol = (CREAM if active else MUTED)
    nn = d.textlength(num, font=f_num)
    d.text((mcx-nn/2, mcy-34), num, font=f_num, fill=tcol+(255,))
    vw = d.textlength(vowel, font=f_vow)
    d.text((mcx-vw/2, mcy+18), vowel, font=f_vow, fill=(TEAL if active else MUTED)+(220,))
    mk = "MIKU"
    mw = d.textlength(mk, font=f_mk)
    d.text((mcx-mw/2, y0+12), mk, font=f_mk, fill=tcol+(180,))

# ---------- title + wordmark (bottom-right) ----------
d = D()
f_wm = font(28)
parts = [("Atelier ", CREAM), ("M", TEAL), ("iku Acappella", CREAM)]
total = sum(d.textlength(t, font=f_wm) for t, _ in parts)
RXR = gx0 + 2*cw + gap  # right edge of panel grid
wx, wy = RXR-total, 40
for t, c in parts:
    d.text((wx, wy), t, font=f_wm, fill=c+(240,)); wx += d.textlength(t, font=f_wm)
d.line([(RXR-total, wy+40), (RXR, wy+40)], fill=GOLD+(150,), width=1)
# title
ty = 900
d.text((gx0, ty), "Antonio Vivaldi", font=font(44), fill=CREAM+(255,))
d.text((gx0, ty+58), "Spring — I. Allegro", font=font(30), fill=CREAM+(225,))
fx = gx0
d.text((fx, ty+102), "from The Four Seasons (1725)  ·  feat. ", font=font(20), fill=CREAM+(165,))
fx += d.textlength("from The Four Seasons (1725)  ·  feat. ", font=font(20))
d.text((fx, ty+102), "Hatsune Miku", font=font(20), fill=TEAL+(230,))

# ---------- paper texture overlay (multiply) ----------
base = img.convert("RGB")
arr = np.asarray(base).astype(float)
noise = Image.effect_noise((W, H), 30).filter(ImageFilter.GaussianBlur(0.6))
low = Image.effect_noise((W, H), 18).resize((W//6, H//6)).resize((W, H)).filter(ImageFilter.GaussianBlur(2))
n = (np.asarray(noise).astype(float) + np.asarray(low).astype(float)) / 2.0
mult = 0.88 + 0.20*(n/255.0)            # ~0.88..1.08 grain
out = np.clip(arr * mult[..., None], 0, 255)
# faint warm paper tint
out[..., 0] = np.clip(out[..., 0]*1.012, 0, 255)
out[..., 2] = np.clip(out[..., 2]*0.99, 0, 255)
Image.fromarray(out.astype("uint8")).save(OUT, "PNG")
print("saved:", OUT)
