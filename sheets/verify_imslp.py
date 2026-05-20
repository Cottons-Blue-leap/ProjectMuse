"""IMSLP work page batch verify + Full Scores (Complete) file ID 추출."""
import csv
import re
import sys
import io
import urllib.request
import urllib.parse
import gzip
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

CSV_PATH = Path(r'C:/Users/user/Desktop/myProject/Project_Muse/planning/candidate_master.csv')
OUT_CSV = Path(r'C:/Users/user/Desktop/myProject/Project_Muse/planning/candidate_master.csv.tmp')
CACHE_DIR = Path(r'C:/Users/user/Desktop/myProject/Project_Muse/sheets/_cache')
CACHE_DIR.mkdir(exist_ok=True)

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'

def fetch(url, priority):
    cache = CACHE_DIR / f'p{priority:03d}.html'
    if cache.exists() and cache.stat().st_size > 10000:
        return cache.read_text(encoding='utf-8', errors='replace'), 200
    # IRI → URI: percent-encode non-ASCII path/query
    try:
        parts = urllib.parse.urlsplit(url)
        encoded_path = urllib.parse.quote(parts.path, safe="/:%(),'")
        encoded_query = urllib.parse.quote(parts.query, safe="=&%")
        url = urllib.parse.urlunsplit((parts.scheme, parts.netloc, encoded_path, encoded_query, parts.fragment))
    except Exception:
        pass
    req = urllib.request.Request(url, headers={
        'User-Agent': UA,
        'Accept-Encoding': 'gzip',
        'Accept': 'text/html,application/xhtml+xml',
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            if resp.headers.get('Content-Encoding') == 'gzip':
                data = gzip.decompress(data)
            html = data.decode('utf-8', errors='replace')
            status = resp.status
            cache.write_text(html, encoding='utf-8')
            return html, status
    except urllib.error.HTTPError as e:
        return '', e.code
    except Exception as e:
        return f'ERR: {e}', -1

def parse_full_scores_complete(html):
    """Find 'Full Scores' or 'Scores' h3 → 'Complete'/'Selections' h4 (or section body) → file IDs."""
    # Try Full_Scores → Scores → Scores_and_Parts → Vocal_Scores → Sheet_Music h2 fallback
    fs_match = None
    for anchor in ('Full_Scores', 'Scores', 'Scores_and_Parts', 'Vocal_Scores'):
        fs_match = re.search(rf'<h3[^>]*>.*?id="{anchor}".*?</h3>', html, re.DOTALL)
        if fs_match:
            break
    if not fs_match:
        # Last fallback: Sheet_Music h2 → next h2
        sm_match = re.search(r'<h2[^>]*>.*?id="Sheet_Music".*?</h2>', html, re.DOTALL)
        if not sm_match:
            return [], None, 'no_sheet_music'
        sm_start = sm_match.end()
        rest_sm = html[sm_start:]
        next_h2 = re.search(r'<h2[^>]*>', rest_sm)
        outer = rest_sm[:next_h2.start() if next_h2 else len(rest_sm)]
        start = sm_start
        section = outer
        blocks = re.split(r'<div[^>]*id="IMSLP(\d+)"', section)
        entries = []
        for i in range(1, len(blocks), 2):
            fid = blocks[i]
            body = blocks[i+1] if i+1 < len(blocks) else ''
            is_manuscript = bool(re.search(r'\bManuscript\b', body[:3000], re.IGNORECASE)) and not re.search(r'\bManuscript\s*typeset\b', body[:3000], re.IGNORECASE)
            entries.append((fid, is_manuscript))
        if not entries:
            return [], None, 'no_imslp_ids_sheet_music'
        recommended = None
        for fid, is_ms in entries:
            if not is_ms:
                recommended = fid
                break
        if recommended is None:
            recommended = entries[0][0]
        all_ids = ';'.join('#' + fid for fid, _ in entries[:30])
        return entries, ('#' + recommended), all_ids
    start = fs_match.end()
    rest = html[start:]
    # Cap to next h2 or h3 sibling (don't escape the parent section)
    next_h3 = re.search(r'<h[23][^>]*>', rest)
    section_outer_end = next_h3.start() if next_h3 else len(rest)
    outer = rest[:section_outer_end]
    # Within outer: first try Complete h4, then Selections, else outer itself
    complete_match = re.search(r'<h4[^>]*>.*?id="Complete(?:_\d+)?".*?</h4>', outer, re.DOTALL)
    if complete_match:
        sec_start = complete_match.end()
        next_h = re.search(r'<h[234][^>]*>', outer[sec_start:])
        sec_end = sec_start + next_h.start() if next_h else len(outer)
        section = outer[sec_start:sec_end]
    else:
        sel_match = re.search(r'<h4[^>]*>.*?id="Selections(?:_\d+)?".*?</h4>', outer, re.DOTALL)
        if sel_match:
            sec_start = sel_match.end()
            next_h = re.search(r'<h[234][^>]*>', outer[sec_start:])
            sec_end = sec_start + next_h.start() if next_h else len(outer)
            section = outer[sec_start:sec_end]
        else:
            section = outer
    blocks = re.split(r'<div[^>]*id="IMSLP(\d+)"', section)
    entries = []
    for i in range(1, len(blocks), 2):
        fid = blocks[i]
        body = blocks[i+1] if i+1 < len(blocks) else ''
        is_manuscript = bool(re.search(r'\bManuscript\b', body[:3000], re.IGNORECASE)) and not re.search(r'\bManuscript\s*typeset\b', body[:3000], re.IGNORECASE)
        entries.append((fid, is_manuscript))
    if not entries:
        return [], None, 'no_imslp_ids_in_section'
    recommended = None
    for fid, is_ms in entries:
        if not is_ms:
            recommended = fid
            break
    if recommended is None:
        recommended = entries[0][0]
    all_ids = ';'.join('#' + fid for fid, _ in entries)
    return entries, ('#' + recommended), all_ids

def process(row):
    p = int(row['priority'])
    url = row['imslp_url']
    if not url or not url.startswith('http'):
        return p, None, 'no_url', 0
    html, status = fetch(url, p)
    if status != 200:
        return p, None, f'http_{status}', 0
    if len(html) < 5000:
        return p, None, 'page_too_small', len(html)
    entries, recommended, all_ids = parse_full_scores_complete(html)
    if not entries:
        return p, None, all_ids, len(html)
    return p, (recommended, all_ids), 'ok', len(html)

def main():
    rows = []
    with CSV_PATH.open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)
    targets = [r for r in rows if r['imslp_url'].startswith('http')]
    print(f'targets: {len(targets)}')
    results = {}
    with ThreadPoolExecutor(max_workers=8) as ex:
        futures = {ex.submit(process, r): r for r in targets}
        done = 0
        for fut in as_completed(futures):
            p, payload, msg, size = fut.result()
            results[p] = (payload, msg, size)
            done += 1
            if done % 10 == 0 or msg != 'ok':
                marker = 'OK' if msg == 'ok' else 'WARN'
                print(f'  [{done}/{len(targets)}] p{p} {marker} ({msg}, size={size})')
    if 'imslp_file_id_recommended' not in fieldnames:
        idx = fieldnames.index('imslp_score_id') + 1
        fieldnames.insert(idx, 'imslp_file_id_recommended')
        fieldnames.insert(idx + 1, 'imslp_file_id_all')
    for r in rows:
        p = int(r['priority'])
        r.setdefault('imslp_file_id_recommended', '')
        r.setdefault('imslp_file_id_all', '')
        if p in results:
            payload, msg, _ = results[p]
            if payload:
                r['imslp_file_id_recommended'] = payload[0]
                r['imslp_file_id_all'] = payload[1]
            else:
                r['imslp_file_id_recommended'] = f'WARN_{msg}'
                r['imslp_file_id_all'] = ''
    with OUT_CSV.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    ok = sum(1 for r in rows if r.get('imslp_file_id_recommended', '').startswith('#'))
    warn = sum(1 for r in rows if r.get('imslp_file_id_recommended', '').startswith('WARN'))
    empty = sum(1 for r in rows if not r.get('imslp_file_id_recommended', ''))
    print(f'\nFINAL: ok={ok} warn={warn} empty={empty} total={len(rows)}')
    for r in rows:
        rec = r.get('imslp_file_id_recommended', '')
        if rec.startswith('WARN'):
            print(f'  WARN p{r["priority"]} {r["piece"]}: {rec}')

if __name__ == '__main__':
    main()
