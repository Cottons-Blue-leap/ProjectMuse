# Role Taxonomy For Miku Acappella

Use roles as musical functions, not as fixed SATB choir parts.

```text
voice part = soprano / alto / tenor / bass
role       = the musical job a Miku layer performs in this piece
```

Miku-only acappella should not imitate a human choir by default. Decide what
the piece needs, then assign only the roles that help the proof sound musical.

## Core Roles

### Melody Role

The face of the piece.

Purpose:

- Carries the recognizable theme.
- Keeps Miku identity audible.
- Must work alone before support layers are added.

Typical design:

```text
voice color: Original or clearest Miku tone
syllables: Ah, Lu, or a very restrained La
mix: center, most intelligible layer
```

Reject or revise the arrangement if the melody role is not convincing by
itself.

### Bass-Function Role

The harmonic floor, not a human bass imitation.

Purpose:

- Shows root motion and harmonic direction.
- Gives the listener a sense of bottom without forcing Miku into an unnatural
  low voice.
- Anchors repeated patterns such as Canon in D's ground bass.

Typical design:

```text
voice color: Soft first, Original only as a very quiet definition layer
syllables: Oo, Uu, or Mm
register: often one octave above the historical bass line
mix: quiet, near center, never boomy
```

Do not judge this role by whether it sounds like a bass singer. Judge it by
whether the harmony feels grounded.

Do not confuse this role with a bass drum or kick part. A harmonic ground
usually starts with `Oo`, `Uu`, or `Mm`. Use `Doo/Dum` attacks only if the
ground pattern needs rhythmic definition.

### Inner Harmony Role

The body of the chord.

Purpose:

- Supplies essential 3rds, 6ths, suspensions, and color tones.
- Connects melody and bass-function roles.
- Creates acappella feeling without overcrowding the texture.

Typical design:

```text
voice color: Soft or low-level Original
syllables: Oo or Ah
mix: lower than melody, slightly off-center
```

Use fewer notes than the source if the middle register becomes cloudy.

### Doubling / Identity Role

The one-Miku-becomes-many illusion.

Purpose:

- Thickens a lead or entry without changing the arrangement.
- Makes layered Miku sound intentional instead of thin.
- Supports identity in pieces where the concept is about multiplication.

Typical design:

```text
timing: 10 to 25 ms away from the lead
pitch: 3 to 6 cents away from the lead
level: clearly below the lead
syllables: usually match the lead
```

If the double is heard as a chorus effect, it is too loud or too different.

### Air / Halo Role

The light around the sound.

Purpose:

- Adds upper shimmer, breath, and spatial lift.
- Helps long vowels feel expensive and intentional.
- Works with shared reverb instead of replacing arrangement.

Typical design:

```text
voice color: Soft, breathy, or very gentle tone
syllables: Oo or Mm
mix: wide, very quiet, often removable
```

This role should usually be felt more than heard.

### Rhythmic Articulation Role

The movement engine.

Purpose:

- Translates fast figures, ostinatos, dances, marches, and repeated gestures.
- Gives pulse when the original depends on instrumental articulation.
- Keeps playful or meme-familiar pieces from becoming static pads.

Typical design:

```text
syllables: Lu, Nu, Du, or very careful Ta
mix: lighter than melody
use: only when the piece genuinely needs motion
```

Avoid this role in the first pass unless rhythm is the piece's identity.

For instrument-like syllables, use `docs/instrument_pronunciation.md`.
Default percussion cues:

```text
bass drum / kick: 둠, 쿵 -> Dum / Doom / Bum
snare:            짝, 챡 -> Cha / Tsa / Psh
combined groove:  쿵-짝 -> Dum-Cha
```

## Decision Questions

Answer these before writing role MIDI:

1. What must the listener hear to recognize the piece?
2. What line or gesture supplies harmonic ground?
3. Which inner notes are essential, and which can be omitted?
4. Does the piece need Miku multiplication, or would doubling blur it?
5. Does the piece need air, or is silence more elegant?
6. Does the piece need rhythmic articulation, or can it breathe as sustained
   vocalise?

## Canon In D First Dogfood

For `Canon in Miku`, use the taxonomy this way:

```text
Melody role:
  first canon entries, clearest Miku identity

Bass-function role:
  D - A - B - F# - G - D - G - A as harmonic floor,
  likely one octave above the historical bass

Inner harmony role:
  only the tones needed to make the canon entries feel supported

Doubling / identity role:
  add when one Miku should feel like many Mikus

Air / halo role:
  optional, only after the dry blend works

Rhythmic articulation role:
  mostly unnecessary for the first Canon proof
```

First listen order:

```text
A. melody only
B. melody + bass-function
C. melody + bass-function + inner harmony
D. add doubling only if C works
E. add air/halo only if D still feels dry or small
```
