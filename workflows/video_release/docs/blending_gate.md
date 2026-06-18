# 렌더 전 블렌딩 게이트 (WS1 · D1-a)

> 입안 2026-06-10 (s414) · 로드맵 `planning/competitiveness_roadmap.md` WS1.
> 엔진 = `workflows/audio_production/scripts/blend_gate.py` · CLI = `python muse.py audio blend-gate` / `calibrate-baseline`.
> 첫 라이브 가동 = ⑩ 헨델 (V6 입력 후 마스터 단).

## 왜

아카펠라는 소리가 본체다. 그런데 우리는 블렌딩 결함을 **렌더·발행 후** 코튼 귀로 적발해 왔다 (쇼팽 Lead 튐 → 재믹싱·재업로드 · 보케리니 4사이클). 코튼 귀가 *유일* 게이트라 확장이 안 된다. 미쿠 단일 음원 LOCK이라 음색 분리로는 못 푼다.

→ **객관 계측 게이트를 렌더 *전*으로 옮긴다.** MOKA는 청취 불가이므로 게이트는 **계측 기반**이고, 코튼 청취는 그 위의 **최종** 게이트로 남는다. 게이트는 코튼 귀를 대체하지 않고, 코튼 귀가 매번 처음부터 다 듣지 않아도 되게 *객관적으로 잡히는 것들을 먼저 거른다.*

## 두 입력

| 입력 | 무엇 | 게이트가 보는 것 |
|---|---|---|
| **풀믹스 마스터** (항상) | 지금까지 뽑던 stereo 마스터 1개 | 라우드니스/스테레오 (d) |
| **성부 stem** (있으면) | 멀티트랙 export | Lead 튐 (a)·성부 충돌 (b)·왜곡 (c) |

stem이 없으면 게이트는 풀믹스 레이어만 돈다 (= (d)만). stem이 있으면 4모드 전부.

## 4 실패모드 — 정의 · 탐지 · 처방 · 신뢰도

### (d) 라우드니스 / 스테레오 드리프트  — **강한 절대 게이트**
- **정의**: LUFS·True-Peak·스테레오 폭이 승인 프로파일을 이탈. 재생목록 Non-Stop에서 혼자 크거나/작게/좁게 들림.
- **탐지**: ffmpeg `loudnorm` (K-weighted Integrated LUFS, True-Peak, LRA) + numpy Mid/Side RMS·L/R 상관. 라이브 6곡 baseline range와 대조.
- **임계**: TP > **-1.0 dBTP** = hard (클리핑/IS-peak). LUFS가 family band **[-18.5, -13.5]** 밖 = hard. -16 타겟밴드 **[-17.0, -15.0]** 밖 = advise (의도면 OK: 친밀곡 -16.5~-17 / 활기곡 -15~-16). L/R 상관 < 0.2 = advise (위상). baseline range ±1dB 밖 = advise.
- **신뢰도**: **높음.** baseline이 실측 6곡(아래)이라 절대 판정 가능.

### (a) Lead 튐  — **stem 기반 게이트 (캘리브레이션 가능)**
- **정의**: 주선율(미쿠가 가사/멜로디를 부르는 성부)이 마스킹 균형을 깨고 튀어나옴 (쇼팽 사례).
- **탐지**: `--lead <트랙명 부분문자열>`로 주선율 트랙 지정 → 그 합 vs 나머지 반주 합의 RMS 차이(전체) + 0.2s 단기 윈도우 시계열(국소 튐).
- **임계**: Lead가 반주 대비 > **6 dB** = hard / > **3 dB** = advise. 단기 윈도우에서 > 9dB 튐이 활성 구간의 > 2%면 국소 튐 advise.
- **처방**: Lead 페이더 down. 국소면 해당 패시지 점검.
- **신뢰도**: **높음** (검증: 합성 Lead +9dB → +7.4dB hard flag 정확 적발). 트랙명은 자유 (악보 성부 그대로 "Miku Violin 1" 등) — `--lead`로만 주선율 식별.

### (b) 성부 충돌  — **측정 리포트 (임계 캘리브레이션 중)**
- **정의**: 동일 음원 성부 간 주파수 간섭/머디 (단일 음원이라 더 심함).
- **탐지**: 트랙 쌍별 옥타브밴드 스펙트럼 cosine(겹침) + 저중역(250-500Hz) 에너지 점유율(mud).
- **현 상태**: **절대 임계 없음.** 측정값을 리포트하고, 헨델~수곡에서 코튼 청취와 대조해 임계를 잡는다. 그 전까지 (b)는 info.

### (c) 멜리스마 / 레가토 왜곡  — **보조 지표 + 코튼 청취 위임**
- **정의**: 긴 모음 지속 시 배음 포락선 디지털 아티팩트.
- **탐지**: Lead HF(8k+16kHz) 점유율 probe.
- **현 상태**: 계측으로 신뢰성 있게 못 잡는다. **이건 코튼 청취가 최종.** 게이트는 info 보조만.

> 정직: (d)(a)는 게이트가 *판정*하고, (b)(c)는 게이트가 *측정해서 보여주되* 판정은 코튼 청취. 과신 금지 = [[feedback_self_audit_limits]] · [[feedback_no_sycophancy]].

