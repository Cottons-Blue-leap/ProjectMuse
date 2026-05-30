# -*- coding: utf-8 -*-
"""v4 썸네일 양식 4곡 일괄 (코튼 결단 s348): 커버 속 미쿠 줌 + 좌하단 제목 + 인셋·라벨 X.
per-song box = 커버(1254² 또는 16:9) 안에서 미쿠를 주인공으로 잡는 crop 영역."""
from PIL import Image, ImageDraw, ImageFont

FONT = "assets/fonts/gfs_didot/GFSDidot-Regular.ttf"
OUT  = "Analytics/_thumbnail_audit"
W, H = 1280, 720

SONGS = {
    "joplin": dict(
        cover="works/joplin_the_entertainer/video/cover/joplin_the_entertainer_album_1x1.png",
        box=(0.16, 0.00, 1.00, 0.52), composer="Scott Joplin", piece="The Entertainer"),
    "vivaldi": dict(
        cover="works/vivaldi_spring_1_allegro/video/cover/album_1x1.png",
        box=(0.21, 0.22, 0.93, 0.62), composer="Antonio Vivaldi", piece="Spring, Mvt. I"),
    "gymnopedie": dict(
        cover="works/gymnopedie_1_first_proof/video/visualizer/public/cover.png",
        box=(0.16, 0.26, 0.98, 0.99), composer="Erik Satie", piece="Gymnopédie No. 1"),
    "salut": dict(
        cover="works/elgar_salut_damour/video/cover/Miku_waterhouse_soul_of_the_rose.png",
        box=(0.00, 0.04, 1.00, 0.80), composer="Edward Elgar", piece="Salut d'Amour"),
}

def fnt(sz): return ImageFont.truetype(FONT, sz)
_probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
def tw(text, f): return _probe.textlength(text, font=f)

def fit(text, maxw, start=122, lo=60):
    for sz in range(start, lo-1, -2):
        if tw(text, fnt(sz)) <= maxw: return fnt(sz), sz
    return fnt(lo), lo

def sub_then_fill(img, box01):
    x0,y0,x1,y1 = box01
    sub = img.crop((int(x0*img.width),int(y0*img.height),int(x1*img.width),int(y1*img.height)))
    s = max(W/sub.width, H/sub.height)
    r = sub.resize((int(sub.width*s+0.5), int(sub.height*s+0.5)), Image.LANCZOS)
    x = (r.width-W)//2; y = (r.height-H)//2
    return r.crop((x, y, x+W, y+H))

def bottom_scrim(bg, start=360):
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)
    for y in range(H):
        a=int(205*max(0,(y-start)/(H-start))); od.line([(0,y),(W,y)],fill=(6,9,13,a))
    return Image.alpha_composite(bg.convert("RGBA"), ov).convert("RGB")

def tsh(d,xy,t,f,fill=(255,255,255),off=4):
    x,y=xy; d.text((x+off,y+off),t,font=f,fill=(0,0,0,170)); d.text((x,y),t,font=f,fill=fill)

def wordmark(d,x,y,sz=38):
    f=fnt(sz)
    for t,c in [("Atelier ",(232,230,222)),("M",(120,224,224)),("iku Acappella",(232,230,222))]:
        d.text((x+2,y+2),t,font=f,fill=(0,0,0,150)); d.text((x,y),t,font=f,fill=c); x+=tw(t,f)

for name, cfg in SONGS.items():
    bg = sub_then_fill(Image.open(cfg["cover"]).convert("RGB"), cfg["box"])
    bg = bottom_scrim(bg, start=350)
    d = ImageDraw.Draw(bg)
    big_f, big_sz = fit(cfg["piece"], W-150)
    comp_f, wm_f = fnt(46), fnt(38)
    # 측정된 ink bbox(디센더 포함)로 아래→위 스택, 줄 사이 실측 간격 보장 (텍스트 겹침 방지).
    cb = _probe.textbbox((0, 0), cfg["composer"], font=comp_f)
    pb = _probe.textbbox((0, 0), cfg["piece"], font=big_f)
    wb = _probe.textbbox((0, 0), "Atelier Miku Acappella", font=wm_f)
    GAP, GAP2 = 22, 12
    wm_y = (H - 26) - wb[3]                          # 워드마크 ink 바닥 = H-26
    big_y = (wm_y + wb[1]) - GAP - pb[3]             # 제목 바닥 = 워드마크 ink 윗선 - GAP
    comp_y = (big_y + pb[1]) - GAP2 - cb[3]          # 작곡가 바닥 = 제목 ink 윗선 - GAP2
    tsh(d, (70, comp_y), cfg["composer"], comp_f, fill=(216, 212, 198))
    tsh(d, (66, big_y), cfg["piece"], big_f)
    wordmark(d, 72, wm_y, 38)
    bg.save(f"{OUT}/thumb_{name}_v4.jpg", quality=90)
    print(f"saved thumb_{name}_v4.jpg  (title {big_sz}px)")
