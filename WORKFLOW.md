# Project Muse — 운영 워크플로우 (단일 진입점)

> 흩어진 워크플로우 문서를 **운영자 관점 end-to-end 흐름** 한 장으로 종합. 각 단계의 상세는 포인터로.
> 짝 문서 = [`ROADMAP.md`](ROADMAP.md) (성장 단계·마일스톤) · 디렉토리 구조 = [`README.md`](README.md) · 전역 독트린 = [`CONVENTIONS.md`](CONVENTIONS.md).
> 최종 갱신 2026-06-12.

---

## 큰 그림 — 3개 루프

```
        ┌─────────────────────────────────────────────┐
        │  ① 곡 제작 루프 (메인 엔진 · 주 2곡 지향)      │
        │     선곡 → 입력 → 마스터+게이트 → 커버         │
        │       → 영상 → 메타 → 발행 → 측정             │
        └───────────────┬─────────────────────────────┘
                        │ 곡 발행마다 게이지 +1
                        ▼
        ┌─────────────────────────────────────────────┐
        │  ② 합본 루프 (부산물 · 임계 도달 시 발동)       │
        │     게이지 갱신 → 임계 → 합본 제작(렌더·발행)   │
        └─────────────────────────────────────────────┘

        ③ 운영 의례 (주간 측정 + 상시 큐레이션) — 위 둘을 받쳐줌
```

---

## ① 곡 제작 루프 (per-song)

| # | 단계 | 하는 일 | owner | 상세 문서 |
|---|------|---------|-------|-----------|
| 1 | **선곡** | candidate에서 다음 곡 + **합본 슬롯 판단 묶기**(어느 게이지 채우나·무드 태그 명시) | 코튼+MOKA | [`planning/candidate_master.csv`](planning/candidate_master.csv) · [`planning/compilation_operating_structure.md`](planning/compilation_operating_structure.md) |
| 2 | **입력/편곡** | V6 수동 입력(채보·성부 분배) | 코튼 | [`workflows/music_acappella/WORKFLOW.md`](workflows/music_acappella/WORKFLOW.md) · `docs/role_taxonomy.md` · `docs/role_division.md` |
| 3 | **마스터+게이트** | MOKA 계측(LUFS/TP/스테레오) → **렌더 전 블렌딩 게이트** → 코튼 청취 | MOKA계측 + 코튼청취 | [`workflows/audio_production/docs/v6_render_workflow.md`](workflows/audio_production/docs/v6_render_workflow.md) · [`workflows/video_release/docs/blending_gate.md`](workflows/video_release/docs/blending_gate.md) · 기준선=`reference_muse_loudness_baseline`(메모리) |
| 4 | **커버** | 명화 선정 + 미쿠 합성(원작서 재생성) | 코튼+MOKA | [`planning/ballet_subfamily_convention.md`](planning/ballet_subfamily_convention.md) · [`planning/classical_miku_anchor.md`](planning/classical_miku_anchor.md) · 커버 재생성 doctrine(메모리) |
| 5 | **영상 렌더** | 레터박스 + B 공유 visualizer + QC 5축 | MOKA | [`workflows/video_release/docs/video_workflow.md`](workflows/video_release/docs/video_workflow.md) · [`docs/shared_visualizer_design.md`](workflows/video_release/docs/shared_visualizer_design.md) · `templates/visualizer-spec.md` |
| 6 | **메타** | 썸네일 + 설명(curator voice) + l10n 10언어 + 태그 + 제목 | MOKA | [`docs/thumbnail_guide.md`](workflows/video_release/docs/thumbnail_guide.md) · [`docs/description_template.md`](workflows/video_release/docs/description_template.md) · [`docs/localization.md`](workflows/video_release/docs/localization.md) · [`planning/title_naming_guide.md`](planning/title_naming_guide.md) |
| 7 | **발행** | 코튼 업로드/예약 → audit → publish → 고정댓글 | 코튼업로드 + MOKA | [`workflows/video_release/docs/post_release_meta_doctrine.md`](workflows/video_release/docs/post_release_meta_doctrine.md) |
| 8 | **측정** | 발행 직후 publish/고정댓글 **검증**만 · 성과 분석은 ③ **주간 의례로 통합**(영상별 7d 측정 폐기) | MOKA | [`Analytics/README.md`](Analytics/README.md) |

엔진 = 단일 CLI `python muse.py <project|audio|thumbnail|render|tidy|doctor|status|list>` · 사용 흐름 = [`USAGE.md`](USAGE.md).

---

## ② 합본 루프 (곡이 쌓이면 발동 · 새 곡 입력 없음)

```
곡 발행마다  → 슬롯 보드 게이지 갱신 (①-1에서 박은 무드 태그로)
임계 도달    → 합본 제작
               · 무드(Evergreen) ~12곡/축
               · Quest(작품집) 전곡 완성
               · Flagship 20~30곡
양식         → 첫 합본(사계 봄)에서 파일럿 정립
제작         → ①의 5~7단계 축소판 (렌더·메타·발행만)
```

정본 = [`planning/compilation_operating_structure.md`](planning/compilation_operating_structure.md) (5버킷 + 발행형식 태그 + 합본/재생목록 판단룰 + 슬롯 보드 + 도전과제 보드).

---

## ③ 운영 의례

- **주간 (일요일)** = 코튼 Studio 도달범위 28일 숫자 → MOKA report + `studio_reach.csv` 행 + 핵심변화 3줄. 첫 회차 2026-06-14. → [`Analytics/README.md`](Analytics/README.md)
- **상시** = candidate 큐레이션 유지 · `muse.py doctor`(works 정본 검사) · 메모리 갱신.

---

## 그 외 트랙 (본편과 별개)

- **쇼츠** = [`workflows/shorts_first_proof/README.md`](workflows/shorts_first_proof/README.md) + MikuDiscovery rig(`canon_round/` · 코튼 차례: 3성부 스템 + 2차창작 미쿠 드롭인).
- **학습영상** = 수요 시그널 조건부(댓글 누적 시 재논의 · 지금 X).

---

## 정본 문서 인덱스 (역할별 빠른 참조)

| 역할 | 문서 |
|------|------|
| 워크플로우 인덱스/순서 | [`workflows/README.md`](workflows/README.md) + `registry.json` |
| 전역 명명·아카이빙 독트린 | [`CONVENTIONS.md`](CONVENTIONS.md) |
| 선곡 후보 풀 | [`planning/candidate_master.csv`](planning/candidate_master.csv) |
| 합본 운영 | [`planning/compilation_operating_structure.md`](planning/compilation_operating_structure.md) |
| 제목 컨벤션 | [`planning/title_naming_guide.md`](planning/title_naming_guide.md) |
| 발레 커버 컨벤션 | [`planning/ballet_subfamily_convention.md`](planning/ballet_subfamily_convention.md) |
| 측정/Analytics | [`Analytics/README.md`](Analytics/README.md) |
| 시리즈 발행 이력 | [`series_history.csv`](series_history.csv) |
