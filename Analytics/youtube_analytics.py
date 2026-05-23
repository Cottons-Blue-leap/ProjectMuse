#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
youtube_analytics.py — Project Muse SEO 분석 도구 (YouTube Analytics API · OAuth)

Atelier Miku Acappella 채널/영상의 다음 자료를 끌어온다:
  - 트래픽 소스 분포 (검색 / 탐색 / 추천 / 외부 …)
  - 검색어 (실제 검색 쿼리 top N)
  - 시청자 지역
  - 평균 시청 지속률 (영상별)

⚠️ 노출수·노출 CTR(썸네일 클릭률)은 YouTube Analytics API에 없음 — Studio "도달범위" 탭 전용.
   이 도구로는 못 가져온다. CTR은 Studio 스샷으로 봐야 함.

setup·usage = Analytics/README.md.
첫 실행 시 브라우저 OAuth 동의 → 토큰 캐시(.youtube_oauth_token.json). 그 뒤론 자동.

usage:
  python youtube_analytics.py all              # 전부
  python youtube_analytics.py traffic          # 트래픽 소스
  python youtube_analytics.py search           # 검색어 top N
  python youtube_analytics.py geo              # 시청자 지역
  python youtube_analytics.py retention        # 영상별 시청 지속률 (평균)
  python youtube_analytics.py retention-curve  # 영상 안 위치별 지속 곡선 (어디서 빠지나)
옵션:
  --days N            최근 N일 (default 28)
  --start YYYY-MM-DD --end YYYY-MM-DD   명시 기간 (--days 대신)
  --video VIDEO_ID    특정 영상만 (default 채널 전체)
  --top N             검색어/지역 표시 개수 (default 25)
