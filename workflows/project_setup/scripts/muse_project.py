#!/usr/bin/env python3
"""Project Muse workspace setup.

Creates a piece workspace with the folder layout the manual-V6 workflow uses.
The previous auto-MIDI pipeline (MusicXML in / MIDI out) is gone, so this
script no longer wraps muse_workflow.py.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
import shutil

# Windows cp949 한글 깨짐 방어 (s355 광역 audit)
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


# 정본 골격.
# CORE  = git 영속 골격. 항상 생성 + 빈 폴더는 .gitkeep으로 영속화. doctor 누락 = FAIL.
#         (내용물이 tracked이거나, dir 자체는 gitignore 안 됨 → .gitkeep 추적 가능)
# LOCAL = 스캐폴더가 만들지만 내용물이 .gitignore 대상(렌더/마스터/바이너리)인 로컬 작업 폴더.
#         git 영속 불가 → .gitkeep X. doctor 누락 = info (FAIL X).
CORE_FOLDERS = [
    "rights",
    "notes",
    "music/mix",
    "video/art_sources",
    "video/cover",
    "video/visualizer",
    "video/exports",
    "video/release",
]
LOCAL_FOLDERS = [
    "music/renders/dry_stems",   # .gitignore: works/*/music/renders/
    "music/masters",             # .gitignore: works/*/music/masters/
    "music/source_scores",       # V6 진입 시 ASCII PDF copy (on-demand)
    "video/edit_project",        # 외부 영상 편집 프로젝트 (일부 작품만)
]
OPTIONAL_FOLDERS = LOCAL_FOLDERS
FOLDERS = CORE_FOLDERS + LOCAL_FOLDERS


PROJECT_JSON_DEFAULT = {
    "piece": "",
    "composer": "",
    "section": "",
    "vocal": "Hatsune Miku",
    "music": {
        "source_score_planning": "planning/candidates_opus/<filename>.pdf",
        "dry_stems_dir": "music/renders/dry_stems",
        "master_audio": "music/masters/master.wav",
    },
    "video": {
        "brief": "video/video-brief.md",
        "final_video": "video/exports/final_4k.mp4",
    },
    "rights_log": "rights/rights-log.md",
}


STATUS_JSON_DEFAULT = {
    "current_phase": "project_setup",
    "rights": "not_started",
    "vocal_input_v6": "not_started",
    "dry_stems": "not_started",
    "master": "not_started",
    "listening_decision": "not_started",
    "video_release": "not_started",
    "last_decision": "Workspace initialized; fill project metadata and rights log next.",
}


LISTENING_NOTES_TEMPLATE = (
    "# Listening Notes\n\n"
    "## v001\n\n"
    "- Date:\n"
    "- Piece section:\n"
    "- What works:\n"
    "- What fails:\n"
    "- Decision:\n"
)


def readme_template(name: str) -> str:
    return (
        f"# {name}\n\n"
        "PDF score lives in `Project_Muse/planning/candidates_opus/`. Reference\n"
        "it from there directly — no copy lands in the work folder.\n\n"
        "Fill `rights/rights-log.md` before entering V6.\n\n"
        "`music/` holds the V6 output side (dry_stems / mix / masters).\n"
        "`video/` is the separate YouTube packaging step that runs only after the\n"
        "audio is worth presenting.\n"
    )


def copy_template(template_root: Path, template_name: str, destination: Path) -> None:
    source = template_root / template_name
    if source.exists() and not destination.exists():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def init_project(args: argparse.Namespace) -> int:
    root = Path(args.project)
    workflows_root = Path(__file__).resolve().parents[2]
    music_template_root = workflows_root / "music_acappella" / "templates"
    video_template_root = workflows_root / "video_release" / "templates"
    shared_template_root = workflows_root / "shared" / "templates"

    for folder in FOLDERS:
        (root / folder).mkdir(parents=True, exist_ok=True)

    copy_template(shared_template_root, "rights-log.md", root / "rights" / "rights-log.md")
    copy_template(music_template_root, "listening-scorecard.csv", root / "music" / "mix" / "listening-scorecard.csv")

    for template_name, destination_name in [
        ("video-brief.md", "video/video-brief.md"),
        ("visualizer-spec.md", "video/visualizer-spec.md"),
    ]:
        copy_template(video_template_root, template_name, root / destination_name)

    project_json = root / "project.json"
    if not project_json.exists():
        write_json(project_json, PROJECT_JSON_DEFAULT)

    status_json = root / "status.json"
    if not status_json.exists():
        write_json(status_json, STATUS_JSON_DEFAULT)

    notes_path = root / "notes" / "listening-notes.md"
    if not notes_path.exists():
        write_text(notes_path, LISTENING_NOTES_TEMPLATE)

    readme_path = root / "README.md"
    if not readme_path.exists():
        write_text(readme_path, readme_template(root.name))

    # 끝까지 빈 CORE 폴더만 .gitkeep으로 git 영속화 (LOCAL은 gitignore 대상이라 제외)
    for folder in CORE_FOLDERS:
        target = root / folder
        if target.is_dir() and not any(target.iterdir()):
            (target / ".gitkeep").write_text("", encoding="utf-8")

    print(f"Initialized project workspace: {root}")
    return 0


# ---------------------------------------------------------------------------
# doctor / status — 정본 골격 lint + 전 작품 진척 대시보드 (s382 reorg P2)
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]          # Project_Muse/
WORKS_DIR = PROJECT_ROOT / "works"

REQUIRED_FILES = ["project.json", "status.json", "README.md"]
OPTIONAL_FILES = ["rights/rights-log.md", "notes/listening-notes.md"]   # 없으면 info (error X)
MISPLACED_EXTS = {".vpr", ".wav", ".mp4", ".mov", ".aiff", ".flac", ".mid", ".midi"}
LEGACY_MARKER = "_LEGACY.md"
STATUS_KEYS = ["current_phase", "rights", "vocal_input_v6", "dry_stems",
               "master", "listening_decision", "video_release"]


def iter_works() -> list[Path]:
    if not WORKS_DIR.exists():
        return []
    return sorted(p for p in WORKS_DIR.iterdir()
                  if p.is_dir() and not p.name.startswith("_"))


def doctor_one(work: Path, fix: bool = False) -> dict:
    """work 1개를 정본 골격 대비 검사. fix=True면 누락 CORE 폴더를 .gitkeep과 함께 생성."""
    if (work / LEGACY_MARKER).exists():
        return {"name": work.name, "status": "LEGACY", "issues": [], "fixed": []}

    issues: list[str] = []
    fixed: list[str] = []
    for folder in CORE_FOLDERS:
        if not (work / folder).is_dir():
            if fix:
                target = work / folder
                target.mkdir(parents=True, exist_ok=True)
                (target / ".gitkeep").write_text("", encoding="utf-8")
                fixed.append(folder)
            else:
                issues.append(f"FAIL  누락 CORE 폴더: {folder}")
    for folder in OPTIONAL_FOLDERS:
        if not (work / folder).is_dir():
            issues.append(f"info  선택 폴더 없음: {folder}")
    for f in REQUIRED_FILES:
        if not (work / f).exists():
            issues.append(f"FAIL  누락 파일: {f}")
    for f in OPTIONAL_FILES:
        if not (work / f).exists():
            issues.append(f"info  선택 파일 없음: {f}")
    # 작업 폴더 루트에 잘못 놓인 바이너리(naming_convention: music/ 하위가 정본). 자동 이동 X — 수동 결단.
    for child in work.iterdir():
        if child.is_file() and child.suffix.lower() in MISPLACED_EXTS:
            issues.append(f"WARN  루트 오배치: {child.name} → music/renders|masters/ 권장")

    fails = [i for i in issues if i.startswith("FAIL")]
    warns = [i for i in issues if i.startswith("WARN")]
    status = "FAIL" if fails else ("WARN" if warns else "OK")
    return {"name": work.name, "status": status, "issues": issues, "fixed": fixed}


def cmd_doctor(args: argparse.Namespace) -> int:
    works = [Path(args.project)] if args.project else iter_works()
    if not works:
        print("검사할 work 없음.")
        return 0
    worst = 0
    rank = {"OK": 0, "LEGACY": 0, "WARN": 1, "FAIL": 2}
    for work in works:
        r = doctor_one(work, fix=args.fix)
        print(f"[{r['status']:6}] {r['name']}")
        for folder in r.get("fixed", []):
            print(f"          fixed 누락 CORE 폴더 생성: {folder}/.gitkeep")
        for issue in r["issues"]:
            print(f"          {issue}")
        worst = max(worst, rank.get(r["status"], 0))
    return 1 if worst >= 2 else 0   # FAIL 있으면 비정상 종료(CI gate 용)


def cmd_status(args: argparse.Namespace) -> int:
    works = iter_works()
    if not works:
        print("works 없음.")
        return 0
    print(f"{'work':<34} {'phase':<24} {'video':<14} last_decision")
    print("-" * 110)
    for work in works:
        sj = work / "status.json"
        phase = video = last = "—"
        if sj.exists():
            try:
                data = json.loads(sj.read_text(encoding="utf-8"))
                phase = str(data.get("current_phase", "—"))[:23]
                video = str(data.get("video_release", "—"))[:13]
                last = str(data.get("last_decision", "—"))[:48]
            except Exception as exc:
                last = f"(status.json 파싱 실패: {exc})"
        else:
            phase = "(status.json 없음)"
        legacy = " [LEGACY]" if (work / LEGACY_MARKER).exists() else ""
        print(f"{work.name + legacy:<34} {phase:<24} {video:<14} {last}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Project Muse workspace setup")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create a piece workspace")
    init.add_argument("--project", required=True)
    init.set_defaults(func=init_project)

    doctor = sub.add_parser("doctor", help="work을 정본 골격 대비 검사 (--project 생략 시 전 작품)")
    doctor.add_argument("--project", default=None)
    doctor.add_argument("--fix", action="store_true", help="누락 CORE 폴더를 .gitkeep과 함께 생성")
    doctor.set_defaults(func=cmd_doctor)

    status = sub.add_parser("status", help="전 작품 status.json 진척 대시보드")
    status.set_defaults(func=cmd_status)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
