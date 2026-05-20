"""s320 PDF 매칭 적용 — candidates_opus 78 PDF 자체엔 csv score_file column update.

자료 axis:
  - auto-match 14건 (자가 분석 base · _s320_pdf_matching_analysis.txt 자료 base)
  - fix 2건 (rank 110 + rank 177 자체엔 PDF filename 자체엔 정확 자료 자체엔 정정)
  - issue 1건 (살탄 황제의 이야기 Op.57.pdf 자체엔 *왕벌의 비행* parent source · rank 18 자체엔 *왕벌의 비행(출처표기필수).pdf* keep · 본 PDF 자체엔 unmatched keep · 출처표기 의무 자료 base)

idempotent path. 본 script 자체엔 매번 실행해도 동일 결과 자료 base.
"""

import csv
from pathlib import Path


PDF_DIR = Path('candidates_opus')
CSV_PATH = Path('candidate_master.csv')
RANK_COL = '﻿rank'

# auto-match 자료 (rank → score_file)
AUTO_MATCH = {
    18: '림스키코르사코프_왕벌의 비행(출처표기필수).pdf',
    19: '바흐_토카타 D단조 BWV 565.pdf',
    20: '멘델스존_결혼 행진곡.pdf',
    21: '루트비히 판 베토벤_엘리제를 위하여.pdf',
    22: '루트비히 판 베토벤_교향곡 5번 중 운명.pdf',
    23: '볼프강 아마데우스 모차르트_터키 행진곡.pdf',
    24: '바그너_로엔그린 중 혼례의 합창.pdf',
    25: '푸치니_공주는 잠 못 이루고.pdf',
    26: '헨델_할렐루야.pdf',
    27: '슈베르트_아베 마리아.pdf',
    28: '엘가_위풍당당 행진곡.pdf',
    30: '생상스_죽음의 무도.pdf',
    31: '요한 슈트라우스 2세_봄의 소리 왈츠 Op. 410.pdf',
    269: '로시니_윌리엄 텔 서곡_새벽.pdf',
}

# fix 자료 (rank → 정확 PDF filename)
FIX_MATCH = {
    110: '안토니오 비발디_사계_겨울.pdf',           # 옛: '비발디_사계_겨울.pdf' (PDF X)
    177: '요하네스 브람스_교향곡 3번.pdf',           # 옛: '브람스_교향곡 3번.pdf' (PDF X)
}


def main():
    pdfs = set(p.name for p in PDF_DIR.glob('*.pdf'))

    # PDF 자체엔 실제 존재 verify
    all_changes = {**AUTO_MATCH, **FIX_MATCH}
    for rank, pdf in all_changes.items():
        if pdf not in pdfs:
            print(f'[ERROR] rank {rank}: PDF "{pdf}" 자체엔 폴더 안 X')
            return

    # csv read
    with open(CSV_PATH, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    changes = []
    for r in rows:
        rank = int(r[RANK_COL])
        if rank in all_changes:
            old = r['score_file']
            new = all_changes[rank]
            if old != new:
                r['score_file'] = new
                changes.append((rank, r['piece_ko'], old, new))

    with open(CSV_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f'\napplied {len(changes)} changes')
    for rank, piece_ko, old, new in changes:
        print(f'  rank {rank}: "{old}" -> "{new}"')

    # 검증 — 최종 매칭 state
    matched = [r for r in rows if r['score_file'].strip() and r['score_file'].strip() != '-']
    verified = [r for r in matched if r['score_file'] in pdfs]

    print(f'\n## final state')
    print(f'csv rows: {len(rows)}')
    print(f'matched: {len(matched)}')
    print(f'verified (PDF exists): {len(verified)}')
    print(f'PDF total: {len(pdfs)}')

    used_pdfs = set(r['score_file'] for r in verified)
    unused_pdfs = sorted(pdfs - used_pdfs)
    print(f'used PDFs: {len(used_pdfs)}')
    print(f'unused PDFs: {len(unused_pdfs)}')
    for u in unused_pdfs:
        print(f'  unused: {u}')


if __name__ == '__main__':
    main()
