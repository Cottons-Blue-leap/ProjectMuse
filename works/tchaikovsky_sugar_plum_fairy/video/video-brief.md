# Video Brief — Dance of the Sugar Plum Fairy (Tchaikovsky)

> 시리즈 시그너처 = [`../../../README.md`](../../../README.md) § *Series Signature* + [`../../../series_history.csv`](../../../series_history.csv) `signature_mark` 컬럼. 캐릭터 anchor = [`../../../planning/classical_miku_anchor.md`](../../../planning/classical_miku_anchor.md).
> **발레 sub-family 컨벤션 = [`../../../planning/ballet_subfamily_convention.md`](../../../planning/ballet_subfamily_convention.md) (이 곡 = 첫 원형).**
> 박힌 날짜: 2026-06-06 · **음악 마스터 LOCK + 커버 LOCK 이후 작성** (실값 확정 brief).
> 확정 상태 단일 source = `../status.json`.

## Identity

- Project: Atelier Miku Acappella
- Piece: Dance of the Sugar Plum Fairy, from *The Nutcracker Suite*, Op.71a No.2(b) (Pyotr Ilyich Tchaikovsky) · 사탕요정 섹션 (Andante non troppo · 2/4 · e단조)
- Release title: Tchaikovsky - Dance of the Sugar Plum Fairy (feat. 初音ミク) · s355 후치 양식 (title=성만 / 본문·커버 헌사=풀네임)
- Original title credit: *The Nutcracker Suite, Op.71a — No.2(b) Danse de la Fée-Dragée* · 1892 작곡
- Composer: Pyotr Ilyich Tchaikovsky (1840–1893)
- Arrangement: 코튼 V6 직접 입력 (첼레스타 R.H. 주선율→lead_miku / 첼레스타 상단 반짝임→halo_high / 현 pizz 베이스→low_oo / pizz 화성→mid_oo / air_mm glue · 모음/humming layer)
- Vocal: Hatsune Miku (V6) · 가사 없음 (기악 원곡 family)
- Duration: **1:46.0 (106.0s)** 확정 (master 실측)
- Release format: YouTube 16:9 (2K 2560×1440) + 1:1 album cover still

## Core Promise

```text
The chiming Sugar Plum Fairy, rebuilt as pure voice: the celesta's glassy bells become Miku's
crystalline upper sparkle while pizzicato strings turn to dry, tip-toeing vowels underneath —
the most delicate dance in the repertoire, danced now with no instrument in the room.
```

## Mood

- Primary mood: 영롱 · 차가운 유리종(celesta) · 통통 튀는 정밀 (staccato 점묘 · tiptoe)
- Secondary mood: 가벼운 우아 · 신비로운 긴장 (e단조 · 서늘한 마법)
- Avoided mood: 무거움 · 따뜻함 · 평온 · 느린 서정 (사탕요정 = 가벼운 staccato지 백조식 비극 서정 X). 캐논의 cumulative warmth, 쇼팽 녹턴의 멜랑콜리 solo와도 구분.
- 차별 axis = **시리즈 첫 발레 sub-family 곡** + 첫 staccato 점묘 텍스처 (이전 곡 legato 흐름과 대비).

## Visual Direction

- Painting: **Pierre-Auguste Renoir · *The Dancer* (La Danseuse) · 1874 · oil on canvas · National Gallery of Art, Washington · Widener Collection 1942.9.72 · Open Access** — **LOCK** (2026-06-06).
- Painting source: Wikimedia Commons (NGA Open Access scan · 3840×5812 · PD-Art) → `art_sources/renoir_the_dancer_1874_nga.jpg`. 라이선스 = `art_sources/source-rights-notes.md`.
- 선정 사유 (발레 sub-family (B) 첫 원형): 사탕요정 = 솔로 발레리나의 우아·정밀한 춤 → *The Dancer*(단독 정면 발레리나)가 직결. 단독 인물 = Classical Miku 합성 최적. Renoir 화가 미사용(중복 0) · PD 최저리스크(d.1919 + NGA Open Access). Degas(백조 예약)와 충돌 없음.
- Color palette (커버 실측 · 2026-06-06 · cold silver-blue 단일 계열):
  - bg deep slate `#3a5468` · mid slate-blue `#54707c` · highlight `#879daa` · floor `#7f9194`
  - 전체 = 차가운 은청(silver-blue) = celesta 유리종/서리 영롱함 인코딩 (Pachelbel식 듀얼톤 아님 = cold 단일).
