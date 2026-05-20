"""s321 부분 박힌 work 누락 movement D tier 추가 — 9건 append.

작업 axis (s320 retro *부분 박힌 work 다른 movement 추가 axis* 의제 path):
  - 비발디 사계 여름 1·2악장 (RV 315)
  - 비발디 사계 겨울 1·3악장 (RV 297)
  - 베토벤 영웅 교향곡 3·4악장 (Op. 55)
  - 차이콥스키 비창 교향곡 2·3악장 (Op. 74)
  - 베토벤 비창 소나타 3악장 (Op. 13)

코튼 결단:
  - 새롭게 추가된 것들 자체엔 다 D tier 박음
  - artwork 자체엔 MOKA 4 axis 사전 결단 자료 박힘 (사전 throw 통과)

명화 자가 detect 통과 (회피 path 3건):
  - Bruegel *The Harvesters* (rank 104 박힘) → 봄 3악장 axis 회피
  - Delacroix *Liberty Leading the People* (rank 160 박힘) → 영웅 폴로네이즈 axis 회피
  - Vereshchagin *The Apotheosis of War* (rank 265 박힘) → 비창 4악장 axis 회피

idempotent path · existing_pieces check · 이미 박혀있는 자료 자체엔 skip.
"""

import csv
from collections import Counter
from pathlib import Path


CSV_PATH = Path('candidate_master.csv')
RANK_COL = '﻿rank'


def _wikimedia_search_url(title: str, artist: str) -> str:
    query = f'{title} {artist} public domain painting'.replace(' ', '+')
    return f'https://commons.wikimedia.org/w/index.php?search={query}&title=Special:MediaSearch&type=image'


