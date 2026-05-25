# YouTube Video Workflow — Atelier Miku Acappella

This workflow is separate from the music production workflow. The music decides
whether the project has value; the video package makes that value legible
without distracting from the sound.

> Series signature: [`../../../README.md`](../../../README.md) § *Series Signature* + [`../../../series_history.csv`](../../../series_history.csv) `signature_mark` 컬럼.
> Character anchor: [`../../../planning/classical_miku_anchor.md`](../../../planning/classical_miku_anchor.md) (Miku 3줄 외형 박힘)
> 두 자료는 매 작품에 prepend. 본 workflow는 곡별 진행 절차.

## Guiding Idea

The video should feel like an album visual, not a tutorial and not a music video
full of cuts.

```text
DAW proof of origin
-> album cover identity
-> restrained vocal visualizer
-> DAW proof of completion
```

## Deliverables

For every finished piece, create:

- Album-cover still image.
- Video edit.
- Visualizer layer.
- YouTube title.
- YouTube description.
- Credits and rights notes.

- Custom YouTube thumbnail (v5 format).

> **썸네일 (s357 supersede · s313 자동썸네일 결정 폐기)**: 더 이상 자동 썸네일(cover 프레임)을 쓰지 않는다.
> 전용 마케팅 표면으로 **custom 썸네일 v5**를 만든다 (3-정보: 명화 / 악곡 / 初音ミク·A CAPPELLA · 좌하단
> 단일 블록 · baseline 앵커링으로 곡 무관 픽셀 동일). 제작·업로드 = **Phase 11 + `docs/thumbnail_guide.md`**.
> 사유: 자동 썸네일은 미쿠가 안 보이고 영어만이라 JP 인식·CTR 약함 (s348 v4 → s357 v5로 진화).

## Phase 1: Video Brief

Create `video/video-brief.md` before making images.

Decide:

- Piece title.
- Release title.
- Original title credit.
- Composer.
- Vocal engine and voice.
- Mood words.
- Visual reference era.
- Painting candidates.
- Candidate CSV artwork match.
- Main color direction.
- Typography direction.
- Letterbox color picks (2~3 hex from the painting, manual).
- Letterbox gradient direction (cover light direction에 따라 dispatch).

채널명·시리즈명은 박힘:

```text
Channel: Atelier Miku Acappella
Search-facing label: Miku Acappella
Precise label (description/about): Miku polyphony · score-faithful
```

Keep the promise modest:

```text
Miku-centered classical acappella experiment
```

Avoid:

- Claiming human choir realism.
- Over-explaining the concept inside the video.
- Making the visual more dramatic than the music.

## Phase 2: Rights And Source Visuals

Use visual sources that can survive public release.

Checklist:

- The painting or artwork source is public domain or clearly licensed.
- The source image page is saved in release notes.
- The generated character image is created for this project.
- Official Miku artwork is not used unless its license permits the release use.
- Font license permits YouTube thumbnails and video use.
- No museum watermark or modern scan branding remains in the final image.

Save:

```text
video/art_sources/source-image-url.txt
video/art_sources/source-rights-notes.md
video/art_sources/<painting_filename>.jpg  # 원본 명화 (수정 X)
```

ChatGPT·image gen sample iteration은 별도 자리:

```text
video/cover/iterations/  # sample 누적 (반복 작업)
```

The candidate master CSV includes one artwork match per piece. Use it as a
starting point:

```text
planning/candidate_master.csv
planning/artwork_matching_guide.md
```

If monetization is possible, be extra conservative with character art and logos.

## Phase 3: Album Cover

> 시리즈 시그너처 적용 의제. [`../../../README.md`](../../../README.md) § *Series Signature* + [`../../../series_history.csv`](../../../series_history.csv) `signature_mark` 컬럼 참조.

1:1 정사각 cover 1건 산출. YouTube 썸네일은 자동 썸네일 활용 (s313 결단) — cover 자체 = 자동 썸네일 base.

### Album Cover Goals

- More elegant than loud.
- Can sit on screen for the full piece.
- Has enough negative space for subtle motion and visualizer.
- Does not look like a meme or game splash screen.
- Readable at small preview size (자동 썸네일 자리에서도 title 읽힘).
- Immediate mood + clear Miku/vocaloid signal.

