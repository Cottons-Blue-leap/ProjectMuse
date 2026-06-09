# Metrics snapshot — Atelier Miku Acappella (28일 윈도우)

> source = `Project_Muse/Analytics/{studio_reach,snapshots,traffic,search,geo}.csv` · 측정일 2026-06-05 (일부 2026-05-22~06-01 추이 포함). 노출/CTR은 Studio 전용이라 studio_reach.csv가 유일 source. R&D 진단용으로 한자리에 모음.

## 채널 총량 추이 (snapshots.csv · CHANNEL row)

| 측정일 | views | watch_min | avg_view_sec | avg_view_pct | likes | comments | subs_gained | shares | like_rate |
|---|---|---|---|---|---|---|---|---|---|
| 05-22 | 164 | 91 | 33 | 17.34 | 23 | 1 | 5 | 4 | 14.0 |
| 05-29 | 318 | 211 | 40 | 20.46 | 30 | 3 | 8 | 5 | 9.4 |
| 06-01 | 362 | 297 | 49 | 24.17 | 34 | 3 | 10 | 6 | 9.4 |
| 06-05 | 494 | 528 | 64 | 27.98 | 50 | 5 | 12 | 7 | 10.1 |

→ 전 지표 우상향. avg_view_sec 33→64 (2배), avg_view_pct 17%→28%, watch_min 91→528.

## 노출·CTR (studio_reach.csv · 06-05 · 28d)

| 영상 | impressions | CTR% | views | 비고 |
|---|---|---|---|---|
| **CHANNEL** | **34,088** | **0.9** | **534** | 블렌드 평균 |
| Gymnopédie No.1 | 13,624 | 0.7 | 165 | 노출 깡패·CTR 바닥 |
| Joplin Entertainer | 13,816 | 0.6 | 125 | 노출 깡패·CTR 바닥 |
| Mozart K.265 | 2,369 | 2.5 | 108 | 웜 트래픽 |
| Elgar Salut d'Amour | 2,790 | 1.1 | 48 | |
| Vivaldi Spring I | 979 | 2.5 | 49 | |
| Chopin Nocturne Op.9-2 | 302 | 3.0 | 21 | 신곡·최고 CTR |
| Pachelbel Canon | 1 | 0 | 1 | 막 발행 |

→ **Gymnopédie + Joplin = 27,440 노출 = 채널 노출의 80.5%**, 둘 다 CTR 0.6~0.7%. 신곡·소노출 영상은 CTR 2.5~3.0%.

## 영상별 유지율 (snapshots.csv · 06-05)

| 영상 | views | avg_view_sec | avg_view_pct | like_rate% |
|---|---|---|---|---|
| Joplin | 120 | 89 | **40.85** | 6.7 |
| Chopin Nocturne | 13 | 125 | **47.78** | 23.1 |
| Vivaldi Spring | 45 | 78 | 39.3 | 11.1 |
| Elgar | 45 | 37 | 26.31 | 2.2 |
| Mozart K.265 | 97 | 76 | 21.06 | 14.4 |
| Gymnopédie | 157 | 38 | 20.03 | 9.6 |

## 트래픽 소스 추이 (traffic.csv · share_pct)

| 소스 | 05-22 | 05-29 | 06-01 | 06-05 | 06-05 views | avg_view_sec |
|---|---|---|---|---|---|---|
| RELATED_VIDEO 추천 | 59.8 | 61.5 | 56.4 | **43.4** | 214 | 54 |
| SUBSCRIBER 구독피드·홈 | 14.0 | 12.6 | 14.4 | **28.2** | 139 | 77 |
| YT_CHANNEL 채널페이지 | 6.1 | 6.9 | 6.1 | 5.3 | 26 | 31 |
| YT_SEARCH 검색 | 2.4 | 1.9 | 4.1 | 5.3 | 26 | 42 |
| NO_LINK_OTHER 직접 | 6.7 | 6.0 | 5.5 | 5.1 | 25 | 58 |
| PLAYLIST 재생목록 | 1.8 | 1.9 | 4.7 | 4.9 | 24 | **141** |
| YT_OTHER_PAGE | 3.7 | 4.1 | 4.4 | 3.9 | 19 | 58 |
| EXT_URL 외부링크 | 5.5 | 5.0 | 4.4 | 3.7 | 18 | 41 |
| END_SCREEN | – | – | – | 0.4 | 2 | **290** |

→ 추천 share 하락(60→43%) · 구독 급증(14→28%) · 재생목록·종료화면 = 소량이나 최장 체류.

## 검색 쿼리 (search.csv · 06-05)

vocaloid6 (4) · salut d'amour (3) · miku v6 (2) · ah vous dirai-je maman (1) · hatsune miku v6 (1) · 初音ミク (1)

→ 전부 **보컬로이드 정체성** 또는 **정확한 곡명**. "classical music"/"relaxing"/"a cappella" 류 일반 쿼리 유입 0.

## 지역 (geo.csv · 06-05)

| 국가 | views | avg_view_pct |
|---|---|---|
| US 미국 | 68 | 27.33 |
| JP 일본 | 11 | 15.93 |
| GB 영국 | 10 | **32.28** |
| KR 한국 | 10 | 19.07 |

→ US 최대 볼륨 · GB 최고 유지율 · **JP 유지율 최저(16%)** (보컬로이드 모국인데 역설).