"""

import sys
import csv
import argparse
import datetime as dt
from pathlib import Path

# 콘솔 인코딩 무관 UTF-8 출력 (cp949 콘솔에서 일본어/한국어 검색어 인코딩 크래시 방지)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
except ImportError:
    sys.exit(
        "의존성 미설치. 먼저 실행:\n"
        "  python -m pip install --user google-api-python-client google-auth-oauthlib google-auth-httplib2"
    )

BASE = Path(__file__).resolve().parent.parent          # Project_Muse/
CLIENT_SECRET = BASE / "client_secret.json"
TOKEN_FILE = BASE / ".youtube_oauth_token.json"
SCOPES = [
    "https://www.googleapis.com/auth/yt-analytics.readonly",
    "https://www.googleapis.com/auth/youtube.readonly",
]

# 시리즈 발행작 (영상 ID → 표시명). 신곡 publish 시 여기 추가.
VIDEOS = {
    "rRnl8RZ3EjY": "Gymnopédie No. 1",
    "0qXLYmZXAx0": "Vivaldi - Spring I",
    "DVIYl09zX-w": "Joplin - Entertainer",
}

# `report` 명령 산출물 자리 (스크립트와 같은 Analytics/ 폴더에 함께 둠).
# BASE(=Project_Muse/)엔 시크릿(client_secret·token)만, 출력물은 이 스크립트 옆에.
ANALYTICS_DIR = Path(__file__).resolve().parent

# 트래픽 소스 코드 → 한국어 표시명 (리포트 가독성용).
TRAFFIC_LABELS = {
    "RELATED_VIDEO": "추천 영상",
    "YT_SEARCH": "YouTube 검색",
    "SUBSCRIBER": "구독 피드·홈",
    "EXT_URL": "외부 링크",
    "NO_LINK_OTHER": "직접·알 수 없음",
    "NO_LINK_EMBEDDED": "임베드(외부)",
    "YT_CHANNEL": "채널 페이지",
    "YT_OTHER_PAGE": "기타 YT 페이지",
    "PLAYLIST": "재생목록",
    "NOTIFICATION": "알림",
    "END_SCREEN": "종료 화면",
    "ANNOTATION": "카드·주석",
    "SHORTS": "Shorts 피드",
    "HASHTAGS": "해시태그",
    "CAMPAIGN_CARD": "캠페인 카드",
}

# 국가 코드 → 한국어 (자주 나오는 것만 · 나머지는 코드 그대로).
COUNTRY_LABELS = {
    "US": "미국", "GB": "영국", "JP": "일본", "KR": "한국",
    "CA": "캐나다", "DE": "독일", "FR": "프랑스", "BR": "브라질",
    "ID": "인도네시아", "PH": "필리핀", "TW": "대만", "AU": "호주",
    "MX": "멕시코", "PL": "폴란드", "RU": "러시아", "IN": "인도",
}


# ----------------------------------------------------------------------
# OAuth
# ----------------------------------------------------------------------
def get_credentials():
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CLIENT_SECRET.exists():
                sys.exit(
                    f"client_secret.json 없음:\n  {CLIENT_SECRET}\n"
                    "GCP에서 OAuth 데스크톱 클라이언트 JSON 받아 위 경로에 두기 (Analytics/README.md 참조)."
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
            print("브라우저가 열립니다. 채널 소유 Google 계정으로 로그인·허용하세요…")
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
        print(f"토큰 캐시됨: {TOKEN_FILE.name}")
    return creds


# ----------------------------------------------------------------------
# Report helpers
# ----------------------------------------------------------------------
def daterange(args):
    if args.start and args.end:
        return args.start, args.end
    end = dt.date.today()
    start = end - dt.timedelta(days=args.days)
    return start.isoformat(), end.isoformat()


def run_report(yta, start, end, metrics, dimensions=None, filters=None,
               sort=None, max_results=None):
    params = dict(
        ids="channel==MINE",
        startDate=start,
        endDate=end,
        metrics=metrics,
    )
    if dimensions:
        params["dimensions"] = dimensions
    if filters:
        params["filters"] = filters
    if sort:
        params["sort"] = sort
    if max_results:
        params["maxResults"] = max_results
    resp = yta.reports().query(**params).execute()
    headers = [h["name"] for h in resp.get("columnHeaders", [])]
    rows = resp.get("rows", [])
    return headers, rows


def fmt_int(v):
    try:
        return f"{int(v):,}"
    except (ValueError, TypeError):
        return str(v)


def fmt_pct(v):
    try:
        return f"{float(v):.1f}%"
    except (ValueError, TypeError):
        return str(v)


def print_table(title, headers, rows, formatters=None):
    print(f"\n=== {title} ===")
    if not rows:
        print("  (데이터 없음 — 기간/영상 확인, 또는 Analytics 2~3일 지연)")
        return
    formatters = formatters or {}
    out_rows = []
    for r in rows:
        out = []
        for h, v in zip(headers, r):
            out.append(formatters.get(h, str)(v))
        out_rows.append(out)
    widths = [max(len(headers[i]), *(len(row[i]) for row in out_rows)) for i in range(len(headers))]
    line = "  " + "  ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    print(line)
    print("  " + "  ".join("-" * widths[i] for i in range(len(headers))))
    for row in out_rows:
        print("  " + "  ".join(row[i].ljust(widths[i]) for i in range(len(row))))


# ----------------------------------------------------------------------
# Reports
# ----------------------------------------------------------------------
def report_traffic(yta, start, end, vfilter):
    headers, rows = run_report(
        yta, start, end,
        metrics="views,estimatedMinutesWatched,averageViewDuration",
        dimensions="insightTrafficSourceType",
        filters=vfilter,
        sort="-views",
    )
    print_table(
        "트래픽 소스",
        headers, rows,
        {"views": fmt_int, "estimatedMinutesWatched": fmt_int,
         "averageViewDuration": lambda v: f"{int(v)}s"},
    )


def report_search(yta, start, end, vfilter, top):
    f = "insightTrafficSourceType==YT_SEARCH"
    if vfilter:
        f += ";" + vfilter
    headers, rows = run_report(
        yta, start, end,
        metrics="views",
        dimensions="insightTrafficSourceDetail",
        filters=f,
        sort="-views",
        max_results=top,
    )
    print_table("검색어 (YouTube 검색 유입)", headers, rows, {"views": fmt_int})


def report_geo(yta, start, end, vfilter, top):
    headers, rows = run_report(
        yta, start, end,
        metrics="views,averageViewPercentage",
        dimensions="country",
        filters=vfilter,
        sort="-views",
        max_results=top,
    )
    print_table("시청자 지역", headers, rows,
                {"views": fmt_int, "averageViewPercentage": fmt_pct})


def report_retention(yta, start, end, vfilter):
    headers, rows = run_report(
        yta, start, end,
        metrics="views,averageViewDuration,averageViewPercentage",
        dimensions="video",
        filters=vfilter,
        sort="-views",
        max_results=50,
    )
    # video ID → 표시명 치환
    if "video" in headers:
        vi = headers.index("video")
        for r in rows:
            r[vi] = VIDEOS.get(r[vi], r[vi])
    print_table("영상별 시청 지속률", headers, rows,
                {"views": fmt_int, "averageViewDuration": lambda v: f"{int(v)}s",
                 "averageViewPercentage": fmt_pct})


def report_retention_curve(yta, start, end, video_id, name):
    """영상 안 위치별 시청 지속 곡선 (어디서 빠지는지)."""
    headers, rows = run_report(
        yta, start, end,
        metrics="audienceWatchRatio,relativeRetentionPerformance",
        dimensions="elapsedVideoTimeRatio",
        filters=f"video=={video_id}",
    )
    print(f"\n=== 시청 지속 곡선: {name} ({video_id}) ===")
    if not rows:
        print("  (데이터 없음 — 뷰 부족(임계 미달) 또는 Analytics 2~3일 지연)")
        return
    pi = headers.index("elapsedVideoTimeRatio")
    wi = headers.index("audienceWatchRatio")
    ri = headers.index("relativeRetentionPerformance")
    # 20개 구간(5%)으로 binning + 평균
    bins = [[] for _ in range(21)]
    rel = []
    for r in rows:
        try:
            pos = float(r[pi]); w = float(r[wi])
        except (ValueError, TypeError):
            continue
        bins[min(20, int(round(pos * 20)))].append(w)
        try:
            rel.append(float(r[ri]))
        except (ValueError, TypeError):
            pass
    curve = [(b * 5, sum(vals) / len(vals)) for b, vals in enumerate(bins) if vals]
    if not curve:
        print("  (집계 가능한 구간 없음)")
        return
    maxw = max(w for _, w in curve) or 1.0
    print("  위치   시청비율  그래프 (0% 대비 상대 잔존)")
    for pct, w in curve:
        bar = "#" * int(round(w / maxw * 30))
        print(f"  {pct:>3}%   {w:>5.2f}   {bar}")
    if rel:
        print(f"\n  상대 retention 성능(평균): {sum(rel)/len(rel):.2f}  "
              "(0=최악 · 0.5=동일 길이 영상 중간 · 1=최고)")


# ----------------------------------------------------------------------
# Snapshot 수집 → CSV 시계열 + 한 페이지 리포트 (`report` 명령)
# ----------------------------------------------------------------------
def _num(v, default=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def _pct(a, b):
    a, b = _num(a), _num(b)
    return round(a / b * 100, 1) if b else ""


def _dicts(headers, rows):
    return [dict(zip(headers, r)) for r in rows]


def _delta(cur, prev):
    """이전 측정 대비 증감 문자열. 비교 대상 없으면 빈 문자열."""
    if prev in (None, ""):
        return ""
    try:
        d = float(cur) - float(prev)
    except (TypeError, ValueError):
        return ""
    sign = "+" if d >= 0 else ""
    if abs(d - round(d)) < 1e-9:
        return f"{sign}{int(round(d))}"
    return f"{sign}{d:.1f}"


SNAP_FIELDS = [
    "measured_on", "window_days", "start_date", "end_date",
    "scope", "video_id", "views", "watch_minutes", "avg_view_sec",
    "avg_view_pct", "likes", "comments", "subs_gained", "shares", "like_rate_pct",
]
TRAFFIC_FIELDS = ["measured_on", "window_days", "source_type", "source_label",
                  "views", "watch_minutes", "avg_view_sec", "share_pct"]
GEO_FIELDS = ["measured_on", "window_days", "country", "country_label",
              "views", "avg_view_pct"]
SEARCH_FIELDS = ["measured_on", "window_days", "query", "views"]


def collect_snapshot(yta, start, end, top=25):
    """채널 + 영상별 + 트래픽 + 지역 + 검색어를 한 번에 끌어와 구조화."""
    data = {}
    h, r = run_report(
        yta, start, end,
        metrics="views,estimatedMinutesWatched,averageViewDuration,"
                "averageViewPercentage,likes,comments,subscribersGained,shares")
    data["channel"] = dict(zip(h, r[0])) if r else {}

    h, r = run_report(
        yta, start, end,
        metrics="views,estimatedMinutesWatched,averageViewDuration,"
                "averageViewPercentage,likes,comments,subscribersGained",
        dimensions="video", sort="-views", max_results=50)  # video 차원은 maxResults 필수
    data["videos"] = _dicts(h, r)

    h, r = run_report(
        yta, start, end,
        metrics="views,estimatedMinutesWatched,averageViewDuration",
        dimensions="insightTrafficSourceType", sort="-views")
    data["traffic"] = _dicts(h, r)

    h, r = run_report(
        yta, start, end,
        metrics="views,averageViewPercentage",
        dimensions="country", sort="-views", max_results=top)
    data["geo"] = _dicts(h, r)

    h, r = run_report(
        yta, start, end,
        metrics="views",
        dimensions="insightTrafficSourceDetail",
        filters="insightTrafficSourceType==YT_SEARCH", sort="-views", max_results=top)
    data["search"] = _dicts(h, r)
    return data


def _upsert_csv(path, fieldnames, new_rows, measured_on):
    """같은 measured_on 행은 갈아끼우고 append (하루 재실행 idempotent)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = []
    if path.exists():
        with path.open(encoding="utf-8", newline="") as f:
            existing = [row for row in csv.DictReader(f)
                        if row.get("measured_on") != measured_on]
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore", restval="")
        w.writeheader()
        for row in existing + new_rows:
            w.writerow(row)


