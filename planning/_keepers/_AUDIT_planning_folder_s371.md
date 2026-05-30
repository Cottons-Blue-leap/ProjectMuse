---
name: planning-folder-audit-s371
description: planning/ 폴더 전수 audit + 구조 제안. 일회성 자료 vs 영구 자료 vs 백업 자료 분류. 코튼 결단 자리.
metadata:
  type: project
  cycle: s371
  date: 2026-05-27
  status: proposal_open
---

# Planning 폴더 Audit + 구조 제안 — s371

> 코튼 throw (2026-05-27 디스코드): *일회성 파일들은 한 곳에 모아두는 게 좋을 것 같아 + 기억할 가치가 있는 것도 폴더 하나 생성해서 모아두는 것도 좋고*.
> 본 자료 = MOKA 1차 audit + 구조 제안. **실 이동 X · 코튼 결단 자리 비움 keep**.

---

## 전수 자료 (현 25 entry · `planning/` 루트)

### A. 영구 자료 (자주 호출 · 정본)

| 파일 | 용도 | 호출 빈도 |
|------|------|----------|
| `candidate_master.csv` | 358 row 정본 · piece_ko stable id base | 매 cycle |
| `candidates_opus/` (144 PDF) | score 자료 정본 · publish 시 자가 점검 | 매 곡 |
| `classical_miku_anchor.md` | 시그너처 캐릭터 anchor (3줄 외형) | publish 시 |
| `title_naming_guide.md` | 정본 제목 양식 (s355 v3 · 근거 3축 + 포맷 history) | publish 시 |
| `artwork_matching_guide.md` | 명화 매칭 가이드 | 곡 선정 시 |
| `repertoire_candidates.md` | 초기 후보곡 자료 (s240~) | 초기 reference |
| `world_loved_classics_validation.md` | 세계 친숙도 validation 자료 (s296~) | tier review 시 |
| `reference_links.txt` | 외부 참고 link 묶음 | reference |
| `VOCALOID_Reference_Manual_ENG.pdf` | V6 manual (4.5MB) | reference |
| `acappella visualization/` | R&D 자료 폴더 (s371 신축) | R&D cycle |

→ **현 자리 keep 추천** (planning/ 루트).

### B. 재사용 가능 도구 (cycle-agnostic)

| 파일 | 용도 | 재사용 기록 |
|------|------|-----------|
| `_apply_tier_review.py` | tier review CHANGES dict apply (idempotent) | s317 C tier + s369 D tier review base · MEMORY.md 박힘 |
| `_renumber_csv.py` | rank 재번호 도구 (csv-agnostic) | s317 + s330 + s368 등 |
| `_audit_new_pdfs.py` | candidates_opus 새 PDF audit (csv ↔ folder 정합 점검) | s338 + s367 등 |

→ **현 자리 keep 추천** (재사용 도구 axis · MEMORY.md 박힘 자료 자체 axis).

### C. 일회성 cycle 자료 (작업 끝남 · 기억 가치 자료)

| 파일 | cycle | 자료 본질 | 기억 가치 |
|------|-------|----------|---------|
| `_d_tier_review_decisions_s369.md` | s369 | D tier 91곡 review draft · 코튼 결단 대기 | ⭐⭐⭐ 결단 후 흡수 base |
| `workflow_audit_2026-05-20.md` | s330 | 워크플로우 자가 점검 자료 | ⭐⭐ R&D reference |
| `영상개선 UI시안_ver1.pptx` | s356 | UI 시안 ver1 (가능성 = 코튼 ChatGPT 출력 자료) | ⭐⭐ R&D reference |

→ **기억 가치 폴더 이동 추천**.

### D. 일회성 cycle 작업 자료 (1회용 · 보존 가치 약)

| 파일 | cycle | 자료 본질 | 기억 가치 |
|------|-------|----------|---------|
| `_apply_score_file_sync.py` | s367 phase 1 | candidate_master.csv score_file 컬럼 sync | ⭐ 양식 reference만 |
| `_apply_score_file_sync_phase2.py` | s367 phase 2 | 동일 sync · phase 2 | ⭐ 양식 reference만 |
| `_apply_score_file_sync_phase3.py` | s367 phase 3 | 동일 sync · phase 3 | ⭐ 양식 reference만 |
| `_apply_rimsky_artwork_s368.py` | s368 | 림스키 row artwork 6 컬럼 박음 (1회) | ⭐ 양식 reference만 |
| `_audit_new_pdfs_out.txt` | s367 | audit output 자료 (이미 csv 흡수) | ⭐ 흡수 통과 자료 |

→ **일회성 archive 폴더 이동 추천**.

### E. 백업 자료 (.bak)

