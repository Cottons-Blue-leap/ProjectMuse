# -*- coding: utf-8 -*-
"""
Project Muse — v5: era arches BUT cover shown in FULL (no cropping). (s356, 코튼 feedback)
Fix: arch no longer masks/crops the painting. Instead —
  - arch interior filled with a soft BLURRED bleed of the painting (ambiance, not void)
  - the FULL painting (contain-fit, uncropped) sits sharply inside, fully identifiable
  - gold arch frame + thin gold frame around the painting + era ornament
Era arch silhouettes kept (rounded / pointed / segmental). Paper texture overlay.
"""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, ImageEnhance

BASE = r"C:/Users/user/Desktop/myProject/Project_Muse"
FONT = BASE + "/assets/fonts/gfs_didot/GFSDidot-Regular.ttf"
OUT_DIR = BASE + "/exploration/visualizer_mockup"
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 1920, 1080
CREAM=(232,224,200); TEAL=(40,180,175); GOLD=(201,169,106); MUTED=(140,138,146)
def font(sz): return ImageFont.truetype(FONT, sz)

AX0, AX1, AY1 = 90, 1040, 1010          # arch left/right, bottom
APEX = 70                                # arch top (apex y)
R = (AX1-AX0)/2.0; CX=(AX0+AX1)/2.0
DOME = {"rounded":210.0, "pointed":280.0, "segmental":120.0}

yy, xx = np.mgrid[0:H, 0:W]

def spring_of(style): return APEX + DOME[style]

def arch_mask(style):
    spring = spring_of(style)
    body = (xx>=AX0)&(xx<=AX1)&(yy>=spring)&(yy<=AY1)
    dh = DOME[style]
    if style=="pointed":
        Rg=900.0
        dL=np.sqrt((xx-AX0)**2+(yy-spring)**2); dR=np.sqrt((xx-AX1)**2+(yy-spring)**2)
        # scale so apex reaches APEX: use ellipse-pointed via two ellipses approx -> fallback: intersection of two big circles centered beyond springpoints
        cyo = spring + (R**2 - dh**2)/(2*dh) if dh< R else spring  # circle through corners+apex
        rad = spring - APEX + (cyo-spring)
        top=(yy<spring)&(xx>=AX0)&(xx<=AX1)& \
            (np.sqrt((xx-AX0)**2+(yy-cyo)**2)<=rad)&(np.sqrt((xx-AX1)**2+(yy-cyo)**2)<=rad)
    else:
        top=(yy<spring)&(xx>=AX0)&(xx<=AX1)&(((xx-CX)/R)**2+((yy-spring)/dh)**2<=1)
    return Image.fromarray(((body|top).astype("uint8")*255),"L")

def contain(im, bw, bh):
    s=min(bw/im.width, bh/im.height)
    return im.resize((max(1,int(im.width*s)), max(1,int(im.height*s))), Image.LANCZOS)
def cover(im, bw, bh):
    s=max(bw/im.width, bh/im.height)
    im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
    l=(im.width-bw)//2; t=(im.height-bh)//2
    return im.crop((l,t,l+bw,t+bh))

roles=[("I","Ah",(216,184,120),True),("II","Ah",(201,143,143),False),
       ("III","Oo",(95,185,179),True),("IV","Oo",(159,185,143),False),
       ("V","Oo",(210,160,96),True),("VI","Mm",(176,168,196),True)]

