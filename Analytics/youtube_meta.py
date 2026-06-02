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
  python Analytics/youtube_meta.py set-description <video_id> \
      [--default-file ...] [--en-file ...] [--ja-file ...] [--ko-file ...] [--dry-run]   # 설명 본문 통째 적용
  python Analytics/youtube_meta.py set-thumbnail <video_id> <image.png>
  python Analytics/youtube_meta.py update-description-line <vid> [vid...] \
      --en-find "X" --en-replace "Y" [--ja-find ... --ja-replace ... --ko-find ... --ko-replace ...] [--dry-run]
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
    from google.auth.exceptions import RefreshError
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
            try:
                creds.refresh(Request())
            except RefreshError:
                print("기존 토큰 만료/취소됨 → 캐시 폐기 후 새 브라우저 인증으로 진행.")
                creds = None
        if not creds or not creds.valid:
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
    if getattr(args, "description", False):
        print(f"\n[default description]\n{sn.get('description', '')}")
        for lang, loc in (v.get("localizations") or {}).items():
            print(f"\n[{lang} description]\n{loc.get('description', '')}")


def cmd_set_title(args):
    provided = {k: v for k, v in (("en", args.en), ("ko", args.ko), ("ja", args.ja)) if v}
    for lang, title in (getattr(args, "loc", None) or []):
        provided[lang] = title
    if not provided and not args.default and not args.default_language:
        sys.exit("바꿀 자료를 하나 이상 지정 (--default / --en / --ko / --ja / --default-language).")

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
    if args.default_language:
        new_snippet["defaultLanguage"] = args.default_language
    elif old.get("defaultLanguage"):
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


def _update_description_line_one(svc, vid, pairs, dry_run):
    """단일 영상에 per-locale find/replace 적용 (read-modify-write · description 외 필드 보존).

    pairs = {'en': (find, replace), 'ja': (find, replace), 'ko': (find, replace), ...}
    'en' 키는 defaultLanguage 로케일과 매칭되면 snippet.description (default) 에도 적용.
    각 로케일은 첫 번째 occurrence만 교체(replace count=1) · find 못 찾으면 skip + warn.
    """
    v = _get_video(svc, vid)
    old = v["snippet"]
    locs = dict(v.get("localizations") or {})
    default_lang = old.get("defaultLanguage")
    if not default_lang:
        default_lang = "en"
        print(f"  [{vid}] defaultLanguage 미설정 → 'en' fallback 박힘 (localizations update 의무 필드)")

    desc = old.get("description", "")
    changes = []  # (label, before, after) tuples for logging

    # default = snippet.description (matched by defaultLanguage)
    if default_lang in pairs:
        find, replace = pairs[default_lang]
        if find in desc:
            desc = desc.replace(find, replace, 1)
            changes.append((f"default[{default_lang}]", find, replace))
        else:
            print(f"  [{vid}/default-{default_lang}] '{find}' 못 찾음 · skip")

    # localizations
    new_locs = dict(locs)
    for lang, (find, replace) in pairs.items():
        if lang not in locs:
            print(f"  [{vid}/{lang}] localization 부재 · skip")
            continue
        entry = dict(locs[lang])
        ldesc = entry.get("description", "")
        if find in ldesc:
            entry["description"] = ldesc.replace(find, replace, 1)
            new_locs[lang] = entry
            changes.append((lang, find, replace))
        else:
            print(f"  [{vid}/{lang}] '{find}' 못 찾음 · skip")

    if not changes:
        print(f"✗ {vid}: 교체 자료 없음 (find 자료 부재)")
        return

    # snippet 재구성: 쓰기 가능한 필드만 보존 (read-only 필드 제외).
    new_snippet = {
        "title": old.get("title"),
        "categoryId": old.get("categoryId"),
        "description": desc,
    }
    if old.get("tags"):
        new_snippet["tags"] = old["tags"]
    if default_lang:
        new_snippet["defaultLanguage"] = default_lang
    if old.get("defaultAudioLanguage"):
        new_snippet["defaultAudioLanguage"] = old["defaultAudioLanguage"]

    if dry_run:
        print(f"[dry-run] {vid}: {len(changes)} 자리 교체 예정")
        for label, before, after in changes:
            print(f"  [{label}] {before!r} → {after!r}")
        return

    try:
        svc.videos().update(
            part="snippet,localizations",
            body={"id": vid, "snippet": new_snippet, "localizations": new_locs},
        ).execute()
    except HttpError as e:
        sys.exit(f"update 실패 ({vid}): {e}")
    print(f"✓ {vid}: {len(changes)} 자리 교체 적용")
    for label, before, after in changes:
        print(f"  [{label}] {before!r} → {after!r}")


