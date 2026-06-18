# v3 Shorts Engine — 확장형 파이프라인 설계

> 설계 LOCK 대기 (코튼 sign-off) · 2026-06-13 (s427).
> 토대 = 락된 R&D: [`05_shorts_funnel.md`](../../../exploration/channel_growth_rnd/05_shorts_funnel.md) §11.2 (어그로 템플릿 v3) · §12 (B 단일화) + 본 워크플로 [`README.md`](../README.md).
> 본 문서 = funnel R&D의 *포맷 결정*을 **반복 가능한 엔진 + 곡별 레시피**로 구현하는 엔지니어링 스펙.

---

## 0. 과제 (한 줄)

현 rig(`canon_round` / `MikuDiscovery` = 캐논 특화 교육형 — 악보 스크롤+플레이헤드)를 **v3 어그로 범용 엔진**으로 일반화한다. 산출물 = 쇼츠 1편이 아니라 *신곡당 가볍게 양산되는 파이프라인*.

---

## 1. 아키텍처 = 엔진 1개 + 곡별 레시피

### 1.1 엔진 (한 번 빌드 · work-agnostic)
- 새 Remotion 컴포지션 **`MikuPile`** (1080×1920 · 30fps · 루프형). 기존 `--short` 렌더 배관(`muse_render.py`) 그대로 사용 — `--comp MikuPile`.
- 디자인 면(색·스프라이트·카피·타이밍·N) **전부 props**. 곡별로 코드 0 수정.
- 본편 엔진(`VisualizerComposition` = canonical ccf27a) + `ShortsComposition`(A·폐기 잔존) + `CanonStageComposition`(교육형 변주) **불가침** — `MikuPile`은 별도 신규 등록.

### 1.2 곡별 레시피 (반복 · 경량)
| 단계 | 입력 | 자동/수동 |
|---|---|---|
| ① 인지 악구 오디오 컷 | 본편 master.wav | MOKA 추천 타임스탬프 → 코튼 승인 · ffmpeg 컷 |
| ② 그라디언트 | 본편 레터박스 3색 | **자동** (본편 데이터서 추출) |
| ③ N (성부 수) | 본편 트랙 수 | 자동/수동 |
| ④ 스프라이트 드롭인 | 대기/노래 PNG | placeholder → 2차창작 교체 |
| ⑤ props.json 생성 | ①~④ + 수동 3칸 | 수동 = `#N` · 곡명 · **훅 카피** |
| ⑥ 렌더 | `muse render <id> --short <slug> --comp MikuPile` | 자동 |
| ⑦ 메타 + 업로드 + 고정댓글 | 락된 퍼널 doctrine | 본편 직후 발행 |

→ **확장성** = 엔진 1회 빌드 후 신곡당 "오디오컷 + 텍스트 3줄 + 스프라이트"만.

---

## 2. `MikuPile` 컴포지션 스펙

### 2.1 Props 스키마
```ts
export type MikuPileProps = {
  // 음악·오디오
  audioPath: string;          // 컷된 악구 (public 상대경로)
  bpm: number;                // 비트싱크용
  beatsPerBar: number;
  buildStartSec: number;      // 페이크 솔로 → 폭증 전환 시각
  // 누적
  voiceCount: number;         // N (= "미쿠 노동력 N명")
  spriteWait: string;         // 대기 PNG (public 상대)
  spriteSing: string;         // 노래 PNG
  // 스킨 (곡별)
  gradient: [string, string, string];  // 본편 레터박스 3색
  // 텍스트 (곡별 = 회차 교체)
  episodeNo: number;          // #N
  pieceLabel: string;         // 부제 곡명 (예: "짐노페디 1번")
  hookCaption: string;        // ★ B층 훅 (코튼 요구 = 곡당 최소 1개 · 필수)
  cornerDetail: string;       // 상시 작은 디테일 (예: "39" / "파")
  // 엔드
  endCta: string;             // "전체 버전은 채널에"
  durationSeconds: number;
} & Record<string, unknown>;
```

### 2.2 비주얼 타임라인 (funnel §11.2 실현)
```
배경(상시) = gradient 3색 (linear 160deg)
상시        = 우상단 카운터 "미쿠 노동력 {N}명" · 화면 구석 cornerDetail (깜빡 X)

[0 ~ buildStart]  ① 페이크 솔로 — 미쿠 1명 잔잔 + 제목 밈 프레임
                     "클래식을 미쿠에 싸서 드셔보세요 #{N}" / "{pieceLabel}"
                     + hookCaption (첫 ~0.5s 번인 = 무음 스크롤 정지력)
[buildStart ~]    ② 폭증 빌드업 ← 심장 — 성부 = 스프라이트 1→N 비트싱크 퐁퐁
                     누적될 때마다 카운터 증가 · 진입 perk-up(튀어오름)
[절정]            ③ N 미쿠 떼창 — 화면 꽉 참
[루프]            마지막 프레임 ≈ 첫 프레임 (무한 리플레이 신호)
[마지막 2s]       엔드 CTA "{endCta}" + 워드마크 (퍼널 다리 §4)
```

