# Cover Generation Notes — Tchaikovsky: Dance of the Sugar Plum Fairy

> Method: **MOKA writes prompt → 코튼이 GPT image generation** (image-edit). NOT local ComfyUI. 선례 = Pachelbel/Chopin cover-gen-notes.

## ★★ LOCKED (2026-06-06) — Renoir *The Dancer* 발레 path

**최종 커버 = `video/cover/Miku_renoir_the_dancer.png` (1:1)** · 코튼 시각 게이트 통과("나쁘지 않다, 이대로 가자").

- **베이스 명화 = Pierre-Auguste Renoir, *The Dancer* (1874, NGA Open Access, PD강)** = `renoir_the_dancer_1874_nga.jpg` (3840×5812). rights/url = source-rights-notes.md / source-image-url.txt.
- **방식 = (가) 명화 보존 image-edit** — 원작 구도·인상주의 화풍·발레리나·손 모티프 보존 + 얼굴/머리/복식만 Classical Miku + 톤 은청 + sparkle. "명화의 일부" doctrine.
- **이 컨벤션 = 발레 sub-family (B)의 첫 원형** → `planning/ballet_subfamily_convention.md` 단일 source.

### cycle history (2026-06-06)
1. **명화 탐색** (코튼 직접 방향 전환) = 요정(Anderson/Blake) → 사탕 정물(Flegel/Beert/van der Hamen — 코튼 "별로") → **발레**. Degas(백조 예약) 제외 → Renoir *The Dancer* 픽 (단독 발레리나·미쿠변환 최적·NGA 고해상·PD 최저리스크).
2. **자세 논의** = 코튼 전략 = "The Dancer 베이스 + 곡별 포즈"로 발레곡 대비. MOKA 판단 → **(B) 컨벤션만 통일** 채택. 사탕요정 포즈 = 안1(sur les pointes + port de bras) 선택.
3. **1차 생성 (실패)** = 프롬프트가 "NEW ballerina" + 안1 큰 포즈변경 → GPT from-scratch = **Renoir 원작 0% "완전 새 그림"** (코튼 거부). → **핵심 발견: '명화 보존' ↔ '포즈 변경'은 image-edit에서 충돌.** (B) 실행법 수정 = 포즈를 합성으로 바꾸지 말고 *곡 무드에 맞는 포즈의 원작을 고른다*. 포즈는 원작(정면 발레리나) 존중.
4. **2차 (가) image-edit (성공)** = 원작 보존 + 미쿠 + 은청 톤. 명화 느낌 살아남. 단 표정 굳음.
5. **표정 수정 1차 (실패)** = 얼굴 서양인화 + 포즈·비율까지 변형(GPT 과잉). → 직전 본으로 복귀.
6. **최종** = 표정 미세 완화 + 미쿠 얼굴 + 1:1 = LOCK.

### LOCK 프롬프트 (image-edit · The Dancer attach)
```
Edit this painting — Renoir's "The Dancer" (1874). Keep the canvas almost entirely intact: soft Impressionist brushwork, the exact pose and composition of the standing ballerina, her tutu, stage setting, painterly surface. Do NOT repaint as a new picture — preserve Renoir's original and ONLY transform the figure into Hatsune Miku:
- Face: same head position/angle, but her face as Hatsune Miku — youthful, serene, gently melancholic young East-Asian girl, in Renoir's soft brushwork. (Do NOT Westernize — round youthful Miku face, large gentle eyes.)
- Hair: long teal-cyan twin-tails (Miku's signature), within Renoir's palette, never neon.
- Costume: same tutu/pose, shift color to muted cool silver-blue / pale teal / ivory.
- Tone: cool the palette toward silver-blue moonlight; add faint crystalline blue-white sparkles around her, like a celesta — subtle, painterly, not glossy.
Keep everything else — pose, composition, brushwork, background — as Renoir painted it. No text, no border. Keep original aspect (crop to square later).
```
> 표정 미세조정 = 별 세션(결과물 attach + "Change ONLY her facial expression · subtle · do NOT re-pose/crop · round East-Asian Miku face").

