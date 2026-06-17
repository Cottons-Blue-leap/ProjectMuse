#!/usr/bin/env python3
"""muse — Project Muse 단일 CLI 디스패처.

흩어진 워크플로우 스크립트로 위임하는 얇은 진입점. 각 스크립트는 그대로 직접 실행해도 됨.

사용:
  python muse.py project init --project ./works/<piece_id>
  python muse.py project doctor [--fix]
  python muse.py project status
  python muse.py doctor            # = project doctor (단축)
  python muse.py status            # = project status (단축)
  python muse.py audio check-stems ...
  python muse.py audio assemble-proof ...
  python muse.py audio blend-gate --master <wav> [--stems <dir> --lead <name>]  # 렌더 전 블렌딩 게이트 (WS1)
  python muse.py thumbnail --song <name> | --all
  python muse.py render <work_id>  # 통합 공유 visualizer 렌더 (양식 B)
  python muse.py captions cues <work_id>   # .vpr → lyrics/cues.json (가사 곡 자막 타이밍)
  python muse.py captions vtt  <work_id>   # cues + lyrics → captions.<lang>.vtt ×N
  python muse.py short init <work_id> <slug> [--start --dur --n --bpm]  # 쇼츠 스핀업 (v3 MikuPile)
  python muse.py tidy [--archive]
  python muse.py list              # 등록 워크플로우 목록 (registry.json)
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

# Windows cp949 한글 깨짐 방어 (s355 광역 audit 정합)
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent

SCRIPTS = {
    "project":   ROOT / "workflows/project_setup/scripts/muse_project.py",
    "audio":     ROOT / "workflows/audio_production/scripts/muse_audio.py",
    "thumbnail": ROOT / "workflows/video_release/scripts/muse_thumbnail.py",
    "render":    ROOT / "workflows/video_release/scripts/muse_render.py",
    "captions":  ROOT / "workflows/video_release/scripts/muse_captions.py",
    "short":     ROOT / "workflows/shorts_first_proof/scripts/muse_shorts.py",
    "tidy":      ROOT / "muse_tidy.py",
}
# 단축 alias → (대상, 선행 인자)
ALIAS = {
    "doctor": ("project", ["doctor"]),
    "status": ("project", ["status"]),
}

USAGE = __doc__


def run(script: Path, args: list[str]) -> int:
    if not script.exists():
        print(f"스크립트 없음: {script}", file=sys.stderr)
        return 2
    return subprocess.run([sys.executable, str(script), *args]).returncode


def cmd_list() -> int:
    reg = ROOT / "workflows/registry.json"
    data = json.loads(reg.read_text(encoding="utf-8"))
    print("Project Muse workflows (registry.json):\n")
    for name in data.get("pipeline_order", []):
        wf = data["workflows"][name]
        print(f"  {name:20} [{wf['type']:10}] {wf['stage']}")
    print("\n상세 = workflows/README.md · CLI = python muse.py <project|audio|thumbnail|render|tidy|doctor|status|list>")
    return 0


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(USAGE)
        return 0
    cmd, rest = argv[0], argv[1:]
    if cmd == "list":
        return cmd_list()
    if cmd in ALIAS:
        target, prefix = ALIAS[cmd]
        return run(SCRIPTS[target], prefix + rest)
    if cmd in SCRIPTS:
        return run(SCRIPTS[cmd], rest)
    print(f"알 수 없는 명령: {cmd}\n", file=sys.stderr)
    print(USAGE)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
