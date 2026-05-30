<!--
name: rights_clearance
stage: 1 · 권리 정합 게이트
type: manual
entry: works/<piece>/rights/rights-log.md 작성 (양식 = workflows/shared/templates/rights-log.md)
inputs: [works/<piece>/project.json]
outputs: [works/<piece>/rights/rights-log.md]
depends_on: [project_setup]
owner: MOKA
-->

# Rights Clearance Workflow

This workflow owns cross-workflow rights decisions.

Rights are not just a music concern. One piece may involve composition rights,
score edition rights, MusicXML reference lineage, synthesized voice output,
character or brand usage, source artwork, fonts, YouTube settings, and future
commercial transition gates.

## Main File

```text
works/<piece>/rights/rights-log.md
```

The template currently lives in:

```text
workflows/shared/templates/rights-log.md
```

## Clearance Layers

- Composition and composer death date.
- Score source and edition.
- Transcription or MusicXML reference lineage.
- Synthesized voicebank output terms.
- Character, logo, and brand usage.
- Visual source and generated-image lineage.
- Font and release packaging rights.
- YouTube license and monetization settings.

## Gate

Every workflow may continue only inside the current rights decision:

```text
approved
needs review
rejected
```

`needs review` is allowed for private dogfood only when the log names the risk,
the allowed use boundary, and the future blocker. Public release and commercial
transition should not rely on implicit or search-summary-only clearance.
