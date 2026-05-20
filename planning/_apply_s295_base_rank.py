"""s295 cycle (다) base_rank 컬럼 도입 + row 재배치 + rank renumber.

doctrine (코튼 결단 = (C) 옵션):
- base_rank 컬럼 추가 = bak17_s289_s_review 시점 rank (frozen)
- 기존 rank 컬럼 = 매 변경 후 sequential renumber (1~total)
- row 순서 = popularity_tier (S→A→B→C→D) 안 base_rank 오름차순

idempotent:
- 이미 base_rank 컬럼 있으면 no-op skip + 재 호출 시 row 재배치 + rank renumber만 수행
- bak17 안 piece_ko 매칭 안 되는 row (drop 1건 외) 발견 시 raise
"""
import csv
import shutil
import time
from pathlib import Path

PLANNING = Path(r'C:\Users\user\Desktop\myProject\Project_Muse\planning')
CURRENT = PLANNING / 'candidate_master.csv'
BASE = PLANNING / 'candidate_master.csv.bak17_s289_s_review'

ts = time.strftime('%H%M%S')
bak = CURRENT.with_suffix(f'.csv.bak20_s295_base_rank_{ts}')

shutil.copy2(CURRENT, bak)
print(f'backup: {bak.name}')

with BASE.open(encoding='utf-8-sig', newline='') as f:
    base_rows = list(csv.DictReader(f))
base_rank_map = {r['piece_ko'].strip(): int(r['rank']) for r in base_rows}
print(f'base mapping: {len(base_rank_map)} entries from bak17')

with CURRENT.open(encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    fieldnames = list(reader.fieldnames)
    rows = list(reader)

if 'base_rank' in fieldnames:
    print('base_rank column already exists — re-sort + renumber path only')
    has_base_rank = True
else:
    rank_idx = fieldnames.index('rank')
    fieldnames.insert(rank_idx + 1, 'base_rank')
    has_base_rank = False

unmatched = []
for r in rows:
    pk = r['piece_ko'].strip()
    if pk not in base_rank_map:
        unmatched.append(pk)
        continue
    r['base_rank'] = str(base_rank_map[pk])

if unmatched:
    raise ValueError(
        f'piece_ko not found in bak17 ({len(unmatched)}): {unmatched}'
    )

bak17_pks = set(base_rank_map.keys())
current_pks = {r['piece_ko'].strip() for r in rows}
dropped = bak17_pks - current_pks
print(f'dropped from bak17 (expected = 1, rank 99 아베 마리아 바흐/구노): {len(dropped)}')
for pk in sorted(dropped):
    print(f'  - {pk} (bak17 rank={base_rank_map[pk]})')

TIER_ORDER = {'S': 0, 'A': 1, 'B': 2, 'C': 3, 'D': 4}
rows.sort(key=lambda r: (TIER_ORDER[r['popularity_tier'].strip()], int(r['base_rank'])))

for i, r in enumerate(rows, start=1):
    r['rank'] = str(i)

with CURRENT.open('w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

dist = {}
for r in rows:
    t = r['popularity_tier'].strip()
    dist[t] = dist.get(t, 0) + 1
print('\nnew distribution:')
for t in ['S', 'A', 'B', 'C', 'D']:
    print(f'  {t}: {dist.get(t, 0)}')
print(f'  total: {sum(dist.values())}')

print('\ntier transitions (row#, tier, new rank, base_rank, piece_ko):')
prev = None
for i, r in enumerate(rows, start=1):
    t = r['popularity_tier'].strip()
    if t != prev:
        print(f'  row {i:>3}: tier={t}  rank={r["rank"]}  base_rank={r["base_rank"]}  piece_ko={r["piece_ko"][:40]}')
        prev = t

print('\ns292 partial apply 4건 sample verify:')
samples = ['파반 작품 50 (포레)', '메이플 리프 래그 (조플린)', '아라베스크 1번 (드뷔시)', '피가로의 결혼 서곡 (모차르트)']
for pk in samples:
    for r in rows:
        if r['piece_ko'].strip() == pk:
            print(f'  rank={r["rank"]:>3}  base_rank={r["base_rank"]:>3}  tier={r["popularity_tier"]}  {pk}')
            break