- Lighting: 어두운 무대 + 미쿠에 떨어지는 soft spotlight + 공중 청백 crystalline sparkle.
- Texture: oil on canvas · Renoir 인상주의 soft blended 화풍 (부드러운 붓터치 보존).
- Typography: GFS Didot (시리즈 lock · **Romantic = medium weight, slightly larger title** per video_workflow Phase 3).
- Visualizer style: 좌·우 letterbox vertical bars (s381 band-remap default) · 바 색 = letterboxColors[2] auto. gain = 곡별 결단 (아래 Risk/의제).
- Cover production note: GPT image-edit (*The Dancer* 원작 attach · 원작 구도/화풍/발레리나 보존 + 얼굴/머리/복식만 Classical Miku + 은청 톤 + sparkle) → **(가) 명화 보존 방식**. 최종 = `cover/Miku_renoir_the_dancer.png` (1254×1254). 프롬프트·cycle = `art_sources/cover-gen-notes.md`. **GPT 생성 = 코튼 손** + MOKA 프롬프트/비평.

## Letterbox (16:9 frame · 1:1 cover 좌·우 negative space)

- Color stops (커버 실측 base · cold silver-blue 단일 계열 = celesta 영롱함):
  - top `#3a5468` (deep slate · 상단 배경 깊이) → mid `#54707c` (slate-blue 전이) → bottom `#7f9194` (밝은 청회 floor · sparkle · 비주얼라이저 바 색 겸용)
  - ⚠️ **base 값 · album_1x1 합성 후 dominant tone 재실측 자리** (텍스트 합성이 색조 미세 변동).
- Gradient direction: `linear-gradient(180deg, [0] 0% → [1] 50% → [2] 100%)`.
- Notes: 듀얼톤(Pachelbel 청록↔웜골드) 아님 = 사탕요정은 cold 단일 영롱 = celesta 유리종. bottom = 비주얼라이저 바 색 겸용.

## Channel Wordmark (시리즈 시그너처 v3 default)

frame 우하단 corner *Atelier Miku Acappella* · 좌하단 title mirror axis.
- Color: cream `#e8e0c8` · *Miku*의 *M*: banner 청록 `rgb(40, 180, 175)`
- text-shadow: `0 2px 12px rgba(0, 0, 0, 0.75)` · Size: 40 (좌하단 piece_title 56 의 ~70%)
- 자리: margin_right 81 + margin_bottom 90 · Opacity: 1.0
- Wordmark notes: v3 default 양식 (family keep).

## Text Stack (좌하단 · 풀네임 헌사)

```text
Pyotr Ilyich Tchaikovsky
Dance of the Sugar Plum Fairy
```
GFS Didot · left align · 좌하단 1/4 quadrant · Romantic medium weight · 명화 영역 침범 X.

## Timeline (acappella-only · master 실측 base · 106.0s)

```text
00:00-00:06
  fade in to cover (Renoir + Classical Miku 합성 · letterbox 동시 fade)

00:06-~01:40
  album cover + restrained visualizer (좌·우 letterbox bars · band-remap)
  staccato 점묘 = 바가 또각또각 점멸 (celesta sparkle 정합 · cumulative arc 아님)

~01:40-01:46
  slow fade to end (reverb tail 보존 · 마지막 프레임 의도적)
```

