#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""일회용: 1년 성장 예측을 위한 일별 시계열 + 현재 총계 pull (s387).
Analytics OAuth 토큰(읽기) 재사용 + Data API key 총계. 출력 = growth_raw.json + 콘솔."""
import sys, json, os, datetime as dt
from pathlib import Path
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import urllib.request

BASE = Path(__file__).resolve().parent.parent.parent  # Analytics/_archive/ → Project_Muse/
TOKEN = BASE / ".youtube_oauth_token.json"
SCOPES = ["https://www.googleapis.com/auth/yt-analytics.readonly",
          "https://www.googleapis.com/auth/youtube.readonly"]
HANDLE = "AtelierMikuAcappella"
CREATED = "2026-05-13"
TODAY = dt.date.today().isoformat()

# --- API key ---
api_key = None
envp = BASE / ".env"
if envp.exists():
    for line in envp.read_text(encoding="utf-8").splitlines():
        if line.startswith("YOUTUBE_API_KEY"):
            api_key = line.split("=", 1)[1].strip().strip('"')

# --- OAuth (analytics) ---
creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
if not creds.valid and creds.expired and creds.refresh_token:
    creds.refresh(Request())
    TOKEN.write_text(creds.to_json(), encoding="utf-8")
yta = build("youtubeAnalytics", "v2", credentials=creds)

out = {"created": CREATED, "today": TODAY}

# 1) 일별 시계열 (채널 생성 이후 전체)
resp = yta.reports().query(
    ids="channel==MINE", startDate=CREATED, endDate=TODAY,
    metrics="views,estimatedMinutesWatched,subscribersGained,subscribersLost,likes,comments",
    dimensions="day", sort="day").execute()
hdr = [h["name"] for h in resp.get("columnHeaders", [])]
rows = resp.get("rows", [])
out["daily_headers"] = hdr
out["daily"] = rows

# 2) 누적 전체기간 합계 (lifetime, 채널 생성 이후)
resp2 = yta.reports().query(
    ids="channel==MINE", startDate=CREATED, endDate=TODAY,
    metrics="views,estimatedMinutesWatched,subscribersGained,subscribersLost,likes,comments,shares").execute()
out["lifetime_headers"] = [h["name"] for h in resp2.get("columnHeaders", [])]
out["lifetime"] = resp2.get("rows", [[]])[0] if resp2.get("rows") else []

# 3) Data API 총계 (총 구독자/총 조회수/영상수 — 현재 시점 절대값)
if api_key:
    url = (f"https://www.googleapis.com/youtube/v3/channels?part=statistics,snippet"
           f"&forHandle=@{HANDLE}&key={api_key}")
    with urllib.request.urlopen(url) as r:
        d = json.load(r)
    it = d["items"][0]
    out["data_api_stats"] = it["statistics"]
    out["data_api_published"] = it["snippet"].get("publishedAt")

# 출력
print("=== LIFETIME (channel since %s) ===" % CREATED)
print(out["lifetime_headers"])
print(out["lifetime"])
print("\n=== DATA API STATS (current absolute) ===")
print(out.get("data_api_stats"))
print("published:", out.get("data_api_published"))
print("\n=== DAILY (%d rows) ===" % len(rows))
print("  ", hdr)
for row in rows:
    print("  ", row)

(Path(__file__).resolve().parent / "growth_raw.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print("\nsaved -> Analytics/_archive/growth_raw.json")
