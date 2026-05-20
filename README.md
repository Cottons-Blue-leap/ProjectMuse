# Project Muse

Project Muse is organized as a chain of small workflows around shared work
projects.

```text
Project_Muse/
  workflows/
    project_setup/
    rights_clearance/
    music_acappella/
    audio_production/
    video_release/
    shared/

  planning/
    candidate_master.csv
    candidates_opus/             # source score PDFs
    classical_miku_anchor.md
    title_naming_guide.md
    artwork_matching_guide.md

  works/
    <piece_name>/
      rights/
      notes/
      music/
      video/
```

## Workflows

- `workflows/project_setup`: piece workspace creation and `project.json`
  manifest contract.
- `workflows/rights_clearance`: score, voicebank, character, visual, and
  release rights decisions.
- `workflows/music_acappella`: V6 entry reference — role taxonomy, syllable
  guide, vocal polishing notes (source PDF 자체엔 `planning/candidates_opus/`
  자료 직접 reference · 별 score ingestion 워크플로우 X · s302 cut).
- `workflows/audio_production`: V6 dry renders, stem checks, light acappella
  assembly (level matching + optional reverb · no DAW), listening critique,
  and approved master audio.
- `workflows/video_release`: album-cover, visualizer, video edit, and YouTube
  release package. (YouTube 자동 썸네일 활용 — 별 썸네일 합성 자리 X · s313 결단.)
- `workflows/shared`: cross-workflow templates and schemas only.
- `planning`: candidate repertoire and early selection notes.

For the full step-by-step usage flow, read [USAGE.md](USAGE.md).

## Series Signature — Atelier Miku Acappella

Shared visual anchor across every release: **GFS Didot** typeface · **lower-left text stack** · **1:1 album cover** · **letterbox gradient** hand-picked from each painting. Per-work signature variation (e.g. corner wordmark version) is tracked in `series_history.csv` via the `signature_mark` column (`none`, `wordmark_v3`, …).

Character anchor (3-line outline): [`planning/classical_miku_anchor.md`](planning/classical_miku_anchor.md).

## Create A New Piece

From this folder:

```powershell
python .\workflows\project_setup\scripts\muse_project.py init `
  --project .\works\canon_in_d_first_proof
```

The generated work project will contain both `music/` and `video/` folders, but
the workflows stay separate.

## Release History

Channel: **Atelier Miku Acappella** ([@AtelierMikuAcappella](https://www.youtube.com/@AtelierMikuAcappella))

| # | Piece | Composer | Released | Folder |
|---|---|---|---|---|
| 1 | Gymnopédie No. 1 | Erik Satie | 2026-05-14 | `works/gymnopedie_1_first_proof/` |
| 2 | Spring (RV 269), Mvt. I Allegro | Antonio Vivaldi | 2026-05-18 | `works/vivaldi_spring_1_allegro/` |
| 3 | The Entertainer | Scott Joplin | 2026-05-21 (scheduled) | `works/joplin_the_entertainer/` |

상세 publish 자료 = `series_history.csv`.

## Proof Goal Doctrine

각 proof 작품 양식:

```text
acappella-only (no instrumental audio)
V6 dry stems primary
light assembly (level matching + optional reverb · no DAW)
video package only after the music is worth presenting
```