> ★ **before-after outro = 이번 편 보류** (코튼 2026-06-06). 디졸브는 프로세스를 제대로 갖춘 뒤 별도 실험 → 원작 1:1 base는 `art_sources/renoir_the_dancer_1874_1x1.png` (5812 · padding+blur)에 확보. 이번 편은 디졸브 없는 standard family 흐름(커버+letterbox+visualizer).

(정확 fade 분량 = 렌더 시점 master 파형 base 미세 조정.)

## Assets

- Master audio: **DONE** `music/masters/Miku_tchaikovsky_sugar_plum_fairy_master.wav` (-17.6 LUFS / TP -1.7 / 106.0s · test5 LOCK).
- Album cover still 1:1: **커버 합성 DONE** (`cover/Miku_renoir_the_dancer.png` 1254×1254) → **pending: album_1x1.png (텍스트 스택 + wordmark 합성 + ≥2560 업스케일)**.
- before-after용 원작 1:1: pending (`art_sources/renoir_the_dancer_1874_nga.jpg` → The Dancer 인물 중심 1:1 crop · 커버와 매칭).
- Visualizer render: pending (band-remap · Root.tsx 2K 직접 지정 · `remotion render` · outro 씬 신규 추가).
- Final export: pending (`video/exports/tchaikovsky_sugar_plum_fairy_final.mp4` · 2K 2560×1440 · Phase 9 정공 path).

## Risk Notes

- **Rights** — composition Tchaikovsky d.1893 · life+70 PD 강(전세계). 명화 = Renoir d.1919 · 1874 작 · PD 강(life+70 1990 / 미국 1929 이전) · NGA Open Access PD-Art. 상세 = `art_sources/source-rights-notes.md`.
- **명화 conflict 자가 점검** — Renoir 시리즈 미사용 → 중복 0. Degas(백조의 호수 *The Star*) 예약과 충돌 없음(발레 sub-family (B) = 곡별 다른 화가).
- **Miku character usage** — official artwork 사용 X (Classical Miku anchor 외부 합성). 라이선스 = `reference_muse_license.md`.
- **Font** — GFS Didot SIL OFL keep.
- **명화↔곡 시대** — Renoir 1874(인상주의) vs Tchaikovsky 1892(낭만). 동시대 근접(19c 후반) · 발레=Renoir Paris 정합.
- **커버 해상도** — 1254×1254 (family 발행 선례 해상도) → album_1x1 ≥2560 업스케일 필요 (Phase 9).

## 사전 점검 의제 (영상 cycle 자리 · 코튼 결단)

- **album_1x1 합성** — 커버(1254) → 텍스트 스택(좌하단 풀네임) + wordmark(우하단) + ≥2560 업스케일.
- **before-after outro (신규)** — 발레 컨벤션 첫 시범. 원작 The Dancer 1:1 crop ↔ 미쿠 커버 디졸브 + 크레딧. visualizer에 outro 씬 추가 (코드 작업) · ~4s · 음악 종료 후. 좋으면 라이브 6곡 소급 검토.
- **1:1 crop (원작)** — The Dancer 원본 portrait(3840×5812) → 발레리나 인물 중심 1:1 (미쿠 커버 구도와 매칭되게).
- **visualizer gain 결단** — band-remap · 캐논·쇼팽 = 2.0 선례. 사탕요정 staccato 점묘 정합 gain은 렌더 단 결단 (또각또각 점멸 살리는 값).
- **playlist** — *Miku in the Romantic Era* (쇼팽 녹턴 등 공유 · status channel).
- **고정 댓글** — 다음 곡 예고 path (publish cycle 시점).
- **썸네일 v5** — muse_thumbnail.py REGISTRY에 tchaikovsky 추가 (dir/cover/box/composer/piece · 풀네임 Pyotr Ilyich Tchaikovsky/공간부족시 성만) → `--song`.
