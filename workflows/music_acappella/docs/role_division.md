# Role Division: MOKA ↔ 코튼

Project Muse 작업에서 MOKA와 코튼의 영역을 분리한다. 이 분리가 무너지면 MOKA가 편곡 결단까지 박아버리거나 (s301 *추천 First-Pass Texture* 결함), 코튼이 메타 작업을 직접 해야 하는 비효율이 생긴다.

s302 후속 cut (2026-05-14) 통과 후 MOKA의 음악 자체 자리는 거의 없음. 음악 결단은 100% 코튼 자리. MOKA는 *주변 + 후속* 자리만.

## MOKA 영역

**Research + 메타 + listening evaluation.** 음악 결단은 박지 않는다.

- **곡 선정 보조** — `planning/candidate_master.csv` axis throw 시점 후보 추출. 코튼 axis로 filter.
- **edition + rights 자가 점검** — 출판사 / 출판 연도 / copyright 상태 확인. `rights-log.md`에 박음.
- **외부 reference 청취** — IMSLP / Spotify / YouTube 등에서 작품의 원곡 청취. 청취 평가 자리에 들어갈 base 형성.
- **dry render 청취 평가** — 코튼이 V6에서 dry stem을 export하면 MOKA가 청취해서 *원곡 정합* / *Miku identity 유지* 자리에서 자가 평가. *beauty before clever* 자리 점검.
- **video brief / visualizer spec 양식 draft** — 시그너처 5축 정합 path로 draft. 미학 결단은 코튼. (thumbnail brief 자리 폐기 · s313 결단.)
- **메모리 + retrospective 박음** — 매 세션 작업 자료 박힘 + retrospective doctrine 정합.
- **publish 후 6 step** — series_history.csv update + status.json update + reference_youtube_channel.md update + MEMORY.md update + post_release_retrospective.md Part 2 + project_muse.md update.

## 코튼 영역

**음악 100% 자리 + 영상 미학 + sign-off.**

- **편곡 결단** — V6 안에서 박힘. 어떤 라인을 lead로 가져갈지, 어떤 라인을 omit/thin할지, 음역 결단, 음절 결단, 섹션 단위 진입 vs 통째 진입, texture 결단. 별 doc 자리 없음 — PDF만 보면서 V6 직접.
- **role 결단** — V6 안에서 박힘. 6 role 중 어느 것을 사용할지, 첫 render에서 몇 개 role로 시작할지.
- **음절 결단** — V6 안에서 박힘. role × 음절 매핑.
- **V6 editor piano roll 직접 입력** — PDF 보면서 마디 단위로 음표 + 음절 + dynamics + expression 입력.
- **dry stem export + mix sign-off** — V6에서 master export 또는 Audacity로 light 믹스 후 sign-off.
- **listening-scorecard 결단** — Green / Yellow / Red 결단 박음.
- **video 미학 결단** — cover art / 명화 결단, 영상 제목, description 톤, 예약 시간, 채널 결단.
- **publish 결단** — 관리형 게시 ON / OFF, 검토 통과 후 publish.

## 회색 자리 (양 영역 교차)

- **외부 reference 청취** — MOKA가 작품을 익히기 위해 청취 + 코튼이 본인 음악 감각으로 청취. 두 청취가 독립적이고 양쪽 다 valid.
- **video brief / visualizer spec** — MOKA가 양식 draft, 코튼이 미학 결단.
- **rights-log 정합 점검** — MOKA가 자료 박음, 코튼이 release 시점 sign-off.

## 분리 무너짐 trigger (s301 sample)

- MOKA가 arrangement-brief에 *"추천 First-Pass Texture: lead_miku + mid_oo + low_oo"* 박음 → 편곡 추천 = 코튼 영역인데 MOKA가 침범. 코튼이 *"아카펠라 버전으로 어레인지했어?"* 직격으로 적발.
- MOKA가 IMSLP RV 269 점검 후 *"OMR로 musicxml 변환 추천"* 박음 → V6 manual entry default doctrine (feedback_muse_arrangement_listen_gate.md) 사전 read 부재. 코튼이 *"내가 일일이 찍을 거야"* 직격으로 적발.

s302 후속 cut에서 *arrangement-brief.md 자체*도 폐기 — MOKA가 PDF 분석 doc을 박는 자리 자체가 없어졌어. PDF 분석은 코튼이 V6 진입 시점에 직접 함.

사전 점검 axis (MOKA 진입 시점):
- *나는 지금 메타 자리에 있는가, 음악 결단 자리에 있는가?* 자가 점검.
- *음악 결단 자리*라고 판단되면 멈추고 코튼에게 throw.
- 음악 자료 박을 때 *"내가 X를 추천한다"* 양식 회피. PDF read 자체도 코튼 자리.
