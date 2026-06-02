# Cover Generation Notes — Pachelbel Canon in D

> Method: **MOKA writes prompt → GPT image generation** (image-edit with the Vermeer
> reference attached). NOT local ComfyUI. Recorded s389 (2026-06-02). Chopin precedent =
> `../../chopin_nocturne_op9_2/video/art_sources/cover-gen-notes.md`.

## Inputs
- **Reference painting**: `vermeer_young_woman_seated_at_a_virginal_NG2568_GAP.jpg` (Wikimedia
  Commons Google Art Project, PD-Art — see source-rights-notes.md). 10100×11371. Attach as the
  edit reference.
- **Character anchor** (`planning/classical_miku_anchor.md`): teal-cyan twin-tails · simple
  late-19th-century European dress in muted tones (blue-gray, dark teal, black, ivory) ·
  quiet melancholic expression. (의상은 이미 명화의 17c 청록 드레스가 anchor 'muted teal/blue'
  정합 → 명화 의상 keep, 머리만 미쿠 트윈테일로.)

## Compositing approach (canon-specific · differs from chopin)
- **Chopin** = Miku replaced a *distant tiny fisherman* → faint-veiled, presence carried by
  thumbnail text. **Canon** = the painting's **central seated woman is already a teal-dressed
  figure at the keyboard** → she simply *becomes* Miku. Presence = **A (clear painterly figure,
  not faint-veiled)** — she is the subject, dissolving her would gut the composition.
- **The one change**: the seated young woman's hair → long teal-cyan twin-tails, rendered in
  Vermeer's smooth tonal brushwork (a soft cool accent inside the palette, NOT bright anime
  hair). Keep her serene face, the blue dress, her pose, the virginal, and EVERYTHING else.
- **Keep untouched (relation hook)**: the **viola da gamba (bass viol) + bow at lower-left**,
  the **virginal (keyboard) with painted lid + sheet music**, the gilt-framed *Procuress*
  painting on the back wall, the blue curtain, the tapestry at the left edge, the
  black-and-white checkered floor, the *"Meer"* signature on the wall. These carry the
  basso-continuo ↔ ground-bass tie — do not alter them.
- **Light**: keep Vermeer's soft left-window side-light (left→right falloff).
- **Aspect**: source is portrait (~0.888). Keep the full painting proportions for the 16:9
  frame source; the 1:1 album crop holds **woman + virginal + viola da gamba** (square crop
  weighted slightly left so the bass viol stays in frame — it is the ground-bass anchor).
- **Resolution**: generate at ≥2560px (2K cover needs ~960px display; 3840 leaves 4K room).

## Prompt v1 (English · GPT image-edit, Vermeer reference attached)

```
Edit this painting — Johannes Vermeer's "A Young Woman seated at a Virginal" (c.1670-72,
National Gallery London). Preserve the original painting's surface completely: its smooth,
softly blended oil brushwork, its warm dark tonal palette with the cool blue-teal accents, the
quiet Dutch-interior light falling from the left, and the calm mood. Keep EVERY element exactly
as it is — the viola da gamba (bass viol) and its bow lying at the lower-left, the virginal
(keyboard instrument) with its painted lid and the sheet music on its stand, the large gilt-
framed painting on the back wall, the blue curtain, the patterned tapestry at the left edge,
the black-and-white checkered marble floor, and the signature on the wall. The seated young
woman keeps her exact pose, her blue-teal satin dress, her white lace, her chair, and her
serene gently-melancholic face.

Make ONE change, painted in Vermeer's identical technique so it belongs completely: give the
seated young woman long teal-cyan twin-tails — her hair gathered into two soft tails — so she
becomes gently recognizable as Hatsune Miku reimagined as a quiet 17th-century presence. Render
the teal hair as a soft, cool, muted accent that sits inside the painting's existing palette,
in the same thin smooth blended brushstrokes: veiled and atmospheric, never bright, no sharp
outlines, no cel shading, no anime gloss, no glow. She stays a graceful, beautiful, painterly
figure — a Vermeer woman who happens to be Miku, not a modern character pasted in.

A single oil painting, smooth and atmospheric, Dutch Baroque interior. No text, no added
signature beyond the existing one, no border, no frame. Keep the portrait aspect ratio of the
reference.
```

## Prompt v2 (pose refine · 코튼 s389 · "구도 유지 + 연주 집중 포즈")
> 원작은 여인이 관객 쪽으로 고개 돌려 응시 → **건반/악보에 몰입한 연주 포즈**로 변경.
> 전체 구도·프레이밍·좌석 위치·스케일·모든 오브젝트는 그대로. 머리 방향/시선/손만 변경.

