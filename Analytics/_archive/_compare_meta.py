# ONE-OFF (2026-05-29 · s375 · 임시 진단)
"""s375 cycle 박힘 — 임시 진단 자료. 5곡 메타데이터 비교 dump."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from youtube_meta import yt

VIDS = [
    ("rRnl8RZ3EjY", "Gymnopedie"),
    ("0qXLYmZXAx0", "Vivaldi"),
    ("DVIYl09zX-w", "Joplin"),
    ("zshjmBhus2I", "Elgar"),
    ("PiR9hy6xmGQ", "Mozart"),
]

svc = yt()
resp = svc.videos().list(
    part="snippet,status,localizations,topicDetails,contentDetails",
    id=",".join(v[0] for v in VIDS),
).execute()

items = {it["id"]: it for it in resp["items"]}

for vid, name in VIDS:
    it = items.get(vid)
    if not it:
        print(f"=== {name} ({vid}) - MISSING ===")
        continue
    sn = it["snippet"]
    st = it.get("status", {})
    cd = it.get("contentDetails", {})
    td = it.get("topicDetails", {})
    locs = it.get("localizations") or {}
    print(f"=== {name} ({vid}) ===")
    print(f"  title:           {sn.get('title')}")
    print(f"  publishedAt:     {sn.get('publishedAt')}")
    print(f"  categoryId:      {sn.get('categoryId')}")
    print(f"  defaultLang:     {sn.get('defaultLanguage')}")
    print(f"  defaultAudioLang:{sn.get('defaultAudioLanguage')}")
    print(f"  duration:        {cd.get('duration')}")
    print(f"  madeForKids:     {st.get('madeForKids')}")
    print(f"  selfDeclaredKids:{st.get('selfDeclaredMadeForKids')}")
    print(f"  privacy:         {st.get('privacyStatus')}")
    print(f"  license:         {st.get('license')}")
    print(f"  embeddable:      {st.get('embeddable')}")
    tags = sn.get("tags", [])
    print(f"  tags({len(tags)}):     {tags}")
    print(f"  localizations:   {list(locs.keys())}")
    print(f"  topicCategories: {td.get('topicCategories', [])}")
    print()
