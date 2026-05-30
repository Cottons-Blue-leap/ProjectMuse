# Project Muse

Project Muse is organized as a chain of small workflows around shared work
projects.

```text
Project_Muse/
  muse.py                        # 단일 CLI 디스패처
  muse_tidy.py                   # 일회성 파일 sweep
  CONVENTIONS.md                 # 명명·아카이빙·일회성 독트린
  workflows/
    README.md  registry.json     # 워크플로우 인덱스 + 머신리더블 레지스트리
    _TEMPLATE/                   # 새 워크플로우 복사 골격
    project_setup/  rights_clearance/  music_acappella/
    audio_production/  video_release/  shorts_first_proof/
    shared/                      # 공유 템플릿·스키마
  planning/
    candidate_master.csv         # 353곡 · 14 컬럼
    candidates_opus/             # source score PDFs
    _archive/  _keepers/         # 닫힌 cycle 산출물 · 미래 reference
  Analytics/                     # YouTube 메트릭 도구 (+_archive/ 1회용)
  works/<piece>/                 # 작품 폴더 (정본 골격 · muse.py doctor)
```

## Workflows

전체 인덱스 + 파이프라인 순서 = [`workflows/README.md`](workflows/README.md) · 머신리더블 = [`workflows/registry.json`](workflows/registry.json).

- `workflows/project_setup`: piece workspace 신축 + `project.json` 계약 + `doctor`/`status` 도구.
- `workflows/rights_clearance`: score, voicebank, character, visual, release 권리 결단.
- `workflows/music_acappella`: V6 entry reference — role taxonomy, syllable, vocal polishing (PDF는 `planning/candidates_opus/` 직접 reference · s302 cut).
- `workflows/audio_production`: V6 dry renders, stem checks, light assembly (no DAW), 청취 평가, master.
- `workflows/video_release`: album-cover, visualizer, video edit, YouTube release package + `scripts/muse_thumbnail.py`.
- `workflows/shorts_first_proof`: 본 영상 publish + 1달 → 쇼츠 1편 (s371).
- `workflows/shared`: cross-workflow templates + schemas.
- `planning`: candidate repertoire + selection notes.

전 프로젝트 명명·아카이빙·일회성 독트린 = [`CONVENTIONS.md`](CONVENTIONS.md). 전체 사용 흐름 = [USAGE.md](USAGE.md).

## Series Signature — Atelier Miku Acappella

Shared visual anchor across every release: **GFS Didot** typeface · **lower-left text stack** · **1:1 album cover** · **letterbox gradient** hand-picked from each painting. Per-work signature variation (e.g. corner wordmark version) is tracked in `series_history.csv` via the `signature_mark` column (`none`, `wordmark_v3`, …).

Character anchor (3-line outline): [`planning/classical_miku_anchor.md`](planning/classical_miku_anchor.md).

## Create A New Piece

From this folder:

```powershell
python .\muse.py project init --project .\works\canon_in_d_first_proof
python .\muse.py doctor          # 정본 골격 검사 (전 작품)
python .\muse.py status          # 전 작품 진척 대시보드
python .\muse.py list            # 등록 워크플로우 목록
```

(각 워크플로우 스크립트를 직접 실행해도 됨 — `muse.py`는 얇은 디스패처.)

The generated work project will contain both `music/` and `video/` folders, but
the workflows stay separate.

## Release History

Channel: **Atelier Miku Acappella** ([@AtelierMikuAcappella](https://www.youtube.com/@AtelierMikuAcappella))

| # | Piece | Composer | Released | Folder |
|---|---|---|---|---|
| 1 | Gymnopédie No. 1 | Erik Satie | 2026-05-14 | `works/gymnopedie_1_first_proof/` |
| 2 | Spring (RV 269), Mvt. I Allegro | Antonio Vivaldi | 2026-05-18 | `works/vivaldi_spring_1_allegro/` |
| 3 | The Entertainer | Scott Joplin | 2026-05-21 | `works/joplin_the_entertainer/` |
| 4 | Salut d'Amour | Edward Elgar | 2026-05-25 | `works/elgar_salut_damour/` |
| 5 | Twelve Variations on "Ah, vous dirai-je, maman" K.265 | W. A. Mozart | 2026-05-28 | `works/mozart_twinkle_variations_k265/` |

상세 publish 자료 = `series_history.csv`.

## Proof Goal Doctrine

각 proof 작품 양식:

```text
acappella-only (no instrumental audio)
V6 dry stems primary
light assembly (level matching + optional reverb · no DAW)
video package only after the music is worth presenting
```
