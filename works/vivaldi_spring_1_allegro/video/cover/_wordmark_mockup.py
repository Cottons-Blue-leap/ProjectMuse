"""s319 시그너처 §3 wordmark 시안 박음 (Atelier Miku Acappella).

비발디 사계 봄 1악장 cover (album_1x1.png · 1254x1254)에 wordmark 합성 시안 3건.

axis:
- font = GFS Didot
- 자리 = 우상단 corner (top-right)
- 적용 = 1:1 cover still (시그너처 §3 정합)
- 시안 = size · color · opacity 가변 3건

본 script는 *시안 자리*. 실제 publish 통과 자료 retrofit 자체 아님 (다음 작품부터 적용 path).
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).parent
COVER = BASE / "album_1x1.png"
FONT = BASE.parent.parent.parent.parent / "assets" / "fonts" / "gfs_didot" / "GFSDidot-Regular.ttf"

WORDMARK = "Atelier Miku Acappella"

assert COVER.exists(), f"cover 자체 X: {COVER}"
assert FONT.exists(), f"font 자체 X: {FONT}"


def measure_luminance(img: Image.Image, box: tuple[int, int, int, int]) -> float:
    """box 자리 (left, top, right, bottom) 안 평균 luminance (0~1) 측정."""
    region = img.crop(box).convert("L")
    pixels = list(region.getdata())
    return sum(pixels) / (len(pixels) * 255)


def draw_wordmark(
    cover: Image.Image,
    *,
    text: str,
    font_size: int,
    color: tuple[int, int, int, int],
    padding_pct: float,
) -> Image.Image:
    """cover 자료에 wordmark text overlay 합성."""
    result = cover.copy().convert("RGBA")
    overlay = Image.new("RGBA", result.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    font = ImageFont.truetype(str(FONT), font_size)

    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    padding = int(result.size[0] * padding_pct / 100)
    x = result.size[0] - text_w - padding - bbox[0]
    y = padding - bbox[1]

    draw.text((x, y), text, font=font, fill=color)
    return Image.alpha_composite(result, overlay).convert("RGB")


def main() -> None:
    cover = Image.open(COVER)
    w, h = cover.size

    padding_px = int(w * 0.05)
    top_right_box = (w - padding_px - 400, padding_px, w - padding_px, padding_px + 100)
    avg_lum = measure_luminance(cover, top_right_box)
    print(f"우상단 자리 luminance ({top_right_box}): {avg_lum:.3f}")
    print(f"  → 어두운 자리 (< 0.5)" if avg_lum < 0.5 else f"  → 밝은 자리 (>= 0.5)")

    variants = [
        {
            "name": "v1_cream_small",
            "font_size": int(h * 0.028),
            "color": (245, 240, 224, 255),
            "padding_pct": 4.5,
            "note": "cream #f5f0e0 · size 35 (2.8%) · 작은 axis · 클래식 메이저 label 양식",
        },
        {
            "name": "v2_cream_medium",
            "font_size": int(h * 0.034),
            "color": (245, 240, 224, 255),
            "padding_pct": 4.0,
            "note": "cream #f5f0e0 · size 43 (3.4%) · 중간 default · 추천 axis",
        },
        {
            "name": "v3_cream_large",
            "font_size": int(h * 0.042),
            "color": (245, 240, 224, 230),
            "padding_pct": 3.5,
            "note": "cream #f5f0e0 · size 53 (4.2%) · opacity 0.9 · 강한 brand axis",
        },
    ]

    for v in variants:
        out = draw_wordmark(
            cover,
            text=WORDMARK,
            font_size=v["font_size"],
            color=v["color"],
            padding_pct=v["padding_pct"],
        )
        out_path = BASE / f"_wordmark_mockup_{v['name']}.png"
        out.save(out_path)
        print(f"  → {out_path.name} ({v['note']})")


if __name__ == "__main__":
    main()
