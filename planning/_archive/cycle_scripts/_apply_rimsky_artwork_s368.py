"""s368 — Fill artwork columns for Rimsky-Korsakov "Three Wonders" row.

The row was added in s368 (rank 358, base_rank 360) with score_file + imslp_url
but artwork columns empty. This script fills 6 artwork columns using Ivan Bilibin's
1905 Tale of Tsar Saltan illustration cycle (PD: Bilibin d.1942, life+70=2013).

Doctrine (s368):
- piece_ko exact match (safety)
- utf-8-sig read/write (BOM preserved)
- backup before write
- verify before commit
- idempotent (safe to re-run; checks if columns already filled)
"""
import csv
import sys
import shutil
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

CSV_PATH = Path(__file__).parent / "candidate_master.csv"
BACKUP_SUFFIX = ".bak_s368_rimsky_artwork"

# piece_ko exact match (full Korean string from the row)
TARGET_PIECE_KO = "살탄 황제의 이야기 중 「세 가지 기적」 작품 57 (림스키-코르사코프)"

# Artwork patch (6 columns)
ARTWORK = {
    "artwork_title": "Tale of Tsar Saltan: 33 Bogatyrs Emerging from the Sea",
    "artwork_artist": "Ivan Bilibin",
    "artwork_year": "1905",
    "artwork_source_lead": "https://commons.wikimedia.org/w/index.php?search=Bilibin+Tale+of+Tsar+Saltan+bogatyrs+public+domain+illustration&title=Special:MediaSearch&type=image",
    "artwork_rights_note": "public_domain_likely_verify_before_release",
    "artwork_match_reason": "Bilibin's 1905 illustration cycle for Pushkin's Tale of Tsar Saltan directly depicts the 33 sea-knights — one of the three wonders Rimsky-Korsakov musically portrays in the symphonic interludes.",
}


def main():
    if not CSV_PATH.exists():
        print(f"FAIL: {CSV_PATH} not found")
        sys.exit(1)

    # Read with utf-8-sig (preserves BOM detection)
    with open(CSV_PATH, encoding='utf-8-sig', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    header = rows[0]
    col_idx = {name: i for i, name in enumerate(header)}
    print(f"header: {header}")

    # Find target row by piece_ko exact match
    piece_ko_idx = col_idx['piece_ko']
    target_row = None
    target_idx = None
    matches_found = []
    for i, row in enumerate(rows[1:], start=1):
        if row[piece_ko_idx] == TARGET_PIECE_KO:
            target_row = row
            target_idx = i
            matches_found.append((i, row))

    if not target_row:
        print(f"FAIL: piece_ko exact match not found: {TARGET_PIECE_KO}")
        # Show closest matches for debug
        print("Rows containing '살탄' or '세 가지':")
        for i, row in enumerate(rows[1:], start=1):
            if '살탄' in row[piece_ko_idx] or '세 가지' in row[piece_ko_idx]:
                print(f"  row {i}: piece_ko={row[piece_ko_idx]!r}")
        sys.exit(1)

    if len(matches_found) > 1:
        print(f"FAIL: multiple matches ({len(matches_found)}) for piece_ko — bailing")
        sys.exit(1)

    print(f"matched row {target_idx}: rank={target_row[col_idx['rank']]} piece_ko={target_row[piece_ko_idx]}")
    print(f"current artwork_title: {target_row[col_idx['artwork_title']]!r}")

    # Idempotent guard
    if target_row[col_idx['artwork_title']].strip():
        print(f"SKIP: artwork_title already populated — already applied?")
        print(f"  artwork_title={target_row[col_idx['artwork_title']]!r}")
        print(f"  artwork_artist={target_row[col_idx['artwork_artist']]!r}")
        sys.exit(0)

    # Backup
    backup_path = CSV_PATH.with_suffix(CSV_PATH.suffix + BACKUP_SUFFIX)
    shutil.copy2(CSV_PATH, backup_path)
    print(f"backup: {backup_path.name}")

    # Apply patch
    for col_name, value in ARTWORK.items():
        idx = col_idx[col_name]
        old = target_row[idx]
        target_row[idx] = value
        print(f"  {col_name}: {old!r} -> {value[:60]!r}{'...' if len(value)>60 else ''}")

    # Write back with utf-8-sig (BOM preserved)
    with open(CSV_PATH, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"\nwrote {CSV_PATH.name} ({len(rows)} rows)")
    print("DONE")


if __name__ == "__main__":
    main()
