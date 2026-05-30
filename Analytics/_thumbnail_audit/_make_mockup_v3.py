# -*- coding: utf-8 -*-
"""Joplin 썸네일 v3/v4 — 코튼 피드백 반영: 인셋 제거(더블 미쿠 해소) + 텍스트 라벨 제거.
미쿠는 명화 안에서 '그림으로' 보여줌. v3=와이드 페인터리, v4=미쿠 줌."""
from PIL import Image, ImageDraw, ImageFont

COVER = "works/joplin_the_entertainer/video/cover/joplin_the_entertainer_album_1x1.png"
FONT  = "assets/fonts/gfs_didot/GFSDidot-Regular.ttf"
OUT   = "Analytics/_thumbnail_audit"
W, H = 1280, 720

cover = Image.open(COVER).convert("RGB")
cw, ch = cover.size

def fill_crop(img, tw, th, top_bias=0.0):
    s = max(tw/img.width, th/img.height)
    nw, nh = int(img.width*s+0.5), int(img.height*s+0.5)
    r = img.resize((nw, nh), Image.LANCZOS)
    x = (nw-tw)//2
    y = int((nh-th)*(0.5 + top_bias*0.5)); y = max(0, min(nh-th, y))
    return r.crop((x, y, x+tw, y+th))

def sub_then_fill(img, box01, tw, th):
    """box01=(x0,y0,x1,y1) in 0..1 of cover → crop → fill 16:9."""
    x0,y0,x1,y1 = box01
    sub = img.crop((int(x0*img.width),int(y0*img.height),int(x1*img.width),int(y1*img.height)))
    return fill_crop(sub, tw, th, top_bias=0.0)

def fnt(sz): return ImageFont.truetype(FONT, sz)
def tsh(draw, xy, txt, font, fill=(255,255,255), off=4):
    x,y=xy; draw.text((x+off,y+off),txt,font=font,fill=(0,0,0,170)); draw.text((x,y),txt,font=font,fill=fill)
def wordmark(draw,x,y,sz):
    f=fnt(sz)
    for t,c in [("Atelier ",(232,230,222)),("M",(120,224,224)),("iku Acappella",(232,230,222))]:
        draw.text((x+2,y+2),t,font=f,fill=(0,0,0,150)); draw.text((x,y),t,font=f,fill=c); x+=draw.textlength(t,font=f)

def title_block(bg, y_joplin=250, big=118):
    d=ImageDraw.Draw(bg)
    tsh(d,(70,y_joplin),"Scott Joplin",fnt(46),fill=(216,212,198))
    tsh(d,(66,y_joplin+50),"The Entertainer",fnt(big))
    wordmark(d,72,y_joplin+50+big+8,38)

def bottom_scrim(bg, start=380):
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)
    for y in range(H):
        a=int(200*max(0,(y-start)/(H-start))); od.line([(0,y),(W,y)],fill=(6,9,13,a))
    return Image.alpha_composite(bg.convert("RGBA"), ov).convert("RGB")

# v3 — 와이드 페인터리 (v2 배경 그대로, 인셋·라벨 제거). 명화 속 미쿠가 우측에 보임.
bg3 = fill_crop(cover, W, H, top_bias=-0.4)
bg3 = bottom_scrim(bg3, start=380)
title_block(bg3, y_joplin=470, big=120)
bg3.save(f"{OUT}/joplin_v3_wide.jpg", quality=90)

# v4 — 미쿠 줌 (명화 우상단 무대 영역 확대 → 미쿠 또렷, 인셋 불필요). 제목 좌하단.
bg4 = sub_then_fill(cover, (0.16, 0.0, 1.0, 0.52), W, H)
bg4 = bottom_scrim(bg4, start=360)
title_block(bg4, y_joplin=470, big=120)
bg4.save(f"{OUT}/joplin_v4_zoom.jpg", quality=90)
print("saved v3_wide, v4_zoom")
