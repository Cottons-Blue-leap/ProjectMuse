# Cover Generation Notes — Handel: Lascia ch'io pianga (Rinaldo HWV 7b, 1711)

> Method: **MOKA writes prompt → 코튼이 GPT image generation** (image-edit). NOT local ComfyUI. 선례 = Pachelbel/Chopin/Sugar Plum/Boccherini cover-gen-notes.
> 표준 path (NOT 발레 sub-family). 화가맵 = **Handel→Rossetti** (status.json rights 단 LOCK 2026-06-09 코튼·s414).

## 베이스 명화 (LOCKED 2026-06-09)

**Dante Gabriel Rossetti, *Proserpine* (1874), oil on canvas 125.1×61cm, Tate Britain N05064.** PD강 (d.1882). 소스 = `rossetti_proserpine_1874_gap.jpg` (1041×2300 · Google Art Project · PD-Art) + `source-image-url.txt` + `source-rights-notes.md`.

**선정 논리** (status.json에서 전재): 지하세계에 *감금*된 페르세포네가 석류(운명의 속박)를 들고 바깥 빛을 갈망 = 투옥된 알미레나의 비탄·자유 갈망·사슬(ritorte)과 1:1 정서 매칭. 단독 여성·세로 구도 = 미쿠 치환 최적.

### 원작 구도 (실물 시각 검증 2026-06-11)
- **단독 여성** (Jane Morris 모델) — 4분의 3 측면, 얼굴 좌향, 시선은 먼 곳 (멜랑콜리·갈망).
- **머리**: 짙은 갈색 풍성한 웨이브 — 화면 상부를 가득 채우는 볼륨.
- **가운**: ★ **짙은 청록(teal-blue) 실크** + 은빛 하이라이트 — **이미 미쿠 시그너처 색**. 보존 시 색 정합 공짜.
- **손**: 한 손에 베어 문 석류(가슴 높이), 다른 손이 그 손목을 감쌈.
- **배경**: 어두운 회색 벽 + 회색 빛 조각(바깥 세계의 빛 한 줄기) + 좌측 담쟁이 덩굴 + 좌하단 청동 향로.
- **원작 명문**: 우상단 소네트 패널 + 하단 서명 스크롤 = 원작의 일부 (보존 대상 · 1:1 크롭에서 빠질 수 있음).

## 설계 결정 (v1 프롬프트 전 · ⑨ 보케리니 7-cycle 교훈 선반영)

