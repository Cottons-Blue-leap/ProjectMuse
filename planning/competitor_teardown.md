# WS2 — 선배 채널 경쟁 분석 (Competitor Teardown)

> 산출: 2026-06-10 · 로드맵 `planning/competitiveness_roadmap.md` WS2 (D2-a / D2-b).
> 데이터 출처: **YouTube Data API v3 (public)** 단일. 원본 응답 캐시 = `Analytics/competitor_raw.json`. pull 스크립트 = `Analytics/competitor_pull.py`.
> 모든 수치는 실 API 응답. fetch 안 된 항목은 "not retrieved"로 명시. 쿼터 사용 = 약 30 units (해결 fallback 2건 포함, 캐시 후 재호출 0).
> 측정일 = 2026-06-10. statistics(subs/views)는 측정 시점 절대값.

---

## 0. 채널 해결 결과 (resolve)

| 대상 | 해결 | channelId | 방법 | 비고 |
|---|---|---|---|---|
| EARLY MUSIC MIDI | ✅ | `UCL1xwMtUATV42V4bG8oawcw` | forHandle `@EARLYMUSICMIDI` | — |
| pikabonT | ✅ | `UCdUYxa4_OkG5jHGf86gqtjA` | forHandle `@pikabonT` | — |
| hamofanjoe | ✅ | `UCaFMa_h4HXJqNyypo98OPbA` | forHandle `@hamofanjoe` | — |
| Gnagre | ✅ | `UCuI7C8E48rt2MXj3LBMY_6Q` | forHandle `@gnagre3` | 실제 핸들 = **@gnagre3** (로드맵 표기 "Gnagre"는 별칭). 초기 검색 fallback이 동명이인 "Grégoire Dev55"를 잘못 잡아 핸들 수정함. |
| Bocaro Choir | ⚠️ **전용 채널 부재** | — | — | "Bocaro Choir" 라는 전용 보컬로이드 채널은 API로 검색·핸들 모두 부재. 유일한 흔적 = *"Ave Maria – Hatsune Miku with Bocaro Choir (Full Album)"* 1개 업로드가 **개인 음악 아카이브 채널 "Banana" (`@banana-ux7ff` / `UCWmPHv5kzr8sTSAT-y0cyHA`, subs 1,230 · 영상 4개 · 전부 잡다한 full-album 아카이브)** 에 존재. 이 채널 통계는 Bocaro Choir 작업물을 대표하지 않으므로 프로파일에서 제외. → **teardown 대상에서 사실상 제거** (코튼 검수 필요: 다른 플랫폼/비공개일 가능성). |

해결된 dedicated 채널 = **4**.

---

## 1. 채널별 프로파일

### 1-A. EARLY MUSIC MIDI  (`@EARLYMUSICMIDI`)
- **생성**: 2017-07-13 · **국가**: US
- **구독자**: **5,280** · **총 영상**: **889** · **총 조회수**: **1,821,153**
- **장르 좌표**: 르네상스·중세·초기 바로크 **다성 성악 복원** (early-music restoration). MAIKA/Miku 등 보컬로이드로 무명 폴리포니를 살림.
- **상위 10 영상** (조회순 · pull 300개 중 = 2022-12 이후분만; 전체 889 중 최신 300):

  | 조회수 | 발행 | 제목 |
  |---|---|---|
  | 7,970 | 2023-01-16 | Heinrich Isaac: Sanctus from "Missa Wohlauff Gsell von hinnen" a 6 (c.1496) |
  | 5,343 | 2023-05-05 | [New Rendition] Thomas Tallis: O sacrum convivium (1575) |
  | 5,277 | 2023-06-09 | Anonymous Italian: Bella gerit (c.1476) |
  | 5,207 | 2025-10-13 | Jean de Cambefort (?): Ouverture from 'Ballet Royal de la Nuit" (1653) |
  | 5,038 | 2025-06-24 | Michel Lambert: Ombre de mon amant (c.1660) |
  | 4,566 | 2025-05-28 | Jean-Baptiste Lully: Je languis nuit et jour (1670) |
  | 3,958 | 2025-05-31 | Jean-Baptiste Lully: Incidental Music from "Le Bourgeois Gentilhomme" (1670) |
  | 3,745 | 2025-05-19 | Anonymous Italian: Dolce mia cara e singular signora (c.1475) |
  | 3,516 | 2023-10-07 | Jacopo da Bologna: Fenice fu' e vissi (c.1350) |
  | 3,405 | 2023-12-24 | [New Rendition] Loyset Compère: Magnificat sexti toni (c.1480) |

  > 주의: pull 300개의 최고 조회수가 ~8K. 전체 889개 중 더 오래된(2022 이전) 영상의 상위는 not retrieved (쿼터 절약 · 최신 300개만 walk). 채널 lifetime 총 조회수(182만)/영상수(889) → 영상당 평균 ~2,049회.
