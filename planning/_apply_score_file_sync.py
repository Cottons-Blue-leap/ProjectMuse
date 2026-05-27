"""score_file column 일괄 sync (s367 cycle).

목적:
  - Cat A: short→long form rename (27 row)
  - Cat B: score_file 빈 row backfill (19 row)
  - Cat C: ambiguous backfill (코튼 *후보곡 포함 시 등재* doctrine · multi-row mapping 박음)

idempotent. 이미 정답이면 skip. piece_ko exact 매칭으로 safety.
재실행 = side-effect 0.

cycle history:
  - 2026-05-27 (s367) 신축: 144 PDF audit base · short→long convention 통합 + backfill
"""

import csv
import shutil
import sys
from pathlib import Path

CSV_PATH = Path('candidate_master.csv')
BACKUP_PATH = Path('candidate_master.csv.bak_s367_score_file_sync')

# (rank, expected piece_ko 부분 안전 match, new_score_file)
# piece_ko exact 매칭 의무. piece_ko 변경 시 본 script 다시 보정 필요.
CHANGES = [
    # === Cat A: RENAME (short→long form · 27 row) ===
    ('15', '카르멘 중 하바네라 (비제)', '조르주 비제_카르멘 중 하바네라.pdf'),
    ('26', '할렐루야 합창 (헨델 - 메시아)', '게오르크 프리드리히 헨델_할렐루야.pdf'),
    ('27', '아베 마리아 (슈베르트)', '프란츠 슈베르트_아베 마리아.pdf'),
    ('28', '위풍당당 행진곡 1번 (엘가)', '에드워드 엘가_위풍당당 행진곡.pdf'),
    ('30', '죽음의 무도 (생상스)', '카미유 생상스_죽음의 무도.pdf'),
    ('36', '야상곡 작품 9-2 (쇼팽)', '프레데리크 쇼팽_녹턴 op.9.pdf'),
    ('38', '지옥의 갤럽 (캉캉) (오펜바흐)', '자크 오펜바흐_지옥의 갤럽 (캉캉).pdf'),
    ('41', '디 엔터테이너 (조플린)', '스콧 조플린_ 디 엔터테이너.pdf'),
    ('43', '라 트라비아타 중 「축배의 노래」 (베르디)', '주세페 베르디_라 트라비아타 중 축배의 노래.pdf'),
    ('44', '아이다 중 개선행진곡 (베르디)', '주세페 베르디_아이다 중 개선행진곡.pdf'),
    ('53', '강아지 왈츠 (1분 왈츠) 작품 64-1 (쇼팽)', '프레데리크 쇼팽_강아지 왈츠.pdf'),
    ('54', '마왕 D.328 (슈베르트)', '프란츠 슈베르트_마왕.pdf'),
    ('57', '피터와 늑대 작품 67 주제 (프로코피예프)', '세르게이 프로코피예프_피터와 늑대.pdf'),
    ('62', '리골레토 중 「여자의 마음」 (베르디)', '주세페 베르디_리골레토.pdf'),
    ('64', '카르멘 중 투우사의 노래 (비제)', '조르주 비제_카르멘 중 투우사의 노래.pdf'),
    ('67', '카르멘 서곡 (비제)', '조르주 비제_카르멘 서곡.pdf'),
    ('68', '송어 D.550 (슈베르트)', '프란츠 슈베르트_송어.pdf'),
    ('70', '왈츠 1번 내림 마장조 작품 18 (쇼팽)', '프레데리크 쇼팽_왈츠 1번 내림 마장조 작품 18.pdf'),
    ('72', '군대 행진곡 D.733 1번 (슈베르트)', '프란츠 슈베르트_군대 행진곡 D.733.pdf'),
    ('73', '베르디 레퀴엠 중 「진노의 날」', '주세페 베르디_레퀴엠.pdf'),
    ('85', '몰다우 (블타바) (스메타나)', '베드르지흐 스메타나_블타바 중 몰다우.pdf'),
    ('88', '세레나데 (슈베르트 - 「슈텐드헨」)', '프란츠 슈베르트_백조의 노래.pdf'),
    ('89', '리날도 중 「울게 하소서」 (헨델)', '게오르크 프리드리히 헨델_울게 하소서.pdf'),
    ('90', '연습곡 작품 10-3 「이별」 (쇼팽)', '프레데리크 쇼팽_에튀드 op.10.pdf'),
    ('251', '세르세 중 「옴브라 마이 푸」 (헨델)', '게오르크 프리드리히 헨델_옴브라 마이 푸.pdf'),
    ('306', '리골레토 중 「그리운 이름이여」 (베르디)', '주세페 베르디_리골레토.pdf'),
    ('307', '베르디 레퀴엠 중 「나를 구하소서」', '주세페 베르디_레퀴엠.pdf'),

    # === Cat B: BACKFILL CLEAR (score_file 빈 row · 19 row) ===
    ('91', '아라베스크 1번 (드뷔시)', '드뷔시_아라베스크.pdf'),
    ('92', '탄호이저 서곡 (바그너)', '바그너_탄호이저 서곡.pdf'),
    ('93', '마술피리 서곡 (모차르트)', '볼프강 아마데우스 모차르트_마술피리 서곡.pdf'),
    ('95', '자장가 D.498 (슈베르트)', '프란츠 슈베르트_자장가.pdf'),
    ('96', '겨울바람 에튀드 작품 25-11 (쇼팽)', '프레데리크 쇼팽_에튀드 op.25.pdf'),
    ('97', '왈츠 작품 64-2 C샵 단조 (쇼팽)', '프레데리크 쇼팽_왈츠 op.64.pdf'),
    ('98', '경기병 서곡 (주페)', '주페_경기병 서곡.pdf'),
    ('106', '차이콥스키 피아노 협주곡 1번 도입부', '차이코프스키_피아노 협주곡 1번.pdf'),
    ('113', '피치카토 폴카 (요한 슈트라우스 2세)', '요한 슈트라우스 2세_피치카토 폴카.pdf'),
    ('114', '아스투리아스 (전설) (알베니스)', '이사크 알베니스_스페인 모음곡 1집.pdf'),
    ('115', '환상 즉흥곡 작품 66 (쇼팽)', '프레데리크 쇼팽_즉흥환상곡.pdf'),
    ('119', '황제 왈츠 작품 437 (요한 슈트라우스 2세)', '요한 슈트라우스 2세_황제 왈츠.pdf'),
    ('120', '교향곡 3번 「오르간」 작품 78 피날레 (생상스)', '카미유 생상스_교향곡 3번 오르간.pdf'),
    ('123', '찌고이너바이젠 작품 20 (사라사테)', '파블로 데 사라사테_찌고이너바이젠 작품 20.pdf'),
    ('124', '피아노 협주곡 A단조 작품 16 1악장 (그리그)', '그리그_피아노 협주곡 A단조 작품 16.pdf'),
    ('125', '교향곡 94번 「놀람」 2악장 (하이든)', '요제프 하이든_교향곡 94번 놀람.pdf'),
    ('139', '일 트로바토레 중 「대장간 합창」 (베르디)', '주세페 베르디_일 트로바토레.pdf'),
    ('163', '혁명 에튀드 작품 10-12 (쇼팽)', '프레데리크 쇼팽_에튀드 op.10.pdf'),
    ('315', '그라나다 (수이트 에스파뇨라 작품 47-1) (알베니스)', '이사크 알베니스_스페인 모음곡 1집.pdf'),

    # === Cat C: AMBIGUOUS BACKFILL (코튼 *후보곡 포함 시 등재* doctrine · 7 row · multi-row mapping) ===
    # 홀스트_행성.pdf (전곡) → 목성·화성 2 row
    ('118', '행성 중 「목성, 즐거움을 가져오는 자」 작품 32 (홀스트)', '구스타브 시어도어 홀스트_행성.pdf'),
    ('218', '행성 중 「화성, 전쟁을 가져오는 자」 작품 32 (홀스트)', '구스타브 시어도어 홀스트_행성.pdf'),
    # 드보르작_슬라브 무곡.pdf (모음집) → 3 row
    ('116', '슬라브 무곡 작품 46-1 (드보르자크)', '드보르작_슬라브 무곡.pdf'),
    ('215', '슬라브 무곡 작품 46-8 (드보르자크)', '드보르작_슬라브 무곡.pdf'),
    ('216', '슬라브 무곡 작품 72-2 (드보르자크)', '드보르작_슬라브 무곡.pdf'),
    # 바흐_브란덴부르크 협주곡 3번.pdf → rank 129 (3번 1악장)
    ('129', '브란덴부르크 협주곡 3번 1악장 BWV 1048 (바흐)', '요한 제바스티안 바흐_브란덴부르크 협주곡 3번.pdf'),
]


