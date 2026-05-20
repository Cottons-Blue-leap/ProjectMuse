# Video Brief — Joplin The Entertainer

> 시리즈 시그너처 = [`../../../README.md`](../../../README.md) § *Series Signature* + [`../../../series_history.csv`](../../../series_history.csv) `signature_mark` 컬럼. 캐릭터 anchor = [`../../../planning/classical_miku_anchor.md`](../../../planning/classical_miku_anchor.md).
> 박힌 날짜: 2026-05-17 (s326) · setup phase · 음악 본격 진입 사전 자료

## Identity

- Project: Atelier Miku Acappella
- Piece: The Entertainer (A Ragtime Two-Step) · 통째 (~3:30-4:00 · 자연 짧은 곡 양식 · 발췌 없음)
- Release title: Joplin - The Entertainer (feat. Hatsune Miku)
- Original title credit: *The Entertainer (A Ragtime Two-Step)* (1902 published · John Stark · Sedalia, Missouri)
- Composer: Scott Joplin (1868-1917)
- Arrangement: 코튼 V6 직접 입력 (RH 싱코페이션 멜로디 + LH stride bass → vocal layer 분배)
- Vocal: Hatsune Miku (V6)
- Duration: ~3:30-4:00 추정 (V6 작업 후 master 자료 정확 분량 확정)
- Release format: YouTube 16:9 + 1:1 album cover still

## Core Promise

```text
The ragtime that the whole world hums — now sung instead of struck, with Miku weaving the melody and the stride.
```

## Mood

- Primary mood: playful · bright · syncopated swagger
- Secondary mood: nostalgic (1902 turn-of-century parlor music · *The Sting* 1973 매칭 자료)
- Avoided mood: heavy · solemn · dramatic (짐노페디 정적 family X · 비발디 vigorous family X · 모차르트 childlike X · ragtime 자체 axis)

## Visual Direction

- Painting era or visual reference: Neo-Impressionism / Pointillism (1891)
- Painting source (artist · title · year · URL): Georges Seurat · *The Circus* · 1890-91 · `https://commons.wikimedia.org/wiki/File:Georges_Seurat_-_The_Circus.jpg`
- Color palette (명화 주조색 2~3건 hex): 사전 자료 (cover 합성 시점 직접 측정 path · 추정 base):
  - warm cream/yellow background `#f0d878` (dominant)
  - circus red `#c83838` (accent)
  - cool blue dots `#3858a0` (pointillism accent)
- Lighting (명화 빛 source 방향): 중앙 무대 spotlight · 전체적으로 평면 양식 (점묘 특성)
- Texture: oil · pointillism dots · 평면 양식
- Typography: GFS Didot (시리즈 lock · regular weight)
- Visualizer style: 비발디 audio waveform bars (좌·우 letterbox) family keep (정합 axis) · 색조 자체엔 *The Circus* palette base
- Candidate CSV artwork: csv row 41 자료 그대로 (Seurat *The Circus* · 매칭 사유 *서커스 흥과 ragtime 흥 정합*)

## Letterbox (16:9 frame · 1:1 cover 좌·우 negative space)

- Color stops (manual hex 2~3건): 사전 자료 (cover 합성 시점 직접 측정 후 자리):
  - warm cream `#f0d878` → muted gold `#b89a48` → deep wine `#5a2828` (추정 base)
- Gradient direction (cover light direction 정합): 좌 → 우 horizontal (서커스 spotlight 양식 정합 axis)
- Notes: *The Circus* 자체엔 점묘 평면 양식 · gradient 자체엔 단순 linear 양식 자연 fit

## Channel Wordmark (시리즈 시그너처 §3 · s320 v3 default 양식 적용)

frame 우하단 corner에 *Atelier Miku Acappella* wordmark · 좌하단 title mirror axis (좌·우 visual symmetry · mass balance).

