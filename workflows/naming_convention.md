# File Naming Convention — Project Muse

> Cross-workflow doctrine. music + video 양 트랙 자료 자가 통합 양식.
> 박힌 날짜: 2026-05-19 (s332) · v1 정본

## piece_id 정의

**양식**: `<composer_last_lowercase>_<piece_snake_case>`

- **lowercase + snake_case** (ASCII only · space X · 특수문자 X)
- **composer_first** (작곡가 성 · 영어 양식)
- **작품 폴더명 = piece_id** (1:1 정합 강 · 양식 doctrine fixed)

**예시**:
- `joplin_the_entertainer`
- `vivaldi_spring_1_allegro`
- `satie_gymnopedie_1`
- `mozart_twinkle_variations_k265`

## 파일 양식 doctrine

| 자리 | 양식 | 예시 (Joplin) |
|---|---|---|
| **마스터 음원** | `music/masters/Miku_<piece_id>_master.wav` | `Miku_joplin_the_entertainer_master.wav` |
| **V6 export** | `music/renders/Miku_<piece_id>.wav` | `Miku_joplin_the_entertainer.wav` |
| **V6 project** | `music/renders/<piece_id>.vpr` | `joplin_the_entertainer.vpr` |
| **Source score (작품 폴더 copy)** | `music/source_scores/<piece_id>.pdf` (또는 .musicxml) | `joplin_the_entertainer.pdf` |
| **Art source 원본** | `video/art_sources/<artist_last>_<artwork_snake>.jpg` | `glackens_hammersteins_roof_garden.jpg` |
| **Cover 최종 (1:1)** | `video/cover/<piece_id>_album_1x1.png` | `joplin_the_entertainer_album_1x1.png` |
| **Cover iterations** | `video/cover/iterations/<piece_id>_iter<N>.png` | `joplin_the_entertainer_iter1.png` 등 |
| **Visualizer audio** | `video/visualizer/public/audio.wav` | (Remotion 양식 fixed · 폴더 context로 식별) |
| **Visualizer cover** | `video/visualizer/public/cover.png` | (Remotion 양식 fixed · 폴더 context로 식별) |
| **Final video** | `video/exports/<piece_id>_final.mp4` | `joplin_the_entertainer_final.mp4` |

## 핵심 원칙 4건

1. **piece_id = lowercase_snake_case + composer_first** (영어 · ASCII only · space X)
2. **Miku prefix** = V6 export + 마스터 자료에만 박음 (vocal 자료 식별 axis)
3. **piece_id prefix 양식** = cover / final / source 자료 양식 정합 (`<piece_id>_album_1x1.png` · `<piece_id>_final.mp4` · `<piece_id>.pdf` family)
4. **iterations/ 폴더** = 작업 자료 누적 자리 (final + iterations 분리 axis)

## Source Score 양식 axis

원본 PDF는 `planning/candidates_opus/<원본 파일명>.pdf` 양식 keep (한글 포함 · csv `score_file` 컬럼 매칭). 작품 진입 시점 (project_setup 후) `works/<piece>/music/source_scores/<piece_id>.pdf` 자리에 **ASCII rename copy** 박음.

- `planning/candidates_opus/` = 큐레이션 master + IMSLP self-host 자료 원본 archive axis
- `works/<piece>/music/source_scores/` = V6 진입 시점 사용 자료 (ASCII piece_id 양식 정합 · cmd line escape risk X)
- `project.json` `music.source_score_planning` 자리 = planning 양식 원본 path 박힘 (역추적 axis)

## 변경 시 axis

본 doctrine 자체엔 라이브 서비스 진입 후 (현 양식 2026-05-19 박힘) keep 양식 axis. 변경 의제 자체엔 시리즈 통째 retrofit 의무 axis 자체엔 신중 결단 자리.

이전 publish 통과 작품 (Gymnopedie + Vivaldi) 자체엔 doctrine 이전 자료 자체엔 retrofit X axis (publish URL keep · 자료 history axis).

## 정정 이력

- v1 (2026-05-19, s332) — Joplin 작업 자료 자체엔 자가 결단 cycle 통과. 핵심 5건 자가 적발 + 자가 정리:
  - space 자료 axis (cmd line escape risk) fix
  - vpr prefix 양식 일관성 박음
  - art source 양식 통합
  - cover 양식 piece_id prefix 양식 박음 (`album_1x1.png` 단독 자체엔 작품 식별 X axis · 코튼 자가 적발)
  - piece_id 정의 명시