### Composition (시리즈 시그너처 그리드 박힘)

Lower-left text stack 양식 (4AD art-driven). 시리즈 anchor는 [`../../../README.md`](../../../README.md) § *Series Signature* 참조.

```text
Background:
  public-domain painting (좌상·중앙·우상 dominant)

Subject:
  Classical Miku integrated into the light, brushwork, and palette
  (anchor 3줄 외형 keep, 명화 맥락 따라 의상·자세·소품 가변)

Text stack (좌하단):
  Composer
  Piece Title
  (Subtitle, optional)
```

- 텍스트 alignment: left
- 텍스트 영역은 이미지 좌하단 1/4 quadrant
- 명화 영역 침범 금지 (negative space로 분리)
- 텍스트 위에 캐릭터 face 박지 X (얼굴은 우상단·중앙 자연)

### Image-To-Image Direction

When generating or editing the image:

- Match the painting's light direction.
- Match brush texture and grain.
- Avoid overly glossy anime rendering.
- Keep the character recognizable but painterly.
- Preserve the piece's emotional temperature.
- Generate at ≥2560px (2K 출력 2560×1440에서 커버 표시 ~960px를 받치게 · Phase 9).

### Typography (시리즈 시그너처 lock)

- Typeface: **GFS Didot** (SIL OFL · `Project_Muse/assets/fonts/gfs_didot/`)
- 본 시리즈 전체에 본 typeface 1종만 사용 — 곡별 가변 X
- 강조: size + weight만 (italic·style mix 회피)

Rules:
- Title must be readable at 10 percent preview size (자동 썸네일 자리 정합).
- 두 번째 typeface 추가 금지 (시리즈 일관성 손실).
- Avoid text effects unless needed for contrast.
- Prefer shadow, blur plate, or subtle stroke only when necessary.

곡 mood에 따른 weight 가변은 자유:
- Satie·Debussy: regular weight, generous letter-spacing
- Bach·Pachelbel: regular weight, compact layout
- Romantic: medium weight, slightly larger title

### Channel Wordmark (시리즈 시그너처 §3 정합 · s320 v3 update)

cover 우하단 corner에 *Atelier Miku Acappella* wordmark 박음 (좌하단 title mirror axis · 좌·우 visual symmetry). 클래식 메이저 label corner 양식 (DG·EMI·Sony Classical) 정합.

```text
+----------------------------+
|                            |
|   [명화 + 미쿠]            |
|                            |
|                            |
|                            |
|                            |
| Composer       Atelier Miku|  ← 좌하단 text + 우하단 wordmark mirror
| Piece Title         Acappella|     (좌·우 mass balance · 자료 base mirror)
+----------------------------+
```

양식 (시리즈 anchor · 작품별 가변 X):
- text: *Atelier Miku Acappella* (전체 channel 이름)
- typeface: GFS Didot (시그너처 typeface 1종 keep)
- weight: regular (강조 X · 명화 압도 회피)
- size: 좌하단 piece_title size 자체엔 ~70-80% (16:9 frame 자체엔 size 40 default · 좌측 piece_title 56 base)
- 자리: 우하단 corner · margin_right 81 + margin_bottom 90 (좌측 title margin axis mirror)
- 색조: cream `#e8e0c8` (좌측 text 색 정합) + *Miku*의 *M* 자체엔 banner 청록 `rgb(40, 180, 175)` (시리즈 brand color)
- text-shadow: `0 2px 12px rgba(0, 0, 0, 0.75)` (좌측 text-shadow 양식 정확 mirror · 시인성 + 정합)
- opacity: 1.0 (자료 base)

작품별 결단 자리 (가변 매우 작음):
- 곡별 `video-brief.md`에 `wordmark_notes` 박음 (예: cover 우하단 자리 dense axis · opacity adjust 의제 등)
- 색조 자체엔 시리즈 anchor 자료 base · 작품별 변경 X

본 양식 1:1 cover still + 16:9 video frame 둘 다 적용 (16:9 frame 자리 = Phase 5 참조).

