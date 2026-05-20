# Project Setup Workflow

본 워크플로우는 *작업 폴더 신축 + project.json 양식*을 담당한다.

음악 / 오디오 / 권리 / 영상 자리와 의도적으로 분리되어 있다. 작업 폴더는 한 번 신축한 후 후속 워크플로우가 같은 `project.json` / `rights/` / `music/` / `video/` 폴더를 공유한다.

## Command

Project Muse root에서:

```powershell
python .\workflows\project_setup\scripts\muse_project.py init `
  --project .\works\<piece_name>
```

`<piece_name>`은 Atelier Ryza 양식 — 짧고 식별성 있게 (e.g. `vivaldi_spring_1_allegro`).

## Created Contract

```text
works/<piece>/
  project.json
  status.json
  README.md
  rights/
    rights-log.md
  notes/
    listening-notes.md
  music/
    renders/dry_stems/
    mix/
      listening-scorecard.csv
    masters/
  video/
    art_sources/
    cover/
    visualizer/
    edit_project/
    exports/
    release/
    video-brief.md
    visualizer-spec.md
```

11 폴더. 음악 자료 (PDF 자체)는 작업 폴더에 복사되지 않음 — `planning/candidates_opus/`에서 직접 reference.

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