- **제목 패턴**: `Composer: Work title (year)` 엄격 통일. 293/300 이 `작곡가:` 콜론 포맷. 일부 `[New Rendition]` 접두.
- **태그 패턴** (300개 distinct 182종, 상위): `vocaloid`(13) · `italian renaissance music`(10) · `villancico`(6) · `spanish renaissance music`(6) · `franco-flemish renaissance music`(6) · `english renaissance music`(5) · `vocaloid maika`(5) · 작곡가명(josquin, willaert, tallis…). → **음악학(시대·지역·장르) 태깅**, 검색-pop 키워드 아님.
- **업로드 케이던스** (pull 300 기준): 2023=94, 2024=85, 2025=91, 2026=26(6월까지). **연 ~85-94개 = 주 1.6~1.8개**. 가장 활발·꾸준한 발행자. 최신 업로드 2026-06-05 = **현재 활성**.
- **공급 지도 (repertoire)**: Isaac·Willaert·Josquin·Palestrina·Tallis·Senfl·Certon·Dufay·Machaut·Monteverdi·Telemann·Bach·Purcell·Handel. **거의 전부 르네상스~초기바로크.** 낭만/대중-클래식 워홀스 = 거의 0 (§3 참조).
- **다국어**: ❌. localized.title ≠ title = **0/300**. `defaultLanguage`는 en 268 + 곡 가사 언어(it/de/la/es) 분포일 뿐, 진짜 다로케일 현지화 아님. `defaultAudioLanguage`=en 300 통일.

### 1-B. pikabonT  (`@pikabonT`)
- **생성**: 2009-12-01 · **국가**: JP
- **구독자**: **306** · **총 영상**: **171** · **총 조회수**: **99,861**
- **장르 좌표**: **일본 남성합창(男声合唱) 보컬로이드 아카이브** — 특히 **多田武彦(다다 다케히코)** 합창 모음곡. 이질 보이스뱅크(KAITO/YOHIOloid/gackpoid) 콰르텟.
- **상위 10 영상**:

  | 조회수 | 발행 | 제목 |
  |---|---|---|
  | 3,425 | 2020-09-09 | アカシヤの径 ～多田武彦 グリークラブのための「ポピュラー・ソング・アルバム１」より第4曲 |
  | 2,766 | 2020-05-30 | 多田武彦 男声合唱組曲「柳河風俗詩・第二」 全6曲 |
  | 2,669 | 2023-06-10 | 多田武彦 男声合唱組曲「中勘助の詩から」 全7曲 |
  | 2,186 | 2022-02-05 | 多田武彦 男声合唱組曲「草野心平の詩から・第二」 全10曲 |
  | 2,067 | 2020-07-03 | 多田武彦 男声合唱組曲「雪国にて」 全6曲 |
  | 1,953 | 2023-04-17 | 多田武彦 男声合唱組曲「富士山」全5曲 |
  | 1,923 | 2019-02-25 | 多田武彦 男声合唱組曲「鳥の歌」 全7曲 |
  | 1,863 | 2020-10-18 | 多田武彦 男声合唱組曲「人間の歌」 全6曲 |
  | 1,842 | 2020-10-04 | 多田武彦 男声合唱組曲「父のいる庭」 全4曲 |
  | 1,811 | 2022-03-08 | ウクライナ民謡 コサックはドナウを越えて Їхав козак за Дунай |
