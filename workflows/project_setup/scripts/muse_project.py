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


FOLDERS = [
    "rights",
    "notes",
    "music/renders/dry_stems",
    "music/mix",
    "music/masters",
    "video/art_sources",
    "video/cover",
    "video/visualizer",
    "video/edit_project",
    "video/exports",
    "video/release",
]


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

    print(f"Initialized project workspace: {root}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Project Muse workspace setup")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create a piece workspace")
    init.add_argument("--project", required=True)
    init.set_defaults(func=init_project)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
