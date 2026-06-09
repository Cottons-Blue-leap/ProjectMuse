# -*- coding: utf-8 -*-
"""One-off (s402 · 2026-06-06): retrofit live titles to the A Cappella bracket badge.

코튼 결단 (s402): title format `Composer - Piece (feat. 初音ミク)` →
`Composer - Piece 【初音ミク A Cappella】` (long titles → abbreviated `【A Cappella】`).
title_naming_guide.md locked 2026-06-06.

Mechanical, uniform transform across ALL locales of each video:
  replace the trailing  " (feat. 初音ミク)"  with the badge, on the default title
  + every localization title. Everything else (description, tags, category,
  defaultLanguage, per-locale descriptions) is read-modify-write preserved.

Run from Project_Muse/:
  python Analytics/_retrofit_acappella_badge_s402.py --dry-run   # preview all 7×10
  python Analytics/_retrofit_acappella_badge_s402.py             # apply + audit
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import youtube_meta as ym  # reuse OAuth (yt) + _get_video
from googleapiclient.errors import HttpError

OLD_SUFFIX = " (feat. 初音ミク)"
FULL_BADGE = " 【初音ミク A Cappella】"
ABBR_BADGE = " 【A Cappella】"  # long-title fallback (初音ミク guaranteed by thumbnail + tags)

# (video_id, label, abbreviated?)  — Mozart K.265 is long in every locale → abbreviated badge.
VIDEOS = [
    ("rRnl8RZ3EjY", "Satie - Gymnopédie No. 1", False),
    ("0qXLYmZXAx0", "Vivaldi - Spring", False),
    ("DVIYl09zX-w", "Joplin - The Entertainer", False),
    ("zshjmBhus2I", "Elgar - Salut d'Amour", False),
    ("PiR9hy6xmGQ", "Mozart - Variations K.265", True),   # long → 【A Cappella】
    ("9EvpHXE3D1s", "Chopin - Nocturne Op.9 No.2", False),
    ("B9ENEwjgAhc", "Pachelbel - Canon in D", False),
    ("759VCWOtC2w", "Tchaikovsky - Sugar Plum Fairy", False),  # #8 scheduled/private (코튼 2026-06-06 "차이코프스키도 맞춰줘")
]

DRY = "--dry-run" in sys.argv


def transform(title, badge):
    """Swap the feat. suffix for the badge. Returns (new_title, ok)."""
    if OLD_SUFFIX not in title:
        return title, False
    return title.replace(OLD_SUFFIX, badge), True


def retrofit_one(svc, vid, label, badge):
    v = ym._get_video(svc, vid)
    old = v["snippet"]
    locs = dict(v.get("localizations") or {})

    print(f"\n=== {vid} · {label} · badge={badge.strip()} ===")

    # default title
    new_default, ok = transform(old.get("title", ""), badge)
    if not ok:
        print(f"  ⚠️ [default] suffix 못 찾음 → SKIP 전체 영상 (안전): {old.get('title')!r}")
        return False
    print(f"  [default] {old.get('title')!r}\n          → {new_default!r}")

    # every localization title
    new_locs = {}
    warned = False
    for lang, loc in locs.items():
        lt = loc.get("title", "")
        nt, ok = transform(lt, badge)
        if not ok:
            print(f"  ⚠️ [{lang}] suffix 못 찾음 → 이 로케일 유지: {lt!r}")
            warned = True
        entry = dict(loc)
        entry["title"] = nt
        if "description" not in entry:
            entry["description"] = ""
        new_locs[lang] = entry
        print(f"  [{lang}] → {nt!r}")

    # read-modify-write snippet (writable fields only)
    new_snippet = {
        "title": new_default,
        "categoryId": old.get("categoryId"),
        "description": old.get("description", ""),
    }
    if old.get("tags"):
        new_snippet["tags"] = old["tags"]
    if old.get("defaultLanguage"):
        new_snippet["defaultLanguage"] = old["defaultLanguage"]
    if old.get("defaultAudioLanguage"):
        new_snippet["defaultAudioLanguage"] = old["defaultAudioLanguage"]

    if DRY:
        print("  [dry-run] 미적용")
        return True

    body = {"id": vid, "snippet": new_snippet, "localizations": new_locs}
    try:
        svc.videos().update(part="snippet,localizations", body=body).execute()
    except HttpError as e:
        print(f"  ✗ update 실패: {e}")
        return False
    print("  ✓ 적용 완료")
    return not warned


def audit_one(svc, vid, badge):
    v = ym._get_video(svc, vid)
    sn = v["snippet"]
    titles = [("default", sn.get("title", ""))]
    titles += [(l, loc.get("title", "")) for l, loc in (v.get("localizations") or {}).items()]
    bad = []
    for lang, t in titles:
        if OLD_SUFFIX in t:
            bad.append(f"{lang}: still has feat. suffix")
        elif badge.strip() not in t:
            bad.append(f"{lang}: badge missing")
    if bad:
        print(f"  ✗ AUDIT FAIL {vid}: " + " | ".join(bad))
        return False
    print(f"  ✓ AUDIT PASS {vid} ({len(titles)} locales · badge present · no feat. suffix)")
    return True


def main():
    svc = ym.yt()
    print(f"{'DRY-RUN preview' if DRY else 'APPLYING'} · {len(VIDEOS)} videos")
    applied = []
    for vid, label, abbr in VIDEOS:
        badge = ABBR_BADGE if abbr else FULL_BADGE
        ok = retrofit_one(svc, vid, label, badge)
        applied.append((vid, badge, ok))

    if DRY:
        print("\n[dry-run] 끝. 적용하려면 --dry-run 빼고 재실행.")
        return

    print("\n\n========== AUDIT ==========")
    all_ok = True
    for vid, badge, _ in applied:
        if not audit_one(svc, vid, badge):
            all_ok = False
    print("\n" + ("✓ 전수 AUDIT PASS" if all_ok else "✗ AUDIT 실패 항목 있음 — 위 로그 확인"))


if __name__ == "__main__":
    main()