def cmd_update_description_line(args):
    pairs = {}
    for lang, find, replace in (
        ("en", args.en_find, args.en_replace),
        ("ja", args.ja_find, args.ja_replace),
        ("ko", args.ko_find, args.ko_replace),
    ):
        if find and replace:
            pairs[lang] = (find, replace)
        elif find or replace:
            sys.exit(f"--{lang}-find와 --{lang}-replace는 함께 지정해야 함.")
    if not pairs:
        sys.exit("교체 자료 지정 X (--en-find/--en-replace · --ja-find/--ja-replace · --ko-find/--ko-replace 중 1쌍 이상).")

    svc = yt()
    for vid in args.videos:
        _update_description_line_one(svc, vid, pairs, dry_run=args.dry_run)


def cmd_set_description(args):
    """설명 본문 통째 적용 (read-modify-write · 제목/태그/카테고리/언어 보존).

    --default-file = snippet.description (보통 defaultLanguage=en 본문).
    --en-file / --ja-file / --ko-file = localizations[lang].description (해당 로케일 제목은 보존).
    defaultLanguage 로케일(보통 en)은 --default-file 과 --en-file 를 동시에 줘서 둘을 일치시킴.
    한 로케일이라도 localizations 항목이 없으면 새로 만들되 title 은 빈 문자열 placeholder.
    """
    def _read(path):
        return Path(path).read_text(encoding="utf-8").strip("\n") if path else None

    desc_default = _read(args.default_file)
    desc_locale = {
        lang: _read(p)
        for lang, p in (("en", args.en_file), ("ja", args.ja_file), ("ko", args.ko_file))
        if p
    }
    for lang, p in (getattr(args, "loc_file", None) or []):
        desc_locale[lang] = _read(p)
    if desc_default is None and not desc_locale:
        sys.exit("적용할 설명 지정 X (--default-file / --en-file / --ja-file / --ko-file 중 1개 이상).")

    svc = yt()
    v = _get_video(svc, args.video)
    old = v["snippet"]
    locs = dict(v.get("localizations") or {})
    default_lang = old.get("defaultLanguage")

    # read-modify-write: 쓰기 가능한 snippet 필드만 보존, description 만 교체(있으면).
    new_snippet = {
        "title": old.get("title"),
        "categoryId": old.get("categoryId"),
        "description": desc_default if desc_default is not None else old.get("description", ""),
    }
    if old.get("tags"):
        new_snippet["tags"] = old["tags"]
    if default_lang:
        new_snippet["defaultLanguage"] = default_lang
    if old.get("defaultAudioLanguage"):
        new_snippet["defaultAudioLanguage"] = old["defaultAudioLanguage"]

    for lang, text in desc_locale.items():
        entry = dict(locs.get(lang, {}))
        entry["description"] = text
        if "title" not in entry:
            entry["title"] = ""  # localizations 항목엔 title 필수
        locs[lang] = entry

    if args.dry_run:
        print(f"[dry-run] {args.video} 적용 예정:")
        if desc_default is not None:
            print(f"  [default] {len(desc_default)}자 · 첫줄 {desc_default.splitlines()[0]!r}")
        for lang, text in desc_locale.items():
            print(f"  [{lang}] {len(text)}자 · 첫줄 {text.splitlines()[0]!r}")
        print("  (제목·태그·카테고리·언어·다른 로케일 보존)")
        return

    body = {"id": args.video, "snippet": new_snippet, "localizations": locs}
    try:
        svc.videos().update(part="snippet,localizations", body=body).execute()
    except HttpError as e:
        sys.exit(f"update 실패: {e}")
    applied = (["default"] if desc_default is not None else []) + list(desc_locale.keys())
    print(f"✓ 설명 적용 완료: {args.video} ({', '.join(applied)})")


