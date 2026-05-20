# Visualizer — Atelier Miku Acappella

Remotion 양식 시리즈 visualizer. 첫 작품 = Gymnopédie No. 1.

## Run

```bash
npm install       # 한 번
npm run studio    # Remotion Studio (preview)
npm run render    # out/prototype_v11.mp4 (final 양식) 박음
```

지난 prototype 자료:
- v1 = silent · time-based breathing (폐기)
- v2 = audio · cover scale breathing (폐기 · 명화 직접 변형 axis)
- v3 = audio · cover halo (폐기 · 양식 약)
- v4 = audio · cover 위 fog layer (폐기 · *버그* 양식)
- v5~v8 = 좌·우 vertical bars 양식 cycle (count·width·amplification·sensitivity 양식 fine-tune)
- v9 = props 양식 박힘 (곡별 가변 axis)
- v10 = circular spectrum (구도만 좋음 · visualization 양식 투박)
- v11 = **final 양식** = v10 구도 + v9 양식 vertical bars (고급 양식)

## Final 양식 (v11)

### Frame & Layout

- Frame: 1920×1080 (16:9)
- Cover: 720×720 center 양식 (시리즈 시그너처 *1:1 cover* keep)
- Letterbox: cover 외곽 4방향 (좌 600 · 우 600 · 위 180 · 아래 180)
- Letterbox gradient: vertical 3 stop (props 자료)
- Text stack: 좌하단 frame 자리 (left 80 · bottom 60) · GFS Didot

### Sound Visualization

- 좌·우 letterbox vertical bars
- 32 bars per side · 64 total (numberOfSamples 64 정합)
- bar width 3px · 자료 자료 자료 자료 자료
- bar opacity 0.6 (subtle 양식)
- bar max height 220px (짐노페디 양식 자료 자료)
- 9시 = 0Hz (좌측 letterbox 맨 왼편) · 시계방향 frequency 증가
- 좌 = low band [0..31] · 우 = high band [32..63]
- per-bar amplification curve (1.0 → 7.0 · exp 1.4)
- sqrt amplitude scaling (작은 amplitude 자연 더 visible)
- center anchored (y 540 양식)
- bar color = letterbox[2] auto (props hex → rgba)

### Audio

- `<Audio src>` component
- `useAudioData` + `visualizeAudio` (numberOfSamples 64)
- audio src = props.audioPath (public/ 자료)

### Font

- GFS Didot (SIL OFL · `public/fonts/GFSDidot-Regular.ttf`)
- delayRender + new FontFace 양식 load
- text stack 양식: composer 32px · piece 56px · subtitle 26px italic

### Fade In

- frame 0~90 (3s @ 30fps) · opacity 0 → 1

## 다음 곡 활용 양식

`src/Root.tsx` 자료 양식 박힘:

```tsx
const someNextSongProps: VisualizerProps = {
  letterboxColors: ["#hex1", "#hex2", "#hex3"], // 명화 주조색 3 stop
  composerName: "...",
  pieceTitle: "...",
  pieceSubtitle: "...", // optional
  audioPath: "audio_next.wav", // public/ 자료
  coverPath: "cover_next.png",  // public/ 자료
};
```

`<Composition id="MuseNextSong" ... defaultProps={someNextSongProps} />` 박힘.

### 자료 자료 곡별 가변 axis 자료

본 prototype 양식 자료 자료 자료 자료. 다음 곡 진입 시 의제:

1. **bar amplitude cap (`BAR_MAX_AMPLITUDE_HEIGHT`)** — 곡별 dynamic 양식 정합
   - 짐노페디 = 220 (sparse · 정적 · 진폭 제한 양식)
   - 야상곡 · 왈츠 = 자료 양식 강 (예: 350~~500)
   - props 양식 박힘 path = `maxAmplitudeHeight` prop 신축 axis

2. **bar count per side (`BAR_COUNT_PER_SIDE`)** — 자료 양식 자료 양식
   - 32 default keep · 자료 양식 자료 양식 자료

3. **amplification curve** — 곡별 frequency 분포 axis
   - high band amplification 7.0 default keep

4. **non-linear scaling exponent** — 0.5 (sqrt) default
   - 자료 자료 자료 자료 양식

5. **fade in duration** — 3s default · 곡별 자료 양식

## 시리즈 시그너처 정합

본 visualizer 양식이 시리즈 시그너처 5축 정합:
1. **타이포 GFS Didot** — keep
2. **그리드 Lower-left text stack** — text 자리 = 좌하단 frame 자리 (cover scale down 양식 정합)
3. **마크 X** — bars + text + cover만, brand mark X
4. **1:1 cover** — keep (size 720 양식 · 비율 keep)
5. **Letterbox vertical gradient** — keep · 4방향 자료 양식 정합

## 의제 / 다음 cycle

- 음악 100% 완성 후 진짜 audio source 박힘 + duration 실측 (현 30s placeholder)
- ~~text stack 자리 정정 axis~~ → s280에서 lock 통과:
  - 16:9 video frame = 좌하단 letterbox 영역 (v11 정합)
  - 1:1 cover still = cover 내부 좌하단 text overlay (외부 배포 visibility 정합)
- candidate_master.csv 다음 곡 선정 cycle
- 다음 곡 진입 시 maxAmplitudeHeight prop axis 박힘 자료