- **제목 패턴**: 일본어, `作曲家 男声合唱組曲「작품」全N曲`. 검색-키워드 의식 없음.
- **태그**: distinct 55. `ボカロ`(124) · `vocaloid`(97) · `男声合唱`(82) · `多田武彦`(81) · 곡명. (105x = 자기 channelId 태그 = 노이즈.)
- **케이던스**: 2018=50, 2019=41, 2020=27, 2021=19, 2022=17, 2023=7, 2024=10. **하락세 → 최신 2024-08-27. 사실상 동면(현재 미활성).**
- **공급 지도**: 일본 근현대 합창(저작권 살아있는 多田武彦 d.2017 포함 — PD 아님!) + 일부 민요. **서양 클래식 PD 워홀스와 거의 무관.**
- **다국어**: ❌. localized 0/171. defaultLanguage=ja 171.

### 1-C. hamofanjoe  (`@hamofanjoe`)
- **생성**: 2013-12-07 · **국가**: not retrieved (None)
- **구독자**: **434** · **총 영상**: **61** · **총 조회수**: **660,890**
- **장르 좌표**: **기악→보컬 치환** 아카펠라. 주력은 **클래식 아님 = 애니/특촬 OP·ED·BGM**(World Trigger, 彼方のアストラ, おジャ魔女どれみ, ゼンカイジャー). 클래식·교회음악은 곁다리.
- **상위 10 영상** (= 채널 조회수 거의 전부가 애니송 1곡에 집중):

  | 조회수 | 발행 | 제목 |
  |---|---|---|
  | 377,549 | 2021-11-03 | ワールドトリガー3期OP「タイムファクター」フル / World Trigger S3 OP Full |
  | 94,432 | 2021-06-26 | 彼方のアストラ EDフル "Glow at the Velocity of Light" / Astra Lost In Space ED |
  | 46,633 | 2021-06-26 | 彼方のアストラ OP TVサイズ "star*frost" |
  | 28,209 | 2021-09-26 | 彼方のアストラ OP Full |
  | 24,614 | 2022-06-05 | おジャ魔女どれみBGMスーパーセレクション |
  | 11,333 | 2022-06-05 | おジャ魔女どれみ実用BGMセレクション |
  | 11,024 | 2021-11-13 | [1-2期版]ワールドトリガー3期OPフル |
  | 8,886 | 2021-05-04 | Zenryoku Zenkai! Zenkaiger Full - Acappella by vocaloids [初音ミク] |
  | 8,862 | 2021-05-08 | Zenkaiger Full - 同時再生：オリジナル＋ボカロアカペラ |
  | 8,455 | 2014-01-18 | Tenohira o taiyo ni (手のひらを太陽に) |
  > 1위 1곡(37.7만)이 채널 조회수(66만)의 57%. **단일 바이럴 의존 구조.**
- **태그**: distinct 16(빈약). `a cappella (musical genre)`(11) · `vocaloid (software genre)`(11) · christmas/gospel/queen/take6 산발. YouTube 자동 "(musical genre)" 라벨 의존.
- **케이던스**: 산발적(2013~2025), 연 1~15개 불규칙. 최신 2025-09-17 = 간헐 활성.
- **공급 지도**: 애니송 중심 + 소수 클래식/성가(Ave Maria류). **클래식 PD 워홀스 공급자 아님.**
- **다국어**: 부분적 = 제목에 **일/영 병기**(슬래시) 습관 있음(번역 아닌 병기). localized 필드 = 0/59. defaultLanguage ja 48 / en 11.