### 잔여 파이프 (커버 LOCK 후)
1:1 crop(album_1x1) → 레터박스 → signature wordmark v3 → render → QC → 썸네일(make_thumbnail.py · Pyotr Ilyich Tchaikovsky) → 비주얼라이저(band-remap·은청 톤 동기) → **영상 outro before-after 디졸브**(원작 The Dancer 1:1 ↔ 미쿠 커버 · 코튼 b방향 · 사탕요정 시범 → 좋으면 라이브 소급) → 영상 패키지 → l10n 9언어 → 예약 발행(에버그린·코튼 a).

---
# (이하 폐기 path 기록 — 보존)

## ⛔ 호두까기 컨셉 = 보류 (코튼 2026-06-06 · 세션 클리어 시점)
> 코튼 최종 = "호두까기 미쿠는 **브랜딩에 안 좋다**(family PD명화+Classical Miku 일관성 이탈) → 적합
> 명화 더 찾자 · 다음 세션 같이". → 아래 호두까기 프롬프트(가/나)는 **미실행 보류**(코튼 생성 전 철회).
> ★ 다음 세션 = 명화 재선정. 무드 나침반 = '움직임/춤/생동' 결(평화/정적/차가운신비 거부) + PD명화+
> Classical Miku 합성 유지. 후보 미탐색 방향 = 발레(Degas 예약 제외)·요정 군무(Blake/Paton)·화려한
> 극적 마법·축제. status.json cover_art = 단일 source.

## ★ PIVOT (코튼 2026-06-06) — 명화 합성 → 호두까기 미쿠 오리지널 컨셉 [보류됨 ↑]
> 명화 path 폐기 history: Hughes *Midsummer Eve* (v1 미쿠化 성공 BUT "너무 평화로움" + 썸네일 요정
> 잘림 CTR 우려 + 톤A 재채색 실패) → Vasnetsov *Snow Maiden*/Dadd/Grimshaw (전부 "곡과 안 어울림")
> → MOKA 무드 오독(차가운 신비) 자인 + 무드 정렬 질문 → **코튼 결단 = 호두까기 인형이 된 미쿠**
> (명화 합성 컨벤션 이탈 · text-to-image 오리지널 컨셉).
> 사유 = 곡 직결성(호두까기 모음곡 주인공 그 자체) > 명화 / 미쿠 정체성 / 썸네일 CTR / 저작권 단순
> (호두까기 = PD 모티프 · 명화 의존 X) / 무드 갈등 우회. **trade = family 7곡 "PD명화+Classical
> Miku" 브랜드 일관성 이탈 → 절충 = 화풍은 클래식 유화/수채 회화 톤 유지(anime 톤 X)로 시리즈 정합.**
> 방향 = **(가) 늠름한 병정 + (나) 춤추는 사탕요정 둘 다 생성**(코튼) → 비교 후 택1/refine.
> 프롬프트(text-to-image · 명화 첨부 無) = 아래 "Nutcracker Miku Prompt 가/나". 명화 기반 섹션
> (Inputs/Compositing/v1/v2)은 폐기된 Hughes path 기록으로 보존(아래).

## Nutcracker Miku Prompt — (가) 늠름한 병정
```
A classical oil painting portrait of Hatsune Miku reimagined as the Nutcracker soldier from
Tchaikovsky's "The Nutcracker." She stands tall and upright in a richly detailed toy-soldier's
uniform — a bright red military coat with gold braid, brass buttons, epaulettes, and a tall black
soldier's hat. Her long teal-cyan twin-tails fall from beneath the hat. Her pose is stiff, poised
and precise like a toy soldier at attention — an alert, faintly tense stillness, as if about to
spring into motion. Her young face is serene yet focused, gently melancholic. Painted entirely in
a soft classical oil-painting technique — smooth blended brushwork, rich warm painterly palette,
gentle theatrical lighting — like a museum-quality 19th-century painting, NOT a modern anime
illustration: no cel shading, no anime gloss, no sharp outlines, no neon. A single classical
painted portrait. Dark, softly atmospheric background with a faint magical warmth. No text, no
border. Portrait composition, the figure from about the waist up, her face clearly visible.
```

