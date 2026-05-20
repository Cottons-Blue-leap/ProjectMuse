# Project Muse 워크플로우 운영 점검 작업계획

> 박힌 날짜: 2026-05-20 (s335) · 코튼 GPT 보고서 (`feedback.txt`) base
> E41 (input audit) + E44 (judgment audit) doctrine 통과 후 박힘

## 1. 보고서 claim verify

| GPT claim | 검증 | 비고 |
|---|---|---|
| `node_modules` ~1.83GB | ✓ gym 592M + joplin 589M + vivaldi 719M = ~1.9GB | 정합 |
| `candidates_opus` PDF ~1.15GB | ✓ 1.2GB | 정합 |
| `.tools` ~197MB | ✓ 204MB | 정합 |
| Git 저장소 아님 | ✓ `.git` 부재 | 정합 |
| Vivaldi + Joplin `VisualizerComposition.tsx` 해시 동일 | ✓ md5 일치 (`89fba3f8…`) · Gymnopedie만 다름 (시범 양식) | 정합 |
| `README.md` `score_ingestion/` 표기 | ✓ line 11·39 stale (실 폴더는 폐기 통과) | 정합 |
| `USAGE.md` 324곡·13컬럼 (실 340·14) | ✓ line 24 stale | 정합 |
| `naming_convention.md` source = `music/source_scores/` vs USAGE = `planning/candidates_opus/` 직접 | ✓ contradiction · 두 양식 양립 가능 (planning에서 reference → works/music/source_scores/로 ASCII rename copy axis 명시 부재) | partial |
| `title_naming_guide.md` `release_title`·`title_strategy`·`original_title_credit` 컬럼 요구 | ✓ csv엔 부재 · guide 자체 stale | 정합 |
| Gymnopedie `project.json` 부재 | ✓ 확인 | 정합 |
| Gymnopedie 구 구조 keep | ✓ `analysis/arrangement/midi/source_scores/vocaloid` | 정합 |
| `master_audio` manifest drift | ✓ Vivaldi project.json = `music/masters/master.wav` · 실제 = `music/Miku_vivaldi_spring_1_allegro.wav` (masters/ 비어있음) · Joplin은 status.json엔 정확 path, project.json엔 stale | 정합 |
| Vivaldi final.mp4 `exports/` 부재 · `visualizer/out/`만 박힘 | ✗ **WRONG** — `exports/vivaldi_spring_1_allegro_final.mp4` 존재 (+ visualizer/out/ 중복) | GPT 오판 1건 |
| `score_file` 96 · PDF 85 · mismatch 3 · unreferenced 7 | ✓ memory `matched 96/340` 정합 · PDF 85 정합 | 정합 |
| `status.json` 긴 의사결정 로그 섞임 | ✓ Joplin `last_decision` field ~3000자 (28 line file의 단일 field 비대) | 정합 |

**MOKA 자가 추가 적발 (GPT 미적발)**:
- `README.md` *Current Dogfood Lock* (line 70-80) = Canon in D · s313 이후 자체 폐기 양식 + publish 통과 작품 (Gym + Vivaldi + Joplin scheduled) 표기 부재
- Vivaldi `exports/` 안 `.bak` 2건 keep ([[feedback-backup-sidecar-preservation]] 정합 · keep axis)
- Joplin `video/exports/joplin_the_entertainer_final.mp4`와 `video/visualizer/out/joplin_the_entertainer_final.mp4` 중복 (Vivaldi sample 동일)

**verify 통과율**: 15 claim 중 14 정합 + 1 false positive = 93%.

## 2. 권장사항 5건 판단 audit (E44)

### A. Git init + `.gitignore` — ✓ ACCEPT

