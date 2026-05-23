# Video Brief — Salut d'Amour (Elgar)

> 시리즈 시그너처 = [`../../../README.md`](../../../README.md) § *Series Signature* + [`../../../series_history.csv`](../../../series_history.csv) `signature_mark` 컬럼. 캐릭터 anchor = [`../../../planning/classical_miku_anchor.md`](../../../planning/classical_miku_anchor.md).
> 박힌 날짜: 2026-05-20 (s337) · setup phase · 음악 본격 진입 사전 자료

## Identity

- Project: Atelier Miku Acappella
- Piece: Salut d'Amour, Op. 12 (Edward Elgar) · 통째 (~3분 · 발췌 없음)
- Release title: Edward Elgar - Salut d'Amour (feat. Hatsune Miku) · 양식 잠정
- Original title credit: *Salut d'Amour* (Liebesgruß) Op. 12 · 1888 작곡 · 1889 출판 · 약혼녀 Alice에게 헌정
- Composer: Edward Elgar (1857-1934)
- Arrangement: 코튼 V6 직접 입력 (OMR 없음 · 원곡 바이올린 선율 → lead_miku · 모음/humming layer)
- Vocal: Hatsune Miku (V6) · 가사 없음 (기악 원곡 family)
- Duration: 미정 (V6 작업 후 master 자료 정확 분량 확정 · ~3분 base)
- Release format: YouTube 16:9 + 1:1 album cover still

## Core Promise

```text
Elgar's little love-greeting for his bride — the violin's tenderest line now sung, not played: Miku alone, voices only.
```

## Mood

- Primary mood: tender · songful · 살롱 낭만의 다정함 (love greeting)
- Secondary mood: nostalgic · 여린 루바토 · 우아한 소품감
- Avoided mood: bright ragtime swagger (조플린 X) · vigorous baroque (비발디 X) · 과한 비장 (라크리모사 family X) · 음울한 모달 (그린슬리브즈 X) · 가벼움·다정함 keep

## Visual Direction

- Painting era or visual reference: late Pre-Raphaelite / Aesthetic (J.W. Waterhouse) · 명화 재선정 path = csv 기본값 Fragonard Rococo → Watts(s343) → Marcus Stone(s344 폐기) → Waterhouse(s345 코튼 확정)
- Painting source (artist · title · year · URL): John William Waterhouse · *The Soul of the Rose (My Sweet Rose)* · 1903 · oil on canvas · private collection · Wikimedia Commons `https://commons.wikimedia.org/wiki/File:John_William_Waterhouse_-_The_Soul_of_the_Rose,_1903.jpg` · 원본 다운로드 = `art_sources/waterhouse_soul_of_the_rose.jpg` (1951×3000 · 2026-05-22 verify 통과)
- Color palette (최종 cover 실측 hex · `Miku_waterhouse_soul_of_the_rose.png` 2026-05-22):
  - warm olive-gold `#564d2e` (dominant · 담벼락·잎·드레스 그늘)
  - deep umber `#241a11` (shadow · 깊은 그늘)
  - terracotta `#9e5c40` (accent · 지붕·화분·장미 · 비주얼라이저 바)
  - soft luminous highlight `#889e6d` (햇빛 든 잎·벽)
- Lighting (명화 빛 source 방향): 우상단 따뜻한 햇빛 · 인물 옆얼굴·뺨·머리에 부드러운 highlight · 배경 깊은 그늘 (저명도·고대비 = 빛나는 하이라이트가 살아있는 구조)
- Texture: oil on canvas · 부드러운 가시 붓질 · 무광 · 깊은 명암 + 빛나는 하이라이트
- Typography: GFS Didot (시리즈 lock · regular weight)
- Visualizer style: 비발디/조플린 audio waveform bars (좌·우 letterbox) family keep · 바 색 = terracotta `#9e5c40`
- Cover production note: AI 합성 = 원작 배경/구도/유화 붓질 보존 + 인물만 미쿠로 유화 리페인트 (edit-on-reference) → 화풍 원작 매칭 → 명도/채도 원작 대조 튜닝. 반복 = `cover/iterations/` (v1 look→v2 outfit→v3 style→v4 luminous). 곡 주제 직결 = 장미 향을 맡는 인물 = *사랑의 인사*(꽃 한 송이 같은 헌정곡).

