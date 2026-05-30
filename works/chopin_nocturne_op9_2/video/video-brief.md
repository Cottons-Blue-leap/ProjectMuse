# Video Brief — Nocturne Op. 9 No. 2 (Chopin)

> 시리즈 시그너처 = [`../../../README.md`](../../../README.md) § *Series Signature* + [`../../../series_history.csv`](../../../series_history.csv) `signature_mark` 컬럼. 캐릭터 anchor = [`../../../planning/classical_miku_anchor.md`](../../../planning/classical_miku_anchor.md).
> 박힌 날짜: 2026-05-27 (s369) · setup phase · 음악 본격 진입 사전 자료 · 그리그 swap path

## Identity

- Project: Atelier Miku Acappella
- Piece: Nocturne in E-flat major, Op. 9 No. 2 (Frédéric Chopin) · 통째 (~4분 · 발췌 없음 · ABA' 양식)
- Release title: Frédéric Chopin - Nocturne Op. 9 No. 2 (feat. 初音ミク) · s355 후치 양식
- Original title credit: *Nocturne in E-flat major, Op. 9 No. 2* · 1830-32 작곡 · 1833 출판 (Maria Wodzińska 헌정)
- Composer: Frédéric Chopin (1810-1849)
- Arrangement: 코튼 V6 직접 입력 (OMR 없음 · 원곡 solo piano · RH bel canto → lead_miku · LH waltz-like arpeggio → mid_oo+low_oo 분배 axis · 모음/humming layer)
- Vocal: Hatsune Miku (V6) · 가사 없음 (기악 원곡 family)
- Duration: 미정 (V6 작업 후 master 자료 정확 분량 확정 · ~4분 base)
- Release format: YouTube 16:9 + 1:1 album cover still

## Core Promise

```text
Chopin's most famous nocturne — Maria Wodzińska's bel canto dedication now sung, not played:
Miku alone, voices only, where the right hand once sang and the left hand wove its arpeggio.
```

## Mood

- Primary mood: lyric · bel canto · 야상곡 정취 (private lamp-lit reverie)
- Secondary mood: ornamental fluency · waltz-like rocking · 살롱 친밀감
- Avoided mood: bright ragtime swagger (조플린 X) · vigorous baroque (비발디 X) · 파스토랄 morning hush (그리그 X · swap) · 음울한 모달 (그린슬리브즈 X) · 고요·정적·sustained lyric keep
- ⚠️ 자가 결함 risk 사전 발화 = 짐노페디(sparse atmospheric calm) + 사랑의 인사(salon lyric) family *calm/lyric* 누적 axis · s337 달빛 추천 시 *짐노페디 계보 post-hoc 장식* 자가 결함 family 정합 risk · 차별 axis = **시리즈 첫 솔로 피아노 원곡** (양식 차별점 강 · 짐노페디 sparse vs 쇼팽 ornamental bel canto)

## Visual Direction

- Painting era or visual reference: ⚠️ **swap path 의제 자리 keep** (csv 기본값 Whistler *Old Battersea Bridge* = 짐노페디 라이브 명화와 정확히 동일 axis = swap 의무 자료) · 코튼 *초안 · 곡 만들고 다시 봐 볼게* 흡수 = V6 본격 진입 후 결단 자리
- Painting source (csv 기본값 = swap 의제 자리 · V6 본격 진입 후 결단): James McNeill Whistler · *Nocturne in Blue and Gold: Old Battersea Bridge* · c. 1872-1875 · oil on canvas · Tate Britain · Wikimedia Commons (V6 진입 시점 verify 자리 · ⚠️ 짐노페디 conflict axis · 원본 다운로드 자리 = `art_sources/{TBD}.jpg`)
- Swap 자가 후보 5건 (V6 본격 진입 후 결단 자리 · 코튼 자가 결단 결단 자리):
  - (a) Whistler *Nocturne in Black and Gold: The Falling Rocket* (1875) — Whistler 야상곡 시리즈 axis 정합 + 다른 작품
  - (b) Whistler *Nocturne: Blue and Silver—Chelsea* (1871) — Whistler 야상곡 시리즈 axis 정합
  - (c) Van Gogh *Starry Night Over the Rhône* (1888) — 같은 화가 다른 야상 작품 (Starry Night MoMA 자료 X)
  - (d) Caspar David Friedrich *Moonrise over the Sea* (1822) — 낭만 야상 anchor 강
  - (e) Friedrich *Two Men Contemplating the Moon* (1819) — 낭만 sublime night
- Color palette (pending · cover 결단 + 합성 후 실측 박을 자리):
  - 자가 자료 X (명화 swap 결단 전 axis · V6 본격 진입 후 결단)
- Lighting (명화 빛 source 방향): pending (명화 결단 후)
- Texture: oil on canvas · 명화별 화풍 axis (Whistler aestheticism / Van Gogh post-impressionism / Friedrich German Romanticism) · 결단 후 자리
- Typography: GFS Didot (시리즈 lock · regular weight)
- Visualizer style: 비발디/조플린/사랑의 인사/그리그 audio waveform bars (좌·우 letterbox) family keep · 바 색 = 명화 결단 후 실측 자리
- Cover production note: AI 합성 = 원작 배경/구도/화풍 보존 + 인물(또는 명화 안 미쿠) 합성 axis (edit-on-reference) → 화풍 원작 매칭 → 명도/채도 원작 대조 튜닝. 반복 = `cover/iterations/`. 곡 주제 직결 = 야상곡 정취 = *밤 lamp-lit lyric* 주제 직결.

## Letterbox (16:9 frame · 1:1 cover 좌·우 negative space)

- Color stops (pending · 명화 결단 + 합성 후 실측 · Root.tsx `letterboxColors` 박을 자리):
  - top `pending` → mid `pending` → bottom `pending`
- Gradient direction: `linear-gradient(180deg, [0] 0% → [1] 50% → [2] 100%)` (명화 dominant tone gradient · 결단 후 자리)
- Notes: 명화 결단 후 dominant tone 자료 실측 + bottom = 비주얼라이저 바 색 겸용 (가시성 + 명화 accent)

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
- Wordmark notes: v3 default 양식 적용 (조플린·사랑의 인사·작은별·그리그 family keep)

## Timeline (acappella-only · no DAW capture · 잠정)

```text
00:00-00:03
  fade in to cover (명화 결단 + Classical Miku 합성)

00:03-...
  A 주제 (bel canto 멜로디 12 마디 · lead_miku · LH waltz-like arpeggio = mid_oo+low_oo)
  cover + visualizer + 우하단 wordmark

  B 발전 (멜로디 변형 12 마디 · emotional crescendo · halo_high lyrical sustain layer 추가)

  A' 재현 (12 마디 · ornamental flourish 양식 결단 자리 · coda)
    - ornamental flourish 32분 음표 fluid passage = V6 양식 challenge axis · 코튼 결단 자리

...-end
  fade to credits or end card (~12초)
```

(정확 분량/형식 = V6 본격 작업 + master 자료 base 자리.)

## Assets Needed

- Master audio: pending (`music/masters/Miku_chopin_nocturne_op9_2_master.wav` · V6 입력 + 마스터링 → -18.0 LUFS · true-peak ≤-1.0)
- Album cover still 1:1: pending (`video/cover/Miku_{TBD}.png` · 명화 결단 후 합성 자리 · 렌더 copy = `visualizer/public/cover.png`)
- Visualizer render: pending (조플린/비발디/사랑의 인사/그리그 양식 family · Root.tsx 박을 자리 · `npx remotion render MuseChopinNocturneOp9No2`)
- Final export (`video/exports/chopin_nocturne_op9_2_final.mp4`): pending (2K 양식 = s352 시리즈 default · `--scale=1.333` Phase 9)

(YouTube 썸네일 = 자동 폰트 축소 logic 적용 [s361 작은별 cycle 박힘] · 별 합성 자리 X.)

## Risk Notes

- **Rights** — composition Chopin d.1849 · life+70 통과(1919) PD 강 (전세계). score = candidates_opus PDF (op.9 통째 박힘 · 9-2 picking + edition_id 자가 점검 V6 진입 시점 · 가장 깨끗한 PD edition 우선). 명화 자료 = swap 의제 자리 keep · 결단 후 verify (Whistler d.1903 life+70 통과 1973 / Van Gogh d.1890 life+70 통과 1960 / Friedrich d.1840 life+70 통과 1910 · 후보 5건 다 PD 강).
- **명화 conflict 자가 적발** — csv 기본값 Whistler *Old Battersea Bridge* = 짐노페디 라이브 1차 곡 명화와 정확히 동일 axis · 시리즈 *같은 명화 두 번* 자가 회피 의무 = swap path 결단 axis (V6 본격 진입 후 코튼 자가 결단).
- **Miku character usage** — official artwork 사용 X (Classical Miku anchor 자가 axis · 외부 합성). 라이선스 doctrine = `reference_muse_license.md`.
- **Font** — GFS Didot SIL OFL keep
- **명화 시대** — pending (명화 결단 후 시대 정합 자가 박을 자리 · 쇼팽 1830-32 = 낭만 초기 · Whistler/Friedrich 19c 후/전반 양식 정합 axis · Van Gogh 1888 post-impressionism axis)
- **자가 색 겹침 risk** — 짐노페디·사랑의 인사 family *calm/lyric* 누적 axis 정직 자가 발화 (s337 달빛 sample 정합) · 차별 axis = 시리즈 첫 솔로 피아노 원곡 양식

## 사전 점검 의제 (다음 cycle 자리)

- **V6 입력** — pending (코튼 자리 · 작은별 publish 통과 후 권고 [s359 doctrine] · 작은별 publish 2026-05-28 20:00 KST 예약)
- **op.9 PDF picking** — score PDF op.9 통째 (9-1·9-2·9-3 추정 · 1.87MB) · V6 진입 시점 9-2 picking 의제
- **edition_id 자가 점검** — V6 진입 시점 자료 (가장 깨끗한 PD edition 우선)
- **명화 결단 자리** — Whistler conflict axis = swap 의무 자료 · 자가 후보 5건 throw · V6 본격 진입 후 결단 자리 (코튼 *곡 만들고 다시 봐 볼게* 자료 정합)
- **ornamental flourish 양식 결단** — A' coda 32분 음표 fluid passage = V6 challenge axis · 코튼 결단 자리 (omit / 단순화 / 그대로 keep)
- **커버 합성** — pending (명화 결단 후 · `cover/Miku_{TBD}.png` · edit-on-reference + 명화 화풍 보존 + 명도/채도 원작 매칭)
- **playlist** — *Miku in the Romantic Era* (사랑의 인사·짐노페디 공유) keep (시대 정합 강 · 쇼팽 1830-32 = 낭만 초기)
- **letterbox 정밀 색조** — pending (명화 결단 + 커버 합성 후 실측 박을 자리)
- **release title 양식** — *Frédéric Chopin - Nocturne Op. 9 No. 2 (feat. 初音ミク)* (s355 후치 양식)
- **그리그 keep 보류 자료** — `../grieg_morning_mood/` keep · 7~8번째 재진입 의제 (코튼 결단 자리)
