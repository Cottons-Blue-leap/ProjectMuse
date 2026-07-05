# Cover Generation Notes — Saint-Saëns: The Swan (Le Cygne · Carnival of the Animals No.13)

> Method: **MOKA writes prompt → 코튼이 GPT image generation** (image-edit · 원작 attach · from-scratch 매 사이클 · 학습은 프롬프트에 누적). 선례 = Handel/Pachelbel/Boccherini cover-gen-notes. doctrine = [[muse-cover-regen-doctrine]].
> 시리즈 = 동물의 사육제 14연작 · 시그니처 = **"미쿠 컬러 동물"**(2026-06-22 개정 · 얼굴 X, 청록 색만). 화가맵 = **Saint-Saëns(백조)→Caspar David Friedrich**.

## 베이스 명화 (LOCKED 2026-06-22)

**Caspar David Friedrich, *Swans in the Reeds* (Schwäne im Schilf), c.1820, oil on canvas 34×44cm, Hermitage (St. Petersburg).** PD강 (d.1840).
- 원본 소스 = `friedrich_swans_in_the_reeds_c1820.jpg` (2292×1743 · Wikimedia Commons `3/3b/Friedrich_schwaene-im-schilf.jpg` · PD-Art) + `source-image-url.txt`.
- ★ **GPT attach용 = `friedrich_swans_in_the_reeds_c1820_clean.jpg` (2250×1703)** — 원본에 스캔/복제 흰 여백(가장자리 순백 255 + 하단 전이 그라데이션)이 있어 크롭 제거. **커버 생성엔 반드시 clean본 첨부**(여백 있으면 GPT가 테두리 보존/반응 우려). 코튼 2회 적발(1차 크롭 후 하단 전이 잔재 → white=min(RGB)>230 감지 + 6px 전이버퍼로 재크롭 · 네 edge white-frac≈0 검증). 교훈 = 명화 크롭 시 순백 margin뿐 아니라 dark content↔white 전이 그라데이션(JPEG)까지 버퍼 트림.

### 원작 구도 (실물 시각 검증 2026-06-22)
- **하늘**: 따뜻한 노을 — 분홍→주황 그라데이션 글로우 (상단). ※컨벤션 doc 旧 '안개/멜랑콜리 회색'은 부정확, 실제는 sunset-glow. 정적·평온 톤은 유지.
- **갈대**: 화면 대부분을 채우는 어둡고 무성한 녹색 갈대 숲 (좌우·상단).
- **백조**: 중앙 하단, **흰 백조 2마리** — 갈대에 안긴 채 목을 서로 마주보게 굽힌 대칭 구도. 좌측 백조 목은 우상향, 우측 백조 목은 좌상향. **화면에서 가장 밝은 초점**(어두운 갈대 대비).
- **전경**: 어두운 수면 + 작은 붉은 갈대 새싹들.

## 설계 결정 (컬러 컨셉 · v1 프롬프트 전)

1. **컨셉 = 두 백조 중 한 마리만 청록 채색** (§1 미쿠 컬러 동물). 흰 짝은 그대로 → 대비로 즉시 식별. teal(청록)↔주황 노을 = **보색 대비 = 썸네일 흡인력 ↑**.
2. **얼굴/이목구비/트윈테일 일절 없음** — 진짜 백조 형태 그대로, **깃털 색만** 미쿠 시그니처 청록. 코튼 지정 = "얼굴 대신 색으로 인식 + 명화에서 눈에 띄는 쪽".
3. **화풍 보존 = 최우선** — Friedrich 유화 글레이즈·노을 광·갈대 톤 그대로. 청록은 채도 명확하되 **유화 질감 안에서 빛나게**(neon/flat/cartoon 금지 · 만화 paste 금지).
4. **어느 백조?** = v1 = **좌측 백조**(목이 우상향하는 쪽) 지정. 코튼이 우측 선호 시 좌→우 1단어 교체로 재생성(원작 from-scratch라 저비용).
5. **곡 정합** = Le Cygne = 솔로 첼로 = 백조 1마리 노래. 청록 미쿠-백조 = '솔로이스트', 흰 백조 = 동반자.
6. **크롭** = 원본 종횡비(4:3 가로)로 생성 → 썸네일/커버 1:1 또는 16:9는 추후 크롭 단계.

## Prompt v1 (image-edit · 원작 Friedrich 1장 attach · GPT 새 세션)

