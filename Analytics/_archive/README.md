# `Analytics/_archive/` — 일회성 자료 archive

`CONVENTIONS.md` §1 + `planning/_archive` 모델 정합. 2026-05-30 (reorg P3) 신축.

## 자리

특정 곡·특정 cycle 전용 **1회용 스냅샷/진단 스크립트** keep. 본 폴더 자체엔 능동 호출 X (path 가정이 root 기준이라 재실행 시 import 경로 확인 필요).

- `_compare_meta.py` — s375 · 5곡 메타 비교 dump (임시 진단)
- `_mozart_snapshot.py` — s380 · K.265 publish 직후 stats
- `_salut_snapshot.py` — s375 · Salut d'Amour publish 직후 stats

## 운영

- `muse_tidy.py`(루트)가 `# ONE-OFF` 표식 스크립트를 본 폴더로 이동(`--archive`).
- 재사용 도구(`youtube_analytics.py`·`youtube_meta.py`·`playlist_meta.py`·`analytics_xlsx.py`)는 `Analytics/` root keep.
