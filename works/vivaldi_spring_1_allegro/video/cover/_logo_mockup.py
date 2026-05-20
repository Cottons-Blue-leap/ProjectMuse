"""s319 wordmark → logo 시안 (Atelier Miku Acappella).

PIL base 가능 axis 자체 자체엔 단순 letter combination + frame 양식 자체.
본격 디자인 로고 자체 자체엔 Figma/Affinity 자체 자료.

자리 = v8 base (우하단 letterbox · margin_right 81 · margin axis mirror).
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).parent
FRAME = BASE / "_frame_5s.png"
FONT = BASE.parent.parent.parent.parent / "assets" / "fonts" / "gfs_didot" / "GFSDidot-Regular.ttf"

FRAME_W = 1920
FRAME_H = 1080
CREAM = (245, 240, 224, 255)
MARGIN_RIGHT = 81
MARGIN_BOTTOM = 90


def draw_ligature_ama(frame, font_size=72, overlap=8):
    """AMA monogram - negative letter spacing 자체 overlap 양식."""
    result = frame.copy().convert("RGBA")
    overlay = Image.new("RGBA", result.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    font = ImageFont.truetype(str(FONT), font_size)

    letters = ["A", "M", "A"]
    widths = []
    for ch in letters:
        bb = draw.textbbox((0, 0), ch, font=font)
        widths.append(bb[2] - bb[0])
    total_w = sum(widths) - overlap * (len(letters) - 1)
    bb_full = draw.textbbox((0, 0), "A", font=font)
    text_h = bb_full[3] - bb_full[1]

    x_right = FRAME_W - MARGIN_RIGHT
    y_baseline = FRAME_H - MARGIN_BOTTOM
    cursor_x = x_right - total_w
    cursor_y = y_baseline - text_h - bb_full[1]

    for i, ch in enumerate(letters):
        bb = draw.textbbox((0, 0), ch, font=font)
        draw.text((cursor_x - bb[0], cursor_y), ch, font=font, fill=CREAM)
        cursor_x += widths[i] - (overlap if i < len(letters) - 1 else 0)

    return Image.alpha_composite(result, overlay).convert("RGB")


def draw_ama_in_circle(frame, font_size=44, radius=58, stroke=2):
    """AMA · circle frame 안 박음."""
    result = frame.copy().convert("RGBA")
    overlay = Image.new("RGBA", result.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    font = ImageFont.truetype(str(FONT), font_size)

    cx = FRAME_W - MARGIN_RIGHT - radius
    cy = FRAME_H - MARGIN_BOTTOM - radius
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                 outline=CREAM, width=stroke)

    text = "AMA"
    bb = draw.textbbox((0, 0), text, font=font)
    tw = bb[2] - bb[0]
    th = bb[3] - bb[1]
    draw.text((cx - tw / 2 - bb[0], cy - th / 2 - bb[1]), text, font=font, fill=CREAM)

    return Image.alpha_composite(result, overlay).convert("RGB")


def draw_am_hierarchy(frame, am_size=72, sub_size=20):
    """AM 큰 자체 + Acappella 작은 자체 hierarchy 양식."""
    result = frame.copy().convert("RGBA")
    overlay = Image.new("RGBA", result.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    font_am = ImageFont.truetype(str(FONT), am_size)
    font_sub = ImageFont.truetype(str(FONT), sub_size)

    am_text = "AM"
    sub_text = "Atelier Miku Acappella"

    am_bb = draw.textbbox((0, 0), am_text, font=font_am)
    am_w = am_bb[2] - am_bb[0]
    am_h = am_bb[3] - am_bb[1]

    sub_bb = draw.textbbox((0, 0), sub_text, font=font_sub)
    sub_w = sub_bb[2] - sub_bb[0]
    sub_h = sub_bb[3] - sub_bb[1]

    x_right = FRAME_W - MARGIN_RIGHT
    y_bottom = FRAME_H - MARGIN_BOTTOM

    sub_x = x_right - sub_w - sub_bb[0]
    sub_y = y_bottom - sub_h - sub_bb[1]
    draw.text((sub_x, sub_y), sub_text, font=font_sub, fill=CREAM)

    am_x = x_right - am_w - am_bb[0]
    am_y = sub_y - am_h - 4 + sub_bb[1] - am_bb[1]
    draw.text((am_x, am_y), am_text, font=font_am, fill=CREAM)

    return Image.alpha_composite(result, overlay).convert("RGB")


def draw_a_center_monogram(frame, big_size=110, sub_size=22):
    """큰 A center 자체 + Atelier Miku Acappella 자체 자체엔 아래 작은 양식."""
    result = frame.copy().convert("RGBA")
    overlay = Image.new("RGBA", result.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    font_big = ImageFont.truetype(str(FONT), big_size)
    font_sub = ImageFont.truetype(str(FONT), sub_size)

    big_text = "A"
    sub_text = "Atelier Miku Acappella"

    big_bb = draw.textbbox((0, 0), big_text, font=font_big)
    big_w = big_bb[2] - big_bb[0]
    big_h = big_bb[3] - big_bb[1]

    sub_bb = draw.textbbox((0, 0), sub_text, font=font_sub)
    sub_w = sub_bb[2] - sub_bb[0]
    sub_h = sub_bb[3] - sub_bb[1]

    x_right = FRAME_W - MARGIN_RIGHT
    y_bottom = FRAME_H - MARGIN_BOTTOM

    sub_x = x_right - sub_w - sub_bb[0]
    sub_y = y_bottom - sub_h - sub_bb[1]
    draw.text((sub_x, sub_y), sub_text, font=font_sub, fill=CREAM)

    big_x = x_right - (sub_w + big_w) / 2 - big_bb[0]
    big_y = sub_y - big_h - 6 + sub_bb[1] - big_bb[1]
    draw.text((big_x, big_y), big_text, font=font_big, fill=CREAM)

    return Image.alpha_composite(result, overlay).convert("RGB")


def main():
    frame = Image.open(FRAME)

    variants = [
        ("v15_ama_ligature", draw_ligature_ama, "AMA ligature · negative spacing overlap 양식"),
        ("v16_ama_circle", draw_ama_in_circle, "AMA in circle frame · 클래식 medallion 양식"),
        ("v17_am_hierarchy", draw_am_hierarchy, "AM large + Atelier Miku Acappella small · hierarchy 양식"),
        ("v18_a_center", draw_a_center_monogram, "큰 A center + Atelier Miku Acappella 아래 · minimalist monogram"),
    ]

    for name, fn, note in variants:
        out = fn(frame)
        path = BASE / f"_logo_{name}.png"
        out.save(path)
        print(f"  → {path.name} ({note})")


if __name__ == "__main__":
    main()
