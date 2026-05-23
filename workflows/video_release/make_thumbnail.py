# -*- coding: utf-8 -*-
"""Atelier Miku Acappella 썸네일 생성기 — v4 양식 (코튼 LOCK s348).

v4 양식:
  - 커버 속 미쿠를 줌(crop)해서 주인공으로 (인셋·텍스트 라벨 X — "썸네일은 그림으로 말한다")
  - 좌하단 제목 블록 = 작곡가(소) / 곡명(대) / Atelier Miku Acappella 워드마크
  - 줄 간격 = 디센더(p·é·g 등 글자 꼬리)까지 실측해 띄움 (제목↔워드마크 겹침 방지)
  - 하단 그라데이션 스크림으로 텍스트 가독성 확보

per-song 가변값 = `box` (커버 안에서 미쿠를 잡는 crop 영역, 0~1 비율). 신곡은 커버를 보고 box를 정함.
업로드는 별도 도구: `Analytics/youtube_meta.py set-thumbnail <video_id> <out.jpg>`.

사용:
  python workflows/video_release/make_thumbnail.py --song salut
  python workflows/video_release/make_thumbnail.py --cover <path> --box 0.2,0.0,1.0,0.55 \
         --composer "Edward Elgar" --piece "Salut d'Amour" --out <out.jpg>
"""
import sys
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE = Path(__file__).resolve().parents[2]          # Project_Muse/
FONT = BASE / "assets/fonts/gfs_didot/GFSDidot-Regular.ttf"
W, H = 1280, 720

# per-song registry. box = (x0,y0,x1,y1) 0~1, 커버 안에서 미쿠를 주인공으로 잡는 영역.
REGISTRY = {
    "gymnopedie": dict(dir="gymnopedie_1_first_proof",
                       cover="video/visualizer/public/cover.png",
                       box=(0.16, 0.26, 0.98, 0.99), composer="Erik Satie", piece="Gymnopédie No. 1"),
    "vivaldi":    dict(dir="vivaldi_spring_1_allegro",
                       cover="video/cover/album_1x1.png",
                       box=(0.21, 0.22, 0.93, 0.62), composer="Antonio Vivaldi", piece="Spring, Mvt. I"),
    "joplin":     dict(dir="joplin_the_entertainer",
                       cover="video/cover/joplin_the_entertainer_album_1x1.png",
                       box=(0.16, 0.00, 1.00, 0.52), composer="Scott Joplin", piece="The Entertainer"),
    "salut":      dict(dir="elgar_salut_damour",
                       cover="video/cover/Miku_waterhouse_soul_of_the_rose.png",
                       box=(0.00, 0.04, 1.00, 0.80), composer="Edward Elgar", piece="Salut d'Amour"),
}

_probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
def fnt(sz): return ImageFont.truetype(str(FONT), sz)
def tw(t, f): return _probe.textlength(t, font=f)

def fit(text, maxw, start=122, lo=60):
    for sz in range(start, lo - 1, -2):
        if tw(text, fnt(sz)) <= maxw:
            return fnt(sz)
    return fnt(lo)

def sub_then_fill(img, box01):
    x0, y0, x1, y1 = box01
    sub = img.crop((int(x0*img.width), int(y0*img.height), int(x1*img.width), int(y1*img.height)))
    s = max(W/sub.width, H/sub.height)
    r = sub.resize((int(sub.width*s+0.5), int(sub.height*s+0.5)), Image.LANCZOS)
    x, y = (r.width-W)//2, (r.height-H)//2
    return r.crop((x, y, x+W, y+H))

def bottom_scrim(bg, start=350):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    for y in range(H):
        a = int(205 * max(0, (y-start)/(H-start)))
        od.line([(0, y), (W, y)], fill=(6, 9, 13, a))
    return Image.alpha_composite(bg.convert("RGBA"), ov).convert("RGB")

def tsh(d, xy, t, f, fill=(255, 255, 255), off=4):
    x, y = xy
    d.text((x+off, y+off), t, font=f, fill=(0, 0, 0, 170))
    d.text((x, y), t, font=f, fill=fill)

def wordmark(d, x, y, sz=38):
    f = fnt(sz)
    for t, c in [("Atelier ", (232, 230, 222)), ("M", (120, 224, 224)), ("iku Acappella", (232, 230, 222))]:
        d.text((x+2, y+2), t, font=f, fill=(0, 0, 0, 150))
        d.text((x, y), t, font=f, fill=c)
        x += tw(t, f)

def render(cover_path, box, composer, piece, out_path):
    bg = sub_then_fill(Image.open(cover_path).convert("RGB"), box)
    bg = bottom_scrim(bg, start=350)
    d = ImageDraw.Draw(bg)
    comp_f, big_f, wm_f = fnt(46), fit(piece, W - 150), fnt(38)
    # 디센더 포함 ink bbox 측정 → 아래(워드마크)부터 위로 스택, 줄 사이 실측 간격 GAP 보장.
    cb = _probe.textbbox((0, 0), composer, font=comp_f)
    pb = _probe.textbbox((0, 0), piece, font=big_f)
    wb = _probe.textbbox((0, 0), "Atelier Miku Acappella", font=wm_f)
    GAP, GAP2 = 22, 12
    wm_y = (H - 26) - wb[3]
    big_y = (wm_y + wb[1]) - GAP - pb[3]
    comp_y = (big_y + pb[1]) - GAP2 - cb[3]
    tsh(d, (70, comp_y), composer, comp_f, fill=(216, 212, 198))
    tsh(d, (66, big_y), piece, big_f)
    wordmark(d, 72, wm_y)
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    bg.save(out_path, quality=92)
    print(f"✓ {out_path}")

def main():
    p = argparse.ArgumentParser(description="Atelier Miku Acappella v4 썸네일 생성기")
    p.add_argument("--song", choices=list(REGISTRY), help="등록된 곡 (registry 사용)")
    p.add_argument("--cover"); p.add_argument("--box", help="x0,y0,x1,y1 (0~1)")
    p.add_argument("--composer"); p.add_argument("--piece"); p.add_argument("--out")
    a = p.parse_args()
    if a.song:
        c = REGISTRY[a.song]
        cover = BASE / "works" / c["dir"] / c["cover"]
        out = a.out or (BASE / "works" / c["dir"] / "video" / "thumbnail_v4.jpg")
        render(cover, c["box"], c["composer"], c["piece"], out)
    else:
        if not all([a.cover, a.box, a.composer, a.piece, a.out]):
            p.error("--song 또는 (--cover --box --composer --piece --out) 전부 필요")
        box = tuple(float(v) for v in a.box.split(","))
        render(a.cover, box, a.composer, a.piece, a.out)

if __name__ == "__main__":
    main()
