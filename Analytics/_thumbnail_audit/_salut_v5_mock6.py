# -*- coding: utf-8 -*-
"""scratch v5 mock #6 — '어색함' 진단 후 3방향.
진단: 굵은 Mincho(Demibold) 틸이 섬세한 Didot와 무게 불일치 + 같은 크기 2줄이 곡명과
      '두 큰 덩어리'로 경쟁 → 위계 흐림.
A 정제형 : Yu Mincho *Regular*(가벼움) + 자간 → Didot와 무게 맞춤 (2줄·큼 유지)
B 위계형 : 初音ミク 大 + アカペラ 小(종속) → JP 안에서 위계 → 곡명과 충돌 완화
C 키커형 : 初音ミク・アカペラ 한 줄 자간 + 가는 룰선 = 에디토리얼 kicker (작지만 우아)
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE = Path(r"C:\Users\user\Desktop\myProject\Project_Muse")
DIDOT = str(BASE / "assets/fonts/gfs_didot/GFSDidot-Regular.ttf")
MIN_R = r"C:\Windows\Fonts\yumin.ttf"      # Yu Mincho Regular (가벼움)
COVER = BASE / "works/elgar_salut_damour/video/cover/Miku_waterhouse_soul_of_the_rose.png"
BOX = (0.00, 0.04, 1.00, 0.80)
COMPOSER, PIECE = "Edward Elgar", "Salut d'Amour"
OUT = Path(r"C:\Users\user\Desktop\myProject\Project_Muse\Analytics\_thumbnail_audit")
W, H = 1280, 720
TEAL = (158, 218, 205)

_p = ImageDraw.Draw(Image.new("RGB", (8, 8)))
def didot(s): return ImageFont.truetype(DIDOT, s)
def minr(s): return ImageFont.truetype(MIN_R, s, index=0)
def tw(t, f): return _p.textlength(t, font=f)
def fit(t, mw, start=110, lo=58):
    for s in range(start, lo-1, -2):
        if tw(t, didot(s)) <= mw: return didot(s)
    return didot(lo)

def sub_then_fill(img, b):
    x0,y0,x1,y1 = b
    sub = img.crop((int(x0*img.width),int(y0*img.height),int(x1*img.width),int(y1*img.height)))
    s = max(W/sub.width, H/sub.height)
    r = sub.resize((int(sub.width*s+0.5),int(sub.height*s+0.5)), Image.LANCZOS)
    x,y = (r.width-W)//2,(r.height-H)//2
    return r.crop((x,y,x+W,y+H))

def scrim(bg, start):
    ov = Image.new("RGBA",(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)
    for y in range(H):
        a = int(212*max(0,(y-start)/(H-start)))
        od.line([(0,y),(W,y)], fill=(6,9,13,a))
    return Image.alpha_composite(bg.convert("RGBA"), ov).convert("RGB")

def sh(d, xy, t, f, fill, off=4):
    x,y=xy; d.text((x+off,y+off),t,font=f,fill=(0,0,0)); d.text((x,y),t,font=f,fill=fill)

def sh_spaced(d, xy, t, f, fill, sp, off=4):
    x,y = xy
    for ch in t:
        d.text((x+off,y+off),ch,font=f,fill=(0,0,0)); d.text((x,y),ch,font=f,fill=fill)
        x += tw(ch,f)+sp

def base():
    return sub_then_fill(Image.open(COVER).convert("RGB"), BOX)

def bottom_latin(d, big_y, comp_y):
    big_f = fit(PIECE, W-150)
    sh(d,(72,comp_y),COMPOSER,didot(44),(216,212,198))
    sh(d,(66,big_y),PIECE,big_f,(255,255,255))

def variant_A():
    bg = base();
    f = minr(86)
    mb=_p.textbbox((0,0),"初音ミク",font=f); ab=_p.textbbox((0,0),"アカペラ",font=f)
    cb=_p.textbbox((0,0),COMPOSER,font=didot(44)); pb=_p.textbbox((0,0),PIECE,font=fit(PIECE,W-150))
    big_y=(H-34)-pb[3]; comp_y=(big_y+pb[1])-12-cb[3]
    aca_y=(comp_y+cb[1])-24-ab[3]; miku_y=(aca_y+ab[1])-10-mb[3]
    bg=scrim(bg,max(250,miku_y-38)); d=ImageDraw.Draw(bg)
    sh_spaced(d,(70,miku_y),"初音ミク",f,TEAL,8); sh_spaced(d,(70,aca_y),"アカペラ",f,TEAL,8)
    bottom_latin(d,big_y,comp_y)
    o=OUT/"_salut_v5_A_refined.jpg"; bg.save(o,quality=92); print("A",o)

def variant_B():
    bg = base()
    mf=minr(98); af=minr(50)
    mb=_p.textbbox((0,0),"初音ミク",font=mf); ab=_p.textbbox((0,0),"アカペラ",font=af)
    cb=_p.textbbox((0,0),COMPOSER,font=didot(44)); pb=_p.textbbox((0,0),PIECE,font=fit(PIECE,W-150))
    big_y=(H-34)-pb[3]; comp_y=(big_y+pb[1])-12-cb[3]
    aca_y=(comp_y+cb[1])-22-ab[3]; miku_y=(aca_y+ab[1])-6-mb[3]
    bg=scrim(bg,max(250,miku_y-38)); d=ImageDraw.Draw(bg)
    sh(d,(70,miku_y),"初音ミク",mf,TEAL); sh_spaced(d,(74,aca_y),"アカペラ",af,TEAL,10)
    bottom_latin(d,big_y,comp_y)
    o=OUT/"_salut_v5_B_hierarchy.jpg"; bg.save(o,quality=92); print("B",o)

def variant_C():
    bg = base()
    kf=minr(46)
    cb=_p.textbbox((0,0),COMPOSER,font=didot(44)); pb=_p.textbbox((0,0),PIECE,font=fit(PIECE,W-150))
    kb=_p.textbbox((0,0),"初音ミク",font=kf)
    big_y=(H-34)-pb[3]; comp_y=(big_y+pb[1])-12-cb[3]
    rule_y=comp_y-26; kick_y=rule_y-18-kb[3]
    bg=scrim(bg,max(250,kick_y-40)); d=ImageDraw.Draw(bg)
    sh_spaced(d,(72,kick_y),"初音ミク ・ アカペラ",kf,TEAL,6)
    d.line([(74,rule_y),(74+360,rule_y)],fill=TEAL,width=2)
    bottom_latin(d,big_y,comp_y)
    o=OUT/"_salut_v5_C_kicker.jpg"; bg.save(o,quality=92); print("C",o)

if __name__ == "__main__":
    variant_A(); variant_B(); variant_C()
