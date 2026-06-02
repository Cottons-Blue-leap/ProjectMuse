# -*- coding: utf-8 -*-
"""Atelier Miku Acappella 썸네일 생성기 — v5 양식 (코튼 LOCK s357).

v5 양식 (3-정보 · 좌하단 단일 블록):
  ① 명화 커버 배경 (커버 속 미쿠를 box로 줌)
  ② 악곡 정보 = 곡명(大) · 작곡가(소) 한 줄 (middot 구분 · baseline 정렬)
  ③ 미쿠·아카펠라 = 初音ミク(아이보리) / A CAPPELLA(민트) 배지
  레이아웃:
    初音ミク           ← Yu Mincho · 아이보리 (JP 인식)
    A CAPPELLA        ← Didot 대문자 자간 · 민트 (포맷 · 영문대문자=작은화면 즉독)
    Salut d'Amour · Edward Elgar   ← Didot · 곡명 흰색 大 + middot + 작곡가 흐림 小
  - 좌측 시각 정렬(좌 side-bearing 보정) · 인라인 baseline 정렬 · 배지/타이틀 2단 여유(22/34)
  - 하단 그라데이션 스크림으로 어떤 명화에서도 가독 확보 (별도 박스 없이 = 앨범커버 결 유지)

이전 v4(워드마크·민트 2줄·상단배지)는 폐기. 기존 thumbnail_v4.jpg는 롤백용 보존(덮어쓰지 않음).
per-song 가변값 = `box`(커버 안 미쿠 crop 0~1) + composer + piece. 신곡은 커버 보고 box 정함.
업로드: `Analytics/youtube_meta.py set-thumbnail <video_id> <out.jpg>`.

사용:
  python workflows/video_release/scripts/muse_thumbnail.py --song salut
  python workflows/video_release/scripts/muse_thumbnail.py --all
  python workflows/video_release/scripts/muse_thumbnail.py --cover <p> --box x0,y0,x1,y1 \
         --composer "Edward Elgar" --piece "Salut d'Amour" --out <out.jpg>
"""
import sys
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE = Path(__file__).resolve().parents[3]          # Project_Muse/ (scripts/→video_release/→workflows/→root)
DIDOT = str(BASE / "assets/fonts/gfs_didot/GFSDidot-Regular.ttf")
# 일본어 글리프용 = Yu Mincho Regular (Windows 시스템 폰트 · MS 라이선스라 repo 미동봉).
# 다른 환경이면 명조 계열 .ttf/.ttc 경로로 교체.
JP_MINCHO = r"C:\Windows\Fonts\yumin.ttf"

W, H = 1280, 720
IVORY = (245, 243, 235)
MINT  = (139, 223, 206)
DIM   = (196, 192, 178)
WHITE = (255, 255, 255)

LEFT        = 72    # 공통 시각 좌측선
# 세로는 baseline(폰트 메트릭 · 크기당 상수)에 앵커링 = 글자(디센더) 무관 → 시리즈 픽셀 동일.
BASE_MARGIN = 44    # 곡명 baseline = H - BASE_MARGIN (하단 여백)
LEAD_TITLE  = 98    # 곡명 → A CAPPELLA baseline 간격
LEAD_BADGE  = 69    # A CAPPELLA → 初音ミク baseline 간격
# 크기 고정 (s357 LOCK · 곡 바뀌어도 동일)
F_MIKU, F_ACA, F_PIECE, F_COMP, F_DOT = 108, 60, 92, 36, 44
ACA_TRACK = 8       # A CAPPELLA 자간

# per-song registry. box=(x0,y0,x1,y1) 0~1, 커버 안에서 미쿠를 주인공으로 잡는 영역.
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
    "mozart_twinkle_variations": dict(dir="mozart_twinkle_variations_k265",
                       cover="video/cover/album_1x1.png",
                       box=(0.30, 0.40, 1.00, 1.00), composer="W.A. Mozart", piece="Twinkle Twinkle Variations"),
    "chopin":     dict(dir="chopin_nocturne_op9_2",
                       cover="video/cover/album_1x1.png",
                       box=(0.30, 0.40, 1.00, 1.00), composer="Frédéric Chopin", piece="Nocturne Op. 9 No. 2"),
    "pachelbel":  dict(dir="pachelbel_canon_in_d",
                       cover="video/cover/album_1x1.png",
                       # box = v8 노래 커버 (코튼 s389: 우측 이동 + 중앙기준 약간 확대 = 중심 0.52 기준 박스 ~7% 축소)
                       box=(0.13, 0.13, 0.91, 0.90), composer="Johann Pachelbel", piece="Canon in D"),
}

_probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
def didot(sz): return ImageFont.truetype(DIDOT, sz)
def mincho(sz): return ImageFont.truetype(JP_MINCHO, sz, index=0)
def tw(t, f): return _probe.textlength(t, font=f)
def bbox(t, f): return _probe.textbbox((0, 0), t, font=f)


def sub_then_fill(img, box01):
    x0, y0, x1, y1 = box01
    sub = img.crop((int(x0*img.width), int(y0*img.height), int(x1*img.width), int(y1*img.height)))
    s = max(W/sub.width, H/sub.height)
    r = sub.resize((int(sub.width*s+0.5), int(sub.height*s+0.5)), Image.LANCZOS)
    x, y = (r.width-W)//2, (r.height-H)//2
    return r.crop((x, y, x+W, y+H))


