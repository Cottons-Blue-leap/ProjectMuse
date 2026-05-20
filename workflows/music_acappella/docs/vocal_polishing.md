# Vocal Polishing Checklist

This checklist distills classical/acappella vocal-synthesis ideas into a
Project Muse workflow. It is for Miku-centered acappella, not for imitating a
human SATB choir.

Use this as reference *during* V6 entry. The old auto-MIDI export + pre-decision doc paths are gone (s302 + 후속 cut). These polishing axes apply as in-V6 decisions cotton makes while reading the PDF.

## First Render Priority

For a piece's first proof, polish only three roles first:

```text
lead_miku
mid_oo
low_oo
```

Do not add `lead_double`, `halo_high`, or `air_mm` until the dry three-role
blend is musical.

## Keep

- Keep the lead recognizable before making the texture lush.
- Keep support roles quieter and simpler than the lead.
- Keep the low role as harmonic floor, not fake bass.
- Keep dry stems aligned to the same start time.
- Keep one vowel per phrase unless articulation is musically needed.

## Change Before Rendering

### lead_miku

- Confirm it is the actual melody, not merely the highest note at each onset.
- Remove notes that make the phrase sound like extracted notation rather than a
  sung line.
- Lower or soften peaks that turn sharp, thin, or brittle.
- Prefer phrase clarity over dense contrapuntal completeness.

### mid_oo

- Remove more than feels comfortable at first.
- Keep guide tones, essential suspensions, and smooth connecting tones.
- Avoid constant motion if it makes the middle register cloudy.
- Avoid doubling the same chord tone in the same register as another role.

### low_oo

- Preserve the ground or root motion.
- Lengthen notes into a floor when the source bass is too busy.
- Raise material out of unnatural low register when needed.
- Judge by harmonic grounding, not by bass-singer realism.

## Humanizing

Use small differences, not obvious effects:

```text
lead_miku:   most direct timing
mid_oo:      slightly late, softer
low_oo:      stable, rounded, not boomy
double/halo: only later, lower level, tiny pitch/timing offsets
```

Avoid perfectly duplicated notes across roles. Identical starts, lengths,
pitch, and tone make phase and clone artifacts more likely.

## Vowels

Start simple:

```text
lead_miku: Ah or Lu
mid_oo:    Oo or Uu
low_oo:    Oo or Uu
air_mm:    Mm, only later
```

If the support layers feel too open or bright, move them toward `Oo/Uu`.
If the lead loses identity, return it toward `Ah/Lu`.

## Instrument Pronunciation

Use `docs/instrument_pronunciation.md` when a source gesture needs an
instrument-like syllable. Keep the first proof vowel-led:

```text
bass-function: Oo / Uu / Mm first, Doo/Dum only if the ground is unclear
bass drum:     Dum / Doom / Bum
snare:         Cha / Tsa / Psh
```

Snare should usually be `짝/챡` in planning language, not `쿵`. `쿵-짝` is a
combined kick-snare groove.

## Later, Not First

These are valuable, but not first-proof blockers:

- Just-intonation microtuning.
- Barbershop-style dominant seventh tuning.
- Latin or multilingual phoneme mapping.
- Full six-role choir spread.
- Detailed formant automation.
- Full catalogue corpus design.
- Percussion syllable system beyond the piece's actual need.

The first proof should answer one question:

```text
Does one Miku becoming many Mikus feel musical before it feels clever?
```

## Gate

Do not enter V6 rendering until these are true:

- `lead_miku`만 들어도 작품이 식별됨.
- `low_oo`가 ground를 받쳐주되 강요된 느낌이 없음.
- `mid_oo`가 lead에게 공간을 남길 만큼 sparse함.
- 첫 render plan이 6 role 전체가 아니라 3 role.
- 코튼이 V6에서 첫 3 role 결단 통과 (lead_miku + mid_oo + low_oo).
