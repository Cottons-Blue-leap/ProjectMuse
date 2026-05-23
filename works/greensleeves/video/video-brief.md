# Video Brief — Greensleeves

> 시리즈 시그너처 = [`../../../README.md`](../../../README.md) § *Series Signature* + [`../../../series_history.csv`](../../../series_history.csv) `signature_mark` 컬럼. 캐릭터 anchor = [`../../../planning/classical_miku_anchor.md`](../../../planning/classical_miku_anchor.md).
> 박힌 날짜: 2026-05-20 (s336) · setup phase · 음악 본격 진입 사전 자료

## Identity

- Project: Atelier Miku Acappella
- Piece: Greensleeves (Traditional) · 통째 (자연 짧은 곡 양식 · 발췌 없음)
- Release title: Greensleeves (feat. Hatsune Miku) · 양식 잠정 (anonymous 작곡가 axis)
- Original title credit: *Greensleeves* (16세기 전통 · Elizabethan-era English ballad · 현존 최초 등록 1580)
- Composer: Anonymous (Traditional · 16th-century England)
- Arrangement: 코튼 V6 직접 입력 (르네상스 consort 양식 → vocal layer 분배 · 가사 axis 결단 후)
- Vocal: Hatsune Miku (V6)
- Duration: 미정 (V6 작업 후 master 자료 정확 분량 확정 · strophic 절 분배 base)
- Release format: YouTube 16:9 + 1:1 album cover still

## Core Promise

```text
The oldest melody the world still hums — a Tudor ballad reborn as Miku's modal voice, sung the way the Renaissance always meant it: voices alone.
```

## Mood

- Primary mood: wistful · tender · modal melancholy (도리안 양식 특유의 애틋함)
- Secondary mood: courtly · antique · 고요한 기품 (Elizabethan court 양식)
- Avoided mood: bright ragtime swagger (조플린 X) · vigorous baroque (비발디 X) · 과한 비장 (라크리모사 family X) · 르네상스 modal 고유 결 keep

## Visual Direction

- Painting era or visual reference: English Renaissance / Elizabethan court portrait (c.1592)
- Painting source (artist · title · year · URL): Marcus Gheeraerts the Younger · *The Ditchley Portrait of Elizabeth I* · c.1592 · `https://commons.wikimedia.org/wiki/File:Elizabeth_I_(Armada_Portrait).jpg` (※ Ditchley 정확 파일 cover 합성 시점 verify · National Portrait Gallery 소장)
- Color palette (명화 주조색 2~3건 hex): 사전 자료 (cover 합성 시점 직접 측정 path · 추정 base):
  - cream/ivory gown `#e8e0d0` (dominant · 엘리자베스 백색 가운)
  - gold ornament `#c8a850` (accent · 보석·자수)
  - storm slate `#3a4858` (background · 우측 폭풍 하늘 양식)
- Lighting (명화 빛 source 방향): 좌측 sun / 우측 storm 대비 양식 (Ditchley 특유의 날씨 alegory) · 인물 정면 court 조명
- Texture: oil · Elizabethan portrait 정밀 양식 · 평면 장식 강
- Typography: GFS Didot (시리즈 lock · regular weight)
- Visualizer style: 비발디/조플린 audio waveform bars (좌·우 letterbox) family keep (정합 axis) · 색조 자체엔 Ditchley palette base
- Candidate CSV artwork: csv row 101 자료 그대로 (Ditchley Portrait · 매칭 사유 *Elizabethan court repertoire 정합*)

## Letterbox (16:9 frame · 1:1 cover 좌·우 negative space)

- Color stops (manual hex 2~3건): 사전 자료 (cover 합성 시점 직접 측정 후 자리):
  - cream ivory `#e8e0d0` → muted gold `#a08840` → storm slate `#2a3440` (추정 base)
- Gradient direction (cover light direction 정합): 좌(sun) → 우(storm) horizontal (Ditchley 날씨 alegory 정합 axis)
- Notes: Elizabethan portrait 평면 장식 양식 · gradient 단순 linear 자연 fit

