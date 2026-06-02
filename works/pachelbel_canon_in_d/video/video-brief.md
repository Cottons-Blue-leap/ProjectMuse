# Video Brief — Canon in D (Pachelbel)

> 시리즈 시그너처 = [`../../../README.md`](../../../README.md) § *Series Signature* + [`../../../series_history.csv`](../../../series_history.csv) `signature_mark` 컬럼. 캐릭터 anchor = [`../../../planning/classical_miku_anchor.md`](../../../planning/classical_miku_anchor.md).
> 박힌 날짜: 2026-06-02 (s389) · **음악 마스터 LOCK + 명화 LOCK 이후 작성** (쇼팽 setup-phase brief와 달리 실값 확정 brief · stale 항목 없음).
> 확정 상태 단일 source = `../status.json`.

## Identity

- Project: Atelier Miku Acappella
- Piece: Canon in D major, P.37 (Johann Pachelbel) · 통째 (~5:48 · 발췌 없음 · Canon만 · 동봉 Gigue 제외 · ground bass + 3성 캐논 양식)
- Release title: Johann Pachelbel - Canon in D (feat. 初音ミク) · s355 후치 양식
- Original title credit: *Canon and Gigue in D major, P.37* · c.1680~90 작곡 추정 (Canon만 발췌)
- Composer: Johann Pachelbel (1653-1706)
- Arrangement: 코튼 V6 직접 입력 (OMR 없음 · 원곡 = 2마디 8음 ground bass [D-A-B-F#-G-D-G-A] 반복 + 3 violin 캐논 → low_oo=ground / lead_miku·mid_oo·halo_high=캐논 시차 entry / air_mm=glue · 모음/humming layer)
- Vocal: Hatsune Miku (V6) · 가사 없음 (기악 원곡 family)
- Duration: **5:48.0 (348.0s)** 확정 (s388 master 실측)
- Release format: YouTube 16:9 (2K 2560×1440) + 1:1 album cover still

## Core Promise

```text
The wedding-canon everyone knows, rebuilt as pure voice: Miku's ground bass turns eight notes
in an endless circle while three more Mikus enter one bar apart and stack the canon over it —
the texture filling, then emptying, with no instrument in the room.
```

## Mood

- Primary mood: warm · serene · cumulative (성부가 겹겹이 쌓이는 다성 충만감)
- Secondary mood: processional dignity · timeless circling (ground bass 순환의 명상성)
- Avoided mood: 쇼팽 녹턴(솔로 피아노 멜랑콜리·잔잔) 직후 → **무드 대비 axis** = 따뜻·고양·다성 카운터포인트로 호흡 전환. 비발디 봄의 vigorous attack과도 구분 (캐논 = gentle cumulative, not vivace).
- 차별 axis = **시리즈 첫 본격 카운터포인트 곡** (짐노페디 sparse / 쇼팽 ornamental solo line 과 양식 차별 강 · 점층 누적 양식).

## Visual Direction

- Painting: **Johannes Vermeer · *A Young Woman seated at a Virginal* · c.1670-72 · oil on canvas · The National Gallery, London · NG2568** — **LOCK** (s388).
- Painting source: Wikimedia Commons Google Art Project scan (10100×11371 · PD-Art) → `art_sources/vermeer_young_woman_seated_at_a_virginal_NG2568_GAP.jpg`. 라이선스 = `art_sources/source-rights-notes.md`.
- 선정 사유 (관계훅): 전경 좌측 **viola da gamba(bass viol) + 버지널(건반) = 바로크 basso continuo(통주저음) 편성** ↔ **캐논 in D = 반복 ground bass 위 성부 쌓기**. 그림이 곧 캐논의 통주저음 텍스처를 담음 (제네릭 음악화 넘어선 특정 관계). + Vermeer 청록 블루 드레스 = Classical Miku 청록 팔레트 정합 + Dutch Baroque = 파헬벨 동시대 + 화가 미사용(중복 0).
- Color palette (명화 실측 · s389):
  - dress(청록 슬레이트, 성부 cool accent) `#2A3F44`
  - viola da gamba(웜 시에나, ground bass warm) `#6D411E`
  - floor `#3D311F` · bg wall `#2C2A25` · curtain `#172026` (warm dark olive-brown dominant)
- Lighting (명화 빛 source): 좌측 창에서 들어오는 부드러운 측광 (Vermeer 전형 · 좌→우 falloff).
- Texture: oil on canvas · Vermeer smooth blended 화풍 (매끈한 음영 전이 · pointillé 하이라이트).
- Typography: GFS Didot (시리즈 lock · regular weight · Bach·Pachelbel = compact layout per video_workflow Phase 3).
- Visualizer style: 좌·우 letterbox vertical bars (s381 band-remap 신형 default · 신곡 ⑥ 쇼팽부터) · 바 색 = letterboxColors[2] auto. gain = 곡별 결단 (아래 Risk/의제).
- Cover production note: GPT 이미지-edit (원작 배경/구도/화풍 보존 + 좌석 여인을 Classical Miku로 재해석) → Vermeer 화풍 매칭 → 명도/채도 원작 대조 튜닝. 반복 = `cover/iterations/`. 프롬프트 = `art_sources/cover-gen-notes.md`. **GPT 이미지 생성 = 코튼 손** + iteration 비평.

## Letterbox (16:9 frame · 1:1 cover 좌·우 negative space)

- Color stops (명화 실측 base · 관계훅 인코딩 = 청록 성부 → 웜 ground bass):
  - top `#2A3F44` (dress 청록) → mid `#33352C` (전이 · olive) → bottom `#4B3A24` (viola/floor warm gold · 채도 muted)
  - ⚠️ **base 값 · 커버 합성 후 dominant tone 재실측 자리** (쇼팽 path 정합 · 합성이 색조 미세 변동).
- Gradient direction: `linear-gradient(180deg, [0] 0% → [1] 50% → [2] 100%)`.
- Notes: 청록(상)→웜골드(하) = 성부(dress)↔통주저음(viola da gamba) duality를 레터박스에 인코딩. bottom = 비주얼라이저 바 색 겸용.

## Channel Wordmark (시리즈 시그너처 v3 default 양식 적용)

frame 우하단 corner *Atelier Miku Acappella* wordmark · 좌하단 title mirror axis.

시리즈 anchor (작품별 가변 X):
- Color: cream `#e8e0c8` · *Miku*의 *M*: banner 청록 `rgb(40, 180, 175)`
- text-shadow: `0 2px 12px rgba(0, 0, 0, 0.75)` · Size: 40 (좌하단 piece_title 56 의 ~70%)
- 자리: margin_right 81 + margin_bottom 90 · Opacity: 1.0
- Wordmark notes: v3 default 양식 적용 (쇼팽·작은별·그리그 family keep).

## Timeline (acappella-only · no DAW capture · master 실측 base)

```text
00:00-00:08
  fade in to cover (Vermeer + Classical Miku 합성 · letterbox 동시 fade)

00:08-~05:43
  album cover + restrained visualizer (좌·우 letterbox bars)
  ground bass 8음 순환 위 캐논 성부 점층 누적 → 후반 비워지는 dynamic arc
  (visualizer 바 밀도가 성부 누적과 정합 · s381 band-remap)

~05:43-05:48
  slow fade to end (reverb tail 보존 · 마지막 프레임 의도적)
```

(정확 fade 분량 = 렌더 시점 master 파형 base 미세 조정.)

## Assets

- Master audio: **DONE** `music/masters/Miku_pachelbel_canon_in_d_master.wav` (-16.8 LUFS / TP -3.3 / 5:48.0 / 24bit 44.1k · passthrough).
- Album cover still 1:1: pending (`video/cover/album_1x1.png` · ≥2560px · GPT 합성 후 · 렌더 copy = `visualizer/public/cover.png`).
- Visualizer render: pending (s381 band-remap · Root.tsx 2K 직접 지정 · `remotion render`).
- Final export: pending (`video/exports/pachelbel_canon_in_d_final.mp4` · 2K 2560×1440 · Phase 9 정공 path = composition 직접 2560×1440 + 내부 scale(4/3), `--scale` 옵션 X).

## Risk Notes

- **Rights** — composition Pachelbel d.1706 · life+70 통과 PD 강 (전세계). score = candidates_opus PDF (Canon and Gigue P.37 · Canon만 picking · Gigue 제외). 명화 = Vermeer d.1675 life+70 통과(1745) PD 강 · Commons PD-Art Google Art Project scan (NG London 자체 스캔 직접 scrape X). 상세 = `art_sources/source-rights-notes.md`.
- **명화 conflict 자가 점검** — Vermeer 시리즈 미사용 → 중복 0. ⚠️ 동명 Leiden Collection(개인소장 소형)판과 구분 — NG London NG2568 확정 (Commons 카테고리 검증).
- **Miku character usage** — official artwork 사용 X (Classical Miku anchor 외부 합성). 라이선스 doctrine = `reference_muse_license.md`.
- **Font** — GFS Didot SIL OFL keep.
- **명화 시대** — Vermeer c.1670-72 = Dutch Baroque = 파헬벨 c.1680-90 동시대 정합 강.
- **figuration passage** — 후반 빠른 16/32분 figuration = V6 양식 challenge였으나 마스터 LOCK 통과 (코튼 청취 OK) → 영상 단 issue 없음.

## 사전 점검 의제 (영상 cycle 자리 · 코튼 결단)

- **커버 합성** — Vermeer 좌석 여인 → Classical Miku 재해석 (청록 트윈테일 · 이미 청록 드레스라 자연 정합). GPT 이미지-edit (코튼 손) + MOKA 프롬프트 (`cover-gen-notes.md`). Miku 존재감 = A (쇼팽 원경 어부와 달리 여인 자체가 연주자 → 존재감 강하되 painterly 통합).
- **1:1 crop 자리** — 원본 portrait (10100×11371). 1:1 square crop에 여인+버지널+viola da gamba 담기게 crop 결단 (합성 후).
- **visualizer gain 결단** — s381 band-remap · 쇼팽 = 2.0 lock. 캐논 gain은 곡별 결단 자리 (cumulative texture 정합 axis).
- **playlist** — *Miku in the Baroque Era* (비발디 봄 1악장 공유 · 시대 정합 강).
- **고정 댓글** — 다음 곡 ⑧ 예고 path (`次の曲：...` 양식 · publish cycle 시점).
- **썸네일 v5** — muse_thumbnail.py REGISTRY에 pachelbel 추가 (dir/cover/box/composer/piece) → `--song`.