def scrim(bg, start, amax=226):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    for y in range(H):
        a = int(amax * max(0, (y-start)/(H-start)))
        od.line([(0, y), (W, y)], fill=(6, 9, 13, a))
    return Image.alpha_composite(bg.convert("RGBA"), ov).convert("RGB")


def sh(d, x, y, t, f, fill, off=4):
    """드롭섀도 + 본 텍스트."""
    d.text((x+off, y+off), t, font=f, fill=(0, 0, 0))
    d.text((x, y), t, font=f, fill=fill)


def sh_sp(d, x, y, t, f, fill, sp, off=4):
    """자간 적용 드롭섀도 텍스트."""
    for ch in t:
        d.text((x+off, y+off), ch, font=f, fill=(0, 0, 0))
        d.text((x, y), ch, font=f, fill=fill)
        x += tw(ch, f) + sp


def render(cover_path, box, composer, piece, out_path):
    bg = sub_then_fill(Image.open(cover_path).convert("RGB"), box)
    mf, af = mincho(F_MIKU), didot(F_ACA)
    # 인라인(piece · composer · middot) = 폭 초과 시 비례 축소 fallback (s361 박힘 · 작은별 K.265 = 첫 적용 곡).
    # 본질 = *잘림이 축소보다 양식 깸이 더 강 axis* + 다른 곡 영향 0 (폭 안 자리 곡은 default LOCK keep).
    piece_sz, comp_sz, dot_sz = F_PIECE, F_COMP, F_DOT
    pf, cf, df = didot(piece_sz), didot(comp_sz), didot(dot_sz)
    pb = bbox(piece, pf)
    inline_w = tw(piece, pf) + 20 + tw("·", df) + 20 + tw(composer, cf)
    inline_target_w = (W - 24) - (LEFT - pb[0])
    if inline_w > inline_target_w:
        scale = inline_target_w / inline_w
        piece_sz, comp_sz, dot_sz = int(F_PIECE*scale), int(F_COMP*scale), int(F_DOT*scale)
        pf, cf, df = didot(piece_sz), didot(comp_sz), didot(dot_sz)
        pb = bbox(piece, pf)
        inline_w_new = tw(piece, pf) + 20 + tw("·", df) + 20 + tw(composer, cf)
        print(f"  ↳ 인라인 폭 자동 축소 scale={scale:.3f} · {int(inline_w)}px → {int(inline_w_new)}px · "
              f"F_PIECE {F_PIECE}→{piece_sz} · F_COMP {F_COMP}→{comp_sz}")

    # bbox[0]=좌 side-bearing(가로 정렬용 · 글자별 OK) · tw=가로 진행폭. 세로엔 미사용(메트릭만).
    mb, ab = bbox("初音ミク", mf), bbox("A CAPPELLA", af)
    asc_p, asc_a, asc_m = pf.getmetrics()[0], af.getmetrics()[0], mf.getmetrics()[0]
    asc_c, asc_d = cf.getmetrics()[0], df.getmetrics()[0]

    # 세로 = 고정 baseline (글자 무관 = 모든 곡 픽셀 동일). draw y(셀 상단) = baseline - ascent.
    B_piece = H - BASE_MARGIN
    B_aca   = B_piece - LEAD_TITLE
    B_miku  = B_aca - LEAD_BADGE
    piece_y, aca_y, miku_y = B_piece - asc_p, B_aca - asc_a, B_miku - asc_m

    bg = scrim(bg, miku_y - 46)
    d = ImageDraw.Draw(bg)

    # 좌측 시각 정렬: x = LEFT - 좌 side-bearing
    sh(d, LEFT - mb[0], miku_y, "初音ミク", mf, IVORY)
    sh_sp(d, LEFT - ab[0], aca_y, "A CAPPELLA", af, MINT, ACA_TRACK)

    # 인라인 타이틀 (곡명 · 작곡가 — 같은 baseline)
    x = LEFT - pb[0]
    sh(d, x, piece_y, piece, pf, WHITE)
    x += tw(piece, pf) + 20
    sh(d, x, B_piece - asc_d, "·", df, DIM)
    x += tw("·", df) + 20
    sh(d, x, B_piece - asc_c, composer, cf, DIM)

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    bg.save(out_path, quality=92)
    print(f"✓ {out_path}")


def render_song(key, out=None):
    c = REGISTRY[key]
    cover = BASE / "works" / c["dir"] / c["cover"]
    out = out or (BASE / "works" / c["dir"] / "video" / "thumbnail_v5.jpg")
    render(cover, c["box"], c["composer"], c["piece"], out)


def main():
    p = argparse.ArgumentParser(description="Atelier Miku Acappella v5 썸네일 생성기")
    p.add_argument("--song", choices=list(REGISTRY), help="등록된 곡 (registry)")
    p.add_argument("--all", action="store_true", help="등록된 4곡 전부")
    p.add_argument("--cover"); p.add_argument("--box", help="x0,y0,x1,y1 (0~1)")
    p.add_argument("--composer"); p.add_argument("--piece"); p.add_argument("--out")
    a = p.parse_args()
    if a.all:
        for k in REGISTRY:
            render_song(k)
    elif a.song:
        render_song(a.song, a.out)
    else:
        if not all([a.cover, a.box, a.composer, a.piece, a.out]):
            p.error("--all / --song / (--cover --box --composer --piece --out) 중 하나 필요")
        box = tuple(float(v) for v in a.box.split(","))
        render(a.cover, box, a.composer, a.piece, a.out)


if __name__ == "__main__":
    main()
