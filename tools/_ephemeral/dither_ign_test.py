"""IGN vs Bayer 디더 배경 — 인코딩 후 최종 비교 (scratch 2026-06-22)."""
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 2560, 1440
OUT = Path(__file__).parent
FF = r"C:\Users\user\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffmpeg.exe"
STOPS = ["#181614", "#6F6A60", "#D8D2C4"]

def hexrgb(h):
    h=h.lstrip("#"); return np.array([int(h[i:i+2],16) for i in (0,2,4)],np.float64)
def gradient_float():
    c0,c1,c2=(hexrgb(s) for s in STOPS); t=np.linspace(0,1,H); col=np.empty((H,3)); lo=t<=0.5
    col[lo]=c0*(1-(t[lo]/0.5)[:,None])+c1*((t[lo]/0.5)[:,None])
    a=((t[~lo]-0.5)/0.5)[:,None]; col[~lo]=c1*(1-a)+c2*a
    return np.repeat(col[:,None,:],W,axis=1)

def frac(x): return x-np.floor(x)
def ign_threshold():
    xv,yv=np.meshgrid(np.arange(W),np.arange(H))
    ign=frac(52.9829189*frac(0.06711056*xv+0.00583715*yv))  # 0~1 blue-noise-like
    return (ign-0.5)[:,:,None]
BAYER8=np.array([[0,32,8,40,2,34,10,42],[48,16,56,24,50,18,58,26],[12,44,4,36,14,46,6,38],
[60,28,52,20,62,30,54,22],[3,35,11,43,1,33,9,41],[51,19,59,27,49,17,57,25],
[15,47,7,39,13,45,5,37],[63,31,55,23,61,29,53,21]],np.float64)
def bayer_threshold():
    ty=(BAYER8+0.5)/64.0-0.5; return np.tile(ty,(H//8+1,W//8+1))[:H,:W,None]
def to8(a): return np.clip(np.round(a),0,255).astype(np.uint8)

g=gradient_float()
methods={
 "A plain":          to8(g),
 "B IGN 1LSB":       to8(g+ign_threshold()*1.0),
 "C IGN 2LSB":       to8(g+ign_threshold()*2.0),
 "D Bayer 1LSB":     to8(g+bayer_threshold()*1.0),
}
def enc(u8,tag):
    s=OUT/f"_i_{tag}.png"; m=OUT/f"_i_{tag}.mp4"; d=OUT/f"_id_{tag}.png"
    Image.fromarray(u8).save(s)
    subprocess.run([FF,"-y","-loop","1","-i",str(s),"-frames:v","1","-c:v","libx264","-crf","16","-pix_fmt","yuv420p",str(m)],check=True,capture_output=True)
    subprocess.run([FF,"-y","-i",str(m),"-frames:v","1",str(d)],check=True,capture_output=True)
    return np.array(Image.open(d).convert("RGB"))

y0,y1,x0,x1=120,760,80,470
crops={k:enc(v,k.split()[0])[y0:y1,x0:x1] for k,v in methods.items()}
h,wd,_=next(iter(crops.values())).shape; gap=6; top=46
im=Image.fromarray(np.full((h+top,wd*4+gap*3,3),18,np.uint8)); d=ImageDraw.Draw(im)
f=ImageFont.truetype(r"C:\Windows\Fonts\malgunbd.ttf",19)
for i,(k,c) in enumerate(crops.items()):
    x=i*(wd+gap); im.paste(Image.fromarray(c),(x,top)); d.text((x+5,13),k,fill=(255,255,255),font=f)
im.save(OUT/"dither_ign_compare.png"); print("saved",im.size)
