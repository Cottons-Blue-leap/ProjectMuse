#!/usr/bin/env python3
"""muse_tidy — 일회성 파일 sweep (목록 제시 전용 · 자동 이동/삭제 X).

CONVENTIONS.md §2 정합. `_`프리픽스 스크립트 + 백업 사이드카 + audit dump를 스캔해서
분류 후 목록만 출력한다. 실제 이동은 코튼 승인 후 수동(또는 --archive 플래그)으로.

사용:
  python muse_tidy.py                 # 스캔 + 분류 리포트
  python muse_tidy.py --archive       # ONE-OFF 표식 스크립트를 같은 디렉토리 _archive/로 이동(확인 후)
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent

# 스캔 제외 (holding area + 외부/빌드)
SKIP_DIRS = {".git", "__pycache__", ".tools", "node_modules", ".venv", "venv"}
HOLDING = {"_archive", "_keepers", "_thumbnail_audit", "_TEMPLATE"}

# 재사용 도구 (basename) — _ prefix지만 cycle-agnostic, keep
REUSABLE = {
    "_apply_tier_review.py",
    "_renumber_csv.py",
    "_audit_new_pdfs.py",
    "_render_svg_to_png.py",
}

ONEOFF_RE = re.compile(r"ONE-OFF|1회용|one[_-]?off|일회용", re.IGNORECASE)


def in_holding(path: Path) -> bool:
    return any(part in HOLDING for part in path.parts)


def has_oneoff_tag(path: Path) -> bool:
    try:
        head = path.read_text(encoding="utf-8", errors="ignore")[:800]
    except Exception:
        return False
    return bool(ONEOFF_RE.search(head))


def scan() -> dict[str, list[Path]]:
    buckets: dict[str, list[Path]] = {
        "ONE-OFF (표식 有 · archive 권장)": [],
        "REVIEW (미분류 _ 스크립트 · 코튼 확인)": [],
        "REUSABLE (allowlist · keep)": [],
        "ALREADY HELD (_archive/_keepers/_thumbnail_audit)": [],
    }
    sidecars: list[Path] = []
    for p in ROOT.rglob("*"):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.is_dir():
            continue
        name = p.name
        # 백업 사이드카 + audit dump (info)
        if re.search(r"\.bak(\.|$|_)", name) or name.endswith("_out.txt"):
            sidecars.append(p)
            continue
        if not (name.startswith("_") and name.endswith(".py")):
            continue
        if in_holding(p):
            buckets["ALREADY HELD (_archive/_keepers/_thumbnail_audit)"].append(p)
        elif name in REUSABLE:
            buckets["REUSABLE (allowlist · keep)"].append(p)
        elif has_oneoff_tag(p):
            buckets["ONE-OFF (표식 有 · archive 권장)"].append(p)
        else:
            buckets["REVIEW (미분류 _ 스크립트 · 코튼 확인)"].append(p)
    buckets["_sidecars"] = sidecars
    return buckets


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT)).replace("\\", "/")


def report(buckets: dict[str, list[Path]]) -> None:
    sidecars = buckets.pop("_sidecars", [])
    for title, items in buckets.items():
        print(f"\n## {title}  ({len(items)})")
        for p in sorted(items):
            print(f"   {rel(p)}")
    print(f"\n## 백업 사이드카 · audit dump  ({len(sidecars)}) — 보존 default (삭제 X)")
    for p in sorted(sidecars):
        print(f"   {rel(p)}")
    print("\n※ 이동/삭제 자동 실행 X. ONE-OFF 항목 정리는 --archive (확인 후) 또는 수동.")


def do_archive(buckets: dict[str, list[Path]]) -> int:
    targets = buckets.get("ONE-OFF (표식 有 · archive 권장)", [])
    if not targets:
        print("archive 대상(ONE-OFF 표식) 없음.")
        return 0
    moved = 0
    for p in sorted(targets):
        dest_dir = p.parent / "_archive"
        dest_dir.mkdir(exist_ok=True)
        dest = dest_dir / p.name
        if dest.exists():
            print(f"skip (이미 존재): {rel(dest)}")
            continue
        shutil.move(str(p), str(dest))
        print(f"moved: {rel(p)} → {rel(dest)}")
        moved += 1
    print(f"\n{moved}건 이동. git에서 rename 확인 후 commit.")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="일회성 파일 sweep (목록 제시 전용)")
    ap.add_argument("--archive", action="store_true",
                    help="ONE-OFF 표식 스크립트를 같은 디렉토리 _archive/로 이동")
    args = ap.parse_args(argv)
    buckets = scan()
    if args.archive:
        return do_archive(buckets)
    report(buckets)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