### 1-D. Gnagre  (`@gnagre3`)
- **생성**: 2012-02-25 · **국가**: not retrieved
- **구독자**: **77** · **총 영상**: **26** · **총 조회수**: **56,861**
- **장르 좌표**: **모차르트 오페라/성가 미쿠 아카펠라 단일 작가**. 단일 미쿠(젠더팩터). 2012~2014 짧은 활동 후 **종료(dormant)**.
- **상위 10 영상**:

  | 조회수 | 발행 | 제목 |
  |---|---|---|
  | 12,600 | 2014-02-15 | Mozart "Leck mich im Arsch," KV231, Hatsune Miku |
  | 4,688 | 2012-11-23 | Mozart KV527 "Don Giovanni a cenar teco m'invitasti," Hatsune Miku |
  | 2,983 | 2012-05-19 | Mozart KV620 Zauberflöte "Bei Männern welche Liebe fühlen" |
  | 2,827 | 2014-02-15 | Mozart KV339 5. Laudate Dominum, Vesperae solennes |
  | 2,786 | 2013-01-18 | Mozart KV620 "Pa-Pa-Pa", Die Zauberflöte |
  | 2,561 | 2012-03-20 | Mozart KV618 Ave Verum Corpus |
  | 2,518 | 2012-09-02 | Mozart KV492(Figaro) "Contessa perdono!" |
  | 2,232 | 2012-06-23 | Mozart KV527 Zerlina "Vedrai carino" |
  | 2,185 | 2013-04-13 | Mozart KV344 Zaide "Ruhe sanft" |
  | 2,057 | 2012-04-21 | Mozart KV620 "Pa-Pa-Pa" |
  > 1위 = 모차르트 풍자 캐논 (제목 자체가 바이럴 미끼). 나머지는 오페라 아리아/성가.
- **제목 패턴**: `Mozart KV### "aria," Hatsune Miku`. KV 번호 명기 = 클래식 매니아 검색 의식.
- **태그**: distinct 28. `mozart`/`モーツァルト`/`クラシック`/`初音ミク`/`ボカロ`(각 13) · `opera`(10) · `classical music`(7). **유일하게 영·일 키워드 균형 태깅** — 단 다국어 제목/현지화는 아님.
- **케이던스**: 2012=17, 2013=5, 2014=4. **2014-11 이후 정지(종료).**
- **공급 지도**: **모차르트 거의 전속** (오페라 아리아·성가·캐논). 26곡 전부 모차르트. 우리가 라이브로 1곡 가진 모차르트 영역과 직접 겹침.
- **다국어**: ❌. localized 0/26.

---

## 2. 교차 채널 종합 (vs 우리 — Atelier Miku A Cappella)

우리 채널 기준선(메모리 라이브 상태): 구독 **11** · 라이브 영상 **9곡 발행**(+예약) · **10로케일 현지화 메타** 전수 적용. (우리 절대수치는 본 API pull 대상 아님 — Studio/Analytics OAuth 별도.)

| 축 | EARLY MUSIC MIDI | pikabonT | hamofanjoe | gnagre3 | **우리 (Atelier)** |
|---|---|---|---|---|---|
| 구독 | 5,280 | 306 | 434 | 77 | 11 |
| 영상수 | 889 | 171 | 61 | 26 | 9 |
| 총 조회 | 1.82M | 99.9K | 660.9K | 56.9K | (별도) |
| 활성 | ✅ 현재 활발 | ⏸ 동면 | 간헐 | ⛔ 종료(2014) | ✅ 신생·활발 |
| 레퍼토리 | 르네상스 폴리포니 | 일본 남성합창 | 애니송>클래식 | 모차르트 오페라 | **낭만/대중 클래식 워홀스 + 명화** |
| 다국어 현지화 | ❌ 0 | ❌ 0 | 제목 병기뿐 | ❌ 0 | ✅ **10로케일** |
| 썸네일 정체성 | not retrieved | not retrieved | not retrieved | not retrieved | 명화+미쿠 시대 큐레이션 |

> 썸네일 패턴은 API thumbnails(자동 생성 URL)만 회수 가능 → 디자인 정체성은 수치화 불가. "not retrieved" 처리. (로드맵상 로케일별 썸네일은 이미 제거됨.)

### 핵심 인사이트 (Top 5)

1. **누구도 메타를 현지화하지 않는다 = 우리의 가장 확실한 해자.** 4개 dedicated 채널 전부 localized.title = **0**. 가장 큰 EARLY MUSIC MIDI(5,280구독)조차 영어 단일. 우리 10로케일 현지화는 씬에서 **유일**. (코튼 진단 "공방의 의의 = 글로벌 유통"을 데이터가 확인.)