```
Edit this painting — Johannes Vermeer's "A Young Woman seated at a Virginal" (c.1670-72,
National Gallery London). Preserve the original painting's surface completely: its smooth,
softly blended oil brushwork, its warm dark tonal palette with the cool blue-teal accents, the
quiet Dutch-interior light falling from the left, and the calm mood. Keep the overall
composition, framing, scale, and the woman's seat and position exactly as they are. Keep EVERY
object exactly as it is — the viola da gamba (bass viol) and its bow at the lower-left, the
virginal (keyboard) with its painted lid and the sheet music on its stand, the large gilt-
framed painting on the back wall, the blue curtain, the tapestry at the left edge, the black-
and-white checkered marble floor, and the signature on the wall. Keep her blue-teal satin
dress, her white lace, and her chair unchanged.

Make TWO changes, both painted in Vermeer's identical technique so they belong completely:

1) Pose — instead of turning her head toward the viewer, she is now absorbed in playing: her
head and gaze incline down toward the keyboard and the sheet music, both hands resting and
engaged on the virginal's keys, her body still in the same seated position and scale. Her
expression is serene and quietly concentrated, lost in the music — not looking out of the
painting. The change is only her head direction, gaze, and hands; the framing stays identical.

2) Hair — give her long teal-cyan twin-tails gathered into two soft tails, so she becomes
gently recognizable as Hatsune Miku reimagined as a quiet 17th-century presence. Render the
teal as a soft, cool, muted accent inside the painting's existing palette, in the same thin
smooth blended brushstrokes: veiled and atmospheric, never bright, no sharp outlines, no cel
shading, no anime gloss, no glow. She stays a graceful, beautiful, painterly figure — a Vermeer
woman who happens to be Miku, not a modern character pasted in.

A single oil painting, smooth and atmospheric, Dutch Baroque interior. No text, no added
signature beyond the existing one, no border, no frame. Keep the portrait aspect ratio of the
reference.
```

## Iteration log (코튼 generation 시점 박음)
- **v2 결과 (코튼 s389)**: 포즈 변경 성공 (건반 몰입 · 구도/viola/배경 전부 보존). BUT 코튼 비평 2건:
  (1) "미쿠 복식 아님" — Vermeer 화려한 바로크 satin 드레스 그대로 = Classical Miku anchor
  (*simple late-19c · muted blue-gray/dark teal*)와 불일치. v2가 "드레스 유지"로 박아 anchor 3대
  고정요소 중 하나를 어김. (2) "너무 서양인처럼" — 얼굴이 17c 유럽 여인 = 미쿠 비인식. + 머리도
  single veil에 가깝고 twin-tails 불명확.
- **진단**: 균형추를 "Vermeer 여인 that happens to be Miku" → "확실히 Hatsune Miku, painterly로
  렌더"로 이동. 얼굴(미쿠/동아시아 youthful) + 머리(또렷한 teal twin-tails) + 드레스(muted simple)
  3개 refine. 포즈/구도/오브젝트 전부 keep.

## Prompt v3 (refine — attach the v2 generated image · face+hair+dress)
> 생성본 위에 refine. 포즈·구도·viola·배경 전부 보존. 얼굴/머리/드레스만 변경.
> **v2 base 보존** = `../cover/iterations/cover_v2_pose_base.png` (1386×... · 포즈 승인된 결과 ·
> v3 진입 시 이 이미지를 reference로 attach). **새 세션 이어받기** (코튼 s389 = 새 세션 재생성):
> 새 세션 = 이 v3 프롬프트 + cover_v2_pose_base.png attach → GPT 이미지-edit → 코튼 비평 →
> album_1x1.png LOCK → render→QC→thumbnail→upload (나머지 전부 스테이징 완료).

