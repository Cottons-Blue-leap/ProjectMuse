# -*- coding: utf-8 -*-
"""
Project Muse — v4: era-matched ARCH variants (s356).
Same Art-Nouveau-Ensemble layout, but the hero arch architecture changes with the
musical/art era of the piece (ties to our era-playlist signature):
  Baroque   -> rounded arch          (Vivaldi / Primavera)
  Romantic  -> pointed Gothic arch   (Elgar / Waterhouse)
  20th C.   -> segmental arch        (Joplin / Glackens)
Borders are traced from the arch mask (shape-agnostic erosion), so any silhouette works.
Hero/panel Miku = placeholder (current covers); real version = official Miku art.
"""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

BASE = r"C:/Users/user/Desktop/myProject/Project_Muse"
FONT = BASE + "/assets/fonts/gfs_didot/GFSDidot-Regular.ttf"
OUT_DIR = BASE + "/exploration/visualizer_mockup"
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 1920, 1080
CREAM = (232, 224, 200); TEAL = (40, 180, 175); GOLD = (201, 169, 106); MUTED = (140, 138, 146)
def font(sz): return ImageFont.truetype(FONT, sz)

# hero arch box
AX0, AY0, AX1, AY1 = 70, 96, 1060, 1004
R = (AX1 - AX0) / 2.0
SPRING = AY0 + R
CX = (AX0 + AX1) / 2.0

yy, xx = np.mgrid[0:H, 0:W]

def arch_mask(style):
    body = (xx >= AX0) & (xx <= AX1) & (yy >= SPRING) & (yy <= AY1)
    if style == "rounded":
        top = (yy < SPRING) & (((xx - CX) / R) ** 2 + ((yy - SPRING) / R) ** 2 <= 1)
    elif style == "segmental":
        domeH = 250.0
        top = (yy < SPRING) & (xx >= AX0) & (xx <= AX1) & \
              (((xx - CX) / R) ** 2 + ((yy - SPRING) / domeH) ** 2 <= 1)
    elif style == "pointed":
        Rg = 700.0
        dL = np.sqrt((xx - AX0) ** 2 + (yy - SPRING) ** 2)
        dR = np.sqrt((xx - AX1) ** 2 + (yy - SPRING) ** 2)
        top = (yy < SPRING) & (xx >= AX0) & (xx <= AX1) & (dL <= Rg) & (dR <= Rg)
    m = (body | top).astype("uint8") * 255
    return Image.fromarray(m, "L")

def gold_band(mask_L, outer, inner):
    e_out = mask_L.filter(ImageFilter.MinFilter(outer))
    e_in = mask_L.filter(ImageFilter.MinFilter(inner))
    return ImageChops.subtract(e_out, e_in)

# ---------- panels data ----------
roles = [("I","Ah",(216,184,120),True),("II","Ah",(201,143,143),False),
         ("III","Oo",(95,185,179),True),("IV","Oo",(159,185,143),False),
         ("V","Oo",(210,160,96),True),("VI","Mm",(176,168,196),True)]