1. **화풍 진단**: Rossetti 라파엘전파 = 매끈한 글레이즈·보석 톤·이상화된 사실주의 = **타이트 계열** (Renoir 인상주의보다 Longhi 쪽에 가까움). → ⑨ 핵심 교훈 직행 적용 = **"Rossetti가 직접 미쿠를 그렸다면" 프레임, 매체(유화)와 식별(특징 3개) 분리 지정**. v1부터 ⑨ v6/v7 패턴으로 시작.
2. **Youthening front-load** (⑨ v1 과보존 교훈): Jane Morris 이목구비가 매우 강함(강한 턱선·두꺼운 입술·성숙한 얼굴) → "NOT the original mature woman" 명시 + 둥근 앳된 얼굴 전면 배치.
3. **포즈 충돌 없음** (⑧ 교훈 회피): 원작 포즈(석류+손목)가 그대로 우리가 원하는 포즈 → 깨끗한 보존+리스킨.
4. **가운 보존**: 청록 실크 = 미쿠 색이 이미 화면의 주인공. 트윈테일은 가운보다 **살짝 밝은 teal**로 분리 지정 (머리↔가운 융합 방지).
5. **표정**: 원작 멜랑콜리 *유지·심화* — 비탄+갈망 (Lascia ch'io pianga 정서축). 생기 있되 슬픈 눈.
6. **크롭 = 1:1 추후** (얼굴+석류+손 중심 예상 · 원본 종횡비로 생성).

## Prompt v1 (image-edit · 원작 Proserpine 1장 attach · GPT 새 세션)

```
Attached is Dante Gabriel Rossetti's "Proserpine" (1874), a Pre-Raphaelite oil painting: a melancholic woman in a deep teal-blue silk gown stands against a dark wall, holding a bitten pomegranate at her chest, her other hand clasping that wrist; an ivy sprig hangs beside her, a soft shaft of gray light glows on the wall, and a small incense burner sits at the lower left.

Edit this painting so the woman becomes Hatsune Miku — while the ENTIRE image still looks like Rossetti's original oil. The single hardest requirement: fully preserve the painting's tone and manner (deep jewel-toned Pre-Raphaelite oil, smooth glazed brushwork, somber light) AND make Miku clearly recognizable AT THE SAME TIME. Do not sacrifice either one.

Imagine Rossetti himself painted a portrait of Hatsune Miku. Render her entirely in his OIL technique — smooth painterly modeling, deep palette, softly painted shading. NOT flat cel shading, NOT hard anime outlines, NOT bright cartoon coloring. She is an oil-painted figure, never a cartoon pasted on top.

Yet she must be unmistakably Hatsune Miku, through her iconic features rendered in oil:
- Long teal twin-tails tied in two tails — her most recognizable trait, replacing the dark wavy hair but framing her face with the same volume; slightly lighter than the gown so they read against it, never neon.
- A youthful, girlish round face — clearly a young teenage girl, NOT the original mature woman: soft round cheeks, a small nose and a small soft mouth, delicate East-Asian features (drop the original's strong jaw and heavy lips).
- Noticeably large, soft, gentle eyes with a teal tint — larger and more expressive than a realistic portrait, but painted softly. Alive, never a blank doll.
- Slender, petite build.

Keep everything else exactly as Rossetti painted it: her exact pose (three-quarter view, head turned, the bitten pomegranate at her chest, one hand clasping the other wrist), the deep teal-blue silk gown with its silvery highlights, the ivy, the shaft of light, the incense burner, the dark wall, the whole composition. Expression: quietly sorrowful and yearning — grief and longing in her eyes, but soft and alive. Keep the original aspect ratio. Add no new text or border; the painting's own small inscription panels may remain.
```

> ⏳ v1 후 4축 체크 = ① 미쿠 식별(트윈테일·앳된 얼굴·큰 눈) ② 원작 톤앤매너 보존(라파엘전파 유화·somber) ③ 포즈·가운·소품 보존 ④ 인형/만화 양극단 회피.
> 실패 모드별 다이얼 (⑨ 매핑 재사용): 성인 그대로 = youthening 더 front-load / 인형(uncanny) = 사실유화 당김 과함 → 눈·생기 쪽 해방 / 만화 paste = anime 해방 과함 → 매체 고정 강화. 표정만 미세조정 = 별 세션 surgical("Change ONLY her facial expression").

## Iteration log (코튼 generation 시점)
- **v1 결과 (코튼 2026-06-11 · 표정 거부)**: 4축 중 3축 성공 — ① 미쿠 식별 ✓ (틸 트윈테일+리본·앳된 둥근 얼굴) ② 톤앤매너 ✓ (라파엘전파 다크 유화·somber 통합·인형/만화 양극단 회피) ③ 포즈·가운·소품 ✓ (석류+손목·청록 실크·담쟁이·빛 조각·향로·명문 패널까지 보존). **BUT ④ 표정 = 무표정** — 눈을 내리깔고 졸린 듯한 수동적 멜랑콜리. 원작 페르세포네의 핵심인 **경계하는 곁눈 시선(wary sidelong gaze)**이 증발.
  - **진단**: v1 프롬프트에서 표정이 맨 끝에 한 줄("quietly sorrowful and yearning")로 묻혀 있었고, "soft/gentle/calm" 계열 형용사가 프롬프트 전반에 깔려 평균이 '온순한 무표정'으로 수렴. 원작 표정의 *심리*(감금된 자의 경계+비탄)를 명시 안 함.
  - **경로 (코튼 지시)**: 처음부터 재작성 (⑨ v3 교훈 정합 = GPT 자기 출력 face-refine은 보수적·무변화 → from-scratch 재생성이 옳음).
- **v2 단일 레버 = 표정 front-load**: 표정을 TONE과 동급의 2대 요구사항으로 승격 + 원작 심리 명시("EXACT psychological expression of Rossetti's original Proserpine · wary, haunted sidelong gaze · captive who senses she is not free") + 구체 지정(눈 뜨고 ALERT·곁눈·먼 곳 응시·미간 살짝·입 다묾) + 부정 명시(NOT expressionless/blank/sleepy/downcast/idle smile). 나머지 v1 그대로 (성공축 3개 불변). = `cover-prompt-v2.txt`
- **v2 결과 (코튼 2026-06-11 · 거부 2건)**: 시선은 곁눈 방향으로 개선(v1 downcast 탈출). BUT ① **머리끈 시대 불일치** — 미쿠 기본 모던 클립(각진 분홍/검정 홀더)이 그대로 나옴 = 1874 그림에 이물 ② **슬픔이 얼굴에서 안 묻어남** — 경계 쪽으로만 읽히고 비탄 불가독.
  - **진단**: ① 프롬프트가 트윈테일만 지정하고 묶는 방식을 미지정 → GPT가 미쿠 기본 클립 디폴트 ② v2에서 wary를 앞세우며 sorrow 구체 지정(눈물·미간·입꼬리)이 없었음.
- **v3 레버 2개 (코튼 지적 그대로)**: ① 머리끈 = 어두운 무광 실크/벨벳 밴드(머리에 녹아드는 딥톤·1874 정합) + 부정 명시(NO plastic clips/Miku's angular red-black holders/bright ribbons/contemporary bows) + TONE 절에 "NOTHING modern anywhere" 추가 ② 슬픔 가독 = 첫눈에 '슬프다'가 읽히게 구체 지정(눈물 참는 촉촉한 눈·눈썹 안쪽 들림·입꼬리 무게) + wary는 유지하되 블렌드 명시("a captive girl on the edge of tears, yet still alert"). = `cover-prompt-v3.txt`
- **v3 결과 (코튼 2026-06-11 · 표정 과침울)**: ① 머리끈 = 딥톤 밴드로 해결 ✓ ② 슬픔 강화는 됐으나 **미간·눈이 과하게 어두워져 침울(anguish) 쪽으로 넘어감** — v2의 경계 곁눈이 가진 생기를 잃음. 코튼 콜 = **"v2 표정 그대로 + 눈물만 조금"** (v2 이미지를 직접 첨부하며 지정).
  - **진단**: 표정을 텍스트로 재생성할 때마다 드리프트 (v1 무표정 → v2 적중 → v3 과침울). 코튼이 v2에서 표정을 이미 승인 → from-scratch 반복은 확보한 표정을 도박에 거는 것. **⑨ v3 '자기 출력 refine 보수적' 교훈이 여기선 오히려 유리** — 원하는 게 최소 변경(표정 보존 + 객체 단위 수정 2건)이므로 surgical edit이 옳은 경로.
- **v4 = v2 이미지 attach + surgical edit 2건**: ① 눈물 추가 — 표정 불변 조건 명시(눈썹·눈매·시선·입 NOT redraw) + 촉촉한 아래 눈꺼풀 + 뺨에 막 흘러내리기 시작한 가는 눈물 한 줄기(같은 유화 기법·빛 글린트) ② 머리끈 교체 — v3에서 검증된 딥톤 무광 실크/벨벳 밴드 지정 이식. 나머지 전부 동결 명시. = `cover-prompt-v4.txt` (★ 첨부 = 원작 아님, **v2 결과 이미지**)
- **v4 미실행 — 코튼 경로 정정 (2026-06-11)**: surgical edit(v2 attach) 반려. ★ **코튼 생성 독트린 확립 = AI 출력 위 편집 체인 금지** — "AI 생성을 계속 돌리다 보면 원작 이미지에서 점차 멀어지고, 이미지 열화가 발생" → **항상 원작에서 재생성, 학습 누적은 프롬프트에**. (⑨ v1 거부 때 "원본에서 재생성·1차 아티팩트 미상속" 콜과 일관 = 시리즈 doctrine으로 승격.) v4 프롬프트는 미사용 보존.
- **v5 = 원작 attach + 학습 전부 통합 from-scratch**: v2 표정 블록(승인된 wary 곁눈) 베이스 + 눈물 추가(촉촉한 아래 눈꺼풀·뺨에 가는 한 줄기·유화 글린트) + ★ v3 과침울 재발 방지 = "눈물이 슬픔을 운반하므로 얼굴 나머지는 침착하게" 명시(눈썹 NOT knit/twist·NOT sobbing/anguished/gloomy — "alert and silent, with tears she does not acknowledge") + v3 검증 머리끈(딥톤 밴드+모던 부정) + "NOTHING modern anywhere". = `cover-prompt-v5.txt`
- **v5 결과 (코튼 2026-06-11 · ★ 4축 첫 동시 통과)**: ① 미쿠 식별 ✓ ② 톤앤매너 ✓ ③ 포즈·가운·소품 ✓ ④ 표정 = 경계 곁눈 + 촉촉한 눈(눈물 은은) ✓ + 머리끈 딥톤 밴드 ✓. MOKA 판정 = LOCK 후보.
- **코튼 질문 = "눈을 감는 게 나을까?"** → MOKA 반대 (뜬 눈 유지 추천 · 직접 표명): ① 그림 선정 논리 자체가 '감금된 자가 바깥 빛을 응시'(경계+갈망=알미레나 1:1) — 감으면 서사 단절 ② 눈 = 트윈테일 다음 미쿠 식별자 + 생기 — 감으면 ⑨ 인형(데스마스크) 골짜기 리스크 ③ 썸네일 시선 견인 + 곡 정서가 흐느낌 아닌 조용한 항변 = 눈물+응시 결이 정합. A/B용 감은 눈 변형 생성은 가능(원작 from-scratch라 저비용) → 코튼 콜 대기.
- **코튼 결정 (2026-06-11) = 뜬 눈 유지, v5 확정** ("OK. 그럼 이대로 진행하자").

---

## ★★★ COVER LOCK (2026-06-11) — v5

**최종 커버 = `video/cover/Miku_rossetti_proserpine_1874_gap.png` (1254×1254 · rgb24 · 코튼 저장 · 이미 1:1 정방형 = 별도 크롭 불필요).**
- 베이스 = Dante Gabriel Rossetti *Proserpine* (1874 · Tate N05064 · PD강 · 화가 미중복) · 단독 여성 → Classical Miku · 포즈(석류+손목)·청록 실크 가운·담쟁이·빛 조각·향로·명문 패널 원작 보존 · 경계 곁눈 + 은은한 눈물 · 딥톤 머리끈.
- 화가 중복맵 갱신: Satie/Chopin=Whistler·Vivaldi=Botticelli·Joplin=Glackens·Elgar=Waterhouse·Mozart=VanGogh·Pachelbel=Vermeer·Degas=백조예약·Tchaikovsky사탕요정=Renoir·Boccherini=Longhi·**Handel=Rossetti**.
- description 크레딧 = 'Cover art, after Rossetti, Proserpine (1874).' (release 단).

### 핵심 교훈 (v1~v5 = 5 cycle · 표정 곡)
1. ★ **코튼 생성 독트린 (시리즈 doctrine 승격)** = AI 출력 위 편집 체인 금지(원작 이탈+열화 누적) → 항상 원작 attach from-scratch, **학습은 프롬프트 텍스트에 누적**. (memory: feedback_muse_cover_regen_doctrine)
2. **표정은 텍스트 재생성마다 드리프트** (v1 무표정→v2 적중→v3 과침울) → 승인된 표정의 *텍스트 블록*을 동결하고 새 요소(눈물)는 "표정 불변 + 감정 운반은 새 요소가" 구조로 추가하는 게 안정적 (v5 성공 패턴 = "눈물이 슬픔을 운반하므로 얼굴 나머지는 침착하게").
3. **시그너처 캐릭터의 디폴트 액세서리 주의** = 트윈테일만 지정하면 GPT가 미쿠 모던 클립을 자동 동반 → 시대물에선 묶는 방식까지 명시 (딥톤 무광 밴드 + 부정 명시).
4. 표정 류 결정(뜬 눈 vs 감은 눈)은 **선정 논리로 회귀해서 판정** — Proserpine 선택 이유(감금된 자의 응시)가 곧 답이었음.

## 잔여 파이프 (커버 LOCK 후)
레터박스 색 도출 → 비주얼라이저 (★ B 공유 엔진 첫 신곡 적용 = props.json 신축 + `python muse.py render handel_lascia_chio_pianga`) → QC → 썸네일(make_thumbnail.py · 풀네임 George Frideric Handel) → release description (첫 '원곡 성악' 스토리 hook 후보 · 크레딧 위 줄) → l10n 9언어 → 코튼 업로드+예약.
