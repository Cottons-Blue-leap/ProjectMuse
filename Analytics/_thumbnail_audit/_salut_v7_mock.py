# -*- coding: utf-8 -*-
"""scratch v7 — GPT 피드백 종합(취사선택).
채택: ① 初音ミク(JP 인식) + 'A CAPPELLA'(영문 대문자=작은화면 즉독+국제성)
      ② 색 분리 = 初音ミク 아이보리 + A CAPPELLA 민트 액센트 (틸 blend 문제 완화·브랜드색 유지)
      ③ 배지를 우선정보로 = 키우고 작곡가는 축소
      ④ 배경 무관 가독 = 강한 backing
적용 갈림: backing을 (a)강한 그라데이션 스크림[우아·내 lean] vs (b)반투명 패널[GPT 박스안] 둘 다 렌더.
거부: 'MIKU ACAPPELLA' 전면 영문화(=JP 인식 목적 무력화) · 굵은 고딕(=아까 어색 주범) 회피."""
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

_p = ImageDraw.Draw(Image.new("RGB", (8, 8)))
def didot(s): return ImageFont.truetype(DIDOT, s)
def minr(s): return ImageFont.truetype(MIN_R, s, index=0)
def tw(t, f): return _p.textlength(t, font=f)
def fit(t, mw, start=92, lo=54):
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

def scrim(bg, start, amax):
    ov = Image.new("RGBA",(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)
    for y in range(H):
        a = int(amax*max(0,(y-start)/(H-start)))
        od.line([(0,y),(W,y)], fill=(6,9,13,a))
    return Image.alpha_composite(bg.convert("RGBA"), ov).convert("RGB")

def panel(bg, box, r=22):
    ov = Image.new("RGBA",(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)
    od.rounded_rectangle(box, radius=r, fill=(9,11,15,148), outline=(236,233,224,80), width=2)
    return Image.alpha_composite(bg.convert("RGBA"), ov).convert("RGB")

def sh(d, xy, t, f, fill, off=4):
    x,y=xy; d.text((x+off,y+off),t,font=f,fill=(0,0,0)); d.text((x,y),t,font=f,fill=fill)

def sh_spaced(d, xy, t, f, fill, sp, off=4):
    x,y=xy
    for ch in t:
        d.text((x+off,y+off),ch,font=f,fill=(0,0,0)); d.text((x,y),ch,font=f,fill=fill)
        x+=tw(ch,f)+sp
    return x

def layout():
    """(miku_f, aca_f, comp_f, big_f, ys...) 계산 — 공통."""
    miku_f, aca_f, comp_f = minr(108), didot(60), didot(38)
    big_f = fit(PIECE, W-150)
    mb=_p.textbbox((0,0),"初音ミク",font=miku_f)
    ab=_p.textbbox((0,0),"A CAPPELLA",font=aca_f)
    cb=_p.textbbox((0,0),COMPOSER,font=comp_f)
    pb=_p.textbbox((0,0),PIECE,font=big_f)
    big_y=(H-36)-pb[3]
    comp_y=(big_y+pb[1])-12-cb[3]
    aca_y=(comp_y+cb[1])-22-ab[3]
    miku_y=(aca_y+ab[1])-12-mb[3]
    return miku_f,aca_f,comp_f,big_f,miku_y,aca_y,comp_y,big_y,mb,ab

def draw_text(bg, L):
    miku_f,aca_f,comp_f,big_f,miku_y,aca_y,comp_y,big_y,mb,ab = L
    d=ImageDraw.Draw(bg)
    sh(d,(70,miku_y),"初音ミク",miku_f,IVORY)
    sh_spaced(d,(74,aca_y),"A CAPPELLA",aca_f,MINT,8)
    sh(d,(72,comp_y),COMPOSER,comp_f,(192,188,176))
    sh(d,(66,big_y),PIECE,big_f,(255,255,255))

def build_scrim():
    bg = sub_then_fill(Image.open(COVER).convert("RGB"), BOX)
    L = layout()
    bg = scrim(bg, max(230, L[4]-44), 226)
    draw_text(bg, L)
    o=OUT/"_salut_v7_scrim.jpg"; bg.save(o,quality=92); print("scrim",o)

def build_panel():
    bg = sub_then_fill(Image.open(COVER).convert("RGB"), BOX)
    bg = scrim(bg, 430, 150)   # 곡명쪽 약한 스크림은 유지
    L = layout()
    miku_y, aca_y, mb, ab = L[4], L[5], L[8], L[9]
    # 배지(初音ミク+A CAPPELLA)만 패널로
    pad = 26
    x0 = 70 - pad
    y0 = miku_y + mb[1] - pad
    y1 = aca_y + ab[3] + pad
    badge_w = max(tw("初音ミク", L[0]), tw("A CAPPELLA", L[1]) + 8*9)
    x1 = 74 + badge_w + pad
    bg = panel(bg, (x0, y0, x1, y1))
    draw_text(bg, L)
    o=OUT/"_salut_v7_panel.jpg"; bg.save(o,quality=92); print("panel",o)

if __name__ == "__main__":
    print("Pillow rounded_rectangle:", hasattr(ImageDraw.ImageDraw, "rounded_rectangle"))
    build_scrim()
    build_panel()
