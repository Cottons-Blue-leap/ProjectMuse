# Video Brief — Gymnopédie No. 1

> 시리즈 시그너처 = [`../../../README.md`](../../../README.md) § *Series Signature* + [`../../../series_history.csv`](../../../series_history.csv) `signature_mark` 컬럼. 캐릭터 anchor = [`../../../planning/classical_miku_anchor.md`](../../../planning/classical_miku_anchor.md).

## Identity

- Project: Atelier Miku Acappella
- Piece: Gymnopédie No. 1
- Release title: Satie - Gymnopédie No. 1 | Atelier Miku Acappella
- Original title credit: after Erik Satie, Gymnopédie No. 1 (1888)
- Composer: Erik Satie
- Arrangement: 통째 (~80마디 ABA 구조 · 멜로디·베이스·내성 3축 박음)
- Vocal: Hatsune Miku (V6) · 6 역할 중 lead_miku · mid_oo · low_oo 우선
- Duration: TBD (음악 100% 완성 후 실측)
- Release format: YouTube 16:9 + 1:1 album cover still

## Core Promise

```text
Miku-centered classical acappella experiment — Satie 1888, score-faithful, no instruments.
```

## Mood

- Primary: 식어버린 밤 (cool · sparse · 정적 · 투명)
- Secondary: melancholic intimacy (boat 위 Miku silhouette)
- Avoided: dramatic · warm · ornamental

## Visual Direction

- Painting era: late 19th-century · Tonalism · Whistler Nocturne 시리즈
- Painting source: James McNeill Whistler, *Nocturne in Blue and Gold: Old Battersea Bridge* (1872-75) · Tate Britain N01959 · https://www.tate.org.uk/art/artworks/whistler-nocturne-blue-and-gold-old-battersea-bridge-n01959 · public domain
- Color palette (명화 주조색 hex):
  - `#1f2c3d` (deep blue-teal · 밤하늘·물·다리 그림자)
  - `#4a5a6e` (muted slate-blue · 안개·중간 톤)
  - `#b8a673` (muted gold · 다리 lantern · 강물 reflection)
- Lighting: 좌하단 lantern reflection 강 + 다리 위 lantern 산재 (점광원 다중)
- Texture: oil painting · soft brushwork · 안개 layer
- Typography: GFS Didot (regular weight · 시리즈 lock)
- Visualizer style: 좌·우 letterbox vertical bars (s279 v11 final · 32 bars per side · subtle gold tone · 짐노페디 진폭 cap 220 · 9시 0Hz 시계방향 · 명화 영향 X · 자료 양식 자료 = `visualizer/README.md`)
- Candidate CSV artwork: TBD (candidate_master.csv row 매칭 의제)

## Letterbox (16:9 frame · 1:1 cover 좌·우 negative space)

- Color stops (3 stop): `#1f2c3d → #4a5a6e → #b8a673` (deep blue → mid slate → gold accent)
- Gradient direction: vertical (상단 deep blue → 중단 mid slate → 하단 gold) · 명화 sky-water-lantern structure 정합
- Notes: 자가 시각 분석 hex · 코튼 design tool color picker로 정밀 추출 권장

## Text Stack (Lower-left · GFS Didot)

```text
Erik Satie
Gymnopédie No. 1
(after 1888)
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
- pixel 좌표: cover composite 시점 결단 (sample_002 base 안 빈 자리 분포 + cover light direction axis)

## Timeline (acappella-only · no DAW capture)

```text
00:00-00:08
  fade in (letterbox + cover 동시 fade)

00:08-end minus 5s
  cover + 최소 visualizer (phrase별 breathing)

last 5s
  slow fade to credits / end card
```

실제 timecode는 음악 100% 마스터 duration 결단 후 박음.

## Assets Needed

- Master audio (`music/masters/master.wav`): TBD (음악 50% 진행 중)
- Album cover 1:1 (`video/cover/album_1x1.png`): TBD (sample_002 base + text stack overlay)
- YouTube 16:9 frame composite (`video/cover/youtube_frame.png`): TBD (letterbox + cover composite)
- Thumbnail 16:9 (`video/cover/thumbnail.png`): TBD
- Visualizer render (`video/visualizer/`): TBD
- Final export (`video/exports/final_4k.mp4`): TBD

## Risk Notes

- Rights:
  - 명화 = Whistler 1872-75 · public domain (사망 1903 + 100년 통과)
  - 폰트 = GFS Didot SIL OFL · 라이브 서비스 안전
  - Miku official artwork 사용 X (ChatGPT 자가 생성 image만)
- Miku character usage: anchor 3줄 keep + 명화 맥락 따라 가변 (현재 sample_002 = boat 위 silhouette + late-19th muted dress)
- Font: GFS Didot 1종만 사용 · 두 번째 typeface 금지
- Visual clutter: 시그너처 5축 정합 점검 (타이포·그리드·마크 X·1:1 cover·letterbox)
- Audio sync: 음악 완성 후 확정
