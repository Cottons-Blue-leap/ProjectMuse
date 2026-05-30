<!--
name: project_setup
stage: 0 · 작업 폴더 + project.json 신축
type: cli
entry: python ./workflows/project_setup/scripts/muse_project.py init --project ./works/<piece_id>
inputs: []
outputs: [works/<piece>/project.json, works/<piece>/status.json, works/<piece>/ 정본 11폴더]
depends_on: []
owner: MOKA
-->

# Project Setup Workflow

본 워크플로우는 *작업 폴더 신축 + project.json 양식*을 담당한다.

음악 / 오디오 / 권리 / 영상 자리와 의도적으로 분리되어 있다. 작업 폴더는 한 번 신축한 후 후속 워크플로우가 같은 `project.json` / `rights/` / `music/` / `video/` 폴더를 공유한다.

## Commands

Project Muse root에서:

```powershell
# 신축
python .\workflows\project_setup\scripts\muse_project.py init --project .\works\<piece_name>

# 정본 골격 검사 (전 작품 lint · CORE 누락 = FAIL · 루트 오배치 = WARN)
python .\workflows\project_setup\scripts\muse_project.py doctor
python .\workflows\project_setup\scripts\muse_project.py doctor --fix       # 누락 CORE 폴더 .gitkeep 생성
python .\workflows\project_setup\scripts\muse_project.py doctor --project .\works\<piece_name>

# 전 작품 진척 대시보드 (status.json: phase / video / last_decision)
python .\workflows\project_setup\scripts\muse_project.py status
```

`<piece_name>`은 Atelier Ryza 양식 — 짧고 식별성 있게 (e.g. `vivaldi_spring_1_allegro`).

## Created Contract (정본 골격)

```text
works/<piece>/
  project.json · status.json · README.md
  rights/      rights-log.md           [CORE]
  notes/       listening-notes.md      [CORE]
  music/
    mix/  listening-scorecard.csv      [CORE]
    renders/dry_stems/                 [LOCAL · .gitignore renders/]
    masters/                           [LOCAL · .gitignore masters/]
    source_scores/                     [LOCAL · V6 진입 시 ASCII PDF copy]
  video/
    art_sources/ cover/ visualizer/    [CORE]
    exports/ release/                  [CORE]
    edit_project/                      [LOCAL · 외부 편집 사용 작품만]
    video-brief.md · visualizer-spec.md
```

- **CORE** = git 영속 골격. 항상 생성 + 빈 폴더는 `.gitkeep`으로 영속화 (clone 시 골격 일관). `doctor` 누락 = **FAIL**.
- **LOCAL** = 스캐폴더가 만들지만 내용물이 `.gitignore` 대상(렌더·마스터·바이너리)인 로컬 작업 폴더. git 영속 불가 → `.gitkeep` X. `doctor` 누락 = info.
- 음악 자료 (PDF 자체)는 작업 폴더에 복사되지 않음 — `planning/candidates_opus/`에서 직접 reference.
- 레거시 작품은 루트 `_LEGACY.md` 표식 → `doctor` 자동 skip (현 정본 retrofit 면제).
- 작업 폴더 루트의 `.vpr`/`.wav`/`.mp4` = `doctor` WARN (naming_convention: `music/` 하위가 정본 · 자동 이동 X · 수동 결단).

(thumbnail-brief.md scaffold 자리 폐기 · s313 결단 · YouTube 자동 썸네일 활용 path · 별 썸네일 합성 자리 X.)

## Handoff Rules

- `project.json`은 후속 워크플로우가 먼저 read하는 manifest. `music.source_score_planning`이 PDF 경로 (planning/ 안).
- `rights/rights-log.md`는 source / music / audio / video 결단이 공유.
- `music/renders/dry_stems/`는 V6 dry stem 자리.
- `music/masters/master.wav`는 video_release로 들어가는 audio handoff.

## s302 리팩토링 + 후속 cut 흡수

본 워크플로우는 두 번 정리됨:

**s302 1차 (자동화 path 폐기):**
- `music/midi/auto_export/` + `music/midi/render_ready_v1/` (자동 MIDI 추출)
- `music/render_studies/` (옛 OMR/MIDI 실험)
- `muse_doctor.py` (자동 phase 결정)
- `muse_workflow.py` (init만 살아있던 통합 스크립트)

**s302 후속 (형식주의 doc 폐기 · 코튼 결단):**
- `music/source_scores/` (PDF는 planning/에서 직접 reference)
- `music/analysis/` + arrangement-brief.md (MOKA가 PDF 분석 doc 박는 자리 자체 폐기)
- `music/arrangement/` + acappella-arrangement.md (편곡 결단은 V6 안에서 박힘)
- `music/vocaloid/` + role-design.md + pronunciation-map.csv (role + 음절 결단도 V6 안에서)
- `workflows/score_ingestion/` 통째 폐기 (PDF + rights만 남고 본 자리는 rights_clearance에 흡수)
