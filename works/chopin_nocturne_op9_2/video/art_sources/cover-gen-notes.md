# Cover Generation Notes — Chopin Nocturne Op.9-2

> Method: **MOKA writes prompt → GPT image generation** (image-edit with the Whistler
> reference attached). NOT local ComfyUI. Recorded s384 (2026-05-30).

## Inputs
- **Reference painting**: `whistler_nocturne_blue_silver_chelsea_GAP.jpg` (Wikimedia Commons
  Google Art Project, PD — see source-rights-notes.md). Attach as the edit reference.
- **Character anchor** (`planning/classical_miku_anchor.md`): teal-cyan twin-tails · simple
  late-19th-century European dress in muted tones (blue-gray, dark teal, black, ivory) ·
  quiet melancholic expression.
- **Miku presence = A (faint veiled figure)** — 코튼 결단 s384. Gymnopédie ① precedent
  (same Whistler nocturne genre). Miku dissolved into Whistler's tonal haze, NOT a sharp
  anime character. Recognition is carried by the 初音ミク thumbnail text downstream.
- **Position**: the lone fisherman at the lower-right shallows → becomes Miku, same scale/softness.
- **Aspect**: keep the reference's landscape proportions (~1.22:1) so one image serves both the
  16:9 video frame and the 1:1 album-cover crop (crop the right-of-center square holding Miku).

## Prompt v1 (English · GPT image-edit, reference attached)

```
Reimagine this painting — James McNeill Whistler's "Nocturne: Blue and Silver — Chelsea"
(1871) — keeping its exact composition, blue-silver tonal palette, soft horizontal
brushwork, oil-on-panel atmosphere, and quiet nocturnal mood completely intact. The dark
Chelsea shoreline silhouette with faint warm lights along the top, the wide calm
silvery-blue Thames, the long moored barge at lower-left, and the small butterfly cartouche
near the bottom-center all stay exactly as they are.

Make ONE change: where the lone fisherman stands in the shallow water at the lower-right,
place instead a single solitary young woman — Hatsune Miku reimagined as a quiet
19th-century presence. She stands at the water's edge in that same spot, seen from a
distance, small within the vast nocturne. She has long teal-cyan twin-tails and wears a
plain, simple late-19th-century European dress in muted tones (blue-gray, dark teal,
ivory); her expression is quiet and melancholic.

Critically: render her as if Whistler himself painted her — a faint, veiled, atmospheric
figure dissolved into the same tonal blue-silver haze and loose brushstrokes, NOT a sharp
modern anime character. No crisp outlines, no cel shading, no bright saturated colours, no
glow. Her teal hair reads only as a soft cooler accent within the painting's palette. She is
a whisper in the mist — the same scale and softness as the original fisherman.

A single oil painting. No text, no added signature beyond the existing butterfly, no border,
no frame. Painterly, tonal, atmospheric, melancholic night scene. Keep the landscape aspect
ratio of the reference.
```

## Iteration 1 critique (코튼 s384)
- Figure **floats** (no reflection, sits on top of the water, too pale → reads as a vague ghost,
  teal hair not legible).
- Brushwork rougher than Whistler's smooth horizontal strokes.
- Miku lacks grace / prettiness (ambiguous smudge).
- Diagnosis: over-pushed "faint veiled" → form dissolved too far; no water-anchor instruction.

## Prompt v2 (English · GPT image-edit, Whistler reference attached)

```
Edit this painting — Whistler's "Nocturne: Blue and Silver — Chelsea" (1871). Preserve the
original painting's surface, its smooth silky horizontal brushwork, blue-silver tonal palette,
and quiet nocturnal mood EXACTLY. Keep the shoreline and its warm lights, the wide calm
Thames, the moored barge at lower-left, and the butterfly cartouche unchanged.

Add only ONE element, painted in the identical technique so it belongs completely: at the
lower-right, where the lone fisherman stands in the shallow water, a single graceful young
woman — Hatsune Miku as a quiet, lovely 19th-century presence. She stands ankle-deep at the
water's edge, and her soft reflection is mirrored in the still water directly beneath her, so
she is grounded in the scene and not floating above it. She is delicate and beautiful: a
serene, gently melancholic face, an elegant slender posture, long teal-cyan twin-tails that
read as a soft cool accent, and a plain late-19th-century dress in muted blue-gray and dark
teal.

Paint her with the same thin, smooth, blended Whistler brushstrokes and the same tonal value
as her surroundings — softly veiled in the blue-silver haze, no sharp outlines, no cel
shading, no anime look, no glow, no bright colours. She must NOT look pasted on or float above
the water; her gentle reflection anchors her to the river. She is a quiet, beautiful figure
dissolved into the mist, the same scale as the original fisherman.

A single oil painting, smooth and atmospheric. No text, no border. Keep the landscape aspect
ratio of the reference.
```

## Iteration 2 — chosen base (코튼 s384)
- Output saved: `cover/iterations/cover_v2_base_1386.png` (1386×1135). 코튼 prefers this — grounded,
  graceful profile figure at the water's edge, well tonally integrated, faint reflection present.
- Remaining gap (zoom inspection): hair reads as a **single grey veil**, not teal twin-tails →
  not recognizable as Miku. Refine **hair only**, keep everything else.

## Prompt v3 (refine — attach cover_v2_base_1386.png as the image)

```
Keep this painting exactly as it is — the same composition, the same soft tonal blue-silver
brushwork, the same standing figure in the same pose and place, the same reflection, the same
mood, and every other element completely unchanged. Make only ONE subtle refinement, to the
figure's hair.

Give the young woman long teal-cyan twin-tails — her hair gathered into two soft tails that
trail down her back and shoulder — in place of the single grey veil, so she becomes gently
recognizable as Hatsune Miku. Render the teal as a soft, cool, muted accent that sits inside
the painting's existing palette, in the same Whistler brushstrokes: veiled and atmospheric,
never bright, never anime, no sharp outlines, no glow. Keep her face serene, melancholic and
pretty. You may very gently deepen her soft reflection in the water so she stays grounded.

Do not change the composition, the dress, the pose, the water, the shoreline, the lights, the
barge, the butterfly, or the brushwork. A single oil painting, smooth and atmospheric, no
text, no border, same landscape aspect ratio.
```

## FINAL — locked (코튼 s384 · 2026-05-30)
- **`video/cover/album_1x1.png`** (1254×1254, 1:1) — confirmed cover. Whistler *Chelsea* square
  crop with Miku grounded at the lower-right water's edge (reflection present), barge lower-left,
  butterfly cartouche bottom-center. Renamed from delivered `Miku.png` to series convention
  (mozart `cover/album_1x1.png`).
- Base kept: `cover/iterations/cover_v2_base_1386.png`.
- Method = GPT image-edit on the Whistler PD reference, prompt v1→v2→v3 (hair-only refine).