2. **"선배"들은 우리와 레퍼토리가 거의 안 겹친다 — 같은 링이 아니다.** EMM=무명 르네상스, pikabonT=일본합창(게다가 저작권 살아있음), hamofanjoe=애니송, gnagre3=모차르트 전속·종료. **낭만·대중-클래식 워홀스(쇼팽 녹턴·파헬벨 캐논·사계·백조의 호수 등) = 이 선배군 거의 공백** (§3). 우리는 빈 칸에 들어가는 중 = 직접 경쟁자라기보다 **인접 씬**.

3. **꾸준한 발행 케이던스가 구독 규모와 직결.** 압도적 1위 EMM = 연 ~90개(주 1.7개) 4년 누적 889개 → 5,280구독. 종료/동면 채널(gnagre3 77, pikabonT 306)은 영상수 적고 traction 낮음. **WS4 "발행 케이던스 유지" 가설을 외부 데이터가 지지.** 우리 9곡 → 갈 길 멂, 하지만 방향은 맞음.

4. **단일 바이럴 의존은 취약.** hamofanjoe는 조회 66만 중 57%가 애니송 1곡(World Trigger OP). 클래식·아카펠라 정체성과 무관한 우연 히트 → 구독은 434에 그침(조회 대비 낮은 전환). **명확한 카탈로그 정체성(우리 명화+시대)이 우연 바이럴보다 구독 전환에 유리**함을 시사.

5. **태그=음악학 vs 검색-pop 두 갈래.** EMM/gnagre3는 시대·작곡가·KV번호 등 **전문 검색어** 태깅. 검색-pop 키워드("relaxing classical", "study music" 류)는 아무도 안 씀. → WS3 검색 정합에서 우리는 **전문 태그(작곡가/작품번호) + 대중 검색어** 둘 다 노릴 빈 공간이 있음.

> 한계 명시: 이 4채널은 **보컬로이드 클래식 아카펠라**라는 좁은 선행자 집합. YouTube 클래식-대중(피아노 커버·릴랙스 채널 등) 광역 경쟁장은 본 pull 범위 밖. 검색 갭(§3)은 "이 선배군 내 공급 부재"이지 "YouTube 전체 공급 부재"가 아님 — WS3 검색 자동완성 데이터로 보강 필요.

---

## 3. D2-b: 검색 수요↑ · (선배)공급↓ 곡 후보 shortlist

**방법**: 4 dedicated 채널의 전체 제목+공개 태그 코퍼스(556 영상분)에 대해 유명 PD 워홀스 키워드 ~80종을 occurrence 카운트. **0회 = 이 선배군 공급 공백**. 이를 우리 `candidate_master.csv`(366행) S/A tier와 교차 → **검색 갭이면서 이미 우리 파이프라인에 있는** 곡을 우선 플래그.

**선배군 공급 카운트 (titles+tags 코퍼스):**
- 공급 있음(>0): mozart 40 · bach 4 · handel 4 · pavane 4 · pachelbel 3 · ave maria 3 · verdi 3 · albinoni 2.
- **공급 0 (= 갭)**: 비발디 사계 · 베토벤(엘리제/월광/환희의송가/비창) · 쇼팽 녹턴 · 드뷔시 클레르드륀 · 사티 짐노페디 · 차이콥스키(백조·호두까기·1812) · 그리그 페르귄트 · 드보르자크 신세계/유모레스크 · 라흐마니노프 보칼리제 · 엘가(위풍당당·사랑의인사) · 비제 카르멘 · 푸치니 네순도르마 · J.슈트라우스 푸른도나우 · 홀스트 목성 · 생상스(백조·죽음의무도) · 로시니 윌리엄텔 · 마스네 타이스의명상 · 멘델스존 결혼행진 · 브람스(자장가·헝가리무곡) · 리스트(사랑의꿈·헝가리광시곡) · 슈베르트 세레나데 등 — **대중-검색 핵심 거의 전부.**

### Shortlist (검색 갭 ∩ 우리 candidate_master S/A tier)

이미 우리 큐레이션에 든 곡 = 선배 공급 0 = **검색 갭 우선 타깃**. (period = candidate_master 분류)

