"""인코딩이 디더를 보존하는가 — background.png를 여러 H.264 설정으로 인코딩 후 비교.
소스(디더 배경)는 OK인데 렌더 클립엔 띠 → 인코딩 단계가 범인. 어떤 설정이 디더를 살리나."""
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).parent
FF = r"C:\Users\user\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffmpeg.exe"
BG = r"C:\Users\user\Desktop\myProject\Project_Muse\works\handel_lascia_chio_pianga\video\visualizer\public\background.png"

# (라벨, 추가 인코딩 인자)
configs = [
    ("A crf16 420p (현재)",   ["-c:v","libx264","-crf","16","-pix_fmt","yuv420p"]),
    ("B crf12 420p",          ["-c:v","libx264","-crf","12","-pix_fmt","yuv420p"]),
    ("C crf16 +tune grain",   ["-c:v","libx264","-crf","16","-pix_fmt","yuv420p","-tune","grain"]),
    ("D crf16 444p",          ["-c:v","libx264","-crf","16","-pix_fmt","yuv444p"]),
    ("E 10bit 420p crf16",    ["-c:v","libx264","-crf","16","-pix_fmt","yuv420p10le","-profile:v","high10"]),
    ("F crf16 +tune grain 10bit", ["-c:v","libx264","-crf","16","-pix_fmt","yuv420p10le","-profile:v","high10","-tune","grain"]),
]

def enc(args, tag):
    m = OUT/f"_e_{tag}.mp4"; d = OUT/f"_ed_{tag}.png"
    subprocess.run([FF,"-y","-loop","1","-i",BG,"-frames:v","1",*args,str(m)],check=True,capture_output=True)
    subprocess.run([FF,"-y","-i",str(m),"-frames:v","1",str(d)],check=True,capture_output=True)
    return np.array(Image.open(d).convert("RGB"))

y0,y1,x0,x1 = 120,760,80,470   # 어두운 상단
crops={}
src = np.array(Image.open(BG).convert("RGB"))[y0:y1,x0:x1]
crops["SRC 원본PNG"] = src
for lab,a in configs:
    crops[lab] = enc(a, lab.split()[0])[y0:y1,x0:x1]

cols = len(crops)
h,wd,_ = src.shape; gap=6; top=44
im = Image.fromarray(np.full((h+top, wd*cols+gap*(cols-1),3),18,np.uint8)); d=ImageDraw.Draw(im)
f = ImageFont.truetype(r"C:\Windows\Fonts\malgunbd.ttf",16)
for i,(k,c) in enumerate(crops.items()):
    x=i*(wd+gap); im.paste(Image.fromarray(c),(x,top)); d.text((x+4,12),k,fill=(255,255,255),font=f)
im.save(OUT/"encode_preserve_compare.png"); print("saved", im.size)
