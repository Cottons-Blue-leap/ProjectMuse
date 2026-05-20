# Toolchain Notes

## Minimal Trial Chain (acappella-only path, 2026-05-11)

```text
Public-domain score
-> MusicXML
-> Python workflow scripts
-> Piapro Studio or VOCALOID6 Trial
-> WAV dry stems
-> Light assembly (V6 master / Audacity / Python wave-ffmpeg)
-> 16-bar listening proof
```

Project output lives under `works/<piece>/music/`.

## MusicXML

Use MusicXML as the workflow exchange format whenever possible. It is easier to
inspect and automate than PDF or audio.

Typical routes:

- MuseScore: import or engrave, then export MusicXML.
- Dorico/Sibelius/Finale: export MusicXML.
- Manual entry for only 16 bars is often faster than fixing poor OMR.

## Piapro Studio

Use Piapro Studio to create Miku trial renders when testing Miku V4X or Miku NT.
For larger acappella work, export one dry WAV per role.

## VOCALOID6

Use VOCALOID6 Editor for Miku V6 after purchase. The full editor is better than
Editor Lite for layered acappella because the workflow needs many vocal tracks.

## Assembly Tool (no DAW)

2026-05-11, cotton decision: the project runs on an acappella-only path. DAW-based mixing is removed.

Assembly options (cotton picks one per piece):

- V6 GUI's built-in master export — simplest if it produces an acceptable sum.
- Audacity — free, non-DAW, level matching + optional reverb.
- Python script — `wave` or `ffmpeg` for batch-style assembly.

The 6 dry stems are designed to sit together; no EQ/compression beyond level matching.

## AI

Use AI for:

- Selection critique.
- Rights log drafting.
- Music analysis interpretation.
- Arrangement planning.
- Vocal direction.
- Mix critique.

Do not use Miku output stems to train a new voice model.
