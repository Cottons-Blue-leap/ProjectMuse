# -*- coding: utf-8 -*-
"""scratch v9 — 코튼 확정 배치 + 위치 미세조정(크기 불변).
배치: 初音ミク / A CAPPELLA / Salut d'Amour · Edward Elgar (3줄 · 곡명·작곡가 한 줄 middot)
미세조정: ① 좌측 시각 정렬(좌side-bearing 보정) ② 인라인 줄 baseline 정렬 ③ 균형 잡힌 세로 리듬."""
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
IVORY = (245, 243, 235); MINT = (139, 223, 206); DIM = (196, 192, 178)
LEFT = 72                       # 공통 시각 좌측선
G_BADGE = 22                    # 初音ミク ↔ A CAPPELLA (10→22: A CAPPELLA 살짝 내림·여유)
G_TITLE = 34                    # A CAPPELLA ↔ 타이틀 (46→34: 균형 · 初音ミク/타이틀 위치 고정)
BOTTOM = 44                     # 하단 여백

# 크기 고정 (코튼: 변경 금지)
F_MIKU, F_ACA, F_PIECE, F_COMP, F_DOT = 108, 60, 92, 36, 44

_p = ImageDraw.Draw(Image.new("RGB", (8, 8)))
def didot(s): return ImageFont.truetype(DIDOT, s)
def minr(s): return ImageFont.truetype(MIN_R, s, index=0)
def tw(t, f): return _p.textlength(t, font=f)
def bbox(t, f): return _p.textbbox((0, 0), t, font=f)

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

def sh(d,x,y,t,f,fill,off=4):
    d.text((x+off,y+off),t,font=f,fill=(0,0,0)); d.text((x,y),t,font=f,fill=fill)

def sh_sp(d,x,y,t,f,fill,sp,off=4):
    for ch in t:
        d.text((x+off,y+off),ch,font=f,fill=(0,0,0)); d.text((x,y),ch,font=f,fill=fill); x+=tw(ch,f)+sp

def build():
    bg=sub_then_fill(Image.open(COVER).convert("RGB"),BOX)
    mf,af,pf,cf,df = minr(F_MIKU),didot(F_ACA),didot(F_PIECE),didot(F_COMP),didot(F_DOT)
    mb,ab,pb=bbox("初音ミク",mf),bbox("A CAPPELLA",af),bbox(PIECE,pf)
    # --- 세로: 아래→위 ---
    piece_y=(H-BOTTOM)-pb[3]                         # 곡명 잉크 하단 = H-BOTTOM
    aca_y=(piece_y+pb[1])-G_TITLE-ab[3]
    miku_y=(aca_y+ab[1])-G_BADGE-mb[3]
    bg=scrim(bg,max(210,miku_y-46)); d=ImageDraw.Draw(bg)
    # --- 좌측 시각 정렬: x = LEFT - 좌side-bearing ---
    sh(d, LEFT-mb[0], miku_y, "初音ミク", mf, IVORY)
    sh_sp(d, LEFT-ab[0], aca_y, "A CAPPELLA", af, MINT, 8)
    # --- 타이틀 인라인 (baseline 정렬) ---
    p_asc=pf.getmetrics()[0]; c_asc=cf.getmetrics()[0]; d_asc=df.getmetrics()[0]
    baseline=piece_y+p_asc
    x=LEFT-pb[0]
    sh(d, x, piece_y, PIECE, pf, (255,255,255))
    x=x+tw(PIECE,pf)+20
    sh(d, x, baseline-d_asc, "·", df, DIM)
    x=x+tw("·",df)+20
    sh(d, x, baseline-c_asc, COMPOSER, cf, DIM)
    o=OUT/"_salut_v9.jpg"; bg.save(o,quality=92); print(o)

if __name__=="__main__":
    build()
