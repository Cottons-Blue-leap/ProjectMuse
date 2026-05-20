"""s319 wordmark 시안 v2 (영상 16:9 frame · 우 letterbox 우상단 corner).

코튼 결단: 1:1 cover에는 박지 X. 영상 화면 기준 우상단 자리 (우 letterbox 영역 안 박힘).

frame = 1920x1080:
- 좌 letterbox  = x 0~420   (420 px)
- 1:1 cover    = x 420~1500 (1080 px · center)
- 우 letterbox  = x 1500~1920 (420 px)

우상단 자리 = 우 letterbox 상단 영역 (x 1500~1920 · y 0~~200).
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).parent
FRAME = BASE / "_frame_5s.png"
FONT = BASE.parent.parent.parent.parent / "assets" / "fonts" / "gfs_didot" / "GFSDidot-Regular.ttf"

WORDMARK = "Atelier Miku Acappella"

assert FRAME.exists(), f"frame X: {FRAME}"
assert FONT.exists(), f"font X: {FONT}"

LETTERBOX_LEFT = 1500
FRAME_W = 1920
FRAME_H = 1080
LETTERBOX_W = FRAME_W - LETTERBOX_LEFT  # 420


def measure_luminance(img: Image.Image, box: tuple[int, int, int, int]) -> float:
    region = img.crop(box).convert("L")
    pixels = list(region.getdata())
    return sum(pixels) / (len(pixels) * 255)


def draw_horizontal_bottom_text(frame: Image.Image, *, text: str = WORDMARK, font_size: int,
                                color: tuple[int, int, int, int],
                                margin_bottom: int, margin_right: int) -> Image.Image:
    result = frame.copy().convert("RGBA")
    overlay = Image.new("RGBA", result.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    font = ImageFont.truetype(str(FONT), font_size)

    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    x = FRAME_W - text_w - margin_right - bbox[0]
    y = FRAME_H - margin_bottom - text_h - bbox[1]
    draw.text((x, y), text, font=font, fill=color)
    return Image.alpha_composite(result, overlay).convert("RGB")


# backward compat alias
draw_horizontal_bottom = draw_horizontal_bottom_text


def main() -> None:
    frame = Image.open(FRAME)
    bottom_right_box = (LETTERBOX_LEFT, FRAME_H - 120, FRAME_W - 20, FRAME_H - 20)
    avg_lum = measure_luminance(frame, bottom_right_box)
    print(f"우 letterbox 하단 luminance ({bottom_right_box}): {avg_lum:.3f}")
    print(f"  → {'어두운' if avg_lum < 0.4 else 'mid' if avg_lum < 0.6 else '밝은'} 자리")

    cream = (245, 240, 224, 255)

    # AMA 로고 axis 시안 (v11~v14)
    ama_variants = [
        {
            "name": "v11_ama_size56",
            "text": "AMA",
            "kwargs": dict(font_size=56, color=cream, margin_bottom=85, margin_right=81),
            "note": "AMA · size 56 · margin axis v8 mirror · 중간 axis",
        },
        {
            "name": "v12_ama_size80",
            "text": "AMA",
            "kwargs": dict(font_size=80, color=cream, margin_bottom=72, margin_right=81),
            "note": "AMA · size 80 · 강 axis (visual weight 자체 자체 자체엔 wordmark 자체와 align axis)",
        },
        {
            "name": "v13_ama_spaced_size56",
            "text": "A M A",
            "kwargs": dict(font_size=56, color=cream, margin_bottom=85, margin_right=81),
            "note": "A M A · size 56 · letter-spaced 양식 · 자체엔 letterbox 자체 자체엔 horizontal 자체 자체 자체 axis",
        },
        {
            "name": "v14_ama_interpunct_size56",
            "text": "A·M·A",
            "kwargs": dict(font_size=56, color=cream, margin_bottom=85, margin_right=81),
            "note": "A·M·A · size 56 · interpunct 양식 · 클래식 typographic 자체 axis",
        },
    ]

    for v in ama_variants:
        out = draw_horizontal_bottom_text(frame, text=v["text"], **v["kwargs"])
        out_path = BASE / f"_wordmark_frame_{v['name']}.png"
        out.save(out_path)
        print(f"  → {out_path.name} ({v['note']})")


if __name__ == "__main__":
    main()
