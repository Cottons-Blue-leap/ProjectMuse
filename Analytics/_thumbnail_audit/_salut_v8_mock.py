# -*- coding: utf-8 -*-
"""scratch v8 — Scrim 채택본 + 작곡가 하단 이동 → 2-tier(배지/타이틀) 세로 여유.
above = 初音ミク / A CAPPELLA  ‖gap‖  Edward Elgar / Salut d'Amour (작곡가 곡명 위·관례)
below = 初音ミク / A CAPPELLA  ‖gap‖  Salut d'Amour / Edward Elgar (작곡가 곡명 아래·byline)"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE = Path(r"C:\Users\user\Desktop\myProject\Project_Muse")
DIDOT = str(BASE / "assets/fonts/gfs_didot/GFSDidot-Regular.ttf")
MIN_R = r"C:\Windows\Fonts\yumin.ttf"
COVER = BASE / "works/elgar_salut_damour/video/cover/Miku_waterhouse_soul_of_the_rose.png"
BOX = (0.00, 0.04, 1.00, 0.80)
COMPOSER, PIECE = "Edward Elgar", "Salut d'Amour"
OUT = Path(r"C:\Users\user\Desktop\myProject\Project_Muse\Analytics\_thumbnail_audit")
W, H = 1280, 720
IVORY = (245, 243, 235)
MINT  = (139, 223, 206)
GAP = 54  # 배지↔타이틀 사이 여유

_p = ImageDraw.Draw(Image.new("RGB", (8, 8)))
def didot(s): return ImageFont.truetype(DIDOT, s)
def minr(s): return ImageFont.truetype(MIN_R, s, index=0)
def tw(t, f): return _p.textlength(t, font=f)
def fit(t, mw, start=92, lo=54):
    for s in range(start, lo-1, -2):
        if tw(t, didot(s)) <= mw: return didot(s)
    return didot(lo)

def sub_then_fill(img, b):
    x0,y0,x1,y1=b
    sub=img.crop((int(x0*img.width),int(y0*img.height),int(x1*img.width),int(y1*img.height)))
    s=max(W/sub.width,H/sub.height)
    r=sub.resize((int(sub.width*s+0.5),int(sub.height*s+0.5)),Image.LANCZOS)
    x,y=(r.width-W)//2,(r.height-H)//2
    return r.crop((x,y,x+W,y+H))

def scrim(bg,start,amax=226):
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)
    for y in range(H):
        a=int(amax*max(0,(y-start)/(H-start)))
        od.line([(0,y),(W,y)],fill=(6,9,13,a))
    return Image.alpha_composite(bg.convert("RGBA"),ov).convert("RGB")

def sh(d,xy,t,f,fill,off=4):
    x,y=xy; d.text((x+off,y+off),t,font=f,fill=(0,0,0)); d.text((x,y),t,font=f,fill=fill)
def sh_sp(d,xy,t,f,fill,sp,off=4):
    x,y=xy
    for ch in t:
        d.text((x+off,y+off),ch,font=f,fill=(0,0,0)); d.text((x,y),ch,font=f,fill=fill); x+=tw(ch,f)+sp

def build(mode):
    bg=sub_then_fill(Image.open(COVER).convert("RGB"),BOX)
    miku_f,aca_f,comp_f,big_f=minr(108),didot(60),didot(36),fit(PIECE,W-150)
    mb=_p.textbbox((0,0),"初音ミク",font=miku_f); ab=_p.textbbox((0,0),"A CAPPELLA",font=aca_f)
    cb=_p.textbbox((0,0),COMPOSER,font=comp_f); pb=_p.textbbox((0,0),PIECE,font=big_f)
    if mode=="below":   # 곡명 위, 작곡가 맨 아래
        comp_y=(H-32)-cb[3]; big_y=(comp_y+cb[1])-12-pb[3]
    else:               # 작곡가 위, 곡명 맨 아래
        big_y=(H-34)-pb[3]; comp_y=(big_y+pb[1])-12-cb[3]
    top_title = min(big_y, comp_y)
    aca_y=(top_title+ (pb[1] if mode!="below" else cb[1]))-GAP-ab[3]
    # 위 식 단순화: 타이틀 그룹 최상단 잉크 상단 기준으로 gap
    title_top_ink = (comp_y+cb[1]) if mode!="below" else (big_y+pb[1])
    aca_y=title_top_ink-GAP-ab[3]
    miku_y=(aca_y+ab[1])-12-mb[3]
    bg=scrim(bg,max(220,miku_y-44))
    d=ImageDraw.Draw(bg)
    sh(d,(70,miku_y),"初音ミク",miku_f,IVORY)
    sh_sp(d,(74,aca_y),"A CAPPELLA",aca_f,MINT,8)
    sh(d,(72,comp_y),COMPOSER,comp_f,(192,188,176))
    sh(d,(66,big_y),PIECE,big_f,(255,255,255))
    o=OUT/f"_salut_v8_{mode}.jpg"; bg.save(o,quality=92); print(mode,o)

if __name__=="__main__":
    build("above")
    build("below")
