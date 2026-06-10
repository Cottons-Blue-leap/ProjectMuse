# -*- coding: utf-8 -*-
import json
base = r'C:\Users\user\Desktop\myProject\Project_Muse\works\handel_lascia_chio_pianga\music\renders'
for tag in ['test3', 'test4']:
    d = json.load(open(rf'{base}\{tag}_vocal_analysis.json', encoding='utf-8-sig'))
    hi = [n for n in d['longest_notes'] if n['f0_Hz'] > 340]
    print(tag, '| soprano-range notes in top12:', len(hi))
    for n in hi:
        print(f"  t={n['t']}s f0={n['f0_Hz']}Hz dur={n['dur_s']}s depth={n['vib_halfdepth_cents']}c rate={n['vib_rate_Hz']}Hz")
