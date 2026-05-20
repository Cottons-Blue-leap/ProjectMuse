"""s319 banner wordmark v24 base 시인성 강화 axis 시안.

v24 결단 자료 자체엔 width 360 · 우하단 letterbox 자체엔 dark brown text 자체엔 visible 약.
시인성 강화 path:
  v25 = invert cream (alpha keep + RGB cream fill)
  v26 = invert white (alpha keep + RGB white fill)
  v27 = invert cream + drop shadow
  v28 = invert cream + outline stroke
"""

from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter

BASE = Path(__file__).parent
FRAME = BASE / "_frame_5s.png"
BANNER = BASE.parent.parent.parent.parent / "assets" / "channel_branding" / "banner_final.png"

FRAME_W = 1920
FRAME_H = 1080
MARGIN_RIGHT = 81
MARGIN_BOTTOM = 90
TARGET_W = 360
# s319 정정: *A* leftmost x=640 · *a* rightmost x=1990 · mirror padding 40
CROP_BOX = (600, 690, 2030, 825)

CREAM = (245, 240, 224)
WHITE = (255, 255, 255)


def crop_alpha_mask() -> Image.Image:
    """banner 안 crop + cream background 자체 자체엔 alpha mask 양식."""
    banner = Image.open(BANNER).convert("RGBA")
    cropped = banner.crop(CROP_BOX)
    arr = np.array(cropped)
    lum = arr[:, :, :3].mean(axis=2)
    alpha = np.clip(255 - lum * 1.2, 0, 255).astype(np.uint8)
    arr[:, :, 3] = alpha
    return Image.fromarray(arr, "RGBA")


def fill_color(mask: Image.Image, color: tuple[int, int, int]) -> Image.Image:
    """alpha mask 자체엔 keep + RGB 자체 자체엔 자체 color 자체엔 fill."""
    arr = np.array(mask)
    arr[:, :, 0] = color[0]
    arr[:, :, 1] = color[1]
    arr[:, :, 2] = color[2]
    return Image.fromarray(arr, "RGBA")


def add_drop_shadow(wm: Image.Image, *, offset: int = 3, blur: int = 4,
                    shadow_color: tuple[int, int, int, int] = (0, 0, 0, 180)) -> Image.Image:
    """text 자체 자체엔 drop shadow 자체 자체엔 추가."""
    w, h = wm.size
    pad = blur * 2 + offset
    canvas = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))

    # shadow layer
    shadow_arr = np.array(wm)
    alpha = shadow_arr[:, :, 3]
    shadow = np.zeros_like(shadow_arr)
    shadow[:, :, 0] = shadow_color[0]
    shadow[:, :, 1] = shadow_color[1]
    shadow[:, :, 2] = shadow_color[2]
    shadow[:, :, 3] = (alpha.astype(np.float32) * shadow_color[3] / 255).astype(np.uint8)
    shadow_img = Image.fromarray(shadow, "RGBA").filter(ImageFilter.GaussianBlur(blur))

    canvas.paste(shadow_img, (pad + offset, pad + offset), shadow_img)
    canvas.paste(wm, (pad, pad), wm)
    return canvas


def add_outline(wm: Image.Image, *, stroke: int = 2,
                outline_color: tuple[int, int, int, int] = (40, 30, 20, 200)) -> Image.Image:
    """text 자체 자체엔 outline stroke 자체 자체엔 추가."""
    w, h = wm.size
    pad = stroke * 2
    canvas = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))

    # outline = shifted alpha (8 directions) 자체 자체엔 합집합
    arr = np.array(wm)
    alpha = arr[:, :, 3]
    outline_arr = np.zeros((h + pad * 2, w + pad * 2, 4), dtype=np.uint8)
    outline_arr[:, :, 0] = outline_color[0]
    outline_arr[:, :, 1] = outline_color[1]
    outline_arr[:, :, 2] = outline_color[2]

    combined_alpha = np.zeros((h + pad * 2, w + pad * 2), dtype=np.uint8)
    for dx in range(-stroke, stroke + 1):
        for dy in range(-stroke, stroke + 1):
            if dx == 0 and dy == 0:
                continue
            y_slice = slice(pad + dy, pad + dy + h)
            x_slice = slice(pad + dx, pad + dx + w)
            combined_alpha[y_slice, x_slice] = np.maximum(combined_alpha[y_slice, x_slice], alpha)

    outline_arr[:, :, 3] = (combined_alpha.astype(np.float32) * outline_color[3] / 255).astype(np.uint8)
    outline_img = Image.fromarray(outline_arr, "RGBA")

    canvas.paste(outline_img, (0, 0), outline_img)
    canvas.paste(wm, (pad, pad), wm)
    return canvas


def paste_to_frame(frame: Image.Image, wm: Image.Image, target_w: int) -> Image.Image:
    result = frame.copy().convert("RGBA")
    aspect = wm.size[1] / wm.size[0]
    target_h = int(target_w * aspect)
    wm_resized = wm.resize((target_w, target_h), Image.LANCZOS)

    x = FRAME_W - target_w - MARGIN_RIGHT
    y = FRAME_H - target_h - MARGIN_BOTTOM
    result.paste(wm_resized, (x, y), wm_resized)
    return result.convert("RGB")


def main():
    frame = Image.open(FRAME)
    mask = crop_alpha_mask()

    wm_cream = fill_color(mask, CREAM)
    wm_white = fill_color(mask, WHITE)
    wm_cream_shadow = add_drop_shadow(wm_cream, offset=3, blur=5)
    wm_cream_outline = add_outline(wm_cream, stroke=2, outline_color=(40, 30, 20, 220))

    # drop shadow / outline 자체엔 size 자체엔 padding 포함 자체 자체엔 자료 자체 → target_w 자체 자체엔 padding 보정
    variants = [
        ("v29_cream_fix_w360", wm_cream, 360, "v25 base + crop_left 정정 · target_w 360 (visual text size 약 small axis)"),
        ("v30_cream_fix_w380", wm_cream, 380, "v25 base + crop_left 정정 · target_w 380 (visual text size v24와 동일 axis · 추천)"),
        ("v31_cream_fix_w400", wm_cream, 400, "v25 base + crop_left 정정 · target_w 400 (강 axis)"),
    ]

    for name, wm, w, note in variants:
        out = paste_to_frame(frame, wm, w)
        path = BASE / f"_visibility_{name}.png"
        out.save(path)
        print(f"  → {path.name} ({note})")


if __name__ == "__main__":
    main()
