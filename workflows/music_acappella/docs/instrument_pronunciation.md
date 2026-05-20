# Instrument Pronunciation Map

Use syllables as orchestration. This map keeps instrument imitation consistent
across pieces without forcing every piece into vocal percussion.

## Two-Layer Rule

Keep two labels separate:

```text
planning cue  = Korean mnemonic for the arranger
render syllable = practical vowel/consonant to try in V6/Piapro
```

Example:

```text
planning cue: 둠
render syllable: Dum / Doo / Bum
```

Hatsune Miku may not render Korean syllables naturally. Use Korean as the
musical memory aid, then choose a V6-friendly syllable or phoneme when rendering.

## First-Proof Boundary

For the Canon dogfood, do not add a drum-kit layer. Canon's `low_oo` is a
bass-function role, not a bass drum role.

Use:

```text
lead_miku  -> Ah / Lu
mid_oo     -> Oo / Uu
low_oo     -> Oo / Uu / Mm
```

Only test `Doo/Dum` attacks on the low role if the ground pattern is unclear
after the plain vowel render.

## Core Map

| Source function | Planning cue | Primary render syllables | Backup syllables | Use when | Avoid when |
|---|---|---|---|---|---|
| Lead melody, vocal line | 아 / 루 | Ah / Lu | La | melody must sing clearly | fast articulation exposes artifacts |
| Bowed strings, legato line | 루 / 우 | Lu / Loo / Oo | Ah | long connected phrase | consonant attacks become too audible |
| Pizzicato or light staccato | 둣 / 뽑 | Doot / Dit / Bop | Dop | short plucked gestures | phrase should remain lyrical |
| Woodwind soft inner line | 우 / 오 | Oo / Uu | Nu / Lu | smooth support or counterline | middle register clouds the lead |
| Brass stab or fanfare | 다 / 바 | Dah / Bah / Dow | Dwe | strong attack is the identity | classical dignity would become comic |
| Bass-function, ground/root | 우 / 음 | Oo / Uu / Mm | Doo | harmony needs a floor | it starts sounding like fake bass |
| Bass drum / kick / timpani | 둠 / 쿵 | Dum / Doom / Bum | Buh / Puh | actual percussion or pulse is needed | source bass is only harmonic |
| Snare accent | 짝 / 챡 | Cha / Chak / Tsa | Ksh / Psh | march, dance, or backbeat needs snap | piece should stay chamber-like |
| Hi-hat or light tick | 츠 / 틋 | Tsu / Ts / T | Ch | subdivision must be audible | it adds noisy fizz |
| Cymbal or shimmer | 쉬 / 스 | Shh / Sss | Hh | transition or halo effect | it distracts from Miku identity |
| Air / halo / glue | 음 / 흠 | Mm / Hm / Oo | Ah very soft | texture needs width or breath | dry blend is already cloudy |

## Bass And Snare Decision

The user's instinct is right: standardize the low pulse and snare-like accent.
Use this convention:

```text
Bass drum / kick:
  cue: 둠 or 쿵
  render: Dum / Doom / Bum

Snare:
  cue: 짝 or 챡
  render: Cha / Chak / Tsa / Psh

Combined groove:
  cue: 쿵-짝
  render: Dum-Cha or Bum-Tsa
```

Do not label snare alone as `쿵`; that makes the low hit and the sharp hit blur
inside the arrangement. `쿵짝` is useful as a combined groove mnemonic.

## Arrangement Use

When deciding syllables inside V6 (편곡 결단이 V6 안에서 박히는 path), add a syllable choice only if it serves
one of these jobs:

- Recognition: the source gesture becomes easier to identify.
- Texture: the layer reads as vocal orchestration, not generic pad.
- Articulation: a rhythmic figure becomes clear without adding instruments.
- Restraint: removing the syllable would make the piece more beautiful.

If the last answer is yes, remove the syllable.

## Render Notes

- Keep one vowel per phrase unless articulation is musically necessary.
- Prefer vowels for first proof; add consonants only after the line works.
- Use consonants as attack color, not as permanent texture.
- Keep support roles quieter and simpler than the lead.
- If a syllable feels clever before it feels musical, simplify it.

