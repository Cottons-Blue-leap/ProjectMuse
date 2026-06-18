<!--
name: shorts_first_proof
stage: 5 · 본편 publish 후 → 쇼츠 (단일 생산 루트)
type: manual
entry: MikuDiscovery rig(스프라이트 드롭인) + 본편 master 오디오 컷 → 1080×1920 어그로 v3 렌더
inputs: [works/<piece>/music/masters/master.wav, works/<piece>/shorts/<rig>/]
outputs: [YouTube Shorts (Studio 예약 publish)]
depends_on: [video_release]
owner: Cotton+MOKA
-->

# Shorts — Atelier Miku A Cappella (단일 생산 루트)

> 쇼츠 생산 루트 **단일화 확정 2026-06-12** (코튼). 이전 A(콜드오픈 미스터리)·DAW 화면 path = 전부 폐기·삭제.
> 포맷 상세 = [`../../exploration/channel_growth_rnd/05_shorts_funnel.md`](../../exploration/channel_growth_rnd/05_shorts_funnel.md) §11 (어그로 템플릿 v3) + §12 (단일화 결정).

## 목적 (코튼 LOCK · 2026-06-12)

1. **각 곡에 유입을 더한다** — 콜드뷰어 → 본편 퍼널.
2. **채널 정체성을 널리 알린다** — "유명곡을 *미쿠로만* 구현하는 채널" 인지 살포.

→ 수단은 자유. 단 **생산 루트는 하나.**

## 트랙 확정

- **B(어그로) 단일.** A(온브랜드 콜드오픈 "This is not an instrument") = 폐기·삭제(2026-06-12).
- founding value = **어그로·재미 1순위** — s403 2층 분업(본진이 충실성을 짊어지므로 서브는 본진이 못 치는 장난을 칠 자유). ⚠️ 점잖음·brand-safe로 끌어내리지 말 것(자가결함 E44).

## 엔진 = `MikuPile` (v3 범용 · BUILT s427)

- **컴포지션** = `visualizer/src/MikuPileComposition.tsx` (1080×1920 · work-agnostic · 디자인 전부 props). funnel §11.2 어그로 v3 구현 = 그라디언트 + 미쿠 스프라이트 1→N 누적 + "노동력 N명" 카운터 + 훅 캡션 + 루프 + 엔드 CTA. **3→32 스케일 검증 완료.**
- **양식** = `works/<piece>/shorts/<slug>/props.json` (`MikuPileProps`) + `public/`(audio.wav 컷 · miku_wait/sing.png · fonts).
- **스핀업** = `python muse.py short init <work_id> <slug> --start <s> --dur <n> --n <N>` → 폴더+placeholder 스프라이트+오디오컷+본편 그라디언트 자동추출+props 스켈레톤 한 방.
- **렌더** = `python muse.py render <work_id> --short <slug> --comp MikuPile`.
- 스프라이트 = 현재 placeholder(`assets/placeholder/` = canon_round 2차창작 재활용) · 실 미쿠 아트 = `public/miku_*.png` 교체만(엔진/props 불변).
- 변주 엔진 보존 = `MikuDiscovery`(`CanonStageComposition` · 캐논/교육형 = 악보+플레이헤드 · `canon_round` 자산) · `MuseShort`(A·폐기 잔존).
- 설계 = [`docs/v3_engine_design.md`](docs/v3_engine_design.md).

## 포맷 (어그로 템플릿 v3 · funnel §11.2)

- 배경 = 곡별 3색 그라디언트(본편 레터박스 색 재활용)
- 빌드업 = 성부 = 미쿠 스프라이트 **1→N 누적**(비트싱크) + "미쿠 노동력 N명" 카운터
- 절정 = N미쿠 떼창 → 첫 프레임과 맞물려 **무한 루프**
- 래퍼(A층 · 내구성) = 시리즈 제목 프레임 "클래식을 미쿠에 싸서 드셔보세요 #N / [곡명]"
- 훅(B층 · 폭소) = 첫 0.5초 어그로 자막(회차 교체) — 무음 스크롤서 "미쿠임"을 0.5초에 *시각* 증명

## 퍼널 다리 (수동 · 필수 · funnel §4)

1. 마지막 2s 온스크린 CTA "전체 버전은 채널에"
2. 고정댓글 = 본편 직링크 1줄(발행 즉시)
3. 발행 = 본편 공개 *직후*(목적지 존재) · 성장판이면 staggered 2편째
4. 제목 별명 forward

## 측정 (퍼널이 *작동*하는지 · funnel §5)

- ✅ Studio "Shorts feed" → 롱폼 뷰/구독 상승 + CTA 경유 전환
- ❌ raw 쇼츠 뷰·구독(스와이프 허영지표)
- 실험 단위 = **4~6편** 후 scale 결정

## 시그니처 정합

- GFS Didot · 곡별 그라디언트(레터박스 색) keep.
- 명화 1:1 커버는 쇼츠 비주얼 본질 **아님**(스프라이트 떼창이 본질) — 명화는 본편이 담당.

## 상태 + 다음

**✅ 시스템(틀) 완성 (s427)** — 엔진 `MikuPile` 빌드 + 스핀업 `muse short init` + 3→32 스케일 검증. 신곡 쇼츠 = `short init` 한 줄 → props 텍스트 3칸(pieceLabel·hookCaption·#N) → render. ep.1 짐노페디 스캐폴딩 = `works/gymnopedie_1_first_proof/shorts/ep01_pile/`(placeholder · 첫22s 임시컷).

**다음 (포맷·창작 = 곡별 · 첫 쇼츠 제작 시점에)**:
- ⚠️ **어그로 다이얼** — v1 정지구도가 *본진처럼 점잖음*(E44 경보). 모션(퐁퐁 바운스·비트 흔들림·절정 줌)+카운터/훅 카피 어그로화는 첫 실제 쇼츠 만들 때 코튼과 곡별로. 틀은 다 받아줌(props/모션 파라미터).
- 곡별 = 인지 악구 선정(오디오 컷 타임스탬프) · 훅 카피 · 실 미쿠 스프라이트 아트 · 상시 구석 디테일 + 퍼널(본편 직후 발행·고정댓글·CTA).
