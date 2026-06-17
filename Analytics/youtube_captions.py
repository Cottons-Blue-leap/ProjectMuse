#!/usr/bin/env python3
"""youtube_captions.py — CC 자막 트랙 업로드/감사 (Atelier Miku Acappella).

Phase 4 of the CC caption pipeline. captions.list / insert / update(delete+insert)
for the per-locale WebVTT tracks produced by muse_captions.py.

인증: youtube_meta.py 의 쓰기 토큰(.youtube_write_token.json)을 그대로 재사용.
captions.insert/list/delete 는 모두 youtube.force-ssl 스코프 = 메타 쓰기 토큰과 동일
→ **재인증 불필요**. (단일 채널 = 양 채널 분기 없음.)

사용:
  python Analytics/youtube_captions.py list <video_id>
  python Analytics/youtube_captions.py audit <video_id> --work <work_id>
  python Analytics/youtube_captions.py insert <video_id> --work <work_id> [--langs en,ko,..] [--replace]
  python Analytics/youtube_captions.py delete <caption_id>

VTT 경로 = works/<work_id>/lyrics/captions.<lang>.vtt (muse_captions.py vtt 산출).
"""
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # allow `import youtube_meta`
try:
    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError
    import youtube_meta as ym
except ImportError as e:
    sys.exit(f"의존성/모듈 미설치: {e}\n  youtube_meta.py 와 동일 환경에서 실행.")

BASE = Path(__file__).resolve().parent.parent             # Project_Muse/
DEFAULT_LANGS = ["en", "ko", "ja", "es", "pt", "de", "fr", "ru", "zh-Hant", "zh-Hans"]


def vtt_path(work_id: str, lang: str) -> Path:
    return BASE / "works" / work_id / "lyrics" / f"captions.{lang}.vtt"


def list_tracks(svc, video_id: str):
    res = svc.captions().list(part="snippet", videoId=video_id).execute()
    return res.get("items", [])


def cmd_list(args):
    svc = ym.yt()
    items = list_tracks(svc, args.video)
    if not items:
        print(f"자막 트랙 없음: {args.video}")
        return
    print(f"자막 트랙 {len(items)}개 — {args.video}")
    for it in items:
        s = it["snippet"]
        print(f"  {it['id']}  lang={s.get('language'):8} name={s.get('name','')!r:14} "
              f"status={s.get('status')} draft={s.get('isDraft')} track={s.get('trackKind')}")


def cmd_audit(args):
    svc = ym.yt()
    items = list_tracks(svc, args.video)
    live = {it["snippet"].get("language"): it for it in items}
    print(f"audit {args.video} (work={args.work}) — 기대 {len(DEFAULT_LANGS)} 트랙")
    ok = True
    for lang in DEFAULT_LANGS:
        present = lang in live
        vtt = vtt_path(args.work, lang)
        mark = "✓" if present else "✗"
        if not present:
            ok = False
        draft = live[lang]["snippet"].get("isDraft") if present else None
        print(f"  {mark} {lang:8} live={present} draft={draft} vtt={'있음' if vtt.exists() else '없음'}")
    extra = [l for l in live if l not in DEFAULT_LANGS]
    if extra:
        print(f"  ⚠ 예상 외 트랙: {extra}")
    print("audit PASS" if ok and not extra else "audit 미완 (누락/잉여 있음)")


def insert_one(svc, video_id: str, lang: str, vtt: Path, name: str = "", replace=False, existing=None):
    if existing and lang in existing:
        if not replace:
            return f"skip {lang} (이미 존재 · --replace 로 교체)"
        svc.captions().delete(id=existing[lang]["id"]).execute()
    body = {"snippet": {"videoId": video_id, "language": lang, "name": name, "isDraft": False}}
    media = MediaFileUpload(str(vtt), mimetype="text/vtt", resumable=False)
    res = svc.captions().insert(part="snippet", body=body, media_body=media).execute()
    return f"OK   {lang} → {res['id']}"


def cmd_insert(args):
    svc = ym.yt()
    langs = args.langs.split(",") if args.langs else DEFAULT_LANGS
    existing = {it["snippet"].get("language"): it for it in list_tracks(svc, args.video)}
    print(f"insert {args.video} (work={args.work}) langs={langs} replace={args.replace}")
    for lang in langs:
        vtt = vtt_path(args.work, lang)
        if not vtt.exists():
            print(f"  ✗ {lang}: VTT 없음 {vtt}")
            continue
        try:
            print("  " + insert_one(svc, args.video, lang, vtt, args.name, args.replace, existing))
        except HttpError as e:
            print(f"  ✗ {lang}: HttpError {e}")
    print("→ 완료 후 `audit` 로 10트랙 확인 권장.")


def cmd_delete(args):
    svc = ym.yt()
    svc.captions().delete(id=args.caption_id).execute()
    print(f"삭제됨: {args.caption_id}")


def main():
    p = argparse.ArgumentParser(description="YouTube CC 자막 트랙 (Atelier Miku Acappella)")
    sub = p.add_subparsers(dest="cmd", required=True)

    pl = sub.add_parser("list", help="영상의 현재 자막 트랙 나열")
    pl.add_argument("video")

    pa = sub.add_parser("audit", help="10로케일 트랙 존재/draft 감사")
    pa.add_argument("video")
    pa.add_argument("--work", required=True)

    pi = sub.add_parser("insert", help="VTT 트랙 업로드 (per-locale)")
    pi.add_argument("video")
    pi.add_argument("--work", required=True)
    pi.add_argument("--langs", help="쉼표구분 (기본=10로케일 전부)")
    pi.add_argument("--name", default="", help="트랙 표시명 (기본 빈값=언어 라벨)")
    pi.add_argument("--replace", action="store_true", help="기존 동일언어 트랙 삭제 후 재삽입")

    pd = sub.add_parser("delete", help="자막 트랙 삭제 (caption id)")
    pd.add_argument("caption_id")

    args = p.parse_args()
    {"list": cmd_list, "audit": cmd_audit, "insert": cmd_insert, "delete": cmd_delete}[args.cmd](args)


if __name__ == "__main__":
    main()