def load_prev_channel(measured_on):
    """오늘 이전 가장 최근 CHANNEL 스냅샷 (delta 계산용)."""
    path = ANALYTICS_DIR / "snapshots.csv"
    if not path.exists():
        return None
    prev = None
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row.get("scope") == "CHANNEL" and row.get("measured_on") != measured_on:
                if prev is None or row["measured_on"] > prev["measured_on"]:
                    prev = row
    return prev


def write_csvs(data, measured_on, window, start, end):
    ch = data["channel"]
    snap_rows = []
    if ch:
        snap_rows.append({
            "measured_on": measured_on, "window_days": window,
            "start_date": start, "end_date": end, "scope": "CHANNEL", "video_id": "",
            "views": ch.get("views", ""), "watch_minutes": ch.get("estimatedMinutesWatched", ""),
            "avg_view_sec": ch.get("averageViewDuration", ""),
            "avg_view_pct": ch.get("averageViewPercentage", ""),
            "likes": ch.get("likes", ""), "comments": ch.get("comments", ""),
            "subs_gained": ch.get("subscribersGained", ""), "shares": ch.get("shares", ""),
            "like_rate_pct": _pct(ch.get("likes"), ch.get("views")),
        })
    for v in data["videos"]:
        vid = v.get("video", "")
        snap_rows.append({
            "measured_on": measured_on, "window_days": window,
            "start_date": start, "end_date": end,
            "scope": VIDEOS.get(vid, vid), "video_id": vid,
            "views": v.get("views", ""), "watch_minutes": v.get("estimatedMinutesWatched", ""),
            "avg_view_sec": v.get("averageViewDuration", ""),
            "avg_view_pct": v.get("averageViewPercentage", ""),
            "likes": v.get("likes", ""), "comments": v.get("comments", ""),
            "subs_gained": v.get("subscribersGained", ""), "shares": "",
            "like_rate_pct": _pct(v.get("likes"), v.get("views")),
        })
    _upsert_csv(ANALYTICS_DIR / "snapshots.csv", SNAP_FIELDS, snap_rows, measured_on)

    total = sum(_num(t.get("views")) for t in data["traffic"]) or 1.0
    traffic_rows = [{
        "measured_on": measured_on, "window_days": window,
        "source_type": t.get("insightTrafficSourceType", ""),
        "source_label": TRAFFIC_LABELS.get(t.get("insightTrafficSourceType", ""),
                                           t.get("insightTrafficSourceType", "")),
        "views": t.get("views", ""), "watch_minutes": t.get("estimatedMinutesWatched", ""),
        "avg_view_sec": t.get("averageViewDuration", ""),
        "share_pct": round(_num(t.get("views")) / total * 100, 1),
    } for t in data["traffic"]]
    _upsert_csv(ANALYTICS_DIR / "traffic.csv", TRAFFIC_FIELDS, traffic_rows, measured_on)

    geo_rows = [{
        "measured_on": measured_on, "window_days": window,
        "country": g.get("country", ""),
        "country_label": COUNTRY_LABELS.get(g.get("country", ""), g.get("country", "")),
        "views": g.get("views", ""), "avg_view_pct": g.get("averageViewPercentage", ""),
    } for g in data["geo"]]
    _upsert_csv(ANALYTICS_DIR / "geo.csv", GEO_FIELDS, geo_rows, measured_on)

    search_rows = [{
        "measured_on": measured_on, "window_days": window,
        "query": s.get("insightTrafficSourceDetail", ""), "views": s.get("views", ""),
    } for s in data["search"]]
    _upsert_csv(ANALYTICS_DIR / "search.csv", SEARCH_FIELDS, search_rows, measured_on)


