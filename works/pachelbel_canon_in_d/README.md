# pachelbel_canon_in_d

Project Muse 7차 작품 (2026-05-30 진입 · 쇼팽 녹턴 Op.9-2 영상화 중 코튼·MOKA 공동 결단). 쇼팽 솔로 피아노 멜랑콜리 직후 **다성 카운터포인트 axis** + 시리즈 두 번째 **바로크 axis** (비발디 봄 이후 · 낭만 포화 해소) + 후보 마스터 **base_rank 1위** anchor. MOKA 1순위 추천 ↔ 코튼 *나도 캐논이 끌렸다* 자가 합치.

```text
piece: Canon in D major, P.37 (Johann Pachelbel)
composer: Johann Pachelbel (1653-1706)
year: c.1680~90 작곡 추정 (바로크 중기) · 현대 대중화 = Paillard 1968 녹음 이후
section: 통째 (~4-5분 · 발췌 없음 · 2마디 8음 ground bass 반복 위 3성부 캐논 + basso continuo · Canon만 · Gigue 제외 axis)
vocal: Hatsune Miku (모음/humming · 기악 원곡 = 가사 없음 · ground + 3 canon voice 다성 분배)
playlist: Miku in the Baroque Era (비발디 봄 1악장 공유 · 바로크 family 정합)
release title: Johann Pachelbel - Canon in D (feat. 初音ミク) · s355 후치 양식
cover art: ⚠️ csv 기본값 = Vermeer *The Music Lesson* (c.1662-65 · 미사용 화가 · 명화 중복 無) · 곡 만들고 결단
source PDF: music/source_scores/pachelbel_canon_in_d.pdf (Canon and Gigue P.37 · 1.84MB)
transcription: 코튼 V6 editor 직접 입력 (OMR 없음 · manual transcription default 정합)
```

## 결단 자료 (7차 곡 선정 lock · 2026-05-30)

- **선정 cycle 통과 자료**:
  - 쇼팽(⑥) 영상화 렌더 대기 중 코튼 *다음 곡 정해보자* 발화 → MOKA가 S급 후보표 + 시리즈 이력 전수 검토 → 아카펠라 적합성 1순위 렌즈로 추천 3안 정리.
  - MOKA 1순위 = 파헬벨 캐논 D장조 (base_rank 1위 · 바로크 · S) → 코튼 *마침 나도 캐논이 끌렸다* 자가 합치 → 확정.
  - 추천 대안 (방향별 keep): (B) 바흐 G선상의 아리아 (또 한 곡 숭고한 지속음 · 녹턴 직후 유사 risk) / (C) 베토벤 환희의 송가·드보르자크 신세계 피날레 (무드 전환 고양) / 보류 큐 = 그리그 아침의 기분 (⑥에서 7~8번째로 미룬 곡 · 여전히 테이블).

- **선정 axis 4건**:
  1. **아카펠라 정면승부 axis** = 곡의 본질이 *그라운드 베이스 위 성부가 겹겹이 쌓이는 캐논* → 다중 미쿠 아카펠라의 교과서적 정합 (시리즈 최강 구조 핏). 후보표 매칭 사유 "layered voices".
  2. **바로크 시대 분산 axis** = 비발디 봄 이후 두 번째 바로크 · 낭만 3곡(사티·엘가·쇼팽) 포화 해소.
  3. **무드 대비 axis** = 쇼팽 녹턴(잔잔·멜랑콜리·솔로피아노) 직후 따뜻·고양·다성 카운터포인트로 호흡 전환.
  4. **세계 axis S tier anchor** = base_rank 1위 · 결혼식·BGM·대중문화 최상위 인지도.

- **분량** = 통째 (~4-5분 · 발췌 없음 · Canon만 · 동봉 Gigue 제외 · family 정합).

- **명화** = ⚠️ csv 기본값 = Vermeer *The Music Lesson* (c.1662-65). 자가 사전 점검:
  - **중복 적발 = 無.** 기사용 화가 = Whistler(짐노페디·쇼팽 2회)·Botticelli(비발디)·Glackens(조플린)·Waterhouse(엘가)·Van Gogh(작은별). Vermeer 미사용 → conflict 없음.
  - 매칭 사유 = 가정 실내악 장면(정돈된 합주·겹치는 성부)이 캐논 구조와 직결.
  - ⚠️ **권리 nuance** = 작품 PD 강(Vermeer d.1675) BUT 소장처 Royal Collection Trust(영국)가 자기 복제 사진에 reproduction 권리 주장 가능(Tate·쇼팽 패턴 동일) → 깨끗한 소스 = Wikimedia Commons PD-Art 판 사용 · Royal Collection 자체 스캔 직접 scrape X. cover 합성 진입 시점에 art_sources/ 소스 url + rights-notes 박는 path.
  - 자가 후보 throw (대안 keep): (a) Vermeer *Girl Reading a Letter at an Open Window* (단 바흐 Air 후보와 동일 화가 — Air도 하면 Vermeer 2회 axis) (b) 그 외 바로크 가정 음악/합주 장면.
  - 코튼 결단 자리 = V6 본격 진입 후 (쇼팽 path 정합 · *곡 만들고 다시 봐* doctrine).

