#!/usr/bin/env python3
"""muse render — 통합 공유 visualizer로 work를 렌더 (s412 양식 B).

단일 공유 Remotion 프로젝트(workflows/video_release/visualizer)에 work별
props.json + public(audio/cover/fonts)을 주입해 렌더한다. work마다 node_modules가
필요 없다 — 엔진/의존성은 공유 프로젝트 한 곳에만 산다.

사용:
  python muse.py render <work_id>               # exports/<id>_final.mp4 렌더
  python muse.py render <work_id> --gate         # visualizer/out/gate_check.mp4 (검증용·exports 미덮어씀)
  python muse.py render <work_id> --still 3500   # 특정 프레임 still png (빠른 시각 점검)
  python muse.py render <work_id> --out <path>   # 출력 경로 지정
  python muse.py render <work_id> --concurrency 4  # 렌더 동시성 (기본 = config의 1)

전제: 공유 프로젝트에 `npm install` 1회 완료.
입력 규약 (work별):
  works/<id>/video/visualizer/props.json   — VisualizerProps + durationSeconds
  works/<id>/video/visualizer/public/      — audio.wav · cover.png · fonts/
설계: workflows/video_release/docs/shared_visualizer_design.md
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

# Windows cp949 한글 깨짐 방어
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[3]
VIS = ROOT / "workflows/video_release/visualizer"
COMPOSITION = "MuseVisualizer"


def vis_work(work_id: str) -> Path:
    return ROOT / "works" / work_id / "video" / "visualizer"


def npx() -> str:
    return "npx.cmd" if os.name == "nt" else "npx"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="muse render", description="통합 공유 visualizer 렌더")
    ap.add_argument("work_id")
    ap.add_argument("--gate", action="store_true",
                    help="검증용 출력 (visualizer/out/gate_check.mp4 · exports 미덮어씀)")
    ap.add_argument("--still", type=int, metavar="FRAME", help="특정 프레임 still png")
    ap.add_argument("--out", help="출력 경로 (기본 = exports/<id>_final.mp4)")
    ap.add_argument("--concurrency", type=int, help="렌더 동시성 (기본 = config)")
    args = ap.parse_args(argv)

    work = ROOT / "works" / args.work_id
    if not work.exists():
        print(f"work 없음: {work}", file=sys.stderr)
        return 2

    props = vis_work(args.work_id) / "props.json"
    public = vis_work(args.work_id) / "public"
    for p in (props, public):
        if not p.exists():
            print(f"입력 없음: {p}", file=sys.stderr)
            return 2
    if not (VIS / "node_modules").exists():
        print(f"공유 프로젝트 미설치 — 먼저 `npm install` (in {VIS})", file=sys.stderr)
        return 2

    gate_out = vis_work(args.work_id) / "out"
    common = [f"--props={props}", f"--public-dir={public}"]
    if args.concurrency:
        common.append(f"--concurrency={args.concurrency}")

    if args.still is not None:
        out = Path(args.out) if args.out else gate_out / f"still_{args.still}.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        cmd = [npx(), "remotion", "still", "src/index.ts", COMPOSITION, str(out),
               f"--frame={args.still}", *common]
    else:
        if args.out:
            out = Path(args.out)
        elif args.gate:
            out = gate_out / "gate_check.mp4"
        else:
            out = work / "video" / "exports" / f"{args.work_id}_final.mp4"
        out.parent.mkdir(parents=True, exist_ok=True)
        cmd = [npx(), "remotion", "render", "src/index.ts", COMPOSITION, str(out), *common]

    print(f"[muse render] {args.work_id} → {out}")
    print(f"  props={props.name}  public={public}")
    print(f"  cwd={VIS}")
    print(f"  $ {' '.join(cmd)}")
    r = subprocess.run(cmd, cwd=str(VIS))
    if r.returncode == 0:
        print(f"✓ 렌더 완료: {out}")
    else:
        print(f"✗ 렌더 실패 (exit {r.returncode})", file=sys.stderr)
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
