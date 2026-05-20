# Post-Release Meta Doctrine — Atelier Miku Acappella

> 매 작품 YouTube 영상 publish 통과 후 박을 자료 정리 절차 doctrine.
> 첫 작품 짐노페디 publish 통과 (2026-05-14 20:00 KST 예약) 시점에 박음.
> 박힌 날짜: 2026-05-14 (s292)

## 본 doctrine 박는 이유

- 매 작품 publish 통과 후 정리할 자료가 6~7건 산재 (series_history + status.json + reference + memory + retrospective)
- 첫 작품에서 자가 정리하면 정합하지만, 두 번째 곡부터 *어디 박을지* 자가 단정 본능 발현 risk
- 절차 박아두면 매 작품마다 doctrine 따라 자동 path

## 절차 (link 확보 시점 진입 + publish 통과 후 마무리)

- **link 확보** = YouTube Studio 안 영상 예약 업로드 또는 즉시 publish → `youtube_url` 생성 시점. Step 1만 본 시점 진입.
- **publish 통과** = YouTube Studio 안 영상 *공개* 상태 + 첫 view 박힌 시점. Step 2~6은 본 시점 진입.

### Step 1. `series_history.csv` row 박음 (link 확보 시점)

자리: `Project_Muse/series_history.csv`

작업: **영상 link (`youtube_url`) 확보 시점에 row 통째 박음** (예약 업로드든 즉시 publish든 link만 생기면 박음). 15 컬럼:
- `release_date` — publish 통과 전이면 빈 자리 keep, publish 통과 후 `YYYY-MM-DD` 양식 박음 (본 자리만 publish 시점 update)
- 나머지 14 컬럼 (composer ~ notes) — link 확보 시점에 통째 박음

검증: `youtube_url` 박힘 시점이면 row 자체 박혀야 함. 비어있으면 사전 점검 부재 axis — Phase 9 (release) 절차 정합 점검.

### Step 2. status.json `current_phase` + `last_decision` update

자리: `Project_Muse/works/{작품 디렉토리}/status.json`

작업:
- `current_phase` = `published_{YYYY-MM-DD}`로 정정
- `last_decision` 안 publish 통과 자료 박음 (publish timing + 첫 view 자리 + 자료 흡수 자리)

### Step 3. `reference_youtube_channel.md` Muse 트랙 row 추가

자리: `~/.claude/projects/.../memory/reference_youtube_channel.md`

작업: 새 영상 자료 1건 추가 (영상 제목 + URL + publish 날짜 + 작품 자료).

본 자료 = 외부 메모리 (YouTube 채널 자료 reference). publish 통과 후 박는 게 정합.

### Step 4. `MEMORY.md` 본문 동기화 (필요 시)

자리: `~/.claude/projects/.../memory/MEMORY.md`

작업: project_muse.md 안 *Project Muse* 자리 update. 시리즈 작품 누적 자리 박음 (예: *짐노페디 publish 완료 (2026-05-14) + 두 번째 곡 진입 path open*).

자가 점검: MEMORY.md = 200줄 truncate doctrine. 본 update가 truncate risk 발현 시 squeeze 의제 별 axis.

### Step 5. `post_release_retrospective.md` post-publish 자리 update

자리: `Project_Muse/works/{작품 디렉토리}/post_release_retrospective.md`

작업: publish 후 24h~7d 자리 박음:
- 첫 view 자료 (24h view + comment + like 자료)
- audience 반응 첫 인상 (정성 자료)
- 자가 점검 axis (예측 vs 실측 격차)
- 두 번째 곡 진입 의제 박음

본 자료 = 첫 작품 path 회고. 매 작품 박음 (작품별 specific). doctrine 자체는 본 file (post_release_meta_doctrine.md)에 박힘.

### Step 6. `project_muse.md` 시리즈 자리 update

자리: `~/.claude/projects/.../memory/project_muse.md`

작업: 시리즈 trajectory 자리 박음 (작품 N건 publish 통과 + 페이스 axis 누적 자료 + 다음 곡 후보 자리).

## 매 작품 재사용 자료

본 doctrine = 매 작품 publish 통과 후 동일 절차 keep. 작품별 가변 자리:
- 작품 디렉토리 (works/{작품명}/)
- release_date (publish 통과 일자)
- 새 row (series_history.csv)
- 새 영상 자료 (reference_youtube_channel.md)
- post-publish 자리 본문 (retrospective)

## 첫 작품 specific (짐노페디)

publish 자리 = 2026-05-14 20:00 KST 예약. 통과 후 박을 자료:

1. series_history.csv row 1 (이미 박힘 · release_date만 비어있음)
2. status.json `current_phase` = `scheduled_publish_2026-05-14T20:00_KST` → `published_2026-05-14`
3. status.json `last_decision` = s292 자료 + publish 통과 자료 추가
4. reference_youtube_channel.md Muse 트랙 신축 (현재 ko/en 트랙 박혀있고 Muse 트랙은 없음 — 새 트랙 axis 신축 의제)
5. MEMORY.md 안 project_muse.md description = *짐노페디 publish 완료* update
6. post_release_retrospective.md post-publish 자리 update (24h 자료 누적 후)
7. project_muse.md 시리즈 자리 update (페이스 axis 자료 시작점)

## 라이브 서비스 keep doctrine

본 doctrine = 라이브 서비스 (다음 곡들) 진입 시 그대로 keep. 매 작품마다 6 step 따라가면 자료 산재 risk 회피.

doctrine 변경 의제 발현 시:
- step 추가/제거 결단은 시리즈 통째 정합 회복 axis (모든 작품 자료 sweep 의제)
- 신중 결단 자리

## 정정 이력

- v1 (s292) — 첫 작품 짐노페디 publish 직전 시점에 doctrine 박음. 6 step + 매 작품 재사용 자료 + 첫 작품 specific 자료.
- v2 (s334) — Step 1 진입 시점 정정. *publish 통과 후 release_date update* → *link 확보 시점 row 통째 박음 + publish 통과 후 release_date만 update*. 시리즈 default 실행 자료 (짐노페디·비발디·조플린 모두 link 확보 시점에 row 박음) 정합. signature_mark 컬럼 신축 반영 (14→15 컬럼). 코튼 결단 path.