# studio_reach.csv 스키마 (Studio '도달범위' 탭 수동 측정 시계열 · API 밖).
# 코튼이 측정마다 행 추가 → report 실행 시 §7이 여기서 자동 렌더(휘발 방지).
STUDIO_REACH_FIELDS = [
    "measured_on", "window_days", "start_date", "end_date",
    "scope", "video_id", "impressions", "ctr_pct", "views", "thumbnail_era",
]


def load_studio_reach():
    """studio_reach.csv → (by_date, sorted_dates). 없거나 비면 None."""
    path = ANALYTICS_DIR / "studio_reach.csv"
    if not path.exists():
        return None
    with path.open(encoding="utf-8", newline="") as f:
        rows = [r for r in csv.DictReader(f) if r.get("measured_on")]
    if not rows:
        return None
    by_date = {}
    for r in rows:
        by_date.setdefault(r["measured_on"], []).append(r)
    return by_date, sorted(by_date)


def _reach_key(r):
    """비교용 안정 키 = video_id(영상) 또는 scope(채널). 표시명 변경에 강함."""
    return r.get("video_id") or r.get("scope") or ""


def render_studio_section(reach):
    """§7 — studio_reach.csv 기반 자동 렌더 (수동 칸 휘발 방지 + 측정 비교)."""
    L = ["## 7. Studio 노출·CTR (API 밖 · `studio_reach.csv` 자동 렌더)", ""]
    if not reach:
        L += [
            "> 노출수·노출 CTR은 Analytics API에 없음 → YouTube Studio **'도달범위'** 탭에서 측정.",
            "> `Analytics/studio_reach.csv`에 행을 추가하면 다음 `report` 실행 때 이 표·비교가 "
            "자동으로 채워진다 (휘발 없음).",
            "",
            "> CSV 양식: `" + ",".join(STUDIO_REACH_FIELDS) + "`",
            "> scope = `CHANNEL` 또는 영상 표시명 · thumbnail_era = 썸네일 버전 태그(예 `pre_v4`/`post_v4`).",
            "",
        ]
        return L

    by_date, dates = reach
    latest = dates[-1]
    rows = by_date[latest]
    ch = next((r for r in rows if r.get("scope") == "CHANNEL"), None)
    vids = sorted((r for r in rows if r.get("scope") != "CHANNEL"),
                  key=lambda r: _num(r.get("impressions")), reverse=True)
    meta = ch or (rows[0] if rows else {})

    L += [
        "> 노출수·노출 CTR은 Analytics API에 없음 → Studio **'도달범위'** 탭 측정 → "
        "`studio_reach.csv`(시계열 원본). **이 §7은 CSV에서 자동 렌더 = `report` 재실행해도 휘발 없음.**",
        f"> **최신 측정 {latest}** · 창 {meta.get('window_days','?')}일 "
        f"({meta.get('start_date','?')}~{meta.get('end_date','?')}) · 썸네일 era=`{meta.get('thumbnail_era','')}`.",
        "",
        "| 영상 | 노출수 | 노출 CTR | 조회수 | era |",
        "|---|--:|--:|--:|---|",
    ]
    for v in vids:
        L.append(f"| {v.get('scope','')} | {fmt_int(v.get('impressions'))} | {fmt_pct(v.get('ctr_pct'))} "
                 f"| {fmt_int(v.get('views'))} | {v.get('thumbnail_era','')} |")
    if ch:
        L.append(f"| **채널 합계** | **{fmt_int(ch.get('impressions'))}** | **{fmt_pct(ch.get('ctr_pct'))}** "
                 f"| **{fmt_int(ch.get('views'))}** | {ch.get('thumbnail_era','')} |")
    L.append("")

    # 판독 (데이터 도출 · 사실만 · 전략 서사는 §5에 둔다)
    if ch:
        imp, ctr = _num(ch.get("impressions")), _num(ch.get("ctr_pct"))
        clicks = round(imp * ctr / 100)
        L += [
            "**판독 (데이터 도출)**:",
            f"- 채널 {meta.get('window_days','?')}일 노출 **{fmt_int(imp)}** · CTR **{ctr}%** → "
            f"클릭 ≈ **{fmt_int(clicks)}**. 노출=도달(알고리즘) · CTR=썸네일·제목 클릭 전환.",
        ]
        if vids and ctr:
            top_imp = max(_num(v.get("impressions")) for v in vids) or 1.0
            for v in vids:
                vctr, vimp = _num(v.get("ctr_pct")), _num(v.get("impressions"))
                if vctr >= ctr * 1.5 and vimp <= top_imp * 0.3:
                    L.append(f"- **{v.get('scope','')}**: CTR {vctr}% (채널 {ctr}%의 {vctr/ctr:.1f}배)인데 "
                             f"노출 {fmt_int(vimp)}뿐 — 전환은 좋고 도달이 약함 (별개 = 알고리즘 노출 문제).")
        L.append("")

    # 측정 비교 (2회 이상 · pre/post era 효과 자동 표)
    if len(dates) >= 2:
        prev_date = dates[-2]
        prev_by_key = {_reach_key(r): r for r in by_date[prev_date]}
        comp = list(vids) + ([ch] if ch else [])
        L += [
            f"**측정 비교 ({prev_date} → {latest})**:",
            "",
            "| 영상 | era | 노출 Δ | CTR 변화 |",
            "|---|---|--:|---|",
        ]
        for v in comp:
            name = "**채널 합계**" if v.get("scope") == "CHANNEL" else v.get("scope", "")
            p = prev_by_key.get(_reach_key(v))
            if not p:
                L.append(f"| {name} | {v.get('thumbnail_era','')} | (이전 없음) | — |")
                continue
            era_chg = f"{p.get('thumbnail_era','')}→{v.get('thumbnail_era','')}"
            imp_d = _delta(v.get("impressions"), p.get("impressions"))
            ctr_chg = f"{fmt_pct(p.get('ctr_pct'))} → {fmt_pct(v.get('ctr_pct'))}"
            L.append(f"| {name} | {era_chg} | {imp_d} | {ctr_chg} |")
        L.append("")

    L.append("> ⚠️ §1·§2 조회수(Analytics API)는 2~3일 지연 → Studio(§7)가 더 신선 "
             "(갓 publish한 영상은 §7에만 잡히기도).")
    L.append("")
    return L


