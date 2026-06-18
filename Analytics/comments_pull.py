#!/usr/bin/env python3
"""comments_pull.py — Atelier Miku A Cappella 댓글 수집기 (시스템 layer 1/3).

발행작 전체의 YouTube 댓글(최상위 + 답글)을 commentThreads/comments API로 끌어와
`Analytics/comments.csv`에 **comment_id upsert** 시계열로 누적한다.

분석 시스템 3층 중 **수집기**:
  1. comments_pull.py      ← 본 파일 (API → comments.csv · 결정적/재현 가능)
  2. (MOKA 분석 패스)       comments.csv → comments_analyzed.csv (정서/카테고리/요청곡/언어 태깅)
  3. (리포트)              comments_report.md (영상별 볼륨·정서 + 미처리 선곡요청 + AI회의 워치 + 튜토 수요)

설계 결정 (2026-06-16 코튼):
- **전부 수집 + 태깅**(드롭 X). 우리 채널 댓글(고정댓글·요청 답글)은 `is_own=1`로 분리
  → 청중 정서/볼륨 집계에서 제외하되, **스레드 맥락**(요청 상태 = 답글 달았나)용으로 보존.
- **답글 전부 수집**(`is_reply` + `parent_id`). "ai slop" 같은 회의 스레드의 전개가 신호.
- `is_own` 판정 = author **channel_id** == 우리 채널 id (텍스트 매칭 X · 정확).

권한 = `youtube.force-ssl` (댓글 read는 readonly로 부족 = API 사양 · youtube_meta 쓰기 토큰 공용).
쿼터 = commentThreads.list 1 unit/page(100개) · 현 볼륨 무시 가능.

사용:
  python Analytics/comments_pull.py            # 수집 → comments.csv upsert
  python Analytics/comments_pull.py --show     # 수집 후 콘솔에 최신순 덤프
"""
import argparse
import csv
import datetime as dt
import io
import sys
from pathlib import Path

# 콘솔 cp949 깨짐 방지 (한/일 댓글) — 파일은 항상 UTF-8.
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

try:
    from googleapiclient.discovery import build
except ImportError:
    sys.exit("의존성 미설치 — Analytics/README.md 참고 (google-api-python-client).")

# 같은 폴더 모듈 재사용: 인증(force-ssl) + 발행작 목록.
import youtube_meta          # get_credentials (force-ssl 쓰기 토큰)
import youtube_analytics     # VIDEOS dict (vid → 표시명)

ANALYTICS_DIR = Path(__file__).resolve().parent
COMMENTS_CSV = ANALYTICS_DIR / "comments.csv"

FIELDS = [
    "comment_id", "video_id", "video_name", "is_reply", "parent_id", "is_own",
    "author", "author_channel_id", "published_at", "updated_at",
    "like_count", "reply_count", "first_seen", "last_seen", "text",
]


def _today():
    return dt.date.today().isoformat()


def _row_from_snippet(sn, video_id, video_name, our_cid, parent_id):
    """top-level/reply 공통 snippet → row dict (first/last_seen 제외)."""
    acid = sn.get("authorChannelId", {}).get("value", "")
    return {
        "comment_id": "",  # 호출부에서 채움
        "video_id": video_id,
        "video_name": video_name,
        "is_reply": 1 if parent_id else 0,
        "parent_id": parent_id or "",
        "is_own": 1 if acid and acid == our_cid else 0,
        "author": sn.get("authorDisplayName", ""),
        "author_channel_id": acid,
        "published_at": sn.get("publishedAt", ""),
        "updated_at": sn.get("updatedAt", ""),
        "like_count": sn.get("likeCount", 0),
        "reply_count": 0,
        "text": (sn.get("textOriginal", "") or "").replace("\r", " ").replace("\n", " ").strip(),
    }


def load_existing():
    if not COMMENTS_CSV.exists():
        return {}
    with COMMENTS_CSV.open(encoding="utf-8", newline="") as f:
        return {r["comment_id"]: r for r in csv.DictReader(f) if r.get("comment_id")}


