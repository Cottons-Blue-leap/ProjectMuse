#!/usr/bin/env python3
"""muse background — work의 letterboxColors로 IGN 디더링된 배경 PNG 생성.

배경(2026-06-22): CSS linear-gradient는 브라우저가 디더 없이 8bit로 양자화해서,
비슷한 3색을 넓게 펼치면 평평한 구간에 밴딩(층)이 생긴다. 근본 원인은 8bit 색심도
(채널당 256단계)지 Remotion이 아니다. 이 스크립트는 그라디언트를 고정밀(float)으로
계산하고 Interleaved Gradient Noise(IGN · blue-noise급 정렬 디더)로 8bit화해서,
1픽셀 단위로 미세하게 변동하는 '띠 없는' 배경을 굽는다.

결과:
  works/<id>/video/visualizer/public/background.png   — 디더링된 배경
  props.json 에 "backgroundPath": "background.png" 기록

Remotion(VisualizerComposition)은 backgroundPath가 있으면 이 PNG를 배경으로 쓰고,
없으면 기존 CSS 그라디언트로 폴백한다(forward 호환 · 구 work 무영향).

사용:
  python muse.py background <work_id>
  python muse.py background <work_id> --lsb 2.0   # 디더 진폭 (기본 1.5)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

# Windows cp949 한글 깨짐 방어
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[3]
WIDTH, HEIGHT = 2560, 1440
# 디더 진폭(LSB · 코튼 2026-06-22 "10비트급으로 가자").
# 8bit 손실압축(H.264)은 1~2 LSB 미세 디더를 DCT 양자화로 뭉개 띠를 되살린다. 측정상
# LSB를 5까지 올리면 8bit crf10 인코딩 후 띠 잔차가 10비트(crf10)와 동급(~0.25)이 된다.
# 10비트는 일반 재생 불가 + 8bit 디스플레이 변환서 다시 띠 → 8bit + 강한 디더가 실해.
DITHER_LSB = 5.0
# 비네팅(가장자리 미세 감광). 평평한 면을 깨서 압축이 '평평한 블록 = 비트 적게'로
# 처리하는 걸 막고(프로 해법), 동시에 중앙 커버로 시선을 모은다. 매우 미묘하게.
VIGNETTE_STRENGTH = 0.06


def vis_work(work_id: str) -> Path:
    return ROOT / "works" / work_id / "video" / "visualizer"


def hexrgb(h: str) -> np.ndarray:
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float64)


def gradient_float(colors, w: int, h: int) -> np.ndarray:
    """180deg 세로 그라디언트 (0%/50%/100% stop) — Remotion CSS와 동일한 보간."""
    c0, c1, c2 = (hexrgb(c) for c in colors)
    t = np.linspace(0.0, 1.0, h)
    col = np.empty((h, 3), np.float64)
    lo = t <= 0.5
    col[lo] = c0 * (1 - (t[lo] / 0.5)[:, None]) + c1 * ((t[lo] / 0.5)[:, None])
    a = ((t[~lo] - 0.5) / 0.5)[:, None]
    col[~lo] = c1 * (1 - a) + c2 * a
    return np.repeat(col[:, None, :], w, axis=1)


def ign_threshold(w: int, h: int) -> np.ndarray:
    """Interleaved Gradient Noise (Jimenez) — blue-noise급 정렬 디더 임계 맵, ±0.5."""
    xv, yv = np.meshgrid(np.arange(w), np.arange(h))
    frac = lambda x: x - np.floor(x)
    ign = frac(52.9829189 * frac(0.06711056 * xv + 0.00583715 * yv))
    return (ign - 0.5)[:, :, None]


def vignette(w: int, h: int, strength: float) -> np.ndarray:
    """가장자리로 갈수록 (1 - strength·r²)배 감광. 중심 1.0, 모서리 1-strength."""
    yy = np.linspace(-1.0, 1.0, h)[:, None]
    xx = np.linspace(-1.0, 1.0, w)[None, :]
    r2 = (xx ** 2 + yy ** 2) / 2.0
    return (1.0 - strength * r2)[:, :, None]


def make_background(colors, w: int = WIDTH, h: int = HEIGHT,
                    lsb: float = DITHER_LSB,
                    vig: float = VIGNETTE_STRENGTH) -> np.ndarray:
    g = gradient_float(colors, w, h)
    g = g * vignette(w, h, vig)             # ② 평평함 깨기 (양자화 전, 디더로 부드럽게)
    g = g + ign_threshold(w, h) * lsb        # ① 강한 IGN 디더
    return np.clip(np.round(g), 0, 255).astype(np.uint8)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="muse background",
                                 description="IGN 디더링된 배경 PNG 생성")
    ap.add_argument("work_id")
    ap.add_argument("--lsb", type=float, default=DITHER_LSB,
                    help=f"디더 진폭 LSB (기본 {DITHER_LSB})")
    ap.add_argument("--vignette", type=float, default=VIGNETTE_STRENGTH,
                    help=f"비네팅 강도 (기본 {VIGNETTE_STRENGTH} · 0=끔)")
    args = ap.parse_args(argv)

    base = vis_work(args.work_id)
    props = base / "props.json"
    if not props.exists():
        print(f"props 없음: {props}", file=sys.stderr)
        return 2
    data = json.loads(props.read_text(encoding="utf-8"))
    colors = data.get("letterboxColors")
    if not colors or len(colors) != 3:
        print("letterboxColors(3색)가 props.json에 필요", file=sys.stderr)
        return 2

    img = make_background(colors, lsb=args.lsb, vig=args.vignette)
    out = base / "public" / "background.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(img).save(out)

    data["backgroundPath"] = "background.png"
    props.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                     encoding="utf-8")
    print(f"✓ 배경 생성: {out}")
    print(f"  colors={colors}  IGN 디더 {args.lsb} LSB  비네팅 {args.vignette}  ({WIDTH}x{HEIGHT})")
    print(f"  props.json ← backgroundPath=background.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
