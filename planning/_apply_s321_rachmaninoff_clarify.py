"""s321 rank 150 Rachmaninoff Piano Concerto No. 2 자체엔 movement 명시 정정.

axis: B 작업 audit 안 *theme* 자체엔 ambiguous axis 적발 · 코튼 결단 = 2악장 Adagio sostenuto 명시.

변경 자료:
  옛 piece: Rachmaninoff Piano Concerto No. 2 theme
  새 piece: Piano Concerto No. 2 Op. 18 second movement Adagio sostenuto
  옛 piece_ko: 라흐마니노프 피아노 협주곡 2번 테마
  새 piece_ko: 피아노 협주곡 2번 작품 18 2악장 아다지오 소스테누토 (라흐마니노프)

다른 자료 자체엔 keep (artwork + imslp + tier).

idempotent path · 이미 정정 통과 시 skip.
"""

import csv
from pathlib import Path


CSV_PATH = Path('candidate_master.csv')
RANK_COL = '﻿rank'

OLD_PIECE = 'Rachmaninoff Piano Concerto No. 2 theme'
NEW_PIECE = 'Piano Concerto No. 2 Op. 18 second movement Adagio sostenuto'
OLD_PIECE_KO = '라흐마니노프 피아노 협주곡 2번 테마'
NEW_PIECE_KO = '피아노 협주곡 2번 작품 18 2악장 아다지오 소스테누토 (라흐마니노프)'


def main():
    with open(CSV_PATH, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    fixed = 0
    already = 0
    not_found = True
    for r in rows:
        if r['piece'] == OLD_PIECE:
            r['piece'] = NEW_PIECE
            r['piece_ko'] = NEW_PIECE_KO
            fixed += 1
            not_found = False
            print(f'rank {r["rank"]} fix:')
            print(f'  piece: "{OLD_PIECE}" -> "{NEW_PIECE}"')
            print(f'  piece_ko: "{OLD_PIECE_KO}" -> "{NEW_PIECE_KO}"')
        elif r['piece'] == NEW_PIECE:
            already += 1
            not_found = False
            print(f'rank {r["rank"]}: 이미 정정 자료 · skip')

    if not_found:
        print(f'rank 150 piece 자료 자체엔 detect 부재 · 의제')
        return

    with open(CSV_PATH, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f'\nfixed: {fixed} · already: {already}')


if __name__ == '__main__':
    main()
