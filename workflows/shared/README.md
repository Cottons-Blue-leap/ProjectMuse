# Shared Workflow Assets

This folder contains shared templates and schemas used by multiple workflows.
It should not own process logic.

Current shared asset:

```text
templates/rights-log.md
```

Use shared templates for common artifacts. Workflow ownership lives elsewhere:

- rights decisions: `workflows/rights_clearance`
- project workspace setup: `workflows/project_setup`
- V6 entry reference (role + 음절 + polishing): `workflows/music_acappella`
- audio render/mix: `workflows/audio_production`
- video package: `workflows/video_release`

PDF score는 별 워크플로우 없음 — `planning/candidates_opus/`에 모여있고 V6 진입 시점 직접 reference (s302 후속 cut · score_ingestion 워크플로우 폐기 통과).

Use shared templates for anything that crosses workflow boundaries:

- rights notes
- release metadata
- source attribution
- project-level schemas
