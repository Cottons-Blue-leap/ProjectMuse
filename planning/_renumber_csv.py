"""candidate_master.csv row 재배치 + rank 컬럼 1~N sequential renumber.

doctrine:
- popularity_tier (S→A→B→C→D) 안 base_rank 오름차순 정렬.
- rank 컬럼 = 1~N sequential renumber (변경 후 row 순서 정합).
- base_rank 컬럼 = frozen (변경 X · s289 기준 자료 keep).
- cycle-agnostic + 재활용 양식. cycle 끝 batch apply step.
- backup 폐기 (idempotent · 결함 시 자가 자료 복구 path 강).
- idempotent: 이미 정렬 통과 시 no-op (rank 컬럼 변경 X).

호출 양식: cycle 안 매 곡 결단 통과 후 마지막에 1회 호출 (또는 매 호출 안전).
"""
import csv
from pathlib import Path

p = Path(r'C:\Users\user\Desktop\myProject\Project_Muse\planning\candidate_master.csv')

TIER_ORDER = ['S', 'A', 'B', 'C', 'D']

with p.open(encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

before_ranks = {r['piece_ko'].strip(): int(r['rank']) for r in rows}

rows.sort(key=lambda r: (TIER_ORDER.index(r['popularity_tier'].strip()), int(r['base_rank'])))

changes = 0
for i, r in enumerate(rows, 1):
    new_rank = str(i)
    if r['rank'] != new_rank:
        changes += 1
    r['rank'] = new_rank

with p.open('w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f'rows: {len(rows)}')
print(f'rank changes: {changes}')

dist = {}
for r in rows:
    t = r['popularity_tier'].strip()
    dist[t] = dist.get(t, 0) + 1
print(f'\ndistribution:')
for t in TIER_ORDER:
    print(f'  {t}: {dist.get(t, 0)}')
print(f'  total: {sum(dist.values())}')

print(f'\ntier boundaries (rank range per tier):')
for t in TIER_ORDER:
    t_rows = [r for r in rows if r['popularity_tier'].strip() == t]
    if t_rows:
        ranks = [int(r['rank']) for r in t_rows]
        print(f'  {t}: rank {min(ranks):>3} ~ {max(ranks):>3}  ({len(t_rows)} rows)')

moved = [(pk, before_ranks[pk], int(r['rank'])) for r in rows for pk in [r['piece_ko'].strip()] if before_ranks.get(pk) != int(r['rank'])]
if moved:
    print(f'\nrow moves ({len(moved)} rows):')
    for pk, before, after in sorted(moved, key=lambda x: x[1])[:10]:
        print(f'  rank {before:>3} -> {after:>3}: {pk}')
    if len(moved) > 10:
        print(f'  ... and {len(moved) - 10} more')
