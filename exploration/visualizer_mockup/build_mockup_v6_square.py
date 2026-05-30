# -*- coding: utf-8 -*-
"""
Project Muse — v6: simple LARGE SQUARE cover + gold border (no arch). (s356, 코튼 feedback)
Drop the arch frame (caused asymmetry with square covers). Clean symmetric layout:
big square cover (full, uncropped) + gold double border, 6 voice panels, era tag + title,
paper-texture overlay. Era now conveyed by the tag/playlist, not the frame.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = r"C:/Users/user/Desktop/myProject/Project_Muse"
FONT = BASE + "/assets/fonts/gfs_didot/GFSDidot-Regular.ttf"
OUT_DIR = BASE + "/exploration/visualizer_mockup"
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 1920, 1080
CREAM=(232,224,200); TEAL=(40,180,175); GOLD=(201,169,106); MUTED=(140,138,146)
def font(sz): return ImageFont.truetype(FONT, sz)
yy, xx = np.mgrid[0:H, 0:W]

def contain(im, b):
    s=min(b/im.width, b/im.height)
    return im.resize((max(1,int(im.width*s)),max(1,int(im.height*s))),Image.LANCZOS)

roles=[("I","Ah",(216,184,120),True),("II","Ah",(201,143,143),False),
       ("III","Oo",(95,185,179),True),("IV","Oo",(159,185,143),False),
       ("V","Oo",(210,160,96),True),("VI","Mm",(176,168,196),True)]

def render(cfg):
    cv0=Image.open(cfg["cover"]).convert("RGB")
    sm=np.asarray(cv0.resize((90,90))).reshape(-1,3).astype(float)
    lum=sm@np.array([0.299,0.587,0.114]); o=np.argsort(lum)
    dark=sm[o[:len(o)//4]].mean(0); mid=sm[o[len(o)//2-250:len(o)//2+250]].mean(0)
    def cap(c,mx,fl=8):
        c=np.array(c,float); m=c.max()
        if m>mx:c=c*(mx/m)
        return np.clip(c,fl,255)
    gd,gm,ga=cap(dark,50),cap(mid,88),cap(dark*0.8+mid*0.2,62)
    t=(((xx/W)+(yy/H))/2.0)[...,None]
    bgarr=np.where(t<0.5,gd+(gm-gd)*(t/0.5),gm+(ga-gm)*((t-0.5)/0.5))
    img=Image.fromarray(np.clip(bgarr,0,255).astype("uint8")).convert("RGBA")
    def D(): return ImageDraw.Draw(img)

    # ---- big square cover (full) + gold double border ----
    SQ=884
    cv=contain(cv0, SQ)
    cx0=90; cy0=(H-cv.height)//2
    # soft shadow
    sh=Image.new("RGBA",(W,H),(0,0,0,0))
    ImageDraw.Draw(sh).rectangle([cx0-14,cy0-14,cx0+cv.width+14,cy0+cv.height+14],fill=(0,0,0,150))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(20)))
    img.paste(cv,(cx0,cy0))
    d=D()
    x1=cx0+cv.width; y1=cy0+cv.height
    d.rectangle([cx0-7,cy0-7,x1+7,y1+7],outline=GOLD+(235,),width=5)   # outer
    d.rectangle([cx0-1,cy0-1,x1+1,y1+1],outline=GOLD+(180,),width=2)   # inner

    # ---- 6 voice panels ----
    gx0,gy0=1120,118; cw,ch,gap=348,232,26
    f_num,f_vow,f_mk=font(40),font(18),font(15)
    for i,(num,vowel,color,active) in enumerate(roles):
        x0=gx0+(i%2)*(cw+gap); y0=gy0+(i//2)*(ch+gap); xx1,yy1=x0+cw,y0+ch
        gl=Image.new("RGBA",(W,H),(0,0,0,0)); gdd=ImageDraw.Draw(gl)
        gdd.rounded_rectangle([x0,y0,xx1,yy1],radius=8,fill=color+(150 if active else 55,))
        if active: img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(18)))
        img.alpha_composite(gl); d=D()
        d.rounded_rectangle([x0,y0,xx1,yy1],radius=8,outline=(20,18,16,235),width=6)
        d.rounded_rectangle([x0+6,y0+6,xx1-6,yy1-6],radius=6,outline=(GOLD if active else MUTED)+(210,),width=2)
        mcx,mcy=(x0+xx1)/2,(y0+yy1)/2; tc=CREAM if active else MUTED
        nn=d.textlength(num,font=f_num); d.text((mcx-nn/2,mcy-34),num,font=f_num,fill=tc+(255,))
        vw=d.textlength(vowel,font=f_vow); d.text((mcx-vw/2,mcy+18),vowel,font=f_vow,fill=(TEAL if active else MUTED)+(220,))
        mw=d.textlength("MIKU",font=f_mk); d.text((mcx-mw/2,y0+12),"MIKU",font=f_mk,fill=tc+(180,))

    # ---- wordmark + era + title ----
    d=D(); f_wm=font(28); parts=[("Atelier ",CREAM),("M",TEAL),("iku Acappella",CREAM)]
    total=sum(d.textlength(t,font=f_wm) for t,_ in parts); RXR=gx0+2*cw+gap; wx,wy=RXR-total,40
    for t,c in parts: d.text((wx,wy),t,font=f_wm,fill=c+(240,)); wx+=d.textlength(t,font=f_wm)
    d.line([(RXR-total,wy+40),(RXR,wy+40)],fill=GOLD+(150,),width=1)
    ty=884
    d.text((gx0,ty),cfg["era"],font=font(20),fill=GOLD+(225,))
    d.text((gx0,ty+34),cfg["composer"],font=font(42),fill=CREAM+(255,))
    d.text((gx0,ty+92),cfg["piece"],font=font(28),fill=CREAM+(225,))
    pre=cfg["sub"]+"  ·  feat. "; fx=gx0
    d.text((fx,ty+134),pre,font=font(19),fill=CREAM+(160,)); fx+=d.textlength(pre,font=font(19))
    d.text((fx,ty+134),"Hatsune Miku",font=font(19),fill=TEAL+(230,))

    # ---- paper texture ----
    base=img.convert("RGB"); arr=np.asarray(base).astype(float)
    noise=Image.effect_noise((W,H),30).filter(ImageFilter.GaussianBlur(0.6))
    low=Image.effect_noise((W,H),18).resize((W//6,H//6)).resize((W,H)).filter(ImageFilter.GaussianBlur(2))
    n=(np.asarray(noise).astype(float)+np.asarray(low).astype(float))/2.0
    mult=0.88+0.20*(n/255.0); out=np.clip(arr*mult[...,None],0,255)
    out[...,0]=np.clip(out[...,0]*1.012,0,255); out[...,2]=np.clip(out[...,2]*0.99,0,255)
    p=OUT_DIR+"/"+cfg["out"]; Image.fromarray(out.astype("uint8")).save(p,"PNG"); print("saved:",p)

configs=[
 dict(cover=BASE+"/works/elgar_salut_damour/video/visualizer/public/cover.png",
      era="❖  ROMANTIC ERA",composer="Edward Elgar",piece="Salut d'Amour",
      sub="Op. 12 (1888)",out="v6_square_elgar.png"),
 dict(cover=BASE+"/works/vivaldi_spring_1_allegro/video/visualizer/public/cover.png",
      era="❖  BAROQUE ERA",composer="Antonio Vivaldi",piece="Spring — I. Allegro",
      sub="The Four Seasons (1725)",out="v6_square_vivaldi.png"),
]
for c in configs: render(c)
print("done")
