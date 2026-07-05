# YouTube Description — Dance of the Sugar Plum Fairy (Tchaikovsky)

> 양식 base: [`../../../../workflows/video_release/docs/description_template.md`](../../../../workflows/video_release/docs/description_template.md) (v13 · curator voice + Welcome/Subscribe 제거 · 챕터 없음[단곡])
> 박힌 날짜: 2026-06-06 · **hook = 코튼 LOCK** (2026-06-06 · bespoke 3줄 = 표준 epithet 템플릿 벗어남)
> N=32 = .vpr audit (`music/renders/Miku_tchaikovsky_sugar_plum_fairy.vpr` · 활성 보컬 트랙 32 = 첼레스타+현+클라리넷+플룻+오보에 전부 미쿠 보컬 layering · not-muted + notes>0). 2-note 미세 doubling 3개(Celesta low3·Violin2 low2·Viola low1) 포함 literal count.

## 영상 제목 (YouTube title)

```
Tchaikovsky - Dance of the Sugar Plum Fairy (feat. 初音ミク)
```
(성만 양식 · title_naming_guide LOCK 정합 · 본문 헌사·썸네일은 풀네임 Pyotr Ilyich Tchaikovsky keep · defaultLanguage en)

## Description (EN · 코튼 LOCK)

```
Our first full orchestral arrangement, and one very overworked Miku.
Thirty-two Mikus sing every part, down to the last line.
Pyotr Ilyich Tchaikovsky - Dance of the Sugar Plum Fairy (1892)

Cover art, after Renoir, 'The Dancer' (1874).
https://commons.wikimedia.org/wiki/File:Renoir_-_Danseuse_NGA.jpg

—

Production tool: VOCALOID6 / Voicebank: Hatsune Miku V6
Hatsune Miku, © Crypton Future Media, Inc.

#HatsuneMiku #Acappella #SugarPlumFairy #初音ミク #Vocaloid #ClassicalMusic #ClassicalCover #RomanticEra #Tchaikovsky #AtelierMikuAcappella
```

## 가변 자리 박힌 자료 (2026-06-06 LOCK)

1. **영상 제목** = `Tchaikovsky - Dance of the Sugar Plum Fairy (feat. 初音ミク)` (성만 · 후치 양식).
2. **hook = 코튼 LOCK · bespoke 3줄** (epithet형 X · 코뮤 보이스):
   - 1줄 = `Our first full orchestral arrangement, and one very overworked Miku.` — **첫 풀 관현악 편곡** 자기인식 + 혹사 코미디.
   - 2줄 = `Thirty-two Mikus sing every part, down to the last line.` — N=32 literal 흡수.
   - 3줄 = `Pyotr Ilyich Tchaikovsky - Dance of the Sugar Plum Fairy (1892)` — 풀네임 헌사 + 작곡 연도(호두까기 1892).
   - KO 정본 = `첫 관현악 편곡. 그리고 혹사당하는 미쿠. / 서른두 명의 미쿠가 한 성부도 빠짐없이 부릅니다. / 표트르 일리치 차이콥스키 - 사탕요정의 춤 (1892)`
   - JA 정본 = `初めての管弦楽編曲。そして酷使される初音ミク。 / 32人のミクが、一つの声部も余さず歌います。 / ピョートル・イリイチ・チャイコフスキー - 金平糖の精の踊り (1892)`
3. **Cover art** = `Cover art, after Renoir, 'The Dancer' (1874).` + Commons(NGA Open Access) URL. KO=르누아르의 '무용수' / JA=ルノワールの「踊り子」 (명화 제목 네이티브 번역 = 쇼팽 선례 정합).
4. **해시태그** = EN 10 · KO/JA 9 (로케일-퓨어). era=#RomanticEra/#낭만주의/#ロマン派 · 작곡가=#Tchaikovsky/#차이콥스키/#チャイコフスキー · 작품=#SugarPlumFairy/#사탕요정의춤/#金平糖の精の踊り.

## ✅ l10n 9언어 — 완료 (2026-06-06 · audit PASS)

이 곡 hook = **bespoke 3줄**이라 표준 템플릿 자동생성 불가 → **`localize_batch.py`에 `custom_hook` per-work 분기 신축**(ⓐ안 · build_description에서 curator/dedication 대신 3줄 블록 통째 사용 · count/sing/NUM 미사용 · 재사용 가능). WORKS entry(custom_hook 7언어 + painter Renoir + PAINTER/TAG_COMPOSER에 Renoir/Tchaikovsky 추가) → `write` → **외부 QA subagent 검수**(de überarbeitete→überlastete · zh-Hant 被操到不行→被使喚到不行 · es/pt cada voz→cada parte · 인명 통일) → `push`(en/ja/ko 보존) → `audit` PASS.

### 교차모델 검수 (코튼 요청 · 2026-06-06)
- **naming 축 = 웹 사실검증**: 7언어 곡명 전부 각 언어 Wikipedia 표제어/표준 표기 확인 (es Danza del Hada de Azúcar · pt Dança da Fada Açucarada · de Tanz der Zuckerfee · fr Danse de la Fée Dragée · ru Танец Феи Драже · zh 糖梅仙子之舞).
- **register/문법 축 = GPT + Gemini + Claude.ai 수동 paste(path ㄴ) 교차검수**:
  - **line→note 적용**(Gemini 단독 적발 · GPT·Claude·subagent 셋 다 놓침 = 다른-계열 시점의 실수확): es/pt/de/fr L2 "última línea/letzten Zeile/dernière ligne"(텍스트 줄로 읽힘) → **nota/Note/note**(음악 자연 + "cada parte…última parte" 반복 회피). ru(строчки 관용구)·zh 유지.
  - **pt "orquest ral" 오타 = phantom** (GPT·Gemini·Claude 3개 다 지적했으나 **라이브 YouTube+파일 실제 바이트 = "orquestral" 정상** · 내 Discord paste의 soft-wrap이 만든 유령). ⚠️ **path ㄴ 구조적 함정 = 모델은 라이브가 아닌 paste를 검수 → 지적 오류는 반드시 라이브 바이트로 adjudicate 후 적용.**
- 결론 = 실수정 line→note ×4 적용 → 재push → audit PASS. 라이브 10 로케일 확정.

## 백엔드 태그 (Studio 태그 칸 · description.tags.txt 단일 source)

공통 베이스 뒤에 차이콥스키/호두까기/사탕요정 곡별 자료 append (이명·로마자↔원어·한일 표기 쌍 안전망). 상세 = `description.tags.txt`.