def render_markdown(data, measured_on, window, start, end, prev):
    ch = data["channel"]
    views = ch.get("views", "?")
    like_rate = _pct(ch.get("likes"), ch.get("views"))
    avg_pct = ch.get("averageViewPercentage", "?")
    subs = ch.get("subscribersGained", "?")

    total_tr = sum(_num(t.get("views")) for t in data["traffic"]) or 1.0
    tr_share = {t.get("insightTrafficSourceType"): _num(t.get("views")) / total_tr * 100
                for t in data["traffic"]}
    suggested = round(tr_share.get("RELATED_VIDEO", 0), 1)
    search_sh = round(tr_share.get("YT_SEARCH", 0), 1)
    jp = next((g for g in data["geo"] if g.get("country") == "JP"), None)
    jp_line = (f"있음 (조회 {jp.get('views')})" if jp else "없음")

    L = []
    L.append("# Atelier Miku Acappella — 채널 헬스 리포트")
    L.append("")
    L.append(f"> **측정일** {measured_on} · **기간** 최근 {window}일 ({start} ~ {end})")
    L.append("> 생성: `python Analytics/youtube_analytics.py report` · YouTube Analytics는 **2~3일 지연**")
    L.append("> ⚠️ 노출수·노출 CTR(썸네일 클릭률)은 API에 없음 → §7은 `studio_reach.csv`에서 자동 렌더 "
             "(Studio 도달범위 탭 측정 → CSV 행 추가)")
    L.append("")

    # 1. 한 줄 현황
    L.append("## 1. 한 줄 현황")
    if prev:
        dv = _delta(views, prev.get("views"))
        ds = _delta(subs, prev.get("subs_gained"))
        cmp_line = f"지난 측정({prev.get('measured_on')}) 대비 — 조회 {dv} · 구독 {ds}"
    else:
        cmp_line = "첫 측정 — 비교 대상 없음 (다음 주부터 증감 표시)"
    L.append(f"- **조회 {views}** · 좋아요율 {like_rate}% · 평균 시청률 {avg_pct}% · 구독 +{subs}")
    L.append(f"- {cmp_line}")
    L.append(f"- 유입 구조: **추천 영상 {suggested}%** 주력 · 검색 {search_sh}% · 일본 유입 **{jp_line}**")
    L.append("")

    # 2. 영상별 스냅샷
    L.append("## 2. 영상별 스냅샷")
    L.append("")
    L.append("| 영상 | 조회 | 좋아요율 | 평균시청 | 시청지속률 | 댓글 | 구독기여 |")
    L.append("|---|--:|--:|--:|--:|--:|--:|")
    for v in data["videos"]:
        name = VIDEOS.get(v.get("video", ""), v.get("video", ""))
        L.append(f"| {name} | {fmt_int(v.get('views'))} | {_pct(v.get('likes'), v.get('views'))}% "
                 f"| {int(_num(v.get('averageViewDuration')))}s "
                 f"| {v.get('averageViewPercentage')}% | {v.get('comments')} | {v.get('subscribersGained')} |")
    L.append("")

    # 3. 트래픽 진단
    L.append("## 3. 트래픽 진단")
    L.append("")
    L.append("| 소스 | 조회 | 비중 | 평균시청(초) |")
    L.append("|---|--:|--:|--:|")
    for t in data["traffic"]:
        code = t.get("insightTrafficSourceType", "")
        label = TRAFFIC_LABELS.get(code, code)
        share = round(_num(t.get("views")) / total_tr * 100, 1)
        L.append(f"| {label} | {fmt_int(t.get('views'))} | {share}% | {int(_num(t.get('averageViewDuration')))}s |")
    L.append("")
    L.append(f"- **추천 영상이 주력 ({suggested}%)** — 알고리즘 추천 노출에 의존하는 구조.")
    L.append(f"- 검색 유입 {search_sh}% — {'사실상 없음' if search_sh < 5 else '미약'}. 고의도 트래픽 키울 여지.")
    L.append(f"- 일본 유입: **{jp_line}** — 최대 미개척 표면 (初音ミク·アカペラ 검색).")
    L.append("")

    # 4. 전환 지표
    L.append("## 4. 전환 지표 (진성팬 레버)")
    L.append("")
    play_views = next((t.get("views") for t in data["traffic"]
                       if t.get("insightTrafficSourceType") == "PLAYLIST"), 0)
    L.append(f"- 구독 **+{subs}** · 좋아요율 **{like_rate}%** (YouTube 평균 2~4% 대비 높음 = fit 강함)")
    L.append(f"- 댓글 {ch.get('comments')} · 공유 {ch.get('shares')} · 재생목록 유입 {play_views}")
    L.append("- 해석: 도달은 작아도 *반응 밀도*는 높다 → 레버는 **구독·재생목록·고정댓글** 전환.")
    L.append("")

    # 5. 전략 피드백 (s340 결론 keep)
    L.append("## 5. 전략 피드백")
    L.append("")
    L.append("- **쫓지 말 것 = 평균 retention.** 구조적임 (니치 취향 × 호기심 트래픽 깔때기). 결함 아님.")
    L.append("- **레버 두 개**: (1) 고의도 트래픽 더 키우기 (SEO·다국어·보카로 팬덤 타깃) "
             "(2) 들어온 사람 진성팬 전환 (구독·재생목록·고정댓글).")
    L.append("- **일본이 최대 미개척** — 미쿠 표기로 자연 필터, JP 검색 표면 확보가 가장 큰 레버.")
    L.append("- 사티 도입부 등 정체성 요소는 retention 수치보다 우선 (코튼 결단 · s340).")
    L.append("")

    # 6. 다음 1주 액션
    L.append("## 6. 다음 1주 액션")
    L.append("")
    L.append("- [ ] (측정) 다음 주 같은 요일 `report` 재실행 → 증감 추적")
    L.append("- [ ] (전환) 각 영상 고정 댓글 + 구독 CTA + 재생목록 정합 점검")
    L.append("- [ ] (트래픽) 일본어 검색 표면 — 제목·태그 初音ミク·アカペラ 키워드 확인")
    L.append("- [ ] (Studio) 도달범위 탭 측정 → `studio_reach.csv`에 새 측정 행 추가 (다음 `report`에서 §7·비교 자동 갱신)")
    L.append("")

    # 7. Studio 노출·CTR (studio_reach.csv 자동 렌더 · 휘발 방지)
    L.extend(render_studio_section(load_studio_reach()))
    L.append("---")
    L.append(f"_재측정: `python Analytics/youtube_analytics.py report` · "
             f"시계열 CSV: `Analytics/snapshots.csv` · Studio 노출: `Analytics/studio_reach.csv` · "
             f"Excel: `Analytics/channel_analysis.xlsx`_")
    L.append("")

    path = ANALYTICS_DIR / "channel_health_report.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(L), encoding="utf-8")
    return path


