"""s319 wordmark → watermark 시안 (channel brand AMA monogram).

브랜드 자료 자체:
  assets/channel_branding/watermark_300x300_transparent.png (teal-cyan + dark brown)

자리 = v8 base (우하단 letterbox · margin_right 81 · margin_bottom 90 · mirror axis).
size axis 가변 (frame H 비율 9.3%/11.1%/13.9%).
"""

from pathlib import Path
from PIL import Image

BASE = Path(__file__).parent
FRAME = BASE / "_frame_5s.png"
WATERMARK = BASE.parent.parent.parent.parent / "assets" / "channel_branding" / "watermark_300x300_transparent.png"

FRAME_W = 1920
FRAME_H = 1080
MARGIN_RIGHT = 81
MARGIN_BOTTOM = 90

assert FRAME.exists(), f"frame X: {FRAME}"
assert WATERMARK.exists(), f"watermark X: {WATERMARK}"


def paste_watermark(frame: Image.Image, *, size: int) -> Image.Image:
    result = frame.copy().convert("RGBA")
    wm = Image.open(WATERMARK).convert("RGBA").resize((size, size), Image.LANCZOS)
    x = FRAME_W - size - MARGIN_RIGHT
    y = FRAME_H - size - MARGIN_BOTTOM
    result.paste(wm, (x, y), wm)
    return result.convert("RGB")


def main():
    frame = Image.open(FRAME)
    variants = [
        ("v19_wm_size100", 100, "size 100 (frame H 9.3%) · 작은 axis · subtle"),
        ("v20_wm_size120", 120, "size 120 (frame H 11.1%) · 중간 default · 좌하단 text stack height mirror axis"),
        ("v21_wm_size150", 150, "size 150 (frame H 13.9%) · 강 axis"),
    ]

    for name, size, note in variants:
        out = paste_watermark(frame, size=size)
        path = BASE / f"_watermark_{name}.png"
        out.save(path)
        print(f"  → {path.name} ({note})")


if __name__ == "__main__":
    main()
