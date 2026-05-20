"""s319 wordmark → banner crop 시안.

banner_final.png 안 *Atelier Miku Acappella* (text + interpunct + bar lines) 부분
자체 자체엔 crop 후 영상 우하단 합성.

crop area (자가 measurement axis):
  y range 693 ~ 820 (text band)
  x range 635 ~ 1990 (좌·우 bar line + 양쪽 interpunct + text)
  → width 1355 · height 130

cream background 자체엔 transparent 자체 axis 자체 자체엔 luminance threshold path.
"""

from pathlib import Path
import numpy as np
from PIL import Image

BASE = Path(__file__).parent
FRAME = BASE / "_frame_5s.png"
BANNER = BASE.parent.parent.parent.parent / "assets" / "channel_branding" / "banner_final.png"

FRAME_W = 1920
FRAME_H = 1080
MARGIN_RIGHT = 81
MARGIN_BOTTOM = 90

CROP_BOX = (635, 690, 1990, 825)  # left, top, right, bottom

assert FRAME.exists()
assert BANNER.exists()


def crop_and_transparent() -> Image.Image:
    """banner 안 *Atelier Miku Acappella* 자체 자체엔 crop + cream background 자체 자체엔 transparent."""
    banner = Image.open(BANNER).convert("RGBA")
    cropped = banner.crop(CROP_BOX)
    arr = np.array(cropped)
    lum = arr[:, :, :3].mean(axis=2)
    alpha = np.clip(255 - lum * 1.2, 0, 255).astype(np.uint8)
    arr[:, :, 3] = alpha
    return Image.fromarray(arr, "RGBA")


def paste_wordmark(frame: Image.Image, wordmark: Image.Image, target_w: int) -> Image.Image:
    result = frame.copy().convert("RGBA")
    aspect = wordmark.size[1] / wordmark.size[0]
    target_h = int(target_w * aspect)
    wm = wordmark.resize((target_w, target_h), Image.LANCZOS)

    x = FRAME_W - target_w - MARGIN_RIGHT
    y = FRAME_H - target_h - MARGIN_BOTTOM
    result.paste(wm, (x, y), wm)
    return result.convert("RGB")


def main():
    frame = Image.open(FRAME)
    wordmark = crop_and_transparent()
    print(f"crop 자체엔 {wordmark.size} (alpha 양식)")

    variants = [
        ("v22_banner_w240", 240, "width 240 (frame W 12.5%) · 작은 axis"),
        ("v23_banner_w300", 300, "width 300 (frame W 15.6%) · 중간 default · 좌하단 text stack height mirror axis"),
        ("v24_banner_w360", 360, "width 360 (frame W 18.8%) · 강 axis"),
    ]

    for name, w, note in variants:
        out = paste_wordmark(frame, wordmark, w)
        path = BASE / f"_banner_{name}.png"
        out.save(path)
        print(f"  → {path.name} ({note})")


if __name__ == "__main__":
    main()
