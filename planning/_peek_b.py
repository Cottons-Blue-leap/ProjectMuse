# -*- coding: utf-8 -*-
import csv
from pathlib import Path

p = Path(r'C:\Users\user\Desktop\myProject\Project_Muse\planning\candidate_master.csv')
with p.open(encoding='utf-8-sig', newline='') as f:
    rows = list(csv.DictReader(f))

for r in rows:
    rk = int(r['rank'])
    if 106 <= rk <= 106:
        print(f"rank={rk} base_rank={r['base_rank']} piece_ko={r['piece_ko']}")
        print(f"piece={r['piece']}")
        print(f"period={r['period']}")
