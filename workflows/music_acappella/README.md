<!--
name: music_acappella
stage: 2 · V6 entry reference (production X)
type: reference
entry: V6 진입 시점 docs/ 자료 참고 (코튼 직접 입력)
inputs: [planning/candidates_opus/<곡>.pdf, works/<piece>/rights/rights-log.md (approved)]
outputs: [works/<piece>/music/renders/dry_stems/*.wav (V6 export)]
depends_on: [rights_clearance]
owner: Cotton
-->

# Music Acappella Workflow

이 워크플로우는 *V6 entry reference library*. 코튼이 PDF 보면서 V6 piano roll에 직접 음표를 찍는 시점에 옆에 펴두고 참고하는 자료 자리.

s302 리팩토링 통과 + 후속 cut 통과 시점에서, 본 워크플로우는 production step이 아니라 *reference* 자리로 좁혀짐:
- 자동 분석 / 자동 MIDI 추출 / MusicXML pipeline 자리 = 다 폐기.
- arrangement-brief / acappella-arrangement / role-design / pronunciation-map 등 사전 doc 자리 = 다 폐기 (편곡 + role + 음절 결단은 V6 안에서 박힘).
- 본 워크플로우 안에서 살아남은 자리 = 6 role taxonomy + 음절 reference + listening doctrine + 곡 선정 reference.

## MOKA ↔ 코튼 영역 분리

`docs/role_division.md` 참조. V6 진입 시점 자가 점검 의무.

## Reference Docs

- `docs/role_taxonomy.md` — 6 role의 음악적 의미 + 결단 axis. V6 시점 어느 role을 사용할지 reference.
- `docs/instrument_pronunciation.md` — 음절 ↔ V6 발음 매핑 reference.
- `docs/vocal_polishing.md` — V6 시점 결단 axis (lead 선명도 / mid 두께 / low fake-bass theater 회피 등).
- `docs/role_division.md` — MOKA ↔ 코튼 영역 분리 doctrine.
- `docs/toolchain.md` — 도구 정합.

## Prompts (선택 사용)

- `prompts/01_selection.md` — 곡 선정 시점 reference (planning 단계).
- `prompts/03_vocal_director.md` — V6 시점 음역 + 음절 사고 정리.
- `prompts/04_mix_critic.md` — dry stem 청취 평가 시점.

s302 후속 cut에서 `prompts/02_arranger.md`도 reference로만 사용 (편곡 결단 자체는 V6 안에서 박힘).

## Templates

- `templates/candidate-scorecard.csv` — 곡 선정 자리 양식 (`planning/`에서 사용).
- `templates/listening-scorecard.csv` — audio_production 자리 listening 결단 양식 (init이 작업 폴더에 복사).

## V6 Entry Flow (코튼)

코튼이 V6 editor를 열고 손에 들고 들어가는 자료:

```text
planning/candidates_opus/<곡>.pdf       (작품 자체)
workflows/music_acappella/docs/role_taxonomy.md     (필요 시 reference)
workflows/music_acappella/docs/instrument_pronunciation.md  (필요 시 reference)
workflows/music_acappella/docs/vocal_polishing.md   (필요 시 reference)
```

V6에서:
- PDF 보면서 마디 단위로 음표 + 음절 + dynamics 입력
- 각 role을 별 track으로 분리
- dry export 준비 (각 role을 별 WAV로)

## Human Checkpoints

1. **Rights checkpoint** — `rights/rights-log.md`에 approved 박혀있는지.
2. **Solo checkpoint** — V6에서 lead만 먼저 dry로 청취 (다른 role 진입 전).
3. **Dry blend checkpoint** — 모든 role을 reverb 없이 청취.
4. **Space checkpoint** (선택) — light reverb 통과 후 청취 (audio_production).
5. **Identity checkpoint** — 결과가 *Miku 답게* 들리는가.

## Safe Boundary

본 워크플로우는 reference + doctrine 자리. 새로운 voice model 학습 자리 X. Miku V6 EULA 정합 path.
