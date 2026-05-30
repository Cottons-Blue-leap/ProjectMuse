<!--
name: audio_production
stage: 3 · dry stem 점검 + light assembly + master
type: cli
entry: python ./workflows/audio_production/scripts/muse_audio.py check-stems | assemble-proof
inputs: [works/<piece>/music/renders/dry_stems/*.wav]
outputs: [works/<piece>/music/mix/stem-report.json, works/<piece>/music/masters/master.wav, works/<piece>/music/mix/listening-scorecard.csv, works/<piece>/notes/listening-notes.md]
depends_on: [music_acappella]
owner: Cotton+MOKA
-->

# Audio Production Workflow

This workflow owns rendering, stem checks, light acappella assembly, critique, and the approved
master audio handoff.

The music acappella workflow decides what the roles should be. Audio production
turns those decisions into dry stems and an approved proof master.

**Acappella-only path (2026-05-11, cotton decision)**: DAW-based mixing is removed from this workflow. The 6 dry stems from V6 are the primary deliverable. Assembly is light-touch (level matching + optional reverb only). Tool = V6 master / Audacity / Python.

## Inputs

```text
planning/candidates_opus/<곡>.pdf      (코튼이 V6 옆에 펴두고 직접 입력)
```

코튼이 V6 editor에서 PDF 보면서 piano roll에 직접 음표 + 음절 + dynamics 입력. 자동 MIDI 추출 path + 사전 doc (arrangement-brief / role-design / pronunciation-map) 다 폐기 (s302 + 후속 cut). 본 워크플로우는 V6에서 export된 dry stem을 받아 점검 + assembly 자리.

## Outputs

```text
works/<piece>/music/renders/dry_stems/*.wav
works/<piece>/music/mix/stem-report.json
works/<piece>/music/masters/master.wav
works/<piece>/music/mix/listening-scorecard.csv
works/<piece>/notes/listening-notes.md
```

## Render Rules

- Render one dry WAV per role.
- Use the same start time for every stem.
- Use the same sample rate and bit depth.
- Do not print master limiting or reverb into the dry stems.
- Start with the three-role proof before expanding to all roles.

Recommended first proof:

```text
lead_miku_ah.wav
mid_oo.wav
low_oo.wav
```

For detailed V6 steps, use:

```text
docs/v6_render_workflow.md
```

## Stem Check

```powershell
python .\workflows\audio_production\scripts\muse_audio.py check-stems `
  --stems .\works\<piece>\music\renders\dry_stems `
  --out .\works\<piece>\music\mix\stem-report.json `
  --expected lead_miku_ah.wav,mid_oo.wav,low_oo.wav
```

## Acappella Assembly

Light-touch assembly only — no DAW mixing.

Tool options (cotton's choice per piece):

- V6 GUI's built-in master export.
- Audacity (free, non-DAW).
- Python `assemble-proof` command for dry level-match proofing.

Assembly order:

1. Level-match dry stems (loudest stem ≤ -3 dBFS peak).
2. Optional: one shared gentle hall reverb (≤ 1.5s decay).
3. Sum to `music/masters/master.wav` (48 kHz / 24 bit).
4. Check mono / low-volume playback.

No EQ, no compression, no per-stem processing. If a stem needs fixing, re-render it from V6, do not patch in assembly.

Dry Python proof command:

```powershell
python .\workflows\audio_production\scripts\muse_audio.py assemble-proof `
  --stems .\works\<piece>\music\renders\dry_stems `
  --include lead_miku_ah.wav,mid_oo.wav,low_oo.wav `
  --out .\works\<piece>\music\masters\master.wav `
  --report .\works\<piece>\music\mix\assembly-report.json
```

This command only level-matches and sums compatible dry stems. It does not add
reverb, EQ, compression, or limiting.

## Decision

Use the listening scorecard and notes to decide:

```text
Green  -> extend the piece or prepare video release
Yellow -> revise piece/key/register/syllables/mix
Red    -> stop this piece or redefine the concept
```
