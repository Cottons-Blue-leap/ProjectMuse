<!--
name: video_release
stage: 4 · 승인된 audio → YouTube package
type: cli+manual
entry: video-brief.md 작성 → Remotion visualizer → export → release/ 패키지 (썸네일 = scripts/muse_thumbnail.py)
inputs: [works/<piece>/music/masters/master.wav, works/<piece>/rights/rights-log.md, works/<piece>/project.json]
outputs: [works/<piece>/video/exports/<piece_id>_final.mp4, works/<piece>/video/release/title.txt, works/<piece>/video/release/description.md, works/<piece>/video/release/credits.md, works/<piece>/video/release/rights-notes.md]
depends_on: [audio_production]
owner: Cotton+MOKA
-->

# Video Release Workflow

This workflow packages an approved music proof into a YouTube-ready music video.
It is intentionally separate from the music workflow.

For the full project-level sequence, read `../../USAGE.md`.

## Input From Upstream Workflows

```text
works/<piece>/music/masters/master.wav
works/<piece>/rights/rights-log.md
works/<piece>/project.json
```

The master audio is produced by `workflows/audio_production`. The arrangement,
role, and MIDI decisions come from `workflows/music_acappella`.

## Main Work Folder (s310 정합)

```text
works/<piece>/video/
  art_sources/        # 명화 원본 + 라이선스 자료
  cover/              # album_1x1.png + (iterations/ 자료)
  visualizer/         # Remotion source code 자리
  exports/            # 최종 mp4 산출
  release/            # 업로드 패키지 (title + description + credits + rights-notes)
```

썸네일은 YouTube 자동 썸네일 활용 (정적 영상이라 별 합성 자리 X · s313 결단).

## Main Documents

- `docs/video_workflow.md`
- `docs/description_template.md`
- `docs/localization.md` — **9개 언어 현지화 doctrine** (release 시 제목·설명 9로케일 / 엔진 `Analytics/localize_batch.py`)
- `docs/post_release_meta_doctrine.md`
- `templates/video-brief.md`
- `templates/visualizer-spec.md`

## Output Package

```text
works/<piece>/video/exports/<piece>_final.mp4
works/<piece>/video/release/title.txt
works/<piece>/video/release/description.md
works/<piece>/video/release/title.<lang>.txt          # 7 신규 로케일 (localize_batch write)
works/<piece>/video/release/description.<lang>.txt    # 7 신규 로케일 (es·pt·de·fr·ru·zh-Hant·zh-Hans)
works/<piece>/video/release/credits.md
works/<piece>/video/release/rights-notes.md
```

## 현지화 (9개 언어 · s393)

release 메타 적용 단계에서 제목·설명을 9개 언어로 push (publish 전). 신곡 = `localize_batch.py WORKS` 에 항목 추가 → `gate`/`review` → 외부 QA → `push --only <vid>` → `audit --only <vid>`. 정본 = `docs/localization.md`.
