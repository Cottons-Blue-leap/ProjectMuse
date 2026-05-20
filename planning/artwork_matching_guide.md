# Artwork Matching Guide

Each row in `planning/candidate_master.csv` has one artwork match for visual
planning.

## Artwork Columns

```text
artwork_title
artwork_artist
artwork_year
artwork_source_lead
artwork_rights_note
artwork_match_reason
```

`artwork_source_lead` is a starting point, not a final source. Before making a
thumbnail or album-cover image, open the link, find a high-quality source image,
and verify the image license.

## Rights Rule

The matched artworks are chosen as likely public-domain classical paintings or
historical artworks. Still, do not treat the CSV as legal clearance.

Before release, record the actual image source in:

```text
works/<piece>/video/art_sources/source-image-url.txt
works/<piece>/video/art_sources/source-rights-notes.md
works/<piece>/rights/rights-log.md
```

Prefer sources from:

- museum open-access collections
- Wikimedia Commons pages with clear public-domain status
- Art Institute of Chicago Open Access
- The Met Open Access
- Rijksmuseum public-domain or CC0 records

## Matching Philosophy

The artwork does not need to literally illustrate the piece. It should give the
video a first-frame emotional identity:

```text
music mood
VOCALOID title language
public-domain visual source
thumbnail readability
```

For playful releases, a witty artwork can work. For serious first proofs, prefer
quiet and dignified images.

## Examples

```text
In the Hall of the Mountain King
-> The Mountain Troll, Theodor Kittelsen
-> supports "In the Hall of the Mountain Queen"

Doll Song from The Tales of Hoffmann
-> Young Girl with a Doll, Henri Rousseau
-> supports the mechanical singer / doll concept

Gymnopedie No. 1
-> The Monk by the Sea, Caspar David Friedrich
-> supports sparse space and solitude
```

## Image-To-Image Use

When using image-to-image generation:

1. Keep the source painting recognizable in mood, not necessarily exact layout.
2. Integrate the Vocaloid character into the painting's light and palette.
3. Do not use official character art unless the release use is permitted.
4. Keep text and face areas clear for thumbnail readability.
5. Save the generated image prompt and model/tool notes in the work folder.
