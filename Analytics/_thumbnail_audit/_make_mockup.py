# -*- coding: utf-8 -*-
"""Joplin thumbnail CTR mockups — fill-frame + Miku inset + bold title. s348 A 작업."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

COVER = "works/joplin_the_entertainer/video/cover/joplin_the_entertainer_album_1x1.png"
FONT  = "assets/fonts/gfs_didot/GFSDidot-Regular.ttf"
OUT   = "Analytics/_thumbnail_audit"
W, H = 1280, 720

cover = Image.open(COVER).convert("RGB")   # 1254x1254, Miku composited
cw, ch = cover.size

def fill_crop(img, tw, th, top_bias=0.0):
    """scale to cover tw x th, crop. top_bias 0=center, -1=keep top."""
    s = max(tw/img.width, th/img.height)
    nw, nh = int(img.width*s+0.5), int(img.height*s+0.5)
    r = img.resize((nw, nh), Image.LANCZOS)
    x = (nw-tw)//2
    y = int((nh-th)*(0.5 + top_bias*0.5))
    y = max(0, min(nh-th, y))
    return r.crop((x, y, x+tw, y+th))

def miku_inset(diam, ring_rgb, ring_w):
    # Miku region in 1254 cover: center ~ (0.65,0.24)
    x0,y0,x1,y1 = int(0.555*cw), int(0.085*ch), int(0.755*cw), int(0.40*ch)
    crop = cover.crop((x0,y0,x1,y1))
    # make square (center crop on width)
    side = min(crop.size)
    cx = (crop.width-side)//2
    crop = crop.crop((cx,0,cx+side,side)).resize((diam,diam), Image.LANCZOS)
    mask = Image.new("L",(diam,diam),0)
    ImageDraw.Draw(mask).ellipse((0,0,diam,diam),fill=255)
    out = Image.new("RGBA",(diam+2*ring_w,diam+2*ring_w),(0,0,0,0))
    d = ImageDraw.Draw(out)
    d.ellipse((0,0,diam+2*ring_w,diam+2*ring_w), fill=ring_rgb+(255,))
    out.paste(crop,(ring_w,ring_w),mask)
    return out

def fnt(sz): return ImageFont.truetype(FONT, sz)

def text_shadow(draw, xy, txt, font, fill=(255,255,255), sh=(0,0,0,180), off=4):
    x,y = xy
    draw.text((x+off,y+off), txt, font=font, fill=sh)
    draw.text((x,y), txt, font=font, fill=fill)

def wordmark(draw, x, y, sz):
    f=fnt(sz); parts=[("Atelier ",(238,236,228)),("M",(120,224,224)),("iku Acappella",(238,236,228))]
    cx=x
    for t,c in parts:
        draw.text((cx+2,y+2),t,font=f,fill=(0,0,0,160)); draw.text((cx,y),t,font=f,fill=c)
        cx+=draw.textlength(t,font=f)

# ---------- Variant 1: cinematic fill + left scrim + Miku inset right ----------
bg = fill_crop(cover, W, H, top_bias=-0.6).convert("RGBA")
# left vertical dark scrim for text legibility
scrim = Image.new("RGBA",(W,H),(0,0,0,0)); sd=ImageDraw.Draw(scrim)
for x in range(W):
    a = int(165*max(0,(1-x/620)))  # fade to 0 by x=620
    sd.line([(x,0),(x,H)], fill=(8,12,18,a))
bg = Image.alpha_composite(bg, scrim)
# bottom subtle gradient
bot=Image.new("RGBA",(W,H),(0,0,0,0)); bd=ImageDraw.Draw(bot)
for y in range(H):
    a=int(120*max(0,(y-470)/250)); bd.line([(0,y),(W,y)],fill=(8,10,14,a))
bg=Image.alpha_composite(bg,bot)
d=ImageDraw.Draw(bg)
text_shadow(d,(70,250),"Scott Joplin",fnt(46),fill=(214,210,196))
text_shadow(d,(66,300),"The Entertainer",fnt(118))
text_shadow(d,(72,430),"(1902)",fnt(44),fill=(206,200,184))
ins=miku_inset(300,(238,236,228),7)
bg.alpha_composite(ins,(W-ins.width-58,150))
d.text((W-ins.width-46,150+ins.height+4),"Hatsune Miku",font=fnt(30),fill=(238,236,228))
wordmark(d,70,H-66,38)
bg.convert("RGB").save(f"{OUT}/joplin_mockup_v1.jpg",quality=90)

# ---------- Variant 2: Miku-forward, big inset top-right, title bottom ----------
bg2 = fill_crop(cover, W, H, top_bias=-0.4).convert("RGBA")
# darken overall a touch + strong bottom band
ov=Image.new("RGBA",(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)
for y in range(H):
    a=int(40 + 175*max(0,(y-340)/380)); od.line([(0,y),(W,y)],fill=(6,9,13,min(220,a)))
bg2=Image.alpha_composite(bg2,ov)
d2=ImageDraw.Draw(bg2)
ins2=miku_inset(384,(120,224,224),8)
bg2.alpha_composite(ins2,(W-ins2.width-50,40))
d2.text((W-ins2.width-44,40+ins2.height-6),"Hatsune Miku",font=fnt(34),fill=(238,236,228))
text_shadow(d2,(66,486),"Scott Joplin",fnt(48),fill=(214,210,196))
text_shadow(d2,(62,540),"The Entertainer",fnt(120))
wordmark(d2,66,H-58,36)
bg2.convert("RGB").save(f"{OUT}/joplin_mockup_v2.jpg",quality=90)
print("saved v1, v2")
