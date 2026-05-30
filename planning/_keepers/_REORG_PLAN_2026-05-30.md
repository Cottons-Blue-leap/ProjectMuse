# Project Muse — 폴더/워크플로우 최적화 작업계획서

> 작성 2026-05-30 · 작성자 MOKA · status = **제안 (코튼 승인 대기)**
> 목적 = 라이브 운영 시 워크플로우 추가/수정/삭제 간소화 + 체계화 + 폴더 구조 정돈 + 일회성 파일 자동 수명관리

---

## 0. 검증된 현황 진단 (블라인드 X · 실측 기반)

### 0-1. 잘 되어 있는 것 (건드리지 않음)
- **git 위생은 이미 우수**. 추적 파일 **203개** (md 85 / json 30 / py 28 / csv 11 / tsx 10 / ts 10 / ttf 6 / png 5) = 순수 source-of-truth만.
  `node_modules` / `visualizer/out` / `.vpr` / `.wav` / `.mp4` / `.pdf` = **git 추적 0개**. `.gitignore`가 정확히 작동 중.
  → **"repo 부풀림" 문제는 없다.** 마찰은 전부 *로컬 작업 디렉토리 인체공학 + 구조 일관성 + 일회성 파일 수명*에 있음.
- `planning/_archive/` + `planning/_keepers/` 아카이빙 독트린 (s371) = 이미 좋은 모델. **이걸 프로젝트 전역 표준으로 승격**하는 게 핵심 방향.
- `.gitignore` axis 주석 = 양식 자체가 문서. 유지.

### 0-2. 실제 마찰점 (이번 작업 대상)
| # | 마찰 | 근거 |
|---|------|------|
| F1 | **워크플로우 레지스트리·인덱스 부재** | `workflows/` 루트에 README/index 없음. 7개 워크플로우 + 순서 + 진입점 + 입출력 + 의존을 한눈에 볼 단일 소스 X. add/edit/delete 시 README.md·USAGE.md 등 여러 곳 수동 갱신 |
| F2 | **워크플로우 내부 레이아웃 불균일** | `project_setup`(docs+scripts) / `music_acappella`(docs+templates+config+prompts·config는 미사용) / `rights_clearance`·`shorts_first_proof`(README만) / `shared`(schemas 빈 폴더) — 새 워크플로우 추가 시 "무슨 폴더를 만들지" 기준 없음 |
| F3 | **스캐폴딩·검사 도구 부재** | 새 work·새 워크플로우를 복사로 시작할 템플릿 골격 없음. work이 정본 구조를 지키는지 검사(lint)할 도구 없음 |
| F4 | **works 구조 드리프트** | 정본(joplin family) 대비 `notes/`·`rights/`·`cover/iterations/`·`edit_project/` 들쭉날쭉. USAGE.md가 박는 11폴더 ≠ 실제 works. 레거시(gymnopedie 구조·greensleeves omr) 명시적 표식 X |
| F5 | **일회성 파일 수명관리 절반만 체계화** | `planning/`은 `_archive` 독트린 有. 그러나 `Analytics/`의 `_mozart_snapshot.py`·`_salut_snapshot.py`·`_compare_meta.py`("1회용" 명시)는 작업 디렉토리에 잔류. 전역 sweep 규칙·도구 X |
| F6 | **고아 템플릿·스크립트** | `audio_production/templates/render-study-*`(어느 문서도 참조 X) / `music_acappella/config/project.json`(미사용) / `prompts/02_arranger.md`(미사용) / `video_release/make_thumbnail.py`(README 미참조·명명 불일치) |
| F7 | **명명 위생** | `planning/acappella visualization`(폴더명 공백) / 스크립트 prefix `muse_*` ↔ `make_*` 혼재 / 버전 표식이 파일명 아닌 본문 s-notation에만 존재 |
| F8 | **문서 드리프트** | USAGE.md "340곡 14컬럼" ↔ 실제 `candidate_master.csv` 353행 15컬럼. 스캐폴더 산출 구조 ↔ 실제 work 구조 불일치 |

---

## 1. 목표 상태 (Target)

> "라이브 운영 중 워크플로우/작품을 **복사 한 번 + 검사 한 번**으로 추가하고, 일회성 파일은 **반자동 sweep**으로 정리되는 상태."

