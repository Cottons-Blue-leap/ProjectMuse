# Cover Generation Notes — ⑫ Mozart: Der Hölle Rache (Queen of the Night aria, Die Zauberflöte K.620, 1791)

> Method: **MOKA writes prompt → 코튼이 GPT image generation** (image-edit). NOT local ComfyUI.
> [[muse-cover-regen-doctrine]] = 원작 1장 attach + 학습 누적 프롬프트로 **from-scratch 재생성**. AI 출력 편집 체인 금지.
> 화가맵 = **Mozart(밤의여왕)→Schinkel**. Mozart 작곡가는 ⑤ Van Gogh 기등재이나 화가 Schinkel unique.

## ★ 베이스 명화 — FINAL LOCK = Schinkel 〈Hall of Stars〉 (2026-06-18 코튼)

**Karl Friedrich Schinkel, 〈Die Sternenhalle der Königin der Nacht / The Hall of Stars in the Palace of the Queen of the Night〉 (c.1815)** · gouache 무대 디자인 · Mozart 《마술피리》 1막 6장 무대 · Berlin Kupferstichkabinett. PD강 (Schinkel d.1841). 소스 = `schinkel_hall_of_stars_1815_gap.jpg` (8033×5955) + `source-image-url.txt`.

### 베이스 선정 경위 (06-18 다단계 pivot · 상세 = source-image-url.txt + cover-candidate-eval.md)
- 06-15 패널 = Collier 〈Clytemnestra〉. → 06-18 코튼 재검토(오페라 스틸).
- 06-18 위엄 방향 = Reynolds 〈Tragic Muse〉 → v1 생성(식별·톤 우수, 청록과채도는 MOKA 결정론적 색보정으로 해결) → 단 코튼 **컨셉 반려**('Tragic Muse=비극 일반이지 *밤*이 아님').
- 06-18 '밤' 탐색 = Arbo 〈Nótt 밤의여신〉(드라마틱 best)·Hughes 〈Train of Stars〉(gentle 부적)·Bouguereau·Blake 제시.
- ★ 코튼 제안 = **Schinkel 〈Sternenhalle〉** = '밤 일반'이 아니라 *바로 이 오페라·이 캐릭터*의 1815 무대 디자인 = 곡 직속. → FINAL.

### Schinkel 선정 논리 + ★ 핵심 컨벤션 일탈
- ★ **가장 literal** = 다른 후보 전부 '밤 일반' 알레고리인데 이건 《마술피리》 밤의 여왕 궁전 그 자체. + '어두컴컴한 밤'(깊은 블루 별 돔) 끝판 + 곡·레터박스·비주얼라이저 색 완벽 연동.
- ⚠️ **컨벤션 의식적 일탈** = 이건 **무대 세트 디자인**이라 인물(여왕)이 초승달 위 **아주 작은 실루엣**. 시리즈 표준(명화 단독 인물 → hero 얼굴 미쿠 치환)과 다름.
- ★ **코튼 결정 (2026-06-18) = "실루엣만 있어도 좋아. 크기는 원본 그대로. 톤앤매너 맞춰 미쿠를 그리면 특색있는 커버"** → hero 확대 합성 NOT 채택. **원본 스케일·실루엣 유지** + 작은 인물만 미쿠로 치환. hero = 별의 돔 자체, 미쿠 = 초승달 위 작은 청록 트윈테일 실루엣(식별자).
- ⚠️ 썸네일 = 얼굴 0 (CTR 독트린상 [[reference_muse_ctr_impression_floor]] 우려 MOKA 1회 제기 → 코튼 의식적 실루엣 선택). 썸네일 단계서 별도 처리(타이틀 배지·약크롭) 검토 keep.

### 원작 구도 (viewing 검증 2026-06-18)
- **거대 블루 돔 밤하늘** = 동심원 호로 퍼지는 작은 흰 별 수백 개(방사형 아치) · 깊은 코발트/미드나잇 블루 gouache.
- **하단 중앙** = 흰 **초승달** 위에 **작고 어두운 여왕 실루엣** 1인 서 있음 · 인물에서 위로 가는 희미한 수직선.
- **하단 띠** = 따뜻한 갈색 구름 층.
- 종횡비 ≈ 1.35:1 (landscape). gouache 특유 matte·약간 거친 질감.