**S tier (최우선):**
| 곡 | piece_ko | period | 선배공급 |
|---|---|---|---|
| Gymnopédie No. 1 | 짐노페디 1번 (사티) | 20세기 | 0 |
| Clair de lune | 달빛 (드뷔시) | 20세기 | 0 |
| Spring I Allegro (Four Seasons) | 사계 봄 1악장 (비발디) | 바로크 | 0 |
| Swan Lake Theme | 백조의 호수 테마 (차이콥스키) | 낭만 | 0 |
| Nocturne Op. 9 No. 2 | 야상곡 9-2 (쇼팽) | 낭만 | 0 *(우리 이미 라이브 ⑥)* |
| Eine kleine Nachtmusik I | 아이네 클라이네 1악장 (모차르트) | 고전 | gnagre는 오페라만 → 이 곡 0 |
| Habanera / Toreador / Overture (Carmen) | 카르멘 (비제) | 낭만 | 0 |
| Nessun dorma (Turandot) | 공주는 잠 못 이루고 (푸치니) | 낭만 | 0 |
| Ave Maria (Schubert) | 아베 마리아 (슈베르트) | 낭만 | (선배=카치니/성가류 3, 슈베르트판 0) |
| Pomp and Circumstance No. 1 | 위풍당당 1번 (엘가) | 낭만 | 0 |
| New World Symphony II / IV | 신세계 2·4악장 (드보르자크) | 낭만 | 0 |
| Danse Macabre | 죽음의 무도 (생상스) | 낭만 | 0 |
| Brahms Lullaby | 브람스 자장가 | 낭만 | 0 |
| The Blue Danube | 푸른 도나우 (J.슈트라우스2세) | 낭만 | 0 |
| Hungarian Dance No. 5 | 헝가리 무곡 5번 (브람스) | 낭만 | 0 |
| Salut d'Amour | 사랑의 인사 (엘가) | 낭만 | 0 |
| Humoresque Op. 101 No. 7 | 유모레스크 (드보르자크) | 낭만 | 0 |
| William Tell Overture Finale | 윌리엄 텔 피날레 (로시니) | 낭만 | 0 |
| Hungarian Rhapsody No. 2 | 헝가리 광시곡 2번 (리스트) | 낭만 | 0 |

**A tier (차순위):**
The Swan (생상스) · Pathétique Adagio cantabile (베토벤) · Liebestraum No. 3 (리스트) · Jesu Joy of Man's Desiring (바흐) · Pavane pour une infante défunte (라벨) · Adagio in G minor (알비노니/지아조토 — 선배 albinoni 2회지만 이 곡 자체 0) · Greensleeves · Jupiter from The Planets (홀스트) · Concierto de Aranjuez Adagio (로드리고) · 사계 나머지 악장(여름/가을/겨울 다수).

### 권고 (candidate_master 반영안)
- `candidate_master.csv`에 **`search_gap` 메모/컬럼** 추가 (로드맵 D2-b 지시) → 위 S-tier 곡에 "선배군 공급 0" 플래그. popularity_tier 단독이 아니라 **검색 갭 축**으로도 선곡.
- **단, §2 한계**대로 "선배군 공급 0"은 YouTube 전체가 비었다는 뜻이 아님. 클레르드륀·짐노페디·사계는 광역 경쟁장에선 포화. → **이 갭 리스트는 "보컬로이드/아카펠라 니치 내 선점 기회"**로 해석하고, 광역 수요는 WS3 검색 자동완성으로 별도 검증해야 함.
- 가장 깨끗한 기회 = **낭만기 워홀스**(쇼팽·차이콥스키·드보르자크·엘가·생상스·비제). EMM(르네상스)·gnagre3(모차르트)·pikabonT(일본합창)·hamofanjoe(애니) 어느 채널도 낭만 대중곡을 안 함 = **선배 0, 우리 큐레이션 풍부.**

---

## 부록: 재현/검증

- pull 스크립트: `Analytics/competitor_pull.py` (`python Analytics/competitor_pull.py` 신규 pull / `--use-cache` 쿼터 0 재분석)
- 원본 API 응답 캐시: `Analytics/competitor_raw.json` (채널 statistics + 전 영상 snippet/statistics 원본)
- 교차참조: `planning/candidate_master.csv` (366행)
- 쿼터: 약 30 units 소비(forHandle 1u×다회 + search fallback 100u×0~2 시도 포함). 일일 free 10,000u 대비 무시 가능.