적용 timing:
- 신규 작품부터 default 적용
- **scheduled publish 양식 작품 자체엔 retrofit OK** (publish 통과 X · scheduled cancel + 새 upload + 다시 schedule path · 새 URL 박힘)
- publish 통과 자료 retrofit X (URL 변경 + metric 영구 잃음 + algorithm boost 7일 손실 axis · 매우 강 cost)
- 비발디 자체엔 s320 본 cycle 자체엔 scheduled publish 양식 base 자체엔 retrofit 통과

상세 = `../../../series_history.csv` `signature_mark` 컬럼 (wordmark 양식 evolution 자료 추적).

## Phase 4: Process Capture (skipped)

2026-05-11, cotton decision: acappella-only path with no DAW. Phase removed.
Open on the album cover instead.

## Phase 5: Main Video Timeline

영상 frame = 16:9 · composition 1920×1080 좌표계 → 출력 2560×1440 (2K · `--scale=1.333` · Phase 9). Cover = 1:1 정사각, frame 가운데에 박힘.
좌·우 negative space = letterbox (시리즈 시그너처 §5 명화 색조 그라데이션).

Frame 구조:
```text
+----[letterbox L]--[cover 1:1]--[letterbox R]----+
|                                                  |
|     gradient L      (album         gradient R   |
|     deep teal →     cover          → muted gold |
|     hex pick 1)     in here)       (hex pick 2) |
+-------------------------------------------------+
```

우하단 channel wordmark = 시리즈 시그너처 §3 정합 (s320 v3 박힘). 자리 = frame 우하단 corner · margin_right 81 + margin_bottom 90 (좌하단 title margin axis mirror). 좌·우 visual symmetry · mass balance. 양식 상세 = Phase 3 §Channel Wordmark.

Default structure (acappella-only, no DAW capture):

```text
00:00-00:08
  fade in to album cover (letterbox + cover 동시 fade)

00:08-end minus 5s
  album cover with restrained visualizer

last 5s
  slow fade to credits or end card
```

The exact durations should follow the music. If the piece begins with a fragile
attack, let the first visual dissolve be slower.

## Phase 6: Motion Design

Current use (s310 박힘): static cover + fade in/out + visualizer bars only.
Motion design 자체 시리즈 양식 *덜 박음* 본질 정합.

Optional future polish (currently unused):

- Slow 2~4% push-in
- Subtle parallax between background and character
- Film grain or paper texture
- Light shimmer tied to vocal energy

Avoid:

- EDM spectrum bars
- Large bouncing waveforms
- Fast particle bursts
- Constant zooming
- Camera moves that feel like a trailer

## Phase 7: Visualizer Design

Current use (s310 박힘): vertical bars in letterbox area.

```text
Letterbox vertical bars:
  32 bars per side (left + right · 64 total)
  9시 = 0Hz · 시계방향 freq 증가
  좌 = low band [0..31] · 우 = high band [32..63]
  bar width 3px · opacity 0.6 · center anchored · pill 양식
  bar color = letterboxColors[2] (light cream tone) auto
  per-bar amplification curve (1.0 → high factor · exp 1.4) — 곡별 axis 가변
  sqrt amplitude scaling
```

Detailed spec per piece: `templates/visualizer-spec.md`.

Optional future designs (currently unused):

- Stem rings (one thin line per Miku role)
- Breath waveform (horizontal line that widens with phrase energy)
- Choral aura (faint light field driven by RMS energy)
- Score pulse (small vertical glows aligned with phrase starts)

Visualizer constraints:

- Never cover the title
- Never obscure the character face
- Stay readable under YouTube compression
- Calm during silence and reverb tails
- Bars stay in letterbox area (cover 1:1 영역 침범 금기)

## Phase 8: Edit And Audio

Use the mastered audio as the authority.

Checklist:

- Audio starts exactly with the music.
- No accidental fade-in unless intended.
- Video cuts happen under musical phrasing.
- Final video uses the approved master only.
- No limiter or loudness processing is added in the video editor.

## Phase 9: Export Specs

Recommended (s310 박힘 · **2K 표준 = 2026-05-25 코튼 결단**):