## 설계 결정 (v1 프롬프트)
1. **편집 범위 = 초승달 위 작은 인물만** 미쿠 실루엣으로. 별 돔·초승달·구름·블루 톤 전부 동결.
2. **스케일 동결** = 확대 X·클로즈업 X·디테일 초상 X. 원본 실루엣 크기·단순함 유지(코튼 명시).
3. **미쿠 식별 = 실루엣 only** → **트윈테일 2갈래**(머리에서 흘러내리는 두 갈래 = 실루엣으로도 읽히는 핵심 식별자) + 가녀린 소녀 체형 + 당당·위엄 포즈(밤의 여왕 = 팔 살짝 벌림/올림 가능) + (옵션) 작은 뾰족 왕관.
4. **화풍 동결** = Schinkel 본인 matte gouache·원작 인물과 동일 딥 블루-블랙 실루엣. 모던 요소 0(1815 정합).
5. **크롭 = 추후** = 1:1 앨범 = 중앙 돔+초승달+미쿠 / 16:9 = 원본 landscape + 레터박스. (별 다 보존 → 크롭 여유.)

## Prompt v1 (image-edit · 원작 Schinkel 1장 attach · GPT 새 세션)

```
Attached is Karl Friedrich Schinkel's "The Hall of Stars in the Palace of the Queen of the Night" (c.1815), the iconic gouache stage design for Mozart's Magic Flute: a vast deep-blue domed night sky filled with hundreds of small white stars arranged in concentric radiating arcs, and at the bottom center a tiny dark figure of the Queen of the Night stands on a white crescent moon, above a band of warm brown clouds.

Edit this image so ONLY the small figure standing on the crescent moon becomes Hatsune Miku — while keeping EVERYTHING else exactly as Schinkel painted it: the entire blue star dome, every arc of stars, the crescent moon, the clouds, the deep-blue gouache tone, the whole composition and palette, completely unchanged.

Keep the figure at the SAME small scale and the SAME simple silhouette treatment as the original — she remains a small, dark silhouette standing on the crescent moon, NOT enlarged, NOT a close-up, NOT detailed portraiture. Paint her in Schinkel's own matte gouache manner, the same deep blue-black as the original figure, reading as a silhouette against the starry sky.

Yet make her unmistakably Hatsune Miku through her silhouette alone: two long twin-tails of hair streaming down from her head — her single most recognizable trait, readable even as a dark silhouette — a slender, girlish figure, standing tall and regal as the Queen of the Night, with her arms slightly raised or spread in a commanding gesture. Optionally a small pointed crown. Nothing modern; she belongs entirely in this 1815 gouache.

Do not add any text or border. Keep the original aspect ratio, tone, and every star exactly in place.
```

> ⏳ v1 후 체크 = ① 미쿠 실루엣 식별(트윈테일 2갈래 읽힘) ② Schinkel gouache 톤·별 돔·초승달·구름 100% 보존 ③ 인물 원본 스케일·실루엣 유지(확대/디테일화 아님) ④ 딥블루-블랙 실루엣·모던 0 ⑤ 별 위치 불변.
> 실패 모드별 다이얼: 인물 너무 커짐/디테일화 = "same small scale·silhouette only" 강조 / 트윈테일 안 읽힘 = 두 갈래 streaming 강조·포즈 단순화 / 별 돔 변형 = "every star exactly in place·only the figure" 강조 / 미쿠 너무 모던 = 1815 gouache 고정.

## ★★★ COVER LOCK (2026-06-18) — v3 재구성 (AS-IS)

**최종 커버 = `video/cover/schinkel_hall_of_stars_1815.png` (1254×1254 · RGB · 코튼 저장 · 이미 1:1 = 별도 크롭 불필요).** visualizer용 `video/visualizer/public/cover.png` 복사 완료.
- 베이스 모티브 = Schinkel 〈Hall of Stars〉(c.1815 · 곡 직속 무대) **자유 재구성**(strict-edit 아님) · 화가맵 **Mozart(밤의여왕)=Schinkel**.
- 구성 = 깊은 미드나잇 블루 별 돔(동심원 금빛 별 아치) + 하단 따뜻한 구름 + 빛나는 초승달 위 **미쿠 = 밤의 여왕** 청록 실루엣(트윈테일 2갈래 높이 묶음 · 작은 뾰족 왕관 · 팔 벌린 위엄 포즈 · 보석 가운). 인물 prominent+돔에 dwarf = 식별+awe 동시.
- 변형 = AS-IS(코튼 선택 · 절제·고전적) · MOKA가 결정론적 teal-halo boost 대안 제시했으나 코튼 AS-IS 확정.
- description 크레딧 = (release 단) 'Cover art, after Schinkel, The Hall of Stars in the Palace of the Queen of the Night (c.1815).' 류.

