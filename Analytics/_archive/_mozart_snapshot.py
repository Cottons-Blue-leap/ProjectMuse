#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""1회용: Data API v3로 5곡 + 채널 실시간 통계 스냅샷 (작은별 K.265 발행 직후 점검 · s380)."""
import sys, json, urllib.request, urllib.parse, datetime as dt
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE = Path(__file__).resolve().parent.parent
KEY = None
for line in (BASE / ".env").read_text(encoding="utf-8").splitlines():
    if line.startswith("YOUTUBE_API_KEY="):
        KEY = line.split("=", 1)[1].strip()
assert KEY, "no key"

VIDEOS = {
    "PiR9hy6xmGQ": "⑤ Mozart - K.265 작은별 변주곡",
    "zshjmBhus2I": "④ Elgar - Salut d'Amour",
    "DVIYl09zX-w": "③ Joplin - Entertainer",
    "0qXLYmZXAx0": "② Vivaldi - Spring I",
    "rRnl8RZ3EjY": "① Satie - Gymnopédie No.1",
}

def api(path, **params):
    params["key"] = KEY
    url = f"https://www.googleapis.com/youtube/v3/{path}?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)

resp = api("videos", part="statistics,snippet,status", id=",".join(VIDEOS))
items = {it["id"]: it for it in resp.get("items", [])}
now = dt.datetime.now(dt.timezone.utc)
print("측정시각(UTC):", now.strftime("%Y-%m-%d %H:%M:%S"))
print()
for vid, label in VIDEOS.items():
    it = items.get(vid)
    if not it:
        print(f"{label}: (없음 — 비공개거나 미발행)")
        print()
        continue
    st = it["statistics"]
    pub = dt.datetime.fromisoformat(it["snippet"]["publishedAt"].replace("Z", "+00:00"))
    age_h = (now - pub).total_seconds() / 3600
    v = int(st.get("viewCount", 0)); l = int(st.get("likeCount", 0)); c = int(st.get("commentCount", 0))
    lr = (l / v * 100) if v else 0
    priv = it.get("status", {}).get("privacyStatus", "?")
    print(f"{label}  [{vid}]  ({priv})")
    print(f"   발행 {pub.astimezone(dt.timezone(dt.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M KST')}  (경과 {age_h:.1f}h / {age_h/24:.1f}d)")
    print(f"   조회 {v:,} · 좋아요 {l:,} ({lr:.1f}%) · 댓글 {c:,}")
    print()

ch = api("channels", part="statistics,snippet", forHandle="AtelierMikuAcappella")
if ch.get("items"):
    s = ch["items"][0]["statistics"]
    print(f"채널: 구독 {int(s.get('subscriberCount',0)):,} · 총조회 {int(s.get('viewCount',0)):,} · 영상수 {s.get('videoCount')}")
