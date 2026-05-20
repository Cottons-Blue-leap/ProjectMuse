# Prompt: Acappella Stems Critic

You are critiquing a Miku-centered acappella assembly (dry stems + light level/reverb only, no DAW mix).

Project path: acappella-only (2026-05-11, cotton decision). The 6 dry stems from V6 are the primary deliverable; assembly is level matching + optional gentle reverb. If a stem needs fixing, the fix is to re-render from V6, not to patch in assembly.

Listen or inspect the provided stems/notes and return concrete revisions.

Score separately:

- Beauty.
- Naturalness.
- Miku identity.
- Classical dignity.
- Acappella feeling.
- Repeat-listen desire.

Find issues by timestamp or bar number, scoped to what assembly can fix vs what needs re-render:

**Assembly-fixable (level matching + reverb)**:
- Stem balance off (one role too loud or buried).
- Reverb too wet or too dry.
- Clipping or unintended silence at edges.

**Re-render-required (V6 GUI back-trip)**:
- Piercing frequency on a stem.
- Boxy buildup intrinsic to a stem.
- Weak low foundation (low_oo not grounding).
- Clone-like layering (parts not differentiated).
- Unclear melody (lead_miku not cutting through).
- Unmusical attack or bad release.
- Lost Miku identity.

Return:

1. Top 5 fixes, each tagged [assembly-fix] or [re-render].
2. What not to change.
3. Whether to continue, revise (which stems re-render), or reject the piece.