def _get_channel(svc):
    resp = svc.channels().list(part="snippet,brandingSettings,localizations", mine=True).execute()
    items = resp.get("items", [])
    if not items:
        sys.exit("소유 채널을 못 찾음. 채널 소유 계정 토큰인지 확인.")
    return items[0]


def cmd_get_channel(args):
    ch = _get_channel(yt())
    sn = ch["snippet"]
    branding = ch.get("brandingSettings", {}).get("channel", {})
    print(f"=== channel {ch['id']} ===")
    print(f"title = {sn.get('title')}")
    print(f"defaultLanguage = {branding.get('defaultLanguage')}")
    print(f"\n[default description]\n{branding.get('description', '')}")
    for lang, loc in (ch.get("localizations") or {}).items():
        print(f"\n[{lang}] title={loc.get('title')!r}\n{loc.get('description', '')}")


def cmd_set_channel(args):
    """채널 현지화 (channels.update · localizations part).

    채널명(title)은 브랜드 고정 → 전 로케일 동일 title 박고 description 만 현지화.
    localizations[lang] = {title, description} (둘 다 필수). title 미지정 시 현재 채널명 사용.
    localizations 가 display 되려면 채널 defaultLanguage 가 설정돼 있어야 함 (--default-language 로 박기 가능).
    """
    svc = yt()
    ch = _get_channel(svc)
    cid = ch["id"]
    brand_title = ch["snippet"].get("title")
    branding = ch.get("brandingSettings", {})
    locs = dict(ch.get("localizations") or {})

    for lang, path in (args.loc_file or []):
        text = Path(path).read_text(encoding="utf-8").strip("\n")
        entry = dict(locs.get(lang, {}))
        entry["description"] = text
        entry["title"] = args.title or entry.get("title") or brand_title  # 브랜드명 고정
        locs[lang] = entry

    if not locs:
        sys.exit("적용할 로케일 description 지정 X (--loc-file LANG PATH 반복).")

    body = {"id": cid, "localizations": locs}
    part = "localizations"
    cur_default = branding.get("channel", {}).get("defaultLanguage")
    if args.default_language and args.default_language != cur_default:
        branding.setdefault("channel", {})["defaultLanguage"] = args.default_language
        body["brandingSettings"] = branding
        part = "brandingSettings,localizations"

    if args.dry_run:
        print(f"[dry-run] channel {cid} 적용 예정 (title 브랜드 고정 = {brand_title!r}):")
        if "brandingSettings" in body:
            print(f"  defaultLanguage → {args.default_language}")
        for lang, path in (args.loc_file or []):
            print(f"  [{lang}] ← {path}")
        return

    try:
        svc.channels().update(part=part, body=body).execute()
    except HttpError as e:
        sys.exit(f"channel update 실패: {e}")
    print(f"✓ 채널 현지화 적용: {cid} ({', '.join(l for l, _ in (args.loc_file or []))})")


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
    g.add_argument("--description", action="store_true", help="설명 본문도 출력 (default + 로케일별)")

    s = sub.add_parser("set-title", help="제목 read-modify-write")
    s.add_argument("video")
    s.add_argument("--default", help="기본(default) 제목")
    s.add_argument("--en")
    s.add_argument("--ko")
    s.add_argument("--ja")
    s.add_argument("--loc", nargs=2, action="append", metavar=("LANG", "TITLE"),
                   help="임의 로케일 제목 (반복 가능): --loc es '...' --loc ru '...' --loc zh-Hant '...'")
    s.add_argument("--default-language", help="snippet.defaultLanguage 박기 (e.g. en) · 제목 안 바꾸고 언어만 set 가능")
    s.add_argument("--dry-run", action="store_true", help="적용 없이 미리보기")

    st = sub.add_parser("set-tags", help="백엔드 태그 칸 read-modify-write (전 로케일 공유)")
    st.add_argument("video")
    st.add_argument("tags", nargs="?", help="콤마 구분 태그 문자열")
    st.add_argument("--from-file", help="태그 문자열을 파일에서 읽기 (콤마/줄바꿈 구분)")
    st.add_argument("--dry-run", action="store_true", help="적용 없이 미리보기")

    sd = sub.add_parser("set-description", help="설명 본문 통째 적용 (per-locale · read-modify-write)")
    sd.add_argument("video")
    sd.add_argument("--default-file", help="snippet.description 본문 파일 (보통 EN)")
    sd.add_argument("--en-file", help="localizations.en.description 본문 파일")
    sd.add_argument("--ja-file", help="localizations.ja.description 본문 파일")
    sd.add_argument("--ko-file", help="localizations.ko.description 본문 파일")
    sd.add_argument("--loc-file", nargs=2, action="append", metavar=("LANG", "PATH"),
                    help="임의 로케일 설명 파일 (반복 가능): --loc-file es path --loc-file zh-Hant path")
    sd.add_argument("--dry-run", action="store_true", help="적용 없이 미리보기")

    gc = sub.add_parser("get-channel", help="채널 제목/설명/현지화 + defaultLanguage 확인")
    gc.set_defaults(_unused=None)

    sc = sub.add_parser("set-channel", help="채널 현지화 (description 만 · title 브랜드 고정)")
    sc.add_argument("--loc-file", nargs=2, action="append", metavar=("LANG", "PATH"),
                    help="로케일 채널설명 파일 (반복): --loc-file es path · en 포함 가능")
    sc.add_argument("--title", help="현지화 title 강제 지정 (기본 = 현재 채널명 = 브랜드 고정)")
    sc.add_argument("--default-language", help="채널 defaultLanguage 박기 (localizations 표시 전제조건)")
    sc.add_argument("--dry-run", action="store_true", help="적용 없이 미리보기")

    t = sub.add_parser("set-thumbnail", help="커스텀 썸네일 업로드")
    t.add_argument("video")
    t.add_argument("image")

    u = sub.add_parser(
        "update-description-line",
        help="설명 1줄 surgical find/replace (per-locale · drift safe · anchor footer 변경 cycle 자리)",
    )
    u.add_argument("videos", nargs="+", help="비디오 ID (여러 개 가능)")
    u.add_argument("--en-find", help="EN(=defaultLanguage)에서 찾을 문자열 · snippet.description + localizations.en 양쪽 적용")
    u.add_argument("--en-replace", help="EN 교체 문자열")
    u.add_argument("--ja-find", help="localizations.ja 에서 찾을 문자열")
    u.add_argument("--ja-replace", help="JA 교체 문자열")
    u.add_argument("--ko-find", help="localizations.ko 에서 찾을 문자열")
    u.add_argument("--ko-replace", help="KO 교체 문자열")
    u.add_argument("--dry-run", action="store_true", help="적용 없이 미리보기")

    args = p.parse_args()
    {
        "auth": cmd_auth,
        "get": cmd_get,
        "set-title": cmd_set_title,
        "set-tags": cmd_set_tags,
        "set-description": cmd_set_description,
        "get-channel": cmd_get_channel,
        "set-channel": cmd_set_channel,
        "set-thumbnail": cmd_set_thumbnail,
        "update-description-line": cmd_update_description_line,
    }[args.cmd](args)


if __name__ == "__main__":
    main()