### 2.3 재활용 프리미티브
- `ShortsComposition`서: GFS Didot 폰트 로딩 · 엔드카드 scrim+CTA+워드마크 · `hexToRgba` · 세이프존(상단 240 / 하단 480 / 우측 200).
- `CanonStageComposition`서: 스프라이트 wait→sing 드롭인 + glow + perk-up · bpm 비트싱크(`beatPulse`) · gradient bg.
- 신규: 1→N **누적 배치**(악보 정렬 대신 화면 채우는 "벽/더미") · 카운터 · 제목 밈 프레임 · 훅 캡션 B층 · 루프 seam.

### 2.4 세이프존·타이포
- 1080×1920 · 상단 240/하단 480/우측 200 회피 (UI·캡션 레일).
- GFS Didot · cream `#e8e0c8` · teal `rgb(40,180,175)` (시리즈 불변 토큰).

---

## 3. per-episode 훅 슬롯 (코튼 요구 = 곡당 최소 1개)

`hookCaption` = **필수 props**. 곡 특성에 따라 훅의 *출처*가 다름:
- **고-N 스펙터클 곡** (사탕요정 N=32): "미쿠 노동력 32명" 카운터 + 떼창 폭증 자체가 훅.
- **저-N 잔잔 곡** (짐노페디 N=3): 스펙터클 약함 → 훅은 **데드팬 대비 카피**가 짊어짐 ("피아노인 줄 알았지? 미쿠 3명임ㅋㅋ" 류) + 저-N 카운터를 *코미디*로("겨우 3명이서").
- 어느 경우든 첫 ~0.5s에 ①인지 멜로디 + ②"미쿠임" 시각증명 + ③훅 카피 더블/트리플샷 (§9.2).

→ 엔진은 둘 다 같은 슬롯(hookCaption + voiceCount 누적)으로 커버. 곡이 약하면 카피가, 강하면 물량이 훅이 됨.

---

## 4. ep.1 = 짐노페디 1번 (업로드 순 · 코튼 결정)

| 필드 | 값 |
|---|---|
| gradient | `#1f2c3d` · `#4a5a6e` · `#b8a673` (휘슬러 Nocturne — 본편 레터박스 재사용) |
| voiceCount (N) | **3** (lead_miku + mid_oo + low_oo) |
| audio | `works/gymnopedie_1_first_proof/music/midi/render_ready_v1/Miku_Gymnopeddie_1.wav` → 인지 악구 컷 |
| episodeNo | 1 |
| pieceLabel | 짐노페디 1번 |
| hookCaption | (제안) **"피아노인 줄 알았지?"** → 폭증서 "미쿠 3명임ㅋㅋ" — 저-N 데드팬 |
| 제목 프레임 | 클래식을 미쿠에 싸서 드셔보세요 #1 / 짐노페디 1번 |

⚠️ 짐노페디 = 시리즈 최약 스펙터클(저-N·잔잔)이라 ep.1로는 난이도 높음(코튼이 "곡당 훅 필수"로 정확히 겨냥). 훅 카피가 전부 짊어지는 첫 시험대.

---

## 5. 스프라이트 계획 (코튼: 아직 없음)

- 엔진은 **sprite-agnostic** — wait/sing PNG를 props로만 받음(CanonStage 양식 동일).
- **지금** = placeholder 스프라이트(단순 미쿠 실루엣/스탠드인)로 엔진 end-to-end 렌더 검증.
- **나중** = 2차창작 미쿠 아트 드롭인 = public PNG 교체만, props/엔진 불변.

---

## 6. 미결 / 코튼 결단 대기

1. **훅 카피** ep.1 (§4 제안 = "피아노인 줄 알았지? 미쿠 3명임") — 코튼 승인/교체.
2. **오디오 악구** = MOKA 인지 악구 추천 → 코튼 승인.
3. **상시 cornerDetail** 내용 (39 / 파 / 기타).
4. **실 스프라이트 아트** 소스 (코튼 2차창작 라인 / image-gen).

---

## 7. 빌드 순서

1. `MikuPileComposition.tsx` 신축 + `Root.tsx` 등록 (`MikuPile`).  ← 엔진
2. placeholder 스프라이트 + 짐노페디 `shorts/ep01_pile/` 스캐폴딩 (오디오 컷·props).
3. still 렌더 → MOKA 시각 검증 → 코튼 react.
4. 훅·악구 확정 → 풀 렌더 → QC → 업로드 파이프(본편 직후).
5. workflow doctrine 동기(`README.md` v3 엔진 절 + registry).
</content>
</invoke>
