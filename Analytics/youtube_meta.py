# -*- coding: utf-8 -*-
"""YouTube 메타데이터 쓰기 도구 (Atelier Miku Acappella).

youtube_analytics.py 는 읽기 전용(analytics). 본 도구는 **쓰기**(force-ssl) 전용으로 분리:
- 제목 / 설명 / 현지화(localizations) 수정  → videos.update
- 커스텀 썸네일 업로드                       → thumbnails.set

토큰도 분리: analytics 읽기 토큰(.youtube_oauth_token.json)은 그대로 두고
쓰기 토큰(.youtube_write_token.json)을 별도 보관 = 최소 권한.

핵심 안전장치 — set-title 은 **read-modify-write**:
  현재 video 리소스를 읽어 제목(기본 + 지정 로케일)만 바꾸고
  나머지(설명·태그·카테고리·다른 로케일·defaultLanguage)는 그대로 다시 씀. 클로버 0.

사용 (Analytics/ 또는 Project_Muse/ 어디서 실행해도 BASE 동일):
  python Analytics/youtube_meta.py auth                       # 1회 OAuth (브라우저 동의)
  python Analytics/youtube_meta.py get <video_id>            # 현재 제목/현지화 확인
  python Analytics/youtube_meta.py set-title <video_id> --default "..." --en "..." --ko "..." --ja "..."
  python Analytics/youtube_meta.py set-tags <video_id> "tag1, tag2, ..."   # 백엔드 태그 칸 (--dry-run 권장)
  python Analytics/youtube_meta.py set-thumbnail <video_id> <image.png>
"""
import sys
import argparse
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError
except ImportError:
    sys.exit(
        "의존성 미설치. 먼저 실행:\n"
        "  python -m pip install --user google-api-python-client google-auth-oauthlib google-auth-httplib2"
    )

BASE = Path(__file__).resolve().parent.parent          # Project_Muse/
CLIENT_SECRET = BASE / "client_secret.json"            # analytics와 공용 OAuth 클라이언트
TOKEN_FILE = BASE / ".youtube_write_token.json"        # 쓰기 전용 토큰 (analytics와 분리)
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]  # videos.update + thumbnails.set


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
                    "GCP OAuth 데스크톱 클라이언트 JSON 을 위 경로에 두기 (Analytics/README.md)."
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
            print("브라우저가 열립니다. 채널 소유 Google 계정으로 로그인 후 '허용'.")
            print("('앱이 확인되지 않음' 경고가 뜨면 → 고급 → 계속/이동 → 허용.)")
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
        print(f"쓰기 토큰 캐시됨: {TOKEN_FILE.name}")
    return creds


def yt():
    return build("youtube", "v3", credentials=get_credentials())


def cmd_auth(args):
    svc = yt()
    me = svc.channels().list(part="snippet", mine=True).execute()
    items = me.get("items", [])
    if not items:
        sys.exit("인증은 됐으나 소유 채널을 못 찾음. 채널 소유 계정으로 로그인했는지 확인.")
    title = items[0]["snippet"]["title"]
    print(f"✓ 쓰기 권한 셋업 완료. 인증된 채널: {title}")
    print(f"  scope: {SCOPES[0]}")
    print("  이제 set-title / set-thumbnail 을 API로 직접 적용할 수 있어요.")


def _get_video(svc, vid):
    resp = svc.videos().list(part="snippet,localizations,status", id=vid).execute()
    items = resp.get("items", [])
    if not items:
        sys.exit(f"video 못 찾음 (비공개/예약이면 API key가 아닌 소유자 토큰 필요 — 본 토큰은 소유자라 OK): {vid}")
    return items[0]


def cmd_get(args):
    v = _get_video(yt(), args.video)
    sn = v["snippet"]
    print(f"=== {args.video} ===")
    print(f"defaultLanguage = {sn.get('defaultLanguage')}")
    print(f"[default title] {sn.get('title')}")
    for lang, loc in (v.get("localizations") or {}).items():
        print(f"  [{lang}] {loc.get('title')}")


def cmd_set_title(args):
    provided = {k: v for k, v in (("en", args.en), ("ko", args.ko), ("ja", args.ja)) if v}
    if not provided and not args.default:
        sys.exit("바꿀 제목을 하나 이상 지정 (--default / --en / --ko / --ja).")

    svc = yt()
    v = _get_video(svc, args.video)
    old = v["snippet"]
    locs = dict(v.get("localizations") or {})

    # read-modify-write: 쓰기 가능한 snippet 필드만 보존해서 재구성 (read-only 필드 제외).
    new_snippet = {
        "title": args.default if args.default else old.get("title"),
        "categoryId": old.get("categoryId"),
        "description": old.get("description", ""),
    }
    if old.get("tags"):
        new_snippet["tags"] = old["tags"]
    if old.get("defaultLanguage"):
        new_snippet["defaultLanguage"] = old["defaultLanguage"]
    if old.get("defaultAudioLanguage"):
        new_snippet["defaultAudioLanguage"] = old["defaultAudioLanguage"]

    # defaultLanguage 로케일은 기본 제목과 일치시킴 (보통 en).
    default_lang = old.get("defaultLanguage")
    if args.default and default_lang and default_lang not in provided:
        provided[default_lang] = args.default

    for lang, title in provided.items():
        entry = dict(locs.get(lang, {}))
        entry["title"] = title
        if "description" not in entry:
            entry["description"] = ""  # localizations 항목엔 description 필수
        locs[lang] = entry

    body = {"id": args.video, "snippet": new_snippet}
    part = "snippet"
    if locs:
        body["localizations"] = locs
        part = "snippet,localizations"

    if args.dry_run:
        print("[dry-run] 적용될 값:")
        print(f"  [default] {new_snippet['title']}")
        for lang, title in provided.items():
            print(f"  [{lang}] {title}")
        print("  (나머지 snippet/localizations 필드는 현재값 보존)")
        return

    try:
        svc.videos().update(part=part, body=body).execute()
    except HttpError as e:
        sys.exit(f"update 실패: {e}")
    print(f"✓ 제목 적용 완료: {args.video}")
    cmd_get(argparse.Namespace(video=args.video))


