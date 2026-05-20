# Visualizer Spec

> 시리즈 시그너처 = [`../../../README.md`](../../../README.md) § *Series Signature* + [`../../../series_history.csv`](../../../series_history.csv) `signature_mark` 컬럼.
> Reference 양식 = `Project_Muse/works/gymnopedie_1_first_proof/video/visualizer/` (Remotion · s279 박힘).
> 도구 = Remotion (s276 박힘 · s279 본격 양식 박힘).

## Concept

- Visualizer name:
- Relationship to music:
- Relationship to cover image:

## 시리즈 공통 양식 (변경 X)

본 양식은 시리즈 모든 곡 공통 keep. 변경 시 시리즈 시그너처 reset 본질.

- **Frame**: 1920×1080 (16:9)
- **Cover**: 720×720 center 양식 (1:1 ratio keep · size scale 양식 axis)
- **Letterbox**: cover 외곽 4방향 (좌 600 · 우 600 · 위 180 · 아래 180)
- **Letterbox gradient**: vertical 3 stop (props 자료)
- **Text stack**: 좌하단 frame 자리 (left 80 · bottom 60) · GFS Didot · composer 32px / piece 56px / subtitle 26px italic
- **Sound visualization**: 좌·우 letterbox vertical bars
  - 32 bars per side · 9시=0Hz · 시계방향 freq 증가
  - 좌 = low band [0..31] · 우 = high band [32..63]
  - bar width 3px · opacity 0.6 · center anchored · pill 양식
  - per-bar amplification curve (1.0 → 7.0 · exp 1.4)
  - sqrt amplitude scaling
- **Fade in**: 3s 양식 (frame 0~90 @ 30fps)
- **Audio**: `<Audio>` + `useAudioData` + `visualizeAudio` (numberOfSamples 64)
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

- Master audio path:
- Audio duration:
- Audio sample rate / bit depth:

### Motion / Amplitude 자료

- **Bar amplitude cap (`BAR_MAX_AMPLITUDE_HEIGHT`)**:
  - 짐노페디 sample = 220 (sparse · 정적 mood 양식 정합)
  - 곡 dynamic 양식 자료 (sparse / mid / dramatic 양식 분기 양식)
- **Amplification curve high factor**:
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

- Resolution: 1920×1080
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
- bar 좌측 0Hz 양식 정합
- YouTube compression 통과
- audio sync 자료 정합 (음악 100% 완성 후 fine-tune)
