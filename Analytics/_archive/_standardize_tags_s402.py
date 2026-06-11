# -*- coding: utf-8 -*-
"""One-off (s402 · 2026-06-06): standardize backend tags across the 8 live videos.
코튼 approved template (doc 04 §3): piece-string(measured/exact first) → composer →
Miku cluster (+ measured converting queries `miku v6`/`hatsune miku v6`, absent before) →
a cappella → genre/era/cover/channel. read-modify-write (other snippet fields preserved).
  --dry-run  : build + print all 8 + char counts, no apply
  (no flag)  : apply live via videos.update + write tags.txt sidecar + audit
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import youtube_meta as ym
from googleapiclient.errors import HttpError

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DRY = "--dry-run" in sys.argv

# shared blocks (identical across all 8) ----------------------------------------
MIKU = ["Hatsune Miku", "Miku", "初音ミク", "hatsune miku v6", "miku v6", "Vocaloid",
        "Vocaloid6", "V6", "하츠네미쿠", "미쿠", "ミク", "보컬로이드", "보카로", "ボカロ"]
ACA = ["a cappella", "Acappella", "Acapella", "miku acappella", "아카펠라", "アカペラ"]
COVER = ["Cover", "vocaloid cover", "ボカロカバー", "커버", "カバー"]
GENRE = ["Classical Music", "Classical"]
CHANNEL = ["Atelier Miku Acappella"]

# per-song head: (vid, slug, label, piece[], composer[], era[])  piece = exact/searched first
SONGS = [
    ("rRnl8RZ3EjY", "gymnopedie_1_first_proof", "Satie",
     ["Gymnopédie No. 1", "Gymnopedie", "Gymnopédie", "gymnopedie no 1", "짐노페디", "ジムノペディ"],
     ["Erik Satie", "Satie", "에릭 사티", "사티", "サティ"], []),
    ("0qXLYmZXAx0", "vivaldi_spring_1_allegro", "Vivaldi",
     ["Spring", "The Four Seasons", "Four Seasons", "Vivaldi Spring", "사계 봄", "四季 春"],
     ["Antonio Vivaldi", "Vivaldi", "비발디", "ヴィヴァルディ"], ["Baroque"]),
    ("DVIYl09zX-w", "joplin_the_entertainer", "Joplin",
     ["The Entertainer", "Entertainer", "Joplin Entertainer", "엔터테이너", "エンターテイナー"],
     ["Scott Joplin", "Joplin", "조플린", "ジョプリン"], ["Ragtime"]),
    ("zshjmBhus2I", "elgar_salut_damour", "Elgar",
     ["Salut d'Amour", "Salut damour", "Love's Greeting", "Liebesgruss", "사랑의 인사", "愛の挨拶"],
     ["Edward Elgar", "Elgar", "엘가", "エルガー"], ["Romantic"]),
    ("PiR9hy6xmGQ", "mozart_twinkle_variations_k265", "Mozart",
     ["Twinkle Twinkle Little Star", "Ah vous dirai-je maman", "Twinkle Variations",
      "Twelve Variations", "きらきら星", "작은별 변주곡"],
     ["Wolfgang Amadeus Mozart", "Mozart", "모차르트", "モーツァルト"], []),
    ("9EvpHXE3D1s", "chopin_nocturne_op9_2", "Chopin",
     ["Nocturne Op.9 No.2", "Nocturne", "Nocturne Op.9-2", "Nocturne in E-flat", "녹턴", "夜想曲"],
     ["Frédéric Chopin", "Chopin", "쇼팽", "ショパン"], ["Romantic"]),
    ("B9ENEwjgAhc", "pachelbel_canon_in_d", "Pachelbel",
     ["Canon in D", "Pachelbel Canon", "Canon in D major", "Pachelbel's Canon", "캐논 D장조", "カノン"],
     ["Johann Pachelbel", "Pachelbel", "파헬벨", "パッヘルベル"], ["Baroque"]),
    ("759VCWOtC2w", "tchaikovsky_sugar_plum_fairy", "Tchaikovsky",
     ["Dance of the Sugar Plum Fairy", "Sugar Plum Fairy", "The Nutcracker", "Nutcracker",
      "사탕요정의 춤", "金平糖の精の踊り"],
     ["Pyotr Ilyich Tchaikovsky", "Tchaikovsky", "차이콥스키", "チャイコフスキー"], ["Romantic"]),
]


def dedupe(tags):
    seen, out = set(), []
    for t in tags:
        k = t.lower()
        if k not in seen:
            seen.add(k); out.append(t)
    return out


def build(piece, comp, era):
    return dedupe(piece + comp + MIKU + ACA + GENRE + era + COVER + CHANNEL)


def charlen(tags):  # YouTube counts ~ sum + quotes(2) for multi-word; approximate as tool does
    return sum(len(t) for t in tags) + (len(tags) - 1) * 2


def main():
    svc = ym.yt()
    built = []
    print(f"{'DRY-RUN' if DRY else 'APPLY'} · 8 videos\n")
    for vid, slug, label, piece, comp, era in SONGS:
        tags = build(piece, comp, era)
        n = charlen(tags)
        status = "OK" if n <= 500 else f"⚠️OVER {n}"
        print(f"=== {label} · {len(tags)} tags · ~{n}/500 {status}")
        print("    " + " | ".join(tags))
        has = all(q in [t.lower() for t in tags] for q in ["miku v6", "hatsune miku v6"])
        if not has:
            print("    ⚠️ measured query missing!")
        built.append((vid, slug, label, tags, n))
        print()

    over = [b for b in built if b[4] > 500]
    if over:
        print("✗ 500자 초과 곡 있음 — 적용 중단:", [b[2] for b in over]); return
    if DRY:
        print("[dry-run] 전부 ≤500 · measured query 포함 확인. 적용하려면 --dry-run 빼기.")
        return

    print("\n========== APPLY ==========")
    for vid, slug, label, tags, n in built:
        v = ym._get_video(svc, vid)
        old = v["snippet"]
        ns = {"title": old.get("title"), "categoryId": old.get("categoryId"),
              "description": old.get("description", ""), "tags": tags}
        if old.get("defaultLanguage"): ns["defaultLanguage"] = old["defaultLanguage"]
        if old.get("defaultAudioLanguage"): ns["defaultAudioLanguage"] = old["defaultAudioLanguage"]
        try:
            svc.videos().update(part="snippet", body={"id": vid, "snippet": ns}).execute()
        except HttpError as e:
            print(f"  ✗ {label}: {e}"); continue
        # sidecar
        sc = Path("works") / slug / "video" / "release" / "tags.txt"
        sc.write_text(", ".join(tags) + "\n", encoding="utf-8")
        print(f"  ✓ {label}: {len(tags)} tags 적용 + sidecar {sc}")

    print("\n========== AUDIT ==========")
    ok = True
    for vid, slug, label, tags, n in built:
        live = ym._get_video(svc, vid)["snippet"].get("tags", [])
        low = [t.lower() for t in live]
        miss = [q for q in ["miku v6", "hatsune miku v6"] if q not in low]
        first_ok = live and live[0] == tags[0]
        if live == tags and not miss:
            print(f"  ✓ {label}: {len(live)} tags · piece-first '{live[0]}' · measured 포함")
        else:
            ok = False
            print(f"  ✗ {label}: live={len(live)} expected={len(tags)} · miss={miss} · first_ok={first_ok}")
    print("\n" + ("✓ 전수 AUDIT PASS" if ok else "✗ AUDIT 실패 — 위 확인"))


if __name__ == "__main__":
    main()
