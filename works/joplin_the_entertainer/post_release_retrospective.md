# Post-Release Retrospective — Scott Joplin, The Entertainer

> Joplin 세 번째 작품 publish 회고 자료. 네 번째 곡 진입 전 자가 점검 axis.
> Pre-publish 자리 = publish 직전 박음 (s332 · 2026-05-19)
> Post-publish 자리 = publish 통과 후 24h~7d 자료 누적 박음 (현재 비워둠)
> 박힌 양식 doctrine = [`workflows/video_release/docs/post_release_meta_doctrine.md`](../../workflows/video_release/docs/post_release_meta_doctrine.md)

## 작품 자료

- 곡: Scott Joplin, The Entertainer (1902)
- 영상 제목: Scott Joplin - The Entertainer (feat. Hatsune Miku)
- 명화: William Glackens, *Hammerstein's Roof Garden* (c.1901) · Whitney Museum of American Art
- 보컬: Hatsune Miku (Vocaloid6) · 9 voice acappella
- 영상 URL: https://youtu.be/DVIYl09zX-w
- Publish 자리: 2026-05-21 (목) 20:00 KST 예약 (s332 코튼 직접 Studio paste path) → publish 통과 자료 비움 (publish 후 update)
- 재생목록: Miku in the 20th Century

---

## Part 1. Pre-Publish 자리 (s326~s332)

### 통과 자료

**음악 production**
- s326 3차 곡 재선정 cycle 통과 (Mozart K.265 drop → 재선정 cycle → Joplin The Entertainer 결단)
- s331 V6 본격 진입 + 1차 분석 + publish 결단 lock (v2 wav · -16.1 LUFS / LRA 2.7 / -2.0 dBTP · 218.57초)
- 9 voice acappella (V6 voice 분배 · ABACAD 5 strain)
- Manual transcription default doctrine keep (시리즈 정합 axis)
- V6 EXP/DYN doctrine Q&A 통과 + 스펙트로그램 우회로 cycle (s331 자가 결함 정정 path)