## Letterbox (16:9 frame · 1:1 cover 좌·우 negative space)

- Color stops (최종 cover 실측 · Root.tsx `letterboxColors` 박힘 2026-05-22):
  - top `#241a11` (deep umber) → mid `#63552f` (warm olive-gold) → bottom `#9e5c40` (terracotta)
- Gradient direction: `linear-gradient(180deg, [0] 0% → [1] 50% → [2] 100%)` (상 어두운 그늘 → 하 따뜻한 terracotta)
- Notes: Waterhouse 저명도·따뜻한 톤 정합 · bottom terracotta = 비주얼라이저 바 색 겸용 (가시성 + 지붕/화분/장미 accent)

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

## Timeline (acappella-only · no DAW capture · 잠정)

```text
00:00-00:03
  fade in to cover (Waterhouse The Soul of the Rose + Classical Miku)

00:03-...
  A 주제 (노래하는 바이올린 선율 · lead_miku)
  cover + visualizer + 우하단 wordmark
  - 멜로디 = lead_miku · 화성 layer = supporting

  B 중간부 (대비 · layer 변화)

  A' 재현 (주제 회귀 · layer 풍성)

...-end
  fade to credits or end card (~12초)
```

(정확 분량/형식 = V6 본격 작업 + master 자료 base 자리.)

## Assets Needed

- Master audio: ✅ done (`music/masters/Miku_elgar_salut_damour_master.wav` · 2:19 · true-peak fix · 코튼 승인 s343)
- Album cover still 1:1: ✅ done (`video/cover/Miku_waterhouse_soul_of_the_rose.png` 1254×1254 · 코튼 확정 s345 · 렌더 copy = `visualizer/public/cover.png`)
- Visualizer render: pending (조플린/비발디 양식 family · Root.tsx 박힘 · `npx remotion render MuseElgarSalutDAmour`)
- Final export (`video/exports/salut_damour_final.mp4`): pending

(YouTube 썸네일 = 자동 썸네일 활용 · s313 결단 · 별 합성 자리 X.)

## Risk Notes

- **Rights** — composition Elgar d.1934 · life+70 통과(2005) PD 강 (전세계). score = candidates_opus PDF (edition_id 자가 점검 V6 진입 시점 · 가장 깨끗한 PD edition 우선). Waterhouse d.1917 · *The Soul of the Rose* 1903 · life+70 통과(1987) PD 강 전세계 (private collection · PD by age regardless of ownership).
- **Miku character usage** — official artwork 사용 X (Classical Miku anchor 자가 axis · 외부 합성). 라이선스 doctrine = `reference_muse_license.md`.
- **Font** — GFS Didot SIL OFL keep
- **명화 시대** — Waterhouse 1903 (late Pre-Raphaelite) vs Elgar 1888 (낭만) ~15년 · 같은 빅토리아-낭만 zone 정합 강.
- **명화 파일 verify** — ✅ 2026-05-22 통과 (Wikimedia Commons PD 원본 1951×3000 다운로드 · `art_sources/waterhouse_soul_of_the_rose.jpg`).

## 사전 점검 의제 (다음 cycle 자리)

- **V6 입력** — ✅ done (코튼 직접 입력 · `Miku_elgar_salut_damour.wav` 2:19 · master 승인 s343)
- **명화 확정** — ✅ Waterhouse *The Soul of the Rose* 1903 lock (코튼 2026-05-22 s345 · Watts→Marcus Stone→Waterhouse 재선정 · 장미=사랑의 인사 주제 직결 + 단일 몰입 인물 = 합성 자연)
- **커버 확정** — ✅ `cover/Miku_waterhouse_soul_of_the_rose.png` (코튼 s345 확정 · edit-on-reference 합성 + 화풍/명도/채도 원작 매칭)
- **playlist** — *Miku in the Romantic Era* (짐노페디 공유) keep / 신규 자리 (영상 진입 시 최종)
- **다음** — Remotion 렌더 → QC(스피커+헤드폰) → 릴리스 패키지(제목 v9 *(Hatsune Miku Acappella)*·설명 현지화·크레딧·권리) → status/series_history 박고 publish
