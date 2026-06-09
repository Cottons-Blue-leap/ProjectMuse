# Atelier Miku A Cappella — 경쟁력 로드맵

> 입안: 2026-06-09 (s413) · 코튼 4 우선순위 결정 승인 후 박음.
> 출발 진단 = "우리는 개척자가 아니라 **공방(atelier)**이다. 의의는 기술·음악학이 아니라 **마감 + 글로벌 유통**에 있다."
> 선행 채널 좌표(우리가 *발명하지 않은* 것들): EARLY MUSIC MIDI(고음악 복원·교차언어), pikabonT(이질 콰르텟 아카이브), hamofanjoe(기악→보컬 치환), Gnagre(단일 미쿠 젠더팩터). 출처 = `보컬로이드 클래식 아카펠라 사례 분석.md` (코튼 조사보고서).

---

## 확정 결정 (코튼 · 2026-06-09)

1. **렌더 전 블렌딩 게이트 시스템화** — 승인. 소리가 제품의 전부 = 사후 봉합 탈피.
2. **미쿠 단일 보이스뱅크 = 브랜드 LOCK** — 제2 음원 도입 **불채택**. pikabonT식 음색 분리(이질 콰르텟)를 *의식적으로 포기*하고, 그 대가(평탄한 블렌딩)는 게이트(WS1)로 관리한다.
3. **선배 채널 경쟁 분석** — 승인.
4. **검색 표현 정합 (제목/태그)** — 승인. ~~로케일별 썸네일~~ = 계획에서 **제거**(코튼 2026-06-09). 사유: YouTube는 영상당 썸네일 1개만 서빙(제목·설명만 언어별 로컬라이즈, 썸네일 교체 불가) → 재제안 금지.
5. **미술관식 정체성 유지** — 승인. 꾸준히 (별도 명문화 deliverable는 제거 · 코튼 2026-06-09).

---

## WS1 — 렌더 전 블렌딩 게이트 (1순위 · 바닥)

**문제**: 아카펠라는 소리가 본체인데, 결함을 *렌더·발행 후* 코튼 귀로 적발 → 재믹싱·재렌더·재업로드(쇼팽 Lead 튐, 보케리니 4사이클). 코튼 귀가 유일 게이트라 확장 불가.

**제약**: 미쿠 단일 음원 LOCK → 음색 분리로 못 푼다. 젠더팩터/EQ/패닝/타이밍 안에서 잡아야 함. MOKA는 청취 불가 → 게이트는 **계측 기반 + 코튼 청취**의 2단.

**반복 실패 모드 (라이브 적발 이력 기반)**:
- (a) Lead 튐 — Lead 성부가 마스킹 균형을 깨고 튀어나옴.
- (b) 성부 충돌 — 동일 음색 성부 간 주파수 간섭(단일 음원이라 더 심함).
- (c) 멜리스마/레가토 왜곡 — 긴 모음 지속 시 배음 포락선 디지털 아티팩트.
- (d) 라우드니스/스테레오 드리프트 — LUFS·TP·Side 레벨 승인 프로파일 이탈.

**deliverable**:
- **D1-a** 실패 모드 체크리스트 md (`workflows/video_release/docs/blending_gate.md`) — 각 모드 정의 + 탐지법 + 처방.
- **D1-b** 계측 스크립트 — 프리마스터 믹스(렌더 전)에 대해: 성부별 라우드니스 균형, 스펙트럼 마스킹/오버랩, true-peak, LRA, 스테레오 폭 측정 → pass/flag 리포트. `muse.py audio` 확장 or Analytics 신축. 기준선 = `reference_muse_loudness_baseline.md` 실측값.
- **D1-c** 워크플로우에 **렌더 전 Phase** 삽입 = 계측(D1-b) → MOKA 자가 점검 → 코튼 청취 → *통과 후에만* 렌더 commit. (현재는 마스터 후 코튼 청취 → 렌더가 먼저 나가는 구조)
- **첫 라이브 적용 = ⑩ 헨델** (공유 visualizer 첫 적용곡과 정렬).

**owner**: MOKA 입안·스크립트 / 코튼 청취 게이트 keep.

---

## WS2 — 선배 채널 경쟁 분석 (2순위 · 전장 파악)

**문제**: 경쟁 정보 0. 한 번도 선배 채널을 계측 기반으로 뜯은 적 없음.

**대상**: EARLY MUSIC MIDI · pikabonT · hamofanjoe · Bocaro Choir(+ Gnagre 보조).

