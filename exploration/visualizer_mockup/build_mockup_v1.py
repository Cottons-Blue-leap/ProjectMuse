# -*- coding: utf-8 -*-
"""
Project Muse — "Singing Painting" visualizer UI mockup (static, v1).
Layout from 코튼 wireframe (s356): left Miku lanes + leftward note scroll,
right cover/title overlay + top-right wordmark + bottom audio visualizer.
Tone & manner: GFS Didot, cream #e8e0c8, Miku teal, masterpiece backdrop, no DAW chrome.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

BASE = r"C:/Users/user/Desktop/myProject/Project_Muse"
FONT = BASE + "/assets/fonts/gfs_didot/GFSDidot-Regular.ttf"
COVER = BASE + "/works/vivaldi_spring_1_allegro/video/visualizer/public/cover.png"
OUT_DIR = BASE + "/exploration/visualizer_mockup"
os.makedirs(OUT_DIR, exist_ok=True)
OUT = OUT_DIR + "/singing_painting_v1.png"

W, H = 1920, 1080
CREAM = (232, 224, 200)
CREAM_DIM = (232, 224, 200, 90)
TEAL = (40, 180, 175)
MUTED = (150, 150, 158)

def font(sz):
    return ImageFont.truetype(FONT, sz)

# ---------- base + masterpiece backdrop ("singing painting") ----------
img = Image.new("RGB", (W, H), (18, 16, 14))
cov = Image.open(COVER).convert("RGB")
# fill 16:9 backdrop from the painting (center-crop)
cr = cov.copy()
scale = max(W / cr.width, H / cr.height)
cr = cr.resize((int(cr.width * scale), int(cr.height * scale)), Image.LANCZOS)
left = (cr.width - W) // 2
top = (cr.height - H) // 2
cr = cr.crop((left, top, left + W, top + H))
cr = ImageEnhance.Color(cr).enhance(0.55)        # desaturate
cr = ImageEnhance.Brightness(cr).enhance(0.32)   # dim (dark gallery)
cr = cr.filter(ImageFilter.GaussianBlur(7))
img.paste(cr, (0, 0))

# warm dark vignette / gradient so notes & text pop
ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(ov)
for y in range(H):  # top->bottom subtle darken
    a = int(60 * (y / H))
    od.line([(0, y), (W, y)], fill=(10, 8, 6, a))
# left side (note field) extra darken for legibility
for x in range(W):
    a = int(70 * max(0, (1 - x / 1240)))
    od.line([(x, 0), (x, H)], fill=(8, 7, 6, a))
img = Image.alpha_composite(img.convert("RGBA"), ov)

draw = ImageDraw.Draw(img)

# ---------- geometry ----------
LANE_X0, LANE_X1 = 28, 158      # Miku label column
NF_X0, NF_X1 = 158, 1180        # note field
PLAYHEAD = NF_X0 + 6
TOP, BOT = 70, 858              # lane band
N = 6
lane_h = (BOT - TOP) / N
VIS_Y0, VIS_Y1 = 906, 1052      # audio visualizer band

# role palette + frozen note data (note-field coords) + label vowel
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

def soft_bar(x0, x1, cy, color, active):
    h = 16 if active else 13
    y0, y1 = cy - h / 2, cy + h / 2
    r = h / 2
    # glow
    gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gl)
    ga = 150 if active else 70
    gd.rounded_rectangle([x0 - 6, y0 - 6, x1 + 6, y1 + 6], radius=r + 6,
                         fill=color + (ga,))
    gl = gl.filter(ImageFilter.GaussianBlur(13 if active else 8))
    img.alpha_composite(gl)
    # core
    cl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(cl)
    ca = 240 if active else 95
    cd.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=color + (ca,))
    img.alpha_composite(cl)

# need a persistent draw after composites
def D():
    return ImageDraw.Draw(img)

# ---------- lanes: dashed guide + notes ----------
for i, (num, vowel, color, notes) in enumerate(roles):
    cy = lane_cy(i)
    active = any(x0 <= PLAYHEAD + 40 for (x0, x1) in notes) and len(notes) > 0 and \
             any(x0 <= PLAYHEAD + 6 <= x1 for (x0, x1) in notes)
    # dashed guide line
    d = D()
    x = NF_X0
    while x < NF_X1:
        d.line([(x, cy), (min(x + 16, NF_X1), cy)], fill=(232, 224, 200, 38), width=1)
        x += 30
    for (x0, x1) in notes:
        soft_bar(x0, x1, cy, color, active)

# ---------- playhead (soft vertical "now" line) ----------
ph = Image.new("RGBA", (W, H), (0, 0, 0, 0))
pd = ImageDraw.Draw(ph)
pd.line([(PLAYHEAD, TOP - 6), (PLAYHEAD, BOT + 6)], fill=TEAL + (120,), width=2)
ph = ph.filter(ImageFilter.GaussianBlur(4))
img.alpha_composite(ph)
D().line([(PLAYHEAD, TOP - 6), (PLAYHEAD, BOT + 6)], fill=TEAL + (200,), width=1)

# ---------- Miku lane labels ----------
f_mini = font(15)
f_num = font(30)
f_vow = font(16)
for i, (num, vowel, color, notes) in enumerate(roles):
    cy = lane_cy(i)
    active = any(x0 <= PLAYHEAD + 6 <= x1 for (x0, x1) in notes)
    bx0, by0, bx1, by1 = LANE_X0, cy - lane_h / 2 + 8, LANE_X1 - 8, cy + lane_h / 2 - 8
    d = D()
    # frame
    bcol = TEAL if active else MUTED
    if active:
        gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(gl).rounded_rectangle([bx0, by0, bx1, by1], radius=10,
                                             fill=TEAL + (55,))
        img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(10)))
    d = D()
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=10, outline=bcol + (235,),
                        width=2)
    cxm = (bx0 + bx1) / 2
    txt = "MIKU"
    tw = d.textlength(txt, font=f_mini)
    d.text((cxm - tw / 2, by0 + 9), txt, font=f_mini,
           fill=(CREAM if active else MUTED) + (235,))
    tw = d.textlength(num, font=f_num)
    d.text((cxm - tw / 2, by0 + 27), num, font=f_num,
           fill=(CREAM if active else MUTED) + (255,))
    tw = d.textlength(vowel, font=f_vow)
    d.text((cxm - tw / 2, by1 - 26), vowel, font=f_vow,
           fill=(TEAL if active else MUTED) + (220,))

# ---------- audio visualizer (bottom, minimal) ----------
import math
d = D()
bars = 72
bw = (NF_X1 - NF_X0) / bars
midy = (VIS_Y0 + VIS_Y1) / 2
for b in range(bars):
    t = b / bars
    amp = (0.35 + 0.65 * abs(math.sin(t * 9.0)) * (0.5 + 0.5 * math.sin(t * 2.3 + 1)))
    hh = amp * (VIS_Y1 - VIS_Y0) * 0.46
    x = NF_X0 + b * bw + bw * 0.28
    col = TEAL if b % 6 == 0 else CREAM
    a = 150 if b % 6 == 0 else 95
    d.rounded_rectangle([x, midy - hh, x + bw * 0.44, midy + hh], radius=2,
                        fill=col + (a,))

# ---------- right column: wordmark, title, cover ----------
RX0, RX1 = 1232, 1892
d = D()

# wordmark top-right ("Miku" M in teal)
f_wm = font(30)
parts = [("Atelier ", CREAM), ("M", TEAL), ("iku Acappella", CREAM)]
total = sum(d.textlength(t, font=f_wm) for t, _ in parts)
wx = RX1 - total
wy = 34
for t, c in parts:
    d.text((wx, wy), t, font=f_wm, fill=c + (240,))
    wx += d.textlength(t, font=f_wm)
# thin rule under wordmark
d.line([(RX1 - total, wy + 44), (RX1, wy + 44)], fill=CREAM + (70,), width=1)

# title block
ty = 150
f_comp = font(46)
f_piece = font(34)
f_sub = font(22)
f_feat = font(24)
d.text((RX0, ty), "Antonio Vivaldi", font=f_comp, fill=CREAM + (255,))
d.text((RX0, ty + 64), "Spring — I. Allegro", font=f_piece, fill=CREAM + (235,))
d.text((RX0, ty + 112), "from  The Four Seasons  (1725)", font=f_sub,
       fill=CREAM + (170,))
# feat line with teal Miku
fx = RX0
d.text((fx, ty + 152), "feat. ", font=f_feat, fill=CREAM + (200,))
fx += d.textlength("feat. ", font=f_feat)
d.text((fx, ty + 152), "Hatsune Miku", font=f_feat, fill=TEAL + (235,))

# cover image panel (1:1) bottom-right with cream frame
cs = 612
cv = Image.open(COVER).convert("RGB")
s = max(cs / cv.width, cs / cv.height)
cv = cv.resize((int(cv.width * s), int(cv.height * s)), Image.LANCZOS)
l = (cv.width - cs) // 2
t = (cv.height - cs) // 2
cv = cv.crop((l, t, l + cs, t + cs))
cxp, cyp = RX1 - cs, H - cs - 56
# soft shadow
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(sh).rectangle([cxp - 10, cyp - 10, cxp + cs + 10, cyp + cs + 10],
                             fill=(0, 0, 0, 150))
img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)))
img.paste(cv, (cxp, cyp))
D().rectangle([cxp, cyp, cxp + cs, cyp + cs], outline=CREAM + (180,), width=2)

# ---------- save ----------
img.convert("RGB").save(OUT, "PNG")
print("saved:", OUT, img.size)
