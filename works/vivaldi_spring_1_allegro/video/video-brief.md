# Video Brief — Vivaldi Spring Mvt. I Allegro

> 시리즈 시그너처 = [`../../../README.md`](../../../README.md) § *Series Signature* + [`../../../series_history.csv`](../../../series_history.csv) `signature_mark` 컬럼. 캐릭터 anchor = [`../../../planning/classical_miku_anchor.md`](../../../planning/classical_miku_anchor.md). 본 brief는 곡별 가변 자리만 박음.

## Identity

- Project: Atelier Miku Acappella
- Piece: Spring, Mvt. I Allegro (Le quattro stagioni, Op. 8 No. 1 · RV 269)
- Release title: Antonio Vivaldi - Spring, Mvt. I (feat. Hatsune Miku)
- Original title credit: after Antonio Vivaldi, Spring, Mvt. I Allegro (1725, from Le quattro stagioni Op. 8 No. 1, RV 269)
- Composer: Antonio Vivaldi
- Arrangement: 통째 (full movement · 5 voice 분배 = 솔로 바이올린 + Violin I + Violin II + Viola + Cello/Basso continuo)
- Vocal: Hatsune Miku (V6) · 5 트랙 동시 분배
- Duration: 3:17 (197.6초 실측)
- Release format: YouTube 16:9 + 1:1 album cover still

## Core Promise

```text
Miku-centered baroque acappella experiment — Vivaldi 1725, score-faithful, no instruments.
```

## Mood

- Primary: 쾌활·생명·약동 (vibrant · alive · vital · 봄의 시 본질)
- Secondary: 자연의 시 (새 소리·시냇물·바람·꽃피움)
- Avoided: 무거움·우울·정적 (짐노페디와 본질 분기)

## Visual Direction

- Painting era: Early Renaissance · Florence · Botticelli
- Painting source: Sandro Botticelli, *Primavera* (c. 1482) · Uffizi Gallery, Florence · Public Domain
- Painting URL: https://commons.wikimedia.org/wiki/File:Botticelli-primavera.jpg (Wikipedia commons · s309 코튼 결단)
- Color palette (cover 실측 색 분포 기반 · s312 코튼 결단 통과):
  - `#3a4a32` (mid forest green · 명화 상단 grove 추출)
  - `#b8a06e` (muted gold · 인물 옷·grove highlight mid tone)
  - `#5e4a3a` (warm dark brown · 하단 흙·인물 그림자 자리)
- Lighting: 왼쪽 위 자연 햇빛 (Mercury 측 자리) + 전체적으로 부드러운 diffuse · 그림자 약함
- Texture: tempera (egg-based · Early Renaissance) · soft brushwork · 디테일 강 (꽃·잎·옷 무늬)
- Typography: GFS Didot (regular weight · 시리즈 lock)
- Visualizer style: 좌·우 letterbox vertical bars (s279 v11 final · 32 bars per side · 비발디 dynamic ensemble · BAR_MAX_AMPLITUDE_HEIGHT 짐노페디 220 대비 더 높을 자료 · sample 380~450 axis · 9시 0Hz 시계방향 · 명화 영향 X · visualizer-spec.md 자체 박음)
- Candidate CSV artwork: TBD (candidate_master.csv row 매칭 의제)

## Letterbox (16:9 frame · 1:1 cover 좌·우 negative space)

- Color stops (3 stop): `#3a4a32 → #b8a06e → #5e4a3a` (mid forest → muted gold → warm dark brown)
- Gradient direction: vertical (상단 mid forest → 중단 muted gold → 하단 warm dark brown) · 따뜻한 mid-tone 흐름 · cover 실측 색 분포 정합 (Primavera = 위·아래 어두움 + 중간 인물 highlight 양식이므로 light meadow 가정 폐기)
- Notes: s312 코튼 결단 통과. 변경 사유 = 옛 stops (`#1f3122 → #d9b88a → #f0e2c0`)는 하단 light cream이 글자 색 `#e8e0c8`과 밝기 충돌로 시인성 약 + cover에 light cream dominant 색이 없어 cover 정합 약. 새 stops = cover 실측 색 픽 + 글자 시인성 통과 + mood (쾌활·생명·약동) 따뜻함 정합.

## Text Stack (Lower-left · GFS Didot)

```text
Antonio Vivaldi
Spring, Mvt. I
(after 1725)
```

공통:
- Alignment: left
- Weight: regular
- Typography: GFS Didot · composer 32px · piece 56px · subtitle 26px italic

**(A) 16:9 video frame** (Remotion render · YouTube 양식)
- Position: 좌하단 letterbox 영역 (left 80px · bottom 60px @ 1920×1080 · v11 visualizer 정합)
- 1:1 cover 영역 침범 X (명화 + 캐릭터 보존)

**(B) 1:1 cover still** (외부 배포용 · `video/cover/album_1x1.png`)
- Position: cover 내부 좌하단 (cover 위 text overlay)
- 이유: Spotify·Bandcamp·playlist visibility 정합
- pixel 좌표: cover composite 시점 결단 (cover light direction axis · Primavera 명화 빈 자리 분포 axis)

## Timeline (acappella-only · no DAW capture)

```text
00:00-00:08
  fade in (letterbox + cover 동시 fade)

00:08-03:12
  cover + 최소 visualizer (phrase별 breathing)

03:12-03:17
  slow fade to credits / end card
```

실측 duration 3:17 (197.6초) 정합.

## Assets Needed

- Master audio (`music/Miku_vivaldi_spring_1_allegro.wav`): ✅ 완성 (197.6초 · 44.1kHz · 24bit 스테레오 PCM)
- Album cover 1:1 (`video/cover/album_1x1.png`): ✅ 완성 (Primavera + Classical Miku · Flora 옆 자리 · s310 결단 · 자동 썸네일 base)
- Visualizer render (`video/visualizer/`): ✅ 완성 (s311 신축 + s312 시안 cycle 통과)
- Final export (`video/visualizer/out/vivaldi_spring_1_allegro_final.mp4`): ✅ 완성 (s312 · 21.3 MB · 198초 · 1920×1080 @ 30fps)

(YouTube 썸네일 = 자동 썸네일 활용 · s313 결단 · 별 합성 자리 X. youtube_frame.png 자리 폐기 · Remotion frame 자체 산출.)

## Risk Notes

- Rights:
  - 명화 = Botticelli *Primavera* (c. 1482) · public domain (사망 1510 + 400년 이상 통과)
  - 폰트 = GFS Didot SIL OFL · 라이브 서비스 안전
  - Miku official artwork 사용 X (ChatGPT 자가 생성 image만)
- Miku character usage: anchor 3줄 keep (teal-cyan twin-tails · late-19th-century European dress · quiet melancholic expression) + Primavera 맥락 따라 가변
- Font: GFS Didot 1종만 사용 · 두 번째 typeface 금지
- Visual clutter: 시그너처 5축 정합 점검 (타이포·그리드·마크 X·1:1 cover·letterbox)
- Audio sync: ✅ 음악 완성 (3:17 실측)
- 톤 분리 axis (짐노페디 vs 비발디): 짐노페디 = 안개·정적·식어버린 밤 / 비발디 = 쾌활·생명·약동·봄. 같은 시그너처 5축 안에서 mood·color·visualizer amplitude 자료 분기
