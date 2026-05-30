# YouTube Description Template — Atelier Miku Acappella

> Atelier Miku Acappella 시리즈 YouTube 영상 description 정본 템플릿.
> 매 작품 description 박을 때 본 template 따라 가변 자리 4건만 채움.
> 박힌 날짜: 2026-05-14 (s292) · v2 update (s295) · v3 update (s303 — Crypton 라이선스 정합 강화) · v4 update (s303 — Block 3 압축) · v5 update (s303 — Block 3·4 swap, 면책 footer 격리) · v6 update (s310 — 일본 청중 유입 해시태그 4건 추가) · v7·v8 update (s339 — No-AI 줄 제거 + 제작툴 라벨) · v9 update (s340 — 영상 제목 Acappella 키워드 양식) · v10 update (s348 — 제목 앞 브래킷 양식 `[Miku Acappella] 작곡가 - 곡명`) · v11 update (s351 — 해시태그 로케일-퓨어 재설계: 공유 이중언어 블록 폐기 → 로케일별 네이티브 라인 + 네이티브 미쿠 front + 다이어트) · v12 update (s355 — 영상 제목 `(feat. 初音ミク)` 후치 양식 · 브래킷/Acappella 폐기 · reveal 설계) · v13 update (s374 — Production tool 줄에 Voicebank 명시: 양식 (A) 두 필드 한 줄 `VOCALOID6 / Voicebank: Hatsune Miku V6` · 에디터·보이스뱅크 layer 분리)
> 첫 작품 자료: [`works/gymnopedie_1_first_proof/video/release/description.md`](../../../works/gymnopedie_1_first_proof/video/release/description.md)

## 4 블록 양식

YouTube description은 4 블록 + 구분선 `—` 양식으로 박음. Block 1·3·4 = anchor (매 작품 동일) / Block 2 = variable (작품별 가변).

```
{영상 제목 — YouTube title 자리에 박음, description 본문에는 X}

[Block 1 — anchor]
Welcome to Atelier Miku Acappella!

This is a fan project: classical music, arranged for Hatsune Miku's voice, one piece at a time.
Hope you find something to love here ♪

—

[Block 2 — variable]
{작곡가} - {곡명} ({작곡 연도}). {N} Mikus sing it now.

Cover art, after {화가}, '{명화 제목}' ({명화 연도}).
{명화 출처 URL}

—

[Block 3 — anchor]
Subscribe to join the Atelier and discover a new side of classical music!

—

[Block 4 — anchor]
Production tool: VOCALOID6 / Voicebank: Hatsune Miku V6
Hatsune Miku, © Crypton Future Media, Inc. — CC BY-NC 3.0 https://creativecommons.org/licenses/by-nc/3.0/

[EN] #HatsuneMiku #Acappella #{곡명EN} #初音ミク #Vocaloid #ClassicalMusic #ClassicalCover #{시대EN} #{작곡가성EN} #AtelierMikuAcappella
[JP] #初音ミク #アカペラ #{곡명JP} #ボカロ #ボカロカバー #クラシック #{시대JP} #{작곡가JP} #AtelierMikuAcappella
[KO] #하츠네미쿠 #아카펠라 #{곡명KO} #初音ミク #보컬로이드 #클래식 #{시대KO} #{작곡가KO} #AtelierMikuAcappella
```

## 가변 자리 4건

매 작품 description 박을 때 채울 자리 4건만:

### 1. 영상 제목 (YouTube title)
```
{작곡가} - {곡명} (feat. 初音ミク)
```
예: `Erik Satie - Gymnopédie No. 1 (feat. 初音ミク)`

현지화 제목 (JP/KR · `Analytics/youtube_meta.py set-title --default --en --ko --ja` 한 명령):
- JP: `{작곡가JP} - {곡명JP} (feat. 初音ミク)` 예: `エリック・サティ - ジムノペディ第1番 (feat. 初音ミク)`
- KR: `{작곡가KR} - {곡명KR} (feat. 初音ミク)` 예: `에릭 사티 - 짐노페디 1번 (feat. 初音ミク)`

