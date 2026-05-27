# Video Brief — Morning Mood (Grieg)

> 시리즈 시그너처 = [`../../../README.md`](../../../README.md) § *Series Signature* + [`../../../series_history.csv`](../../../series_history.csv) `signature_mark` 컬럼. 캐릭터 anchor = [`../../../planning/classical_miku_anchor.md`](../../../planning/classical_miku_anchor.md).
> 박힌 날짜: 2026-05-27 (s365) · setup phase · 음악 본격 진입 사전 자료

## Identity

- Project: Atelier Miku Acappella
- Piece: Morning Mood, Peer Gynt Suite No. 1, Op. 46 No. 1 (Edvard Grieg) · 통째 (~4분 · 발췌 없음)
- Release title: Edvard Grieg - Morning Mood (feat. 初音ミク) · s355 후치 양식
- Original title credit: *Morgenstemning* (Morning Mood) · Peer Gynt 극음악 1875 작곡 · Op.46 Suite No.1 1888 재편 · 페르 귄트 4막 도입 전주
- Composer: Edvard Grieg (1843-1907)
- Arrangement: 코튼 V6 직접 입력 (OMR 없음 · 원곡 plaintive 목관 멜로디[플루트·오보에 교대] → lead_miku · 모음/humming layer)
- Vocal: Hatsune Miku (V6) · 가사 없음 (기악 원곡 family)
- Duration: 미정 (V6 작업 후 master 자료 정확 분량 확정 · ~4분 base)
- Release format: YouTube 16:9 + 1:1 album cover still

## Core Promise

```text
Grieg's morning over Norwegian fjords — Peer Gynt's prelude to the desert sunrise now sung, not piped:
Miku alone, voices only, where flute and oboe once traded the rising sun.
```

## Mood

- Primary mood: serene · plaintive · 아침 햇살이 천천히 솟는 정적 (slow reveal)
- Secondary mood: pastoral · 노르웨이 민속 색조 · pentatonic 청량감
- Avoided mood: bright ragtime swagger (조플린 X) · vigorous baroque (비발디 X) · 살롱 다정함 (사랑의 인사 X) · 음울한 모달 (그린슬리브즈 X) · 고요·정적·자연 색조 keep

## Visual Direction

- Painting era or visual reference: Impressionism (Monet) · csv 기본값 · 인상주의 시조 작품 (인상주의 라는 이름 자체가 이 그림에서 유래) · 음악(낭만 후기 1875)과 *인상주의로 가는 다리* axis 정합
- Painting source (artist · title · year · URL): Claude Monet · *Impression, Sunrise* (Impression, soleil levant) · 1872 · oil on canvas · Musée Marmottan Monet (Paris) · Wikimedia Commons `https://commons.wikimedia.org/wiki/File:Monet_-_Impression,_Sunrise.jpg` (V6 진행 중 verify) · 원본 다운로드 자리 = `art_sources/monet_impression_sunrise.jpg`
- Color palette (예상 · cover 합성 후 실측 update 자리):
  - misty blue-grey (dominant · 안개 낀 항구·하늘·물)
  - dusky teal (mid-tone · 물·배·실루엣)
  - warm sunrise orange (accent · 떠오르는 태양·물 반사)
  - soft pink-grey (highlight · 새벽 공기)
- Lighting (명화 빛 source 방향): 우측 수평선 위 떠오르는 태양 · 안개 낀 부드러운 확산 빛 · 짙은 톤 base + 따뜻한 sunrise accent
- Texture: oil on canvas · 인상주의 broken brushwork · 흐릿한 안개 효과 · 빠른 가시 붓질
- Typography: GFS Didot (시리즈 lock · regular weight)
- Visualizer style: 비발디/조플린/사랑의 인사 audio waveform bars (좌·우 letterbox) family keep · 바 색 = sunrise orange accent (cover 실측 후 확정)
- Cover production note: AI 합성 = 원작 배경/구도/인상주의 broken brushwork 보존 + 인물(또는 배 위 미쿠) 합성 axis (edit-on-reference) → 화풍 원작 매칭 → 명도/채도 원작 대조 튜닝. 반복 = `cover/iterations/`. 곡 주제 직결 = 떠오르는 태양 = *아침의 기분*(morning reveal) 주제 직결 · csv 분석 *A sunrise image fits the musical morning reveal.*

