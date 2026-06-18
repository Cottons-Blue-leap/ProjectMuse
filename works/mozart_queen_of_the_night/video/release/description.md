# YouTube Description — Mozart: Der Hölle Rache (Queen of the Night aria, Die Zauberflöte K.620)

> 양식 정본: [`../../../../workflows/video_release/docs/description_template.md`](../../../../workflows/video_release/docs/description_template.md) (custom_hook 경로 = 사탕요정·미뉴엣·헨델 family · Welcome 블록·Subscribe CTA 제거 axis)
> 박힌 날짜: 2026-06-18 · 코튼 hook LOCK (디스코드 컨펌)
> N=22 (.vpr 활성 보컬 트랙 실측: Soprano(밤의여왕) + Flauti 1/2 · Oboi 1/2 · Fagotti 1/2 · Corni 1/2 · Trombe 1/2 · Timpani · Violino 1(+low1/2) · Violino 2(+low1/2) · Viola(+low) · Violoncello · Basso = 전부 미쿠)

## 영상 제목 (YouTube title · 【初音ミク A Cappella】 badge 양식)

- default/en: `Mozart - Queen of the Night Aria 【初音ミク A Cappella】` (코튼 2026-06-18 ⓑ 선택 = 통용명·인식 우선. 영상 비주얼라이저는 원제 'Der Hölle Rache'+'Queen of the Night' 부제 → 인비디오/메타 정합)
- ko: `모차르트 - 밤의 여왕 아리아 【初音ミク A Cappella】`
- ja: `モーツァルト - 夜の女王のアリア 【初音ミク A Cappella】`
- es/pt/de/fr/ru/zh-Hant/zh-Hans = `title.{lang}.txt` (localize_batch 생성 · 각 로케일 'Queen of the Night aria' 통용명)

## Hook 설계 (코튼 LOCK 2026-06-18)

- **컨셉 = 'Mozart = 천재'** (코튼 지정). ★ **형식 = 기호 등식 'Mozart = Genius'** (코튼 2026-06-18 최종: 완결 문장 "Mozart is a genius."는 '딱딱' → `=` 기호 등식으로 = 펀치+캐주얼). 로케일별 술어 현지화 + `=` 기호 유지: EN "Mozart = Genius" / KO "모차르트 = 천재" / JA "モーツァルト = 天才" / es Genio / pt Gênio / de Genie / fr Génie / ru "Моцарт = гений" / zh-Hant 莫札特=天才 / zh-Hans 莫扎特=天才. (마침표 없음 · `=` 양옆 공백.)
- 진행 경위 = 'was'(과거) → 'is'(현재 등식) → **`=` 기호 등식**(최종).
- 2행 = 미쿠 라인 "22인의 미쿠가 부릅니다 —" (헨델식 간결형) + 3행 곡 크레딧.

## 곡명 로케일 정책 (코튼 원칙: 세계 표준 우선 · 로케일별 익숙명 우선)

- **본문 곡 크레딧** = 원제 독일어 'Der Hölle Rache' **전 로케일 병기**(QA 일관성 반영 2026-06-18). EN/euro = 'Der Hölle Rache' 선두 + 'Queen of the Night aria' 로케일 디스크립터 + 오페라명. CJK(JA/KO/zh) = 로케일 통용명(夜の女王のアリア / 밤의 여왕 아리아 / 夜后咏叹调) + 〈Der Hölle Rache〉 병기 (QA가 JA/KO의 독일어 원제 누락 적발 → 통일).
- **제목(title)** = 코튼 ⓑ = 통용명 'Queen of the Night Aria'(인식 우선). 로케일 = es 'Aria de la Reina de la Noche' / pt 'Ária da Rainha da Noite' / de 'Arie der Königin der Nacht' / fr 'Air de la Reine de la Nuit' / ru 'Ария Царицы ночи' / zh-Hant 夜后詠嘆調 / zh-Hans 夜后咏叹调.
- 작곡가 = EN/es/pt/de/fr 'Wolfgang Amadeus Mozart' / surname 'Mozart' · ru 'Вольфганг Амадей Моцарт'/'Моцарт' · zh-Hant '莫札特' / zh-Hans '莫扎特' (mozart_twinkle 선례 정합).

## CC(자막) 안내 (가사곡 전용 · 코튼 LOCK 2026-06-17 · 시리즈 2번째 성악곡)

- **위치 = 설명란 최상단** (hook 바로 위 · 빈 줄 1개 · 디바이더 X · [더보기] 전 hook 노출). 헨델 ⑩ 선례.
- **카피**: EN `📃 For lyrics, turn on CC (captions).` / KO `📃 가사 보기 → CC(자막)을 켜 주세요.` / JA `📃 歌詞はCC（字幕）をオンに。`
- 구현 = en/ja/ko hand-sidecar 최상단 직접 · 7언어 = `localize_batch.py` `CC_LYRICS` + work `"lyrics": True` → `build_description` 최상단 주입.

## 9언어 sidecar 상태

- **en/ja/ko** = hand-sidecar 정본 (description.{en,ja,ko}.txt · 코튼 컨펌 2026-06-18).
- **es/pt/de/fr/ru/zh-Hant/zh-Hans** = `localize_batch.py` WORKS custom_hook 생성 → **외부 QA subagent 게이트** (feedback_l10n_cross_verification 3층).

## Cover art

`Cover art, after Schinkel, 'The Hall of Stars in the Palace of the Queen of the Night' (c.1815).` + Wikimedia Commons URL (원본 gouache · 코튼 2026-06-18 Wikimedia 지정). Karl Friedrich Schinkel d.1841 PD강. ★ 우리 커버 = 'after'(재구성) — Schinkel 무대 모티브 자유 재구성 + 미쿠 밤의여왕 실루엣. 그림 제목 = 영어 원제 유지(l10n 정책).

## 백엔드 태그

`description.tags.txt` (Der Hölle Rache 오타변형 + Queen of the Night + Magic Flute/Die Zauberflöte + K.620/KV620 + 4국어 통용명).

## 발행 정보

- vid = **`Gv5-QVuPZQs`** (CC 자막 baked 영상 재업로드 · 구 `9WXvxZYhzn4` 교체) · 예약 publish **2026-06-22 18:45 KST**(2026-06-22T09:45:00Z · private→자동공개). 메타 전수 적용+audit PASS (2026-06-18 재적용): defaultLang=en · 제목 10로케일 · 설명 10로케일(en/ja/ko hand + 7 push) · 태그 45개(~448자) · 썸네일 thumbnail_v5.jpg. 적용 순서 = title→desc→push→thumbnail→set-tags(last). **CC 자막 10로케일 업로드 완료**(youtube_captions insert · en=ASR 위 standard 별도 삽입 · audit 10/10 PASS).
