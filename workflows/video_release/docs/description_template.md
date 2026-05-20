# YouTube Description Template — Atelier Miku Acappella

> Atelier Miku Acappella 시리즈 YouTube 영상 description 정본 템플릿.
> 매 작품 description 박을 때 본 template 따라 가변 자리 4건만 채움.
> 박힌 날짜: 2026-05-14 (s292) · v2 update (s295) · v3 update (s303 — Crypton 라이선스 정합 강화) · v4 update (s303 — Block 3 압축) · v5 update (s303 — Block 3·4 swap, 면책 footer 격리) · v6 update (s310 — 일본 청중 유입 해시태그 4건 추가)
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
No AI for music — every note placed by hand in Vocaloid6 Editor.
Subscribe to join the Atelier and discover a new side of classical music!

—

[Block 4 — anchor]
Hatsune Miku, © Crypton Future Media, Inc. — CC BY-NC 3.0 https://creativecommons.org/licenses/by-nc/3.0/

#{작곡가성} #{곡명} #Cover #HatsuneMiku #初音ミク #Acappella #アカペラ #Vocaloid #ボカロ #VOCALOID #ClassicalMusic #AtelierMikuAcappella #Vocaloid6
```

## 가변 자리 4건

매 작품 description 박을 때 채울 자리 4건만:

### 1. 영상 제목 (YouTube title)
```
{작곡가} - {곡명} (feat. Hatsune Miku)
```
예: `Erik Satie - Gymnopédie No. 1 (feat. Hatsune Miku)`

### 2. 작품 헌사 (Block 2 첫 줄)
```
{작곡가} - {곡명} ({작곡 연도}). {N} Mikus sing it now.
```
예: `Erik Satie - Gymnopédie No. 1 (1888). Seven Mikus sing it now.`

가변 양식:
- 작품 라벨 양식 = YouTube title (`{작곡가} - {곡명}`)과 일관 (display label 연속성)
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

### 4. 작품별 해시태그 2건 (Block 4 마지막 줄 앞쪽)
```
#{작곡가성} #{곡명} #Cover ...
```
예: `#Satie #Gymnopedie #Cover ...`

가변 양식:
- 작곡가성 = 영어 last name (Satie / Bach / Debussy)
- 곡명 = 단일 단어 (Gymnopedie / Goldberg / Clair) · 다중 단어 작품은 합본 (e.g. *MoonlightSonata*)
- 작품 분류 anchor 1건 (`#Cover`) = 모든 작품 공통 anchor (cover 콘텐츠 검색 노출 axis · s295 신축)
- 채널 anchor 10건 (`#HatsuneMiku #初音ミク #Acappella #アカペラ #Vocaloid #ボカロ #VOCALOID #ClassicalMusic #AtelierMikuAcappella #Vocaloid6`) = 채널 anchor keep. 일본어 양식 4건 (#初音ミク + #アカペラ + #ボカロ + #VOCALOID) = 일본 청중 유입 axis (s310 신축)

## Anchor 자료 (변경 시 시리즈 통째 정합 회복 의제)

### Block 1 — 채널 환영
- *Welcome to Atelier Miku Acappella!* — 첫 줄 환영 인사
- 정체성 1줄 — *fan project · classical music · for Hatsune Miku's voice · one piece at a time*
- *Hope you find something to love here ♪* — 따뜻한 closing + ♪ 음표 시그너처 (♪ 앞 공백 1칸 박음)

### Block 3 — 본질 + CTA (v5 swap)
- *No AI for music — every note placed by hand in Vocaloid6 Editor.* — 작업 본질 (음악 한정 명시 · cover art는 AI 합성 axis라 *covers* wording 회피 · v3 정합 keep)
- *Subscribe to join the Atelier and discover a new side of classical music!* — 구독 유도 + Atelier 소속감 + new side discovery axis (v2 신축 자료 · v5 swap으로 Block 3로 이동)

### Block 4 — 의무 표기 + 해시태그 footer (v5 swap)
- *Hatsune Miku, © Crypton Future Media, Inc. — CC BY-NC 3.0 https://creativecommons.org/licenses/by-nc/3.0/* — 자료 §3.2 의무 표기 (저작자 표시 + 라이선스 원문 URL)
- 해시태그 줄 — 작품별 2건 + 작품 분류 anchor 1건 (#Cover) + 채널 anchor 10건 (영문 6건 + 일본어 4건)

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
