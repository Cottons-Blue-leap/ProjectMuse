# World-Loved Classics Validation

This file checks famous classical pieces against the Project Muse question:

```text
Can this world-loved classic become a listenable Miku-centered acappella proof?
```

Recognition alone is not enough. Some world-famous pieces are poor first tests
because they depend on orchestration, piano resonance, religious meaning, or
copyright-sensitive modern sources.

## Source Signals Used

These sources are popularity/reference signals, not final rights proof:

- Classic FM Hall of Fame is described by Classic FM as the world's biggest
  classical music chart.
- Classic FM Hall of Fame 2026 notes its Top 300 and Top 10 public voting
  results.
- Classical California Ultimate 101 (2025) gives another contemporary public
  radio popularity snapshot.
- BBC Music Magazine's "famous classical music moments" article is useful for
  identifying excerpts whose themes are famous outside their larger works.

Use these sources to find "world-loved" candidates. Use `rights-log.md` to
verify any actual release source.

Manage all candidate rows in:

- `planning/candidate_master.csv`

## Validation Key

```text
Green:
  worth a 16-bar Miku acappella proof soon

Yellow:
  famous, but arrangement or tone risk is high

Red:
  do not use for the first proof
```

## Green Candidates

These combine recognition with plausible Miku/acappella fit.

| Priority | Piece | Composer | Why It Is Famous | Why It Might Work | Main Risk | Test Section |
|---:|---|---|---|---|---|---|
| 1 | Canon in D | Johann Pachelbel | Ubiquitous wedding/pop culture classic; appears in popularity lists. | One voice becoming many voices matches the project perfectly. | Can feel too familiar or like a demo. | Opening ground and first canon entries. |
| 2 | Gymnopedie No. 1 | Erik Satie | Frequently listed and recognizable; Classical California lists Satie's Gymnopedies. | Sparse, secular, transparent, and close to the "first sound" concept. | Thin sustain can expose Miku. | First 16 bars. |
| 3 | Air from Orchestral Suite No. 3 | J. S. Bach | BBC Music Magazine highlights the famous "Air" as a widely loved classical moment. | Long lyrical melody over slow support is ideal for vocalise. | Too much warmth is expected from the melody. | Main theme, slow `Ah` lead with `Oo` supports. |
| 4 | Largo from New World Symphony | Antonin Dvorak | Classical California ranks Dvorak's New World Symphony very high. | The "Going Home" melody is song-like and can survive acappella reduction. | Low register and orchestral breadth may be hard. | Main Largo theme in a Miku-comfortable key. |
| 5 | Nimrod from Enigma Variations | Edward Elgar | Elgar's Enigma Variations appears high in popularity charts; Nimrod is deeply familiar. | Chorale-like, slow, and naturally suited to layered voices. | It can become too solemn and heavy for Miku-only. | First build, very soft `Oo/Ah` layers. |
| 6 | Brahms Lullaby | Johannes Brahms | One of the most globally recognized melodies. | Simple, secular-feeling, intimate, and suited to `Lu/Oo`. | Can become childish if not treated elegantly. | One verse as wordless lullaby. |
| 7 | The Swan | Camille Saint-Saens | Widely recognized; Classical California lists it from Carnival of the Animals. | Strong lyrical line for Miku solo plus pads. | Miku may lack cello warmth. | Main theme only. |
| 8 | Vocalise, Op. 34 No. 14 | Sergei Rachmaninoff | Classical California lists Vocalise; conceptually already wordless voice. | Perfect concept match: voice before words. | Needs emotional warmth and long-line control. | First phrase, transposed if needed. |

## Yellow Candidates

These are famous, but not clean first tests.