NEW_ROWS = [
    {
        'piece': 'Summer I Allegro non molto from The Four Seasons',
        'piece_ko': '사계 중 여름 1악장 Allegro non molto (비발디)',
        'period': '바로크',
        'imslp_url': 'https://imslp.org/wiki/Violin_Concerto_in_G_minor,_RV_315_(Vivaldi,_Antonio)',
        'artwork_title': 'The Gleaners',
        'artwork_artist': 'Jean-François Millet',
        'artwork_year': '1857',
        'artwork_match_reason': "Stooped peasant women in summer fields match the movement's oppressive heat and toil.",
        'popularity_tier': 'D',
    },
    {
        'piece': 'Summer II Adagio from The Four Seasons',
        'piece_ko': '사계 중 여름 2악장 Adagio (비발디)',
        'period': '바로크',
        'imslp_url': 'https://imslp.org/wiki/Violin_Concerto_in_G_minor,_RV_315_(Vivaldi,_Antonio)',
        'artwork_title': 'The Angelus',
        'artwork_artist': 'Jean-François Millet',
        'artwork_year': '1857-1859',
        'artwork_match_reason': "Twilight pause in the fields echoes the shepherd's uneasy slumber before the storm.",
        'popularity_tier': 'D',
    },
    {
        'piece': 'Winter I Allegro non molto from The Four Seasons',
        'piece_ko': '사계 중 겨울 1악장 Allegro non molto (비발디)',
        'period': '바로크',
        'imslp_url': 'https://imslp.org/wiki/Violin_Concerto_in_F_minor,_RV_297_(Vivaldi,_Antonio)',
        'artwork_title': 'The Sea of Ice',
        'artwork_artist': 'Caspar David Friedrich',
        'artwork_year': '1823-1824',
        'artwork_match_reason': "Shattering ice and frozen desolation match the movement's biting cold and trembling.",
        'popularity_tier': 'D',
    },
    {
        'piece': 'Winter III Allegro from The Four Seasons',
        'piece_ko': '사계 중 겨울 3악장 Allegro (비발디)',
        'period': '바로크',
        'imslp_url': 'https://imslp.org/wiki/Violin_Concerto_in_F_minor,_RV_297_(Vivaldi,_Antonio)',
        'artwork_title': 'Winter Landscape with Ice Skaters',
        'artwork_artist': 'Hendrick Avercamp',
        'artwork_year': 'c. 1608',
        'artwork_match_reason': "Skaters slipping on frozen canal match the finale's depiction of treacherous ice.",
        'popularity_tier': 'D',
    },
    {
        'piece': 'Eroica Symphony third movement Scherzo Op. 55',
        'piece_ko': '영웅 교향곡 3악장 스케르초 (베토벤)',
        'period': '고전',
        'imslp_url': 'https://imslp.org/wiki/Symphony_No.3,_Op.55_(Beethoven,_Ludwig_van)',
        'artwork_title': 'The Charging Chasseur',
        'artwork_artist': 'Théodore Géricault',
        'artwork_year': '1812',
        'artwork_match_reason': "Charging mounted officer matches the Scherzo's hunting-horn fanfare and martial drive.",
        'popularity_tier': 'D',
    },
    {
        'piece': 'Eroica Symphony fourth movement Finale Op. 55',
        'piece_ko': '영웅 교향곡 4악장 피날레 (베토벤)',
        'period': '고전',
        'imslp_url': 'https://imslp.org/wiki/Symphony_No.3,_Op.55_(Beethoven,_Ludwig_van)',
        'artwork_title': 'Oath of the Horatii',
        'artwork_artist': 'Jacques-Louis David',
        'artwork_year': '1784',
        'artwork_match_reason': "Neoclassical heroic oath matches the finale's variation-built triumphant resolve.",
        'popularity_tier': 'D',
    },
    {
        'piece': 'Symphony No. 6 Pathetique Op. 74 second movement Allegro con grazia',
        'piece_ko': '비창 교향곡 작품 74 2악장 Allegro con grazia (차이콥스키)',
        'period': '낭만',
        'imslp_url': 'https://imslp.org/wiki/Symphony_No.6,_Op.74_(Tchaikovsky,_Pyotr)',
        'artwork_title': 'The Dance Class',
        'artwork_artist': 'Edgar Degas',
        'artwork_year': '1874',
        'artwork_match_reason': "Asymmetric ballet rehearsal matches the movement's 5/4 limping waltz grace.",
        'popularity_tier': 'D',
    },
    {
        'piece': 'Symphony No. 6 Pathetique Op. 74 third movement Allegro molto vivace',
        'piece_ko': '비창 교향곡 작품 74 3악장 Allegro molto vivace (차이콥스키)',
        'period': '낭만',
        'imslp_url': 'https://imslp.org/wiki/Symphony_No.6,_Op.74_(Tchaikovsky,_Pyotr)',
        'artwork_title': 'Barge Haulers on the Volga',
        'artwork_artist': 'Ilya Repin',
        'artwork_year': '1870-1873',
        'artwork_match_reason': "Russian laborers' grinding procession matches the march's relentless triumph turned tragic.",
        'popularity_tier': 'D',
    },
    {
        'piece': 'Pathetique Sonata third movement Rondo Allegro Op. 13',
        'piece_ko': '비창 소나타 3악장 론도 알레그로 (베토벤)',
        'period': '고전',
        'imslp_url': 'https://imslp.org/wiki/Piano_Sonata_No.8,_Op.13_(Beethoven,_Ludwig_van)',
        'artwork_title': 'Wanderer above the Sea of Fog',
        'artwork_artist': 'Caspar David Friedrich',
        'artwork_year': '1818',
        'artwork_match_reason': "Romantic solitary wanderer matches the Rondo's restless emotional sweep.",
        'popularity_tier': 'D',
    },
]


def main():
    with open(CSV_PATH, encoding='utf-8') as f:
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
    print(f'\nmax base_rank: {max_base_rank}')

    for i, data in enumerate(new_to_add):
        new_base_rank = max_base_rank + 1 + i
        new_rank = len(rows) + 1 + i
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
        print(f'  appended: rank {new_rank} (base_rank {new_base_rank}) · {data["piece"]}')

    with open(CSV_PATH, 'w', encoding='utf-8', newline='') as f:
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
