#!/usr/bin/env python3
"""WS3 (D3-a) — search-expression audit for Atelier Miku A Cappella.

Collects YouTube search autocomplete (the real phrases people type) per piece
per locale, then audits whether our live title/tags cover those phrases. The
goal is *warm traffic* (search intent) per reference_muse_ctr_impression_floor,
not prettier thumbnails.

The SEO lever per 코튼 doctrine = backend tags (+ title badge, already LOCKed).
Description body stays curator human-voice. So the audit ranks phrases and the
retrofit proposal targets the **tags** field.

Endpoint = Google/YouTube suggest (firefox client → clean JSON array). `hl`
selects locale. No API key / quota. Cache raw so we don't re-hit.

  python Analytics/search_gap_audit.py collect [--out Analytics/search_audit_raw.json]
  python Analytics/search_gap_audit.py report  [--raw ...] [--tags Analytics/live_tags.json]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent

# locale code (our 10) → suggest `hl`
LOCALES = {
    "en": "en", "ja": "ja", "ko": "ko", "es": "es", "pt": "pt",
    "de": "de", "fr": "fr", "ru": "ru", "zh-Hant": "zh-TW", "zh-Hans": "zh-CN",
}

# piece_id → seed queries. English/universal first; locale-native names added
# where the canonical search term differs by script (drives that locale's tail).
SEEDS = {
    "satie_gymnopedie": ["gymnopedie no 1", "gymnopédie", "ジムノペディ", "짐노페디"],
    "vivaldi_spring":   ["vivaldi spring", "four seasons spring", "四季 春", "비발디 봄"],
    "joplin_entertainer": ["the entertainer", "scott joplin entertainer", "エンターテイナー"],
    "elgar_salut":      ["salut d'amour", "elgar salut d'amour", "愛の挨拶", "사랑의 인사"],
    "mozart_k265":      ["twinkle twinkle variations", "ah vous dirai-je maman", "mozart k265", "きらきら星変奏曲"],
    "chopin_nocturne":  ["chopin nocturne op 9 no 2", "nocturne op 9 no 2", "ノクターン 9-2", "쇼팽 녹턴"],
    "pachelbel_canon":  ["pachelbel canon", "canon in d", "パッヘルベル カノン", "캐논"],
    "tchaikovsky_sugarplum": ["dance of the sugar plum fairy", "sugar plum fairy", "金平糖の踊り", "사탕요정"],
    "boccherini_minuet": ["boccherini minuet", "minuet boccherini", "ボッケリーニ メヌエット", "보케리니 미뉴엣"],
}

# Identity terms we differentiate on — does anyone search these for the piece?
IDENTITY_TERMS = ["miku", "hatsune", "初音", "ミク", "미쿠", "acappella", "a cappella",
                  "vocal", "cover", "アカペラ", "아카펠라"]


def fetch(q: str, hl: str, retries: int = 2) -> list[str]:
    url = "https://suggestqueries.google.com/complete/search?" + urllib.parse.urlencode(
        {"client": "firefox", "ds": "yt", "hl": hl, "q": q})
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            data = json.loads(urllib.request.urlopen(req, timeout=10).read().decode("utf-8"))
            return data[1] if len(data) > 1 and isinstance(data[1], list) else []
        except Exception as exc:  # noqa: BLE001
            if attempt == retries:
                print(f"   ! fetch failed q={q!r} hl={hl}: {exc}", file=sys.stderr)
                return []
            time.sleep(0.6)
    return []


def cmd_collect(args: argparse.Namespace) -> int:
    out = Path(args.out or ROOT / "search_audit_raw.json")
    result: dict = {"locales": LOCALES, "pieces": {}}
    for pid, seeds in SEEDS.items():
        result["pieces"][pid] = {}
        for lang, hl in LOCALES.items():
            suggs: dict[str, list[str]] = {}
            for seed in seeds:
                s = fetch(seed, hl)
                if s:
                    suggs[seed] = s
                time.sleep(0.25)  # be polite
            result["pieces"][pid][lang] = suggs
            total = sum(len(v) for v in suggs.values())
            print(f"  {pid:24} {lang:8} → {total} suggestions across {len(suggs)}/{len(seeds)} seeds")
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nraw → {out}")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    raw = json.loads(Path(args.raw or ROOT / "search_audit_raw.json").read_text(encoding="utf-8"))
    live_tags = {}
    if args.tags and Path(args.tags).exists():
        live_tags = json.loads(Path(args.tags).read_text(encoding="utf-8"))

    report = {"pieces": {}}
    for pid, by_lang in raw["pieces"].items():
        # flatten all suggestions across locales
        all_sugg = []
        for lang, seedmap in by_lang.items():
            for seed, suggs in seedmap.items():
                all_sugg.extend(s.lower() for s in suggs)
        uniq = sorted(set(all_sugg))
        identity_hits = [s for s in uniq if any(t.lower() in s for t in IDENTITY_TERMS)]
        # tag coverage: of the suggestion *tokens*, which appear in our tags?
        tags = [t.lower() for t in live_tags.get(pid, [])]
        covered = uncovered = 0
        sample_gap = []
        for s in uniq:
            toks = [w for w in s.replace(",", " ").split() if len(w) > 2]
            if not toks:
                continue
            if tags and any(any(w in tag for tag in tags) for w in toks):
                covered += 1
            else:
                uncovered += 1
                if len(sample_gap) < 12:
                    sample_gap.append(s)
        report["pieces"][pid] = {
            "n_unique_suggestions": len(uniq),
            "identity_term_hits": identity_hits,   # do people search miku/acappella for it?
            "has_live_tags": bool(tags),
            "tag_covered": covered, "tag_uncovered": uncovered,
            "uncovered_sample": sample_gap,
        }
        ident = f"{len(identity_hits)} identity-hits" if identity_hits else "NO identity search"
        cov = f"{covered}/{covered+uncovered} tag-covered" if tags else "(no live tags loaded)"
        print(f"  {pid:24} {len(uniq):3} phrases | {ident:22} | {cov}")
    out = Path(args.out or ROOT / "search_audit_report.json")
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nreport → {out}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="WS3 search-expression audit")
    sub = p.add_subparsers(dest="command", required=True)
    c = sub.add_parser("collect", help="Fetch search autocomplete per piece per locale")
    c.add_argument("--out", default="")
    c.set_defaults(func=cmd_collect)
    r = sub.add_parser("report", help="Audit live tag coverage vs collected phrases")
    r.add_argument("--raw", default="")
    r.add_argument("--tags", default="", help="JSON {piece_id: [live tags]}")
    r.add_argument("--out", default="")
    r.set_defaults(func=cmd_report)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    args = build_parser().parse_args()
    raise SystemExit(args.func(args))