## Letterbox (16:9 frame · 1:1 cover 좌·우 negative space)

- Color stops (예상 · 최종 cover 실측 후 Root.tsx `letterboxColors` 박을 자리):
  - top `misty blue-grey 예정` → mid `dusky teal 예정` → bottom `sunrise orange 예정`
- Gradient direction: `linear-gradient(180deg, [0] 0% → [1] 50% → [2] 100%)` (상 안개 → 하 sunrise warm)
- Notes: Monet *Impression, Sunrise* 안개·따뜻한 sunrise 톤 정합 · bottom orange = 비주얼라이저 바 색 겸용 (가시성 + sunrise accent)

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
- Wordmark notes: v3 default 양식 적용 (조플린·사랑의 인사·작은별 family keep)

## Timeline (acappella-only · no DAW capture · 잠정)

```text
00:00-00:03
  fade in to cover (Monet Impression, Sunrise + Classical Miku 합성)

00:03-...
  A 주제 (떠오르는 sunrise 모티프 · plaintive 목관 멜로디 · lead_miku)
  cover + visualizer + 우하단 wordmark
  - 멜로디 = lead_miku · 화성 layer = supporting · pentatonic 색조

  B 발전 (멜로디 layer 확장 · 모음/humming 풍성)

  C 재현 (주제 회귀 · 아침이 본격 밝아오는 climactic)

...-end
  fade to credits or end card (~12초)
```

(정확 분량/형식 = V6 본격 작업 + master 자료 base 자리.)

## Assets Needed

- Master audio: pending (`music/masters/Miku_grieg_morning_mood_master.wav` · V6 입력 + 마스터링 → -18.0 LUFS · true-peak ≤-1.0)
- Album cover still 1:1: pending (`video/cover/Miku_monet_impression_sunrise.png` · 합성 자리 · 렌더 copy = `visualizer/public/cover.png`)
- Visualizer render: pending (조플린/비발디/사랑의 인사 양식 family · Root.tsx 박을 자리 · `npx remotion render MuseGriegMorningMood`)
- Final export (`video/exports/grieg_morning_mood_final.mp4`): pending (2K 양식 = s352 시리즈 default · `--scale=1.333` Phase 9)

(YouTube 썸네일 = 자동 폰트 축소 logic 적용 [s361 작은별 cycle 박힘] · 별 합성 자리 X.)

## Risk Notes

- **Rights** — composition Grieg d.1907 · life+70 통과(1977) PD 강 (전세계). score = candidates_opus PDF (edition_id 자가 점검 V6 진입 시점 · 가장 깨끗한 PD edition 우선). Monet d.1926 · *Impression, Sunrise* 1872 · life+70 통과(1996) PD 강 전세계 (Musée Marmottan Monet 소장 · PD by age regardless of ownership).
- **Miku character usage** — official artwork 사용 X (Classical Miku anchor 자가 axis · 외부 합성). 라이선스 doctrine = `reference_muse_license.md`.
- **Font** — GFS Didot SIL OFL keep
- **명화 시대** — Monet 1872 (인상주의 시조) vs Grieg 1875 (낭만 후기·국민악파) ~3년 · 거의 동시대 · 두 장르 모두 *낭만 후기에서 모더니즘으로 가는 다리* axis 정합 강.
- **명화 파일 verify** — pending (Wikimedia Commons PD 원본 다운로드 → `art_sources/monet_impression_sunrise.jpg` · V6 진행 중 verify 자리).

## 사전 점검 의제 (다음 cycle 자리)

- **V6 입력** — pending (코튼 자리 · 작은별 publish 통과 후 권고 [s359 doctrine] · 작은별 publish 2026-05-28 20:00 KST 예약)
- **명화 확정** — Monet *Impression, Sunrise* 1872 (csv 기본값 lock · 원본 verify는 V6 진행 중)
- **커버 합성** — pending (`cover/Miku_monet_impression_sunrise.png` · edit-on-reference + 인상주의 broken brushwork 보존 + 명도/채도 원작 매칭)
- **playlist** — *Miku in the Romantic Era* (사랑의 인사·짐노페디 공유) keep (s359 결단)
- **letterbox 정밀 색조** — pending (cover 합성 후 실측 박을 자리)
- **release title 양식** — *Edvard Grieg - Morning Mood (feat. 初音ミク)* (s355 후치 양식)
