"""s292 cycle [52/83]~[83/83] A tier review 부분 반영 (매 곡 통과 후 즉시 csv 반영 doctrine).

idempotent: 이미 통과한 row는 no-op skip (재 호출 안전).

review 통과 자료:
- rank 85 (파반 작품 50 [포레]): A → B
- rank 86 (메이플 리프 래그 [조플린]): A → S
- rank 87 (아라베스크 1번 [드뷔시]): A keep (no-op)
- rank 88 (피가로의 결혼 서곡 [모차르트]): A → S
"""
import csv
import shutil
import time
from pathlib import Path

p = Path(r'C:\Users\user\Desktop\myProject\Project_Muse\planning\candidate_master.csv')
ts = time.strftime('%H%M%S')
bak = p.with_suffix(f'.csv.bak_s292_partial_{ts}')

shutil.copy2(p, bak)
print(f'backup: {bak.name}')

CHANGES = {
    '파반 작품 50 (포레)': ('A', 'B'),
    '메이플 리프 래그 (조플린)': ('A', 'S'),
    '피가로의 결혼 서곡 (모차르트)': ('A', 'S'),
}

with p.open(encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

changes = []
skipped = []
for r in rows:
    pk = r['piece_ko'].strip()
    if pk in CHANGES:
        expected_old, new = CHANGES[pk]
        actual_old = r['popularity_tier'].strip()
        if actual_old == new:
            skipped.append((int(r['rank']), pk, actual_old))
            continue
        if actual_old != expected_old:
            raise ValueError(
                f"tier mismatch for piece_ko='{pk}': "
                f"expected old={expected_old} or new={new}, actual={actual_old}"
            )
        r['popularity_tier'] = new
        changes.append((int(r['rank']), pk, actual_old, new))

matched_pks = {c[1] for c in changes} | {s[1] for s in skipped}
missing = set(CHANGES.keys()) - matched_pks
if missing:
    raise ValueError(f'piece_ko not found in csv: {missing}')

with p.open('w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f'changes applied ({len(changes)}):')
for c in sorted(changes):
    print(f'  rank {c[0]:>3}: {c[1]}  {c[2]} -> {c[3]}')
if skipped:
    print(f'\nskipped (already at target tier, {len(skipped)}):')
    for s in sorted(skipped):
        print(f'  rank {s[0]:>3}: {s[1]}  already={s[2]}')

dist = {}
for r in rows:
    t = r['popularity_tier'].strip()
    dist[t] = dist.get(t, 0) + 1
print('\nnew distribution:')
for t in ['S', 'A', 'B', 'C', 'D']:
    print(f'  {t}: {dist.get(t, 0)}')
print(f'  total: {sum(dist.values())}')
