# V6 Render Workflow

본 워크플로우는 코튼이 V6 editor에 piano roll 직접 입력 완료한 시점에서 시작. 자동 MIDI 추출 + 사전 doc path 다 폐기 (s302 + 후속 cut) — 코튼이 `planning/candidates_opus/<곡>.pdf` 옆에 펴두고 V6에서 음표를 직접 찍는다.

목표는 3 role dry proof를 먼저 통과시킨 후 full choir로 확장하는 자리.

## Inputs

```text
planning/candidates_opus/<곡>.pdf
```

## Output

```text
works/<piece>/music/renders/dry_stems/lead_miku_ah.wav
works/<piece>/music/renders/dry_stems/mid_oo.wav
works/<piece>/music/renders/dry_stems/low_oo.wav
```

## Small Test Order

1. Render `lead_miku` for 4 bars.
2. Try `Ah`, `Lu`, and if needed `Oo`.
3. Keep the vowel that makes the melody clear without sounding harsh.
4. Add `low_oo` for the same 4 bars.
5. Try `Oo` and `Uu`.
6. Add sparse `mid_oo` only after the lead and low floor work.
7. Extend to 16 bars only after the 4-bar dry blend is acceptable.

## Bulk Vowel Replacement

In VOCALOID6 Editor, use multi-note lyric entry:

```text
select notes
-> Job
-> Lyric Input Mode
-> Letter Mode
-> Insert Lyrics
```

For support roles, enter repeated vowel lyrics such as:

```text
u u u u u
```

or Japanese:

```text
う う う う う
```

If the written lyric changes but the sound does not, convert phonemes to match
the language or check whether phoneme editing/protection is active.

## Minimal Tuning

Do first:

- Soften attacks.
- Avoid heavy vibrato.
- Keep phrase releases connected.
- Reduce harsh high notes by vowel, register, or level before adding effects.

Do later:

- Detailed pitch bends.
- Microtonal tuning.
- Formant automation.
- Full six-role choir polish.

## Export Rules

- Dry WAV only.
- Same start time for every stem.
- Same sample rate and bit depth.
- No printed reverb.
- No master limiter.
- One role per file.

Recommended:

```text
48 kHz / 24 bit WAV
mono or stereo consistently across all stems
```

## First Listening Gate

Listen with no reverb first:

- Melody is recognizable.
- Low role grounds harmony without fake bass theater.
- Middle role does not cloud the lead.
- Miku identity remains audible.
- The dry blend sounds intentional enough to continue.
