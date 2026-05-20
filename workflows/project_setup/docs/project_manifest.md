# Project Manifest Contract

작업 폴더 루트에 `project.json` 하나가 박힌다.

본 manifest는 light pointer file이지 full database가 아니다. 작게 + 안정적으로 keep해서 워크플로우 문서가 handoff 경로 single source of truth를 reference할 수 있게.

## Required Top-Level Fields

```json
{
  "piece": "",
  "composer": "",
  "section": "",
  "vocal": "Hatsune Miku",
  "music": {},
  "video": {},
  "rights_log": "rights/rights-log.md"
}
```

## Music Contract (s302 후속 cut 양식)

```json
{
  "music": {
    "source_score_planning": "planning/candidates_opus/<filename>.pdf",
    "dry_stems_dir": "music/renders/dry_stems",
    "master_audio": "music/masters/master.wav"
  }
}
```

3 키만 남음:
- `source_score_planning` — PDF 경로 (`planning/candidates_opus/` 안 · 작업 폴더에 복사되지 않음).
- `dry_stems_dir` — V6 dry export 자리.
- `master_audio` — light assembly 결과물.

s302 이전 양식에 있던 키 폐기:
- 자동화 키: `analysis` (auto JSON) / `vocal_plan` / `auto_midi` / `render_ready_midi` / `render_studies`
- s302 후속 cut 키: `source_score` (PDF 복사) / `arrangement_brief` / `acappella_arrangement` / `role_design` / `pronunciation_map`

이유 = PDF는 planning/에서 직접 reference + MOKA의 PDF 분석 doc 박는 자리 자체 폐기 + 편곡/role/음절 결단은 V6 안에서 박힘.

## Video Contract

```json
{
  "video": {
    "brief": "video/video-brief.md",
    "final_video": "video/exports/final_4k.mp4"
  }
}
```

(`thumbnail` 키 폐기 · s313 결단 · YouTube 자동 썸네일 활용 path.)

## Stability Rule

새로운 persistent handoff 경로가 필요한 워크플로우가 발생하면, brief나 spec에 hard-code하기 전에 `project.json`에 박는다.
