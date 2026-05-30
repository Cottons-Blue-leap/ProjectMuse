# Post-Release Retrospective — Mozart, Twelve Variations K.265

> 작은별 변주곡 다섯 번째 작품 publish 회고 자료. 여섯 번째 곡(쇼팽 녹턴 Op.9-2) 진입 전 자가 점검 axis.
> Post-publish 자리 = publish 통과 후 박음 (s380 · 2026-05-29)
> 박힌 양식 doctrine = [`workflows/video_release/docs/post_release_meta_doctrine.md`](../../workflows/video_release/docs/post_release_meta_doctrine.md)

## 작품 자료

- 곡: Wolfgang Amadeus Mozart, Twelve Variations on "Ah, vous dirai-je, maman" K.265 (1781-82) · 통째 (Theme + 12 Variations · 13 챕터 · 0:00~5:09)
- 영상 제목: Mozart - Variations on "Twinkle, Twinkle, Little Star" K.265 (feat. Hatsune Miku)
- 명화: Vincent van Gogh, *Starry Night Over the Rhône* (1888) · Musée d'Orsay · Public Domain
- 보컬: Hatsune Miku (Vocaloid6) · 9 voice acappella (Lead 3 + Mid 2 + Base 4)
- 영상 URL: https://youtu.be/PiR9hy6xmGQ
- Publish: 2026-05-28 (목) 20:00 KST · public/processed (s380 라이브 확인)
- 재생목록: Miku in the Classical Era (시리즈 첫 고전파)

---

## Part 1. Pre-Publish 자리 (s320~s361)

**음악 production**
- s320 3차 곡 결단 → s326 keep 보류(scope 부담 자가 적발) → s347 재진입(코튼 *A로 진행* · full-12 결단) → s361 완주
- V6 코튼 직접 입력 9 Mikus (Lead 3 + Mid 2 + Base 4 · .vpr audit)
- master 6:02 도돌이 제거(s352) → `music/renders/Miku_Ah! vous dirai-je, maman.wav` 95MB · 48kHz stereo · V6 export 직 master
- listening_decision passed (s361 · 코튼 *품질 OK* · Phase 10 시청 통과)

**영상 production (s361) — 시리즈 첫 2K 마일스톤**
- 2K 정공 path = composition 직접 2560×1440 + wrap div `transform: scale(4/3)`로 1920×1080 좌표계 keep (이전 `--scale=1.333` 비정수 trap[1080×1.333=1439.64 ffmpeg 거부] 자가 catch + video_workflow.md Phase 5·9 + visualizer-spec.md 정정 박음 · 신곡 default 2K 박힘)
- cover = Starry Night Over the Rhône (1888) base + Classical Miku 우하단 강가 자리 합성(원작 커플 Miku 단독 교체 · ChatGPT 코튼 path) · 2508×2508 `video/cover/album_1x1.png`
- 썸네일 v5 자동 폰트 축소 logic 신축(make_thumbnail.py · scale=0.836 · F_PIECE 92→76 · 폭 초과 fallback default doctrine)
- 풀 렌더 = `video/exports/mozart_twinkle_variations_k265_final.mp4` 2560×1440 · 361.5s · 59.5MB · h264+aac
- 챕터 13 (Theme + Var 1~12 · 0:00~5:09)
- description 3 로케일 curator voice 코튼 직접 정정 (en "The familiar melody from childhood." / ja "幼い頃に聞きなれた曲。" / ko "어릴 적 자주 듣던 노래.")
- audit s361 통과 후 defaultLanguage=en 누락 catch → youtube_meta.py에 --default-language 옵션 부수 추가 + set 적용

---

## Part 2. Post-Publish 자리 (publish + ~28h · Data API v3 · s380 · 2026-05-29)

> publish + 30분/24h 정시 스냅샷은 미측정. 본 자료 = publish + ~27.9h 시점 Data API v3(공개 stats · 비지연) 단일 측정.

- PRIVACY = `public`
- PUBLISHED_AT = 2026-05-28 20:00 KST (예약 정시)
- VIEW_COUNT = **20**
- LIKE_COUNT = 4 (**like rate 20.0% = 시리즈 최고**)
- COMMENT_COUNT = 1

**채널 stats** (동시 측정):
- subscriberCount = 11 (조플린 48h 시점 8 → +3 누적)
- videoCount = 5
- channel viewCount = 340

**시리즈 비교** (현재 누적 · 경과 일수 다름):
- ① 짐노페디 145뷰 / 14라이크 (publish + ~15일)
- ② 비발디 38뷰 / 5라이크 / 1댓글 (publish + ~11일)
- ③ 조플린 112뷰 / 8라이크 / 2댓글 (publish + ~8일 · 여전히 누적 선두)
- ④ 엘가 36뷰 / 1라이크 (publish + ~4일)
- ⑤ **작은별 20뷰 / 4라이크 (20.0%) / 1댓글 (publish + ~28일... +28h)**

### 자가 점검 (예측 vs 실측)

- **좋아요율 시리즈 최고(20%)지만 뷰 속도는 modest** = 본 시리즈 트래픽 가설 정합. 조플린 breakout(업비트·인식 멜로디 → 추천 멀리)이 *뷰 velocity*를 만들었다면, 작은별은 *친숙도 강(작은별=세계적 인식 멜로디)*인데도 5분 길이 + 클래식 변주 양식이 velocity를 누른 것으로 추정. 좋아요율 20%는 *온 사람은 만족*을 시사 → 노출/CTR 병목 가설과 정합.
- ⚠️ 본 측정은 단일 시점(+28h)이라 추세 단정 X. +3d(5/31) / +7d(6/4) 도달 자료가 정합 결론 base (s379 retro 이월 의제 · `studio_reach.csv` 코튼 손).

### 레버 자료

- 시리즈 첫 2K 작품 = 화질 레버 (썸네일/영상 선명도 향상 · CTR 영향 관찰 axis keep)
- CTR/노출은 Studio 전용(Data API 미노출) → 코튼 Studio 확인 의제 keep

---

## Part 3. 여섯 번째 곡 진입 전 자가 점검 (publish 후)

### 시리즈 trajectory

낭만[짐노페디] → 바로크[비발디] → ragtime[조플린] → 낭만[엘가] → **고전[작은별]** → 낭만[쇼팽 녹턴 Op.9-2, 진행 중]

### 여섯 번째 곡

- **쇼팽 녹턴 Op.9-2** (낭만 · 1830-32 작곡) · setup 완료(s369) · V6 입력 전 명화 결단 cycle 진입(s380)
- 미해결 결단 2건: (a) 명화 — csv 기본값이 짐노페디 라이브와 동일 Whistler *Old Battersea Bridge*라 충돌 → swap 결단 자리 / (b) edition_id 자가 점검 (op.9 통째 PDF에서 9-2 picking)

### Doctrine 정정 의제 후보

- 2K 정공 path(composition 직접 2K + wrap scale)가 신곡 default로 박힘 → video_workflow.md Phase 5·9 + visualizer-spec.md 정정 통과(s361). 후속 곡 default 적용 검증 axis keep.

---

## 정정 이력

- v1 (s380 · 2026-05-29 · publish + ~28h) — Pre-publish(Part 1) + Post-publish(Part 2 · Data API v3 20뷰/4라이크[20% 시리즈 최고]/1댓글 + 채널 11sub/340뷰/5영상) + Part 3(6번째 곡 쇼팽 진입) 통째 박음. post_release_meta_doctrine 6 step 완주.
