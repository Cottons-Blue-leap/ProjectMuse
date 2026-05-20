# gymnopedie_1_first_proof — Video

영상 산출물 자리. 워크플로우는 [`../../../workflows/video_release/`](../../../workflows/video_release/) 참조.

## 하위 자리

```text
art_sources/        # 명화 원본 + 라이선스 자료
cover/              # 최종 cover 산출물
  album_1x1.png         # 1:1 정사각 album cover (Atelier 시그너처)
  thumbnail.png         # 16:9 thumbnail (YouTube)
  iterations/           # ChatGPT·image gen sample 누적 (있을 때만)
visualizer/         # Remotion source code 자리
exports/            # 최종 export (<piece>_final.mp4)
release/            # 업로드 패키지 (title.txt · description.md 등)
```

## 시리즈 시그너처 적용

- 명화: 휘슬러 *Nocturne in Blue and Gold: Old Battersea Bridge* (1872-75)
- 타이포: GFS Didot
- 그리드: Lower-left text stack
- Letterbox: deep teal + muted gold 그라데이션 (manual hex 의제)
- 캐릭터: Classical Miku anchor 3줄 + boat 위 자세

자세한 양식: [`../../../README.md`](../../../README.md) § *Series Signature* + [`../../../series_history.csv`](../../../series_history.csv) `signature_mark` 컬럼.
