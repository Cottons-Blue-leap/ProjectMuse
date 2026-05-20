"""s320 르네상스 D tier 추가 — 6건 append + rank 318 piece_ko 정정.

작업 axis:
  (나) path = 6건 추가 (Spem in alium 제외 · rank 318 이미 박힘) + rank 318 piece_ko 자체엔 mismatch 정정

신축 6 row 자료 (D tier · 르네상스):
  - Josquin des Prez (1450-1521) - Ave Maria... virgo serena (c. 1480)
  - Tomás Luis de Victoria (1548-1611) - O magnum mysterium (1572)
  - Giovanni Palestrina (1525-1594) - Missa Papae Marcelli, Kyrie (1562)
  - Gregorio Allegri (1582-1652) - Miserere mei, Deus (c. 1630) [르네상스 분류 코튼 결단]
  - John Dowland (1563-1626) - Flow, my tears (1600)
  - Thomas Morley (1557-1602) - Now is the month of maying (1595)

rank 318 piece_ko 정정:
  옛: 방랑하는 자들이 찾는 시편 (탈리스 - 40성부 모테트) [잘못된 한국어 axis]
  새: 오직 그분께만 희망을 두었네 (탈리스 - 40성부 모테트) [Spem in alium 직역 axis]

idempotent path · artwork 자체엔 빈 axis (별 cycle · 코튼 결단 자리).
"""

import csv
from pathlib import Path


CSV_PATH = Path('candidate_master.csv')
RANK_COL = '﻿rank'

# rank 318 정정
RANK_318_FIX = {
    'old_piece_ko': '방랑하는 자들이 찾는 시편 (탈리스 - 40성부 모테트)',
    'new_piece_ko': '오직 그분께만 희망을 두었네 (탈리스 - 40성부 모테트)',
}

# 신축 6 row 자료 (base_rank 자체엔 동적 axis · max+1 ~ max+6)
NEW_ROWS = [
    {
        'piece': 'Ave Maria... virgo serena',
        'piece_ko': '아베 마리아... 영원한 동정녀 (조스캥 - 르네상스 motet 대표)',
        'period': '르네상스',
        'popularity_tier': 'D',
    },
    {
        'piece': 'O magnum mysterium',
        'piece_ko': '오 큰 신비여 (빅토리아 - 크리스마스 motet)',
        'period': '르네상스',
        'popularity_tier': 'D',
    },
    {
        'piece': 'Missa Papae Marcelli, Kyrie',
        'piece_ko': '마르첼리 교황 미사 키리에 (팔레스트리나 - 6성부 미사)',
        'period': '르네상스',
        'popularity_tier': 'D',
    },
    {
        'piece': 'Miserere mei, Deus',
        'piece_ko': '미제레레 (알레그리 - 시스티나 채플 9성부)',
        'period': '르네상스',
        'popularity_tier': 'D',
    },
    {
        'piece': 'Flow, my tears',
        'piece_ko': '흘러내려라 나의 눈물이여 (다울런드 - 영국 류트 가곡)',
        'period': '르네상스',
        'popularity_tier': 'D',
    },
    {
        'piece': 'Now is the month of maying',
        'piece_ko': '5월이 오니 (몰리 - 영국 마드리갈)',
        'period': '르네상스',
        'popularity_tier': 'D',
    },
]


def main():
    with open(CSV_PATH, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    # idempotent — 이미 박혀있는 자료 자체엔 skip
    existing_pieces = set(r['piece'] for r in rows)
    new_to_add = [r for r in NEW_ROWS if r['piece'] not in existing_pieces]
    skipped = [r for r in NEW_ROWS if r['piece'] in existing_pieces]

    print(f'new rows to add: {len(new_to_add)}')
    print(f'skipped (already exists): {len(skipped)}')
    for s in skipped:
        print(f'  skipped: {s["piece"]}')

    # rank 318 piece_ko 정정 (idempotent — 이미 정정 자체엔 skip)
    rank_318_fixed = False
    for r in rows:
        if int(r[RANK_COL]) == 318:
            if r['piece_ko'] == RANK_318_FIX['old_piece_ko']:
                r['piece_ko'] = RANK_318_FIX['new_piece_ko']
                rank_318_fixed = True
                print(f'\nrank 318 piece_ko fix: "{RANK_318_FIX["old_piece_ko"]}" -> "{RANK_318_FIX["new_piece_ko"]}"')
            elif r['piece_ko'] == RANK_318_FIX['new_piece_ko']:
                print(f'\nrank 318 piece_ko: 이미 정정 자료 · skip')
            else:
                print(f'\nrank 318 piece_ko: 현재 "{r["piece_ko"]}" · 옛 자료 자체엔 mismatch · 수동 의제')

    # base_rank 자체엔 max+1부터 append
    max_base_rank = max(int(r['base_rank']) for r in rows if r['base_rank'].strip())
    print(f'\nmax base_rank: {max_base_rank}')

    appended_rows = []
    for i, new_row_data in enumerate(new_to_add):
        new_base_rank = max_base_rank + 1 + i
        new_rank = len(rows) + 1 + i  # append axis
        appended = {
            RANK_COL: str(new_rank),
            'base_rank': str(new_base_rank),
            'piece': new_row_data['piece'],
            'piece_ko': new_row_data['piece_ko'],
            'period': new_row_data['period'],
            'score_file': '',
            'imslp_url': '',
            'artwork_title': '',
            'artwork_artist': '',
            'artwork_year': '',
            'artwork_source_lead': '',
            'artwork_rights_note': '',
            'artwork_match_reason': '',
            'popularity_tier': new_row_data['popularity_tier'],
        }
        rows.append(appended)
        appended_rows.append(appended)
        print(f'  appended: rank {new_rank} (base_rank {new_base_rank}) · {new_row_data["piece"]}')

    with open(CSV_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f'\n## final state')
    print(f'total rows: {len(rows)}')
    from collections import Counter
    period_dist = Counter(r['period'] for r in rows)
    tier_dist = Counter(r['popularity_tier'] for r in rows)
    print(f'period dist: {dict(period_dist)}')
    print(f'tier dist: {dict(tier_dist)}')

    renaissance = [r for r in rows if r['period'] == '르네상스']
    print(f'\n르네상스 자료 = {len(renaissance)} (이전 8 → 현재 {len(renaissance)})')


if __name__ == '__main__':
    main()