양식 결단 (s355 · 코튼 · v10/s348 앞 브래킷 supersede):
- `{작곡가 풀네임} - {곡명} (feat. 初音ミク)` 후치 양식. **제목에 "Acappella" 없음** = 채널명+태그가 담고, 영상이 acappella를 *reveal* (curiosity-gap 설계 · 스펙시트 X · 평가 모드 → 발견 모드).
- feat. 크레딧 = **전 로케일 `初音ミク`** (정체성 마크 · 검색 키워드 X). 검색≈0 + 썸네일>>제목(s352)이라 제목 키워드 위치는 레버 아님 · 로마자/한글 미쿠는 태그·설명·해시태그가 담당.
- 곡명 = 시장 canonical (원어가 세계표준이면 원어 [Salut d'Amour·Gymnopédie] · 현지표준 있으면 현지 [四季 春·사계 봄]).
- defaultLanguage=en + en/ko/ja 현지화 set (한 명령 push).
- **정본 규칙 = `planning/title_naming_guide.md` (s355 재작성 · 근거 3축 + 포맷 history).**

### 2. 작품 헌사 (Block 2 첫 줄)
```
{작곡가} - {곡명} ({작곡 연도}). {N} Mikus sing it now.
```
예: `Erik Satie - Gymnopédie No. 1 (1888). Seven Mikus sing it now.`

가변 양식:
- 작품 라벨 양식 = YouTube title의 `{작곡가} - {곡명}` core와 일관 (`(feat. 初音ミク)` 크레딧 suffix 제외 · display label 연속성)
- *(연도)* 괄호 = cover art *(명화 연도)* 와 평행 (미술관 라벨 양식 통일)
- N = 합창 미쿠 수 (Seven / Five / Three 등 영어 단어 양식 keep)
- N=1 변형: `Hatsune Miku sings it now.` (단수 처리)
- *now* 단어 = 시간 가교 anchor (작곡 연도 → 현재). 양식 keep

### 3. Cover art (Block 2 둘째·셋째 줄)
```
Cover art, after {화가}, '{명화 제목}' ({명화 연도}).
{명화 출처 URL}
```
예:
```
Cover art, after Whistler, 'Nocturne in Blue and Gold: Old Battersea Bridge' (1872–75).
https://www.tate.org.uk/art/artworks/whistler-nocturne-blue-and-gold-old-battersea-bridge-n01959
```

가변 양식:
- *Cover art, after* = 미술사 정본 표기 (원작 차용 + 변형 axis 박음)
- 화가 = 성만 (Whistler, Vermeer, Monet 등)
- 명화 제목 = 단일 인용부호 `'...'`
- 연도 = en dash `–` (1872–75)
- 출처 URL = 미술관 공식 사이트 우선 (Tate / Met / Louvre 등)

### 4. 해시태그 — 로케일-퓨어 (Block 4 마지막 줄) · v11(s351)

v11부터 **공유 이중언어 블록 폐기**. 설명을 로케일별로 서빙하니 해시태그도 로케일별 네이티브 라인으로 분리한다 (한 로케일 안에 타 언어 태그 = 슬롯 낭비 + 분류기 혼선). 라인 = **앞 3개(영상 제목 위 노출) `[네이티브 미쿠][네이티브 포맷][작품]` + 꼬리 `[유니버설 #初音ミク][플랫폼][장르][커버][시대/장르 가변][작곡가][브랜드]`**.

| 슬롯 | EN | JP | KO |
|---|---|---|---|
| ① 미쿠 (front·노출) | #HatsuneMiku | #初音ミク | #하츠네미쿠 |
| ② 포맷 (front·노출) | #Acappella | #アカペラ | #아카펠라 |
| ③ 작품 (front·노출) | #{곡명EN} | #{곡명JP} | #{곡명KO} |
| ④ 유니버설 앵커 | #初音ミク | (①이 곧 앵커) | #初音ミク |
| ⑤ 플랫폼 | #Vocaloid | #ボカロ | #보컬로이드 |
| ⑥ 장르 | #ClassicalMusic | #クラシック | #클래식 |
| ⑦ 커버 | #ClassicalCover | #ボカロカバー | (생략 · 플랫폼으로 대체) |
| ⑧ 시대/장르 가변 | #{시대EN} | #{시대JP} | #{시대KO} |
| ⑨ 작곡가 | #{작곡가성EN} | #{작곡가JP} | #{작곡가KO} |
| ⑩ 브랜드 | #AtelierMikuAcappella | (동일) | (동일) |

→ 로케일당 **EN 10 / JP·KO 9개** (15 한도 한참 아래 = 곡별 실험 여유).

**다이어트 결단 (v11):**
- `#VOCALOID` 삭제 — 대소문자 무시라 `#Vocaloid`와 동일 페이지 = 순수 중복.
- `#Vocaloid6` 해시태그에서 제거 → 백엔드 키워드 태그로 (니치 · craft 신호는 백엔드 자리).
- `#Cover` → 로케일별 뾰족한 커버 태그(`#ClassicalCover` / `#ボカロカバー`)로 교체 (전 세계 팝·K팝 커버와 분리). KO는 커버 슬롯 생략하고 플랫폼(`#보컬로이드`)으로.

**가변 양식:**
- 작곡가성/작품/시대 = 로케일 네이티브 스크립트 (EN Latin / JP Katakana·Kanji / KO Hangul). 작품·시대명은 시장 canonical.
- 시대 슬롯은 장르가 더 정확하면 장르로 (예: 조플린 = `#Ragtime` / `#ラグタイム` / `#래그타임`).
- 작품 다중 단어는 합본 (e.g. `#TheEntertainer` · `#SalutDamour`).
- 앞 3개 = 영상 제목 *위* 노출 자리라 채널 차별점(미쿠·아카펠라) front-load (제목엔 이미 곡명이 있으니 곡명보다 미쿠·포맷 우선)·EN/KO 미쿠 슬롯은 네이티브 스크립트(#HatsuneMiku/#하츠네미쿠), JP는 #初音ミク.

## 백엔드 태그 (Studio '태그' 칸 · v11 cycle s351)

해시태그와 별개 = Studio 영상 세부정보 하단 **태그 칸** (최대 500자 · **전 로케일 공유 단일 칸** · 가중치 낮음). 전략 = *오타·약어·동의어·3국어 융합* 안전망 (정확 좌표는 제목·해시태그가 잡음 · 키워드 스터핑 X). 강한 것 앞 배치(앞 태그 약간 더 비중). 영상당 = **공통 베이스 + 곡별** 통째 붙여넣기 (≈350~370자 · 500 여유).

**공통 베이스** (매 영상 동일):
```
Hatsune Miku, Miku, 初音ミク, 하츠네미쿠, 미쿠, ミク, miku acappella, Vocaloid, Vocaloid6, V6, ボカロ, 보컬로이드, 보카로, Acappella, Acapella, a cappella, 아카펠라, アカペラ, Classical Music, Classical, 클래식, クラシック, Cover, 커버, カバー, vocaloid cover, ボカロカバー, Atelier Miku Acappella
```

**곡별** (베이스 뒤 `, ` 이어붙임 · 작곡가 풀네임+성 EN/KO + JP 카타카나 + 곡명 3국어 + 이명/합본/오타):
- 짐노페디: `Erik Satie, Satie, 에릭 사티, 사티, サティ, Gymnopedie, Gymnopédie, gymnopedie no 1, 짐노페디, ジムノペディ`
- 비발디 봄: `Antonio Vivaldi, Vivaldi, Vivardi, 안토니오 비발디, 비발디, ヴィヴァルディ, The Four Seasons, Four Seasons, Spring, 사계, 사계 봄, 봄, 四季, 四季 春`
- 조플린: `Scott Joplin, Joplin, 스콧 조플린, 조플린, ジョプリン, The Entertainer, Entertainer, 엔터테이너, エンターテイナー, Ragtime, 래그타임, ラグタイム`
- 사랑의 인사: `Edward Elgar, Elgar, 에드워드 엘가, 엘가, エルガー, Salut d'Amour, Salut damour, Love's Greeting, Liebesgruss, 사랑의 인사, 愛の挨拶`

**핵심 안전망** = 흔한 오타(`Acapella` p1개 · `Vivardi`) + 띄어쓴 철자(`a cappella`) + 이명(`Love's Greeting`/`Liebesgruss` · `Four Seasons`) + 로마자↔원어 쌍.

라이브 적용 = Studio 태그 칸에 베이스+곡별 붙여넣기 (s340 17개 태그 **supersede** · 코튼 Studio 수동). `youtube_meta.py`는 태그 write 미구현(set-title/thumbnail만).

## 업로드 기본 설정 (Studio Upload Defaults · s351)

신규 업로드에 자동 적용될 **기본 설명 + 기본 태그**를 Studio *설정 → 업로드 기본값*에 미리 채워둔다 (매 업로드 공통 부분 재입력 제거). 단 기본값은 **default 언어(en)만** 적용 = JP/KO 현지화 제목·설명은 곡마다 별도 (Studio 자막 또는 `youtube_meta.py set-description` [예정]). 태그 칸은 로케일 공유라 기본값 = 공통 베이스, 곡별은 업로드 후 append (또는 `set-tags`로 통짜 push).

**기본 태그** (= 백엔드 공통 베이스 그대로):
```
Hatsune Miku, Miku, 初音ミク, 하츠네미쿠, 미쿠, ミク, miku acappella, Vocaloid, Vocaloid6, V6, ボカロ, 보컬로이드, 보카로, Acappella, Acapella, a cappella, 아카펠라, アカペラ, Classical Music, Classical, 클래식, クラシック, Cover, 커버, カバー, vocaloid cover, ボカロカバー, Atelier Miku Acappella
```

**기본 설명** (en skeleton · `[ ]` = 곡별 채움):
```
[큐레이터 보이스 — 곡 분위기 한 줄]
[작곡가 풀네임] - [곡명] ([연도]). [N] Mikus sing it now.

Cover art, after [화가 성], '[명화 제목]' ([연도]).
[명화 출처 URL]

—

Production tool: VOCALOID6 / Voicebank: Hatsune Miku V6
Hatsune Miku, © Crypton Future Media, Inc. — CC BY-NC 3.0 https://creativecommons.org/licenses/by-nc/3.0/

#HatsuneMiku #Acappella #[곡명] #初音ミク #Vocaloid #ClassicalMusic #ClassicalCover #[시대] #[작곡가성] #AtelierMikuAcappella
```

- 스킬레톤 = s346(엘가) 진화형 = 큐레이터 보이스 + 작품 헌사 + cover art + footer (Welcome 블록·Subscribe CTA 없음). Welcome 블록 복원 원하면 맨 위 추가 (코튼 결단 · 옛 template Block1/Block3 reconciliation 자리).
- footer(Production tool + © 라인) = 유일한 완전 고정 텍스트 = 기본값 핵심 가치 (매번 재입력 제거).
- 곡별 `[ ]` 채워 default(en) 완성 → JP/KO 현지화는 별도 set.

## Anchor 자료 (변경 시 시리즈 통째 정합 회복 의제)

### Block 1 — 채널 환영
- *Welcome to Atelier Miku Acappella!* — 첫 줄 환영 인사
- 정체성 1줄 — *fan project · classical music · for Hatsune Miku's voice · one piece at a time*
- *Hope you find something to love here ♪* — 따뜻한 closing + ♪ 음표 시그너처 (♪ 앞 공백 1칸 박음)

### Block 3 — CTA (v7 — No AI 줄 제거)
- *Subscribe to join the Atelier and discover a new side of classical music!* — 구독 유도 + Atelier 소속감 + new side discovery axis (v2 신축 자료 · v5 swap으로 Block 3로 이동)
- ~~*No AI for music — every note placed by hand in Vocaloid6 Editor.*~~ — v7 (s339) 제거 (코튼 결단 · 3곡 라이브 전부 이미 제거 상태 정합). 본질 = 작업 본질(손 작업·음악 AI 미사용) 명시 줄. 신호 남기려면 고정 댓글/채널 정보로 이전 선택지.

### Block 4 — 제작 크레딧 + 의무 표기 + 해시태그 footer (v8)
- *Production tool: VOCALOID6 / Voicebank: Hatsune Miku V6* — v8 (s339) 신축 + v13 (s374) Voicebank 필드 추가. 미니멀 제작 도구 크레딧 (손 조성 도구 명시 = AI 자동생성과 구분 신호) + 보이스뱅크 layer 분리. ja = `制作ツール：VOCALOID6 / ボイスバンク：初音ミクV6` / ko = `제작툴: VOCALOID6 / 보이스뱅크: 하츠네 미쿠 V6`. (v7에서 뺀 'No AI' 줄의 대체 자리. 문장형 craft 진술 후보 → 코튼 결단으로 미니멀 라벨 확정 · 깔끔함 우선. v13에서 vocaloid 커뮤 표준 양식 = 에디터(Yamaha VOCALOID6) ↔ 보이스뱅크(Crypton Hatsune Miku V6) 분리 박음.)
- *Hatsune Miku, © Crypton Future Media, Inc. — CC BY-NC 3.0 https://creativecommons.org/licenses/by-nc/3.0/* — 자료 §3.2 의무 표기 (저작자 표시 + 라이선스 원문 URL)
- 해시태그 줄 — **v11(s351) 로케일-퓨어**: 로케일별 네이티브 라인 (EN 10 / JP·KO 9개). 앞 3개 = `[네이티브 미쿠][네이티브 포맷][작품]` 노출 + 꼬리 = 유니버설 #初音ミク · 플랫폼 · 장르 · 커버 · 시대/장르 · 작곡가 · 브랜드. (공유 이중언어 블록 폐기 · #VOCALOID/#Vocaloid6/#Cover 다이어트. 상세 = 가변 자리 #4.)

v5 swap 본질 = 면책 wording을 가장 마지막 *footer 자리*로 격리 (시청자 진입 장벽 격하 + 시각적 가벼움). 면책 + 해시태그 한 footer 자리에 합본해서 *법적 wording 격리* axis 박음.

### v4에서 빠진 자리 (v4 압축 결단 keep · 자료 history 자리)
- *A non-commercial fan project.* — CC BY-NC 자체가 비상업 명시 자리 → 중복 표기 자리. 빼는 결단.
- *This video is published under the Standard YouTube License.* — 영상 라이선스 옵션 자체가 verify 통과 자리 (Studio 안 박힘) → description 안 명시 의무 X. 시청자 오독 risk 사실상 X.
- *2007* 연도 자리 — 자료 §3.2 *예시* 안 박힌 자리. 의무 본질 = 저작자 표시 + 라이선스 원문 링크. 연도 자리 의무 X.

### URL 양식 정정 (v5)
- v3·v4 양식 = `CC BY-NC 3.0 (URL).` (괄호 + 마침표)
- v5 양식 = `CC BY-NC 3.0 URL` (괄호 X + 마침표 X)
- 이유: 시각적 가벼움 + URL 자체 자동 링크 검출 자리 (괄호/마침표 X로 자동 hyperlink 안전 axis)

## 점검 의제 결단 자료 (s292)

- (a) 작품 헌사 양식 — *{N} Mikus sing it now* default keep · N=1 시 `Hatsune Miku sings it now.` 변형
- (b) 명화 cover description 양식 — *Cover art, after {화가}* 정본 박음 (미술사 양식 정합)
- (c) 다국어 axis — en keep default · ko/ja 다국어는 자막 axis로 분리 (description은 en single)

## 라이브 서비스 keep doctrine

본 template = 라이브 서비스 (다음 곡들) 진입 시 그대로 keep. anchor 블록 (1·3·4) 변경 시 *시리즈 통째 정정* 본질이라 신중 결단 자리. 가변 자리 4건만 매 작품 채움.

## 정정 이력

- v1 (s292) — 첫 작품 짐노페디 description 자료 흡수 + 3 블록 양식 박음. 4 가변 자리 + 2 anchor 블록 + 점검 의제 3건 default 결단.
- v2 (s295) — 4 블록 양식 확장 (Block 4 = CTA 신축) + Block 2 첫 줄 양식 변경 ({작곡가 행위 = `wrote it in`} → {작품 라벨 = `- {곡명} ({연도})`}) + 해시태그 작품 분류 anchor #Cover 신축. 이유 = (1) closing layer 격리 (♪ closing + CTA closing) (2) YouTube title과 description 안 작품 라벨 양식 일관 (3) cover 콘텐츠 검색 노출 axis 추가.
- v3 (s303) — Crypton 라이선스 정합 강화 3축 update. 이유 = 코튼 결단 자리 (Hatsune Miku 라이선스 자료 audit 통과 · §3.2 CC 원문 링크 의무 + §5.1 주의 1 영상 옵션 명시 + cover art axis wording 정합). 변경 자리:
  - (1) Block 3 첫 줄 *No AI covers* → *No AI for music* (cover art는 AI 합성 axis · 음악 한정 명시 wording 회피)
  - (2) Block 3 면책 2 = CC BY-NC 3.0 + 원문 URL 명시 (자료 §3.2 *라이선스 원문 링크 제공* 의무 정합)
  - (3) Block 3 면책 3 신축 = *This video is published under the Standard YouTube License.* (자료 §5.1 주의 1 *CC-BY 옵션 절대 금지* doctrine 박음 · 시청자 오독 회피)
- v4 (s303) — Block 3 압축 결단. 코튼 *간소화 본질 axis* 결단 흡수 + Studio 라이선스 옵션 verify 통과 (*표준 YouTube 라이선스* 박힘) → description 안 면책 중복 자리 빼는 path. 변경 자리:
  - (1) *A non-commercial fan project.* 자리 빼기 — CC BY-NC 자체가 비상업 명시 자리, 중복 wording
  - (2) *This video is published under the Standard YouTube License.* 자리 빼기 — Studio 옵션 자체가 verify 통과 (시청자 오독 risk 사실상 X)
  - (3) *2007* 연도 자리 빼기 — 자료 §3.2 의무 본질 = 저작자 표시 + 라이선스 원문 링크. 연도 자리 의무 X
  - 결과: Block 3 = 4줄 → 2줄 (시청자 진입 장벽 격하). 자료 의무 통과 keep (저작자 표시 + CC 원문 URL).
- v5 (s303) — Block 3·4 swap 결단. 코튼 *시각적 가벼움 axis* 결단 흡수. 변경 자리:
  - (1) Block 3 = *작업 본질* + *Subscribe CTA* 합본 (CTA가 Block 4 → Block 3로 이동)
  - (2) Block 4 = *Crypton 의무 표기* + *해시태그* 합본 (의무 표기가 Block 3 → Block 4로 이동)
  - (3) URL 양식 정정 — `CC BY-NC 3.0 (URL).` → `CC BY-NC 3.0 URL` (괄호·마침표 X)
  - 본질 = 면책 wording을 가장 마지막 *footer 자리*로 격리. 시청자가 진입하는 자리 (Block 1·2·3)에는 환영·작품 정보·CTA만 박혀서 *시각적 가벼움 안전* + 면책은 footer 자리 (해시태그 위)에서 *대중이 쉽게 인식* 의무 통과 (자료 §3.2 정합).
- v6 (s310) — 일본 청중 유입 axis 해시태그 4건 추가. 코튼 결단 자리 (`#初音ミク + #ボカロ` 명시 + MOKA 추천 자료 자체 axis). 변경 자리:
  - (1) 채널 anchor 자리 = 6건 → 10건 (영문 6건 + 일본어 4건)
  - (2) 추가 자료 자체 = `#初音ミク + #アカペラ + #ボカロ + #VOCALOID` (#クラシック 자료 자체 #Vivaldi + #ClassicalMusic 자료 자체 mid 중복 axis 약하서 빼는 결단)
  - (3) 자리 자체 = 영문 양식 자체 옆 자체 mid 박는 path (`#HatsuneMiku #初音ミク` / `#Acappella #アカペラ` / `#Vocaloid #ボカロ #VOCALOID`)
  - 본질 = 일본 vocaloid 청중 axis 자체 자료 자체 = 영문 양식 검색 자체 자료 axis 자체 별도 자리. dilution risk 자료 자체 자체 axis 약 (별도 청중 자체 자료).
- v7 (s339) — Block 3 'No AI for music…' 줄 제거. 코튼 결단 (디스코드 s339). 변경 자리:
  - (1) Block 3 = 작업 본질 줄 제거 → Subscribe CTA 단독. 이유 = 3곡 라이브 전부 이미 해당 줄 제거 상태 (코튼 라이브 편집) + 명시적 제거 결단. 시청자 진입 자리 가벼움 axis.
  - (2) 작업 본질(음악 AI 미사용) 신호 필요 시 고정 댓글/채널 정보 이전 선택지 (description 밖 자리).
  - 주의 (미해결 drift): 본 template은 curator voice 양식 등 라이브 진화분과 추가 drift 존재 (Welcome 블록 optional + Subscribe 위치 + curator voice 1줄). 다음 곡 진입 전 full reconciliation 의제.
- v8 (s339) — Block 4 푸터에 제작 도구 크레딧 1줄 신축. 코튼 결단 (디스코드 s339). 변경 자리:
  - (1) Block 4 = `Production tool: VOCALOID6` + © 라인 + 해시태그. 크레딧 줄이 © 바로 위 footer 자리. (ja `制作ツール：VOCALOID6` / ko `제작툴: VOCALOID6`)
  - (2) v7에서 뺀 'No AI for music' (부정·방어형 · 맨 위 무거움)의 대체. 후보 = 문장형 craft 진술(`Every Miku voice tuned by hand…` · 調声 용어) → 코튼 *깔끔함 우선* 결단으로 미니멀 도구 라벨로 확정.
  - (3) 진입 자리(Block 1·2·3) 가벼움 keep + 제작 신호는 footer 자리. 채널 About은 prose라 라벨 미적용 (코튼 원본 환영문 keep · 영상 푸터 한정).
- v9 (s340 · 2026-05-22) — 영상 제목 양식 `(feat. Hatsune Miku)` → `(Hatsune Miku Acappella)`. SEO cycle A 감사 결단 (코튼 디스코드 s340). 변경 자리:
  - (1) 가변 자리 1 (영상 제목) = `feat.` 양식 폐기 → `Acappella` 키워드 양식. 라이브 3곡(짐노페디·비발디·조플린) 제목 전부 retrofit + 신곡부터 default. JP/KR 현지화 제목도 `（初音ミク アカペラ）` / `(하츠네 미쿠 아카펠라)` 양식 박음.
  - (2) 이유 = A 감사(라이브 메타데이터 직접 추출)에서 EN/JP/KR 제목 전부 채널 최대 적합 검색어 *Acappella/アカペラ* 부재 적발. 채널명은 *Atelier Miku Acappella* 인데 영상 제목엔 키워드 미표기 = 검색 발견성 손실.
  - (3) 부수 적발 (제목 양식과 별개 · backlog) = 3곡 카테고리 People&Blogs(22) 오설정 [→음악(10)] + 태그 0개. Studio 수동 fix 자리 (코튼 backlog).
- v10 (s348 · 2026-05-23) — 영상 제목 양식 `{작곡가} - {곡명} (Hatsune Miku Acappella)` → `[<미쿠키워드> Acappella] {작곡가} - {곡명}` (앞 브래킷 · 키워드 front-load · 코튼 결단). 변경 자리:
  - (1) 미쿠 키워드 로케일별 = EN `Miku` / KO `미쿠` / JP `初音ミク`(검색어라 풀네임 유지 · 최대 시장). EN/KO는 간결 (풀네임은 설명·태그·채널명에 잔존).
  - (2) 비발디 JP/KO outlier(성만+다른 틀) 정규화 = 작곡가 풀네임 - 곡명 통일.
  - (3) 라이브 4곡(짐노페디·비발디·조플린·사랑의 인사) 전부 코튼 Studio 적용 완료 + repo 동기화(title.txt·series_history.csv·description.localized.md·reference 메모리). 정본 규칙 = `planning/title_naming_guide.md` 재작성. 쓰기 자동화 = `Analytics/youtube_meta.py` (force-ssl).
- v11 (s351 · 2026-05-23) — 해시태그 로케일-퓨어 재설계 (코튼 디스코드 결단). 변경 자리:
  - (1) 공유 이중언어 블록(영문 6 + 일본어 4 = 한 줄 혼재) **폐기** → 로케일별 네이티브 라인 분리. 설명을 이미 로케일별 서빙하니 한 로케일 안 타 언어 태그 = 슬롯 낭비 + 분류기 혼선. `#初音ミク`만 유니버설 앵커로 전 로케일 keep.
  - (2) 다이어트 3종 = `#VOCALOID` 삭제(`#Vocaloid` 대소문자 중복) · `#Vocaloid6` 해시태그 제거→백엔드 키워드 · `#Cover` → 로케일 뾰족 커버(`#ClassicalCover`/`#ボカロカバー`).
  - (3) 앞 3개 재배치 = `[네이티브 미쿠][네이티브 포맷][작품]` (제목 위 노출 자리에 채널 차별점 front-load). EN/KO 미쿠 = `#HatsuneMiku`/`#하츠네미쿠`, JP = `#初音ミク`. 코튼 원안은 세 로케일 다 `#初音ミク` front였으나, EN/KO 네이티브 스크립트 복원이 로케일-퓨어 완성형 (MOKA 카브 · 코튼 수용).
  - (4) 다이어트로 푼 슬롯에 시대/장르 가변 + 로케일 네이티브 작곡가·작품 태그 추가. 결과 = EN 10 / JP·KO 9개 (15 한도 아래 여유). 비발디 작품태그 `#Spring`→`#FourSeasons`(범용 회피) · 조플린 시대슬롯=`#Ragtime`(장르=정확 좌표).
  - (5) 라이브 4곡 적용 = Studio 수동 끝줄 교체 (`youtube_meta.py`는 set-description 미구현 + 라이브↔repo 본문 drift라 태그만 바꾸는 surgical 변경은 수동이 안전). repo 정본(본 템플릿 + 4곡 `description.md`·`description.localized.md`) 동기.
  - (6) **백엔드 태그(Studio 태그 칸) 신설** = 해시태그와 별개 안전망 필드 (오타·약어·동의어·3국어 융합 · 500자 공유 단일 칸 · s340 17태그 supersede). 공통 베이스 + 곡별 = 본 템플릿 §백엔드 태그. Gemini 안 교차검증으로 합본(a cappella·Vivardi·이명 + 미쿠/V6/풀네임).
- v12 (s355 · 2026-05-25) — 영상 제목 양식 `[Miku Acappella] {작곡가} - {곡명}` → `{작곡가} - {곡명} (feat. 初音ミク)` (앞 브래킷 폐기 · feat. 후치 · 코튼 디스코드 결단). 변경 자리:
  - (1) 제목에서 "Acappella/アカペラ/아카펠라" 통째 제거 = **reveal 설계** (스펙 전부 공개 → 평가 모드 "생각대로/별로야" / "Acappella"를 영상 안에서 발견 → 발견 모드 "아 아카펠라구나!"). Acappella는 채널명+태그가 담당.
  - (2) feat. 크레딧 = 전 로케일 `初音ミク` 통일 (정체성 마크 · 검색 X). s351 해시태그 로케일-네이티브(#HatsuneMiku/#하츠네미쿠)와 **표면-역할 분리** (해시태그=검색 → 네이티브 / 제목 크레딧=정체성 → 아이코닉 初音ミク).
  - (3) 근거 = s352 데이터 (검색≈0 · 썸네일>>제목 CTR · 끝텍스트 검색무익 · 추천 65%) → 앞 브래킷 SEO front-load 베팅의 값 약화. launch 양식 `(feat. Hatsune Miku)` 후치로 회귀하되 크레딧만 `初音ミク`.
  - (4) 라이브 4곡 retrofit 완료 (`youtube_meta.py set-title` default+en/ko/ja 한 명령) + repo 동기(title.txt 4 · series_history.csv release_title 4 · description.localized.md 4 제목 · title_naming_guide.md 재작성 · 본 템플릿 §1). 정본 = `planning/title_naming_guide.md`.
- v13 (s374 · 2026-05-28) — Block 4 footer Production tool 줄에 **Voicebank 필드 추가** (코튼 디스코드 결단). 변경 자리:
  - (1) 양식 = (A) 두 필드 한 줄 슬래시 = `Production tool: VOCALOID6 / Voicebank: Hatsune Miku V6` (EN) · `制作ツール：VOCALOID6 / ボイスバンク：初音ミクV6` (JP) · `제작툴: VOCALOID6 / 보이스뱅크: 하츠네 미쿠 V6` (KR). 옵션 (B) 두 줄 / (C) 콤마 합본 후보 폐기 (footer 1줄 유지 + layer 정확성 balance).
  - (2) 이유 = v8 `Production tool: VOCALOID6`만 박혀서 *에디터*(Yamaha VOCALOID6)만 크레딧 · *보이스뱅크*(Crypton Hatsune Miku V6) 미표기 → "어느 미쿠 보이스뱅크"(V5/NT/V6) 누락 = craft 정밀도 ↓ + vocaloid 커뮤 청중 정보 결핍. © Crypton 줄이 "Hatsune Miku"는 박지만 V6 product는 미표기. V6 명시 = 사용 제품 정확 크레딧 + Crypton 의무 정합 강화.
  - (3) KR 라벨 = `보이스뱅크` (직역·명확) 선택. 후보 = `보컬` (짧음·범용) · `음원` (한국 "녹음물" 어감 risk라 폐기). JP `音源` = vocaloid 표준 용어 keep.
  - (4) 적용 = v8-정합 파일 12 슬롯 즉시 동기 (Elgar EN + Mozart EN + 5 localized.md × JP+KR). 라이브 5 영상 × 3 로케일 = 코튼 Studio 수동 교체 (`youtube_meta.py set-description` 미구현 · 라이브↔repo drift doctrine s351 = 태그만 바꾸는 surgical 변경 = 수동 안전). 짐노/비발디/조플린 EN description.md = stale v6/v7 drift (Production tool 줄 부재 + 옛 *No AI for music — every note placed by hand in Vocaloid6 Editor.* 잔존) → 별 scope 의제(코튼 결단 자리: reconcile vs drift keep).
