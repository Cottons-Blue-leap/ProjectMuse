# Project Muse — Comment Intelligence Report

> 생성 2026-06-16 · source `comments.csv` (19건 = 청중 11 / 우리 8 · 답글 4) · 발행작 10편
> layer 1 수집 = `comments_pull.py` (결정적) · layer 2 분석 = MOKA 패스 (정서/카테고리/요청/언어 태깅)
> ⚠️ `is_own=1`(우리 고정댓글·답글)은 청중 집계에서 제외 · 스레드 맥락(요청 상태)용으로만 사용

---

## 1. 한눈에

- **청중 댓글 11건 / 10영상** · 정서 **거의 전부 긍정** (positive 10 · negative 1→해소)
- **언어 = 전부 영어** — l10n 9개 언어 적용에도 현재 댓글 유입은 anglophone (JP/KO 미유입 = 워치 포인트)
- **미처리 선곡요청 1건**(밤의 여왕) · **AI회의 스레드 1건(해소됨)** · **튜토 명시요청 0**

## 2. 영상별 청중 볼륨

| 영상 | 청중 댓글 | 비고 |
|---|--:|---|
| Boccherini - Minuet | 2 | AI회의 스레드(답글 3) + 발견 |
| Tchaikovsky - Sugar Plum Fairy | 2 | 선곡요청(밤의여왕) + 호평 |
| Joplin - Entertainer | 2 | "A classic" / "sturdy to this beat"(밈) |
| Handel - Lascia ch'io pianga | 1 | "Such masterpiece" |
| Pachelbel - Canon in D | 1 | "this is the best" (유일 좋아요 1) |
| Mozart - K.265 | 1 | "wow genius!!" |
| Vivaldi - Spring I | 1 | "HATSUNE MIKU?!?!?!" (리빌 반응) |
| Gymnopédie / Elgar / Chopin | 0 | 청중 댓글 없음 |

## 3. 정서 분포 (청중 11)

- **positive 10 · neutral 0 · negative 1**(해소) — 부정 1건은 "ai slop" 우려였고 응대 후 전향 → 실질 순긍정.

## 4. 🎵 선곡 요청 (열린 것)

| 요청곡 | 출처 | 상태 | 메모 |
|---|---|---|---|
| **Queen of the Night** (Mozart, *Der Hölle Rache* K.620) | Tchaikovsky 영상 | **acknowledged** (우리 답글 *"Noted! …the Queen is coming soon"*) | candidate_master S tier 등재곡 · 코튼 "⑩ 헨델 이후 자격" → **이제 자격 충족** · 첫 청취자 신청곡 |

→ 액션: 밤의 여왕은 **"청취자 요청받아 만든 곡" description hook 자산**으로 묶임(post-release doctrine 정합). 차기 선곡 후보 1순위 재료.

## 5. ⚠️ AI 회의 워치 ([[muse_v6_positioning]] 방어선)

- **Boccherini 스레드**: 청중 *"I see a song from 2026, my first fear is ai slop."* → 우리 *"Miku V6 & VOCALOID6 editor로 손수 제작"* 설명 → **회의자 전향** *"ahaa.. thats nice! this is a very nice project."*
- **학습 = 방어선 작동 검증**: AI 낙인 우려 → **즉시 응대 + hand-made V6 설명**이 전향시킴. 향후 동일 패턴 재현 시 그대로 대응. (회의 = 무시 X · 대화로 해자 강화)

## 6. 발견 / 리빌 반응 (s355 커튼 설계 검증)

- *"HATSUNE MIKU?!?!?!"* (Vivaldi) · *"finally… I know the name of this piece"* (Boccherini) · *"This is definitely a new way to hear Miku"* (Tchaikovsky)
- → 제목에서 'a cappella' 감춰 발견시키는 설계 + 클래식 인지 멜로디 조합이 의도대로 작동.

## 7. 튜토리얼 / 학습트랙 수요 (s325 조건부 게이트)

- **명시 요청 0건** — 단 AI회의 스레드에서 우리가 V6 제작법을 자발 설명함.
- counter = 0 → 학습 영상 트랙 **미발동 (정상)**. *"how did you make this / tutorial please"* 누적 시 게이트 재논의.

## 8. 다음

- **주기**: 주간 수집 의례 통합 vs on-demand (코튼 결정 대기).
- **스케일링**: 볼륨 증가 시 layer 2를 구조화(`comments_analyzed.csv` 태그 컬럼) + subagent 태깅으로 확장. 현 볼륨(11)은 본 리포트 단일 산출이 적정 altitude.
