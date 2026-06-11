# -*- coding: utf-8 -*-
"""s411 (2026-06-09): JP 2차창작 유입 보강 — 백엔드 태그에 4종 추가 + 보케리니 0-태그 백필.

근거 = GPT JP 유입 진단 보고서(jp_2nd_creation_inflow_report_2026-06-09) → MOKA 판단 적용분 (1).
SEO 레버 = 태그/해시태그만 손댄다 (설명 본문·제목 badge 불가침 · feedback_muse_description_human_voice).

추가 태그 (NEW_JP): 全部ミク(N-Mikus 시그너처 = 우리 정체성 정확 일치) · ミクアカペラ(일본어 표기 부재) ·
VOCALOIDカバー · 初音ミクカバー (보고서 지적 부재 핵심어). ※ ミクカバー = 기존 ボカロカバー와 중복이라 제외.

방식 = APPEND read-modify-write (기존 태그 순서/내용 보존 · 라이브가 알파벳 정렬 반환하는 quirk 회피 위해
재빌드 X). 보케리니(라이브 0 태그)만 s402 템플릿으로 풀빌드 후 NEW_JP 부착.
  --dry-run : 빌드 + char 카운트 + diff 출력, 미적용
  (no flag) : videos.update(part=snippet) 적용 + works/<slug>/video/release/tags.txt 갱신 + audit
"""
import sys, importlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
std = importlib.import_module("_standardize_tags_s402")
import youtube_meta as ym
from googleapiclient.errors import HttpError

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DRY = "--dry-run" in sys.argv
NEW_JP = ["全部ミク", "ミクアカペラ", "VOCALOIDカバー", "初音ミクカバー"]

VIDS = [
    ("rRnl8RZ3EjY", "gymnopedie_1_first_proof"),
    ("0qXLYmZXAx0", "vivaldi_spring_1_allegro"),
    ("DVIYl09zX-w", "joplin_the_entertainer"),
    ("zshjmBhus2I", "elgar_salut_damour"),
    ("PiR9hy6xmGQ", "mozart_twinkle_variations_k265"),
    ("9EvpHXE3D1s", "chopin_nocturne_op9_2"),
    ("B9ENEwjgAhc", "pachelbel_canon_in_d"),
    ("759VCWOtC2w", "tchaikovsky_sugar_plum_fairy"),
    ("X9xxOeqi2Sk", "boccherini_minuet"),
]

# 보케리니 풀빌드용 (s402 SONGS에 없던 신곡 · piece exact/searched first → composer → era)
BOC_PIECE = ["Minuet", "Boccherini Minuet", "Boccherini Minuetto", "Minuetto",
             "String Quintet", "メヌエット", "미뉴엣", "미뉴에트"]
BOC_COMP = ["Luigi Boccherini", "Boccherini", "ボッケリーニ", "보케리니"]


def main():
    svc = ym.yt()
    print(f"{'DRY-RUN' if DRY else 'APPLY'} · {len(VIDS)} videos · +NEW_JP {NEW_JP}\n")
    plans = []
    for vid, slug in VIDS:
        v = ym._get_video(svc, vid)
        old = v["snippet"]
        cur = old.get("tags", []) or []
        if not cur:
            if slug != "boccherini_minuet":
                print(f"  ⚠️ {slug}: 태그 0인데 보케리니 아님 — 수동확인 필요, skip"); continue
            base = std.build(BOC_PIECE, BOC_COMP, ["Classical"])
            origin = "FULL-BUILD(보케리니 백필)"
        else:
            base = cur
            origin = f"append(기존 {len(cur)})"
        final = std.dedupe(base + NEW_JP)
        n = std.charlen(final)
        added = [t for t in final if t not in cur]
        status = "OK" if n <= 500 else f"⚠️OVER {n}"
        changed = final != cur
        print(f"=== {slug} [{vid}] · {origin} → {len(final)} tags · ~{n}/500 {status} · {'CHANGED' if changed else 'no-op'}")
        print(f"    +added: {added}")
        plans.append((vid, slug, old, cur, final, changed))
        print()

    over = [p for p in plans if std.charlen(p[4]) > 500]
    if over:
        print("✗ 500자 초과 — 중단:", [p[1] for p in over]); return
    if DRY:
        print("[dry-run] 전부 ≤500. 적용하려면 --dry-run 제거.")
        return

    print("\n========== APPLY ==========")
    for vid, slug, old, cur, final, changed in plans:
        if not changed:
            print(f"  · {slug}: no-op skip"); continue
        ns = {"title": old.get("title"), "categoryId": old.get("categoryId"),
              "description": old.get("description", ""), "tags": final}
        if old.get("defaultLanguage"): ns["defaultLanguage"] = old["defaultLanguage"]
        if old.get("defaultAudioLanguage"): ns["defaultAudioLanguage"] = old["defaultAudioLanguage"]
        try:
            svc.videos().update(part="snippet", body={"id": vid, "snippet": ns}).execute()
        except HttpError as e:
            print(f"  ✗ {slug}: {e}"); continue
        sc = Path("works") / slug / "video" / "release" / "tags.txt"
        sc.parent.mkdir(parents=True, exist_ok=True)
        sc.write_text(", ".join(final) + "\n", encoding="utf-8")
        print(f"  ✓ {slug}: {len(final)} tags 적용 + sidecar")

    print("\n========== AUDIT (set-membership) ==========")
    ok = True
    for vid, slug, old, cur, final, changed in plans:
        live = ym._get_video(svc, vid)["snippet"].get("tags", []) or []
        low = [t.lower() for t in live]
        miss = [t for t in NEW_JP if t.lower() not in low]
        n = std.charlen(live)
        if not miss and n <= 500 and len(live) >= len(final) - 0:
            print(f"  ✓ {slug}: {len(live)} tags · NEW_JP 포함 · ~{n}/500")
        else:
            ok = False
            print(f"  ✗ {slug}: live={len(live)} miss={miss} ~{n}/500")
    print("\n" + ("✓ 전수 AUDIT PASS" if ok else "✗ AUDIT 실패"))


if __name__ == "__main__":
    main()