- **score** = candidates_opus `요한 파헬벨_캐논 in D.pdf` 통째 copy (Canon and Gigue P.37 · 1.84MB · V6 진입 시점 Canon만 picking[Gigue 제외] + edition_id 자가 점검 의제) · IMSLP PD 강.

## 다성 카운터포인트 양식 자료

- **ground bass + 캐논 texture** — 원곡 = 2마디 8음 ground bass (D-A-B-F#-G-D-G-A) 약 28회 반복 + 그 위 3 violin이 한 마디 간격으로 동일 선율을 캐논으로 쌓음. 미쿠 분배 axis = low_oo (ground bass 8음 반복) / lead_miku·mid_oo·halo_high (3성 캐논 entry 시차 쌓기) / air_mm (glue sustain). 쇼팽 5~6성부 ornamental 통과 → 캐논 = **시차 entry로 텍스처가 점층 누적되는 양식** (시리즈 첫 본격 카운터포인트 axis).
- **점층 누적 양식** — ground 위에 성부가 하나씩 들어와 점점 풍성해지고 후반 다시 비워지는 dynamic arc. 비주얼라이저(band-remap 신형)와 정합 강 (성부 누적 → 바 밀도 점층).
- **V6 challenge 자료** — 후반 16분·32분 음표 빠른 figuration passage = legato sustain 미쿠 양식과 tension axis · 코튼 결단 자리 (그대로 / 단순화). 단 화성은 8음 순환이라 simple keep.

## 시그너처 v3 wordmark 적용 자료

본 작품 = doctrine v3 default 양식 적용 (우하단 corner · 좌하단 title mirror · cream + *M* 청록 · text-shadow blur 12 · GFS Didot). 시리즈 anchor = `../../README.md` § *Series Signature* + `../../series_history.csv` `signature_mark` 컬럼 (wordmark_v3 default).

## 진행 자리

1. ✅ 곡 선정 결단 (2026-05-30 · 파헬벨 캐논 D장조 lock · MOKA 추천 ↔ 코튼 합치)
2. ✅ 작업 폴더 신축 (2026-05-30)
3. ✅ rights 자가 점검 통과 (별 doc 자리 X · 양식 부담 elevation 회피 doctrine 정합)
   - **Composition**: Pachelbel d.1706 · life+70 통과 · 전세계 PD 강
   - **Score**: IMSLP self-host PD · candidates_opus PDF copy 박힘 (edition_id 자가 점검 V6 진입 시점 keep · 가장 깨끗한 PD edition 우선)
   - **Cover Art**: ⚠️ csv 기본값 Vermeer *The Music Lesson* = 중복 無 · 작품 PD 강 · 소장처 reproduction 권리 nuance → Commons PD-Art 소스 사용 path · 코튼 결단 자리 keep (V6 진입 후)
   - **Decision**: `approved (composition · score) · cover 명화 = Vermeer 기본값 keep, 중복 無 (V6 진입 후 코튼 결단)`
4. ✅ score 통째 copy (`music/source_scores/pachelbel_canon_in_d.pdf` · 1.84MB · Canon and Gigue P.37)
5. ⏳ V6 editor 직접 입력 (코튼 자리 · **본격 진입 = 쇼팽(⑥) publish 통과 후 권고** [s359 doctrine] · 사전 진입도 코튼 자율)
6. ⏳ acappella-only skip (doctrine 정합)
7. ⏳ master = `music/masters/Miku_pachelbel_canon_in_d_master.wav`
8. ⏳ listening decision = 영상화 진행 승인
9. ⏳ 영상: 명화 결단 → 커버 합성 → visualizer 배선(s381 band-remap 신형 default) → 2K 렌더 → QC
10. ⏳ YouTube package + publish

## 시리즈 정합

- 시그너처 = `../../README.md` § *Series Signature* + `../../series_history.csv` `signature_mark` 컬럼 (wordmark_v3 default)
- 비주얼라이저 = **s381 band-remap 신형 default** (신곡 ⑥ 쇼팽부터 · `../../workflows/video_release/templates/visualizer-composition.s381-bandremap.tsx`) · gain은 곡별 결단 (쇼팽 = 2.0 lock)
- 제목 양식 = `../../planning/title_naming_guide.md` (s355 후치 양식)
- 라이선스 doctrine = `reference_muse_license.md` (Crypton PCL + B-4 YPP path 정합)
- playlist = *Miku in the Baroque Era* (비발디 봄 공유 · 시대 정합 강)

## 사전 점검 의제 (다음 cycle 자리 · 코튼 결단)

- **V6 입력 진입 timing** — 쇼팽(⑥) publish 통과 후 권고 (s359 doctrine). 그 전 진입 = 코튼 자율.
- **Canon picking 자리** — score PDF는 Canon and Gigue P.37 통째 · V6 진입 시점 Canon만 picking(Gigue 제외) + edition_id 자가 점검 의제.
- **명화 결단 자리** — Vermeer *The Music Lesson* 기본값 (중복 無) · 자가 대안 throw · V6 본격 진입 후 결단 자리.
- **figuration passage 양식 결단** — 후반 빠른 음표 passage = V6 양식 challenge · 코튼 결단 자리 (그대로 / 단순화).
- **고정 댓글 자료** = 다음 곡 예고 path (`次の曲：パッヘルベル「カノン」` 양식 · publish cycle 시점 박음).
