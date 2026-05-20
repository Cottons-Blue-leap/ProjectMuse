# vivaldi_spring_1_allegro

Project Muse 2차 작품 (s301 진입, 2026-05-14). 짐노페디 first_proof 통과 후 정식 양식 첫 진입. s302 워크플로우 리팩토링 + 후속 cut 정합.

```text
piece: Spring (RV 269), Mvt. I Allegro
composer: Antonio Vivaldi (1678–1741)
parent work: Le quattro stagioni (The Four Seasons), Op. 8 No. 1
publication: 1725 (Amsterdam, Le Cène)
section: 통째 (full movement, ~3:30)
vocal: Hatsune Miku
playlist: Miku in the Baroque Era
release title: Antonio Vivaldi - Spring, Mvt. I (feat. Hatsune Miku)
cover art: Botticelli, Primavera (c. 1482)
source PDF: planning/candidates_opus/안토니오 비발디_사계_봄.pdf (28 page · 1악장 = page 1~11)
edition: Eulenburg (Robert Launchbury, 1982 · EE 6718)
transcription: 코튼 V6 editor 직접 입력 path
```

## 결단 자료 (s300~s302)

- ~5분 + S tier + 악기 ≤5건 axis → 14곡 추출 → *쾌활* + *낭만 회피* axis → 5곡 → **사계 봄 1악장** 결단.
- 정식 양식 진입 (first_proof dogfood 양식 폐기).
- 자동화 path (OMR / MusicXML / auto-MIDI) 다 폐기.
- 형식주의 doc (acappella-arrangement.md / arrangement-brief.md / role-design.md / pronunciation-map.csv) 다 폐기 — 코튼이 PDF만 보면서 V6에 직접 입력.

## 진행 자리

1. ✅ 곡 결단 (s300)
2. ✅ 작업 폴더 신축 (s301)
3. ✅ rights-log approved (s301 · composition + cover art Public Domain · edition keep)
4. ⏳ V6 editor 직접 입력 (코튼)
5. ⏳ dry stem export → `music/renders/dry_stems/`
6. ⏳ stem 점검 (`muse_audio.py check-stems`)
7. ⏳ light assembly → `music/masters/master.wav`
8. ⏳ listening decision (`music/mix/listening-scorecard.csv`)
9. ⏳ video brief + visualizer + 영상 작업 (썸네일 자리 폐기 · s313 결단 · YouTube 자동 썸네일 활용)
10. ⏳ YouTube package + publish

## 시리즈 정합

- 시그너처 = `../../README.md` § *Series Signature* + `../../series_history.csv` `signature_mark` 컬럼 (wordmark_v3 retrofit)
- 영상 description 양식 = `workflows/video_release/docs/description_template.md`
- 명화 = Botticelli *Primavera* (c. 1482)
