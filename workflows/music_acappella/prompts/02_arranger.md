# Prompt: Acappella Arranger

You are arranging a public-domain classical score section for Miku-only
acappella proof.

Rules:

- No instrumental audio.
- Miku identity must remain audible.
- Do not overfill the texture.
- Use mostly Ah, Oo, Mm, and Lu.
- Treat low parts as harmonic foundation hints, not human bass imitation.
- Preserve the recognizable melody.
- Use roles as musical functions, not fixed SATB parts.
- Omit roles that the piece does not need.

Inputs:

- Source PDF (`planning/candidates_opus/<곡>.pdf`).
- Role taxonomy guide (`docs/role_taxonomy.md`).
- Target section.
- Miku role ranges.

Return:

1. Arrangement thesis: what should survive when the score becomes Miku-only acappella.
2. Non-negotiable identity: melody, bass pattern, harmonic rhythm, signature gestures.
3. Omission plan: notes, lines, registers, or continuo material to remove.
4. Register plan: source range, target vocal range, and octave rules.
5. Bar-by-bar texture plan.
6. Syllable map.
7. Role handoff decisions:
   - Melody.
   - Bass-function.
   - Inner harmony.
   - Doubling / identity.
   - Air / halo.
   - Rhythmic articulation.
8. A 16-bar first-pass arrangement plan.
9. A second-pass expansion plan.
10. A first render order from sparse to fuller texture.

Write the output as cotton's own in-head decision notes — not as a doc to persist. The s302 workflow (+ 후속 cut) keeps all arrangement / role / syllable decisions in-V6; the only artifacts that land are the V6 piano-roll entries themselves and the dry stem WAVs.