1. `workflows/` = 단일 레지스트리 + 균일 폴더 계약 + `_TEMPLATE` 골격.
2. `works/` = 정본 골격 1개 문서화 + 레거시 명시적 면제 + lint/dashboard 도구.
3. 일회성 파일 = 전역 `_archive` 독트린 + `_oneoff` 태깅 + sweep 도구.
4. 단일 CLI 진입점 `muse.py` (선택) — 흩어진 `muse_project.py`/`muse_audio.py`/`make_thumbnail.py` 통합 dispatcher.
5. README·USAGE = 레지스트리/독트린을 가리키도록 갱신, 드리프트 제거.

---

## 2. 단계별 작업 (레버리지·가역성 순)

### Phase 0 — 베이스라인 스냅샷 (안전장치 · ~5분)
- 현재 미추적 13건(`_archive`/`_keepers`/`shorts_first_proof`/exploration/Analytics 1회용 등)을 **먼저 커밋**해서 되돌림 기준점 확보.
- 본 계획서 자체도 커밋.
- ⛔ 어떤 이동/삭제도 이 커밋 이후에만.

### Phase 1 — 워크플로우 시스템 표준화 (★ 최고 레버리지)
1-1. **균일 폴더 계약 정의** — 각 워크플로우는 `README.md`(표준 front-matter: `name / stage / entry / inputs / outputs / depends_on`) 필수 + `docs/ scripts/ templates/`는 선택(있으면 이 이름). `config/`·`prompts/`는 `music_acappella` 특수 케이스로 한정.
1-2. **`workflows/README.md` 레지스트리 신축** + 머신리더블 `workflows/registry.json` (워크플로우명·stage 순서·진입 명령·io·deps). add/edit/delete = 이 한 파일만 갱신.
1-3. **`workflows/_TEMPLATE/` 골격** — 새 워크플로우 = 복사 → front-matter 채움 → registry 등록. 끝.
1-4. **고아 정리(F6)** — 각 항목 코튼 확인 후: render-study-* 템플릿(audio_production README에 편입 or 삭제) / music_acappella `config/`·`prompts/02_arranger`(reference 표식 명시 or 정리) / `make_thumbnail.py`(→ `muse_thumbnail.py` 改名 + video_release README 등재).
1-5. **명명 통일** — 실행 스크립트 `muse_*.py` prefix. 템플릿 배치 정책 1줄 룰: "2개 이상 워크플로우 공유 → `shared/templates/`, 단일 → 워크플로우-local `templates/`".

### Phase 2 — works 정본 + 스캐폴딩/대시보드 (라이브 운영 직결)
2-1. **정본 골격 문서화** — joplin/mozart/vivaldi family를 정본으로 `workflows/project_setup/docs/`에 단일 소스화. USAGE.md 11폴더 표기를 정본과 일치시킴(드리프트 제거).
2-2. **선택 폴더 정책 결정(코튼 결단 필요 · §4)** — `notes/`·`rights/`·`cover/iterations/`·`edit_project/`를 (a)항상 빈 폴더+`.gitkeep` 생성 / (b)필요 시 생성 중 하나로 통일.
2-3. **레거시 면제 표식** — `gymnopedie_1_first_proof`·`greensleeves/omr_audiveris`에 `_LEGACY.md` 한 줄 표식("정본 retrofit 면제, 사유"). 검사 도구가 자동 skip.
2-4. **`muse_project.py doctor`** — work을 정본 대비 lint(누락/잉여 폴더 보고, 레거시 skip).
2-5. **`muse_project.py status`** — 전 works `status.json`을 읽어 한 화면 진척 대시보드(곡·phase·다음 게이트). 라이브 운영 최대 편의.
2-6. **루트 .vpr/.wav 정돈** — work 루트의 `*.vpr`/`Miku_*.wav`(elgar·greensleeves·vivaldi) → `music/renders/`(또는 `music/source_vpr/`)로 이동. 로컬 전용·gitignore 유지, 단지 정돈.