```
Attached is Caspar David Friedrich's "Swans in the Reeds" (c.1820), a Romantic oil painting: two white swans nestle together at the center among tall dark green reeds, their necks curving toward each other, set against a warm pink-and-orange sunset sky, with dark still water and small reddish reed shoots in the foreground.

Edit this painting in ONE way only: recolor the plumage of the LEFT of the two swans (the one whose neck curves up and to the right) so its feathers are Hatsune Miku's signature teal / turquoise color. Leave the RIGHT swan exactly as it is — natural white. Change NOTHING else in the entire painting.

The single hardest requirement: the recolored swan must still look like a real swan that Friedrich painted in oil — same body, same pose, same soft painterly feathers and the same warm sunset light falling on it — only its color is now teal instead of white. It is an oil-painted teal swan, NEVER a cartoon, NEVER a flat or neon shape pasted on top. No Hatsune Miku face, no eyes, no twin-tails, no human or anime features of any kind — it stays a swan. Miku is recognizable here purely through her iconic teal color.

Make the teal clear and saturated enough that a viewer instantly reads it as Hatsune Miku's color and the swan stands out boldly against its white companion and the dark reeds — but render it with Friedrich's soft oil glazing, letting the warm sunset glow play across the teal feathers (cooler in shadow, warmer where the light hits). Distinct, but painterly and luminous, never garish.

Keep everything else exactly as Friedrich painted it: the right white swan, the dark reeds, the pink-orange sunset sky, the still water, the reed shoots, the whole composition, the oil technique and tonality. Keep the original aspect ratio. Add no new text, border, or signature.
```

> ⏳ v1 후 4축 체크 = ① **미쿠 색 인식**(teal 명확·미쿠 색으로 즉독·흰 짝/갈대 대비 pop) ② **원작 톤앤매너 보존**(Friedrich 유화·노을·갈대 그대로) ③ **한 마리만 채색**(우측 백조 흰색 유지·형태/포즈/구도 불변) ④ **만화/네온 회피**(유화 질감·sunset 광 통합).
> 실패 모드별 다이얼: 색 약함/탁함 = teal 채도·명료 당김 / 네온·플랫 = "Friedrich oil glaze + sunset light 통합" 강조 / 백조 형태 왜곡 = "ONLY recolor, do NOT change shape or pose" 강조 / 양쪽 다 칠해짐 = "the RIGHT swan stays natural white" 강조 / 얼굴·트윈테일 새어나옴 = "NO face/eyes/twin-tails, it stays a swan" 강조.

## Iteration log (코튼 generation 시점)
- **v1 결과 (코튼 2026-06-22 · ★ 첫 시도 4축 동시 통과 → LOCK)**: ① 미쿠 색 인식 ✓✓(청록 선명·luminous·즉독·흰 짝+갈대 대비·teal↔주황 보색 작동) ② 원작 톤앤매너 ✓(Friedrich 낭만 유화·노을·갈대·물+붉은 새싹 보존·somber) ③ 한 마리만 채색 ✓(좌 teal/우 흰색 분리) ④ 만화/네온 회피 ✓(유화 글레이즈·빛 통합·얼굴/트윈테일 누출 0·진짜 백조 유지). 참고 = GPT가 갈대 좀 더 빽빽 재해석 + 1:1 reframe(1254² = Handel 커버 동일 규격 = 우리 표준이라 OK · 픽셀복제 아닌 'after Friedrich' 재해석 = 크레딧 정합). 코튼 콜 = "이대로 Lock 가자".

## ★★★ COVER LOCK (2026-06-22) — v1
**최종 커버 = `video/cover/Miku_friedrich_swans_in_the_reeds_c1820_clean.png` (1254×1254 · RGB · 코튼 GPT 생성·저장 · 이미 1:1 정방형).**
- 베이스 = Caspar David Friedrich *Swans in the Reeds* (c.1820 · Hermitage · PD강 d.1840 · 화가 미중복). 두 백조 중 **좌측 백조 → 미쿠 청록 채색**, 우측 흰 백조·갈대·노을·물·붉은 새싹·유화 화법 보존. 얼굴/트윈테일 없음 = §1 미쿠 컬러 동물 시그니처.
- 화가맵 갱신: …Boccherini=Longhi·Handel=Rossetti·**Saint-Saëns(백조)=Caspar David Friedrich**.
- description 크레딧(release 단) = 'Cover art, after Caspar David Friedrich, Swans in the Reeds (c.1820).'
- ★ 시리즈 의의 = 사육제 14연작 **앵커 + 컬러 시그니처('미쿠 컬러 동물') 첫 구현**. 첫 시도 통과 = 색-컨셉이 grafting보다 안정적이라는 가설 1차 입증.

### 핵심 교훈
1. **색-시그니처 = 1-shot 안정성** — 얼굴 grafting(Handel 5 cycle·Boccherini 7 cycle)과 달리 색 채색만은 표정 드리프트 없이 첫 판 통과. 14연작 균일성 가설 뒷받침.
2. **base 크롭 = 전이 그라데이션까지** — 순백 margin뿐 아니라 dark↔white JPEG 전이를 white=min(RGB)>230 + 버퍼로 제거(코튼 2회 적발).

## 잔여 파이프 (커버 LOCK 후)
레터박스 색 도출(teal/노을 팔레트) → 비주얼라이저 (B 공유 엔진 · props.json + `python muse.py render saint_saens_the_swan`) → QC → 썸네일 → release description(작곡가 성만 Saint-Saëns · 사육제 시리즈 앵커 hook 후보) → l10n 로케일 → 코튼 업로드+예약. ※기악곡 = CC 자막 불필요.
