"""신규 candidates_opus PDF 감사 (s336).

목적:
  - 폴더 안 PDF vs csv score_file 매칭 state 비교
  - unmatched PDF 식별 (폴더엔 있는데 어느 row도 참조 X)
  - 각 unmatched PDF에 대해 piece_ko 기준 fuzzy 후보 제시 (기존 row 매칭 vs 신규 후보 분류 보조)
  - 오늘(2026-05-20) 추가분 표기

read-only. csv 변경 X.
"""

import csv
import re
import sys
import datetime as dt
from pathlib import Path

PDF_DIR = Path('candidates_opus')
CSV_PATH = Path('candidate_master.csv')
OUT_PATH = Path('_audit_new_pdfs_out.txt')

_OUT_LINES = []


def emit(line=''):
    _OUT_LINES.append(line)


def normalize(s: str) -> str:
    """비교용 정규화: 괄호 안 작곡가 제거 + 공백/문장부호 제거 + 소문자."""
    s = s.split('(')[0]  # piece_ko 안 작곡가 괄호 제거
    s = re.sub(r'\.pdf$', '', s, flags=re.IGNORECASE)
    s = re.sub(r'[\s_,.\-·:;()\[\]]', '', s)
    return s.lower()


def pdf_title_core(name: str) -> str:
    """PDF filename 안 작곡가_ prefix 제거 후 core title."""
    stem = re.sub(r'\.pdf$', '', name, flags=re.IGNORECASE)
    # 첫 '_' 뒤가 title (작곡가_제목)
    parts = stem.split('_', 1)
    title = parts[1] if len(parts) > 1 else parts[0]
    return title


def main():
    pdfs = list(PDF_DIR.glob('*.pdf'))
    pdf_names = set(p.name for p in pdfs)

    today = dt.date(2026, 5, 20)
    today_pdfs = set(
        p.name for p in pdfs
        if dt.date.fromtimestamp(p.stat().st_mtime) == today
    )

    with open(CSV_PATH, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    referenced = set(
        r['score_file'].strip() for r in rows
        if r['score_file'].strip() and r['score_file'].strip() != '-'
    )

    # row 정규화 인덱스 (정규화 piece_ko/piece -> row)
    row_index = []
    for r in rows:
        row_index.append({
            'rank': r['rank'],
            'tier': r['popularity_tier'],
            'piece_ko': r['piece_ko'],
            'piece': r['piece'],
            'score_file': r['score_file'].strip(),
            'norm_ko': normalize(r['piece_ko']),
            'norm_en': normalize(r['piece']),
        })

    emit('## 전체 state')
    emit(f'PDF total: {len(pdf_names)}')
    emit(f'csv rows: {len(rows)}')
    emit(f'referenced (score_file 채워진 row): {len(referenced)}')
    verified = referenced & pdf_names
    emit(f'verified (PDF 실존): {len(verified)}')
    dangling = sorted(referenced - pdf_names)
    emit(f'dangling (csv 참조하는데 PDF 없음): {len(dangling)}')
    for d in dangling:
        emit(f'  dangling: {d}')

    unmatched = sorted(pdf_names - referenced)
    emit(f'\n## unmatched PDF (폴더엔 있는데 csv 미참조): {len(unmatched)}')
    emit(f'   (이 중 오늘 추가분: {len(set(unmatched) & today_pdfs)})')

    emit('\n## unmatched 각각 fuzzy 후보 (기존 row 매칭 가능성)')
    for pdf in unmatched:
        core = pdf_title_core(pdf)
        ncore = normalize(core)
        tag = ' [오늘추가]' if pdf in today_pdfs else ''
        # 후보: 정규화 substring 양방향 포함
        cands = []
        for ri in row_index:
            nk = ri['norm_ko']
            ne = ri['norm_en']
            if not ncore:
                continue
            score = 0
            if ncore in nk or nk in ncore:
                score = max(score, len(set(ncore) & set(nk)))
            # 토큰 일부 포함 (4자 이상 공통)
            if len(ncore) >= 3 and (ncore[:4] in nk or (len(nk) >= 4 and nk[:4] in ncore)):
                score = max(score, 1)
            if score > 0:
                cands.append((score, ri))
        cands.sort(key=lambda x: -x[0])
        emit(f'\n  PDF: {pdf}{tag}')
        emit(f'       core="{core}"')
        if cands:
            for score, ri in cands[:3]:
                sf = f' [score_file 이미: {ri["score_file"]}]' if ri['score_file'] else ' [score_file 빔]'
                emit(f'       -> rank {ri["rank"]} [{ri["tier"]}] {ri["piece_ko"]}{sf}')
        else:
            emit('       -> (NO MATCH · 신규 후보 가능성)')


if __name__ == '__main__':
    main()
    OUT_PATH.write_text('\n'.join(_OUT_LINES), encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    print(f'wrote {OUT_PATH} ({len(_OUT_LINES)} lines)')
