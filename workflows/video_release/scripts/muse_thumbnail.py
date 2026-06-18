# -*- coding: utf-8 -*-
"""Atelier Miku Acappella 썸네일 생성기 — v5 양식 (코튼 LOCK s357) + v5.2 텍스트 헤일로 (코튼 LOCK 2026-06-11).

v5.2 (2026-06-11): 텍스트 렌더만 변경 — 4px 하드섀도 → 소프트 헤일로(blur7×3겹) + 2px 크리스프 섀도.
  사유 = 배경 명화에 따라 시인성 들쭉날쭉 (스크림이 텍스트 최상단에서 알파 ~10-30) → 글자 주변
  local 대비로 균일화. 스크림·사이즈·레이아웃·색 = v5 LOCK 그대로 (커버 불침범 — v5.1 적응형
  스크림 밴드는 '커버 잘리는 느낌'으로 코튼 반려). 라이브 8편 + ⑨ 일괄 재생성·스왑 (2026-06-11).

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
from PIL import Image, ImageDraw, ImageFilter, ImageFont

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
    "sugar_plum": dict(dir="tchaikovsky_sugar_plum_fairy",
                       cover="video/cover/album_1x1.png",
                       # box = gentle 우측 이동 (코튼 2026-06-06: 정중앙 미쿠 → 좌하단 텍스트 균형 위해 우측 12% 크롭 →
                       # 미쿠 얼굴 ~0.57 우측 배치). piece=hook 단축형 "Sugar Plum Fairy" · 풀네임 Tchaikovsky 풀사이즈 정합.
                       box=(0.0, 0.05, 0.88, 0.545), composer="Pyotr Ilyich Tchaikovsky", piece="Sugar Plum Fairy"),
    "boccherini_minuet": dict(dir="boccherini_minuet",
                       cover="video/cover/Miku_longhi_dancing_lesson_c1741_wga.png",
                       # box = 중앙 댄서 미쿠를 hero로 줌 (Longhi 다인 장면 → 미쿠 얼굴·상반신 확대 + 좌하단 텍스트
                       # 균형 위해 우측 배치). 코튼 헤드룸 미세조정 (2026-06-08): 0.05 과함→0.025 → "조금만 더 올려"
                       # → 0.0125 시프트 (y 0.10→0.0875·0.70→0.6875) = 리본 위 최소 여백. piece="Minuet" · 풀네임 Luigi Boccherini.
                       box=(0.12, 0.0875, 0.74, 0.6875), composer="Luigi Boccherini", piece="Minuet"),
    "handel_lascia": dict(dir="handel_lascia_chio_pianga",
                       cover="video/cover/Miku_rossetti_proserpine_1874_gap.png",
                       # box = B_wide (코튼 2026-06-11 · B2 얼굴우측 후보와 비교 후 확정): 얼굴 + 석류(서사 소품) +
                       # 담쟁이 + PROSERPINA 명문 패널 동시 생존. B2(우측 줌·box 0.0,0.14,0.76,0.5675)는 석류가
                       # 곡명 줄에 가려 반려 — 석류가 얼굴 바로 아래라 '얼굴 우측+석류' 양립 불가 구도.
                       box=(0.0, 0.04, 1.0, 0.72), composer="George Frideric Handel", piece="Lascia ch'io pianga"),
    "queen_of_night": dict(dir="mozart_queen_of_the_night",
                       cover="video/cover/schinkel_hall_of_stars_1815.png",
                       # box = 초승달 위 미쿠 밤의여왕 실루엣을 hero로 줌(트윈테일·왕관 읽힘). 인물이 silhouette →
                       # 짐노페디 선례처럼 初音ミク 텍스트가 인식 보강. 코튼 2026-06-18 "미쿠 미세 우측 이동(글자 덜 겹치게)"
                       # → box를 좌로 0.06 평행이동(중심 0.50→0.44) = 인물 우측 배치 + 좌하단 텍스트 클리어런스. piece="Queen of the Night"(통용명·인식 우선).
                       box=(0.06, 0.565, 0.82, 0.99), composer="W.A. Mozart", piece="Queen of the Night"),
    "haydn_trumpet": dict(dir="haydn_trumpet_concerto_finale",
                       cover="video/cover/Miku_strozzi_personification_of_fame_wga.png",
                       # box = T1_wide (코튼 2026-06-15 · T2 face-tight 후보와 비교 후 확정): 얼굴 大 + 트럼펫이
                       # 프레임 가로지르는 히어로 대각선(벨까지 온전) + 날개. T2(0.16,0.03,0.90,0.50)는 트럼펫 벨이
                       # 잘려 반려. piece="Trumpet Concerto"(Finale는 영상 제목에 · 썸네일 간결) · 풀네임 Joseph Haydn.
                       box=(0.10, 0.02, 1.0, 0.56), composer="Joseph Haydn", piece="Trumpet Concerto"),
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


def _draw_run(d, x, y, t, f, fill, track=None):
    """자간(track) 옵션 텍스트 1줄."""
    if track is None:
        d.text((x, y), t, font=f, fill=fill)
    else:
        for ch in t:
            d.text((x, y), ch, font=f, fill=fill)
            x += tw(ch, f) + track


def halo_text(base, items, blur=7, layers=3, alpha=200, off=2):
    """v5.2 텍스트 파이프라인 (코튼 LOCK 2026-06-11): 소프트 헤일로 + 미세 크리스프 섀도 + 본문.

    구 4px 하드섀도 대체. 헤일로 = 글자 주변 ~10px만 은은하게 어두워지는 local 대비
    → 배경(명화) 불침범 + 어떤 커버에서도 최소 가독 보장 (배경 의존 들쭉날쭉 해소).
    items = [(x, y, text, font, fill, track|None), ...]
    """
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for x, y, t, f, _fill, track in items:
        _draw_run(gd, x + 1, y + 2, t, f, (0, 0, 0, alpha), track)
    glow = glow.filter(ImageFilter.GaussianBlur(blur))
    out = base.convert("RGBA")
    for _ in range(layers):
        out = Image.alpha_composite(out, glow)
    d = ImageDraw.Draw(out)
    for x, y, t, f, fill, track in items:
        _draw_run(d, x + off, y + off, t, f, (0, 0, 0, 255), track)
        _draw_run(d, x, y, t, f, fill, track)
    return out.convert("RGB")


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

    # 좌측 시각 정렬: x = LEFT - 좌 side-bearing · 인라인(곡명·작곡가)은 같은 baseline
    x_inline = LEFT - pb[0]
    items = [
        (LEFT - mb[0], miku_y, "初音ミク", mf, IVORY, None),
        (LEFT - ab[0], aca_y, "A CAPPELLA", af, MINT, ACA_TRACK),
        (x_inline, piece_y, piece, pf, WHITE, None),
        (x_inline + tw(piece, pf) + 20, B_piece - asc_d, "·", df, DIM, None),
        (x_inline + tw(piece, pf) + 20 + tw("·", df) + 20, B_piece - asc_c, composer, cf, DIM, None),
    ]
    bg = halo_text(bg, items)

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
