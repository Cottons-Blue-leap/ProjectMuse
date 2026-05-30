---
name: planning-archive
description: planning/ 안 일회성 자료 archive. cycle_scripts/ + backups/. 작업 끝난 자료 keep · 본 폴더 자체엔 능동 호출 X axis.
metadata:
  type: archive
  created: 2026-05-27 s371
---

# `_archive/` — 일회성 자료 archive

s371 (2026-05-27) 신축. 코튼 MOKA 자율위임 결단 흡수.

## 구조

- **`cycle_scripts/`** = 1회성 cycle 작업 자료. 본 cycle 종료 후 재사용 가능성 약 (양식 reference만).
- **`backups/`** = candidate_master.csv.bak_* 자료. [feedback_backup_sidecar_preservation.md] 정합 · 데드 에셋 X · 롤백 자료 keep.

## 운영 doctrine

- 신규 자료 추가 시점 = cycle 종료 시점. *완료된 작업 자료*만 본 폴더 박음.
- 재사용 가능 도구 (cycle-agnostic) = 본 폴더 X · `planning/` 루트 자리 (`_apply_tier_review.py` / `_renumber_csv.py` / `_audit_new_pdfs.py` 등).
- 자료 검색 시점 외 호출 빈도 약. 본 폴더 안 자료 직접 import 양식 X (자료 양식 reference만).
