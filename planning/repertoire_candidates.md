# Repertoire Candidates

This is separate from the production workflows. It is a repertoire board: a
place to decide what is worth testing before creating a full work project under
`works/`.

For a broader audience-recognition pass, see:

- `planning/world_loved_classics_validation.md`

Manage all candidate rows in:

- `planning/candidate_master.csv`

For release-title rules, see:

- `planning/title_naming_guide.md`

The first proof should answer one question:

```text
Can this piece sound beautiful with Miku-centered acappella before the concept
has to explain itself?
```

## Selection Rules

Use these rules before committing to a 16-bar prototype:

1. Prefer public-domain compositions and public-domain source scores.
2. Prefer a famous melody or instantly clear musical identity.
3. Prefer slow or moderate music where Miku's tone can be shaped.
4. Avoid pieces whose beauty depends mainly on orchestration or piano resonance.
5. Avoid dense textures for the first test unless the melody can be extracted.
6. Use the same 16-bar test method across candidates.
7. Treat rights status here as preliminary; verify it again in `rights-log.md`.

## Immediate Test Tier

These are the strongest first-test candidates.

| Rank | Piece | Composer | Why It Fits | Main Risk | Suggested Test |
|---:|---|---|---|---|---|
| 1 | Canon in D | Johann Pachelbel | The canon structure naturally shows one voice becoming many voices. Excellent for Miku-only layering and the first dogfood identity. | Overfamiliar and can feel like a technical demo. | Opening ground bass and first entries. Build from solo to 3-4 layers. |
| 2 | Gymnopedie No. 1 | Erik Satie | Sparse, non-religious, iconic, and close to the "first beautiful sound" idea. Miku's transparent tone may become a feature. | It can sound thin or emotionally flat if the sustain is not beautiful. | Keep as the strongest tone-first backup after Canon. |
| 3 | Prelude in C Major, BWV 846 | J. S. Bach | Pure harmonic movement, very recognizable to classical listeners, strong public-domain safety. | Arpeggios can become mechanical if translated too literally. | Convert broken chords into sustained `Oo/Ah` harmonic pulses. |
| 4 | The Swan | Camille Saint-Saens | A lyrical line that can work as Miku solo first, then supported by quiet vocal pads. | The cello-like warmth may expose Miku's thinness. | Main theme only. Keep support very soft. |
| 5 | Vocalise, Op. 34 No. 14 | Sergei Rachmaninoff | Originally wordless voice, conceptually perfect for "voice as sound." | Very expressive and wide; may demand more warmth than Miku can provide. | First phrase at a comfortable key; test solo before layers. |
| 6 | Clair de lune | Claude Debussy | Moonlit, transparent, and highly compatible with a painterly visual identity. | Harmonic nuance and piano texture are hard to preserve in acappella. | Opening phrase only; simplify aggressively. |

## Secondary Tier

Use these after the first proof shows the concept can work.

| Piece | Composer | Why It Might Work | Risk |
|---|---|---|---|
| Nocturne in E-flat Major, Op. 9 No. 2 | Frederic Chopin | Famous singing melody, strong emotional pull. | Ornamentation and rubato can become awkward in Miku. |
| Traumerei | Robert Schumann | Gentle, short, intimate, and lyrical. | May become too small unless the sound design is excellent. |
| Ode to Joy | Ludwig van Beethoven | Extremely recognizable and easy to test. | Too simple and overused; weak first-piece symbolism. |
| Swan Lake Theme | Pyotr Ilyich Tchaikovsky | Dramatic, famous, and visually strong. | Orchestral drama may not translate to Miku-only acappella. |
| Salut d'Amour | Edward Elgar | Warm, secular, and welcoming as a "first greeting." | Sentimental tone may fight Miku's artificial clarity. |
| Morning Mood | Edvard Grieg | Clear sunrise image and simple melodic identity. | May feel more instrumental than vocal. |
| Pavane, Op. 50 | Gabriel Faure | Elegant, restrained, and choral-adjacent. | The best-known color often comes from orchestral/choral versions. |
| Song to the Moon | Antonin Dvorak | Vocal origin, moon imagery, strong melody. | Text/aria identity may pull away from pure vocalise. |
| Ah! vous dirai-je, maman | W. A. Mozart | "First song" symbolism and broad recognition. | Can sound childish unless arranged with real taste. |

## Current Recommendation

The first dogfood is locked:

```text
Pachelbel - Canon in D
release title: Canon in Miku (feat. Hatsune Miku)
test section: opening ground bass and first canon entries, 16 bars
reason: best proof of one Miku becoming many voices
```

Gymnopedie No. 1 remains the strongest tone-first backup, but it is no longer
the first dogfood. Only continue Canon to a 60-90 second proof if the 16-bar
test passes the listening test:

```text
Does it sound beautiful before it sounds clever?
```

## Source Leads

Use these as starting points for rights/source verification. Do not skip the
work-project `rights-log.md`.

- IMSLP public-domain guide: https://imslp.org/wiki/Public_Domain
- Satie, 3 Gymnopedies: https://imslp.org/wiki/3_Gymnop%C3%A9dies_(Satie,_Erik)
- Pachelbel, Canon and Gigue: https://imslp.org/wiki/Canon_and_Gigue_in_D_major_(Pachelbel,_Johann)
- Bach, Well-Tempered Clavier I: https://imslp.org/wiki/Das_wohltemperierte_Klavier_I,_BWV_846-869_(Bach,_Johann_Sebastian)
- Saint-Saens, The Carnival of the Animals: https://imslp.org/wiki/Le_carnaval_des_animaux_(Saint-Sa%C3%ABns,_Camille)
- Debussy, Suite bergamasque: https://imslp.org/wiki/Suite_bergamasque_(Debussy,_Claude)
- Rachmaninoff, 14 Romances Op. 34: https://imslp.org/wiki/14_Romances,_Op.34_(Rachmaninoff,_Sergei)

## Notes For The First Listening Session

For each candidate, make the same three renders:

```text
A. lead_miku only
B. lead_miku + mid_oo + low_oo
C. lead_miku + lead_double + halo_high + mid_oo + low_oo
```

Score each render on:

- beauty
- Miku identity
- acappella feeling
- classical dignity
- repeat-listen desire
- "worth buying tools for?"

If none of the three immediate candidates pass, the project should change
musical direction before buying Miku V6 Starter Pack.
