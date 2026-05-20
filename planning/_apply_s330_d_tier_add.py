"""s330 D tier 추가 — 코튼 list 안 csv 미매칭 3곡 append.

작업 axis (s330 코튼 list 12곡 자가 매칭 cycle 후 NO MATCH 3건 axis):
  - 파가니니 바이올린 협주곡 2번 3악장 라 캄파넬라 (Op. 7 · 원곡 · rank 52 La Campanella는 리스트 편곡 S.141 axis 별)
  - 하이든 트럼펫 협주곡 3악장 (Hob.VIIe:1 Finale)
  - 비발디 조화의 영감 6번 1악장 (Op. 3 No. 6 · RV 356)

코튼 결단:
  - 다 D tier 박음
  - 명화 자가 결단 axis (3건 다 OK 결단 통과)

자가 결함 차단 axis (E41 family 재발 사전 차단):
  - s321 `new_rank = len(rows) + 1 + i` self-double bug 박힌 자료 axis
  - 본 cycle 양식 = `new_rank = len(rows) + 1` (i 더하기 X · append 후 rows 자체 자가 길이 +1)

idempotent path · existing_pieces check · 이미 박혀있는 자료 자체엔 skip.
"""

import csv
from collections import Counter
from pathlib import Path


CSV_PATH = Path('candidate_master.csv')
RANK_COL = 'rank'  # csv DictReader 안 utf-8-sig 자체 자가 자가 strip BOM


def _wikimedia_search_url(title: str, artist: str) -> str:
    query = f'{title} {artist} public domain painting'.replace(' ', '+')
    return f'https://commons.wikimedia.org/w/index.php?search={query}&title=Special:MediaSearch&type=image'


NEW_ROWS = [
    {
        'piece': 'Violin Concerto No. 2 third movement Rondo La Campanella Op. 7',
        'piece_ko': '바이올린 협주곡 2번 3악장 론도 라 캄파넬라 (파가니니)',
        'period': '낭만',
        'imslp_url': 'https://imslp.org/wiki/Violin_Concerto_No.2,_Op.7_(Paganini,_Niccolò)',
        'artwork_title': 'Portrait of Niccolò Paganini',
        'artwork_artist': 'Eugène Delacroix',
        'artwork_year': 'c. 1831',
        'artwork_match_reason': "Delacroix's Romantic portrait of Paganini matches the violinist's virtuosic flair and the Rondo's spectral bell figure.",
        'popularity_tier': 'D',
    },
    {
        'piece': 'Trumpet Concerto Hob.VIIe:1 third movement Finale Allegro',
        'piece_ko': '트럼펫 협주곡 3악장 피날레 알레그로 (하이든)',
        'period': '고전',
        'imslp_url': 'https://imslp.org/wiki/Trumpet_Concerto,_Hob.VIIe:1_(Haydn,_Joseph)',
        'artwork_title': 'Napoleon at the Battle of Eylau',
        'artwork_artist': 'Antoine-Jean Gros',
        'artwork_year': '1808',
        'artwork_match_reason': "Gros's tumultuous battlefield matches the Finale's fanfare exuberance and the military trumpet's origins.",
        'popularity_tier': 'D',
    },
    {
        'piece': "L'estro armonico Op. 3 No. 6 first movement Allegro RV 356",
        'piece_ko': '조화의 영감 작품 3-6 1악장 알레그로 (비발디)',
        'period': '바로크',
        'imslp_url': 'https://imslp.org/wiki/Violin_Concerto_in_A_minor,_RV_356_(Vivaldi,_Antonio)',
        'artwork_title': 'The Bucintoro Returning to the Molo on Ascension Day',
        'artwork_artist': 'Canaletto',
        'artwork_year': 'c. 1733-34',
        'artwork_match_reason': "Canaletto's Venetian ceremonial pageantry matches Vivaldi's Venetian baroque virtuosity and the concerto's brilliant interplay.",
        'popularity_tier': 'D',
    },
]


def main():
    with open(CSV_PATH, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    existing_pieces = set(r['piece'] for r in rows)
    new_to_add = [r for r in NEW_ROWS if r['piece'] not in existing_pieces]
    skipped = [r for r in NEW_ROWS if r['piece'] in existing_pieces]

    print(f'new rows to add: {len(new_to_add)}')
    print(f'skipped (already exists): {len(skipped)}')
    for s in skipped:
        print(f'  skipped: {s["piece"]}')

    if not new_to_add:
        print('\n전부 이미 박힘 · idempotent skip · 종료')
        return

    max_base_rank = max(int(r['base_rank']) for r in rows if r['base_rank'].strip())
    print(f'\nmax base_rank prev: {max_base_rank}')

    for data in new_to_add:
        new_base_rank = max_base_rank + 1
        # self-double bug 차단: append 후 rows 자체 자가 길이 +1 axis · i offset X
        new_rank = len(rows) + 1
        appended = {
            RANK_COL: str(new_rank),
            'base_rank': str(new_base_rank),
            'piece': data['piece'],
            'piece_ko': data['piece_ko'],
            'period': data['period'],
            'score_file': '',
            'imslp_url': data['imslp_url'],
            'artwork_title': data['artwork_title'],
            'artwork_artist': data['artwork_artist'],
            'artwork_year': data['artwork_year'],
            'artwork_source_lead': _wikimedia_search_url(data['artwork_title'], data['artwork_artist']),
            'artwork_rights_note': 'public_domain_likely_verify_before_release',
            'artwork_match_reason': data['artwork_match_reason'],
            'popularity_tier': data['popularity_tier'],
        }
        rows.append(appended)
        max_base_rank = new_base_rank
        print(f'  appended: rank {new_rank} (base_rank {new_base_rank}) · {data["piece"]}')

    # utf-8-sig 양식 자가 자가 자가 keep
    with open(CSV_PATH, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f'\n## final state')
    print(f'total rows: {len(rows)}')
    period_dist = Counter(r['period'] for r in rows)
    tier_dist = Counter(r['popularity_tier'] for r in rows)
    print(f'period dist: {dict(period_dist)}')
    print(f'tier dist: {dict(tier_dist)}')


if __name__ == '__main__':
    main()
