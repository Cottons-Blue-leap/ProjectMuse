# Thumbnail Guide — v5 (Atelier Miku Acappella)

> Locked s357 (2026-05-25, 코튼). The thumbnail is a **separate marketing surface** from the
> in-video visualizer — optimized for *recognition at feed scale*, not a copy of the video frame.
> Supersedes v4 (wordmark / mint two-line / top badge). v4 files kept for rollback (not overwritten).

## Why v5 (the recognition diagnosis)

v4 carried only **English** text (Composer / Piece / "Atelier Miku Acappella" wordmark). But:
- A scrolling **Japanese Vocaloid fan** — our biggest untapped audience — sees no `初音ミク` and may
  not register it as Miku content at a glance.
- YouTube shows **one global thumbnail** (thumbnails are *not* localized per viewer), so that
  all-English surface reaches everyone, including Japan.

v5 fixes this: it states the channel's three pieces of information explicitly, with `初音ミク` (the
recognition hook) in Japanese. Goal = "in 1 second on a small screen, this reads as *Miku · a cappella ·
classical*", without becoming a loud clickbait thumbnail (that would betray the 정제미 / no-AI identity
and likely backfire with this taste-driven, AI-sensitive audience).

## The three pieces of information (코튼's spec)

1. **명화 커버 배경** (painting) — ① identity/mood, no text.
2. **악곡 정보** (piece · composer) — ②.
3. **미쿠가 A Cappella한 곡** (初音ミク + A CAPPELLA) — ③, the channel differentiator.

## The v5 format

```text
初音ミク                          ← Yu Mincho (明朝 serif) · IVORY  (③ JP recognition)
A CAPPELLA                       ← Didot CAPS, letter-spaced · MINT (③ format; EN caps = reads
                                    faster small + international; mint = brand accent only)
Salut d'Amour · Edward Elgar     ← Didot · piece (large, WHITE) · middot · composer (small, DIM)
                                    (② — one line, baseline-aligned)
```

- **Single bottom-left block** (all text in one zone → gaze lands once; the painting/Miku breathe upper-right).
- **Serif harmony**: Japanese Mincho + Latin Didot share a refined high-contrast serif feel (a bold
  gothic clashed — rejected). Light weight, not heavy.
- **Backing = gradient scrim** (no hard label box). The scrim guarantees legibility on any painting
  (dark nocturne → bright Botticelli all tested) while keeping the album-cover aesthetic.
- **Colors**: `初音ミク` IVORY (not mint — mint blended into Miku's hair/background); MINT reserved as
  the `A CAPPELLA` accent so the brand color stays without garishness.
- **1280×720 JPG.**

### Fixed sizes & spacing (LOCK — do not change per song)

| element | font | size | color |
|---|---|--:|---|
| 初音ミク | Yu Mincho | 108 | ivory (245,243,235) |
| A CAPPELLA | Didot (caps, track 8) | 60 | mint (139,223,206) |
| piece | Didot | 92 | white |
| `·` middot | Didot | 44 | dim (196,192,178) |
| composer | Didot | 36 | dim |

- **Vertical = baseline-anchored** (font metrics, constant per size) so positions are **pixel-identical
  across every song**, regardless of the title's letters/descenders. Constants: piece baseline = `H − 44`
  (`BASE_MARGIN`); A CAPPELLA baseline = `−98` above (`LEAD_TITLE`); 初音ミク baseline = `−69` above that
  (`LEAD_BADGE`). Each line drawn at `y = baseline − font.ascent`.
  - ⚠ **Do NOT anchor to per-string ink bboxes** (the v4 method). Ink boxes include descenders (g/y/p/，)
    that differ per title, so absolute positions drift ~15–20px between songs — wrong for a series.
    Caught s357 (코튼). Descenders simply extend below the shared baseline, consistently.
- **Left visual alignment**: each line drawn at `x = LEFT(72) − ink left side-bearing` (`bbox[0]`) so the
  left edges line up optically across scripts (this *is* per-string, and correct — it aligns the visual
  left edge).
- **Inline title baseline-aligned**: piece + `·` + composer share the piece baseline (mixed sizes).

## Per-song variable: the crop `box`

The only per-song tuning is the crop region (`box = x0,y0,x1,y1` in 0–1 of the cover) that frames Miku
as the subject. Pick it by viewing the cover. Keep Miku's **head/face + teal hair** in frame; a box near
16:9 crops least.

| song | box (x0,y0,x1,y1) | note |
|---|---|---|
| Gymnopédie | 0.16, 0.26, 0.98, 0.99 | Whistler nocturne; Miku is a faint veiled figure — here the `初音ミク` text carries the recognition |
| Vivaldi Spring | 0.21, 0.22, 0.93, 0.62 | Miku (teal) among Primavera figures |
| Joplin | 0.16, 0.00, 1.00, 0.52 | Miku dancing on the upper stage |
| Salut d'Amour | 0.00, 0.04, 1.00, 0.80 | Miku is already the cover subject — minimal crop |

## Font dependency

`初音ミク` uses **Yu Mincho Regular** (`C:\Windows\Fonts\yumin.ttf`), a Windows system font — *not*
bundled in the repo (Microsoft license). On another machine, point `JP_MINCHO` in `scripts/muse_thumbnail.py`
to any Mincho `.ttf/.ttc`. GFS Didot ships in `assets/fonts/`.

## Workflow

```text
1. Generate:
     python workflows/video_release/scripts/muse_thumbnail.py --all          # all 4 in the registry
     python workflows/video_release/scripts/muse_thumbnail.py --song <name>  # one
     (ad-hoc new song: --cover <path> --box x0,y0,x1,y1 --composer "..." --piece "..." --out <path>)
     → works/<song>/video/thumbnail_v5.jpg
2. Review at feed scale (shrink to ~210px wide): does 初音ミク read? title legible? block balanced?
3. Upload (live, swaps only the image — video/title/schedule untouched):
     python Analytics/youtube_meta.py set-thumbnail <video_id> <thumbnail_v5.jpg>
```

New song checklist: add it to `REGISTRY` (dir/cover/box/composer/piece) → `--song` → review small →
upload. The tool warns if the inline `piece · composer` line overflows the width (sizes are locked, so
that signals shortening the displayed piece name or re-checking the box, not shrinking text).

## Open

- Gymnopédie's Miku isn't recognizable even zoomed (by the nocturne's design); the `初音ミク` text now
  covers recognition there. A stronger Miku hook would need a re-composited cover (image-gen) — deferred.
- *Elegant vs punchy* is an intuition bet: at our scale CTR can't be cleanly attributed to the thumbnail.
  v5 is the considered bet (elegant + clearly Miku); measure via Studio 도달범위 after it's lived a while.
