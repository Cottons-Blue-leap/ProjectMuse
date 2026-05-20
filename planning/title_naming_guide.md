# Title Naming Guide

Project Muse release titles should balance two things:

```text
respect for the source piece
VOCALOID culture and Miku-specific playfulness
```

The default title format is:

```text
Original Title (feat. Hatsune Miku)
```

Use a playful title only when the substitution is immediately understandable
and does not hide the source piece.

## Required Metadata

Every candidate row in `planning/candidate_master.csv` has three title fields:

```text
release_title
title_strategy
original_title_credit
```

Use `release_title` for YouTube title drafts, thumbnails, and album-cover text.
Use `original_title_credit` in the YouTube description and rights notes.

## Title Strategies

```text
faithful_feat
  Use the original title plus "(feat. Hatsune Miku)".

respectful_prefix
  Add Miku as a prefix without changing the original identity.

light_adaptation
  Slightly adapt the title while keeping it clear.

known_theme_adaptation
  Use a famous theme name or common nickname with source credit.

playful_substitution
  Replace one title element with Miku/queen/synth/etc.

conceptual_substitution
  Replace the title idea with a workflow or vocal-synthesis concept.

vocaloid_culture_wordplay
  Use render/synth/voicebank-style wordplay.

risky_wordplay
  Funny, but likely too cute or too obscure. Use only after review.
```

## Good Examples

```text
Canon in Miku (feat. Hatsune Miku)
after Johann Pachelbel, Canon in D

In the Hall of the Mountain Queen (feat. Hatsune Miku)
after Edvard Grieg, In the Hall of the Mountain King

Miku Song from The Tales of Hoffmann (feat. Hatsune Miku)
after Jacques Offenbach, Doll Song from The Tales of Hoffmann

Air for Miku (feat. Hatsune Miku)
after J. S. Bach, Air from Orchestral Suite No. 3
```

## Caution Examples

```text
Danse Mikuabre
```

This is memorable but pun-heavy. It may work for a seasonal or fan-facing upload,
but it may weaken a serious first release.

```text
Ballet of the Unrendered Miku
```

This is charming for VOCALOID fans, but it is too insider for a broad classical
audience.

## Rules

1. Do not imply that the altered title is the historical title.
2. Always credit the source in the description with `after Composer, Original Title`.
3. Keep `feat. Hatsune Miku` unless the title becomes too long.
4. Prefer playful titles for short experiments and fan-facing uploads.
5. Prefer faithful titles for serious first proof pieces.
6. Avoid title jokes that require technical VOCALOID knowledge for the music to
   feel valid.
7. Avoid jokes around sacred titles, memorial pieces, or culturally sensitive
   titles.

## First Release Recommendation

For the first dogfood proof, use the locked title:

```text
Canon in Miku (feat. Hatsune Miku)
```

Credit it in descriptions and rights notes as:

```text
after Johann Pachelbel, Canon in D
```

Gymnopedie No. 1 remains a strong later tone-first release, but it is no longer
the first dogfood title.
