#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WS2 — 선배 채널 경쟁 분석 pull (YouTube Data API v3, public data only).

Atelier Miku A Cappella 경쟁력 로드맵 WS2.
대상 보컬로이드/MIDI 클래식 편곡 채널을 Data API v3 로 계측:
  - 채널 해결 (channels?forHandle → fallback search.list type=channel)
  - statistics (subs / video_count / view_count) + uploads playlist
  - uploads playlist 워크 (playlistItems.list, 1 unit) → 영상 id 수집
  - videos.list (part=snippet,statistics; 1 unit/50개) → 제목/태그/조회수/업로드일/defaultLanguage/localizations
  - 상위 조회수 영상, 태그 패턴, 업로드 케이던스, 다룬 곡(공급 지도), 다국어 여부

쿼터: search.list = 100u (해결 fallback 시만), 나머지 list = 1u. 50영상/페이지.
원본 응답 → Analytics/competitor_raw.json 캐시 (재호출 시 --use-cache 로 쿼터 0).

실행:
  python Analytics/competitor_pull.py            # API 호출 (캐시 없으면)
  python Analytics/competitor_pull.py --use-cache  # 캐시만 사용, 쿼터 0
  python Analytics/competitor_pull.py --max 200    # 채널당 최대 영상 수 (기본 300)
