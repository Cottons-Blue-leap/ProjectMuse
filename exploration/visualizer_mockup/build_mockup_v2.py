# -*- coding: utf-8 -*-
"""
Project Muse — "note-scroll" visualizer mockup v2 (s356).
Change from v1: background no longer the dim painting. Two variants:
  v2a = 3-color gradient derived from the painting palette (per-song variation, ties to our letterbox-gradient signature)
  v2b = single solid color derived from the painting
Painting now appears ONLY in the cover panel (no redundancy). Everything else identical to v1.
Tone: GFS Didot, cream #e8e0c8, Miku teal, minimal, no DAW chrome.
"""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = r"C:/Users/user/Desktop/myProject/Project_Muse"
FONT = BASE + "/assets/fonts/gfs_didot/GFSDidot-Regular.ttf"
COVER = BASE + "/works/vivaldi_spring_1_allegro/video/visualizer/public/cover.png"
OUT_DIR = BASE + "/exploration/visualizer_mockup"
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 1920, 1080
CREAM = (232, 224, 200)
TEAL = (40, 180, 175)
MUTED = (150, 150, 158)

def font(sz):
    return ImageFont.truetype(FONT, sz)

# ---------- derive palette from painting ----------
cov_full = Image.open(COVER).convert("RGB")
small = np.asarray(cov_full.resize((90, 90))).reshape(-1, 3).astype(float)
lum = small @ np.array([0.299, 0.587, 0.114])
order = np.argsort(lum)
dark = small[order[: len(order) // 4]].mean(0)
mid = small[order[len(order) // 2 - 250: len(order) // 2 + 250]].mean(0)
mx = small.max(1); mn = small.min(1); sat = (mx - mn) / (mx + 1e-6)
accent = small[np.argsort(sat)[-60:]].mean(0)

def cap(c, maxv, floor=8):
    c = np.array(c, float)
    m = c.max()
    if m > maxv:
        c = c * (maxv / m)
    c = np.clip(c, floor, 255)
    return c

g_dark = cap(dark, 60)
g_mid = cap(mid, 104)
g_acc = cap(accent, 78)
g_solid = cap(mid * 0.6 + dark * 0.4, 40)

def gradient_bg():
    yy, xx = np.mgrid[0:H, 0:W]
    t = ((xx / W) + (yy / H)) / 2.0
    t = t[..., None]
    out = np.where(t < 0.5,
                   g_dark + (g_mid - g_dark) * (t / 0.5),
                   g_mid + (g_acc - g_mid) * ((t - 0.5) / 0.5))
    return Image.fromarray(np.clip(out, 0, 255).astype("uint8"), "RGB")

def solid_bg():
    return Image.new("RGB", (W, H), tuple(int(v) for v in g_solid))

# ---------- geometry / data ----------
LANE_X0, LANE_X1 = 28, 158
NF_X0, NF_X1 = 158, 1180
PLAYHEAD = NF_X0 + 6
TOP, BOT = 70, 858
N = 6
lane_h = (BOT - TOP) / N
VIS_Y0, VIS_Y1 = 906, 1052
RX0, RX1 = 1232, 1892

roles = [
    ("I",   "Ah", (216, 184, 120), [(158, 478)]),
    ("II",  "Ah", (201, 143, 143), [(330, 612)]),
    ("III", "Oo", (95, 185, 179),  [(158, 422)]),
    ("IV",  "Oo", (159, 185, 143), [(556, 868)]),
    ("V",   "Oo", (210, 160, 96),  [(158, 470)]),
    ("VI",  "Mm", (176, 168, 196), [(158, 292), (356, 520), (602, 818)]),
]

def lane_cy(i):
    return TOP + lane_h * (i + 0.5)

def render(bg, out_name):
    img = bg.convert("RGBA")

    def D():
        return ImageDraw.Draw(img)

    def soft_bar(x0, x1, cy, color, active):
        h = 16 if active else 13
        y0, y1 = cy - h / 2, cy + h / 2
        r = h / 2
        gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(gl).rounded_rectangle([x0 - 6, y0 - 6, x1 + 6, y1 + 6],
                                             radius=r + 6,
                                             fill=color + (150 if active else 70,))
        img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(13 if active else 8)))
        cl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(cl).rounded_rectangle([x0, y0, x1, y1], radius=r,
                                             fill=color + (240 if active else 95,))
        img.alpha_composite(cl)

    # lanes
    for i, (num, vowel, color, notes) in enumerate(roles):
        cy = lane_cy(i)
        d = D()
        x = NF_X0
        while x < NF_X1:
            d.line([(x, cy), (min(x + 16, NF_X1), cy)],
                   fill=(232, 224, 200, 34), width=1)
            x += 30
        for (x0, x1) in notes:
            active = any(a <= PLAYHEAD + 6 <= b for (a, b) in notes)
            soft_bar(x0, x1, cy, color, active)

    # playhead
    ph = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(ph).line([(PLAYHEAD, TOP - 6), (PLAYHEAD, BOT + 6)],
                            fill=TEAL + (130,), width=3)
    img.alpha_composite(ph.filter(ImageFilter.GaussianBlur(5)))
    D().line([(PLAYHEAD, TOP - 6), (PLAYHEAD, BOT + 6)], fill=TEAL + (210,), width=1)

    # Miku lane labels
    f_mini, f_num, f_vow = font(15), font(30), font(16)
    for i, (num, vowel, color, notes) in enumerate(roles):
        cy = lane_cy(i)
        active = any(a <= PLAYHEAD + 6 <= b for (a, b) in notes)
        bx0, by0, bx1, by1 = LANE_X0, cy - lane_h / 2 + 8, LANE_X1 - 8, cy + lane_h / 2 - 8
        if active:
            gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(gl).rounded_rectangle([bx0, by0, bx1, by1], radius=10,
                                                 fill=TEAL + (60,))
            img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(10)))
        d = D()
        bcol = TEAL if active else MUTED
        d.rounded_rectangle([bx0, by0, bx1, by1], radius=10, outline=bcol + (235,),
                            width=2)
        cxm = (bx0 + bx1) / 2
        tw = d.textlength("MIKU", font=f_mini)
        d.text((cxm - tw / 2, by0 + 9), "MIKU", font=f_mini,
               fill=(CREAM if active else MUTED) + (235,))
        tw = d.textlength(num, font=f_num)
        d.text((cxm - tw / 2, by0 + 27), num, font=f_num,
               fill=(CREAM if active else MUTED) + (255,))
        tw = d.textlength(vowel, font=f_vow)
        d.text((cxm - tw / 2, by1 - 26), vowel, font=f_vow,
               fill=(TEAL if active else MUTED) + (220,))

    # audio visualizer
    d = D()
    bars = 72
    bw = (NF_X1 - NF_X0) / bars
    midy = (VIS_Y0 + VIS_Y1) / 2
    for b in range(bars):
        t = b / bars
        amp = 0.35 + 0.65 * abs(math.sin(t * 9.0)) * (0.5 + 0.5 * math.sin(t * 2.3 + 1))
        hh = amp * (VIS_Y1 - VIS_Y0) * 0.46
        x = NF_X0 + b * bw + bw * 0.28
        col = TEAL if b % 6 == 0 else CREAM
        a = 150 if b % 6 == 0 else 95
        d.rounded_rectangle([x, midy - hh, x + bw * 0.44, midy + hh], radius=2,
                            fill=col + (a,))

    # wordmark
    d = D()
    f_wm = font(30)
    parts = [("Atelier ", CREAM), ("M", TEAL), ("iku Acappella", CREAM)]
    total = sum(d.textlength(t, font=f_wm) for t, _ in parts)
    wx, wy = RX1 - total, 34
    for t, c in parts:
        d.text((wx, wy), t, font=f_wm, fill=c + (240,))
        wx += d.textlength(t, font=f_wm)
    d.line([(RX1 - total, wy + 44), (RX1, wy + 44)], fill=CREAM + (70,), width=1)

    # title
    ty = 150
    d.text((RX0, ty), "Antonio Vivaldi", font=font(46), fill=CREAM + (255,))
    d.text((RX0, ty + 64), "Spring — I. Allegro", font=font(34), fill=CREAM + (235,))
    d.text((RX0, ty + 112), "from  The Four Seasons  (1725)", font=font(22),
           fill=CREAM + (170,))
    fx = RX0
    d.text((fx, ty + 152), "feat. ", font=font(24), fill=CREAM + (200,))
    fx += d.textlength("feat. ", font=font(24))
    d.text((fx, ty + 152), "Hatsune Miku", font=font(24), fill=TEAL + (235,))

    # cover panel
    cs = 612
    cv = Image.open(COVER).convert("RGB")
    s = max(cs / cv.width, cs / cv.height)
    cv = cv.resize((int(cv.width * s), int(cv.height * s)), Image.LANCZOS)
    l = (cv.width - cs) // 2; t = (cv.height - cs) // 2
    cv = cv.crop((l, t, l + cs, t + cs))
    cxp, cyp = RX1 - cs, H - cs - 56
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle([cxp - 10, cyp - 10, cxp + cs + 10, cyp + cs + 10],
                                 fill=(0, 0, 0, 150))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)))
    img.paste(cv, (cxp, cyp))
    D().rectangle([cxp, cyp, cxp + cs, cyp + cs], outline=CREAM + (180,), width=2)

    out = OUT_DIR + "/" + out_name
    img.convert("RGB").save(out, "PNG")
    print("saved:", out)

render(gradient_bg(), "singing_painting_v2a_gradient.png")
render(solid_bg(), "singing_painting_v2b_solid.png")
print("gradient stops:", g_dark.astype(int), g_mid.astype(int), g_acc.astype(int))
print("solid:", g_solid.astype(int))