## Nutcracker Miku Prompt — (나) 춤추는 사탕요정
```
A classical oil painting of Hatsune Miku reimagined as the Sugar Plum Fairy dancing, from
Tchaikovsky's "The Nutcracker." She is captured mid-dance in a graceful ballet pose — light and
poised on pointe, arms extended in an elegant precise movement, her body alive with delicate
sparkling motion. She wears a refined classical ballet costume with subtle fairy touches (a soft
tutu in muted teal and ivory with hints of gold), and her long teal-cyan twin-tails sweep with
the motion. Her young face is serene and focused, gently melancholic, absorbed in the dance.
Around her, faint crystalline sparkles shimmer in the air like the chime of a celesta. Painted
entirely in a soft classical oil-painting technique — smooth blended brushwork, rich painterly
palette, gentle theatrical stage lighting — like a museum-quality 19th-century painting, NOT a
modern anime illustration: no cel shading, no anime gloss, no sharp outlines, no neon. A single
classical painted scene. Dark, softly atmospheric stage background with a faint magical glow. No
text, no border. Portrait composition, the full graceful figure visible, her face clear.
```

> ⏳ 결과 후 = 곡매칭 + 썸네일 가독성 + 미쿠 인식도로 택1/refine → album_1x1 LOCK → 레터박스 →
> 썸네일 → 비주얼라이저 → 영상. ⚠️ 호두까기 = PD 모티프라 명화 rights/화가중복 점검 不要(source-
> rights-notes.md의 Hughes 항목은 폐기 path 기록 · 신 커버는 오리지널 생성물).

---
# (이하 폐기된 Hughes 명화 path 기록 — 보존)

## Inputs
- **Reference painting**: `hughes_midsummer_eve_1908_commons.jpg` (Wikimedia Commons, PD-Art —
  source-rights-notes.md 참조). 533×800. edit reference로 attach.
  - ⚠️ 해상도 우려 해소: GPT가 **from-scratch 재생성**하므로 소스 533×800은 *구도 인식*에만 쓰임 →
    출력 해상도는 GPT 생성본이 결정(family 1254px 발행 선례 = 2K 프레임 내 ~960px 표시로 충분).
    즉 (a) 경로가 개인소장 저해상 문제를 우회. 유료 고해상 스캔 불필요.
- **Character anchor** (`planning/classical_miku_anchor.md`): teal-cyan twin-tails · simple
  late-19th-century European dress in muted tones (blue-gray, dark teal, ivory) · quiet
  melancholic expression.

