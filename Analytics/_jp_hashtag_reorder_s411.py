# -*- coding: utf-8 -*-
"""s411 (2026-06-09): JP 설명 해시태그 상위 재배열 — JA localization description만.

근거 = GPT JP 유입 진단 보고서 → MOKA 판단 적용분 (1).
현 JA 해시태그: #初音ミク #アカペラ #{곡명} #ボカロ #ボカロカバー #クラシック #{시대} #{작곡가} #AtelierMikuAcappella
변경 후 (top-3 = 初音ミク / ボカロカバー / アカペラ · 2차창작 신호 全部ミク·ミクアカペラ 추가 · 시대 해시태그 drop):
  #初音ミク #ボカロカバー #アカペラ #{곡명} #全部ミク #ミクアカペラ #ボカロ #クラシック #{작곡가} #AtelierMikuAcappella

설명 본문(큐레이터/bespoke hook)은 불변 — 마지막 해시태그 1줄만 교체 (feedback_muse_description_human_voice).
4개 work(boccherini/chopin/pachelbel/tchaikovsky)는 description.ja.txt sidecar도 동기화 (drift 회피).
나머지 5 레거시작은 ja sidecar 없음 → 라이브가 source (그대로).
  --dry-run : old/new 해시태그 줄 diff 출력, 미적용
  (no flag) : videos.update(part=snippet,localizations) 적용 + sidecar 동기화 + audit
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import youtube_meta as ym
from googleapiclient.errors import HttpError

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DRY = "--dry-run" in sys.argv

# slug → (vid, #곡명, #작곡가)
WORKS = [
    ("gymnopedie_1_first_proof", "rRnl8RZ3EjY", "#ジムノペディ", "#サティ"),
    ("vivaldi_spring_1_allegro", "0qXLYmZXAx0", "#四季", "#ヴィヴァルディ"),
    ("joplin_the_entertainer", "DVIYl09zX-w", "#ジエンターテイナー", "#ジョプリン"),
    ("elgar_salut_damour", "zshjmBhus2I", "#愛の挨拶", "#エルガー"),
    ("mozart_twinkle_variations_k265", "PiR9hy6xmGQ", "#きらきら星変奏曲", "#モーツァルト"),
    ("chopin_nocturne_op9_2", "9EvpHXE3D1s", "#ノクターン", "#ショパン"),
    ("pachelbel_canon_in_d", "B9ENEwjgAhc", "#カノン", "#パッヘルベル"),
    ("tchaikovsky_sugar_plum_fairy", "759VCWOtC2w", "#金平糖の精の踊り", "#チャイコフスキー"),
    ("boccherini_minuet", "X9xxOeqi2Sk", "#メヌエット", "#ボッケリーニ"),
]


def new_line(piece, comp):
    return (f"#初音ミク #ボカロカバー #アカペラ {piece} #全部ミク #ミクアカペラ "
            f"#ボカロ #クラシック {comp} #AtelierMikuAcappella")


def swap_hashtag_line(desc, piece, comp):
    """마지막 '#初音ミク...' 줄을 새 줄로 교체. 정확히 1줄이어야 함."""
    lines = desc.splitlines()
    idx = [i for i, l in enumerate(lines) if l.strip().startswith("#初音ミク")]
    if len(idx) != 1:
        return None, f"해시태그 줄 {len(idx)}개 (1개 기대)"
    old = lines[idx[0]]
    lines[idx[0]] = new_line(piece, comp)
    return "\n".join(lines), old


def main():
    svc = ym.yt()
    print(f"{'DRY-RUN' if DRY else 'APPLY'} · {len(WORKS)} videos (JA localization)\n")
    plans = []
    for slug, vid, piece, comp in WORKS:
        v = svc.videos().list(part="snippet,localizations", id=vid).execute()["items"][0]
        sn = v["snippet"]; locs = dict(v.get("localizations") or {})
        ja = locs.get("ja")
        if not ja:
            print(f"  ⚠️ {slug}: ja localization 없음 — skip"); continue
        newdesc, old = swap_hashtag_line(ja["description"], piece, comp)
        if newdesc is None:
            print(f"  ✗ {slug}: {old} — skip"); continue
        nl = new_line(piece, comp)
        changed = newdesc != ja["description"]
        print(f"=== {slug} [{vid}] {'CHANGED' if changed else 'no-op'}")
        print(f"    old: {old}")
        print(f"    new: {nl}")
        plans.append((slug, vid, sn, locs, ja, newdesc, changed))
        print()

    if DRY:
        print("[dry-run] 적용하려면 --dry-run 제거.")
        return

    print("\n========== APPLY ==========")
    for slug, vid, sn, locs, ja, newdesc, changed in plans:
        if not changed:
            print(f"  · {slug}: no-op skip"); continue
        locs["ja"] = {"title": ja["title"], "description": newdesc}
        new_snippet = {"title": sn.get("title"), "categoryId": sn.get("categoryId"),
                       "description": sn.get("description", "")}
        if sn.get("tags"): new_snippet["tags"] = sn["tags"]
        if sn.get("defaultLanguage"): new_snippet["defaultLanguage"] = sn["defaultLanguage"]
        if sn.get("defaultAudioLanguage"): new_snippet["defaultAudioLanguage"] = sn["defaultAudioLanguage"]
        try:
            svc.videos().update(part="snippet,localizations",
                                body={"id": vid, "snippet": new_snippet, "localizations": locs}).execute()
        except HttpError as e:
            print(f"  ✗ {slug}: {e}"); continue
        # sidecar 동기화 (있는 경우만)
        piece, comp = next((p, c) for s, v_, p, c in WORKS if s == slug)
        sc = Path("works") / slug / "video" / "release" / "description.ja.txt"
        sidemsg = ""
        if sc.exists():
            sd, _ = swap_hashtag_line(sc.read_text(encoding="utf-8"), piece, comp)
            if sd:
                sc.write_text(sd + "\n", encoding="utf-8")
                sidemsg = " + sidecar"
        print(f"  ✓ {slug}: JA 해시태그 재배열{sidemsg}")

    print("\n========== AUDIT ==========")
    ok = True
    for slug, vid, sn, locs, ja, newdesc, changed in plans:
        piece, comp = next((p, c) for s, v_, p, c in WORKS if s == slug)
        live = svc.videos().list(part="localizations", id=vid).execute()["items"][0]
        jad = (live.get("localizations") or {}).get("ja", {}).get("description", "")
        want = new_line(piece, comp)
        htlines = [l for l in jad.splitlines() if l.strip().startswith("#初音ミク")]
        good = len(htlines) == 1 and htlines[0] == want
        print(f"  {'✓' if good else '✗'} {slug}: {htlines[0] if htlines else '(없음)'}")
        if not good: ok = False
    print("\n" + ("✓ 전수 AUDIT PASS" if ok else "✗ AUDIT 실패"))


if __name__ == "__main__":
    main()
