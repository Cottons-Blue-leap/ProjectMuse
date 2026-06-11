# `Analytics/_archive/` — 일회성 자료 archive

`CONVENTIONS.md` §1 + `planning/_archive` 모델 정합. 2026-05-30 (reorg P3) 신축.

## 자리

특정 곡·특정 cycle 전용 **1회용 스크립트 + 그 산출물 리포트** keep. 본 폴더 자체엔 능동 호출 X (path 가정이 root 기준이라 재실행 시 import 경로 확인 필요).

**진단 스냅샷 스크립트**
- `_compare_meta.py` — s375 · 5곡 메타 비교 dump (임시 진단)
- `_mozart_snapshot.py` — s380 · K.265 publish 직후 stats
- `_salut_snapshot.py` — s375 · Salut d'Amour publish 직후 stats
- `growth_pull.py` (+ `growth_raw.json`) — 채널 성장 stats 1회 pull (기존 아카이브 · 현 누적 성장 지표는 `youtube_analytics.py`에 통합 ·06-12·)

**마이그레이션 retrofit 스크립트 (실행 완료 · ·06-12· Analytics root에서 이주)**
- `_retrofit_acappella_badge_s402.py` · `_mozart_full_badge_s402.py` · `_standardize_tags_s402.py` · `_sync_series_history_titles_s402.py` — s402 badge/태그 retrofit
- `_augment_jp_tags_s411.py` · `_jp_hashtag_reorder_s411.py` — s411 JP 태그/해시태그 (⚠️ augment가 standardize를 import → 둘은 같은 폴더 유지 필요)

**일회성 진단 산출물 리포트 (·06-12· Analytics root에서 이주)**
- `discovery_diagnosis.md` — 채널 발견(discovery) 진단
- `project_diagnosis_2026-06-10.html` — 프로젝트 종합 진단 (2026-06-10)
- `jp_2nd_creation_inflow_report_2026-06-09.txt` — 일본 2차창작 유입 리포트 (2026-06-09)

## 운영

- `muse_tidy.py`(루트)가 `# ONE-OFF` 표식 스크립트를 본 폴더로 이동(`--archive`).
- 재사용 도구(`youtube_analytics.py`·`youtube_meta.py`·`playlist_meta.py`·`analytics_xlsx.py`)는 `Analytics/` root keep.
