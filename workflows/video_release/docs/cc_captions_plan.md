# CC 자막 트랙 표준화 — 작업계획

> 작성 2026-06-17 · 발의 코튼 (Discord) · 대상 = Project Muse 가사 곡(미쿠가 실제 가사를 부르는 성악 레퍼토리)
> 파일럿 = ⑩ 헨델 「Lascia ch'io pianga」 (vid `xHzbkP_Wcm0` · 예약 6/15 18:45 KST 발행)

---

## 0. 확정 사항 (코튼 LOCK · 2026-06-17)

- **CC 자막 트랙을 표준으로 채택** (로케일별 트랙 = 10개).
- **2줄 표출 = [1줄: 원어] + [2줄: 시청자 국적어 번역].**
  - 예외: `시청자 국적어 == 원어`인 트랙은 원어 1줄만 (반복 회피).
  - 헨델 원어 = 이탈리아어 → 우리 10로케일(en·ja·ko·es·pt·de·fr·ru·zh-Hant·zh-Hans) 중 이탈리아어 없음 → **헨델은 10트랙 전부 2줄.** 예외 룰은 미래 곡(예: 독일 가곡 → de 트랙 1줄)에 발동.
- **영상 자체에 "자막 있음" 표시 필요** → ① 인트로 짧은 큐(3~5초) + ② 설명란/고정댓글 텍스트 안내. 썸네일 뱃지는 비채택(아트워크 정체성 보호).
- **적용 범위 = 가사 곡 한정.** 기악→보칼리제("Ah") 곡은 자막·인트로 큐 대상 아님.

---

## 1. 핵심 리스크 — 자막 타이밍 (MOKA 청취불가 제약)

자막은 timed cue(각 가사 줄의 start/end)가 필요한데 MOKA는 오디오 청취가 안 됨([[reference_muse_loudness_baseline]] 계측 자문 축). 타이밍 소스 후보:

1. **(추천) V6 프로젝트(.vpr) 노트 온셋 추출** — VOCALOID6 프로젝트에 Lead 트랙 음절별 노트 시작 시각이 이미 들어있음. 음절→가사 줄 매핑으로 줄 단위 cue 자동 생성. MOKA가 청취 없이 만들 수 있는 유일한 정밀 소스.
2. **(게이트) 코튼 1회 청취 sync 확인** — 자동 생성 cue를 마스터에 얹어 코튼이 1회 들으며 밀림 보정. listen-gate 독트린([[feedback_muse_arrangement_listen_gate]]) 정합.
3. (폴백) 느린 아리아라 줄 수가 적음(A절4+B절4, da capo로 A 재등장) → 최악의 경우 코튼 수동 마킹도 현실적.

→ **결정 필요 (코튼)**: .vpr 온셋 추출을 1차 경로로 갈지. (status.json 상 헨델 마스터=test4, .vpr 보존 여부 확인 필요 — Phase 2에서 점검.)

da capo A-B-A 구조라 A절 가사는 **두 번** 등장 = cue도 2세트.

---

## 2. 작업 단계

### Phase 1 — 가사 마스터 + 번역 (10로케일)
- 원어(이탈리아어) 가사 = `notes/lyrics_and_arrangement.md §1`에 이미 존재 (Rossi 리브레토 1711 · PD).
- 신규 `works/<id>/lyrics/lyrics.json` = 줄 단위 원어 + 10로케일 번역 마스터(단일 source).
- **번역 방법론 (코튼 2026-06-17 · 직접 번역 X)**:
  1. 각 로케일별 **기존 권위 번역본 탐색** (웹) — 유명 아리아라 정평 번역이 다수 존재(공연 자막·악보·아트송 DB·학술). 출처 기록.
  2. 권위본을 **토대로** + 원문 직역을 **참고**하여 **우리 확정본 합성**. (정평본 verbatim 복제는 **저작권 회피** — 근래 번역가 번역은 보호 대상일 수 있음. 참고로 의미·뉘앙스 정합만 차용하고 우리 표현으로 확정. PD/출처불명 고전 번역은 인용 여지.)
  3. 확정본 → **l10n 교차검수 3층 게이트**([[feedback_l10n_cross_verification]]) (Claude QA → 웹 사실검증 → 교차모델). 기준 = "의미 충실 + 시적 자연스러움 + 원문 행 대응".
