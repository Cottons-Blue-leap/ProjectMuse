"""s320 v39 시안 — v35 양식 mirror + GFS Didot 직접 vector render.

v35 자료 base axis (s319 코튼 결단 자리):
  자리 = 우하단 (MARGIN_RIGHT=81, MARGIN_BOTTOM=90)
  text-shadow = blur 12 · offset 0,2 · alpha 192 (좌측 *Antonio Vivaldi · Spring, Mvt. I · (after 1725)* mirror axis)
  color = cream #e8e0c8 (좌측 text 색 정합)
  typeface = GFS Didot Regular (banner crop 폐기)
  size = v35 banner width 400 자료 base · GFS Didot size 36 → width 377 정합

자가 발화 axis (코튼 자리):
  본 path 자체엔 시그너처 §3 v2 *우상단 corner* axis 자체와 충돌.
  *우상단* axis 자체엔 s319 박힘 (1주일 안). v35 자료 base 자체엔 *우하단 자리 + 좌측 mirror* axis 자체엔 시그너처 §3 v3 update path 자체 자가 발화 의제.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = Path(__file__).parent
FRAME = BASE / "_frame_5s.png"
FONT = BASE.parent.parent.parent.parent / "assets" / "fonts" / "gfs_didot" / "GFSDidot-Regular.ttf"

FRAME_W = 1920
FRAME_H = 1080
MARGIN_RIGHT = 81       # v35 자료 base (좌측 *Antonio Vivaldi* margin_left axis mirror)
MARGIN_BOTTOM = 90      # v35 자료 base

WORDMARK_TEXT = "Atelier Miku Acappella"
CREAM = (232, 224, 200)             # #e8e0c8 좌측 text 색 정합 (시그너처 §1 typo color)

# text-shadow 양식 (좌측 visualizer source mirror)
SHADOW_BLUR = 12
SHADOW_OFFSET_Y = 2
SHADOW_ALPHA = 192      # rgba(0,0,0,0.75) 정합


def render_wordmark(text: str, font_size: int) -> Image.Image:
    """GFS Didot vector render + text-shadow Gaussian (좌측 양식 정확 mirror)."""
    font = ImageFont.truetype(str(FONT), font_size)

    tmp = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
    bbox = ImageDraw.Draw(tmp).textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    pad = SHADOW_BLUR * 3 + max(SHADOW_OFFSET_Y, 1) + 4
    canvas_w = text_w + pad * 2
    canvas_h = text_h + pad * 2

    # shadow layer (offset_y · blur · alpha)
    shadow_layer = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    sd_draw = ImageDraw.Draw(shadow_layer)
    sd_draw.text((pad - bbox[0], pad - bbox[1] + SHADOW_OFFSET_Y), text,
                 font=font, fill=(0, 0, 0, SHADOW_ALPHA))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(SHADOW_BLUR))

    # text layer
    text_layer = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    tx_draw = ImageDraw.Draw(text_layer)
    tx_draw.text((pad - bbox[0], pad - bbox[1]), text,
                 font=font, fill=CREAM + (255,))

    out = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    out.paste(shadow_layer, (0, 0), shadow_layer)
    out.paste(text_layer, (0, 0), text_layer)
    return out


def paste_bottom_right(frame: Image.Image, wm: Image.Image) -> Image.Image:
    """우하단 corner paste · v35 자리 정확 mirror."""
    result = frame.copy().convert("RGBA")

    bbox = wm.getbbox()
    if not bbox:
        return result.convert("RGB")

    # right edge alignment + bottom edge alignment (text 자체 안 padding axis)
    text_right = bbox[2]
    text_bottom = bbox[3]
    x = FRAME_W - MARGIN_RIGHT - text_right
    y = FRAME_H - MARGIN_BOTTOM - text_bottom

    result.paste(wm, (x, y), wm)
    return result.convert("RGB")


def main():
    frame = Image.open(FRAME)

    # 3 size variation
    variants = [
        ("v39_vector_size32", 32, "small · width 334px"),
        ("v39_vector_size36", 36, "default · width 377px · v35 banner 400 정합 axis"),
        ("v39_vector_size40", 40, "large · width 417px"),
    ]

    for name, size, note in variants:
        wm = render_wordmark(WORDMARK_TEXT, font_size=size)
        out = paste_bottom_right(frame, wm)
        path = BASE / f"_{name}.png"
        out.save(path)
        print(f"  -> {path.name} ({note})")


if __name__ == "__main__":
    main()
