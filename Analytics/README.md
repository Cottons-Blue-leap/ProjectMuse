# Project Muse — Analytics

## youtube_analytics.py — YouTube Analytics 분석 (SEO 모니터링)

Atelier Miku Acappella 채널/영상의 **트래픽 소스 · 검색어 · 시청자 지역 · 시청 지속률**을
YouTube Analytics API(OAuth)로 끌어온다.

> ⚠️ **노출수 · 노출 CTR(썸네일 클릭률)은 이 API에 없다.** Studio "도달범위" 탭 전용 →
> CTR은 Studio 스샷으로만 확인 가능. 이 도구 범위 밖.
>
> 이 도구가 주는 것: 검색어(실제 쿼리) · 트래픽 소스 분포 · 지역 · 평균 시청 지속률.

---

### 1. 최초 1회 세팅

**(A) GCP** (콘솔 작업)
1. [console.cloud.google.com](https://console.cloud.google.com) → 기존 프로젝트(YouTube Data API 키 있는 그 프로젝트) 선택
2. **API 및 서비스 → 라이브러리 → "YouTube Analytics API"** 검색 → 사용 설정
3. **API 및 서비스 → OAuth 동의 화면**
   - User Type = External
   - 앱 이름 + 본인 이메일 입력
   - **테스트 사용자에 채널 소유 Google 계정 추가** (안 하면 로그인 차단)
4. **API 및 서비스 → 사용자 인증 정보 → 사용자 인증 정보 만들기 → OAuth 클라이언트 ID**
   - 애플리케이션 유형 = **데스크톱 앱**
   - 만든 뒤 **JSON 다운로드**
5. 그 JSON을 `Project_Muse/client_secret.json` 이름 그대로 저장
   (`.gitignore`에 등록됨 — 커밋 안 됨)

**(B) 의존성**
```
python -m pip install --user -r Analytics/requirements.txt
```

**(C) 최초 인증** (한 번만)
```
python Analytics/youtube_analytics.py all
```
→ 브라우저가 열림 → **채널 소유 계정**(브랜드 계정이면 Atelier Miku Acappella 선택)으로 로그인·허용
→ 토큰이 `Project_Muse/.youtube_oauth_token.json`에 캐시됨 (이후 자동, gitignore됨).

---

### 2. 사용

```
python Analytics/youtube_analytics.py all          # 전부 (트래픽 + 검색어 + 지역 + 지속률)
python Analytics/youtube_analytics.py traffic      # 트래픽 소스 분포
python Analytics/youtube_analytics.py search       # 검색어 top N
python Analytics/youtube_analytics.py geo          # 시청자 지역
python Analytics/youtube_analytics.py retention    # 영상별 시청 지속률 (평균)
python Analytics/youtube_analytics.py retention-curve  # 영상 안 위치별 지속 곡선 (어디서 빠지나)
```

> `retention-curve`는 영상별로 *어느 지점에서* 이탈하는지 보여줌 (`--video ID`로 한 곡만, 생략 시 발행작 전부).
> 단 retention 데이터는 영상에 최소 시청량이 쌓여야 나옴 — 뷰 적은 신곡은 "데이터 없음".

옵션:
| 옵션 | 의미 | 기본값 |
|---|---|---|
| `--days N` | 최근 N일 | 28 |
| `--start / --end YYYY-MM-DD` | 명시 기간 (`--days` 대신) | — |
| `--video VIDEO_ID` | 특정 영상만 | 채널 전체 |
| `--top N` | 검색어/지역 표시 개수 | 25 |

예:
```
python Analytics/youtube_analytics.py search --days 7
python Analytics/youtube_analytics.py all --video rRnl8RZ3EjY
```

> 한국어/일본어가 콘솔에서 깨지면(cp949) 파일로 받기: `python Analytics/youtube_analytics.py all > seo.txt`
> (출력은 UTF-8로 강제됨 — 파일은 깨끗하게 저장됨.)

---

### 3. 한 페이지 리포트 + Excel — `report` (라이브 운영용)

```
python Analytics/youtube_analytics.py report          # 최근 28일
python Analytics/youtube_analytics.py report --days 7 # 최근 7일
```

한 번 돌리면 `Project_Muse/Analytics/`에 네 가지가 생긴다 (스크립트와 같은 폴더):

| 산출물 | 내용 |
|---|---|
| `channel_health_report.md` | **한 페이지 채널 헬스 리포트** (현황·영상별·트래픽·전환·전략·액션·§7 Studio 노출/CTR) · 매번 덮어씀 |
| `snapshots.csv` 외 3종 | **시계열 CSV** (채널+영상별 / 트래픽 / 지역 / 검색어) · 측정할 때마다 한 줄씩 누적 |
| `channel_analysis.xlsx` | **Excel 분석 워크북** (개요·영상별·추이[차트]·트래픽[차트]·지역검색·원자료) · CSV에서 재생성 |

- **운영 방식**: 주 1회 같은 요일에 `report` 실행 → CSV에 측정 row 누적 → md/xlsx 자동 재생성. 측정이 쌓일수록 리포트 '한 줄 현황'에 **지난주 대비 증감**이 뜨고, Excel '추이' 차트가 자란다.
- 같은 날 두 번 돌리면 그날 측정은 **갈아끼움**(중복 없음).
- ⚠️ **노출수·CTR은 여전히 API 밖** → Studio **'도달범위'** 탭 측정값을 `studio_reach.csv`에 **행으로 추가**하면 md **§7이 자동 렌더**(측정 2회 이상이면 pre/post era 비교 표까지). 더 이상 md를 손으로 안 채워도 됨(휘발 방지). (xlsx '개요'의 노란 칸은 아직 수동.)
  - `studio_reach.csv` 양식: `measured_on,window_days,start_date,end_date,scope,video_id,impressions,ctr_pct,views,thumbnail_era` · scope=`CHANNEL` 또는 영상 표시명 · era=썸네일 버전 태그(`pre_v4`/`post_v4` 등). report가 생성하는 게 아니라 **손으로 관리하는 입력 파일**.
- `channel_analysis.xlsx`는 재생성 바이너리라 `.gitignore` 처리됨. CSV·md는 커밋 대상(source of truth).
- Excel은 `analytics_xlsx.py`가 만든다 (`openpyxl` 필요 — requirements.txt에 포함). 미설치 시 `report`는 md·CSV까지만 만들고 Excel만 건너뛴다.

---

### 메모

- **신곡 publish 시**: `youtube_analytics.py`의 `VIDEOS` 딕셔너리에 `영상ID: "표시명"` 추가.
- **데이터 지연**: YouTube Analytics는 2~3일 지연. 오늘 변경은 며칠 뒤부터 반영.
- **토큰 만료/스코프 변경 시**: `.youtube_oauth_token.json` 삭제 후 재인증.
- **보안**: `client_secret.json` + `.youtube_oauth_token.json` 둘 다 gitignore됨. 절대 커밋·공유 X.