```text
Video frame:
  16:9
  composition 1920×1080 (코드 좌표계 keep) → 출력 2560×1440 (2K / 1440p)
  렌더 = remotion render ... --scale=1.333   ← composition 무변경 (px 하드코딩 보존)
  ~1.78× render cost (4K 대비 절반 이하)
  30 fps
  H.264 High Profile
  BT.709 SDR
  progressive scan
  cover 1:1 + letterbox gradient 양 옆 (Remotion이 frame 자체 산출)

Audio:
  stereo
  48 kHz
  AAC-LC or PCM before final encode

Album cover still (1:1 · 외부 배포 · 자동 썸네일 base):
  ≥2560×2560 (2K 커버 표시 ~960px를 충분히 받침 · 3840×3840이면 향후 4K 여지)
  PNG (transparency 자료가 visualizer에 쓰일 가능성)
```

**왜 2K (4K 아님)**: 유튜브가 1440p+에 주는 고급 코덱(VP9)으로 1080p(AVC)보다 선명 + 명화
디테일 품격 + 에버그린 아카이브 가치. 4K 기각 = 커버 소스(현 1254px)가 4K 커버 표시(1920px)
미달 + 정적 콘텐츠(중앙 정사각 커버 + 레터박스)라 오버킬 + 렌더 4배. **기존 publish 영상은
retrofit X** (재업로드 = URL·metric·algorithm boost 손실) — 신곡부터 적용.

For a mostly static music visual, 30 fps is enough.

Filename convention (work folder):
```text
video/cover/album_1x1.png       # 1:1 cover still (Atelier 시그너처 · 자동 썸네일 base)
```

(thumbnail.png 자리 폐기 — YouTube 자동 썸네일 활용 · s313 결단 · 정적 영상이라 자동 썸네일 충분.)
(youtube_frame.png 자리 폐기 — Remotion이 frame 자체 산출 통과 path.)

## Phase 10: Quality Control

Watch the full video at least three times:

1. Fullscreen desktop.
2. Phone-sized preview.
3. Low volume, then normal volume.

Check:

- Cover title is readable (자동 썸네일 자리에서도 통과).
- No text is cut off.
- No visualizer flicker is unpleasant.
- Audio is in sync.
- Reverb tail is not cut.
- Last frame feels intentional.
- Description credits match the actual sources.

## Phase 11: Upload Package

Prepare:

```text
video/exports/<piece>_final.mp4     # final video (e.g. gymnopedie_1_final.mp4)
video/release/title.txt
video/release/description.md
video/release/credits.md
video/release/rights-notes.md
```

### Custom thumbnail (v5 · s357)

```text
video/thumbnail_v5.jpg               # custom 썸네일 (자동 썸네일 폐기 · s357)
```

- 생성: `python workflows/video_release/make_thumbnail.py --song <name>` (신곡은 `REGISTRY`에 dir/cover/box/composer/piece 추가 → `--song`).
- 검수: ~210px로 줄여 初音ミク 읽힘·블록 균형 확인.
- 업로드(라이브, 이미지만 교체): `python Analytics/youtube_meta.py set-thumbnail <video_id> <thumbnail_v5.jpg>`.
- 양식·디자인 LOCK·폰트 의존성 = `docs/thumbnail_guide.md`. (cover still은 여전히 제작하되 *썸네일 ≠ cover* — 전용 v5를 따로 만든다.)

Title format examples:

```text
Satie - Gymnopédie No. 1 | Atelier Miku Acappella
Pachelbel - Canon in D | Atelier Miku Acappella
Bach - Prelude in C Major | Atelier Miku Acappella
```

채널명 suffix는 시리즈 시그너처 keep. *acappella*는 search-facing label (외부 발견용), description·about에는 *Miku polyphony · score-faithful*로 정밀화.

For playful title rules, use `planning/title_naming_guide.md` and the
`release_title` / `original_title_credit` columns in
`planning/candidate_master.csv`.

Description should include:

- Composition source.
- Arrangement credit.
- Vocal engine/voice.
- Visual source.
- No instrumental audio note, if true.
- Rights notes for public-domain sources.

## Phase 12: Post-Release Review

After release, record:

- Audience reaction.
- Retention dips.
- Comments about sound quality.
- Comments about visual identity.
- Thumbnail CTR (Studio 도달범위) — does the v5 custom thumbnail convert impressions to clicks.
- Whether the next piece should be more Miku-only or more hybrid.

The goal is not only views. The goal is whether listeners accept the sound as
music before they accept it as a concept.