### Phase 3 — 일회성 파일 전역 수명관리
3-1. **전역 독트린 문서** — `planning/_archive` 모델을 `workflows/_TEMPLATE` 또는 루트 `CONVENTIONS.md`에 일반화: "디렉토리별 `_archive/` + 1회용 스크립트 헤더 `# ONE-OFF (날짜·용도)`".
3-2. **`Analytics/_archive/` 신축** + `_mozart_snapshot.py`·`_salut_snapshot.py`·`_compare_meta.py` 이동.
3-3. **`muse_tidy.py` (반자동 sweep)** — `_`프리픽스 + ONE-OFF 태그 스크립트를 스캔 → **목록만 제시**(자동 삭제 X · [[feedback-unknown-dir-investigate]] + 백업 사이드카 보존 독트린 준수). 코튼이 승인한 것만 해당 디렉토리 `_archive/`로 이동.

### Phase 4 — 명명 위생 + 문서 갱신
4-1. `planning/acappella visualization` → `planning/acappella_visualization`(공백 제거).
4-2. **버전 표식 정책 결정(코튼 결단 · §4)** — (a)현행 유지: 본문 s-notation + 단일 정본 파일명 + git 히스토리 / (b)`.vN` 접미사 일관 도입. 권장 = (a)(파일명 증식 방지).
4-3. README.md + USAGE.md를 레지스트리·CONVENTIONS·정본 골격 가리키게 갱신. csv 행/컬럼 수 실측 반영.

### Phase 5 — 검증 (5축 · [[feedback-workflow-verify-axes]])
- `_TEMPLATE` 복사로 throwaway 워크플로우 생성 → registry 등재 → 정상 인지 확인.
- 전 works `doctor` 실행 → 정본 일치/레거시 skip 확인.
- 흩어졌던 스크립트가 改名 후에도 정상 실행되는지 smoke test.
- `git status` 클린 + 문서 상호링크 해소 확인.
- USAGE 순서대로 신규 work 1개 dry-run 스캐폴딩.

---

## 3. 추가 라이브 운영 효율화 방안 (선택 · 큰 레버리지)

| 방안 | 효과 | 비용 | 권장도 |
|------|------|------|--------|
| **A. 단일 `muse.py` CLI dispatcher** | `muse project init/doctor/status`·`muse audio check`·`muse video thumbnail` 한 진입점. 워크플로우 탐색성 ↑ | 중 | ★★★ |
| **B. 공유 visualizer 워크스페이스** | 현재 work마다 Remotion 프로젝트+`npm install` 복제(디스크·시간 낭비). 단일 visualizer 템플릿 + per-work config·assets 주입 → 설치 1회·시각화 개선 전파 자동 | 상(구조 변경) | ★★ (별도 사이클 권장) |
| **C. work `status.json` 스키마 고정 + 검증** | `shared/schemas/`(현재 빈 폴더)에 JSON schema 등재 → status/project.json 게이트 일관 | 중 | ★★ |
| **D. publish 후 메타 자동화 일부** | `post_release_meta_doctrine` 6step 중 기계화 가능분을 Analytics 도구와 연결 | 중 | ★ (Muse 정식 트랙 안착 후) |

---

## 4. 코튼 결단 필요 항목 (착수 전)
1. **선택 폴더 정책** (Phase 2-2): 항상-빈폴더 생성 vs 필요-시 생성.
2. **버전 표식 정책** (Phase 4-2): 현행 유지(권장) vs `.vN` 도입.
3. **추가 방안 채택 범위** (§3): A만? A+C? B는 별도 사이클?
4. **실행 범위/순서**: Phase 1~5 한 번에 vs Phase 1(워크플로우)부터 단계 승인.

---

## 5. 산출물 (완료 시)
- `workflows/README.md` + `registry.json` + `_TEMPLATE/`
- `workflows/project_setup/docs/` 정본 골격 문서 + `doctor`·`status` 명령
- 루트 `CONVENTIONS.md` (아카이빙·명명·일회성 독트린 단일 소스)
- `Analytics/_archive/` + `muse_tidy.py`
- 갱신된 README.md·USAGE.md (드리프트 0)
- (선택) `muse.py` dispatcher

---
*본 계획서는 `planning/_keepers/` 독트린(s371 audit-doc 컨벤션) 양식으로 보관.*
