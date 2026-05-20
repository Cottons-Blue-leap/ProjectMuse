# Visualizer Spec — Vivaldi Spring Mvt. I

> 시리즈 시그너처 = [`../../../README.md`](../../../README.md) § *Series Signature* + [`../../../series_history.csv`](../../../series_history.csv) `signature_mark` 컬럼.
> Reference 양식 = `Project_Muse/works/gymnopedie_1_first_proof/video/visualizer/` (Remotion · s279 박힘).
> 도구 = Remotion (s276 박힘 · s279 본격 양식 박힘).

## Concept

- Visualizer name: Atelier Miku Acappella series visualizer v11 (Vivaldi Spring variant)
- Relationship to music: phrase별 breathing · acappella ensemble dynamic 정합 · 비발디 5 voice 동시 + forte/piano 대비 axis
- Relationship to cover image: 명화 영향 X (시그너처 fix · bar color = letterboxColors[2] light cream tone auto)

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
  - per-bar amplification curve (1.0 → 7.0 · exp 1.4) — 본 곡 axis 가변
  - sqrt amplitude scaling
- **Fade in**: 3s 양식 (frame 0~90 @ 30fps)
- **Audio**: `<Audio>` + `useAudioData` + `visualizeAudio` (numberOfSamples 64)
- **Font**: GFS Didot · staticFile + FontFace API · delayRender 양식

## 곡별 가변 자료 (props)

```tsx
{
  letterboxColors: ["#3a4a32", "#b8a06e", "#5e4a3a"], // cover 실측 색 3 stop (s312 코튼 결단 · video-brief 정합)
  composerName: "Antonio Vivaldi",
  pieceTitle: "Spring, Mvt. I",
  pieceSubtitle: "(after 1725)",
  audioPath: "Miku_vivaldi_spring_1_allegro.wav",
  coverPath: "cover.png",
}
```

bar color는 `letterboxColors[2]` (마지막 stop · `#5e4a3a` warm dark brown tone) 자동 변환 → 명화별 자동 가변.

## 곡별 axis 결단 자료

### Audio Inputs

- Master audio path: `../music/Miku_vivaldi_spring_1_allegro.wav`
- Audio duration: 197.6s (3:17)
- Audio sample rate / bit depth: 44.1kHz · 24bit · 스테레오 PCM

### Motion / Amplitude 자료

- **Bar amplitude cap (`BAR_MAX_AMPLITUDE_HEIGHT`)**: **400**
  - 짐노페디 sample = 220 (sparse · 정적 mood)
  - 비발디 봄 = dynamic ensemble (5 voice 동시 + forte/piano 대비 + ripieno 진입 자체 강) → 더 높은 cap
  - 다만 720 cover 영역 침범 X · letterbox 영역 안 박힘 axis keep → 400 mid 결단

- **Amplification curve high factor**: **6.0**
  - 짐노페디 sample = 7.0 (sparse → high amplification 필요)
  - 비발디 봄 = 이미 dense bands (ensemble · 동시 진입) → 과도 amplification 회피
  - 6.0 결단 (짐노페디 대비 약간 낮춤)

- **Fade in duration**: **3s** (시리즈 공통 keep · entry mood 양식 정합)

### Visual Element Notes

- **Idle state**: minimal sparse bars · base level ~10% · phrase 사이 미세 gap에서만 적용
- **Phrase attack**: ripieno ensemble forte 진입 → bars sharp rise (특히 첫 ripieno tutti 자리 · 마디 1~7 *Spring has come* 자체)
- **Sustained notes**: 솔로 라인 sustained 자체 → mid bars steady · vibrato 자체 frequency content 통해 bars 미세 떨림
- **Reverb tail**: V6 reverb decay 1.5~2.0초 → bars slow fade out · phrase 끝 자연 transition
- **Silence**: 본 곡 자체 silence 거의 X (continuous ensemble) · phrase 사이 미세 gap만 · idle state 진입

## Layout Constraints (시리즈 공통)

- Safe title zone: 좌하단 frame (left 0~600 · bottom 0~200) 양식 자체에 박힘
- Safe face zone: cover 영역 (cover image 자체 영향 X · 명화 침범 절대 X · 금기)
- Edge margin: cover 외곽 60px 양식 자료
- Letterbox boundary: bars 자체 letterbox 영역 안 박힘 양식
- Maximum brightness: bar opacity 0.6 default
- Maximum motion: 진폭 cap 400 (본 곡 axis)

## Colors

```text
letterbox_top_hex: #3a4a32 (mid forest green · props.letterboxColors[0])
letterbox_mid_hex: #b8a06e (muted gold · props.letterboxColors[1])
letterbox_bottom_hex: #5e4a3a (warm dark brown · props.letterboxColors[2])
bar_color_auto: hexToRgba("#5e4a3a", 0.6) → warm dark brown tone bars
text_color: #e8e0c8 (시리즈 공통 keep)
```

## Export

- Resolution: 1920×1080
- Frame rate: 30
- Codec: H.264 (default Remotion)
- Audio codec: AAC 48kHz stereo
- File name: `out/prototype_v{N}.mp4` (iteration) → `out/vivaldi_spring_1_allegro_final.mp4`

## QC (시리즈 공통)

- 명화 자체 영향 X 양식 (절대 axis · 금기)
- letterbox 영역 keep (그라데이션 자체 visible)
- text 영역 X 침범
- bar 양식 *고급스러움* 양식 정합 (subtle · thin · sparse 양식 본질)
- *EDM 양식 dense bars* 회피
- bar 좌측 0Hz 양식 정합
- YouTube compression 통과
- audio sync 자료 정합 (음악 100% 완성 후 fine-tune · 본 곡 ✅ 완성)
- 비발디 dynamic ensemble axis 점검 (짐노페디 대비 amplitude cap 높음 + amplification 낮춤 결단 정합)
