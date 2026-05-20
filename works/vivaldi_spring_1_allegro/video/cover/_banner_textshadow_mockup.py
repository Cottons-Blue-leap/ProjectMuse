"""s319 wordmark 통합 시안 v3 (좌측 text-shadow 정합 axis).

좌측 visualizer source 자가 inspection:
  color: #e8e0c8 (cream)
  textShadow: '0 2px 12px rgba(0, 0, 0, 0.75)'
  → letter per letter Gaussian drop shadow 양식 (별 explicit dark rectangle X)

정합 path:
  v33 dark rectangle overlay 제거
  대신 wordmark 자체엔 동일 text-shadow 적용 (offset 0,2 · blur 12 · alpha 0.75)
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
TARGET_W = 400

CROP_BOX = (540, 690, 2050, 825)
CREAM = (232, 224, 200)  # 좌측 text color #e8e0c8 정합
TEAL = (40, 180, 175)


def crop_with_teal_invert() -> Image.Image:
    banner = Image.open(BANNER).convert("RGBA")
    cropped = banner.crop(CROP_BOX)
    arr = np.array(cropped)
    r = arr[:, :, 0].astype(int)
    g = arr[:, :, 1].astype(int)
    b = arr[:, :, 2].astype(int)
    lum = arr[:, :, :3].mean(axis=2)

    teal_mask = (r < g - 5) & (r < b - 5) & (r < 200) & (lum < 220)
    dark_mask = (lum < 150) & ~teal_mask

    alpha = np.clip(255 - lum * 1.2, 0, 255).astype(np.uint8)
    arr[:, :, 3] = alpha

    arr[dark_mask, 0] = CREAM[0]
    arr[dark_mask, 1] = CREAM[1]
    arr[dark_mask, 2] = CREAM[2]
    arr[teal_mask, 0] = TEAL[0]
    arr[teal_mask, 1] = TEAL[1]
    arr[teal_mask, 2] = TEAL[2]

    return Image.fromarray(arr, "RGBA")


def add_text_shadow(wm: Image.Image, *, offset_y: int = 2, blur: int = 12,
                    shadow_alpha: int = 192) -> Image.Image:
    """좌측 text-shadow 양식 mirror: offset(0,2) · blur 12 · rgba(0,0,0,0.75)."""
    w, h = wm.size
    pad = blur * 2 + max(offset_y, 1)
    canvas = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))

    arr = np.array(wm)
    alpha = arr[:, :, 3]
    shadow = np.zeros_like(arr)
    shadow[:, :, 3] = (alpha.astype(np.float32) * shadow_alpha / 255).astype(np.uint8)
    shadow_img = Image.fromarray(shadow, "RGBA").filter(ImageFilter.GaussianBlur(blur))

    canvas.paste(shadow_img, (pad, pad + offset_y), shadow_img)
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
    wm = crop_with_teal_invert()
    wm_with_shadow = add_text_shadow(wm, offset_y=2, blur=12, shadow_alpha=192)

    aspect_orig = wm.size[1] / wm.size[0]
    aspect_shadow = wm_with_shadow.size[1] / wm_with_shadow.size[0]
    # shadow 자체엔 padding 자체엔 target_w 자체엔 자체 자체엔 약 더 강 axis 자체엔 자료
    target_w_shadow = int(TARGET_W * (wm_with_shadow.size[0] / wm.size[0]))

    variants = [
        ("v35_textshadow_default", wm_with_shadow, target_w_shadow,
         "text-shadow blur 12 · 좌측 양식 정확 mirror axis · MOKA 추천"),
    ]

    # 자체 자체엔 자체 자체엔 light blur 자체엔 자체 자체엔 자료 axis 자체엔 자체 자체엔 자료 비교
    wm_blur8 = add_text_shadow(wm, offset_y=2, blur=8, shadow_alpha=192)
    target_w_blur8 = int(TARGET_W * (wm_blur8.size[0] / wm.size[0]))
    variants.append(("v36_textshadow_blur8", wm_blur8, target_w_blur8,
                     "text-shadow blur 8 · subtle axis"))

    wm_blur16 = add_text_shadow(wm, offset_y=3, blur=16, shadow_alpha=210)
    target_w_blur16 = int(TARGET_W * (wm_blur16.size[0] / wm.size[0]))
    variants.append(("v37_textshadow_blur16", wm_blur16, target_w_blur16,
                     "text-shadow blur 16 · strong axis"))

    for name, wm_var, w, note in variants:
        out = paste_to_frame(frame, wm_var, w)
        path = BASE / f"_textshadow_{name}.png"
        out.save(path)
        print(f"  → {path.name} ({note})")


if __name__ == "__main__":
    main()