def main():
    sys.stdout.reconfigure(encoding='utf-8')

    if not CSV_PATH.exists():
        print(f'ERROR: {CSV_PATH} not found')
        sys.exit(1)

    if not BACKUP_PATH.exists():
        shutil.copy(CSV_PATH, BACKUP_PATH)
        print(f'backup created: {BACKUP_PATH}')
    else:
        print(f'backup exists, skip: {BACKUP_PATH}')

    with open(CSV_PATH, encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    changes_dict = {}
    for rank, piece_ko, new_sf in CHANGES:
        changes_dict.setdefault(rank, []).append((piece_ko, new_sf))

    applied = 0
    skipped_same = 0
    not_found = []
    piece_mismatch = []

    for r in rows:
        if r['rank'] in changes_dict:
            for expected_pk, new_sf in changes_dict[r['rank']]:
                if r['piece_ko'] != expected_pk:
                    piece_mismatch.append(
                        f'rank {r["rank"]} | csv=\"{r["piece_ko"]}\" vs expected=\"{expected_pk}\"'
                    )
                    continue
                if r['score_file'] == new_sf:
                    skipped_same += 1
                else:
                    old_sf = r['score_file']
                    r['score_file'] = new_sf
                    applied += 1
                    print(f'  rank {r["rank"]} | {r["piece_ko"][:40]}... | "{old_sf}" -> "{new_sf}"')

    # not_found: changes_dict 안 rank가 csv에 없는 경우
    csv_ranks = set(r['rank'] for r in rows)
    for rank in changes_dict:
        if rank not in csv_ranks:
            not_found.append(rank)

    print()
    print(f'applied: {applied}')
    print(f'skipped (already correct): {skipped_same}')
    print(f'piece_ko mismatch: {len(piece_mismatch)}')
    for m in piece_mismatch:
        print(f'  {m}')
    print(f'rank not found in csv: {not_found}')

    if piece_mismatch:
        print('ABORT: piece_ko mismatch — csv 변경 X. CHANGES dict 정정 후 재실행.')
        sys.exit(2)

    # utf-8-sig (BOM 보존) — Excel cp949 오해석 한글 깨짐 방지
    with open(CSV_PATH, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f'wrote {CSV_PATH}')


if __name__ == '__main__':
    main()