def render(cfg):
    style = cfg["style"]; cover = cfg["cover"]
    # palette + gradient bg
    cv0 = Image.open(cover).convert("RGB")
    sm = np.asarray(cv0.resize((90,90))).reshape(-1,3).astype(float)
    lum = sm @ np.array([0.299,0.587,0.114]); o = np.argsort(lum)
    dark = sm[o[:len(o)//4]].mean(0); mid = sm[o[len(o)//2-250:len(o)//2+250]].mean(0)
    def cap(c,mx,fl=8):
        c=np.array(c,float); m=c.max()
        if m>mx: c=c*(mx/m)
        return np.clip(c,fl,255)
    gd,gm,ga = cap(dark,52),cap(mid,92),cap(dark*0.8+mid*0.2,64)
    t=(((xx/W)+(yy/H))/2.0)[...,None]
    bgarr=np.where(t<0.5, gd+(gm-gd)*(t/0.5), gm+(ga-gm)*((t-0.5)/0.5))
    img=Image.fromarray(np.clip(bgarr,0,255).astype("uint8")).convert("RGBA")
    def D(): return ImageDraw.Draw(img)

    # hero: cover via arch mask
    mask = arch_mask(style)
    bb_w, bb_h = AX1-AX0, AY1-AY0
    cv = cv0.copy(); s=max(bb_w/cv.width, bb_h/cv.height)
    cv=cv.resize((int(cv.width*s),int(cv.height*s)),Image.LANCZOS)
    l=(cv.width-bb_w)//2; tp=(cv.height-bb_h)//2; cv=cv.crop((l,tp,l+bb_w,tp+bb_h))
    cvl=Image.new("RGBA",(W,H),(0,0,0,0)); cvl.paste(cv,(AX0,AY0))
    img.paste(cvl,(0,0),mask)
    # gold borders from mask (shape-agnostic)
    for (oz,iz,a) in [(9,1,235),(27,21,180)]:
        band = gold_band(mask, oz, iz) if iz>1 else ImageChops.subtract(mask, mask.filter(ImageFilter.MinFilter(oz)))
        gl=Image.new("RGBA",(W,H),GOLD+(a,)); img.paste(gl,(0,0),band)

    d=D()
    # per-era ornament + apex/spandrel motifs
    apex_y = {"rounded":AY0+2,"pointed":AY0+2,"segmental":int(SPRING-250)+2}[style]
    if style=="rounded":   # baroque keystone
        d.rounded_rectangle([CX-26,apex_y+6,CX+26,apex_y+54],radius=8,outline=GOLD+(235,),width=3)
        d.arc([CX-26,apex_y+30,CX,apex_y+78],270,360,fill=GOLD+(180,),width=2)
        d.arc([CX,apex_y+30,CX+26,apex_y+78],180,270,fill=GOLD+(180,),width=2)
        for sx in (AX0+8,AX1-8):  # springline volutes
            d.arc([sx-30,SPRING-30,sx+30,SPRING+30],0,300,fill=GOLD+(200,),width=3)
    elif style=="pointed": # gothic finial + spandrel trefoils
        d.line([(CX,apex_y-30),(CX,apex_y+34)],fill=GOLD+(220,),width=3)
        d.line([(CX-16,apex_y),(CX+16,apex_y)],fill=GOLD+(220,),width=3)
        for sx in (AX0+70,AX1-70):
            for (dx,dy) in [(-14,0),(14,0),(0,-14)]:
                d.ellipse([sx+dx-12,SPRING-150+dy-12,sx+dx+12,SPRING-150+dy+12],
                          outline=GOLD+(190,),width=2)
    else:                  # art nouveau whiplash
        for sgn,sx in ((1,AX0+6),(-1,AX1-6)):
            d.arc([sx-46,SPRING-46,sx+46,SPRING+46],0 if sgn>0 else 90,140 if sgn>0 else 230,fill=GOLD+(210,),width=3)
            d.arc([sx-20+sgn*30,SPRING-70,sx+20+sgn*30,SPRING-30],180,360,fill=GOLD+(170,),width=2)
        d.ellipse([CX-6,apex_y+10,CX+6,apex_y+24],outline=GOLD+(220,),width=2)

    # 6 stained-glass voice panels (2x3)
    gx0,gy0=1120,118; cw,ch,gap=348,232,26
    f_num,f_vow,f_mk=font(40),font(18),font(15)
    for i,(num,vowel,color,active) in enumerate(roles):
        x0=gx0+(i%2)*(cw+gap); y0=gy0+(i//2)*(ch+gap); x1,y1=x0+cw,y0+ch
        gl=Image.new("RGBA",(W,H),(0,0,0,0)); gdd=ImageDraw.Draw(gl)
        gdd.rounded_rectangle([x0,y0,x1,y1],radius=8,fill=color+(150 if active else 55,))
        if active: img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(18)))
        img.alpha_composite(gl)
        d=D()
        d.rounded_rectangle([x0,y0,x1,y1],radius=8,outline=(20,18,16,235),width=6)
        d.rounded_rectangle([x0+6,y0+6,x1-6,y1-6],radius=6,outline=(GOLD if active else MUTED)+(210,),width=2)
        mcx,mcy=(x0+x1)/2,(y0+y1)/2; tcol=CREAM if active else MUTED
        nn=d.textlength(num,font=f_num); d.text((mcx-nn/2,mcy-34),num,font=f_num,fill=tcol+(255,))
        vw=d.textlength(vowel,font=f_vow); d.text((mcx-vw/2,mcy+18),vowel,font=f_vow,fill=(TEAL if active else MUTED)+(220,))
        mw=d.textlength("MIKU",font=f_mk); d.text((mcx-mw/2,y0+12),"MIKU",font=f_mk,fill=tcol+(180,))

    # wordmark (top-right)
    d=D(); f_wm=font(28)
    parts=[("Atelier ",CREAM),("M",TEAL),("iku Acappella",CREAM)]
    total=sum(d.textlength(t,font=f_wm) for t,_ in parts); RXR=gx0+2*cw+gap
    wx,wy=RXR-total,40
    for t,c in parts: d.text((wx,wy),t,font=f_wm,fill=c+(240,)); wx+=d.textlength(t,font=f_wm)
    d.line([(RXR-total,wy+40),(RXR,wy+40)],fill=GOLD+(150,),width=1)

    # era tag + title (bottom-right)
    ty=884
    d.text((gx0,ty),cfg["era"],font=font(20),fill=GOLD+(225,))
    d.text((gx0,ty+34),cfg["composer"],font=font(42),fill=CREAM+(255,))
    d.text((gx0,ty+92),cfg["piece"],font=font(28),fill=CREAM+(225,))
    fx=gx0; pre=cfg["sub"]+"  ·  feat. "
    d.text((fx,ty+134),pre,font=font(19),fill=CREAM+(160,)); fx+=d.textlength(pre,font=font(19))
    d.text((fx,ty+134),"Hatsune Miku",font=font(19),fill=TEAL+(230,))

    # paper texture multiply
    base=img.convert("RGB"); arr=np.asarray(base).astype(float)
    noise=Image.effect_noise((W,H),30).filter(ImageFilter.GaussianBlur(0.6))
    low=Image.effect_noise((W,H),18).resize((W//6,H//6)).resize((W,H)).filter(ImageFilter.GaussianBlur(2))
    n=(np.asarray(noise).astype(float)+np.asarray(low).astype(float))/2.0
    mult=0.88+0.20*(n/255.0)
    out=np.clip(arr*mult[...,None],0,255)
    out[...,0]=np.clip(out[...,0]*1.012,0,255); out[...,2]=np.clip(out[...,2]*0.99,0,255)
    p=OUT_DIR+"/"+cfg["out"]; Image.fromarray(out.astype("uint8")).save(p,"PNG"); print("saved:",p)

configs=[
 dict(style="rounded",cover=BASE+"/works/vivaldi_spring_1_allegro/video/visualizer/public/cover.png",
      era="❖  BAROQUE ERA",composer="Antonio Vivaldi",piece="Spring — I. Allegro",
      sub="The Four Seasons (1725)",out="era_arch_baroque_vivaldi.png"),
 dict(style="pointed",cover=BASE+"/works/elgar_salut_damour/video/visualizer/public/cover.png",
      era="❖  ROMANTIC ERA",composer="Edward Elgar",piece="Salut d'Amour",
      sub="Op. 12 (1888)",out="era_arch_romantic_elgar.png"),
 dict(style="segmental",cover=BASE+"/works/joplin_the_entertainer/video/visualizer/public/cover.png",
      era="❖  20TH CENTURY",composer="Scott Joplin",piece="The Entertainer",
      sub="A Ragtime Two-Step (1902)",out="era_arch_20c_joplin.png"),
]
for c in configs: render(c)
print("done")
