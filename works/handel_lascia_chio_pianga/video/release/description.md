# YouTube Description — Handel: Lascia ch'io pianga (Rinaldo HWV 7b, Act II)

> 양식 정본: [`../../../../workflows/video_release/docs/description_template.md`](../../../../workflows/video_release/docs/description_template.md) (custom_hook 경로 = 사탕요정·미뉴엣 family · Welcome 블록·Subscribe CTA 제거 axis)
> 박힌 날짜: 2026-06-11 · 코튼 hook LOCK (디스코드 컨펌 통과)
> N=13 (.vpr 활성 보컬 트랙 실측: Sorprano main+L+R · Violin1 L/R · Violin2 L/R · Viola L/R · D.B. high L/R · D.B. low L/R)

## 영상 제목 (YouTube title · 【初音ミク A Cappella】 badge 양식)

- default/en: `Handel - Lascia ch'io pianga 【初音ミク A Cappella】`
- ko: `헨델 - 울게 하소서 【初音ミク A Cappella】`
- ja: `ヘンデル - 私を泣かせてください 【初音ミク A Cappella】`
- es/pt/de/fr/ru/zh-Hant/zh-Hans = `title.{lang}.txt` (localize_batch 생성)

## Hook 설계 (코튼 LOCK 2026-06-11)

- **형식 = 1행 epithet** (코튼 직접 지정): KR "울지 마 미쿠야" / JP "泣かないで" / EN = 의미 번안 "Don't cry, Miku." — 곡 제목('울게 하소서')과의 대구.
- 2행 = 미쿠 라인 간결형 "13인의 미쿠가 부릅니다 —" (코튼 간결화 지시 · 소프라노/현 구조 설명 제거).
- **JP 호칭 = ミクさん** (코튼 지정 · 본문 산문만 · footer 제품명 初音ミクV6·해시태그는 고정 표기 유지).
- 시리즈 첫 '원곡 성악' 서사는 description에서 제외 (간결화) → 고정 댓글 후보.

## 곡명 로케일 정책 (코튼 원칙: 세계 표준 우선 · 로케일별 익숙명 우선)

- EN/es/pt/de/fr/ru = 이탈리아어 원제 `Lascia ch'io pianga` (세계 표준).
- KO = 「울게 하소서」 (압도적 통용명 · 코튼 LOCK).
- JA = 「私を泣かせてください」 (일본 통용명).
- zh-Hant = 《讓我哭泣吧》 (대만 통용 · zh위키 표제 · QA 게이트 수정) / zh-Hans = 《让我痛哭吧》 (대륙 통용 · 百度百科).
- 작곡가 표기 = EN `George Frideric Handel`(영어권 귀화 철자) / de·es·pt `Georg Friedrich Händel` / fr `Haendel` / ru `Гендель` / zh-Hant 韓德爾 / zh-Hans 亨德尔.

## CC(자막) 안내 (가사곡 전용 · 코튼 LOCK 2026-06-17)

- **위치 = 설명란 최상단** (hook "울지 마 미쿠야" 위 · `—` 디바이더로 분리된 배너 블록). 코튼 "즉시 인지" 우선 결정.
- **카피 (짧은 지시형)**: EN `📃 For lyrics, turn on CC (captions).` / KO `📃 가사 보기 → CC(자막)을 켜 주세요.` / JA `📃 歌詞はCC（字幕）をオンに。`
- 구현 = en/ja/ko는 hand-sidecar 최상단 직접 삽입 · 7언어는 `localize_batch.py` `CC_LYRICS` dict + work `"lyrics": True` 플래그 → `build_description` 최상단 주입. **가사곡에 `"lyrics": True`만 켜면 자동 적용** (시리즈 가사곡 재사용 메커니즘).

## 9언어 sidecar 상태

- **en/ja/ko** = hand-sidecar 정본 (description.{en,ja,ko}.txt · 코튼 컨펌 2026-06-11).
- **es/pt/de/fr/ru/zh-Hant/zh-Hans** = `localize_batch.py` WORKS custom_hook 생성 (description.{lang}.txt + title.{lang}.txt).

## Cover art

`Cover art, after Rossetti, 'Proserpine' (1874).` + Tate 공식 URL (https://www.tate.org.uk/art/artworks/rossetti-proserpine-n05064 · 소장 N05064). Dante Gabriel Rossetti d.1882 PD강. KO/JA 그림 표기 = 썸네일 명문 PROSERPINA 정합 '프로세르피나/プロセルピナ'.

## 백엔드 태그

`description.tags.txt` (오타 변형 Lascia chio pianga + 영어명 Let me weep + Farinelli + 바로크 3국어).

## 발행 정보

- vid = `xHzbkP_Wcm0` · 예약 2026-06-15 18:45 KST 자동공개 (코튼 재업로드 2026-06-11 = test5 재렌더본 · 구 `sExC_ygSrSk` 삭제). 메타 10로케일 재적용+audit PASS (2026-06-11).
