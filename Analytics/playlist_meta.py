# -*- coding: utf-8 -*-
"""YouTube 재생목록 메타데이터 쓰기 (Atelier Miku Acappella).

youtube_meta.py family · 같은 OAuth scope(youtube.force-ssl) · 토큰 재사용.

핵심 안전장치 — set-desc 는 **read-modify-write**:
  현재 playlist 리소스를 읽어 설명(기본 + 지정 로케일)만 바꾸고
  나머지(제목·privacy·다른 로케일 등)는 그대로 다시 씀. 클로버 0.

사용:
  python Analytics/playlist_meta.py list                           # 채널 재생목록 목록
  python Analytics/playlist_meta.py get <playlist_id>             # 현재 제목/설명/현지화 확인
  python Analytics/playlist_meta.py set-desc <playlist_id> --default "..." --en "..." --ko "..." --ja "..." [--dry-run]
"""
import sys
import argparse
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Reuse OAuth + service from youtube_meta.py (same scope · 같은 토큰).
sys.path.insert(0, str(Path(__file__).resolve().parent))
from youtube_meta import yt  # noqa: E402
from googleapiclient.errors import HttpError  # noqa: E402


def _get_playlist(svc, pid):
    resp = svc.playlists().list(part="snippet,localizations,status", id=pid).execute()
    items = resp.get("items", [])
    if not items:
        sys.exit(f"playlist 못 찾음: {pid}")
    return items[0]


def cmd_list(args):
    svc = yt()
    me = svc.channels().list(part="snippet", mine=True).execute()
    ch_id = me["items"][0]["id"]
    resp = svc.playlists().list(part="snippet,contentDetails", channelId=ch_id, maxResults=50).execute()
    print(f"=== {me['items'][0]['snippet']['title']} ===")
    for p in resp.get("items", []):
        sn = p["snippet"]
        cnt = p["contentDetails"]["itemCount"]
        desc_len = len(sn.get("description", ""))
        print(f"  {p['id']}  ({cnt:>2}곡 · desc {desc_len:>3}c)  {sn['title']}")


def cmd_get(args):
    p = _get_playlist(yt(), args.playlist)
    sn = p["snippet"]
    print(f"=== {args.playlist} ===")
    print(f"title: {sn.get('title')}")
    print(f"defaultLanguage = {sn.get('defaultLanguage')}")
    desc = sn.get("description", "") or "(empty)"
    print(f"[default desc]")
    for line in desc.split("\n"):
        print(f"  {line}")
    for lang, loc in (p.get("localizations") or {}).items():
        print(f"[{lang}] title: {loc.get('title')}")
        ldesc = loc.get("description", "") or "(empty)"
        for line in ldesc.split("\n"):
            print(f"  {line}")


def cmd_set_desc(args):
    provided = {k: v for k, v in (("en", args.en), ("ko", args.ko), ("ja", args.ja)) if v}
    if not provided and args.default is None:
        sys.exit("바꿀 설명을 하나 이상 지정 (--default / --en / --ko / --ja).")

    svc = yt()
    pl = _get_playlist(svc, args.playlist)
    old = pl["snippet"]
    locs = dict(pl.get("localizations") or {})

    # read-modify-write: title 보존 + description 만 교체.
    new_snippet = {
        "title": old.get("title"),  # title 필수
        "description": args.default if args.default is not None else old.get("description", ""),
    }
    # defaultLanguage 우선순위: CLI > 기존 라이브 값. localizations 업데이트엔 필수 (Google API).
    default_lang = args.default_language or old.get("defaultLanguage")
    if default_lang:
        new_snippet["defaultLanguage"] = default_lang
    if old.get("tags"):
        new_snippet["tags"] = old["tags"]

    # defaultLanguage 로케일은 default 설명과 일치시킴 (보통 en).
    if args.default is not None and default_lang and default_lang not in provided:
        provided[default_lang] = args.default

    for lang, desc in provided.items():
        entry = dict(locs.get(lang, {}))
        entry["description"] = desc
        if "title" not in entry:
            entry["title"] = old.get("title", "")  # localizations 항목엔 title 필수
        locs[lang] = entry

    body = {"id": args.playlist, "snippet": new_snippet}
    part = "snippet"
    if locs:
        body["localizations"] = locs
        part = "snippet,localizations"

    if args.dry_run:
        print("[dry-run] 적용될 값:")
        print(f"  title (보존): {new_snippet['title']}")
        print(f"  [default desc]")
        for line in new_snippet["description"].split("\n"):
            print(f"    {line}")
        for lang, desc in provided.items():
            print(f"  [{lang} desc]")
            for line in desc.split("\n"):
                print(f"    {line}")
        print("  (title 및 나머지 snippet 필드는 현재값 보존)")
        return

    try:
        svc.playlists().update(part=part, body=body).execute()
    except HttpError as e:
        sys.exit(f"update 실패: {e}")
    print(f"✓ 설명 적용 완료: {args.playlist}")
    cmd_get(argparse.Namespace(playlist=args.playlist))


def main():
    p = argparse.ArgumentParser(description="YouTube 재생목록 메타데이터 쓰기 (Atelier Miku Acappella)")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="채널 재생목록 목록")

    g = sub.add_parser("get", help="현재 제목/설명/현지화 확인")
    g.add_argument("playlist")

    s = sub.add_parser("set-desc", help="설명 read-modify-write")
    s.add_argument("playlist")
    s.add_argument("--default", help="기본(default) 설명")
    s.add_argument("--en")
    s.add_argument("--ko")
    s.add_argument("--ja")
    s.add_argument("--default-language", help="snippet.defaultLanguage 설정 (localizations 업데이트엔 필수 · 기존 설정 시 생략)")
    s.add_argument("--dry-run", action="store_true", help="적용 없이 미리보기")

    args = p.parse_args()
    {
        "list": cmd_list,
        "get": cmd_get,
        "set-desc": cmd_set_desc,
    }[args.cmd](args)


if __name__ == "__main__":
    main()