- **본질**: 300+ session 누적인데 version control X · history·rollback·release tag 부재 · 단발 cost 작음
- **risk**: large binary commit 사고 (gitignore 미흡 시) · push 의제 자체엔 안 박힘 (local commit only path keep 가능)
- **gitignore default**: `node_modules/` · `.tools/` · `video/visualizer/out/` · `video/exports/debug/` · `*.bak` · `*.mp4` · `*.wav` · `planning/candidates_opus/*.pdf` · `.env`
- **결단 자리 코튼**: 음원·영상·PDF는 git 밖 · 별 backup path (Google Drive · 외장하드 등) 확보 통과 여부
- **timing**: Joplin publish 통과 (2026-05-21 20:00 KST) 후 진입

### B. Remotion 공용 패키지 추출 — ⚠️ DEFER

- **본질 강**: 작품별 ~600MB 중복 · `VisualizerComposition.tsx` 동일 hash sample = 진짜 중복
- **risk**:
  - publish 통과 작품 3건 (Gym + Vivaldi + Joplin) retrofit risk
  - Remotion props 작품별 (cover · audio · title · duration · layout) 추상화 fitting 부담
  - [[feedback-premature-launch-kills-enthusiasm]] 정합 — 인프라 작업이 작품 출시 열의를 깎을 risk
- **대안**:
  - **Path α (지금)**: gitignore로 git 상 disk 제외 · 실제 local disk 그대로 keep · 운영 risk X
  - **Path β (6개월차)**: 작품 8-10건 누적 시점에 양식 명확해진 후 공용 패키지 결단
- **결단**: 지금은 α · β는 의제 keep

### C. `doctor` 명령 (path 검증) — ✓ ACCEPT (scoped)

- **본질**: manifest drift 사전 적발 axis · Moltbook `tools/validate_episode_ready.py` 양식 sample 정합 (s328)
- **scope** (over-engineer 회피):
  1. `project.json` 모든 path field (source_score_planning · master_audio · final_video) 존재 verify
  2. `status.json` `master_file` · `cover_file` · `art_source_file` · `source_pdf` 존재 verify
  3. release 4종 (`title.txt`·`description.md`·`credits.md`·`rights-notes.md`) 존재 verify (publish 통과 작품만)
  4. mismatch 자리 path 명시 보고
- **자리**: `workflows/project_setup/scripts/muse_doctor.py` 신축 (또는 `muse_project.py doctor` subcommand)
- **timing**: Joplin publish 통과 후

### D. 문서 정합성 정리 — ✓ STRONG ACCEPT

- **본질 강**: 새 작품 진입 시점 stale doc이 혼선·잘못된 양식 axis risk
- **fix 4건**:
  1. **`README.md`** — `score_ingestion` 표기 2곳 (line 11·39) 제거 + *Current Dogfood Lock* (line 70-80 Canon in D) cut 또는 publish 누적 양식으로 polished
  2. **`USAGE.md`** — line 24 *324곡 · 13 컬럼* → *340곡 · 14 컬럼* update
  3. **`naming_convention.md`** — row 27 source score 양식에 *복사 양식* axis 명시 (planning/candidates_opus/ → works/<piece>/music/source_scores/ ASCII rename copy)
  4. **`title_naming_guide.md`** — `release_title`·`title_strategy`·`original_title_credit` 컬럼 자체 csv에 없음 · stale doctrine 폐기 또는 강 polished (현 실 양식 = piece 컬럼 + publish 시점 release_title 결단)
- **risk**: X (read-only doc 정리만 · live workflow 손대지 않음)
- **timing**: 지금 진입 가능

### E. 산출물 정책 분리 — ⚠️ PARTIAL ACCEPT

- **현 자료**:
  - `exports/` 안 final.mp4 + `.bak` + debug PNG + `_qc_frame` 섞임
  - `visualizer/out/`에 final.mp4 중복 (Joplin·Vivaldi sample)