## Channel Wordmark (시리즈 시그너처 v3 default 양식 적용)

frame 우하단 corner에 *Atelier Miku Acappella* wordmark · 좌하단 title mirror axis (좌·우 visual symmetry · mass balance).

시리즈 anchor (작품별 가변 X · 자료 base default):
- Color: cream `#e8e0c8`
- *Miku*의 *M*: banner 청록 `rgb(40, 180, 175)`
- text-shadow: `0 2px 12px rgba(0, 0, 0, 0.75)`
- Size: 40 (좌하단 piece_title 56 의 ~70%)
- 자리: margin_right 81 + margin_bottom 90
- Opacity: 1.0

작품별 자리 (가변):
- Wordmark notes: v3 default 양식 적용 (조플린 family keep)

## Timeline (acappella-only · no DAW capture · strophic 양식 · 잠정)

```text
00:00-00:03
  fade in to cover (Ditchley Portrait + Classical Miku)

00:03-...
  verse 1 (modal 멜로디 · main vocal lead)
  cover + visualizer + 우하단 wordmark
  - 멜로디 = main vocal · consort 하성부 = supporting layer

  refrain ("Greensleeves was all my joy...")
  - layer 합세 · 화성 풍성

  verse 2~ (절 반복 · 점층 양식 · 가사/humming axis 결단 base)

...-end
  fade to credits or end card (~12초)
```

(절 수 / 반복 분배 / 정확 분량 자체엔 V6 본격 작업 + 가사 axis 결단 후 master 자료 base 자리.)

## Assets Needed

- Master audio (`music/masters/master.wav`): pending
- Album cover still 1:1 (`video/cover/greensleeves_album_1x1.png` · 자동 썸네일 base): pending (Ditchley Portrait + Classical Miku 합성)
- Visualizer render: pending (조플린/비발디 양식 family keep · 색조 변경 axis)
- Final export (`video/exports/greensleeves_final.mp4`): pending

(YouTube 썸네일 = 자동 썸네일 활용 · s313 결단 · 별 합성 자리 X.)

## Risk Notes

- **Rights** — composition anonymous 16세기 전통 PD 강 (전세계 정합). Gheeraerts d.1636 · Ditchley c.1592 · PD 강 (life+70 통과). score = candidates_opus 4 후보 (edition_id 자가 점검 V6 진입 시점 · 가장 깨끗한 PD edition 우선).
- **Miku character usage** — official artwork 사용 X (Classical Miku anchor 자가 axis · 외부 합성)
- **Font** — GFS Didot SIL OFL keep
- **가사 axis (NEW · 확정 s336)** — 영어 가사 사용 확정 = 시리즈 첫 텍스트 vocal · 영어 voicebank 가능 confirmed (s336) · **딕션 polish가 신규 craft challenge** (이전 일본어/모음 Miku 이탈 axis · 발음 자연스러움 V6 통제)
- **모달 화성** — 도리안 raised-6th false relation 양식 · 화성 처리 신규 axis · V6 본격 작업 시 polish 자가 결단
- **명화 파일 verify** — Ditchley Portrait 정확 commons 파일 cover 합성 시점 verify 의무 (Armada Portrait 등 엘리자베스 초상 혼동 risk · NPG 소장 Ditchley 특정)

## 사전 점검 의제 (다음 cycle 자리)

- **score pick** — `그린슬리브스_1~4.pdf` 4 후보 중 채택 편곡 (코튼 나중에 직접)
- ✅ **가사 axis** — 영어 가사 사용 확정 (s336) · 가사 선정/절 분배 코튼 직접 · V6 영어 딕션 신규
- **form 분배** — strophic 절 반복 (몇 절 / 간주 / 점층)
- **Classical Miku 배치** — Ditchley = 엘리자베스 1세 단독 정면 court 양식 · Classical Miku 배치 자연 path (인물 대체 X · 별도 자리 / 배경 court axis) · 사전 verify 의제
- **letterbox 정밀 색조** — cover 합성 시점 직접 측정 path