```
Keep this painting almost exactly as it is — the same composition, the same Vermeer oil
brushwork and warm tonal palette, the same seated pose absorbed in playing at the virginal,
the same viola da gamba and bow at the lower-left, the same gilt-framed painting on the back
wall, the same blue curtain, tapestry, checkered floor, and instruments. Refine ONLY the
figure herself so she clearly reads as Hatsune Miku, not as a 17th-century European woman.

1) Face — give her the youthful face of Hatsune Miku: a soft, serene, gently melancholic young
East-Asian girl, NOT a mature Western-European woman. Keep it painterly in Vermeer's smooth
blended oil technique — recognizably Miku, yet rendered as if Vermeer himself painted her: no
sharp outlines, no cel shading, no anime gloss.

2) Hair — give her clear, long teal-cyan TWIN-TAILS: her hair gathered into two distinct tails
(Hatsune Miku's signature), not a single loose veil of hair. Render the teal as a soft cool
accent inside the painting's palette, painterly and atmospheric, never neon or bright.

3) Dress — replace the ornate bright-blue Baroque satin court gown with the character's own
costume: a SIMPLE, plain late-19th-century European dress in muted tones (muted dark teal,
blue-gray, ivory), high-necked, modest and understated. Still painted in Vermeer's smooth oil
technique and tonal values so it sits naturally in the painting's light — but simpler and
plainer than a 17th-century court gown.

Everything else stays identical. A single Vermeer-style oil painting, smooth and atmospheric,
Dutch Baroque interior. No text, no border. Keep the portrait aspect ratio.
```

## Prompt v4 (FROM-SCRATCH · 원본 Vermeer reference attach · 코튼 s389 = 새 ChatGPT 챗 처음부터)
> 코튼 결단 = v2 출력물 refine이 아니라 **새 ChatGPT 세션에서 원본 명화 기준 처음부터 재생성**.
> → v2(포즈) + v3(얼굴·머리·드레스) 변경을 **한 프롬프트에 통합**, **원본 `vermeer_young_woman_seated_at_a_virginal_NG2568_GAP.jpg` attach**하고 한 번에 적용.

```
Edit this painting — Johannes Vermeer's "A Young Woman seated at a Virginal" (c.1670-72,
National Gallery London). Preserve the original painting's surface completely: its smooth,
softly blended oil brushwork, its warm dark tonal palette with cool blue-teal accents, the
quiet Dutch-interior light falling from the left, and the calm mood. Keep the overall
composition, framing, and scale exactly. Keep EVERY object unchanged — the viola da gamba
(bass viol) and its bow at the lower-left, the virginal (keyboard) with its painted lid and
the sheet music on its stand, the large gilt-framed painting on the back wall, the blue
curtain, the tapestry at the left edge, the black-and-white checkered marble floor, and the
signature on the wall. Keep her seated in the same place, at the same scale, on the same chair.

Reimagine ONLY the seated woman herself as Hatsune Miku — painted entirely in Vermeer's own
smooth, blended oil technique and tonal values, so she belongs completely in the painting (no
sharp outlines, no cel shading, no anime gloss, no glow, never neon or bright):

- Pose: she is absorbed in playing, not turned toward the viewer. Her head and gaze incline
  down toward the keyboard and the sheet music, both hands resting and engaged on the virginal's
  keys, lost in the music. Same seated position and scale; only her head direction, gaze, and
  hands change from a viewer-facing pose to an inward, playing one.
- Face: the youthful face of Hatsune Miku — a soft, serene, gently melancholic young East-Asian
  girl, recognizably Miku, NOT a mature Western-European woman. Painterly, as if Vermeer painted
  her.
- Hair: long teal-cyan TWIN-TAILS — her hair clearly gathered into two distinct tails (Miku's
  signature), a soft cool teal accent inside the painting's palette, painterly and atmospheric.
- Dress: a SIMPLE, plain late-19th-century European dress in muted tones (muted dark teal,
  blue-gray, ivory), high-necked, modest and understated — NOT an ornate Baroque satin court
  gown. Painted in the same oil technique so it sits naturally in the light. (A late-19th-c
  dress in a 17th-c room is intentional — this is Miku's consistent series costume.)

A single Vermeer-style oil painting, smooth and atmospheric, Dutch Baroque interior. No text,
no added signature beyond the existing one, no border, no frame. Keep the portrait aspect ratio
of the reference.
```

## Prompt v6 (pose → SINGING · 코튼 s389 · refine on locked album_1x1.png)
> 코튼 결단 = 연주 자세 → **노래 부르는 자세**(두 손 가슴팍에 모으고). 사유 = 아카펠라 채널 본질
> (voice only · 악기 연주 X)과 정합 강 · 악기는 관계훅 소품으로 잔존. + 3색 그라데이션이 어두운
> 커버와 밝기 불일치 → 레터박스 재도출 의제(새 커버 기준 darker/warmer · 옵션 비교).
> 방법 = locked album_1x1.png attach → 자세/손만 변경 refine (승인된 얼굴/머리/드레스 보존).

