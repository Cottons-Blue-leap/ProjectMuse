# -*- coding: utf-8 -*-
"""One-off (s402): sync series_history.csv release_title column to the A Cappella badge.
Live retrofit already done (_retrofit_acappella_badge_s402.py); this mirrors it in the log.
Tchaikovsky (#8) intentionally skipped — still scheduled/old-format pending 코튼 decision.
"""
from pathlib import Path

P = Path(__file__).resolve().parent.parent / "series_history.csv"
REPL = [
    ("Satie - Gymnopédie No. 1 (feat. 初音ミク)", "Satie - Gymnopédie No. 1 【初音ミク A Cappella】"),
    ("Vivaldi - Spring, Mvt. I (feat. 初音ミク)", "Vivaldi - Spring, Mvt. I 【初音ミク A Cappella】"),
    ("Joplin - The Entertainer (feat. 初音ミク)", "Joplin - The Entertainer 【初音ミク A Cappella】"),
    ("Elgar - Salut d'Amour (feat. 初音ミク)", "Elgar - Salut d'Amour 【初音ミク A Cappella】"),
    ("K.265 (feat. 初音ミク)", "K.265 【A Cappella】"),  # Mozart → abbreviated badge
    ("Chopin - Nocturne Op. 9 No. 2 (feat. 初音ミク)", "Chopin - Nocturne Op. 9 No. 2 【初音ミク A Cappella】"),
    ("Pachelbel - Canon in D (feat. 初音ミク)", "Pachelbel - Canon in D 【初音ミク A Cappella】"),
]
s = P.read_text(encoding="utf-8")
for a, b in REPL:
    assert a in s, f"못 찾음: {a!r}"
    assert s.count(a) == 1, f"중복 {s.count(a)}건: {a!r}"
    s = s.replace(a, b)
P.write_text(s, encoding="utf-8")
print(f"✓ series_history.csv: {len(REPL)} release_title 갱신 (Tchaikovsky 제외)")