- KO 직역 이미 있음(같은 파일 §1.30) = 참고 baseline (이것도 권위본 대조 후 확정).
- 산출: `lyrics/lyrics.json` (lines[] = {idx, section(A/B), original, {ko,en,ja,...}}) + 로케일별 출처/참고 메모.

### Phase 2 — 타이밍 추출 + sync 게이트
- 헨델 `.vpr` 존재/보존 확인 (`music/` 또는 `edit_project/`).
- `.vpr` 파싱 → Lead 트랙 음절 노트 온셋 → 가사 줄 경계 cue (start/end) 생성. da capo 반복 포함.
- 신규 스크립트 `workflows/video_release/scripts/muse_captions.py` (timing 추출 + VTT 생성 통합).
- **코튼 1회 청취 sync 게이트** → 밀림 보정값 반영.
- 산출: `lyrics/cues.json` (timed · 언어 무관 · 1세트).

### Phase 3 — 로케일별 VTT 생성 (2줄 포맷)
- `cues.json` × `lyrics.json` → 로케일별 `lyrics/captions.<lang>.vtt` (10개).
- 줄 구성: `{original}\n{translation}` (cue당 2줄). `lang==원어` 예외 시 1줄.
- WebVTT 포맷 (YouTube 권장). 검증: cue 시간 겹침 0, 끝 cue ≤ durationSeconds.

### Phase 4 — YouTube 자막 업로드 도구
- 신규 `Analytics/youtube_captions.py` (youtube_meta.py 패턴 병렬):
  - `captions.insert()` (트랙 신규) / `captions.list()` (감사) / `captions.update()` 또는 delete+insert (갱신).
  - **스코프**: 기존 write 토큰이 `youtube.force-ssl` 보유 → captions.insert 동일 스코프라 **재인증 불필요**(Phase 4 착수 시 1차 검증).
  - 트랙당 `language` 파라미터 = 로케일 코드. `name`(트랙 표시명) 규약 정하기.
  - **양 채널 주의 없음** — Muse는 단일 채널. (Moltbook 2채널과 다름.)
- 산출: `python ... youtube_captions.py insert --vid <id> --lang ko --file captions.ko.vtt` 등 + 일괄 push.