```
Keep this painting almost exactly as it is — the same Hatsune Miku figure with her teal-cyan
twin-tails, her serene young face, her simple muted dark-teal dress, seated in the same chair
in the same place, at the same scale. Keep the entire room and every object unchanged: the
virginal (keyboard) and its sheet music, the viola da gamba and bow at the lower-left, the
gilt-framed painting on the back wall, the blue curtain, the tapestry, the checkered floor.
Keep Vermeer's smooth oil brushwork, warm tonal palette, and the soft light from the left.

Change ONLY her pose and hands: instead of playing the keyboard, she now sits upright in the
same seat and sings — both hands gently gathered together at her chest, clasped near her heart
in a quiet, prayer-like singing gesture, no longer touching the keys. Her posture lifts a
little; her face is serene and gently absorbed in singing, eyes softly lowered or barely closed
— a calm, inward singing expression, not theatrical, mouth only barely parted. She stays
recognizably Hatsune Miku, painted in Vermeer's smooth technique: no sharp outlines, no cel
shading, no anime gloss, no glow.

A single Vermeer-style oil painting, smooth and atmospheric, Dutch Baroque interior. No text,
no border, no frame. Keep the square 1:1 composition.
```
> ⏳ 새 커버 후: 레터박스 재도출(현 [#2A3F44,#4A4537,#B7A988] = cream bottom이 dark 커버와 밝기충돌
> → darker/warmer 2~3옵션) → Root.tsx 갱신 → re-render. 기존 render/cover는 v6로 supersede.

## Prompt v7 (singing refine: head up + lips parted + slimmer hands · 코튼 s389)
> v6 결과(노래 자세 들어옴) → 코튼 비평: (1) 가슴 앞 손이 두껍/무거움 (2) 고개 아직 숙임 →
> 위로 들고 입 살짝 벌린 노래 자세로. refine on v6 singing image (attach).

```
Keep this painting almost exactly as it is — the same Hatsune Miku figure with her teal-cyan
twin-tails, simple muted dark dress, seated in the same chair and place at the same scale, both
hands gathered at her chest in a singing gesture. Keep the whole room and every object
unchanged: the virginal and its sheet music, the viola da gamba and bow at the lower-left, the
gilt-framed painting, the blue curtain, the tapestry, the checkered floor. Keep Vermeer's
smooth oil brushwork, warm tonal palette, and the soft left light.

Make TWO refinements only:
1) Head and expression — instead of bowing her head downward, she now lifts her head gently
upward and forward as she sings: her lips are slightly parted as if sustaining a soft note, her
face serene and uplifted, eyes gently closed or softly raised. A calm, lyrical singing
expression — not theatrical, mouth only slightly open.
2) Hands — her clasped hands at her chest currently look too thick and heavy; refine them into
more delicate, slender, graceful hands, softly painted.

Keep her recognizably Hatsune Miku, painted in Vermeer's smooth technique: no sharp outlines,
no cel shading, no anime gloss, no glow. A single Vermeer-style oil painting, smooth and
atmospheric, Dutch Baroque interior. No text, no border, no frame. Keep the square 1:1 composition.
```

## Prompt v8 (FROM-SCRATCH · 깨끗한 원본 · 노래 구도 통합 · 코튼 s389)
> 코튼 적발 = v6/v7 결과에 검정 반점·열화 (img2img edit chain 아티팩트 누적). → 깨끗한 고해상
> 원본 `vermeer_young_woman_seated_at_a_virginal_NG2568_GAP.jpg`(10100×11371) attach하고 **목표
> 구도(노래 자세 미쿠)를 한 번에 from-scratch**. v4(미쿠化) + v6/v7(노래·고개위·가는손) 통합.
> 출력 = portrait(원본 비율) keep → MOKA가 1:1 crop (여인+viola da gamba).

```
Edit this painting — Johannes Vermeer's "A Young Woman seated at a Virginal" (c.1670-72,
National Gallery London). Preserve the original painting's surface, technique, and atmosphere
completely: its smooth, softly blended oil brushwork, its warm dark tonal palette with cool
blue-teal accents, the quiet Dutch-interior light from the left, the calm mood. Keep the
overall composition, framing, and scale. Keep EVERY object exactly: the viola da gamba (bass
viol) and bow at the lower-left, the virginal (keyboard) with its painted lid and the sheet
music on its stand, the large gilt-framed painting on the back wall, the blue curtain, the
tapestry at the left edge, the black-and-white checkered floor, and the signature on the wall.
Keep her seated in the same chair, same place, same scale.

Reimagine ONLY the seated woman as Hatsune Miku, singing — painted entirely in Vermeer's own
smooth, blended oil technique so she belongs completely (no sharp outlines, no cel shading, no
anime gloss, no glow, never neon):

- She is singing, not playing: she sits upright in her chair and does NOT touch the keyboard.
  Both hands are gently gathered together at her chest, clasped near her heart — delicate,
  slender, graceful hands. Her head lifts gently upward and forward as she sings, her lips
  slightly parted as if sustaining a soft note, her face serene and uplifted with eyes softly
  closed. A calm, lyrical, inward singing expression — not theatrical.
- Face: the youthful face of Hatsune Miku — a soft, serene young East-Asian girl, recognizably
  Miku, not a mature Western-European woman.
- Hair: long teal-cyan twin-tails gathered into two distinct tails, a soft cool teal accent
  within the painting's palette, painterly and atmospheric.
- Dress: a simple, plain late-19th-century European dress in muted tones (muted dark teal,
  blue-gray, ivory), high-necked and understated — not an ornate Baroque court gown.

A single Vermeer-style oil painting, smooth, clean and atmospheric, with a pristine painterly
surface and NO blotches or dark artifacts. Dutch Baroque interior. No text, no added signature
beyond the existing one, no border, no frame. Keep the portrait aspect ratio of the reference.
```
> ⏳ 레터박스 A/B/C 선택은 clean 버전에도 그대로 유효 (구도·팔레트 동일 · 톤만 깨끗). 독립 결정 가능.

## 드레스 결단 (코튼 s389 · LOCK)
- **시대 불일치 OK** (코튼 2026-06-02). → Classical Miku anchor 문자 그대로 **simple late-19c
  European muted dress** 적용. 1670s Vermeer 실내에 19c 드레스 = anachronism이지만 시리즈 복식
  일관성 우선 (쇼팽 등 family 동일 앵커 드레스). period-plausible 절충안 폐기.

## FINAL — locked (코튼 s389 · 2026-06-02)
- **`video/cover/album_1x1.png`** (1254×1254 · 1:1) — confirmed cover (**v8 clean from-scratch**).
  Miku **singing** (NOT playing): seated upright, head lifted, lips slightly parted, eyes softly
  closed, both hands clasped at her chest (slim/delicate), serene uplifted singing expression.
  Clear teal twin-tails, simple muted dark-teal late-19c dress. Viola da gamba + bow fully in
  frame lower-left (ground-bass/continuo relation hook), virginal + sheet music, gilt-framed
  painting upper-right, blue curtain, tapestry, checkered floor — all preserved. **Pristine
  surface, no blotches** (검정 반점 = img2img edit-chain 열화 → from-scratch on clean original로 해결).
- Method = GPT image-edit, **from-scratch on the clean original Vermeer NG2568 reference**
  (10100×11371) · Prompt **v8** consolidated (Miku化 + 노래자세 + 고개위 + 가는손 + 19c muted dress).
- Iteration history (above): v1→v2(pose)→v3 → v4(from-scratch playing) → [코튼 LOCK→재오픈]
  → v5(playing delivered) → v6(singing) → v7(head-up/slim-hands refine) → **v8(clean from-scratch
  singing = FINAL)**. 모든 delivered 보존 = `cover/iterations/cover_v{2,5,7,8}_*.png`.
- ⚠️ 1254² < 2560 ideal but 쇼팽 1254 발행 선례 = 충분 (2K 프레임 내 커버 표시 ~960px 받침).
- ⏳ 레터박스 색 = A/B/C 중 코튼 택1 대기 (MOKA 추천 B teal-accent). 선택 후 Root.tsx 갱신 → re-render.

## ⚠️ 코튼 결단 자리 (generation 진입 시)
1. **Miku presence 강도** — 본 노트 default = A(clear painterly 여인=미쿠). 더 faint-veiled로
   갈지(쇼팽 톤) 코튼 결단. 본 명화는 여인이 중심이라 clear 권고.
2. **트윈테일 vs 17c 헤어** — 미쿠 인식 vs Vermeer 시대 정합 trade. default = teal 트윈테일
   (인식 우선 · painterly 톤다운). 코튼 조정.
3. **1:1 crop 텍스트 자리** — 좌하단 text stack이 viola/virginal busy 영역과 겹침 → blur plate/
   shadow 강도 or crop 미세조정 iteration 자리 (cover 합성 후).