시리즈 anchor (작품별 가변 X · 자료 base default):
- Color: cream `#e8e0c8`
- *Miku*의 *M*: banner 청록 `rgb(40, 180, 175)`
- text-shadow: `0 2px 12px rgba(0, 0, 0, 0.75)`
- Size: 40 (좌하단 piece_title 56 의 ~70%)
- 자리: margin_right 81 + margin_bottom 90
- Opacity: 1.0

작품별 자리 (가변):
- Wordmark notes: 본 작품 = v3 default 양식 적용 (모차르트 first 적용 다음 axis · 비발디 retrofit 통과 후 default 정착)

## Timeline (acappella-only · no DAW capture · ABACAD 5 strain 양식)

```text
00:00-00:03
  fade in to cover (Seurat The Circus + Classical Miku)

00:03-~00:48
  A strain (16 마디 + repeat · ~45초 추정)
  cover + visualizer + 우하단 wordmark
  - RH 메인 멜로디 = main vocal
  - LH stride bass = low layer (oom-pah 양식)

~00:48-~01:33
  B strain (16 마디 + repeat · ~45초 추정)
  - 멜로디 변화 · 톤 약간 어둡게 (subdominant key 변화 양식)

~01:33-~02:18
  A strain return (16 마디 · ~45초 · repeat X 또는 단축 axis)

~02:18-~03:03
  C strain (16 마디 + repeat · ~45초 · 가장 lyrical 자리)
  - 멜로디 노래성 강화 · vocal main lead 자리

~03:03-~03:48
  D strain (16 마디 + repeat · ~45초 · finale 자리)
  - texture 가장 풍성 · layer 다 합세

~03:48-end
  fade to credits or end card (~12초)
```

(strain repeat 자료 / form 정확 분량 자체엔 V6 본격 작업 후 master 자료 base 자리.)

## Assets Needed

- Master audio (`music/masters/master.wav`): pending
- Album cover still 1:1 (`video/cover/album_1x1.png` · 자동 썸네일 base): pending (Seurat *The Circus* + Classical Miku 합성)
- Visualizer render: pending (비발디 양식 family keep · 색조 변경 axis)
- Final export (`video/exports/joplin_the_entertainer_final.mp4`): pending

(YouTube 썸네일 = 자동 썸네일 활용 · s313 결단 · 별 합성 자리 X.)

## Risk Notes

- **Rights** — Joplin d.1917 · The Entertainer 1902 출판 · PD 강 전세계 정합. Seurat d.1891 · *The Circus* 1890-91 · PD 강 (life+135). 둘 다 audit 통과 확정.
- **Miku character usage** — official artwork 사용 X (Classical Miku anchor 자가 axis · 외부 합성)
- **Font** — GFS Didot SIL OFL keep
- **ragtime 양식 신규 challenge** — syncopation 정밀도 + stride bass on voice + 2층 텍스쳐 통제 = V6 첫 ragtime axis · 본격 작업 시 polish iteration cycle 자가 결단
- **swung vs straight** — Joplin 자가 indication *Notice: Do not play this piece fast* 박힘 · straight-time keep default · 코튼 본격 작업 시 자가 결단 자리
- **분량 axis** — 자연 짧은 곡 통째 ~3:30-4:00 · 짐노페디·비발디 family 정합 axis · 기초 체력 path 정합 강

## 사전 점검 의제 (다음 cycle 자리)

- **form repeat 분배** — ABACAD 각 strain repeat 자료 자체엔 코튼 결단 자리 (전체 repeat 다 / 일부 repeat skip 양식)
- **vocal 분배 axis** — RH 멜로디 = main vocal · LH bass = low layer · mid chord = supporting layer · 가사 axis (모음 humming / scat / 영어/한국어 가사) 결단 자리
- **Classical Miku 배치** — *The Circus* = 서커스 무대 자체엔 acrobat (전경) + clown (좌하단) + horse (중앙) + 관객 (배경) 양식 · Classical Miku 자체엔 어디 배치 자연 path (acrobat 자리 / 관객 자리 / 별 axis) · 사전 verify 의제
- **letterbox 정밀 색조** — cover 합성 시점 직접 측정 path