### 핵심 교훈 (커버 6 cycle = 베이스 4 pivot + 접근 1 pivot · 시리즈 최장 탐색)
1. ★ **베이스 선정 = 곡 정체성 직격이 최강** — 알레고리(Collier 복수/Reynolds 비극/Arbo 밤)보다 *바로 그 오페라의 무대*(Schinkel)가 컨셉 승. 코튼이 후보 viewing 반복 끝에 도달.
2. ★ **strict 보존이 식별의 벽이 될 수 있음** — 무대세트 작은 실루엣을 픽셀보존하면 GPT가 generic-queen으로 수렴(트윈테일 누락). 코튼 콜 = "원본 모티브로만 삼아 재구성" → 보존 강박 해제하니 트윈테일+분위기 동시 확보. **교훈 = 베이스가 figure-portrait가 아닌 scene/set일 땐 strict-edit보다 motif 재구성이 식별에 유리.**
3. **실루엣 식별 = 트윈테일 단일 레버** — 작은 실루엣에선 트윈테일 2갈래가 식별 전부. 여러 식별자 나열 X, "THE ONE CRITICAL REQUIREMENT"로 단독 강조해야 GPT가 안 빠뜨림.
4. ★ **결정론적 색보정 = doctrine-safe 보조 도구** — AI 재생성(편집체인 드리프트) 없이 hue 대역 채도조정(머리색)·radial teal glow(halo)·crescent tint를 승인 이미지 위에 정밀 적용. 마스터링이 오디오 후처리이듯 이미지 색보정도 후처리 = 재생성 독트린과 별개. (향후 재사용)

## Iteration log (코튼 generation 시점)
- **Schinkel v1 결과 (코튼 2026-06-18 · 식별 약·무드 good)**: ★ 무드 excellent — 별 돔/별 호/구름/딥블루 gouache 톤 100% 보존 + GPT가 자동 **1:1(1254²)로 recompose**(앨범 커버 정합 = 보너스) + 초승달 위 작은 인물 유지. **BUT 미쿠 식별 실패** — 인물 확대 검증(sch_fig) 결과 실루엣이 **왕관 + 긴 가운 + 팔 벌린 자세 = 일반적 '밤의 여왕'**으로 읽힘. ★ **트윈테일 부재** = 미쿠 유일 실루엣 식별자가 안 들어감 → 'Miku' 아닌 'generic night-queen'. 코튼 콜 = "식별력은 잘 모르겠지만 분위기는 있어"(정확 진단).
  - **진단**: v1 프롬프트가 트윈테일을 여러 식별자 중 하나로 나열 → GPT가 crown+gown 실루엣으로 수렴, 트윈테일 누락. 무대세트 작은 실루엣에선 트윈테일 하나에 식별 전부 걸림.
  - **v2 단일 레버 = 트윈테일 실루엣 강제**: 크기·돔·톤·당당한 포즈 동결 + "THE ONE CRITICAL REQUIREMENT" = 두 갈래 긴 트윈테일이 어깨 아래까지 흘러내리는 **분리된 2 tail** 명시 + 부정(single veil/cloak/gown-merge NOT) + "twin-tails must read first·dominate, crown은 작게 OK". 나머지 v1 성공축(무드·돔·1:1) 전부 keep. = (v2 미실행)
- **★ 접근 PIVOT (코튼 2026-06-18) = strict-edit → 자유 재구성**: 코튼 인사이트 = "원본에 대한 너무 빡빡한 톤앤매너 유지가 되려 (미쿠 식별의) 벽이 됐다" → **Schinkel을 모티브로만 삼아 재구성**(별 보존 강박 해제). + 청록 색 정체성 아이디어(halo/초승달) 통합. MOKA가 청록 halo/crescent를 **결정론적 색보정으로 3 variant(A halo·B crescent·C both) 선실증** → 예쁘고 톤 보존(원본 그림 무변) 확인, 단 색만으론 실루엣이 여전히 '일반 여왕' → 트윈테일 shape 필요 재확인.
- **v3 = 재구성 프롬프트 (text-to-image, Schinkel 모티브)**: 1:1 · 별 돔/초승달/구름 + 깊은 블루 gouache 무드 keep · ★ 트윈테일 2갈래 실루엣 최우선(식별) · 청록 halo+실루엣 엣지+초승달 tint(미쿠 색 정체성·코튼 아이디어 baked-in) · 회화적(아니메/사진 X·시리즈 classical 정합) · 인물은 읽힐 만큼 prominent하되 돔에 dwarf(awe). = (코튼 generation 대기)
- ★ **재사용 자산 = 결정론적 청록 색보정 스크립트**(radial teal glow screen-blend + 밝은 crescent 픽셀 teal tint · /tmp 세션) — 최종 figure 확정 후 미세 색 입힘에 재사용 가능.
- [history] Reynolds Tragic Muse v1 = 식별·톤 우수했으나 컨셉('밤' 아님) 반려 (06-18). 결정론적 hair 색보정(MILD/MEDIUM/STRONG) 기법은 보존 가치 = AI 안 거치고 청록 hue 대역만 채도↓로 승인본 보존하며 머리색만 조정(향후 재사용).