**영상 production (s332)**
- Phase B 명화 재선정 cycle (Seurat *The Circus* → Glackens *Hammerstein's Roof Garden*)
- Phase C cover 합성 (ChatGPT image gen 3 iteration · 1차 그림체 훼손 5건 자가 적발 → 3차 elegant lock · `joplin_the_entertainer_album_1x1.png` 3.03MB)
- naming convention v1 정본 박힘 (`workflows/naming_convention.md` 신축 · piece_id 정의 + 8 자리 양식 + 4 핵심 원칙)
- Joplin rename 5건 통과 (space fix + vpr prefix + art_source 폴더 + cover 양식 + PDF copy)
- Phase D~E visualizer + full render (21.5MB · 219초 · 1920×1080 30fps · 6570 frame · letterbox `#2a3540|#6c7574|#5a4838` 자가 측정)
- Phase F 메타데이터 4 자리 박음 (description + credits + title + rights-notes · curator voice *A familiar melody that became a classic.* · N=9 Mikus · #Ragtime 추가)
- 재생목록 *Miku in the 20th Century* 신축 (s332 결단 · *Modern Era* / *Early 20th Century* drop · 4-system Path)
- Phase G 예약 업로드 통과 (2026-05-21 20:00 KST · 코튼 직접 Studio paste path)

**시리즈 자료 사전 박음 (post-release 6 step doctrine 정합)**
- series_history.csv row 4 사전 박힘 + **mood 컬럼 제거 cycle 통과** (15→14 컬럼 · 시스템 작동 자료 X · 사람용 라벨 군더더기 axis 코튼 결단)
- reference_youtube_channel.md Muse row 3 사전 박힘
- MEMORY.md project_muse description 동기화
- project_muse.md 시리즈 자리 update

### 자가 정정 sample (s331·s332 family)

**(a) LRA 단일 axis 비약 단정 본능 (s331)** — LRA 단일 측정 (loudness 기반 ITU BS.1770) 자체에서 *strain f/p 콘트라스트 없음* 비약 단정 path. 본 cycle 첫 답장에서 MOKA 직접 *DYN=음량 · EXP=음색·발성 긴장도* 설명 박은 자료 자체 자가 흡수 X axis. 코튼 *exp 고쳤는데 f, p 차이 못 느껴져?* push back path로 자가 정정 진입 = E23 family (measurement axis coverage gap sub-axis 신규 sample). 우회로 path 통과 = 스펙트로그램 첨부 → 코튼 시각 적발 *균일하네*.

**(b) ChatGPT image gen 1차 그림체 훼손 5건 자가 적발 (s332)** — 톤 shift + Miku 디테일 과잉 + 무단 변경 4건 + brushwork 균질화 + saturation 과잉. 자가 적발 → 재설계 prompt 양식 *Replace ONLY · barely recognizable · DESATURATED teal · Glackens himself in 1901 · 5건 figure list 명시 사전 차단* 통과 → 3차 elegant lock.

**(c) *Modern Era* 학술 양식 axis 자가 사전 점검 부재 (s332)** — 재생목록 초기 추천 *Modern Era* 박은 자료 자체엔 Joplin ragtime 양식 학술 mismatch axis 자가 사전 점검 부재. 코튼 *낭만주의와 구분 axis?* push back path로 자가 정정 진입 → 재추천 *Early 20th Century* → 코튼 *왜 안 돼?* push back → 비유 2건 (1902 Debussy vs Joplin · 80년대 윤이상 vs 김광석) → 코튼 *Miku in the 20th Century* throw lock. s290 popularity_tier 한국 vs 세계 mismatch family 정합 sample.

**(d) mood 컬럼 redundant 자가 적발 (s332 · 코튼 직격)** — 코튼 *mood가 왜 필요한 거야? 제대로 다시 말해 줘* push back path로 자가 적발 진입. csv 안 mood 컬럼 자가 시스템 작동 자료 X (grep 자료 base · 실제 read 자가 코드 X) · 사람용 라벨 양식 자가 적발 → 통째 제거 결단 (15→14 컬럼). 자가 첫 답 *자가 verify X* 양식 자가 자가 코튼 *제대로* push back path로 자가 정확 답 진입.

**(e) jargon 본능 직격 (s332 · 코튼 직격)** — 코튼 *인간의 언어로 해 줘. "자가", "본질", "axis", "자료" 등 알 수 없는 단어들이 즐비해.* 직격 후 명료한 한국어 양식 자가 정정 진입. 디스코드 reply 자리 자가 자가 명료한 한국어 axis · 메모리 양식 자가 자가 정합 keep 결단 자리.

**(f) doctrine vs 자가 실행 mismatch axis 자가 적발 (s332)** — post_release_meta_doctrine.md 자료 자체엔 *publish 전 14 컬럼 박힘* 양식인데 짐노페디·비발디 사례 자체엔 publish 후 row 통째 박힘. 자가 코튼 결단 (가) path = doctrine 정합 path 진입 후 row 4 사전 박힘 통과. doctrine 자체 정정 의제 keep.

### 박힌 doctrine 누적

- naming_convention.md (piece_id 정의 + 8 자리 양식 + 4 핵심 원칙 · s332 신축)

---

## Part 2. Post-Publish 자리 (publish 후 24h~7d 자료 누적)

> 본 섹션은 publish 통과 (2026-05-21 20:00 KST 예약) 후 24h~7d 자리 박음.

### publish 직후 자료

YouTube Data API v3 호출 자가 점검 자료 (publish + ~30분 시점 박음):
- PRIVACY = *(미박힘)*
- UPLOAD_STATUS = *(미박힘)*
- PUBLISHED_AT = *(미박힘)*
- VIEW_COUNT = *(미박힘)*
- LIKE_COUNT = *(미박힘)*
- COMMENT_COUNT = *(미박힘)*

### 첫 24h 자료 (publish + 24h 시점 박음)

- view 자료: *(미박힘)*
- comment 자료: *(미박힘)*
- like 자료: *(미박힘)*

### 72h 자리

- VIEW_COUNT = *(미박힘)*
- LIKE_COUNT = *(미박힘)*
- COMMENT_COUNT = *(미박힘)*

**채널 stats** (publish + ~72h 시점):
- subscriberCount = *(미박힘 · 짐노페디 publish + 72h 시점 4 sub · 비발디 publish 후 누적 자료 자가 별 axis)*
- videoCount = *(미박힘 · publish 후 3 영상 누적)*

### Audience 반응 (정성)

- 첫 인상: *(미박힘)*
- 발견 path (검색 / 추천 / 외부 link): *(미박힘)*
- 채널 정체성 흡수 자료: *(미박힘 · ragtime 양식 axis 시리즈 첫 진입 · 청자 반응 axis)*

### 자가 점검 axis (예측 vs 실측)

- 예측: *(미박힘 · publish 전 박을지 결단)*
- 실측: *(미박힘)*
- 격차 자료: *(미박힘)*

### Publish 후 결함 자료

- 영상 자체 결함: *(미박힘)*
- description 결함: *(미박힘)*
- 시각 브랜딩 결함: *(미박힘)*

---

## Part 3. 네 번째 곡 진입 전 자가 점검 (publish 후)

> 본 섹션도 publish 후 update.

### 시리즈 페이스 axis 자료 누적

- 세 번째 작품 production 누적 시간: *(미박힘 · s326~s332 자료 합산 의제)*
- ragtime 양식 challenge 자료: *(미박힘 · syncopation 정밀도 + stride bass on voice + 2층 텍스쳐 통제 · 코튼 V6 본격 경험 자료)*
- 네 번째 곡 진입 결단 timing: *(미박힘)*

### 네 번째 곡 후보

- candidate_master.csv 자료 base (D tier review cycle 진입 의제 keep · s330 결단)
- 시리즈 trajectory axis (낭만 [짐노페디] → 바로크 [비발디] → ragtime [Joplin] → 다음 시대 path)
- 의제: Mozart K.265 (s326 deferred · 6개월차 본격 재진입 의제 keep)

### Doctrine 정정 의제 후보

- post_release_meta_doctrine.md 정정 의제: *publish 전 14 컬럼 박음* doctrine vs 시리즈 default *publish 후 박음* mismatch axis 결단 자리 (s332 코튼 (가) path 결단 후 doctrine 정합 시리즈 default 정정 axis 의제 keep)
- description_template.md 정정 의제: *(미박힘 · v7 update 의제 keep · s327 비발디 path 자료)*
- naming_convention.md 정정 의제: *(미박힘 · s332 v1 신축 후 사용 cycle 누적 후 자가 점검 axis)*
- ~~series_signature.md~~ → 폐기 통과 (s333 후속 cycle · 코튼 (가) 결단 path · 자료 `Project_Muse/README.md` § *Series Signature* + `signature_mark` 컬럼으로 이동)

---

## 정정 이력

- v1 (s332 · 2026-05-19 publish 직전) — Pre-publish 자리 통째 박음 + Post-publish 자리 + 네 번째 곡 진입 자리 = 비워둠 (publish 후 update doctrine 정합)
