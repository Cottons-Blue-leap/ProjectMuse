# Visualizer — Vivaldi Spring Mvt. I

Atelier Miku Acappella 시리즈 visualizer. 짐노페디 베이스 (`works/gymnopedie_1_first_proof/video/visualizer/`)에서 본 작품용으로 옮긴 자료.

## Run

```bash
npm install       # 한 번
npm run studio    # Remotion Studio (preview)
npm run render    # out/vivaldi_spring_1_allegro_final.mp4 박음
```

## 곡별 정정 자료 (vs 짐노페디 베이스)

| 자료 | 짐노페디 | 비발디 봄 1악장 |
|---|---|---|
| Composition id | MuseGymnopedie1 | MuseVivaldiSpring1Allegro |
| DURATION_SECONDS | 189 | 198 (audio 197.6초 + tail) |
| letterboxColors | `["#1f2c3d", "#4a5a6e", "#b8a673"]` | `["#1f3122", "#d9b88a", "#f0e2c0"]` |
| composerName | Erik Satie | Antonio Vivaldi |
| pieceTitle | Gymnopédie No. 1 | Spring, Mvt. I |
| pieceSubtitle | (after 1888) | (after 1725) |
| BAR_MAX_AMPLITUDE_HEIGHT | 220 | 400 (dynamic ensemble) |
| AMPLIFICATION_HIGH | 7.0 | 6.0 (이미 dense bands) |
| audio.wav | 짐노페디 master | Miku_vivaldi_spring_1_allegro.wav (197.6s) |
| cover.png | 짐노페디 cover | album_1x1.png (Primavera) |

자료 출처 = `../visualizer-spec.md` 정합.

## 시리즈 공통 양식 (변경 X)

- Frame 1920×1080 (16:9) · Cover 720×720 center
- Letterbox 좌·우 600 / 위·아래 180 + vertical 3 stop gradient
- 좌·우 32 bars (총 64 · numberOfSamples 64) · BAR_WIDTH 3px · opacity 0.6
- Amplification curve (1.0 → high · exp 1.4) · sqrt amplitude scaling
- Fade in 3s (frame 0~90)
- Text stack 좌하단 (left 80 / bottom 60) · GFS Didot · 32 / 56 / 26px italic

## 다음 곡 활용 양식

새 작품 진입 시 본 폴더 통째로 복사 → `Root.tsx` props 6건 + `VisualizerComposition.tsx` 2건 (BAR_MAX + AMPLIFICATION_HIGH) + `package.json` name/scripts + `public/audio.wav`·`cover.png` 교체 cycle.

상세 시리즈 doctrine = `Project_Muse/README.md` § *Series Signature* + `Project_Muse/series_history.csv` `signature_mark` 컬럼.
