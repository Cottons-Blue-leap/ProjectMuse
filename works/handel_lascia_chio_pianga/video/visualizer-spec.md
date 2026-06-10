# Visualizer Spec

> 시리즈 시그너처 = [`../../../README.md`](../../../README.md) § *Series Signature* + [`../../../series_history.csv`](../../../series_history.csv) `signature_mark` 컬럼.
> Reference 양식 = `Project_Muse/works/gymnopedie_1_first_proof/video/visualizer/` (Remotion · s279 박힘 · project scaffold) + frame 2K wrap = 작은별 K.265 (s361).
> **Sound-viz 컴포넌트 신형(s381 band-remap) reference = [`visualizer-composition.s381-bandremap.tsx`](visualizer-composition.s381-bandremap.tsx)** (신곡 ⑥부터).
> 도구 = Remotion (s276 박힘 · s279 본격 양식 박힘).

## Concept

- Visualizer name: 시리즈 공통 양식 (B 공유 엔진 · ★ 신곡 첫 적용 = props.json + public 주입 + `python muse.py render handel_lascia_chio_pianga`)
- Relationship to music: 단악장 아리아 (A–B–A' da capo · 225.0s) → variationStarts=[0], variationLabels=[""] (챕터 라벨 미표시)
- Relationship to cover image: 커버 = Rossetti Proserpine 미쿠 치환 (1254×1254). 레터박스 = **D_farinelli_ivory `#181614 #6F6A60 #D8D2C4`** (코튼 최종 LOCK 2026-06-11 round 2 · 무채=파리넬리 흰색 상징[카스트라토 순수·텅 빈 마음] · 시리즈 첫 무채 = 첫 원곡 성악 예외 면허 · 갤러리 액자 효과 · bar 근백색='하얀 목소리' · round 1 C 브론즈는 superseded · 상세 = art_sources/letterbox_candidates/README.md). bar 색 = #D8D2C4 자동.

## 시리즈 공통 양식 (변경 X)

본 양식은 시리즈 모든 곡 공통 keep. 변경 시 시리즈 시그너처 reset 본질.

- **Frame**: Composition 2560×1440 (2K · 16:9) · 내부 1920×1080 좌표계 wrap 양식 (default = s361 박힘 · 작은별 K.265 첫 적용 · 신곡 default · 기존 publish 작품 retrofit X)
- **Cover**: 720×720 center (1920×1080 좌표계 안 · wrap scale 4/3 후 출력 자리엔 960×960 박힘)
- **Letterbox**: cover 외곽 4방향 (좌 600 · 우 600 · 위 180 · 아래 180 · 1920×1080 좌표계)
- **Letterbox gradient**: vertical 3 stop (props 자료)
- **Text stack**: 좌하단 frame 자리 (left 80 · bottom 60) · GFS Didot · composer 32px / piece 56px / subtitle 26px italic
- **Sound visualization** (s381 supersede · 미쿠 실측 대역 정합 · **신곡 ⑥ 쇼팽부터 default** · 발행 ①~⑤ = 구 linear 양식 retrofit X):
  - 입력: `visualizeAudio(numberOfSamples 2048)` = 선형 FFT (~10.8 Hz/bin) → **64 display bar로 로그 재버킷팅** (`logBars()`)
  - **대역 = 60 Hz ~ 6 kHz · 로그 스케일.** 근거 = 미쿠 V6 실측 점유대역(에너지 98% in 320Hz–2.6kHz · 최저음 F#2 92Hz · >5kHz 무음) → `exploration/feedback_review_s381/`
  - 좌우 분할 = 1 kHz (에너지 중앙값): 좌 32바 = 60–1000Hz(기음·멜로디) · 우 32바 = 1000–6000Hz(배음·치찰음) · 9시=저역 · 바깥=고역
  - per-bar 값 = max(대역내 linear bin) ∪ 중심주파수 선형보간(sub-bin 저역바용) · `min(1, v×GAIN)` clamp
  - **spectral tilt** (저음쏠림 보정 필수) = amplification 1.0 → **3.5** · exp 1.0 (고역 점진 리프트 = 자연 롤오프 상쇄)
  - **SPECTRUM_GAIN 3.0** (정제미 절제 · 코튼 lock s381 · 4.0→3.0 한 발 더 다운) · sqrt amplitude scaling
  - **temporal smoothing (s381b · 코튼 승인)**: 어택 즉시 + **릴리스 ~0.27s** (decaying-max look-back `SMOOTH_RELEASE_FRAMES 8` · `SMOOTH_DECAY 0.82`). 소리 그쳐도 바가 *서서히 잦아듦* → "없다↔있다" 팝핑 제거. 구현 = `mkBars()`가 frame·frame-1..-8의 rebucket을 decaying max로 합성 (visualizeAudio 프레임 캐시로 비용 amortize)
  - **baseline `BAR_MIN_HEIGHT 8`** (s381b · 4→8): 무음에도 옅은 바닥선 유지 = 완전한 "없다" 상태 제거 (정제미 resting state)
  - bar width 3px · opacity 0.6 · center anchored · pill
  - reference 구현 = [`visualizer-composition.s381-bandremap.tsx`](visualizer-composition.s381-bandremap.tsx)
  - ⚠ chapter-label 블록은 K.265(변주곡) 전용. 단악장 곡은 `variationStarts=[0]`, `variationLabels=[""]` 전달(라벨 미표시) 또는 블록 제거.
- **구 양식 (발행 ①~⑤ · 변경 X · retrofit X)**: `visualizeAudio(numberOfSamples 64)` 선형 0–22kHz · 좌 low[0..31]/우 high[32..63] · amp 1.0→6~7 exp1.4
- **Fade in**: 3s 양식 (frame 0~90 @ 30fps)
- **Audio**: `<Audio>` + `useAudioData` + `visualizeAudio` (신곡 numberOfSamples 2048 · 구 64)
- **Font**: GFS Didot · staticFile + FontFace API · delayRender 양식

## 곡별 가변 자료 (props)

```tsx
{
  letterboxColors: ["#hex1", "#hex2", "#hex3"], // 명화 주조색 3 stop
  composerName: "...",
  pieceTitle: "...",
  pieceSubtitle: "...", // optional
  audioPath: "audio.wav",
  coverPath: "cover.png",
}
```

bar color는 `letterboxColors[2]` (마지막 stop) 자동 변환 → 명화별 자동 가변.

## 곡별 axis 결단 자료 (visualizer-spec 박힘 의무)

본 spec 자료 자료에 다음 곡 결단 박힘:

### Audio Inputs

- Master audio path: `music/masters/Miku_handel_lascia_chio_pianga_master.wav` (→ `video/visualizer/public/audio.wav` 복사 주입)
- Audio duration: 225.0s (224.998957 · 6750 frames @ 30fps)
- Audio sample rate / bit depth: 44.1kHz / 24-bit stereo

### Motion / Amplitude 자료

> **신형(s381 band-remap) = 진폭값 고정 · 곡별 튜닝 거의 불요** (로그 대역 + 고정 게인이 자가 정규화). 아래 짐노페디/구 양식 값은 발행 ①~⑤ 기록용.

- **신형 고정값 (s381 lock)**: `SPECTRUM_GAIN 3.0` · `AMPLIFICATION_HIGH 3.5`(tilt) · `AMPLIFICATION_CURVE 1.0` · `BAR_MAX_AMPLITUDE_HEIGHT 400` · `BAR_MIN_HEIGHT 8`(baseline) · `SMOOTH_RELEASE_FRAMES 8` · `SMOOTH_DECAY 0.82`(릴리스)
- **Bar amplitude cap (`BAR_MAX_AMPLITUDE_HEIGHT`)** [구 양식]:
  - 짐노페디 sample = 220 (sparse · 정적 mood 양식 정합)
  - 곡 dynamic 양식 자료 (sparse / mid / dramatic 양식 분기 양식)
- **Amplification curve high factor** [구 양식]:
  - 짐노페디 sample = 7.0
  - 곡 frequency 분포 자료 axis
- **Fade in duration**:
  - 짐노페디 sample = 3s
  - 곡 entry mood 정합 axis

### Visual Element Notes

- Idle state:
- Phrase attack:
- Sustained notes:
- Reverb tail:
- Silence:

## Layout Constraints (시리즈 공통)

- Safe title zone: 좌하단 frame (left 0~600 · bottom 0~200) 양식 자체에 박힘
- Safe face zone: cover 영역 (cover image 자체 영향 X · 명화 침범 절대 X · 금기)
- Edge margin: cover 외곽 60px 양식 자료
- Letterbox boundary: bars 자체 letterbox 영역 안 박힘 양식
- Maximum brightness: bar opacity 0.6 default
- Maximum motion: 진폭 cap (곡별 가변)

## Colors

```text
letterbox_top_hex: (props.letterboxColors[0])
letterbox_mid_hex: (props.letterboxColors[1])
letterbox_bottom_hex: (props.letterboxColors[2])
bar_color_auto: hexToRgba(letterboxColors[2], 0.6)
text_color: #e8e0c8 (시리즈 공통 keep)
```

## Export

- Composition: **2560×1440 (2K · default · s361 박힘)**
  - Root.tsx `width={2560} height={1440}`
  - 내부 wrap div: `width: 1920, height: 1080, transform: scale(1.3333333), transformOrigin: "top left"` → 1920×1080 좌표계 keep (px 하드코딩 보존)
  - 본 양식 = s361 정공 path (이전 `--scale=1.333` 박힌 doctrine 자체엔 ffmpeg dimension 비정수 trap [1080×1.333 = 1439.64] 자가 catch · 정정)
- Output resolution: 2560×1440 (composition 그대로 · `--scale` 옵션 X)
- Render 명령: `remotion render src/index.ts <CompositionId> out/<piece_id>_final.mp4`
- Frame rate: 30
- Codec: H.264 (default Remotion)
- Audio codec: AAC 48kHz stereo
- File name: `out/prototype_v{N}.mp4` (iteration) → `out/{piece_id}_final.mp4`

## QC (시리즈 공통)

- 명화 자체 영향 X 양식 (절대 axis · 금기)
- letterbox 영역 keep (그라데이션 자체 visible)
- text 영역 X 침범
- bar 양식 *고급스러움* 양식 정합 (subtle · thin · sparse 양식 본질)
- *EDM 양식 dense bars* 회피
- bar 좌측 저역 양식 정합 (신형 = 9시 60Hz · 구 양식 = 0Hz)
- YouTube compression 통과
- audio sync 자료 정합 (음악 100% 완성 후 fine-tune)