## Compositing approach (Sugar Plum Fairy 고유)
- **원작**: 달빛 숲에서 젊은 여인이 **빛을 든 작은 요정 무리**(will-o'-wisp 광원)에 둘러싸여 그들을
  바라봄. 푸른빛 도는 어두운 숲 · 마법적 글로우.
- **중앙 여인 → Classical Miku** (Pachelbel식 = 여인이 *곧 미쿠가 됨* · clear painterly 주체 ·
  faint-veil 아님 · 그녀가 화면의 주인공).
- **★ 관계훅 = 빛나는 요정 무리 (절대 보존)**: 이 글로우 요정들 = 첼레스타 영롱함 + 제목의 "Sugar
  Plum **Fairy**" 그 자체. Pachelbel의 viola-da-gamba(ground bass)에 대응하는 이 곡의 정체성 훅 →
  **요정·광원·달빛 숲 전부 그대로.** (커버가 아카펠라로 깎인 고역 반짝임을 시각으로 보강하는 선정논리.)
- **변경 = 중앙 여인만**: 얼굴(미쿠 youthful 동아시아 serene) + 머리(teal twin-tails · Hughes 수채
  톤다운 · neon 금지) + 드레스(anchor muted late-19c · 원작 창백한 가운 → muted dark teal/blue-gray).
- **Light**: Hughes의 달빛 황혼 + 요정 광원의 푸른 글로우 유지.
- **기법**: Hughes 수채+과슈의 부드럽고 환상적인 표면 (oil 아님 · 수채 luminous wash) · no cel
  shading · no anime gloss · no sharp outline.
- **Aspect**: 원본 portrait(세로 ~0.67). 16:9 프레임 소스는 portrait 비율 keep · 1:1 앨범 crop =
  **미쿠 + 그녀를 둘러싼 빛나는 요정 링** 담기게.

## ⚠️ 코튼 결단 자리 (generation 진입 시)
1. **포즈** — family 컨벤션은 **노래 자세**(두 손 가슴에 모음 · 눈 감고 inward singing · 아카펠라
   정합). BUT 이 곡 원작의 혼은 *요정을 바라보는 경이*임. → **절충 default 채택**: 미쿠가 요정들
   가운데 서서 **고요히 노래하되**(입술 살짝 벌림), 시선은 빛나는 요정들을 부드럽게 응시(경이+평온).
   양쪽(아카펠라 노래 cue + 원작 narrative) 다 살림. **strict 눈감은 inward singing 원하면 코튼 조정.**
   → **LOCK = A 절충안** (코튼 2026-06-06). v1 프롬프트가 곧 A이므로 그대로 사용.
2. **Miku presence 강도** — default A(clear painterly 여인=미쿠 · 그녀가 주체). 본 명화는 중앙
   여인이 핵심이라 clear 권고 (faint-veil은 부적합).
3. **드레스 시대 불일치 OK** (family LOCK 정합) — 1908 수채 숲에 late-19c muted 드레스 = 시리즈
   복식 일관성 우선. 원작 창백 가운 → anchor muted dark teal/blue-gray로.

## Prompt v1 (English · GPT image-edit, Hughes reference attached · 통합 from-scratch)

```
Edit this painting — Edward Robert Hughes's "Midsummer Eve" (c.1908), a luminous watercolour
of a young woman standing in a moonlit woodland glade, encircled by a ring of small glowing
fairies holding aloft little lights. Preserve the painting's surface and magic completely: its
soft, luminous watercolour-and-gouache washes, its dusky blue-green moonlit palette, the
enchanted glow radiating from the fairies' lights, and the still, wondering mood. Keep EVERY
magical element exactly as it is — the ring of small winged fairies and their glowing lights,
the dark woodland and foliage, the moonlit dusk, the soft bluish atmosphere. These glowing
fairies are the heart of the image; do not alter, remove, or dim them.

Reimagine ONLY the standing young woman as Hatsune Miku — painted entirely in Hughes's own soft,
luminous watercolour technique so she belongs completely in the scene (no sharp outlines, no cel
shading, no anime gloss, never neon or bright):

- Pose: she stands among the glowing fairies, softly singing — her lips just barely parted as if
  sustaining a quiet, gentle note, her face serene and enchanted as her gaze rests tenderly on
  the ring of fairy lights around her. Her hands are gently gathered near her, calm and graceful.
  Standing in the same place and scale as the original woman; a quiet, inward, wonder-filled
  singing presence, not theatrical.
- Face: the youthful face of Hatsune Miku — a soft, serene, gently melancholic young East-Asian
  girl, recognizably Miku, not a mature Western-European woman. Painterly, as if Hughes painted her.
- Hair: long teal-cyan twin-tails gathered into two distinct soft tails (Miku's signature),
  rendered as a cool teal accent within the painting's moonlit palette, luminous and atmospheric,
  never neon.
- Dress: a simple, plain late-19th-century European dress in muted tones (muted dark teal,
  blue-gray, ivory), high-necked and understated — painted in the same soft watercolour washes so
  it sits naturally in the moonlight. (A late-19th-c dress is Miku's consistent series costume.)

A single Hughes-style watercolour, soft, luminous and atmospheric, an enchanted moonlit fairy
glade. No text, no border, no frame. Keep the portrait aspect ratio of the reference.
```

## Iteration log (코튼 generation 시점 박음)
- **v1 결과 (코튼 2026-06-06 · `_cover_v1_raw.png` 1254×1254 보존)**: Miku化 성공 — teal 트윈테일 또렷
  · 동아시아 youthful serene 얼굴 · muted dark-teal/ivory 드레스 · Hughes 수채 톤 완벽 융합 · 발치
  요정 글로우 풍성 · 달빛 숲 보존. **BUT 구도 문제(코튼 적발 + MOKA 시뮬 검증)**: 미쿠 얼굴=상단,
  요정 글로우=하단 1/3 = **수직 분리** → 얼굴중심 썸네일 crop 시 요정 0개(`_thumb_sim_facecrop.png`
  증거) = 영롱함 보강 논리 무력화 + CTR 우려. 부차 = 눈 감겨 나옴(A 의도=요정 응시와 어긋남).
- **진단**: 자세 변경 필요 — 단순 변경 X, **"요정을 얼굴 높이로 끌어올리는 인터랙션"**. 미쿠가 빛나는
  요정 하나를 두 손으로 가슴~얼굴 높이에 받쳐 들고 눈 떠서 응시하며 노래 → ① 글로우가 얼굴 옆 →
  썸네일 crop에 반짝임 동반 ② 든 빛이 얼굴 비춤 = 어두운 배경 발광 포커스 = CTR↑ ③ 마법적 순간 +
  A 의도 완성. 발치 요정 무리는 keep. → **v2 prompt 발행(아래)**.

## Prompt v2 (pose + COLD TONE 통합 · 코튼 2026-06-06 · refine on v1 image attach)
> 코튼 미학 적발 = 사탕요정의 춤 = e단조 staccato 점묘 = **긴장된 신비**(tiptoe suspense · 첼레스타
> 차가운 유리종/서리)인데 Midsummer Eve는 **평온한 경이** = 톤 갭. 단 정반대 아닌 "같은 밤요정 우주
> 안 톤차이" → 명화 유지 + 연출(색온도·표정)로 좁힘 = **(A) 채택**(코튼). (B 명화재선정은 A 실패 시).
> 통합 변경 = ① 자세(요정빛 얼굴높이 받쳐듦 = 썸네일 CTR) + ② 표정(숨죽인 긴장) + ③ 톤(따뜻amber →
> 차가운 은청 달빛·청백 sparkle·콘트라스트↑). refine on v1 image. (안 먹으면 clean 원본 from-scratch.)

```
Keep this painting's figure and composition — the same Hatsune Miku with her teal-cyan twin-tails,
her young face, her simple muted dark dress, standing in the same place and scale in the moonlit
woodland glade, with the ring of small glowing fairies around her. Keep Hughes's soft luminous
watercolour technique. But shift the whole mood from peaceful warmth to a colder, tenser, more
mysterious enchantment.

Make these changes:

1) Pose, hands, eyes — she now gently lifts both hands to cradle one small glowing fairy-light
close to her, held at her chest just below her face. Her eyes are open, gazing down intently at
the little glowing light cupped in her hands, her lips just barely parted as if softly singing to
it. The light casts a glow upward onto her face and hands against the dark woodland.

2) Expression — not a peaceful smile but a quiet, intent, gently melancholic look, hushed and a
little spellbound, as if holding her breath. Serene yet tense.

3) Tone & light — shift the palette from warm amber moonlight to colder silver-blue moonlight.
Render the fairy-lights as cool blue-white sparkles, crystalline like frost or glass, not warm
amber. Deepen the shadows and raise the contrast so the scene feels mysterious and suspenseful —
a cold, glittering, enchanted night with an edge.

Still Hughes's smooth luminous watercolour washes: no sharp outlines, no cel shading, no anime
gloss, never neon. A single Hughes-style watercolour, atmospheric, an enchanted cold moonlit
fairy glade. No text, no border, no frame. Keep the portrait/square composition.
```
> ⏳ 결과 후 = 톤이 곡(긴장된 신비)과 붙었는지 코튼 청취-시각 대조 → 부족 시 (B) 명화 재선정 재고.
> 레터박스/비주얼라이저도 차가운 톤(silver-blue)으로 동기화 예정.

## 다음 (커버 LOCK 후)
album_1x1.png LOCK → 레터박스 색 도출(Hughes 달빛 무드 = dark blue-green base 권고 · A/B/C 비교) →
signature wordmark v3 → render → QC → 썸네일(make_thumbnail.py · 풀네임 Pyotr Ilyich Tchaikovsky
or 공간부족시 성만 fallback) → 비주얼라이저 → 영상 패키지.