## Stem export 요건 (코튼 2026-06-09 합의)

1. **트랙명 자유** — 악보 성부 그대로 ("Miku Violin 1", "Miku Viola left" 등) OK. prefix 불필요. 게이트 호출 시 `--lead`로 주선율 트랙만 지정.
2. **같은 시작·같은 길이** — 전 트랙 0초부터 곡 전체. 250ms 이상 어긋나면 게이트 경고.
3. **마스터 버스 토글 불필요** — 평소엔 버스 켠 채로 stem+풀믹스 둘 다 뽑으면 됨. 게이트가 **stem 합산 톤 ↔ 풀믹스 톤 cosine**으로 버스가 밸런스를 왜곡했는지 자동 진단 (≥0.97 = 밸런스 신뢰 / <0.97 = 그 곡만 버스 컴프·리미터 바이패스 재export 권고). EQ/톤은 모든 트랙에 동일 적용돼 상대 밸런스 보존되므로 무관, 문제는 세게 걸린 버스 컴프/리미터뿐.
4. **위치** = `works/<work>/music/renders/dry_stems/` (헨델부터 dry_stems 부활 · status.json `dry_stems` skipped → 갱신).

## 사용법

```bash
# baseline 재생성 (라이브 마스터 늘면)
python muse.py audio calibrate-baseline --out workflows/audio_production/docs/blend_gate_baseline.json

# 게이트 (풀믹스만)
python muse.py audio blend-gate --master <master.wav> \
  --baseline workflows/audio_production/docs/blend_gate_baseline.json

# 게이트 (stem 포함 · 권장)
python muse.py audio blend-gate --master <master.wav> \
  --stems works/<work>/music/renders/dry_stems --lead "Violin 1" \
  --baseline workflows/audio_production/docs/blend_gate_baseline.json \
  --out works/<work>/music/mix/blend_gate_report.json --strict
```

`--strict` = verdict FAIL이면 exit 1 (CI/렌더 게이트용).

## Verdict 해석

- **PASS** — hard·advise 0. 계측상 깨끗.
- **REVIEW** — advise 있음. 의도면 진행, 아니면 점검.
- **FAIL** — hard 있음 (TP 초과·LUFS family band 이탈·Lead 6dB+ 튐). 재export 권고.

> PASS/REVIEW/FAIL은 **계측 레이어 판정일 뿐.** 어느 경우든 **코튼 청취가 최종 게이트** ((b)(c)와 톤·따뜻함·비브라토는 계측 밖). = [[feedback_muse_arrangement_listen_gate]].

## 라이브 baseline (calibrate 산출 · 6곡 · 2026-06-10)

| metric | min | max | mean |
|---|---|---|---|
| LUFS | -18.0 | -15.5 | -17.17 |
| True-Peak dBTP | -4.1 | -1.2 | — |
| LRA | 2.3 | 8.3 | — |
| Side RMS dB | -34.49 | -26.78 | -31.73 |

(LUFS/TP/LRA는 `reference_muse_loudness_baseline.md` 실측과 일치 확인. 보케리니는 스테레오 native 복구로 Side 가장 넓음·corr 0.525.)

## 캘리브레이션 로드맵

- (d)(a) = 즉시 가동 (절대/경험 임계 확보).
- (b)(c) = 헨델부터 수곡간 **게이트 측정값 ↔ 코튼 청취 판정**을 대조해 임계 도출. 그 전까진 info.
- 새 라이브곡 마스터 늘 때마다 `calibrate-baseline` 재실행 → baseline range 갱신.

## 기각된 모드 — 시간축 구간 이상 탐지 (2026-06-13)

⑥⑨⑩이 "특정 구간만 주변과 다르게 묻힘/튐" 유형이라, 5번째 모드로 *풀믹스 10초 윈도별 밴드에너지 z-score 이탈 구간 플래그*(→ "청취 타겟 구간" 리스트)가 제안됐다. **backtest 결과 기각.**

- ground truth(결함본↔수정본 직접 차분)는 결함을 정확히 국소화한다(⑨ 0:50–1:40 / ⑩ 1:45–2:00 · 둘 다 ~2.3배 집중) — 결함은 실재한다.
- 그러나 z-score 탐지기는 결함본과 수정본에서 *같은 구간을 같은 점수로* 지목한다(⑨ 1.59↔1.57 / ⑩ 2.59↔2.77, ⑩은 수정 후 오히려 더 높음). 즉 결함이 아니라 *곡의 정상적 음악 변화*(클라이맥스 등 음악적으로 두드러진 패시지)를 가리킨다. 결함 크기 0.25dB(⑨)~2dB(⑩)이 **8배 차이나도 둘 다 미검출**.
- 근본 한계 = 기준선이 "곡 자신의 평균"이라, 음악의 정상적 구간 변화가 결함 신호를 압도한다. self-referential 방식의 구조적 무효 (크기 임계를 낮춰도 음악 변화를 더 많이 플래그할 뿐).
- **결론**: 구간 밸런스 결함의 1차 방어선은 **발행 전 갭 청취**(WORKFLOW.md ①루프 게이트). 계측 게이트는 전곡 단위 (d)(a)(b)(c)에 한정한다. 검증 스크립트 = `workflows/audio_production/scripts/_section_backtest.py`.
