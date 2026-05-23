# Thumbnail Guide — v4 (Atelier Miku Acappella)

> Locked s348 (2026-05-23, 코튼). The thumbnail is a **separate marketing surface** from the
> in-video visualizer — optimized for click-through, not a copy of the video frame.

## Why v4 (the CTR diagnosis)

The old thumbnails were just the video's visualizer frame: a small 1:1 painting centered with
~55% empty letterbox, Miku nearly invisible inside the painting, thin low-contrast text. Joplin's
live CTR was ~0.5% (typical 2–10%) — impressions arrive but the thumbnail doesn't convert clicks.
Miku is the channel's #1 hook (Vocaloid audience) yet wasn't visible at feed scale.

## The v4 format

```text
- Fill the frame with the cover (no letterbox).
- Zoom (crop) so Miku is the clear subject — shown through the IMAGE, no inset, no "Hatsune Miku" label.
  ("썸네일은 그림으로 말한다" — Miku is the identity; she shouldn't need a text label.)
- Bottom-left title block: Composer (small) / Piece (large) / Atelier Miku Acappella wordmark.
- Bottom gradient scrim for text legibility.
- 1280×720 JPG.
```

### Text spacing (mandatory)

Stack the title block from the bottom using **measured ink bounding boxes that include descenders**
(p, é, g, comma…), not nominal font size — otherwise the title's descenders collide with the
wordmark. This is the standard going forward (코튼 s348). The tool does this automatically
(`textbbox` + fixed gaps).

## Per-song variable: the crop `box`

The one per-song tuning is the crop region (`box = x0,y0,x1,y1` in 0–1 of the cover) that frames
Miku as the subject. Pick it by viewing the cover:

- Keep Miku's **head/face + teal hair** in frame (her recognizable features). A crop that cuts the
  head reads as an anonymous figure (the Vivaldi first-pass mistake — fixed).
- Box aspect close to 16:9 crops least; a tall box over-zooms and cuts heads/feet.

### Registry (current catalog)

| song | box (x0,y0,x1,y1) | note |
|---|---|---|
| Gymnopédie | 0.16, 0.26, 0.98, 0.99 | exception — Whistler nocturne, Miku is a dark veiled figure; moody, weakest Miku hook |
| Vivaldi Spring | 0.21, 0.22, 0.93, 0.62 | Miku (teal) among Primavera figures, head-to-thigh |
| Joplin | 0.16, 0.00, 1.00, 0.52 | Miku dancing on the upper stage |
| Salut d'Amour | 0.00, 0.04, 1.00, 0.80 | Miku is already the cover subject — minimal crop |

## Workflow

```text
1. python workflows/video_release/make_thumbnail.py --song <name>
     → works/<song>/video/thumbnail_v4.jpg
   (or ad-hoc: --cover <path> --box x0,y0,x1,y1 --composer "..." --piece "..." --out <path>)
2. Review at feed scale (does "it's Miku" read instantly? title legible? no overlap?).
3. Upload: python Analytics/youtube_meta.py set-thumbnail <video_id> <thumbnail_v4.jpg>
     (thumbnails.set — swaps only the thumbnail image; does NOT touch the video, title, or schedule.)
```

## Open

- Gymnopédie's Miku isn't recognizable even zoomed (by the nocturne's design). If we want a stronger
  Miku hook there, it needs a re-composited cover (image-gen) — deferred, 코튼's call.