def cmd_set_tags(args):
    if args.from_file:
        raw = Path(args.from_file).read_text(encoding="utf-8")
    else:
        raw = args.tags or ""
    tags = [t.strip() for t in raw.replace("\n", ",").split(",") if t.strip()]
    if not tags:
        sys.exit("태그가 비어있음 (콤마 구분 문자열 또는 --from-file 지정).")

    # YouTube 태그 칸 = 전 태그 합산 ~500자 한도 (콤마 포함 근사). 초과 시 API가 거부.
    approx = sum(len(t) for t in tags) + (len(tags) - 1) * 2
    if approx > 500:
        sys.exit(f"태그 총 길이 ~{approx}자 > 500 한도. 줄이세요.")

    svc = yt()
    v = _get_video(svc, args.video)
    old = v["snippet"]

    # read-modify-write: snippet 의 tags 만 교체, 나머지(제목·설명·카테고리·언어)는 보존.
    # part="snippet" 만 보내므로 localizations 파트는 건드리지 않음 = 현지화 제목/설명 보존.
    new_snippet = {
        "title": old.get("title"),
        "categoryId": old.get("categoryId"),
        "description": old.get("description", ""),
        "tags": tags,
    }
    if old.get("defaultLanguage"):
        new_snippet["defaultLanguage"] = old["defaultLanguage"]
    if old.get("defaultAudioLanguage"):
        new_snippet["defaultAudioLanguage"] = old["defaultAudioLanguage"]

    if args.dry_run:
        old_tags = old.get("tags") or []
        print(f"[dry-run] {args.video}")
        print(f"  현재 태그 {len(old_tags)}개 → 새 태그 {len(tags)}개 (~{approx}/500자)")
        print("  새 태그: " + ", ".join(tags))
        print("  (제목·설명·현지화 등 나머지 snippet/localizations 보존)")
        return

    try:
        svc.videos().update(part="snippet", body={"id": args.video, "snippet": new_snippet}).execute()
    except HttpError as e:
        sys.exit(f"update 실패: {e}")
    print(f"✓ 태그 적용 완료: {args.video} ({len(tags)}개 · ~{approx}/500자)")


def cmd_set_thumbnail(args):
    img = Path(args.image)
    if not img.exists():
        sys.exit(f"이미지 없음: {img}")
    svc = yt()
    try:
        svc.thumbnails().set(
            videoId=args.video,
            media_body=MediaFileUpload(str(img)),
        ).execute()
    except HttpError as e:
        sys.exit(f"thumbnail 업로드 실패: {e}")
    print(f"✓ 썸네일 업로드 완료: {args.video} ← {img.name}")


def main():
    p = argparse.ArgumentParser(description="YouTube 메타데이터 쓰기 (Atelier Miku Acappella)")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("auth", help="1회 OAuth 셋업 (브라우저 동의)")

    g = sub.add_parser("get", help="현재 제목/현지화 확인")
    g.add_argument("video")

    s = sub.add_parser("set-title", help="제목 read-modify-write")
    s.add_argument("video")
    s.add_argument("--default", help="기본(default) 제목")
    s.add_argument("--en")
    s.add_argument("--ko")
    s.add_argument("--ja")
    s.add_argument("--dry-run", action="store_true", help="적용 없이 미리보기")

    st = sub.add_parser("set-tags", help="백엔드 태그 칸 read-modify-write (전 로케일 공유)")
    st.add_argument("video")
    st.add_argument("tags", nargs="?", help="콤마 구분 태그 문자열")
    st.add_argument("--from-file", help="태그 문자열을 파일에서 읽기 (콤마/줄바꿈 구분)")
    st.add_argument("--dry-run", action="store_true", help="적용 없이 미리보기")

    t = sub.add_parser("set-thumbnail", help="커스텀 썸네일 업로드")
    t.add_argument("video")
    t.add_argument("image")

    args = p.parse_args()
    {
        "auth": cmd_auth,
        "get": cmd_get,
        "set-title": cmd_set_title,
        "set-tags": cmd_set_tags,
        "set-thumbnail": cmd_set_thumbnail,
    }[args.cmd](args)


if __name__ == "__main__":
    main()