def report(yta, start, end, window, top=25):
    measured_on = dt.date.today().isoformat()
    print(f"\n[report] 스냅샷 수집 중 … 기간 {start} ~ {end}")
    data = collect_snapshot(yta, start, end, top=top)
    prev = load_prev_channel(measured_on)
    write_csvs(data, measured_on, window, start, end)
    md = render_markdown(data, measured_on, window, start, end, prev)
    print(f"  CSV:      {(ANALYTICS_DIR / 'snapshots.csv')}")
    print(f"            (+ traffic.csv · geo.csv · search.csv)")
    print(f"  리포트:   {md}")
    # Excel은 있으면 같이 (openpyxl 미설치/실패해도 report 자체는 성공).
    try:
        import analytics_xlsx
        xlsx = analytics_xlsx.build(ANALYTICS_DIR)
        print(f"  Excel:    {xlsx}")
    except Exception as e:  # noqa: BLE001
        print(f"  (Excel 생성 건너뜀: {e})")
    print()


# ----------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Project Muse YouTube Analytics 분석 도구")
    ap.add_argument("command",
                    choices=["all", "traffic", "search", "geo", "retention",
                             "retention-curve", "report"])
    ap.add_argument("--days", type=int, default=28)
    ap.add_argument("--start")
    ap.add_argument("--end")
    ap.add_argument("--video", help="특정 영상 ID만")
    ap.add_argument("--top", type=int, default=25)
    args = ap.parse_args()

    start, end = daterange(args)
    vfilter = f"video=={args.video}" if args.video else None

    creds = get_credentials()
    yta = build("youtubeAnalytics", "v2", credentials=creds)

    cmd = args.command
    if cmd == "report":
        report(yta, start, end, args.days, args.top)
        return

    scope = f"video {args.video}" if args.video else "채널 전체"
    print(f"\n[Atelier Miku Acappella] 기간 {start} ~ {end} · {scope}")

    if cmd in ("all", "traffic"):
        report_traffic(yta, start, end, vfilter)
    if cmd in ("all", "search"):
        report_search(yta, start, end, vfilter, args.top)
    if cmd in ("all", "geo"):
        report_geo(yta, start, end, vfilter, args.top)
    if cmd in ("all", "retention"):
        report_retention(yta, start, end, vfilter)
    if cmd == "retention-curve":
        targets = [args.video] if args.video else list(VIDEOS.keys())
        for vid in targets:
            report_retention_curve(yta, start, end, vid, VIDEOS.get(vid, vid))
    print()


if __name__ == "__main__":
    main()