def render(cfg):
    style=cfg["style"]; cv0=Image.open(cfg["cover"]).convert("RGB")
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

    spring=spring_of(style); mask=arch_mask(style)
    # blurred bleed fill inside arch (ambiance)
    bleed=cover(cv0, AX1-AX0, AY1-APEX).filter(ImageFilter.GaussianBlur(24))
    bleed=ImageEnhance.Brightness(bleed).enhance(0.62)
    bl=Image.new("RGBA",(W,H),(0,0,0,0)); bl.paste(bleed,(AX0,APEX)); img.paste(bl,(0,0),mask)
    # sharp FULL painting (contain, uncropped) centered in body
    bx0,bx1=AX0+30, AX1-30; by0,by1=spring+8, AY1-30
    sharp=contain(cv0, bx1-bx0, by1-by0)
    px=int((bx0+bx1)/2 - sharp.width/2); py=int((by0+by1)/2 - sharp.height/2)
    img.paste(sharp,(px,py))
    d=D(); d.rectangle([px-3,py-3,px+sharp.width+3,py+sharp.height+3],outline=GOLD+(230,),width=2)
    # gold arch frame from mask (shape-agnostic)
    for (oz,a) in [(9,235),(0,0)]:
        if oz:
            band=ImageChops.subtract(mask, mask.filter(ImageFilter.MinFilter(oz)))
            gl=Image.new("RGBA",(W,H),GOLD+(a,)); img.paste(gl,(0,0),band)
    band2=ImageChops.subtract(mask.filter(ImageFilter.MinFilter(23)),mask.filter(ImageFilter.MinFilter(29)))
    gl=Image.new("RGBA",(W,H),GOLD+(150,)); img.paste(gl,(0,0),band2)
    # era ornament near apex
    d=D()
    if style=="rounded":
        d.rounded_rectangle([CX-24,APEX+8,CX+24,APEX+50],radius=7,outline=GOLD+(230,),width=3)
    elif style=="pointed":
        d.line([(CX,APEX-6),(CX,APEX+46)],fill=GOLD+(220,),width=3)
        d.line([(CX-15,APEX+16),(CX+15,APEX+16)],fill=GOLD+(220,),width=3)
    else:
        d.ellipse([CX-7,APEX+10,CX+7,APEX+26],outline=GOLD+(220,),width=2)

    # 6 panels
    gx0,gy0=1120,118; cw,ch,gap=348,232,26
    f_num,f_vow,f_mk=font(40),font(18),font(15)
    for i,(num,vowel,color,active) in enumerate(roles):
        x0=gx0+(i%2)*(cw+gap); y0=gy0+(i//2)*(ch+gap); x1,y1=x0+cw,y0+ch
        gl=Image.new("RGBA",(W,H),(0,0,0,0)); gdd=ImageDraw.Draw(gl)
        gdd.rounded_rectangle([x0,y0,x1,y1],radius=8,fill=color+(150 if active else 55,))
        if active: img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(18)))
        img.alpha_composite(gl); d=D()
        d.rounded_rectangle([x0,y0,x1,y1],radius=8,outline=(20,18,16,235),width=6)
        d.rounded_rectangle([x0+6,y0+6,x1-6,y1-6],radius=6,outline=(GOLD if active else MUTED)+(210,),width=2)
        mcx,mcy=(x0+x1)/2,(y0+y1)/2; tc=CREAM if active else MUTED
        nn=d.textlength(num,font=f_num); d.text((mcx-nn/2,mcy-34),num,font=f_num,fill=tc+(255,))
        vw=d.textlength(vowel,font=f_vow); d.text((mcx-vw/2,mcy+18),vowel,font=f_vow,fill=(TEAL if active else MUTED)+(220,))
        mw=d.textlength("MIKU",font=f_mk); d.text((mcx-mw/2,y0+12),"MIKU",font=f_mk,fill=tc+(180,))

    # wordmark + era + title
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

    # paper texture
    base=img.convert("RGB"); arr=np.asarray(base).astype(float)
    noise=Image.effect_noise((W,H),30).filter(ImageFilter.GaussianBlur(0.6))
    low=Image.effect_noise((W,H),18).resize((W//6,H//6)).resize((W,H)).filter(ImageFilter.GaussianBlur(2))
    n=(np.asarray(noise).astype(float)+np.asarray(low).astype(float))/2.0
    mult=0.88+0.20*(n/255.0); out=np.clip(arr*mult[...,None],0,255)
    out[...,0]=np.clip(out[...,0]*1.012,0,255); out[...,2]=np.clip(out[...,2]*0.99,0,255)
    p=OUT_DIR+"/"+cfg["out"]; Image.fromarray(out.astype("uint8")).save(p,"PNG"); print("saved:",p)

configs=[
 dict(style="rounded",cover=BASE+"/works/vivaldi_spring_1_allegro/video/visualizer/public/cover.png",
      era="❖  BAROQUE ERA",composer="Antonio Vivaldi",piece="Spring — I. Allegro",
      sub="The Four Seasons (1725)",out="v5_baroque_vivaldi.png"),
 dict(style="pointed",cover=BASE+"/works/elgar_salut_damour/video/visualizer/public/cover.png",
      era="❖  ROMANTIC ERA",composer="Edward Elgar",piece="Salut d'Amour",
      sub="Op. 12 (1888)",out="v5_romantic_elgar.png"),
 dict(style="segmental",cover=BASE+"/works/joplin_the_entertainer/video/visualizer/public/cover.png",
      era="❖  20TH CENTURY",composer="Scott Joplin",piece="The Entertainer",
      sub="A Ragtime Two-Step (1902)",out="v5_20c_joplin.png"),
]
for c in configs: render(c)
print("done")
