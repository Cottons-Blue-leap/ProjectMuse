# Project Muse Usage Guide

본 가이드는 분리된 워크플로우의 진행 순서를 박는다 (s302 리팩토링 + 후속 cut 통과 양식).

```text
project_setup    -> 작업 폴더 + project.json 신축
rights_clearance -> source + release 권리 정합
music_acappella  -> V6 entry reference (role taxonomy / syllable doc · 코튼이 V6 시점 참고)
audio_production -> V6 dry stem 점검 + light assembly + master
video_release    -> 결단된 audio를 YouTube package로 박음
shared           -> 워크플로우 간 공유 양식
works            -> 곡 작업 폴더
planning         -> 곡 후보 + PDF (`candidates_opus/`) + 시그너처 자산
```

모든 명령은 Project Muse root에서:

```powershell
cd C:\Users\user\Desktop\myProject\Project_Muse
```

## 1. Pick A Piece

`planning/candidate_master.csv` (340곡 · 14 컬럼)에서 axis throw → 후보 추출 → 코튼 결단. 본 자리에서 *디렉토리 이름* + *명화* + *재생목록* + *진입 timing* 결단.

PDF는 `planning/candidates_opus/`에 모여있어. csv `score_file` 컬럼이 채워진 곡 = PDF 박혀있음.

## 2. Create A Piece Workspace

식별성 있고 짧은 작업 폴더 이름 (Atelier Ryza 양식 — e.g. `vivaldi_spring_1_allegro`):

```powershell
python .\workflows\project_setup\scripts\muse_project.py init `
  --project .\works\vivaldi_spring_1_allegro
```

신축 결과 (11 폴더):

```text
works/vivaldi_spring_1_allegro/
  project.json
  status.json
  README.md
  rights/
  notes/
  music/
    renders/dry_stems/
    mix/
    masters/
  video/
    art_sources/
    cover/
    visualizer/
    edit_project/
    exports/
    release/
```

PDF는 작업 폴더에 복사되지 않음. `planning/candidates_opus/`에서 직접 reference.

## 3. Fill Metadata + Rights

`project.json`에 piece / composer / section 박음. `source_score_planning` 키는 `planning/candidates_opus/<filename>.pdf` 양식.

`rights/rights-log.md` 채움:
- source authority + edition
- composition copyright 상태 (PD 여부 + 사망 연도)
- edition copyright 상태 (출판사 + 출판 연도)
- cover art copyright 상태 (명화 + 화가 사망 연도)
- 보이스뱅크 라이센스 정합

본 자리가 clean하지 않으면 멈춤.

## 4. V6 Direct Entry (코튼 직접)

코튼이 `planning/candidates_opus/<곡>.pdf`를 V6 editor 옆에 펴두고 piano roll에 직접 음표 + 음절 + dynamics 입력.

별 doc 자리 없음 (s302 cut). 편곡 결단 (살릴 자리 / omit / octave / 텍스처 / 음절) + role 결단 + 음절 결단 다 V6 안에서 박힘.

V6 시점 참고 자료 (선택):
- `workflows/music_acappella/docs/role_taxonomy.md` — 6 role 의미
- `workflows/music_acappella/docs/instrument_pronunciation.md` — 음절 + 발음 reference
- `workflows/music_acappella/docs/vocal_polishing.md` — V6 시점 결단 axis

각 role을 별 track으로 분리해서 dry export 준비.

## 5. Render Dry Miku Stems

V6에서 각 role을 dry로 export:

```text
no reverb
no master limiter
same start time
same sample rate
same bit depth
one role per WAV
```

추천 = 48 kHz / 24 bit WAV. 저장 자리:

```text
works/<piece>/music/renders/dry_stems/
```

추천 이름:

```text
lead_miku_ah.wav
lead_double_ah.wav
halo_high_oo.wav
mid_oo.wav
low_oo.wav
air_mm.wav
```

상세 = `workflows/audio_production/README.md`.

## 6. Check The Stems

```powershell
python .\workflows\audio_production\scripts\muse_audio.py check-stems `
  --stems .\works\<piece>\music\renders\dry_stems `
  --out .\works\<piece>\music\mix\stem-report.json `
  --expected lead_miku_ah.wav,mid_oo.wav,low_oo.wav
```

`stem-report.json` 점검:
- mismatched sample rate
- mismatched duration
- clipping
- missing stems

## 7. Assemble The Proof (Acappella-only · light-touch)

2026-05-11 코튼 결단: DAW 믹스 제거. V6 dry stem 6개가 primary deliverable. assembly는 가볍게.

도구 옵션 (하나 선택):
- V6 GUI의 built-in master export.
- Audacity (무료, non-DAW).
- Python `assemble-proof` (`workflows/audio_production/scripts/muse_audio.py`).

순서:
1. Level-match (loudest stem ≤ -3 dBFS peak).
2. (선택) one shared gentle hall reverb (≤ 1.5s decay).
3. Sum to single file.
4. Check mono.
5. Check low volume.
6. Export proof master.

EQ / 압축 / per-stem 처리 없음. stem이 문제면 V6에서 다시 render.

저장 자리:

```text
works/<piece>/music/masters/master.wav
```

```powershell
python .\workflows\audio_production\scripts\muse_audio.py assemble-proof `
  --stems .\works\<piece>\music\renders\dry_stems `
  --include lead_miku_ah.wav,mid_oo.wav,low_oo.wav `
  --out .\works\<piece>\music\masters\master.wav `
  --report .\works\<piece>\music\mix\assembly-report.json
```

## 8. Listening Decision

```text
works/<piece>/music/mix/listening-scorecard.csv
```

결단 axis:

```text
Green   -> 진행 (video 자리)
Yellow  -> 곡 / key / register / 음절 결단 다시
Red     -> 멈춤
```

## 9. Video Workflow

audio가 publish할 만큼 통과한 후에만 video 진입.

```text
works/<piece>/video/video-brief.md
works/<piece>/video/visualizer-spec.md
```

상세 = `workflows/video_release/docs/video_workflow.md` + `README.md` § *Series Signature*.

작업 폴더:
```text
video/art_sources/
video/cover/
video/visualizer/
video/edit_project/
video/exports/
video/release/
```

## 10. YouTube Package

```text
works/<piece>/video/exports/final_4k.mp4
works/<piece>/video/release/title.txt
works/<piece>/video/release/description.md
works/<piece>/video/release/credits.md
works/<piece>/video/release/rights-notes.md
```

썸네일은 YouTube 자동 썸네일 활용 (정적 영상이라 별 합성 자리 X · s313 결단). cover 자체 = 자동 썸네일 base.

Upload 전 점검:
- reverb tail이 잘리지 않음
- source credit이 rights-log와 정합
- 영상이 approved master audio만 사용

publish 후 자리 = `workflows/video_release/docs/post_release_meta_doctrine.md` 6 step.

## MOKA ↔ 코튼 영역

`workflows/music_acappella/docs/role_division.md` 양식 정합. MOKA = 곡 선정 보조 + 권리 자료 + 영상 양식 + 청취 평가 + publish 후 메타 update. 코튼 = 음악 결단 + V6 입력 + 영상 미학 결단 + sign-off.
