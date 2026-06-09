# haydn_trumpet_concerto_finale

Project Muse 8차 작품 (2026-06-02 진입 · 코튼 결단 *월요일 업로드니까 기분 좋아질 만한 노래*). 쇼팽 녹턴⑥ release + 캐논⑦ 예약 후 선정. velocity(업비트·조플린 breakout 정합) + 시대대비(⑦ 캐논 바로크 → 고전) + 월요일 mood-lift + 세계 S anchor(rank 85). MOKA가 코튼 후보 4곡 전수 대조 → 코튼이 트럼펫 협주곡 결단(금관→목소리 충실도 risk + 가상 transcription 부담 의식적 감수).

```text
piece: Trumpet Concerto in E-flat major, Hob.VIIe:1, 3rd movement (Finale: Allegro) (Joseph Haydn)
composer: Joseph Haydn (1732-1809)
year: 1796 작곡 (고전기)
section: 3악장 Finale Allegro 통째 (~4:00-4:30 · 2/4 론도 · 발췌 없음 · family 정합)
vocal: Hatsune Miku (모음/humming · Ah·Oo·Mm · 기악 원곡 = 가사 없음 · 트럼펫 솔로→lead_miku / 반주→mid_oo·low_oo·halo_high / air_mm glue)
playlist: Miku in the Classical Era (작은별 K.265 공유 · 고전 family 정합)
release title: Haydn - Trumpet Concerto, Finale (feat. 初音ミク) · 성만 양식 (title_naming_guide 정합)
cover art: ⏸ 재선정 보류 (csv 기본값 Gros *Napoleon at Eylau* = mood mismatch · MOKA 비추) → 곡 V6 입력 완주 후 결단
source PDF: music/source_scores/haydn_trumpet_concerto.pdf (35p · 2.0MB · IMSLP PD 강)
transcription: 코튼 V6 editor 직접 입력 (OMR 없음 · manual transcription default 정합)
```

## 채보 방식 — manual V6 입력 (OMR RnD 보류)

정식 경로 = **코튼 V6 editor 직접 입력** (`project.json` 정합). 2026-06-03 측정 기반 자작 OMR 채보 파이프라인 RnD 시도했으나 코튼 판단 *OMR은 아직은 이른 감* (E2E 작동했으나 청취 오차 큼 · 미해결=박자 정합) → **보류 + 부산물 전량 삭제**(코튼 *아카이브까지 지워*). RnD 결과·재개 경로는 메모리 `project_haydn_acapella`에 보존 (OMR 재방문 시 유일 출발점).

## 편성 (10트랙, 코튼 확정)

Lead Trumpet(솔로) / Soprano=Vln I / Alto=Vln II / Viola / Bass=Vlc+Basso / Flute / Oboe / Bassoon / Horn / Timpani. 솔로 에피소드=5트랙(현+솔로), 관·금관·팀파니는 투티에서만(원곡 오케스트레이션 그대로). 솔로 50마디 진입, 1~49마디는 Vln I 주제 제시(Lead↔Soprano 콜&리스폰스). **이조 필수**: tr.solo·2 Trombe in Es = +단3도 / Corni in Es = −장6도 / Contrabass = −8도. 현·목관 비이조. 팡파르 staccato·악센트가 모음(Ah)에서 사는지가 게이트.

## rights

self-audit 사전 통과 (2026-06-02). Composition = Haydn d.1809 life+70 통과 · 전세계 PD 강 (Hob.VIIe:1 · 1796). Score = IMSLP self-host PD. Cover art = ⚠️ 재선정 필요 (V6 입력 후 결단 · 화가 중복 점검 path).

## 진행 자리

1. ✅ 곡 선정 lock (2026-06-02 · 코튼 mood-lift)
2. ✅ 작업 폴더 + 메타 + rights 자가 점검
3. ✅ score 확보 (`music/source_scores/haydn_trumpet_concerto.pdf` · 35p)
4. 🚫 OMR 채보 RnD 보류 (2026-06-03) → 부산물 정리 완료 (아카이브 `music/_archive/omr_rnd/`)
5. ⏳ V6 editor 직접 입력 (코튼 자리 · 3악장 Finale Allegro · `renders/Miku_*.vpr` 빈 8트랙 골격 활용)
6. ⏳ master = `music/masters/Miku_haydn_trumpet_concerto_finale_master.wav`
7. ⏳ listening decision → 명화 재선정 → 영상화(커버+visualizer s381 band-remap+2K 렌더+QC) → publish

## 시리즈 정합

- 시그너처 = `../../README.md` § *Series Signature* + `../../series_history.csv` `signature_mark` (wordmark_v3 default)
- 비주얼라이저 = s381 band-remap 신형 default (gain 곡별 결단)
- 제목 양식 = `../../planning/title_naming_guide.md` (성만 양식)
- 라이선스 = `reference_muse_license.md` (Crypton PCL + B-4 YPP)
- playlist = *Miku in the Classical Era* (작은별 K.265 공유)
