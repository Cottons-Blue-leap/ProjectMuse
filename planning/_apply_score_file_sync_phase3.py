"""score_file column sync phase 3 + 림스키 살탄 황제 신규 row 등재 (s367 cycle).

목적:
  - Phase 3 backfill 7 row (csv 기존 row · fuzzy match 부족으로 audit이 못잡은 자료 · 코튼 *MOKA 추천대로* 결단 흡수)
  - 림스키 살탄 황제의 이야기 모음곡 신규 row 등재 (Three Wonders · tier D · niche)
  - csv consistency = utf-8-sig (BOM 보존)

idempotent. 이미 정답이면 skip. piece_ko exact 매칭 의무.

자가 결단 자료:
  - 그린슬리브스 4 PDF 중 1번만 score_file 박음 (csv multi-PDF 양식 미사용 → consistency keep)
  - 림스키 살탄: Three Wonders 박음 (가장 알려진 movement · 왕벌의 비행 별도 rank 18 등재) · tier D (한국 lesson culture X · 세계 기준 niche)
"""

import csv
import shutil
import sys
from pathlib import Path

CSV_PATH = Path('candidate_master.csv')
BACKUP_PATH = Path('candidate_master.csv.bak_s367_score_file_sync_phase3')

# Phase 3 backfill: (rank, expected piece_ko, new_sf)
CHANGES = [
    ('71', 'G장조 미뉴에트 BWV Anh. 114 (페촐트, 바흐 전집 수록)', '요한 제바스티안 바흐_바흐 전집.pdf'),
    ('86', '예수 인류의 기쁨이 되시니 (바흐)', '요한 제바스티안 바흐_마음과 입과 행동과 생명으로 BWV0147.pdf'),
    ('94', '비창 소나타 1악장 (베토벤)', '루트비히 판 베토벤_비창 소나타 1악장.pdf'),
    ('101', '그린슬리브즈 (16세기 영국 전통)', '그린슬리브스_1.pdf'),
    ('107', '기사들의 춤 (프로코피예프 - 로미오와 줄리엣)', '세르게이 프로코피예프_로미오와 줄리엣 1막.pdf'),
    ('126', '「나는 거리의 만물박사」 (로시니 - 세비야의 이발사)', '조아키노 로시니_세비야의 이발사 1막.pdf'),
    ('130', '교향곡 25번 G단조 1악장 (모차르트)', '볼프강 아마데우스 모차르트_교향곡 제25번 G단조 작품 183.pdf'),
]

# 신규 row 등재: 림스키 살탄 황제 「세 가지 기적」
# 모든 column 채움 (artwork = 빔 = cotton 결단 자리)
NEW_ROW = {
    'piece': 'The Three Wonders from Tale of Tsar Saltan Op. 57',
    'piece_ko': '살탄 황제의 이야기 중 「세 가지 기적」 작품 57 (림스키-코르사코프)',
    'period': '낭만',
    'score_file': '니콜라이 림스키코르사코프_살탄 황제의 이야기 Op.57.pdf',
    'imslp_url': 'https://imslp.org/wiki/Tale_of_Tsar_Saltan_(Rimsky-Korsakov,_Nikolay)',
    'artwork_title': '',
    'artwork_artist': '',
    'artwork_year': '',
    'artwork_source_lead': '',
    'artwork_rights_note': '',
    'artwork_match_reason': '',
    'popularity_tier': 'D',
}


def main():
    sys.stdout.reconfigure(encoding='utf-8')

    if not CSV_PATH.exists():
        print(f'ERROR: {CSV_PATH} not found')
        sys.exit(1)

    pdfs = set(p.name for p in Path('candidates_opus').glob('*.pdf'))

    # backfill target PDFs 폴더 실존 verify
    targets = [new_sf for _, _, new_sf in CHANGES] + [NEW_ROW['score_file']]
    missing = [t for t in targets if t not in pdfs]
    if missing:
        print('ABORT: 다음 target PDF 폴더에 없음:')
        for m in missing:
            print(f'  {m}')
        sys.exit(2)

    if not BACKUP_PATH.exists():
        shutil.copy(CSV_PATH, BACKUP_PATH)
        print(f'backup created: {BACKUP_PATH}')

    with open(CSV_PATH, encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    # Phase 3 backfill
    changes_dict = {rank: (pk, sf) for rank, pk, sf in CHANGES}
    applied = 0
    skipped = 0
    piece_mismatch = []
    for r in rows:
        if r['rank'] in changes_dict:
            expected_pk, new_sf = changes_dict[r['rank']]
            if r['piece_ko'] != expected_pk:
                piece_mismatch.append(f'rank {r["rank"]} | csv="{r["piece_ko"]}" vs expected="{expected_pk}"')
                continue
            if r['score_file'] == new_sf:
                skipped += 1
            else:
                old_sf = r['score_file']
                r['score_file'] = new_sf
                applied += 1
                print(f'  backfill rank {r["rank"]} | {r["piece_ko"][:35]} | "{old_sf}" -> "{new_sf}"')

    if piece_mismatch:
        print('ABORT: piece_ko mismatch:')
        for m in piece_mismatch:
            print(f'  {m}')
        sys.exit(3)

    # 림스키 살탄 새 row 등재 (idempotent · 동일 piece_ko 이미 있으면 skip)
    new_row_added = False
    existing_with_piece_ko = [r for r in rows if r['piece_ko'] == NEW_ROW['piece_ko']]
    if existing_with_piece_ko:
        print(f'  림스키 살탄 row 이미 존재 (rank {existing_with_piece_ko[0]["rank"]}) — skip')
    else:
        max_rank = max(int(r['rank']) for r in rows)
        max_base_rank = max(int(r['base_rank']) for r in rows)
        new_row = {
            'rank': str(max_rank + 1),
            'base_rank': str(max_base_rank + 1),
            **NEW_ROW,
        }
        rows.append(new_row)
        new_row_added = True
        print(f'  새 row 등재: rank {new_row["rank"]} base_rank {new_row["base_rank"]} | {NEW_ROW["piece_ko"]}')

    print()
    print(f'backfill applied: {applied}')
    print(f'backfill skipped (already correct): {skipped}')
    print(f'new row added: {new_row_added}')
    print(f'total rows: {len(rows)}')

    # utf-8-sig (BOM 보존)
    with open(CSV_PATH, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f'wrote {CSV_PATH}')


if __name__ == '__main__':
    main()
