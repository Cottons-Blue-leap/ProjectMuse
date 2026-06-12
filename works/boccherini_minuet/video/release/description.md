# YouTube Description — Boccherini: Minuet (String Quintet Op.11 No.5, G.275, 3rd mvt)

> 양식 정본: [`../../../../workflows/video_release/docs/description_template.md`](../../../../workflows/video_release/docs/description_template.md) (custom_hook 경로 = 사탕요정 family · Welcome 블록·Subscribe CTA 제거 axis)
> 박힌 날짜: 2026-06-08 · 코튼 hook LOCK
> N=9 (.vpr 활성 보컬 트랙 실측: Violin1 L/R · Violin2 high L/R · Violin2 low L/R · Viola · Cello · ContreBasse)

## 영상 제목 (YouTube title · 【初音ミク A Cappella】 badge 양식)

- default/en: `Boccherini - Minuet 【初音ミク A Cappella】`
- ko: `보케리니 - 미뉴엣 【初音ミク A Cappella】`
- ja: `ボッケリーニ - メヌエット 【初音ミク A Cappella】`
- es/pt/de/fr/ru/zh-Hant/zh-Hans = `title.{lang}.txt` (localize_batch 생성)

## Hook 설계 (코튼 LOCK 2026-06-08)

- **형식 = "토막 상식 + 미뉴엣 어원"** (코튼 결정). 어원 = 프랑스어 **menu(작다)** → 작은 보폭의 춤. "(menu)" 괄호 = 전 로케일 보존.
- 도입부 lead-in 로케일별 = EN "Did you know?" (코튼 "Fun fact"는 *재미 과약속*이라 반려 → 중립 "Did you know?" LOCK) / KO "토막 상식:" / JA "豆知識：" / 기타 네이티브 등가.
- line 2 = N=9 미쿠가 현악 5중주(5성부) 노래 · line 3 = 작곡가 풀네임 - 곡 - 1771.

## 9언어 sidecar 상태

- **en/ja/ko** = hand-sidecar 정본 (description.{en,ja,ko}.txt · Cotton hook LOCK).
- **es/pt/de/fr/ru/zh-Hant/zh-Hans** = `localize_batch.py` WORKS custom_hook 생성 (description.{lang}.txt + title.{lang}.txt).
- **외부 QA subagent 게이트 통과** (2026-06-08): 2건 수정 적용 = ① zh-Hant 작곡가명 鮑凱里尼→**鮑凱利尼**(대만 표준 利 · 다중출처) ② pt "dança cortesã"(courtesan 오독)→**"dança da corte"**(court dance). 나머지 5언어 OK + 어원/음악용어/러시아어/zh-Hans 博凯里尼 확인. fr = "menus" 네이티브 형용사로 어원 inline 처리(우수).

## Cover art

`Cover art, after Longhi, 'The Dancing Lesson' (c.1741).` + WGA URL (https://www.wga.hu/html/l/longhi/pietro/1/01dancin.html). Pietro Longhi d.1785 PD강.

## 백엔드 태그

`description.tags.txt` (497/500자 · 다국어 검색어).

## 표기 결정 (코튼 LOCK 2026-06-08)

- KO = **"미뉴엣"으로 통일** (코튼 결정). 제목·트리비아·헌사·해시태그 전부 미뉴엣. 단 **백엔드 태그는 미뉴엣·미뉴에트 병기**(코튼 · 검색 커버리지).
- vid = `10ZSa-TPOC4` · 예약 2026-06-11 21:15 KST 자동공개 · 메타 10로케일 전수 재적용+audit PASS (2026-06-11 3차 업로드 · 구 `X9xxOeqi2Sk` 삭제 = 발행 후 0:50~1:40 밸런스 음향 수정 재렌더 · 그 전 `TqS1F8I-SKw`도 삭제됨).
