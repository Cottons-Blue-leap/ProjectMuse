# Project Muse — Workflows Index

> 단일 레지스트리 = [`registry.json`](registry.json) (머신리더블) · 본 파일 = 인간용 인덱스.
> 새 워크플로우 = [`_TEMPLATE/`](_TEMPLATE/) 복사 → README front-matter 채움 → `registry.json` 등재.
> 전 프로젝트 순서 = [`../USAGE.md`](../USAGE.md) · 명명 양식 = [`naming_convention.md`](naming_convention.md).

## 파이프라인 순서

```text
project_setup    → 0 · 작업 폴더 + project.json 신축          [cli]
rights_clearance → 1 · 권리 정합 게이트                        [manual]
music_acappella  → 2 · V6 entry reference (production X)       [reference]
audio_production → 3 · dry stem 점검 + light assembly + master [cli]
video_release    → 4 · 승인된 audio → YouTube package          [cli+manual]
shorts_first_proof → 5 · 본 영상 +1달 → 쇼츠 1편               [manual]
```

지원 자리: `shared/` (공유 템플릿·스키마) · `naming_convention.md` (piece_id doctrine).

## 워크플로우 요약

| 워크플로우 | stage | type | 진입점 | 산출 | 소유 |
|---|---|---|---|---|---|
| **project_setup** | 0 | cli | `muse_project.py init` | `project.json` + 11폴더 계약 | MOKA |
| **rights_clearance** | 1 | manual | `rights/rights-log.md` 작성 | 권리 결단 (approved/needs review/rejected) | MOKA |
| **music_acappella** | 2 | reference | V6 옆 docs 참고 | dry stems (V6 export) | 코튼 |
| **audio_production** | 3 | cli | `muse_audio.py check-stems / assemble-proof / blend-gate` | `master.wav` + blend_gate_report + listening 결단 | 코튼+MOKA |
| **video_release** | 4 | cli+manual | video-brief → `muse.py render <work_id>` (공유 visualizer) → release/ | `<piece>_final.mp4` + 업로드 패키지 | 코튼+MOKA |
| **shorts_first_proof** | 5 | manual | master 30초 cut + V6 녹화 | YouTube Short | 코튼+MOKA |

게이트 2종: **rights_clearance**(stage 1 · 권리) + **blend-gate**(stage 3→4 사이 · 렌더 전 객관 블렌딩 측정 · spec = [`video_release/docs/blending_gate.md`](video_release/docs/blending_gate.md) · un-gated master 렌더 금지). 영상 렌더 = 공유 visualizer 단일 프로젝트([`video_release/visualizer/`](video_release/), 양식 B s412 · 설계 = `video_release/docs/shared_visualizer_design.md`).

상세 입출력·의존은 [`registry.json`](registry.json) 참조. 각 워크플로우 폴더 `README.md` 첫머리에 front-matter(name/stage/entry/inputs/outputs/depends_on) 박힘.

## 내부 폴더 계약

각 워크플로우는 `README.md` 필수. 아래 하위 폴더는 **있으면 이 이름**(없어도 됨):

| 폴더 | 용도 |
|---|---|
| `docs/` | 상세 절차·doctrine 문서 |
| `scripts/` | 실행 스크립트 (`muse_*.py` prefix) |
| `templates/` | 이 워크플로우 단독 사용 양식 |
| `config/` | 워크플로우 설정 (music_acappella 특수 케이스만) |
| `prompts/` | 시점별 사고 정리 reference (music_acappella) |

> 2개 이상 워크플로우가 공유하는 템플릿은 `shared/templates/`로. 단일 사용은 워크플로우-local `templates/`로.

## 워크플로우 추가 / 수정 / 삭제

**추가**
1. `cp -r workflows/_TEMPLATE workflows/<new_name>`
2. `<new_name>/README.md` front-matter 채움 + 본문 작성
3. 필요한 하위 폴더만 남기고 나머지 삭제 (docs/scripts/templates)
4. `registry.json`의 `workflows{}` + `pipeline_order`에 등재
5. 순서에 영향 주면 `../USAGE.md` 갱신

**수정**: 해당 폴더 + `registry.json` 항목만 갱신. (s-notation으로 본문에 변경 이력 박음 · 파일명 버전 증식 X)

**기능 신축** (기존 워크플로우에 새 스크립트·docs·CLI 명령·subdir 추가): *같은 커밋*에서 `registry.json` 해당 entry(entry/outputs/docs/subdirs) + 본 인덱스 요약표 갱신. (s412 visualizer·s414 blend-gate 2사이클 연속 누락 → 2026-06-10 점검 적발 교훈)

**삭제**: 폴더 제거 + `registry.json`에서 빼기 + `../USAGE.md`/의존 워크플로우 `depends_on` 정정. 폐기 자료는 `workflows/_archive/`로 (즉시 삭제 X).

## 명명·일회성 doctrine

전 프로젝트 명명·아카이빙·일회성 파일 수명 = 루트 [`../CONVENTIONS.md`](../CONVENTIONS.md) 단일 소스.
