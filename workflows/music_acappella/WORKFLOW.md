# Detailed Music Acappella Workflow

본 자료는 음악 자리 전체 phase 시퀀스다. 인접 워크플로우에 속한 자리는 그쪽으로 throw:

- 작업 폴더 신축: `workflows/project_setup`
- 권리 결단: `workflows/rights_clearance`
- V6 dry render + stem 점검 + 라이트 assembly: `workflows/audio_production`
- YouTube package: `workflows/video_release`

본 워크플로우는 *V6 entry reference library* 자리. production step이 아니라 V6 진입 시점에 참고할 자료를 모아둔 자리 (s302 리팩토링 + 후속 cut 통과).

## Phase 0: Project Question

곡 진입 전 본질 질문:

```text
미쿠 한 명의 보이스 디자인이 이 클래식 작품을 반주 없이도 아름답고
계속 들을 만하게 만들 수 있는가?
```

추천 proof size:
- 16 마디 — 첫 fit 확인 (옛 dogfood 양식).
- 60~90초 — serious proof.
- 작품 전체 — 짧은 proof가 통과한 후.

## Phase 1: Repertoire Selection

본 자리는 `planning/`에 누적. 자료 = `planning/candidate_master.csv` (S/A/B/C/D tier · 14 컬럼). 곡 선정 시점 점검 axis는 `prompts/01_selection.md` 참조.

PDF는 `planning/candidates_opus/`에 박힘. 본 워크플로우 안에서는 *결단된 곡 진입* path만 다룬다.

## Phase 2: Source And Rights

`workflows/rights_clearance/README.md` 양식 정합. 본 워크플로우 안에서는 *이미 approved된 상태*로 진입한다.

## Phase 3: V6 Direct Entry (코튼 직접)

코튼이 `planning/candidates_opus/<곡>.pdf`를 V6 editor 옆에 펴두고 piano roll에 직접 음표 + 음절 + dynamics + expression 입력. 본 phase가 본 워크플로우의 본질 자리.

별 doc 자리 없음 (s302 후속 cut · 코튼 결단 · 2026-05-14). 편곡 결단 (살릴 자리 / omit / octave / 텍스처 / 음절) + role 결단 + 음절 결단 다 V6 안에서 박힘.

V6 시점 참고 자료 (선택 reach):

```text
docs/role_taxonomy.md           6 role 의미 + 결단 axis
docs/instrument_pronunciation.md 음절 + V6 발음 매핑
docs/vocal_polishing.md          lead 선명도 / mid 두께 / low fake-bass 회피 axis
prompts/03_vocal_director.md     음역 + 음절 사고 정리
```

Role 양식 reference:

```text
Melody              작품의 식별 자리
Bass-function       harmonic floor (인간 베이스 흉내 X)
Inner harmony       melody와 floor 사이 chord 자료
Doubling/identity   한 명의 미쿠가 여럿이 되는 자리
Air/halo            light / shimmer / spatial lift
Rhythmic role       motion / ostinato / articulation
```

작품이 필요로 하지 않는 role은 첫 render에서 omit. 첫 proof는 보통 3 role (lead_miku + mid_oo + low_oo)로 시작.

음절 ↔ role 양식 reference:

```text
lead_miku        Ah   central melody
lead_double      Ah   quieter identity support
halo_high        Oo   upper air layer
mid_oo           Oo   inner harmony
low_oo           Oo   low foundation hint
air_mm           Mm   soft glue layer
```

이 이름은 구현 라벨일 뿐. 각 role은 작품의 음악적 기능과 매핑되어야 한다. 작품에 불필요한 role은 omit. 첫 proof는 Miku-only로 keep.

V6 작업 부담 점검 axis:
- 4시간 1세션 / 3세션 1 작품 추정 (짐노페디 base).
- 부담 elevation 발생 시 *섹션 단위 진입* 결단 자리.

각 role을 별 track으로 분리해서 dry export 준비. 본 phase 통과 후 audio_production으로 throw.

## Phase 4: Render & Assembly

`workflows/audio_production/README.md`로 throw. V6에서 dry stem export + stem 점검 + light assembly.

## Phase 5: Critique

`prompts/04_mix_critic.md` + `music/mix/listening-scorecard.csv`. 청취 평가 자리.

판단 axis (분리):
- Beauty.
- Naturalness.
- Miku identity.
- Classical dignity.
- Acappella feeling.
- Repeat-listen desire.

## Phase 6: Decision

```text
Green:
  진행 — 다음 자리 (video_release).

Yellow:
  곡 / key / register / syllable 결단 다시.

Red:
  더 사지 말고 멈춤.
```

첫 결단은 *컨셉이 아니라 청취*에서 박혀야 한다.
