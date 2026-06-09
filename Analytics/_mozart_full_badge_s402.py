# -*- coding: utf-8 -*-
"""One-off (s402b · 2026-06-06): Mozart K.265 → full badge for consistency.
코튼: "初音ミク가 없는데?" → abbreviated 【A Cappella】 was the single inconsistency;
both fit under YouTube's 100-char cap, so unify Mozart to 【初音ミク A Cappella】 like the other 7.
Live read-modify-write across all 11 locales + audit.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import youtube_meta as ym
from googleapiclient.errors import HttpError

VID = "PiR9hy6xmGQ"
ABBR = "【A Cappella】"
FULL = "【初音ミク A Cappella】"

svc = ym.yt()
v = ym._get_video(svc, VID)
old = v["snippet"]
locs = dict(v.get("localizations") or {})

def fix(t):
    return t.replace(ABBR, FULL) if (ABBR in t and FULL not in t) else t

new_default = fix(old.get("title", ""))
print(f"[default] {old.get('title')!r}\n        → {new_default!r}")
new_locs = {}
for lang, loc in locs.items():
    e = dict(loc)
    e["title"] = fix(loc.get("title", ""))
    if "description" not in e:
        e["description"] = ""
    new_locs[lang] = e
    print(f"  [{lang}] → {e['title']!r}")

snip = {"title": new_default, "categoryId": old.get("categoryId"), "description": old.get("description", "")}
if old.get("tags"): snip["tags"] = old["tags"]
if old.get("defaultLanguage"): snip["defaultLanguage"] = old["defaultLanguage"]
if old.get("defaultAudioLanguage"): snip["defaultAudioLanguage"] = old["defaultAudioLanguage"]

try:
    svc.videos().update(part="snippet,localizations", body={"id": VID, "snippet": snip, "localizations": new_locs}).execute()
except HttpError as e:
    sys.exit(f"update 실패: {e}")
print("✓ 적용")

# audit
v2 = ym._get_video(svc, VID)
titles = [("default", v2["snippet"].get("title", ""))] + [(l, lo.get("title", "")) for l, lo in (v2.get("localizations") or {}).items()]
bad = [l for l, t in titles if FULL not in t]
print("✗ AUDIT FAIL: " + str(bad) if bad else f"✓ AUDIT PASS ({len(titles)} locales · full badge)")
