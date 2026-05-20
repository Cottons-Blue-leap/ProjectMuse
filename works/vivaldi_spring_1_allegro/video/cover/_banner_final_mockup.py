"""s319 wordmark 통합 시안 (3 axis 통합).

1. crop_left 540 (A 잘림 정정 · *A* serif fully 포함)
2. *M* teal-cyan keep (banner *Miku* 양식 정합)
3. dark shading background (좌하단 vignette mirror axis)

base = v31 (target_w 400 · invert cream + teal M).
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
TARGET_W = 400

# s319 정정: *A* serif x 595~630 자체엔 자체 자체엔 자체 자체엔 자료 → crop_left 540 (padding 60)
CROP_BOX = (540, 690, 2050, 825)

CREAM = (245, 240, 224)
TEAL = (40, 180, 175)  # banner icon_final 자체엔 자체 자체엔 vibrant teal


def crop_with_teal_invert() -> Image.Image:
    """banner 안 crop + cream background → transparent + *M* teal keep + dark → cream invert."""
    banner = Image.open(BANNER).convert("RGBA")
    cropped = banner.crop(CROP_BOX)
    arr = np.array(cropped)
    r = arr[:, :, 0].astype(int)
    g = arr[:, :, 1].astype(int)
    b = arr[:, :, 2].astype(int)
    lum = arr[:, :, :3].mean(axis=2)

    # teal-cyan mask (R < G AND R < B AND R < 180 자체엔 자체 자체엔 자체 자체엔 lum 자체엔 strong)
    teal_mask = (r < g - 5) & (r < b - 5) & (r < 200) & (lum < 220)
    # dark brown mask (lum < 150 AND not teal)
    dark_mask = (lum < 150) & ~teal_mask

    # alpha = inverse luminance
    alpha = np.clip(255 - lum * 1.2, 0, 255).astype(np.uint8)
    arr[:, :, 3] = alpha

    # dark pixel → cream
    arr[dark_mask, 0] = CREAM[0]
    arr[dark_mask, 1] = CREAM[1]
    arr[dark_mask, 2] = CREAM[2]
    # teal pixel → vibrant teal
    arr[teal_mask, 0] = TEAL[0]
    arr[teal_mask, 1] = TEAL[1]
    arr[teal_mask, 2] = TEAL[2]

    return Image.fromarray(arr, "RGBA")


def paste_with_shading(frame: Image.Image, wm: Image.Image, target_w: int,
                       shading_alpha: int, pad_x: int = 40, pad_y: int = 25) -> Image.Image:
    result = frame.copy().convert("RGBA")
    aspect = wm.size[1] / wm.size[0]
    target_h = int(target_w * aspect)
    wm_resized = wm.resize((target_w, target_h), Image.LANCZOS)

    x = FRAME_W - target_w - MARGIN_RIGHT
    y = FRAME_H - target_h - MARGIN_BOTTOM

    if shading_alpha > 0:
        shading = Image.new("RGBA",
                            (target_w + pad_x * 2, target_h + pad_y * 2),
                            (25, 20, 15, shading_alpha))
        # frame 자체엔 자체 자체엔 자체 자체엔 우 letterbox 자체엔 자체 자체엔 fit clamp
        sx = max(0, x - pad_x)
        sy = max(0, y - pad_y)
        result.paste(shading, (sx, sy), shading)

    result.paste(wm_resized, (x, y), wm_resized)
    return result.convert("RGB")


def main():
    frame = Image.open(FRAME)
    wm = crop_with_teal_invert()
    print(f"crop mask 자체엔 {wm.size}")

    variants = [
        ("v32_shading80", 80, "shading alpha 80 (subtle · 가벼운 dark fade)"),
        ("v33_shading120", 120, "shading alpha 120 (medium · 좌측 vignette mirror axis 자체엔 가장 가까움 axis · 추천)"),
        ("v34_shading160", 160, "shading alpha 160 (strong · 강 contrast axis)"),
    ]

    for name, alpha, note in variants:
        out = paste_with_shading(frame, wm, TARGET_W, shading_alpha=alpha)
        path = BASE / f"_final_{name}.png"
        out.save(path)
        print(f"  → {path.name} ({note})")


if __name__ == "__main__":
    main()
