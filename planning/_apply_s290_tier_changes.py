"""s290 cycle [1/83]~[51/83] A tier review 결단 CSV 반영 (raw + retro reconstruct base).

본 script는 `_s290_review_reconstruct.md` 자료 자료 base.
source: jsonl raw extract (`6c5a4987-...jsonl` · 36곡 매칭) + retro 압축 명단 (15곡 자료) cross-check.

변경 자료 (51곡 review + 1곡 drop):
- N=1 ~ N=51: rank 34 ~ rank 84 (Tier A 83곡 중 1~51번째 rank order)
- drop: rank 101 (아베 마리아 [바흐/구노]) row 자체 delete

Tier 변경 자료 (raw 자료 ground truth · retro mismatch axis = retro 압축 결함 자료):
- S 17곡 (변경)
- A keep 16곡 (변경 X)
- B 12곡 (변경)
- C 6곡 (변경)
- 변경 합 35곡 + A keep 16 + drop 1 = 52 ✓

총 분포 변동 (s292 본 session 후 csv base):
- S: 33 + 17 = 50
- A: 81 - 35 - 1 = 45 (35곡 변경 빠짐 + rank 101 drop)
- B: 66 + 12 = 78
- C: 90 + 6 = 96
- D: 55 변동 X
- total: 325 - 1 = 324 (rank 101 delete)
"""
import csv
import shutil
from pathlib import Path

p = Path(r'C:\Users\user\Desktop\myProject\Project_Muse\planning\candidate_master.csv')
bak = p.with_suffix('.csv.bak19_s290_reconstruct')

shutil.copy2(p, bak)
print(f'backup: {bak.name}')

# rank → 새 tier 매핑 (51곡 자료 + drop 1)
# rank order 자료 자료 자료 (csv 안 Tier A 자료 자료 자료 rank order 자료 자료)
# raw + retro reconstruct base · piece_ko substring verify 박음
CHANGES = {
    # rank: (substring keyword, 새 tier)
    34: ('님로드', 'B'),
    35: ('브람스의 자장가', 'S'),
    36: ('백조', 'A'),  # keep
    37: ('검투사', 'S'),
    38: ('타이스', 'C'),
    39: ('오 사랑하는 나의 아버지', 'B'),
    40: ('알레그레토', 'C'),
    41: ('피아노 협주곡 21번 안단테', 'C'),
    42: ('비창 소나타 중 아다지오', 'A'),  # keep
    43: ('키예프의 대문', 'B'),
    44: ('카발레리아', 'A'),  # keep
    45: ('어떤 갠 날', 'C'),
    46: ('호프만', 'B'),
    47: ('사계 중 봄 2악장', 'C'),
    48: ('꽃의 이중창', 'B'),
    49: ('라흐마니노프', 'B'),
    50: ('K.545', 'A'),  # keep
    51: ('무반주 첼로 모음곡 1번 전주곡', 'S'),
    52: ('야상곡 작품 9-2', 'S'),
    53: ('어머니께', 'S'),  # 작은 별 변주곡 = K.265 「아 어머니께」
    54: ('마법사의 제자', 'A'),  # keep
    55: ('지옥의 갤럽', 'S'),
    56: ('밤의 여왕', 'S'),
    57: ('발키리', 'A'),  # keep
    58: ('차라투스트라', 'S'),
    59: ('피아노 소나타 2번 중 장송행진곡', 'A'),  # keep
    60: ('세비야의 이발사 서곡', 'A'),  # keep
    61: ('민둥산', 'A'),  # keep
    62: ('디 엔터테이너', 'S'),
    63: ('사랑의 꿈 3번', 'A'),  # keep
    64: ('헝가리 무곡 5번', 'S'),
    65: ('몰다우', 'A'),  # keep
    66: ('1812년', 'B'),
    67: ('축배의 노래', 'S'),
    68: ('아이다 중 개선행진곡', 'S'),
    69: ('라데츠키', 'S'),
    70: ('로미오와 줄리엣', 'B'),
    71: ('볼레로', 'S'),
    72: ('라크리모사', 'S'),
    73: ('예수 인류의 기쁨', 'A'),  # keep
    74: ('레베리', 'B'),
    75: ('솔베이그', 'B'),
    76: ('죽은 왕녀를 위한 파반', 'A'),  # keep
    77: ('슈텐드헨', 'A'),  # keep
    78: ('울게 하소서', 'A'),  # keep
    79: ('노래의 날개 위에', 'C'),
    80: ('평균율 클라비어곡집 1권 1번', 'S'),
    81: ('연습곡 작품 10-3', 'A'),  # keep
    82: ('아마빛 머리의 소녀', 'B'),
    83: ('트로이메라이', 'B'),
    84: ('사랑의 인사', 'S'),
}

DROP_RANK = 99  # raw extract 안 *rank 101*은 s290 시점 rank · 그 이후 renumber 박힌 자료. 현재 csv는 rank 99.
DROP_KEYWORD = '아베 마리아 (바흐/구노)'  # 슈베르트 아베 마리아 (rank 27)와 분리 axis

with p.open(encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

changes = []
mismatches = []
for r in rows:
    rk = int(r['rank'])
    pk = r['piece_ko']
    if rk in CHANGES:
        kw, new_tier = CHANGES[rk]
        if kw not in pk:
            mismatches.append((rk, kw, pk))
            continue
        old = r['popularity_tier'].strip()
        if old != 'A':
            mismatches.append((rk, f'expected old=A, actual={old}', pk))
            continue
        if old != new_tier:
            r['popularity_tier'] = new_tier
            changes.append((rk, pk, old, new_tier))
        else:
            changes.append((rk, pk, old, 'A keep'))

if mismatches:
    print('MISMATCH 자료:')
    for m in mismatches:
        print(f'  {m}')
    raise SystemExit('mismatch 자료 자료 자료 자료')

# rank 101 drop verify
drop_idx = None
for i, r in enumerate(rows):
    if int(r['rank']) == DROP_RANK:
        if DROP_KEYWORD not in r['piece_ko']:
            raise ValueError(f'rank {DROP_RANK} piece_ko mismatch: {r["piece_ko"]}')
        drop_idx = i
        break
if drop_idx is None:
    raise ValueError(f'rank {DROP_RANK} 자료 자료')
dropped = rows.pop(drop_idx)
print(f'\ndrop: rank {DROP_RANK} {dropped["piece_ko"]}')

with p.open('w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f'\n변경 자료 ({len(changes)}곡):')
keep_count = sum(1 for c in changes if c[3] == 'A keep')
change_count = len(changes) - keep_count
print(f'  변경: {change_count}곡 / A keep: {keep_count}곡')

dist = {}
for r in rows:
    t = r['popularity_tier'].strip()
    dist[t] = dist.get(t, 0) + 1
print('\nnew distribution:')
for t in ['S', 'A', 'B', 'C', 'D']:
    print(f'  {t}: {dist.get(t, 0)}')
print(f'  total: {sum(dist.values())}')