### Phase 5 — "자막 있음" 큐 (비주얼라이저) · **디자인 LOCK (코튼 2026-06-17)**
- `VisualizerComposition.tsx`에 prop `hasCaptions: boolean` (기본 false) 추가 → true일 때만 큐 렌더. **구현 완료.**
- **LOCK 디자인** = `CC ▸ Lyrics` 표식 (CC = **검정 블록(#141414) + 밝은 회색 글씨(#ECECEC)** = 표준 자막 아이콘 컨벤션, ▸ = teal 워드마크색, Lyrics = 크림 TEXT_COLOR, GFSDidot). **위치 = 우하단, "Atelier Miku Acappella" 워드마크 바로 위 · 우측 정렬**(우측 끝이 워드마크와 정렬). **상시 고정 · opacity 0.92(워드마크급 시인성) · 깜박임/펄스 없음.** Lyrics 글씨 서식 = 다른 텍스트(워드마크·작곡가)와 **통일**(색 TEXT_COLOR·섀도우 TEXT_SHADOW·자간 0.02em·폰트사이즈만 별도). 전역 FADE_IN(90프레임)과 함께 자연 페이드인. 중간/늦은 유입 시청자도 인지 = 상시 표시 채택. 검정 블록 = 밝은 레터박스 하단에서도 대비 확보(시인성).
  - (시안 cycle 기록: ① 우상단 초반 페이드아웃 → ② 펄스 2회+상시 → ③ Rec식 깜박임+상시 → ④ 상시 고정 0.7 → ⑤ **우하단 워드마크 위 우측정렬로 이동** 채택. 코튼 "깜박임 없이 상시 고정 0.7, 우하단 워드마크 위 우측정렬, 시인성 확보".)
- `props.json`에 `hasCaptions: true` 주입(가사 곡만). 기악 곡 = 미주입 → 변화 없음(forward-only, 기존 6곡 영향 0).
- **헨델 제외** (위 Phase 8 참조). 실제 적용 = 차기 가사 곡부터. 시안 LOCK 산출 = `works/handel.../video/visualizer/out/cc_cue_LOCK.png`.

> **부수 변경 — 전역 텍스트 윤곽선 (코튼 2026-06-17, CC 작업 중 발의)**: 비주얼라이저 **모든 온스크린 텍스트**(작곡가·제목·부제·워드마크·챕터·CC큐)에 **0.8px 다크 stroke**(`rgba(0,0,0,0.5)` · `paintOrder: stroke fill`로 글자 면 뒤 윤곽) 추가. `TEXT_OUTLINE` 공유 상수. **forward-only** — 발행된 6곡은 재렌더 X(신·구 영상 미세차 인지·수용). CC 한정 아님 = 전 신곡 영상에 적용.

### Phase 6 — 설명/고정댓글 CC 안내
- description 템플릿에 선택 블록 1줄: "▸ 가사 자막을 보려면 CC를 켜세요 (원어 + 번역)" (로케일별).
- `localize_batch.py` 에 가사 곡 플래그 시 자동 삽입(custom_hook 분기 방식 재활용).
- 고정댓글에도 동일 안내 1줄 (post_release 단계).

### Phase 7 — 표준화 (도구·문서·CLI)
- `muse.py` 서브커맨드 `captions` 추가 (SCRIPTS dict 1줄 + `muse_captions.py`).
- 신규 독트린 `workflows/video_release/docs/cc_captions_doctrine.md` (포맷·2줄 룰·예외·타이밍 소스·업로드 절차).
- `post_release_meta_doctrine.md` **Step 9 신설** = "가사 곡: CC 자막 10로케일 업로드 + audit".
- `naming_convention.md` 에 `lyrics/` 디렉토리 + 파일 규약 추가.
- `description_template.md` 에 CC 안내 블록 명시.

### Phase 8 — 헨델 파일럿 적용 + 감사
- Phase 1~4·6 헨델에 실제 적용 → 10트랙 업로드 → `captions.list()` audit (10개 존재·언어코드·2줄 확인) → 코튼 실시청 1회.
- 헨델은 이미 발행 예약본(`xHzbkP_Wcm0`)이라 **라이브 비디오에 자막 트랙 추가**(메타와 달리 자막은 발행 후에도 안전하게 추가 가능).
- **⚠️ 헨델은 인트로 큐(Phase 5) 제외** (코튼 2026-06-17) — 영상이 이미 렌더+발행 예약됨. 재렌더 시 vid 변경·예약 파기 비용 > 인트로 큐 이득. 따라서 헨델 = **CC 자막 트랙 + 설명/고정댓글 안내까지만.** 인트로 큐는 **시안만 제작**(차기 가사 곡 적용 준비) → 코튼 시안 승인 후 다음 가사 곡부터 영상 단계에 편입.

### Phase 9 — 미래 곡 정착
- 신곡 제작 워크플로우(WORKFLOW.md)에 "가사 곡이면 자막 단계" 분기 추가.
- 다음 가사 곡부터 영상 단계에 기본 편입.

---

## 3. 신규/변경 산출물 요약

| 종류 | 경로 | 상태 |
|---|---|---|
| 가사 마스터 | `works/<id>/lyrics/lyrics.json` | 신규 |
| 타이밍 cue | `works/<id>/lyrics/cues.json` | 신규 |
| 로케일 VTT | `works/<id>/lyrics/captions.<lang>.vtt` ×10 | 신규 |
| 자막 도구 | `Analytics/youtube_captions.py` | 신규 |
| 통합 스크립트 | `workflows/video_release/scripts/muse_captions.py` | 신규 |
| 비주얼라이저 | `VisualizerComposition.tsx` (+`hasCaptions`) · `props.json` | 변경 |
| CLI | `muse.py` (+`captions`) | 변경 |
| 문서 | `cc_captions_doctrine.md`(신규) · `post_release_meta_doctrine.md`(Step9) · `naming_convention.md` · `description_template.md` · `localize_batch.py` | 변경 |

---

## 4. 코튼 결단 대기 (착수 전)

1. **타이밍 소스** = .vpr 노트 온셋 추출 1차 경로 OK? (대안 = 코튼 수동 마킹)
2. **인트로 큐 문안/위치** = "CC ▸ Lyrics" 코너 페이드 방향 OK? 시안 먼저 볼지(--still 렌더).
3. **착수 범위** = 전체 파이프 한 번에 vs 헨델 1곡 end-to-end 먼저 깔고 표준화는 그 뒤. (추천 = 후자 = 헨델로 검증 후 doctrine 박기.)
