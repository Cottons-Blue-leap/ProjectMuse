# Cover Generation Notes — Boccherini: Minuet (String Quintet Op.11 No.5, G.275, 3rd mvt)

> Method: **MOKA writes prompt → 코튼이 GPT image generation** (image-edit). NOT local ComfyUI. 선례 = Pachelbel/Chopin/Sugar Plum cover-gen-notes.
> ⚠️ 표준 path (NOT 발레 sub-family). 미뉴에트=궁정 사교춤이지만 발레곡 아님 → ballet_subfamily_convention 비적용.

## ★★ LOCKED (2026-06-08) — Longhi *The Dancing Lesson* preserve path

**베이스 명화 = Pietro Longhi, *The Dancing Lesson* (La lezione di ballo/danza, c.1741, 61×51cm, Gallerie dell'Accademia Venice)**. 화가 d.1785 → PD강. 화가 중복 점검 통과(Longhi 미사용). 시대·국적 정합 = 이탈리아 베네치아 로코코 c.1741 ↔ 보케리니 이탈리아 고전/갈랑 1771.

**선정 논리** = 미뉴에트는 *음악이자 궁정 춤*인데, 이 그림이 **춤(무도 레슨) + 음악(바이올린)을 한 장에** 담아 곡 정체성에 가장 정확. (다른 AI 6점 패널 교차검증 → Tiepolo *The Minuet*[가면 카니발 군무·무드 불일치·attr.] 반려, Fragonard *Young Girl Reading*[단독 인물형 대안]보다 '춤+음악' 이중성에서 우위. 코튼 2026-06-08 확정.)

### 원작 구도 (4인 · 사실 대조 완료)
- **중앙**: 흰 새틴 드레스(분홍 모피 트림)의 젊은 여인 = 주인공. 무도 선생 향해 미뉴에트 스텝. 어두운 방에 흰 드레스만 환하게 떠오름. 원작 시선 = vezzoso(요염·도발).
- **우측**: 무도 선생 — 삼각모+작은 검을 스툴에 내려놓고 지도.
- **좌측**: 바이올린 주자 — 거리 두고 반주.
- **앉음**: 어머니가 지켜봄.
- 방: 초록 새틴 소파·벽지, 무거운 벨벳 커튼, 벽거울, 인공조명 → 다크 톤.

### LOCK 결정 (코튼 2026-06-08 "추천대로")
1. **미쿠 = 중앙 춤추는 여인 1인만 교체.** 초점·조명·단독성 최적 자리.
2. **나머지 3인(선생·바이올린·어머니) 전원 보존** — '춤+음악' 서사 = 이 그림 선정 이유. 빠지면 무력화.
3. **포즈 = 원작 미뉴에트 스텝 그대로 보존.** ★ ⑧ 사탕요정의 '명화 보존↔포즈 변경' 충돌을 여기선 회피 — 원작이 이미 우리가 원하는 춤 포즈라 포즈 합성 불필요. 깨끗한 보존+리스킨.
4. **드레스 = 흰 새틴 보존** (anchor ivory 정합 · 머리만 미쿠여도 충분히 읽힘). 분홍 트림 청록 악센트는 옵션.
5. **표정 = 유일한 변경** — 원작 요염 시선 → anchor대로 조용·약간 멜랑콜리.
6. **크롭 = 1:1**, 중앙 미쿠 초점 + 3인이 프레임 감쌈.

## 잔여 (현재 → 커버 LOCK)
- ✅ **source image 확보 완료 (2026-06-08)** = `longhi_dancing_lesson_c1741_wga.jpg` (WGA · PD-Art) + `source-image-url.txt` + `source-rights-notes.md`. 실제 이미지 시각 검증 = 4인 구도 노트 일치(정정 = 바이올린 주자 좌측 **서서** 연주 · 어머니 좌측 전경 등돌려 앉음). ※ image-edit는 GPT from-scratch라 소스는 구도 인식용 → 발행 해상도는 GPT 생성본 결정(family 선례).
- 실제 생성 = V6 입력 + 마스터 후 영상 패키지 단계 (지금은 베이스·구도 spec LOCK까지).

## LOCK 프롬프트 draft (image-edit · The Dancing Lesson attach)
```
Edit this painting — Pietro Longhi's "The Dancing Lesson" (c.1741), a Venetian Rococo interior:
a young woman in a white satin dress dances a minuet step before a dancing master (right), a
standing violinist plays at the left, and her mother sits watching in the foreground, in a dark room with
a green satin sofa and velvet curtains. Keep the canvas almost entirely intact — Longhi's soft
warm Rococo brushwork, the exact composition, the dancing master, the violinist, the mother, the
room, the dark painterly atmosphere with the white dress glowing against it. Do NOT repaint as a
new picture — preserve Longhi's original and ONLY transform the central dancing young woman into
Hatsune Miku:
- Pose: keep her EXACT pose and scale — mid-minuet step, the same graceful dancing stance and the
  same placement in the room. Do not re-pose her.
- Face: same head position/angle, but her face as Hatsune Miku — youthful, serene, gently
  melancholic young East-Asian girl, in Longhi's soft painterly brushwork. (Do NOT Westernize —
  round youthful Miku face, large gentle eyes. Soften the original flirtatious look to quiet calm.)
- Hair: long teal-cyan twin-tails (Miku's signature), within Longhi's warm palette, never neon.
- Costume: keep the same white satin dress with pink fur trim; render it in Longhi's brushwork.
  (Optional: a faint cool teal accent, but keep it essentially the white satin gown.)
Keep everything else — the dancing master, the violinist, the mother, the room, the composition,
the brushwork, the dark warm lighting — exactly as Longhi painted it. No text, no border. Keep
original aspect (crop to square later).
```
> 표정 미세조정 필요 시 = 별 세션(결과물 attach + "Change ONLY her facial expression · subtle · do NOT re-pose/crop · round East-Asian Miku face").

## Iteration log (코튼 generation 시점)
- **v1 결과 (코튼 2026-06-08 · 거부)**: 명화 보존은 우수(방·3인·붓터치·포즈·머리 청록 트윈테일 완벽). **BUT 중앙 인물 = 원작 성인 여성의 얼굴형·체형·표정을 거의 그대로 두고 머리만 청록으로 칠함** → "청록 머리한 18세기 성인 여인"이지 미쿠 아님. 코튼 적발 = 체형·얼굴형·표정·드레스 4개 다 어긋남.
  - **진단**: 프롬프트의 "keep EXACT pose/scale·preserve original" 보존 압력이 너무 세서 "youthful round Miku face" 변환을 억눌렀음. ⑧과 **정반대 실패**(⑧=과생성/명화상실, v1=과보존/미쿠상실). 4개 지적 = 한 뿌리 = 인물을 미쿠로 '덜' 바꿈.
  - **수정 방향**: keep(장면+포즈+위치+흰새틴 정체성) vs transform(나이·얼굴형·체형·머리·표정)을 명확히 분리하고, **"young teenage girl, NOT a grown woman"을 front-load**. 보수적 보존이 인물 변환을 못 잡아먹게.
  - **경로 결정 (코튼 2026-06-08)**: refine-on-result 말고 **원본 Longhi에서 v2 재생성**(1차 아티팩트 미상속).

### Prompt v2 (원본 Longhi attach · keep/transform 분리 · youthening front-load)
```
Edit this painting — Pietro Longhi's "The Dancing Lesson" (c.1741). Keep the entire scene as a real Longhi Rococo oil painting: the dark warm room, the green satin sofa, the velvet curtain, the wall mirror, the standing violinist at the left, the dancing master at the right, the seated mother in the foreground, the whole composition, lighting and soft warm brushwork — all preserved exactly.

Transform ONLY the central dancing figure into Hatsune Miku as a young teenage girl. Keep her exact POSE and POSITION (mid-minuet step, hand extended, standing in the same spot in the frame), but fully reimagine HER as Miku — do NOT leave her as a grown 18th-century woman:
- Age & body: a young teenage girl — slender, petite and girlish, NOT a mature full-figured woman. Slim youthful build.
- Face: a soft, ROUND young face — smooth youthful cheeks, large gentle eyes, small nose, a delicate young East-Asian girl, clearly Hatsune Miku. NOT a narrow mature Western face.
- Hair: long teal-cyan twin-tails (Miku's signature), tied in two tails, within Longhi's warm painterly palette, never neon.
- Expression: quiet, calm and gently melancholic — serene, lips closed or barely parted, no coy adult smile.
- Dress: keep her in a white satin gown of the period (so she belongs in the painting), but clean smooth white/ivory satin with a modest higher neckline (not low-cut), subtle trim. Painted in Longhi's soft brushwork.

Render her entirely in Longhi's oil-painting technique so she belongs in the canvas — soft warm brushwork, no anime gloss, no sharp outlines, no cel shading, never neon. Keep everything else — the three other figures, the room, the composition, the pose — exactly as Longhi painted it. No text, no border. Keep the original aspect ratio.
```
> ⏳ v2 결과 후 = 4 체크(미쿠 인식도/원작 보존도/포즈·드레스/표정). 여전히 성인이면 youthening 더 강화 or 얼굴만 별도 패스.

- **v2 결과 (코튼 2026-06-08 · 거부)**: youthening 성공 — 체형 슬림·어려짐, 흰 새틴 목선 정리, 청록 트윈테일 길어짐, 장면 보존 우수. **BUT 새 벽 = "미쿠 인형(porcelain doll) 같다 → 기존 미쿠팬 불쾌한 골짜기"** (코튼). 원인 = 그림체(Longhi 타이트 리얼리스트 유화)에 맞추려고 얼굴을 *사실적 유화*로 렌더 → 미쿠 캐릭터성(큰 눈·생기)이 죽고 굳은 마네킹/도자기 인형이 됨.
  - **진단**: Longhi의 어둡고 타이트한 장르화 화풍은 ⑧ Renoir·짐노페디 Whistler의 *부드러운 인상주의*보다 미쿠 합성에 적대적 — soft 붓질이 안 숨겨주니 사실적 얼굴이 곧장 uncanny. v1=과보존(성인), v2=과사실(인형). **레버 = 얼굴을 사실 유화 ↔ 미쿠 캐릭터 가독성 사이에서 후자 쪽으로** = 큰 또렷한 눈·생기·살아있는 표정 우선, painterly하되 '인형' 아닌 '그려진 미쿠 캐릭터'.
  - **경로 (코튼 답 대기)**: v2의 체형·드레스·머리·장면은 good → **얼굴만 겨냥한 v3 face-refine**(surgical). degrade 시 원본 재생성.

### Prompt v3 (face-targeted refine · v2 결과 attach · 인형→캐릭터 가독성)
```
Refine ONLY the central figure's face and head in this image. Everything else is good — keep the whole scene, her pose, her white satin dress, her teal twin-tails, the three other figures, the room, the brushwork — all unchanged.

The problem: her face currently looks like a stiff porcelain doll / mannequin (uncanny valley). Fix it so she clearly and warmly reads as the Hatsune Miku CHARACTER — alive, not a doll:
- Give her Miku's characteristic face: larger, brighter, clearly defined eyes with soft lively catchlights, an unmistakably Miku look (anime-rooted), rendered in a soft painterly way so she still sits inside the painting — but do NOT render her as a hyper-realistic oil portrait, which is what made her look like a doll.
- Expression: soft, calm and gently melancholic but LIVING and warm — natural softness, not a blank stiff stare. Relax the rigid doll-like symmetry.
- Keep her youthful face shape, teal hair, and head position/angle.
Do not change anything else in the painting. No text, no border.
```
> ⏳ v3 후 = 인형감 해소 + 미쿠 인식도. 여전히 골짜기면 = 화풍 적대성 의심 → 얼굴 anime 가독성 더 강화 or (최후) Longhi 적합성 재고(부드러운 화풍 명화 vs Longhi 유지).

- **v3 결과 (코튼 2026-06-08 · 거의 무변화)**: GPT가 자기 출력 face-refine에 보수적 → 차이 없음. 코튼 = "다시 처음부터". **핵심 교훈 누적 = v1 과보존(성인)·v2 과사실(인형) 양 극단 → 진짜 레버는 "사실 유화로 칠하지 말고, 미쿠 일러스트를 유화에 부드럽게 녹여라"**. 즉 *현실 인간을 미쿠 색으로 리페인트*(→ 인형)가 아니라 *미쿠 캐릭터(큰 anime 눈·생기)를 painterly하게 blend*. 양 학습(youthening + 캐릭터 가독성) 통합해 **원본에서 v4 재생성**.

### Prompt v4 (원본 Longhi attach · "미쿠 일러스트를 유화에 blend" 프레임 · 통합)
```
Edit this painting — Pietro Longhi's "The Dancing Lesson" (c.1741). Keep the entire scene as a real Longhi oil painting: the dark warm room, green satin sofa, velvet curtain, wall mirror, the standing violinist (left), the dancing master (right), the seated mother (foreground), the composition, lighting and soft brushwork — all preserved exactly.

Replace ONLY the central dancing woman with Hatsune Miku. Keep her exact pose and position (mid-minuet step, hand extended, same spot), but she must be unmistakably the Hatsune Miku CHARACTER — a cute young anime girl — gently painted into the canvas. THIS IS THE KEY: render her like an illustration of Miku softly blended into the oil painting, NOT a realistic human repainted in her colors (a realistic oil face turns her into a lifeless doll — avoid that completely).
- Face: clearly Hatsune Miku's own anime face — a soft round young face with LARGE, bright, expressive teal anime eyes (her signature look), small nose and mouth, alive and charming, recognizable to any Miku fan as Miku herself. NOT a realistic woman, NOT a stiff porcelain doll. Give her a gentle painterly finish so she belongs in the scene, but keep her anime character features and life fully intact.
- Expression: quiet, soft and gently melancholic, but warm and alive.
- Body: a slender, petite teenage girl.
- Hair: long teal-cyan twin-tails in two tails, Miku's signature, painterly, never neon.
- Dress: a clean white/ivory satin period gown with a modest neckline, subtle trim, soft-painted.

Keep everything else — the three other figures, room, composition, pose, brushwork, warm lighting — exactly as Longhi painted it. Blend Miku in with soft painterly edges (no harsh cutout), but she stays recognizably the Miku character. No text, no border. Keep the original aspect ratio.
```
> ⏳ v4 후 = 인형감 탈출 + 미쿠 인식도 + 장면 보존 동시 충족 여부. 실패 시 = Longhi 화풍 적대성 확정 → 코튼에 2갈래(anime 더 세게 vs 부드러운 화풍 명화 교체) 정직 제시.

- **v4 결과 (코튼 2026-06-08 · "이걸로도 안 되겠어")** → **커버 렌더링 일시 중단 + 세션 초기화** (코튼).

---

## ★★ NEXT SESSION 재개점 (2026-06-08 세션 초기화 시점)

**상태**: 베이스 명화 = Longhi *The Dancing Lesson* + 구도 컨셉(중앙 여인만 미쿠·3인 보존·1:1)은 LOCK 유지. **단 image-edit 렌더 v1~v4 전부 코튼 거부 → 렌더링 미해결.**

**확정된 진단** (4회 누적): Longhi의 **어둡고 타이트한 장르화 화풍이 미쿠 합성에 구조적으로 적대적**. soft 붓질(⑧ Renoir 인상주의·짐노페디 Whistler)이 없어서 — 얼굴을 사실적으로 칠하면 성인/인형(uncanny), anime로 밀면 붙인 듯(⑧ paste 위험). 양립 어려움. ★ 이건 **명화 선정 시 못 본 축** = 곡 정체성(춤+음악 다인 장면=Longhi) ↔ 미쿠 합성 용이성(부드러운 단독 인물화)이 **상충**.

**다음 세션 결정 fork (코튼 콜)**:
- **(A) Longhi 고수** + 얼굴 anime 가독성 더 세게(유화 합성 포기, 미쿠 얼굴 우선 · paste 위험 감수). 혹은 ComfyUI 등 다른 파이프 시도.
- **(B) 부드러운 화풍 명화로 교체** = 미쿠가 깨끗이 녹는 soft brushwork. 후보 = **Fragonard *A Young Girl Reading*(c.1769 · 패널 2순위 · 단독 인물·깃털 같은 로코코·이탈리아 아니지만 시대 일치)** 또는 다른 soft 로코코. trade = '춤+음악' 이중 테마 상실 → 단독 인물형 수용.
- **(C) 기타**(보케리니용 다른 컨셉 / 곡 순서 조정 등).

**MOKA 잠정 견해**: 4회 거부는 화풍 적대성 신호가 강함 → (B) 쪽이 현실적. 단 'Longhi 선정 논리(춤+음악)'를 버리는 결정이라 코튼 확인 필수. 재개 시 이 fork부터 제시.

**보존 자산**: 원본 PD 이미지 + rights 사이드카 + v1~v4 프롬프트 전문(위) = 재시도/타 명화 전환 둘 다 재사용 가능.

---

## ★★ fork 결정 = (A) Longhi 고수 (코튼 2026-06-08 "A로 진행. 분명 적합한 방법이 있을거야")

**재진단 (디버그 single-change 원칙)**: v1~v4가 전부 **같은 레버**였음 = Longhi 그림 1장만 attach + "중앙 여인을 미쿠로 transform". → GPT가 "사실적 유화 인물을 미세 수정"으로 인식 → 미쿠 anime 얼굴을 **텍스트만으로** 생성 못 함 → 성인(v1)/인형(v2) 양극단. 4회 모두 미답인 축 = **미쿠 캐릭터의 시각 앵커 부재**.

> ※ MOKA 1차안 = 미쿠 레퍼런스 2-image composite. **코튼 반려 (2026-06-08 "원작만 있어도 가능하게")** → 원작 1장 전용으로 전환. (2-image는 폴백 보존.)

### Prompt v5 (★ 단일 레버 = 얼굴 유화 사실주의 금지 + anime 미쿠 + 화풍 대비 허용 · 원작 1장만)
**진단**: v1~v4가 계속 "soft painterly finish · 유화에 녹여 · belongs in the canvas"라고 한 게 곧 **인형(사실적 얼굴=uncanny)의 원인**. GPT는 Vocaloid 미쿠를 이미 앎 — anime 정체성을 매번 유화 사실주의로 억눌렀던 게 실패 뿌리.
**단일 변경**: **얼굴만은 사실적 유화 렌더 명시 금지, 진짜 anime 미쿠로 그리고 그녀↔배경 화풍 대비를 의도된 것으로 허용**(붙인 느낌 회피보다 인형 탈출 우선). 배경·3인·방은 그대로 유화. v4와 정반대 방향(v4=사실쪽 당김 vs v5=anime쪽 해방).
```
Edit this painting — Pietro Longhi's "The Dancing Lesson" (c.1741). Keep the entire painting exactly as Longhi painted it: the dark warm room, green satin sofa, velvet curtain, wall mirror, the standing violinist (left), the dancing master (right), the seated mother (foreground), the whole composition, lighting and soft warm oil brushwork — all untouched, still a real oil painting.

Replace ONLY the central dancing woman with the iconic Vocaloid character Hatsune Miku, drawn in her own recognizable ANIME art style. Keep her exact pose, scale and position (mid-minuet step, hand extended, same spot).

THIS IS THE KEY, and the opposite of a realistic repaint: do NOT render her face as a realistic oil portrait — that is exactly what turned her into a lifeless porcelain doll before. Draw her as the actual anime Miku character:
- Face: a clean ANIME face — youthful, round, with LARGE glossy teal anime eyes, small nose and mouth, soft cel-style shading. Instantly recognizable as Hatsune Miku to any fan. Alive and gently expressive, NOT a stiff doll, NOT a realistic woman.
- Hair: long gray-teal twin-tails, her signature, tied in two tails.
- Expression: quiet, soft, gently melancholic but warm and alive.
- Body: a slender, petite teenage girl.
- Dress: a clean white/ivory satin period gown, modest neckline, so she still fits the scene.

Let her read as an anime Miku illustration standing within the oil-painted room — a gentle STYLE CONTRAST between her and the painted background is fine and intended. Only slightly soften her hardest outlines so she sits in the room's light; do NOT oil-realism her face. Keep everything else — the three other figures, the room, composition, pose, brushwork, warm lighting — exactly as Longhi painted it. No text, no border. Keep the original aspect ratio.
```
> ⏳ v5 후 = 4축 체크(미쿠 인식도/원작 보존/포즈·드레스/인형감 탈출).

- **v5 결과 (코튼 2026-06-08 · 거부)**: "미쿠만 너무 만화풍 그림체가 됐다". 풀anime로 밀었더니 명화 톤앤매너 파괴(붙인 만화). → **양 극단 매핑 완료** = v2 사실유화=인형 ↔ v5 풀anime=만화. **진짜 타깃 = 중간 바늘** = 명화 톤앤매너(유화 매체) 유지 + 미쿠 식별력 충분 *동시*.

### Prompt v6 (★ 프레임 = "Longhi가 직접 미쿠를 그렸다면" · 매체=유화 고정 + 식별=특징3개로 분리 · GPT 새 세션·원작 1장만)
**핵심 통찰**: 실패는 매번 *매체*와 *식별*을 한 다이얼로 묶은 것. v6 = 둘 분리 = **매체는 Longhi 유화로 고정**(cel/만화 outline/밝은 채색 명시 금지) + **식별은 특징 3개(① 그레이-틸 트윈테일=최강 식별자 ② 앳된 둥근 얼굴 ③ 큰 부드러운 눈)를 유화 붓질로 끌어올림**. "유화에 녹여"(v4·약함)도 "anime로"(v5·과함)도 아님.
```
Attached is Pietro Longhi's painting "The Dancing Lesson" (c.1741), a Venetian Rococo oil painting: a young woman in a white satin gown dances a minuet step in a dark warm room, with a dancing master at the right, a standing violinist at the left, and her seated mother in the foreground.

Edit this painting so that the central dancing woman becomes Hatsune Miku — while keeping the ENTIRE image looking like Longhi's original oil painting. The single hardest requirement: fully preserve the painting's tone and manner (warm dark Rococo oil, soft brushwork, painterly light) AND make Miku clearly recognizable AT THE SAME TIME. Do not sacrifice either one.

Imagine Longhi himself painted a portrait of Hatsune Miku. Render her entirely in his OIL technique — soft painterly brushwork, warm palette, gentle painted shading. NOT flat cel shading, NOT hard anime outlines, NOT bright cartoon coloring. She is an oil-painted figure in the canvas, never a cartoon pasted on top.

Yet she must be unmistakably Hatsune Miku, through her iconic features rendered in oil:
- Long gray-teal twin-tails — her single most recognizable trait, clearly tied in two tails. This is the key identifier; make sure it reads at a glance.
- A youthful, girlish round face — clearly a teenage girl, not a grown woman.
- Noticeably large, soft, gentle eyes with a faint teal tint — larger and more expressive than a realistic portrait, but painted softly (not flat anime eyes). Alive and calm, never a blank doll.
- Slender, petite build.

Keep her exact pose and position (mid-minuet step, hand extended, same spot), in a white/ivory satin period gown with a modest neckline so she belongs in the scene. Expression: quiet, soft, gently melancholic, but warm and alive.

Keep everything else exactly as Longhi painted it — the dancing master, the violinist, the mother, the room, the green satin sofa, the velvet curtain, the composition, lighting and brushwork. No text, no border. Keep the original aspect ratio.
```
> ⏳ v6 후 = 4축(톤앤매너 유지 / 미쿠 식별 / 포즈·드레스 / 인형·만화 양극단 회피). 실패 시 = ComfyUI 인페인팅(미쿠 모델·denoise 제어로 중간점 직접 타격) 또는 2-image 폴백.

- **v6 결과 (코튼 2026-06-08 · 통과 후보)**: ★ 6번 중 최고 — 톤앤매너 유지(전체 유화 통합)+미쿠 식별(또렷한 틸 트윈테일·큰 눈)+포즈·드레스 보존+인형/만화 양극단 회피 4축 통과. MOKA 권고 = LOCK 후보. 미세 = 눈이 식별 위해 약간 anime-large.
- **v7 결과 (코튼 2026-06-08 · ★ LOCK 확정 "이걸로 확정")**: v6 대비 눈을 사실쪽으로 미세 조정 = **톤 통합 우세본**(얼굴 완전 유화·anime-lean 제거·uncanny 0). MOKA 비교 = v7=더 좋은 그림(톤 완벽) / v6=더 강한 미쿠(한눈 식별). 코튼 톤 우선 → v7 채택. 식별은 틸 트윈테일이 지탱 + 썸네일 텍스트가 보강.

## ★★★ COVER LOCK (2026-06-08) — v7

**최종 커버 = `video/cover/Miku_longhi_dancing_lesson_c1741_wga.png` (1254×1254 · rgb24 · 코튼 저장).**
- 베이스 = Pietro Longhi *The Dancing Lesson* (c.1741 · PD강 · 화가 미중복) · 중앙 댄서만 Classical Miku · 3인+방 원작 보존 · 미뉴에트 스텝 포즈 보존 · 흰 새틴 가운.
- 좌하단 붉은 물체 = **코튼 확인 = 배경물**(엠블럼/텍스트 아님 · QC clear).
- 화가 중복맵 갱신: Satie/Chopin=Whistler·Vivaldi=Botticelli·Joplin=Glackens·Elgar=Waterhouse·Mozart=VanGogh·Pachelbel=Vermeer·Degas=백조예약·Tchaikovsky사탕요정=Renoir·**Boccherini미뉴에트=Longhi**.
- description 크레딧 = 'Cover art, after Longhi, The Dancing Lesson (c.1741).' (release 단).

### 핵심 교훈 (v1~v7 = 7회 cycle)
타이트 장르화(Longhi) + 미쿠 합성의 상충은 **매체와 식별을 한 다이얼로 묶을 때** 발생. 양 극단 = v1 과보존(성인)·v2 과사실(인형)·v5 과anime(만화). **해결 = 둘 분리** = "Longhi가 직접 미쿠를 그렸다면" 프레임으로 **매체=유화 고정 + 식별=시그너처 특징(트윈테일·앳된얼굴·큰눈)을 유화 붓질로 끌어올림**. ⑧ Renoir(부드러운 인상주의)와 달리 타이트 화풍에선 이 분리 지정이 필수. 차기 타이트 장르화 명화 재사용 가능.

## 잔여 파이프 (커버 LOCK 후)
1:1 crop(album_1x1) → 레터박스 색 도출(다크 웜 살롱 무드 = warm-dark base 권고) → signature wordmark v3 → render → QC → 썸네일(make_thumbnail.py · Luigi Boccherini) → 비주얼라이저 → 영상 패키지 → l10n 9언어 → 예약 발행.
