#!/usr/bin/env python3
"""muse short — 쇼츠 스핀업 도구 (v3 MikuPile 엔진용 · s427).

신곡 쇼츠 1편을 *한 방에* 띄우는 틀. 폴더 생성 · placeholder 스프라이트/폰트 복사 ·
본편 master 오디오 컷(ffmpeg) · 본편 레터박스색 그라디언트 자동 추출 · MikuPile
props.json 스켈레톤 생성까지 자동. 이후 = props 텍스트 3칸(곡명·훅·#N) 손보고
`muse render <work_id> --short <slug> --comp MikuPile`.

사용:
  python muse.py short init <work_id> <slug> [옵션]
    --start 0       오디오 컷 시작 (초 또는 MM:SS · ffmpeg 양식)
    --dur 22        오디오 컷 길이(초)
    --master <wav>  master 오디오 경로 override (기본 = 자동 탐지)
    --n 3           성부 수 N (= "미쿠 노동력 N명")
    --bpm 100       비트싱크 BPM (곡별 · 기본 placeholder → 편집 권장)
    --beats 4       마디당 박 (기본 4)
    --ep 1          회차 번호 #N
    --gradient "#a,#b,#c"   그라디언트 override (기본 = 본편 레터박스색 자동)
    --force         기존 슬러그 덮어쓰기

설계 = workflows/shorts_first_proof/docs/v3_engine_design.md
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[3]
PLACEHOLDER = ROOT / "workflows/shorts_first_proof/assets/placeholder"
DEFAULT_GRADIENT = ["#1f2c3d", "#4a5a6e", "#b8a673"]


def find_master(work: Path, override: str | None) -> Path | None:
    """본편 master.wav 자동 탐지 (신/구 폴더 구조 모두)."""
    if override:
        p = Path(override)
        return p if p.exists() else None
    candidates: list[Path] = []
    candidates += sorted(work.glob("music/masters/*.wav"))
    candidates += sorted(work.glob("music/**/render_ready*/*.wav"))
    candidates += sorted(work.glob("music/**/*master*.wav"))
    candidates += sorted(work.glob("music/**/*.wav"))
    return candidates[0] if candidates else None


def pull_gradient(work: Path) -> tuple[list[str], str]:
    """본편 visualizer props.json 에서 letterboxColors 추출 (없으면 기본+경고)."""
    p = work / "video/visualizer/props.json"
    if p.exists():
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            lc = data.get("letterboxColors")
            if isinstance(lc, list) and len(lc) == 3:
                return list(lc), f"본편 추출 ({p.relative_to(ROOT)})"
        except Exception:
            pass
    return list(DEFAULT_GRADIENT), "⚠️ 본편 props 없음 → 기본값 (props.json 손수 교체 권장)"


def cmd_init(a: argparse.Namespace) -> int:
    work = ROOT / "works" / a.work_id
    if not work.exists():
        print(f"work 없음: {work}", file=sys.stderr)
        return 2

    base = work / "shorts" / a.slug
    if base.exists() and not a.force:
        print(f"이미 존재: {base.relative_to(ROOT)} (덮어쓰려면 --force)", file=sys.stderr)
        return 2

    master = find_master(work, a.master)
    if not master:
        print(f"master 오디오 못 찾음 (--master 로 지정). 탐지 = music/masters/*.wav · "
              f"music/**/render_ready*/*.wav", file=sys.stderr)
        return 2

    public = base / "public"
    (public / "fonts").mkdir(parents=True, exist_ok=True)
    (base / "exports").mkdir(exist_ok=True)

    # placeholder 스프라이트 + 폰트
    for f in ("miku_wait.png", "miku_sing.png"):
        shutil.copy(PLACEHOLDER / f, public / f)
    shutil.copy(PLACEHOLDER / "fonts/GFSDidot-Regular.ttf", public / "fonts/GFSDidot-Regular.ttf")

    # 오디오 컷 (ffmpeg)
    audio_out = public / "audio.wav"
    cut = ["ffmpeg", "-y", "-ss", str(a.start), "-t", str(a.dur), "-i", str(master), str(audio_out)]
    r = subprocess.run(cut, capture_output=True, text=True)
    if r.returncode != 0 or not audio_out.exists():
        print(f"ffmpeg 컷 실패:\n{r.stderr[-500:]}", file=sys.stderr)
        return 2

    # 그라디언트 = override 우선, 없으면 본편 자동 추출
    if a.gradient:
        parts = [s.strip() for s in a.gradient.split(",")]
        if len(parts) != 3:
            print(f"--gradient 는 '#a,#b,#c' 3색 (받은 값: {a.gradient!r})", file=sys.stderr)
            return 2
        gradient, grad_src = parts, "override (--gradient)"
    else:
        gradient, grad_src = pull_gradient(work)

    # props 스켈레톤
    props = {
        "audioPath": "audio.wav",
        "bpm": a.bpm,
        "beatsPerBar": a.beats,
        "buildStartSec": 4,
        "voiceCount": a.n,
        "spriteWait": "miku_wait.png",
        "spriteSing": "miku_sing.png",
        "gradient": gradient,
        "episodeNo": a.ep,
        "pieceLabel": "TODO: 부제 곡명",
        "hookCaption": "TODO: B층 훅 카피 (곡당 최소 1개 · 필수)",
        "cornerDetail": "39",
        "endCta": "전체 버전은 채널에",
        "durationSeconds": float(a.dur),
    }
    (base / "props.json").write_text(json.dumps(props, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    rel = base.relative_to(ROOT)
    print(f"✓ 쇼츠 스캐폴딩 완료: {rel}")
    print(f"  master   = {master.relative_to(ROOT)}  (cut {a.start} +{a.dur}s)")
    print(f"  gradient = {gradient}  [{grad_src}]")
    print(f"  N        = {a.n}  · bpm={a.bpm} beats={a.beats} (곡별 · props 확인)")
    print(f"  스프라이트 = placeholder (실 미쿠 아트 = public/miku_*.png 교체)")
    print(f"\n다음:")
    print(f"  1. {rel}/props.json 에서 pieceLabel · hookCaption · bpm/beatsPerBar 손보기")
    print(f"  2. python muse.py render {a.work_id} --short {a.slug} --comp MikuPile --still 90  # 미리보기")
    print(f"  3. python muse.py render {a.work_id} --short {a.slug} --comp MikuPile             # 풀 렌더")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="muse short", description="쇼츠 스핀업 (v3 MikuPile)")
    sub = ap.add_subparsers(dest="sub", required=True)
    ini = sub.add_parser("init", help="신곡 쇼츠 스캐폴딩 (폴더+스프라이트+오디오컷+props)")
    ini.add_argument("work_id")
    ini.add_argument("slug")
    ini.add_argument("--start", default="0", help="오디오 컷 시작 (초 또는 MM:SS)")
    ini.add_argument("--dur", type=int, default=22, help="오디오 컷 길이(초)")
    ini.add_argument("--master", help="master 오디오 경로 override")
    ini.add_argument("--n", type=int, default=3, help="성부 수 N")
    ini.add_argument("--bpm", type=int, default=100, help="BPM (곡별)")
    ini.add_argument("--beats", type=int, default=4, help="마디당 박")
    ini.add_argument("--ep", type=int, default=1, help="회차 번호 #N")
    ini.add_argument("--gradient", help='그라디언트 override "#a,#b,#c"')
    ini.add_argument("--force", action="store_true", help="기존 슬러그 덮어쓰기")
    a = ap.parse_args(argv)

    if a.sub == "init":
        return cmd_init(a)
    ap.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