"""
import sys
import json
import argparse
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE = Path(__file__).resolve().parent.parent          # Project_Muse/
RAW = Path(__file__).resolve().parent / "competitor_raw.json"

# (handle, fallback_search_query) — 핸들 우선, 실패 시 검색어로 type=channel
# Bocaro Choir: 전용 채널 없음. "Ave Maria - Hatsune Miku with Bocaro Choir" 단일 업로드가
#   개인 음악 아카이브 채널 @banana-ux7ff (UCWmPHv5kzr8sTSAT-y0cyHA)에 존재. 채널 통계는
#   Bocaro Choir 작업물을 대표하지 않음 → teardown에서 'dedicated 채널 부재'로 처리.
# Gnagre: 실제 핸들 @gnagre3 (UCuI7C8E48rt2MXj3LBMY_6Q · 미쿠 모차르트 아카펠라).
TARGETS = [
    ("EARLYMUSICMIDI", "EARLY MUSIC MIDI"),
    ("pikabonT", "pikabonT vocaloid"),
    ("hamofanjoe", "hamofanjoe"),
    ("gnagre3", "gnagre3 Hatsune Miku"),
]

API = "https://www.googleapis.com/youtube/v3/"


def load_api_key():
    envp = BASE / ".env"
    if not envp.exists():
        sys.exit(f"[FATAL] .env 없음: {envp}")
    for line in envp.read_text(encoding="utf-8").splitlines():
        if line.startswith("YOUTUBE_API_KEY"):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("[FATAL] .env 에 YOUTUBE_API_KEY 없음")


class Quota:
    used = 0


def api_get(endpoint, params, api_key, cost):
    params = dict(params)
    params["key"] = api_key
    url = API + endpoint + "?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            data = json.load(r)
        Quota.used += cost
        return data
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        raise RuntimeError(f"HTTP {e.code} on {endpoint}: {body}") from e


def resolve_channel(handle, query, api_key):
    """forHandle 우선 → 실패 시 search.list. (channelId, uploads_playlist, snippet, stats, method)"""
    # 1) forHandle (1u)
    d = api_get("channels",
                {"part": "snippet,statistics,contentDetails",
                 "forHandle": "@" + handle, "maxResults": 1},
                api_key, 1)
    if d.get("items"):
        it = d["items"][0]
        return _pack(it, "forHandle"), d
    # 2) forUsername (1u) — 레거시 유저네임
    d2 = api_get("channels",
                 {"part": "snippet,statistics,contentDetails",
                  "forUsername": handle, "maxResults": 1},
                 api_key, 1)
    if d2.get("items"):
        it = d2["items"][0]
        return _pack(it, "forUsername"), d2
    # 3) search.list type=channel (100u)
    s = api_get("search",
                {"part": "snippet", "q": query, "type": "channel", "maxResults": 5},
                api_key, 100)
    if not s.get("items"):
        return None, {"forHandle": d, "search": s}
    cid = s["items"][0]["snippet"]["channelId"]
    d3 = api_get("channels",
                 {"part": "snippet,statistics,contentDetails", "id": cid},
                 api_key, 1)
    if d3.get("items"):
        it = d3["items"][0]
        return _pack(it, "search"), {"search": s, "channels": d3}
    return None, {"forHandle": d, "search": s}


def _pack(it, method):
    return {
        "channelId": it["id"],
        "title": it["snippet"]["title"],
        "publishedAt": it["snippet"].get("publishedAt"),
        "country": it["snippet"].get("country"),
        "uploads": it["contentDetails"]["relatedPlaylists"]["uploads"],
        "statistics": it["statistics"],
        "resolve_method": method,
    }


def walk_uploads(uploads_pl, api_key, max_videos):
    """playlistItems.list (1u/page) → video id 목록."""
    ids, token = [], None
    while len(ids) < max_videos:
        params = {"part": "contentDetails", "playlistId": uploads_pl, "maxResults": 50}
        if token:
            params["pageToken"] = token
        d = api_get("playlistItems", params, api_key, 1)
        for it in d.get("items", []):
            vid = it["contentDetails"].get("videoId")
            if vid:
                ids.append(vid)
        token = d.get("nextPageToken")
        if not token:
            break
    return ids[:max_videos]


def fetch_videos(video_ids, api_key):
    """videos.list part=snippet,statistics (1u/50)."""
    out = []
    for i in range(0, len(video_ids), 50):
        chunk = video_ids[i:i + 50]
        d = api_get("videos",
                    {"part": "snippet,statistics", "id": ",".join(chunk), "maxResults": 50},
                    api_key, 1)
        for it in d.get("items", []):
            sn = it["snippet"]
            st = it.get("statistics", {})
            out.append({
                "id": it["id"],
                "title": sn.get("title"),
                "publishedAt": sn.get("publishedAt"),
                "tags": sn.get("tags", []),
                "defaultLanguage": sn.get("defaultLanguage"),
                "defaultAudioLanguage": sn.get("defaultAudioLanguage"),
                "localized": sn.get("localized", {}),
                "viewCount": int(st["viewCount"]) if "viewCount" in st else None,
                "likeCount": int(st["likeCount"]) if "likeCount" in st else None,
                "commentCount": int(st["commentCount"]) if "commentCount" in st else None,
            })
    return out


def pull(api_key, max_videos):
    result = {"_quota_note": "search.list=100u, others=1u/call", "channels": {}}
    for handle, query in TARGETS:
        print(f"\n=== {handle} ({query}) ===")
        try:
            ch, raw = resolve_channel(handle, query, api_key)
        except RuntimeError as e:
            print(f"  [ERROR resolve] {e}")
            result["channels"][handle] = {"resolved": False, "error": str(e)}
            continue
        if not ch:
            print("  [NOT RESOLVED] 핸들/검색 모두 실패")
            result["channels"][handle] = {"resolved": False, "error": "no channel found"}
            continue
        print(f"  -> {ch['title']}  ({ch['channelId']})  via {ch['resolve_method']}")
        st = ch["statistics"]
        print(f"     subs={st.get('subscriberCount')} videos={st.get('videoCount')} views={st.get('viewCount')}")
        try:
            vids_ids = walk_uploads(ch["uploads"], api_key, max_videos)
            print(f"     walked {len(vids_ids)} upload ids")
            videos = fetch_videos(vids_ids, api_key)
            print(f"     fetched {len(videos)} video details")
        except RuntimeError as e:
            print(f"  [ERROR videos] {e}")
            ch["resolved"] = True
            ch["video_pull_error"] = str(e)
            ch["videos"] = []
            result["channels"][handle] = ch
            continue
        ch["resolved"] = True
        ch["videos"] = videos
        result["channels"][handle] = ch
    result["_quota_used"] = Quota.used
    return result


def summarize(result):
    print("\n\n########## SUMMARY ##########")
    for handle, ch in result["channels"].items():
        print(f"\n--- {handle} ---")
        if not ch.get("resolved"):
            print(f"  NOT RESOLVED: {ch.get('error')}")
            continue
        st = ch["statistics"]
        print(f"  title         : {ch['title']}")
        print(f"  channelId     : {ch['channelId']}")
        print(f"  resolve_method: {ch['resolve_method']}")
        print(f"  created       : {ch.get('publishedAt')}  country={ch.get('country')}")
        print(f"  subs          : {st.get('subscriberCount')}")
        print(f"  videoCount    : {st.get('videoCount')}")
        print(f"  viewCount     : {st.get('viewCount')}")
        vids = ch.get("videos", [])
        print(f"  pulled videos : {len(vids)}")
        if ch.get("video_pull_error"):
            print(f"  video_error   : {ch['video_pull_error']}")
        if not vids:
            continue
        # top 10 by views
        top = sorted([v for v in vids if v["viewCount"] is not None],
                     key=lambda v: v["viewCount"], reverse=True)[:10]
        print("  TOP 10 by views:")
        for v in top:
            print(f"    {v['viewCount']:>9,}  {v['publishedAt'][:10]}  {v['title']}")
        # multilingual
        ml = [v for v in vids if len(v.get("localized") and v["localized"] or {}) and v.get("localized", {}).get("title") != v["title"]]
        with_loc_field = [v for v in vids if v.get("defaultLanguage")]
        print(f"  defaultLanguage set on {len(with_loc_field)}/{len(vids)} videos")
        # tag frequency
        from collections import Counter
        tagc = Counter()
        for v in vids:
            for t in v.get("tags", []):
                tagc[t.lower()] += 1
        print(f"  total distinct tags: {len(tagc)} ; top 15:")
        for t, c in tagc.most_common(15):
            print(f"    {c:>3}x  {t}")
        # upload cadence (per year)
        yrc = Counter(v["publishedAt"][:4] for v in vids if v.get("publishedAt"))
        print(f"  uploads by year (within pulled): {dict(sorted(yrc.items()))}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--use-cache", action="store_true", help="캐시만 사용, 쿼터 0")
    ap.add_argument("--max", type=int, default=300, help="채널당 최대 영상 수 (기본 300)")
    args = ap.parse_args()

    if args.use_cache and RAW.exists():
        result = json.loads(RAW.read_text(encoding="utf-8"))
        print(f"[cache] {RAW.name} 로드 (쿼터 0)")
    else:
        api_key = load_api_key()
        result = pull(api_key, args.max)
        RAW.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n[saved] {RAW}  (quota used this run: {Quota.used} units)")
    summarize(result)


if __name__ == "__main__":
    main()