def fetch_all_replies(yt, parent_id, video_id, video_name, our_cid):
    """답글 5개 초과 스레드 = comments.list로 전수 페이지네이션."""
    out, tok = [], None
    while True:
        resp = yt.comments().list(
            part="snippet", parentId=parent_id, maxResults=100,
            pageToken=tok, textFormat="plainText",
        ).execute()
        for it in resp.get("items", []):
            row = _row_from_snippet(it["snippet"], video_id, video_name, our_cid, parent_id)
            row["comment_id"] = it["id"]
            out.append(row)
        tok = resp.get("nextPageToken")
        if not tok:
            return out


def collect(yt, our_cid):
    rows = []
    for vid, name in youtube_analytics.VIDEOS.items():
        tok = None
        while True:
            try:
                resp = yt.commentThreads().list(
                    part="snippet,replies", videoId=vid, maxResults=100,
                    pageToken=tok, textFormat="plainText", order="time",
                ).execute()
            except Exception as e:  # noqa: BLE001 — 댓글 비활성/삭제 영상 등은 스킵
                print(f"  ! {name} 스킵: {str(e)[:80]}")
                break
            for it in resp.get("items", []):
                top_sn = it["snippet"]["topLevelComment"]["snippet"]
                top_id = it["snippet"]["topLevelComment"]["id"]
                n_replies = it["snippet"].get("totalReplyCount", 0)
                top = _row_from_snippet(top_sn, vid, name, our_cid, parent_id="")
                top["comment_id"] = top_id
                top["reply_count"] = n_replies
                rows.append(top)
                # 답글: 인라인 5개 이하면 그대로, 초과면 전수 재조회.
                inline = it.get("replies", {}).get("comments", [])
                if n_replies and n_replies > len(inline):
                    rows.extend(fetch_all_replies(yt, top_id, vid, name, our_cid))
                else:
                    for rc in inline:
                        r = _row_from_snippet(rc["snippet"], vid, name, our_cid, parent_id=top_id)
                        r["comment_id"] = rc["id"]
                        rows.append(r)
            tok = resp.get("nextPageToken")
            if not tok:
                break
    return rows


def upsert(fetched):
    """fetched rows를 comments.csv에 comment_id 기준 upsert. (수집수, 누적수, 신규수) 반환."""
    existing = load_existing()
    prev_ids = set(existing)
    today = _today()
    seen = set()
    for row in fetched:
        cid = row["comment_id"]
        seen.add(cid)
        prev = existing.get(cid)
        row["first_seen"] = prev["first_seen"] if prev else today
        row["last_seen"] = today
        existing[cid] = row
    # 사라진(삭제된) 댓글은 보존하되 last_seen 미갱신 = 이탈 추적 가능.
    with COMMENTS_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for cid, row in sorted(existing.items(), key=lambda kv: kv[1].get("published_at", "")):
            w.writerow({k: row.get(k, "") for k in FIELDS})
    new = len(seen - prev_ids)
    return len(seen), len(existing), new


def main():
    ap = argparse.ArgumentParser(description="Atelier Miku A Cappella 댓글 수집기")
    ap.add_argument("--show", action="store_true", help="수집 후 최신순 콘솔 덤프")
    args = ap.parse_args()

    creds = youtube_meta.get_credentials()
    yt = build("youtube", "v3", credentials=creds)
    me = yt.channels().list(part="id,snippet", mine=True).execute()["items"][0]
    our_cid = me["id"]
    print(f"[comments_pull] 채널 {me['snippet']['title']} ({our_cid}) · 발행작 {len(youtube_analytics.VIDEOS)}편")

    fetched = collect(yt, our_cid)
    pulled, total, new = upsert(fetched)
    own = sum(1 for r in fetched if r["is_own"])
    replies = sum(1 for r in fetched if r["is_reply"])
    print(f"  수집 {pulled}건 (청중 {pulled - own} · 우리 {own} · 답글 {replies}) · 신규 {new} → {COMMENTS_CSV.name} (누적 {total})")

    if args.show:
        print("\n--- 최신순 (date | video | own R=reply | L=likes | text) ---")
        for r in sorted(fetched, key=lambda x: x["published_at"], reverse=True):
            tag = "OWN" if r["is_own"] else ("RPLY" if r["is_reply"] else "    ")
            print(f"{r['published_at'][:10]} | {r['video_name'][:20]:<20} | {tag} | L{r['like_count']} | {r['text'][:70]}")


if __name__ == "__main__":
    main()
