"""s320 v40 시안 — size 40 + *M* 청록 (banner color) + text-shadow keep.

코튼 결단 (s320 2 axis):
  1. v40 size (40) 자체엔 좋음
  2. 왼편 text-shadow 양식 자체엔 동일 적용 (이미 v39에서 적용 박힘 · keep)
  3. *Miku*의 *M* 자체엔 banner 청록색 (40,180,175) 적용

자료 base axis:
  text = "Atelier Miku Acappella"
  char 양식 = "Atelier " (8 cream) + "M" (teal) + "iku Acappella" (13 cream)
  banner *M* color 자체엔 _banner_textshadow_mockup.py 안 TEAL = (40, 180, 175)
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = Path(__file__).parent
FRAME = BASE / "_frame_5s.png"
FONT = BASE.parent.parent.parent.parent / "assets" / "fonts" / "gfs_didot" / "GFSDidot-Regular.ttf"

FRAME_W = 1920
FRAME_H = 1080
MARGIN_RIGHT = 81
MARGIN_BOTTOM = 90

WORDMARK_TEXT = "Atelier Miku Acappella"
CREAM = (232, 224, 200)      # #e8e0c8
TEAL = (40, 180, 175)        # banner *M* color (RGB)

SHADOW_BLUR = 12
SHADOW_OFFSET_Y = 2
SHADOW_ALPHA = 192

FONT_SIZE = 40


def render_wordmark_m_teal(text: str, font_size: int) -> Image.Image:
    """GFS Didot vector render · *Miku*의 *M*만 청록 · 나머지 cream · text-shadow Gaussian."""
    font = ImageFont.truetype(str(FONT), font_size)

    # full text bbox (positioning base)
    tmp = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
    draw_tmp = ImageDraw.Draw(tmp)
    full_bbox = draw_tmp.textbbox((0, 0), text, font=font)
    text_w = full_bbox[2] - full_bbox[0]
    text_h = full_bbox[3] - full_bbox[1]

    pad = SHADOW_BLUR * 3 + max(SHADOW_OFFSET_Y, 1) + 4
    canvas_w = text_w + pad * 2
    canvas_h = text_h + pad * 2

    # *M* index 자체엔 "Atelier " (8 chars + 1 space) 다음 자리 = index 8
    m_index = text.index("Miku")  # = 8
    part1 = text[:m_index]              # "Atelier "
    part2 = text[m_index:m_index + 1]   # "M"
    part3 = text[m_index + 1:]          # "iku Acappella"

    # char별 width 측정 (cursor advance axis)
    def char_x_offset(prefix: str) -> int:
        if not prefix:
            return 0
        prefix_bbox = draw_tmp.textbbox((0, 0), prefix, font=font)
        return prefix_bbox[2] - prefix_bbox[0]

    x0 = pad - full_bbox[0]
    y0 = pad - full_bbox[1]
    x_m = x0 + char_x_offset(part1)
    x_rest = x0 + char_x_offset(part1 + part2)

    # shadow layer (full text shadow · 색 무관 black)
    shadow_layer = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    sd_draw = ImageDraw.Draw(shadow_layer)
    sd_draw.text((x0, y0 + SHADOW_OFFSET_Y), text,
                 font=font, fill=(0, 0, 0, SHADOW_ALPHA))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(SHADOW_BLUR))

    # text layer (3 part 자체엔 색 분리)
    text_layer = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    tx_draw = ImageDraw.Draw(text_layer)
    tx_draw.text((x0, y0), part1, font=font, fill=CREAM + (255,))
    tx_draw.text((x_m, y0), part2, font=font, fill=TEAL + (255,))
    tx_draw.text((x_rest, y0), part3, font=font, fill=CREAM + (255,))

    out = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    out.paste(shadow_layer, (0, 0), shadow_layer)
    out.paste(text_layer, (0, 0), text_layer)
    return out


def paste_bottom_right(frame: Image.Image, wm: Image.Image) -> Image.Image:
    result = frame.copy().convert("RGBA")
    bbox = wm.getbbox()
    if not bbox:
        return result.convert("RGB")
    text_right = bbox[2]
    text_bottom = bbox[3]
    x = FRAME_W - MARGIN_RIGHT - text_right
    y = FRAME_H - MARGIN_BOTTOM - text_bottom
    result.paste(wm, (x, y), wm)
    return result.convert("RGB")


def main():
    frame = Image.open(FRAME)
    wm = render_wordmark_m_teal(WORDMARK_TEXT, font_size=FONT_SIZE)
    out = paste_bottom_right(frame, wm)
    path = BASE / "_v40_vector_m_teal.png"
    out.save(path)
    print(f"  -> {path.name}")


if __name__ == "__main__":
    main()