| Piece | Composer | Why It Is Tempting | Why It Is Risky | Possible Use |
|---|---|---|---|---|
| Clair de lune | Claude Debussy | Extremely recognizable and visually perfect for the project. | Piano color and harmonic haze are hard to translate. | Test after Satie if the Miku tone works. |
| Moonlight Sonata, I | Ludwig van Beethoven | Famous, slow, and atmospheric. | The arpeggiated piano texture can become mechanical as vocals. | Use only the top melodic contour and harmonic pads. |
| Ode to Joy | Ludwig van Beethoven | Universally known and easy. | Too simple; can sound like an exercise. | Workflow smoke test, not first artistic proof. |
| Vivaldi Spring | Antonio Vivaldi | One of the most recognizable classical openings. | Fast string figuration fights vocal acappella. | Use a very short rhythmic `La/Ta` study. |
| Swan Lake Theme | Pyotr Ilyich Tchaikovsky | Dramatic and globally known. | Orchestral drama may not survive Miku-only. | Later, with darker sound design. |
| Morning Mood | Edvard Grieg | Clear image and familiar melody. | It may feel more instrumental than vocal. | Good video concept, moderate music risk. |
| Flower Duet from Lakme | Leo Delibes | Already vocal, famous, and beautiful. | Duet identity may push away from Miku-only acappella. | Use later when adding another vocal color. |
| Habanera from Carmen | Georges Bizet | Extremely recognizable vocal classic. | Character, rhythm, and sensuality may clash with Miku tone. | Only if intentionally stylized. |
| Rachmaninoff Piano Concerto No. 2 theme | Sergei Rachmaninoff | Very loved; appears high in Classic FM 2026. | Piano/orchestra texture and romantic weight are demanding. | Extract a slow melody after Vocalise succeeds. |
| Mozart Eine kleine Nachtmusik | W. A. Mozart | Instantly recognizable. | Strongly instrumental; risks sounding novelty-like. | Short proof only, not main first piece. |
| Bach Cello Suite No. 1 Prelude | J. S. Bach | Iconic and public-domain friendly. | Continuous arpeggios are not naturally vocal. | Convert to harmonic pulses, not literal notes. |

## Red Candidates For The First Proof

These may be loved, but they are bad first tests for this specific project.

| Piece | Composer | Reason To Avoid First |
|---|---|---|
| The Armed Man: A Mass for Peace | Karl Jenkins | Classic FM 2026 No.1, but modern copyright and religious/choral identity make it unsuitable. |
| O Fortuna from Carmina Burana | Carl Orff | Famous, but copyright and huge choral/orchestral force make it unsuitable. |
| Adagio for Strings | Samuel Barber | Famous, but modern copyright and string-orchestra identity are poor first-test fit. |
| Appalachian Spring | Aaron Copland | Loved, but modern copyright and orchestral identity create avoidable risk. |
| The Lark Ascending | Ralph Vaughan Williams | Beloved, but violin tone and rights/source complexity make it a later-stage candidate. |
| Allegri Miserere | Gregorio Allegri | Acappella and famous, but strongly religious and already a sacred-choir benchmark. |
| Handel Hallelujah Chorus | G. F. Handel | Choral and famous, but religious and too strongly associated with text. |
| Schubert Ave Maria | Franz Schubert | Beautiful and famous, but religious color conflicts with the current first-piece direction. |
| Ravel Bolero | Maurice Ravel | Very famous, but repetitive orchestration is the core; not a good Miku acappella proof. |
| Film scores by living/recent composers | Various | Popular, but copyright/licensing risk is high and unnecessary for the first proof. |

## Revised Top 5 For Project Muse

If we include world-loved classics, the first dogfood is now locked as Canon in
D. The revised test order is:

```text
1. Pachelbel - Canon in D
   layering-first, one Miku becoming many voices

2. Bach - Air from Orchestral Suite No. 3
   melody-first, vocal-line proof

3. Satie - Gymnopedie No. 1
   concept-first, tone-first backup

4. Dvorak - New World Symphony, II Largo
   universally loved melody, strong emotional proof

5. Elgar - Nimrod
   chorale-like blend proof
```

This is slightly different from the earlier shortlist. The earlier list was
more concept-led; this one is more audience-recognition-led.

## First Listening Batch

Run the first Canon dogfood as three tiny 16-bar renders:

```text
A. lead_miku only
B. lead_miku + mid_oo + low_oo
C. lead_miku + lead_double + halo_high + mid_oo + low_oo
```

Judge with one brutal question:

```text
Would a listener keep listening even if they did not care about VOCALOID?
```

If yes, the project has legs. If no, the concept is not enough yet.
