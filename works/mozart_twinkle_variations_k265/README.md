# mozart_twinkle_variations_k265

Project Muse 3차 작품 (s320 진입, 2026-05-17). 시리즈 첫 Classical period 진입 + 시그너처 §3 v3 wordmark 적용 first 작품 axis.

```text
piece: Twelve Variations on "Ah, vous dirai-je, maman" K.265
composer: Wolfgang Amadeus Mozart (1756–1791)
year: 1781-82 (Vienna)
section: 주제 + 12 변주 전체 (~12분 · 코튼 결단 *한 번에 다 만들기* · 시리즈 본격 작품 양식 axis)
vocal: Hatsune Miku
playlist: Miku in the Classical Era
release title: Mozart - Variations on "Twinkle, Twinkle, Little Star" K.265 (feat. Hatsune Miku)
cover art: Van Gogh, The Starry Night (1889)
source PDF: planning/candidates_opus/볼프강 아마데우스 모차르트_작은 별 변주곡.pdf (이미 박힘 · 9 page · scanned image · s322 자가 결함 적발 정정 자료)
transcription: 코튼 V6 editor 직접 입력 path
```

## 결단 자료 (s320 · MOKA 자가 4 axis · 코튼 *MOKA 추천대로 진행* 결단)

- **분량** = 주제 + **12 변주 전체** (~12분). 코튼 후속 결단 (*한 번에 다 만들기*) · MOKA 사전 추천 *5~6 변주 5-6분 fit axis* 자체엔 폐기. 시리즈 양식 (4분 + 3분) 대비 3-4x · 시리즈 본격 작품 양식 axis (분량 자체엔 작품별 가변 doctrine).
- **명화** = Van Gogh *The Starry Night* (1889) · **tentative axis (s322 코튼 throw · 변경 가능 axis 자료 · Lock X)**. *작은 별* anchor 매우 강 (universal · *Twinkle Twinkle Little Star* 직접 link). 시대 mismatch axis 자체엔 *anchor 강이 본질* doctrine (Primavera vs 비발디 sample 정합 base). csv default Bruegel *Children's Games* 자체엔 dense composition (200명+ · 80개 놀이) Miku 배치 fit X risk axis 회피.
- **acappella 양식** = V6 coloratura strong path. 변주 figuration (scale runs · arpeggios · trills · ornamentation) 자체엔 V6 strong axis. 변주별 voice 분배 자체엔 본격 작업 시 자리.
- **score** = `planning/candidates_opus/볼프강 아마데우스 모차르트_작은 별 변주곡.pdf` 이미 박힘 (9 page · scanned image · IMSLP self-host · s322 자가 결함 적발 정정 — 옛 *신축 자리* 양식 잔재 axis). Edition info 자체엔 IMSLP page 자가 점검 의제 (PDF text 자체엔 비어있음 · scanned 양식 axis).

## 시그너처 §3 v3 wordmark 적용 first 작품 axis

본 작품 자체엔 doctrine v3 (s320 박힘 · 우하단 corner · 좌하단 title mirror · cream + *M* 청록 · text-shadow blur 12 · GFS Didot size 40) 적용 first 작품. 비발디 자체엔 s320 retrofit 통과 자료 (scheduled publish 양식 base) · 본 작품 자체엔 default 양식 적용 axis.

## 진행 자리

1. ✅ 곡 결단 (s320)
2. ✅ 작업 폴더 신축 (s320)
3. ✅ rights 자가 점검 통과 (별 doc 자리 X · 코튼 s322 결단 *rights-log 신축 X · 양식 부담 elevation 회피* 정합)
   - **Composition**: Mozart 1791 사망 → life+70 통과 1861년 · 1785년 출판 · K.265 = 1781-82 Vienna 작곡 · PD 강
   - **IMSLP Edition** (5 edition 다 PD · candidates_opus PDF 자체엔 어느 edition인지 자가 점검 의제 axis = V6 본격 진입 시점 코튼 PDF 직접 보면서 자가 점검 path):
     - Breitkopf & Härtel (1878) - PD · recommended general use
     - C.F. Peters (undated · plate 6695) - PD · Köhler/Ruthardt
     - G. Henle Verlag (1959 · plate HN 116) - PD · Zimmermann (Urtext)
     - Bärenreiter (1961 · plate BA 4525) - PD · Kurt von Fischer (NMA critical · scholar-preferred · 비발디 Eulenburg sample 정합 base)
     - Carl Fischer (1924 · plate CC23003-12) - PD · Siloti
   - **Cover Art**: Vincent van Gogh, *The Starry Night* (1889) · life+100 통과 · PD 강 · MoMA NYC accession 472.1941 since 1941
     - High-res 자료 = Wikimedia Commons via Google Art Project · 44,567 × 35,291 px · 663.94 MB JPEG
     - Direct URL = `https://upload.wikimedia.org/wikipedia/commons/e/ea/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg`
   - **Decision**: `approved (composition + cover art) · edition_id V6 진입 시점 자가 점검 의제 axis keep`
4. ✅ score PDF 이미 박힘 (`planning/candidates_opus/볼프강 아마데우스 모차르트_작은 별 변주곡.pdf` · 9 page · s322 정정)
5. ⏳ V6 editor 직접 입력 (코튼 · 변주 결단 axis)
6. ⏳ dry stem export → `music/renders/dry_stems/`
7. ⏳ stem 점검 (`muse_audio.py check-stems`)
8. ⏳ light assembly → `music/masters/master.wav`
9. ⏳ listening decision (`music/mix/listening-scorecard.csv`)
10. ⏳ video brief + visualizer + 영상 작업 (썸네일 자리 폐기 · s313 결단 · YouTube 자동 썸네일 활용 + 시그너처 §3 v3 wordmark 적용)
11. ⏳ YouTube package + publish

## 시리즈 정합

- 시그너처 = `../../README.md` § *Series Signature* + `../../series_history.csv` `signature_mark` 컬럼 (wordmark_v3 default)
- 영상 description 양식 = `workflows/video_release/docs/description_template.md`
- 명화 = Van Gogh *The Starry Night* (1889 · MoMA collection)

## 사전 점검 의제 (다음 cycle 자리)

- **변주 선택 axis** — 12 변주 중 어떤 5~6 변주 자체엔 결단 (음악 verify 후 자리)
- **Classical Miku 배치 axis** — *Starry Night* 자체엔 cypress tree + village + swirling sky 양식 · Miku 자체엔 어디 배치 자연 path (foreground / mid-ground / 별 axis)
- **letterbox 색조 axis** — *Starry Night* 주조색 = deep blue (#0f1c4a) + yellow stars (#f4d03f) + cypress dark green (#2a3018) 양식 · 명화 light direction 정합 path