- **fix**:
  - `exports/` 안 `debug/` 폴더 양식 · `_qc_frame*.png` → `exports/debug/` 이동 (gitignore axis · disk keep)
  - `visualizer/out/`는 gitignore (build artifact axis)
  - `.bak` keep ([[feedback-backup-sidecar-preservation]] 정합)
- **timing**: gitignore (A) 진입 시점에 함께

## 3. MOKA 자가 추가 의제

### F. Gymnopedie post-hoc manifest — ✓ ACCEPT (5분 작업)

- **자료**: 시범 첫 작품이라 `project.json` 부재 · 구 구조 keep
- **fix**: `project.json` 신축 + README에 *legacy structure (first proof)* 명시
- **자료 양식**: `master_audio`에 실제 path 박음 · naming convention v1 retrofit X (publish 통과 doctrine 정합)

### G. `status.json` 양식 의제 — ⚠️ DEFER + WATCH

- **GPT 자료**: *decisions.md / post_release_retrospective.md로 빼라*
- **counter**: `status.json`은 현재 작동 양식 · 모든 결단 한 자리 *live retrospective* axis 정합 · 라이브 서비스 keep doctrine 정합
- **결단**: 지금은 keep · 8-10작품 누적 후 fragmentation risk 발생 시 재결단

## 4. 우선순위

### Tier 1 — 지금 진입 가능 (Joplin publish risk X)

| 순서 | ID | 자리 | 시간 |
|---|---|---|---|
| 1 | D-1 | `README.md` polished (score_ingestion 제거 + dogfood block update) | 10분 |
| 2 | D-2 | `USAGE.md` 324→340 / 13→14 update | 2분 |
| 3 | D-3 | `naming_convention.md` source score 양식 axis 박음 | 5분 |
| 4 | D-4 | `title_naming_guide.md` 검토 + 결단 (강 polished or cut) | 15분 |
| 5 | F | Gymnopedie post-hoc `project.json` + README note | 5분 |

**Tier 1 합계 ~37분**.

### Tier 2 — Joplin publish 통과 후 (2026-05-21 20:00 KST 이후)

| 순서 | ID | 자리 | 시간 |
|---|---|---|---|
| 6 | A | Git init + `.gitignore` (코튼 결단 + backup path 확인) | 30분 |
| 7 | E | `exports/debug/` 양식 + visualizer/out/ gitignore | 10분 |
| 8 | C | `muse_doctor.py` 신축 (scope 박힌 양식) | 1시간 |

**Tier 2 합계 ~1.7시간**.

### Tier 3 — 의제 keep (now 진입 X)

- **B**: Remotion 공용 패키지 추출 (6개월차 8-10작품 누적 후 결단)
- **G**: `status.json` 양식 분리 (8-10작품 누적 후 결단)

## 5. 코튼 결단 자리

1. **Git init OK?** node_modules·PDF·wav·mp4 gitignore + code/doc/csv commit 양식. 별 backup path 확보 통과?
2. **`title_naming_guide.md`** = 강 polished (실 양식으로 update) vs cut (양식 자체 *piece 컬럼 + 발행 시점 결단* sufficient)?
3. **Tier 1 지금 진입 OK?** (5건 · ~37분 · Joplin scheduled flow risk X)
4. **Remotion 공용 패키지** = 지금 (Path β) vs 6개월차 결단 keep (Path α gitignore-only)?

## 6. 자가 결함 catalog

- **process layer**: 1차 박힘 시 *자체엔 자료* jargon 자리표시자 100+ 반복 (E33 family 재발 sample · jargon 본능 자가 사후 정정 cycle 통과 양식 s334 박힘 후 재발) → 통째 rewrite path 통과
- **input audit (E41)**: 통과 — GPT 15 claim 전수 verify (1 false positive 적발)
- **judgment audit (E44)**: 통과 — 5 recommendation 자체 doctrine cross-check + accept/defer 분리 (B 자체 [[feedback-premature-launch-kills-enthusiasm]] 정합 적발이 핵심 분기점)
