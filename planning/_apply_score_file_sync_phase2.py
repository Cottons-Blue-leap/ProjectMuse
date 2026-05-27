"""score_file column sync phase 2 (s367 cycle).

목적:
  - Phase 1 (`_apply_score_file_sync.py`) 적용 후 폴더 PDF가 *FullName* 양식으로 추가 표준화됨 자가 catch
  - 27 dangling short-form → 폴더 안 long-form 1:1 매핑 (자동 추출 통과)
  - 30 row 영향 (일부 short-form 자료 → 다중 row reference)

idempotent. 이미 long-form이면 skip. 1:1 매핑이라 piece_ko 매칭 불필요 (score_file string 직접 replace).
재실행 = side-effect 0.
"""

import csv
import shutil
import sys
from pathlib import Path

CSV_PATH = Path('candidate_master.csv')
BACKUP_PATH = Path('candidate_master.csv.bak_s367_score_file_sync_phase2')

# score_file string 1:1 매핑 (short → long full-name)
RENAME_MAP = {
    '그리그_피아노 협주곡 A단조 작품 16.pdf': '에드바르 그리그_피아노 협주곡 A단조 작품 16.pdf',
    '뒤카_마법사의 제자.pdf': '폴 뒤카_마법사의 제자.pdf',
    '드보르작_슬라브 무곡.pdf': '안토닌 드보르작_슬라브 무곡.pdf',
    '드보르작_유모레스크.pdf': '안토닌 드보르작_유모레스크.pdf',
    '드뷔시_달빛.pdf': '클로드 드뷔시_달빛.pdf',
    '드뷔시_아라베스크.pdf': '클로드 드뷔시_아라베스크.pdf',
    '드뷔시_전주곡 1권 L.117_1-6.pdf': '클로드 드뷔시_전주곡 1권 L.117_1-6.pdf',
    '드뷔시_전주곡 1권 L.117_7-12.pdf': '클로드 드뷔시_전주곡 1권 L.117_7-12.pdf',
    '들리브_라크메 중 꽃의 이중창.pdf': '레오 들리브_라크메 중 꽃의 이중창.pdf',
    '라벨_볼레로.pdf': '모리스 라벨_볼레로.pdf',
    '로시니_세비야의 이발사 서곡.pdf': '조아키노 로시니_세비야의 이발사 서곡.pdf',
    '로시니_윌리엄 텔 서곡_새벽.pdf': '조아키노 로시니_윌리엄 텔 서곡_새벽.pdf',
    '리스트_라 캄파넬라.pdf': '프란츠 리스트_라 캄파넬라.pdf',
    '리스트_사랑의 꿈.pdf': '프란츠 리스트_사랑의 꿈.pdf',
    '리스트_헝가리 광시곡 2번.pdf': '프란츠 리스트_헝가리 광시곡 2번.pdf',
    '멘델스존_결혼 행진곡.pdf': '펠릭스 멘델스존_결혼 행진곡.pdf',
    '멘델스존_무언가 중 봄의 노래.pdf': '펠릭스 멘델스존_무언가 중 봄의 노래.pdf',
    '무소르그스키_민둥산의 하룻밤.pdf': '모데스트 무소륵스키_민둥산의 하룻밤.pdf',
    '바그너_로엔그린 중 혼례의 합창.pdf': '리하르트 바그너_로엔그린 중 혼례의 합창.pdf',
    '바그너_발키리의 기행.pdf': '리하르트 바그너_발키리의 기행.pdf',
    '바그너_탄호이저 서곡.pdf': '리하르트 바그너_탄호이저 서곡.pdf',
    '보로딘_폴로베츠인의 춤.pdf': '알렉산드르 보로딘_폴로베츠인의 춤.pdf',
    '쇼팽_피아노 소나타 2번.pdf': '프레데리크 쇼팽_피아노 소나타 2번.pdf',
    '에리크 사티_짐노페디.pdf': '에릭 사티_짐노페디.pdf',
    '주페_경기병 서곡.pdf': '프란츠 폰 주페_경기병 서곡.pdf',
    '푸치니_공주는 잠 못 이루고.pdf': '자코모 푸치니_공주는 잠 못 이루고.pdf',
    '푸치니_노래에 살고, 사랑에 살고.pdf': '자코모 푸치니_노래에 살고, 사랑에 살고.pdf',
}


def main():
    sys.stdout.reconfigure(encoding='utf-8')

    if not CSV_PATH.exists():
        print(f'ERROR: {CSV_PATH} not found')
        sys.exit(1)

    # 폴더 안 PDF set verify 모든 target long-form 실존
    pdfs = set(p.name for p in Path('candidates_opus').glob('*.pdf'))
    missing_targets = [t for t in RENAME_MAP.values() if t not in pdfs]
    if missing_targets:
        print('ABORT: 다음 target long-form PDF 폴더에 없음:')
        for m in missing_targets:
            print(f'  {m}')
        sys.exit(2)
    print(f'verify 통과: 모든 {len(RENAME_MAP)} target long-form PDF 폴더 실존')
    print()

    if not BACKUP_PATH.exists():
        shutil.copy(CSV_PATH, BACKUP_PATH)
        print(f'backup created: {BACKUP_PATH}')

    with open(CSV_PATH, encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    applied = 0
    skipped = 0
    for r in rows:
        sf = r['score_file']
        if sf in RENAME_MAP:
            new_sf = RENAME_MAP[sf]
            r['score_file'] = new_sf
            applied += 1
            print(f'  rank {r["rank"]:>3} | {r["piece_ko"][:35]:<35} | "{sf}" → "{new_sf}"')
        elif sf in RENAME_MAP.values():
            skipped += 1

    print()
    print(f'applied: {applied}')
    print(f'skipped (already long-form): {skipped}')

    # utf-8-sig (BOM 보존) — Excel cp949 오해석 한글 깨짐 방지
    with open(CSV_PATH, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f'wrote {CSV_PATH}')


if __name__ == '__main__':
    main()
