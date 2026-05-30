"""s320 wordmark 통합 시안 — GFS Didot 직접 vector render path (banner crop 폐기).

이전 cycle (s319 v1~v37) 자가 결함:
  banner crop 양식 자체엔 light-bg-dark-text 자료 → letterbox dark-bg 위 invert/cream 어떤 변환 박아도
  *M* 청록 + *Atelier · iku Acappella* dark ink 양식 자체엔 contrast 충돌. 본 path 자체엔 본질 양식 미정합.

본 cycle path:
  GFS Didot-Regular.ttf 직접 text render → 단일 cream 색 → letterbox warm dark brown 위 contrast 통과
  시그너처 §1 (typeface 1종 GFS Didot) + §3 v2 (wordmark text · 우상단 corner) doctrine 정합.

자리 axis (시그너처 §3 v2):
  placement = 우상단 corner (frame 안쪽 padding ~3-5%)
  size default = 좌하단 title height의 ~50-60% (label 자리 본질 — 작아야 함)
  color = cream (letterbox dark 위 contrast 통과) · #e8e0c8 base
  weight = regular (강조 X · 명화 압도 회피)
  alignment = right
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

BASE = Path(__file__).parent
FRAME = BASE / "_frame_5s.png"
FONT = BASE.parent.parent.parent.parent / "assets" / "fonts" / "gfs_didot" / "GFSDidot-Regular.ttf"

FRAME_W = 1920
FRAME_H = 1080
PADDING_TOP = 72       # frame 안쪽 ~6.7% (시그너처 axis 3-5% range 자가 점검)
PADDING_RIGHT = 72     # frame 안쪽 ~3.75%

WORDMARK_TEXT = "Atelier Miku Acappella"
CREAM = (232, 224, 200)            # #e8e0c8 · 좌하단 text 색 정합 (시그너처 §1 typo color 일치)
SHADOW_RGBA = (0, 0, 0, 160)       # 약한 soft shadow · 명화 일부 위 박힐 risk 대비


def render_wordmark(text: str, font_size: int, color: tuple = CREAM,
                    shadow_blur: int = 6, shadow_offset_y: int = 2,
                    shadow_alpha: int = 160) -> Image.Image:
    """GFS Didot vector render + 약한 soft shadow (안전 자리용)."""
    font = ImageFont.truetype(str(FONT), font_size)

    # text bbox 측정
    tmp = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
    draw_tmp = ImageDraw.Draw(tmp)
    bbox = draw_tmp.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # shadow padding 자체엔 blur axis 자체 자리 보장
    pad = shadow_blur * 3 + max(shadow_offset_y, 1) + 4
    canvas_w = text_w + pad * 2
    canvas_h = text_h + pad * 2

    # shadow layer
    shadow_layer = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    sd_draw = ImageDraw.Draw(shadow_layer)
    sd_draw.text((pad - bbox[0], pad - bbox[1] + shadow_offset_y), text,
                 font=font, fill=(0, 0, 0, shadow_alpha))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(shadow_blur))

    # text layer
    text_layer = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    tx_draw = ImageDraw.Draw(text_layer)
    tx_draw.text((pad - bbox[0], pad - bbox[1]), text,
                 font=font, fill=color + (255,))

    # composite
    out = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    out.paste(shadow_layer, (0, 0), shadow_layer)
    out.paste(text_layer, (0, 0), text_layer)
    return out


def paste_top_right(frame: Image.Image, wm: Image.Image) -> Image.Image:
    """우상단 corner paste · padding axis 정합."""
    result = frame.copy().convert("RGBA")
    wm_w, wm_h = wm.size

    # right-aligned · top-padded
    x = FRAME_W - wm_w + (wm_w - wm.getbbox()[2] if wm.getbbox() else 0)
    # bbox right-aligned axis 자체엔 padding 안에서 visible 글자 우측 정합
    bbox = wm.getbbox()
    if bbox:
        text_right_in_canvas = bbox[2]
        x = FRAME_W - PADDING_RIGHT - text_right_in_canvas
        y = PADDING_TOP - bbox[1]
    else:
        x = FRAME_W - wm_w - PADDING_RIGHT
        y = PADDING_TOP

    result.paste(wm, (x, y), wm)
    return result.convert("RGB")


def main():
    frame = Image.open(FRAME)

    # size 3 variation
    # 좌하단 title "Spring, Mvt. I" 자체엔 ~44px (자가 측정 axis · 후속 정정 path)
    # default = title height 50-60% = ~22-26px range
    variants = [
        ("v38_vector_size22", 22, "small · label 자리 본질"),
        ("v38_vector_size26", 26, "medium · default axis · MOKA 추천 첫 자리"),
        ("v38_vector_size32", 32, "large · brand visibility 강화 axis"),
    ]

    for name, size, note in variants:
        wm = render_wordmark(WORDMARK_TEXT, font_size=size)
        out = paste_top_right(frame, wm)
        path = BASE / f"_{name}.png"
        out.save(path)
        print(f"  → {path.name} ({note})")


if __name__ == "__main__":
    main()
