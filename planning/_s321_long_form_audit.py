"""s321 긴 곡 split audit — csv 안 movement 명시 부재 자료 catalog.

axis: Symphony / Concerto / Sonata / Suite / Mass / Requiem / Quartet / Quintet / Cantata / Oratorio / Vespro
자체엔 자체엔 movement keyword 부재 자료 자체엔 split 후보 catalog.

산출물: _s321_long_form_audit.txt (UTF-8) 자체엔 file write path · console encoding 회피.
"""

import csv
from pathlib import Path


CSV_PATH = Path('candidate_master.csv')
OUT_PATH = Path('_s321_long_form_audit.txt')

LONG_FORM_KEYWORDS = [
    'Symphony', 'Concerto', 'Sonata', 'Suite', 'Mass', 'Requiem',
    'Quartet', 'Quintet', 'Cantata', 'Oratorio', 'Vespro',
]
MOVEMENT_KEYWORDS = [
    'first movement', 'second movement', 'third movement', 'fourth movement',
    'fifth movement', 'I Allegro', 'II Adagio', 'III Allegro', 'IV ', 'V ',
    'movement', 'Allegro', 'Adagio', 'Andante', 'Largo', 'Presto', 'Scherzo',
    'Finale', 'Lassan', 'Kyrie', 'Magnificat', 'Aria', 'Sanctus', 'Agnus',
    'Credo', 'Gloria', 'Lacrimosa', 'Dies irae', 'Rondo', 'Minuet', 'Menuet',
    'Variations', 'Prelude', 'Fugue', 'Toccata', 'Funeral March', 'Opening',
    'Adagietto', 'Andantino', 'Hymn of the Cherubim', 'Vivace', 'Cantabile',
    'Marche', 'Mvt', 'Ave verum', 'Tuba mirum', 'Recordare', 'Confutatis',
    'Ode to Joy', 'Symphony of Sorrowful',  # specific single-movement-focused entries
]


def main():
    with open(CSV_PATH, encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))

    candidates = []
    for r in rows:
        piece = r['piece']
        is_long_form = any(kw in piece for kw in LONG_FORM_KEYWORDS)
        has_movement = any(kw in piece for kw in MOVEMENT_KEYWORDS)
        if is_long_form and not has_movement:
            candidates.append(r)

    lines = [f'# csv 안 긴 곡 split 후보 audit\n']
    lines.append(f'후보 자료: {len(candidates)}건\n\n')
    for r in candidates:
        lines.append(f'rank {r["rank"]:>3} (tier {r["popularity_tier"]}): {r["piece"]}\n')
        lines.append(f'         {r["piece_ko"]}\n')
        if r['imslp_url']:
            lines.append(f'         IMSLP: {r["imslp_url"]}\n')
        lines.append('\n')

    OUT_PATH.write_text(''.join(lines), encoding='utf-8')
    print(f'wrote: {OUT_PATH} ({len(candidates)} candidates)')


if __name__ == '__main__':
    main()