**추출 항목** (YouTube Data API v3 = 보유 · `reference_youtube_channel.md` OAuth):
- 상위 영상(조회순) + 제목 패턴 + 썸네일 패턴 + 공개 태그 + 업로드 케이던스 + 다룬 곡 목록(=공급 지도) + 다국어 여부(대부분 無 = 우리 갭).

**deliverable**:
- **D2-a** teardown 문서 (`planning/competitor_teardown.md`).
- **D2-b** **검색 수요↑ · 공급↓ 곡 후보 shortlist** → `candidate_master.csv` 선정 축에 "검색 갭" 컬럼/메모 반영. 레퍼토리를 popularity_tier 단독이 아니라 검색 갭으로도 고른다.

**owner**: MOKA (API pull + 분석) → 코튼 검수.

---

## WS3 — 검색 표현 정합 (3순위 · 해자)

**문제**: 10로케일 메타가 *깔려만* 있는지 *작동*하는지 모름. CTR↔노출 반비례(=차가운 트래픽 구조 바닥, `reference_muse_ctr_impression_floor.md`)는 정상이나, 해법은 더 예쁜 썸네일이 아니라 **따뜻한 트래픽**(검색 의도·구독).
- **D3-a** 곡×로케일별 *실제 검색 표현* 매핑 — YouTube 검색 자동완성 + 경쟁자 태그(WS2) 프록시. 우리 라이브 제목/태그가 그 표현에 맞는지 audit.
- **D3-b** 불일치분 라이브 retrofit (`youtube_meta.py` 제목/태그). `localize_batch.py` 라인업과 정합 유지.

> ~~Part B 로케일별 썸네일~~ = 제거(코튼 2026-06-09). YouTube 영상당 썸네일 1개 서빙 = 언어별 교체 불가.

**owner**: MOKA audit·retrofit → 코튼 검수.

---

## WS4 — 미술관식 정체성 + 카탈로그 깊이 (4순위 · 지속)

**문제**: 소리·기법·기하학은 다 선행자 있음. **명화 + 미쿠 + 시대별 미술관식 큐레이션**이 씬에서 우리가 가장 선명한 표면. 구독 11/영상 9 = traction 이전 → 폴리싱보다 깊이·리듬.

**deliverable**:
- **D4-a** 발행 케이던스 유지 + 명화·미쿠·시대 큐레이션 표면 일관 keep (별도 신축 X · 기존 워크플로우). ~~convention 명문화~~ = 제거(코튼 2026-06-09 · 이미 암묵 컨벤션으로 작동 중).

**owner**: 코튼 주도(꾸준히).

---

## 진행 (s414 · 2026-06-10)

- **WS1 ✅ spec+엔진 완성** — `blend_gate.py`(풀믹스 d + stem a/b/c + 버스 자동진단) · baseline 6곡 캘리브레이션(`docs/blend_gate_baseline.json` · 메모리 실측 일치 검증) · spec `docs/blending_gate.md`(D1-a) · 워크플로우 삽입(D1-c) · CLI `muse.py audio blend-gate`. 검증 = Lead+9dB→hard FAIL 정확/보케리니 실곡 PASS. **남은 = 헨델 stem 첫 라이브 가동(코튼 V6 export 대기) + (b)(c) 임계 헨델+수곡 청취 대조 캘리브레이션.** stem 요건 합의 = 트랙명 자유+`--lead`+버스 토글 불필요.
- **WS2 ✅ 완료(검증)** — `planning/competitor_teardown.md`(D2-a) + 검색갭 shortlist(D2-b) · raw `Analytics/competitor_raw.json`(quota 0 재현). EMM 5280/889/1.8M · pikabonT 306휴면 · hamofanjoe 434(애니OP 1편 57%) · gnagre3 77종료 · **Bocaro Choir=전용채널 아님(코튼 확인要)**. 핵심=①다국어 0=우리만 ②낭만 워홀스 선배 공급 0=검색갭 ③케이던스가 구독 견인. **남은 = candidate_master `search_gap` 축 반영(코튼 검수).**

## 실행 순서 (의존성)

- **Phase 1 (병렬)**: WS1(블렌딩 게이트 spec+스크립트) ∥ WS2(teardown). 둘 다 독립.
- **Phase 2**: WS3 검색 audit(WS2 산출 사용) → 라이브 제목/태그 retrofit.
- **Phase 3 / 지속**: WS4 케이던스 + 큐레이션 표면 keep.

## 비고
- 본 작업 산출물은 미커밋 git 백로그(128건, 다음 세션 논리분할 커밋 예정)에 합류 → 깨끗이 분리 커밋.
- WS1 게이트는 ⑩ 헨델 렌더 전에 1차 가동 = 첫 라이브 테스트.