| 파일 | cycle |
|------|-------|
| `candidate_master.csv.bak_s367_score_file_sync` | s367 |
| `candidate_master.csv.bak_s367_score_file_sync_phase2` | s367 |
| `candidate_master.csv.bak_s367_score_file_sync_phase3` | s367 |
| `candidate_master.csv.bak_s368_rimsky_artwork` | s368 |

→ **백업 폴더 이동 추천** ([feedback_backup_sidecar_preservation.md] 정합 · 데드 에셋 X · 롤백 자료 keep).

---

## 구조 제안 3 양식

### 양식 1 (코튼 hint 정합 · 2 폴더)

```
planning/
├── (영구 자료 · 도구 · candidates_opus · acappella visualization 등 = 루트 keep)
├── _archive/              ← 일회성 자료 한 곳
│   ├── (cycle scripts: _apply_score_file_sync.py 등 4건)
│   ├── (백업: candidate_master.csv.bak_* 4건)
│   └── (output: _audit_new_pdfs_out.txt 1건)
└── _keepers/              ← 기억 가치 자료
    ├── _d_tier_review_decisions_s369.md
    ├── workflow_audit_2026-05-20.md
    └── 영상개선 UI시안_ver1.pptx
```

**장점**: 코튼 hint 정합 + 단순 (2 폴더만 신축).
**단점**: `_archive/` 안 *cycle scripts + 백업 + output* 자료 다 섞임 (혼합 자료).

### 양식 2 (MOKA 추천 · 3 폴더)

```
planning/
├── (영구 자료 · 도구 · candidates_opus · acappella visualization 등 = 루트 keep)
├── _archive/
│   ├── cycle_scripts/     ← 일회성 .py (4건)
│   └── backups/           ← .bak 자료 (4건)
└── _keepers/              ← 기억 가치 자료 (3건)
```

**장점**: cycle script + 백업 분리 → 미래 검색 시 본질 명확.
**단점**: 폴더 1단 더 깊음 + 코튼 hint 양식 살짝 elaborate.

### 양식 3 (날짜 양식 · 코튼 결단 자리)

```
planning/
├── (영구 자료 · 도구 · candidates_opus · acappella visualization 등 = 루트 keep)
├── _archive/
│   ├── 2026-05_s367_score_sync/   ← cycle별 묶음
│   ├── 2026-05_s368_rimsky/
│   └── ...
└── _keepers/              ← 기억 가치 자료 (3건)
```

**장점**: cycle별 자료 + 백업 자료 함께 묶음 (양식 정합 강).
**단점**: 매 cycle 폴더 신축 부담 + 향후 운영 부담 axis.

---

## MOKA 추천 axis (코튼 자리 우선)

**양식 2 추천 axis** = cycle_scripts vs backups 본질 다름 + 미래 검색 시 분리 강. 단 양식 1 (코튼 hint 직접 정합)도 viable. 코튼 자가 결단 자리.

---

## 자가 사전 발화

- **자료 손실 risk 0 axis** = 본 audit = 분류만 + 이동만. 자료 삭제 X · 원복 path 자동.
- **추천 push 본능 자가 인식** = MOKA 양식 2 추천 axis 자가 인식. 코튼 hint 양식 1 직접 정합 자체엔 코튼 자가 우선 doctrine.
- **`_d_tier_review_decisions_s369.md` 자료 자리 axis** = *기억 가치* axis 자료 자체엔 *코튼 결단 진행 중* 자료 axis. 결단 완료 후 흡수 path · 흡수 통과 후 archive 자료. 본 cycle 시점 *keepers* 자리 정합 (결단 진행 중 = 자주 호출 자리).
- **acappella visualization 폴더 자리 axis** = 영구 자료 axis? R&D 자료 axis? 현 시점 *R&D 자료* 자리이지만 본 path 진입 결단 후 영구 자료 axis로 격상 자료. **현 자리 = 루트 keep** 추천 (R&D cycle 자주 호출 자리).
- **candidates_opus 자리 axis** = 영구 자료 keep · 144 PDF score 자료 정본 · 매 곡 publish 시점 자가 점검 자리.

---

## 의제 자리 (코튼 결단)

- (가) **양식 결단** = 양식 1 / 양식 2 / 양식 3 / 다른 양식
- (나) **폴더 명명 결단** = `_archive` + `_keepers` / 다른 명명 (`archive_oneshot` / `references` 등)
- (다) **`_d_tier_review_decisions_s369.md` 자리 결단** = keepers / 루트 keep (결단 진행 중) / 둘 다 keep
- (라) **MOKA 자율 결단 axis** = 본 결단 자체 코튼 *MOKA 자율 결단* 위임 결단 가능 axis · 위임 통과 시 MOKA 양식 2 default 진입 path
