# Localization Doctrine — Atelier Miku Acappella (9개 언어)

> 매 작품 release 시 제목·설명을 **9개 언어**로 현지화하는 표준 절차.
> 박힌 날짜: 2026-06-03 (s393) · 코튼 결단 *"앞으로도 현지화 루트 워크플로우에 반영"*.
> 엔진 = `Analytics/localize_batch.py` (단일 source of truth) · 쓰기 = `Analytics/youtube_meta.py`.

## 적용 시점

**release 메타 적용 단계** (publish 전, EN/JA/KO 제목·설명 확정 직후). 영상이 처음부터 현지화된 채 공개되도록 publish 전에 push. post_release_meta_doctrine.md Step 1(link 확보) 전후가 자연 자리.

## 로케일 (9개)

- 기존: `en` · `ja` · `ko` (release 본문에서 직접 작성)
- 신규 7개: `es` · `pt`(브라질향) · `de` · `fr` · `ru` · `zh-Hant`(번체/대만·홍콩) · `zh-Hans`(간체)
- **영상 = bare 코드**(`es`/`zh-Hant`…) · **채널 = region 코드**(`es_ES`/`zh_TW`… · 기존 `en_US`/`ja_JP`/`ko_KR` 스타일 정합). 채널은 1회 세팅 = 곡마다 안 건드림.

## Lock 정책 (s393 · JA/KO 선례 + 코튼 결단)

1. **네이티브 스크립트 완전 현지화** — 작곡가명 키릴/중국어 음역(쇼팽=Шопен/蕭邦/肖邦), 곡명 시장 canonical(夜曲/Ноктюрн/Nocturne).
2. **명화 제목 = 영어 원제 keep** — 검증 불가 6개 언어 오역 회피. 프레임 문구("Cover art, after…")만 현지화. (JA/KO는 번역했으나 신규 7개는 보수적.)
3. **독일어 = KV**(쾨헬), 나머지 K. — 예: `KV 265`.
4. **"The Entertainer"** = 영문 고유제목 유지(음역 X).
5. **제목 = 작곡가 성만** + ` (feat. 初音ミク)` 접미(전 로케일 불변·브랜드). [title_naming_guide 정본]
6. **곡명 정식 vs 별칭** = 제목은 정식(s361) — **단 zh Mozart K.265 = 별칭 `《小星星變奏曲》` 의도적 예외**(중국어 정식명=프랑스 원제 무검색 → 발견성 우선). 별칭이 곡 식별에 사실상 표준인 시장은 곡별 판단.
7. **채널명** = 브랜드 `Atelier Miku A Cappella` 전 로케일 고정 · 설명만 현지화.

## 품질 게이트 — 3층 교차검수 (필수 · 코튼 2026-06-06 "당분간 유지")

우리가 못 읽는 6개 언어 → **3층 교차검수** (feedback_self_audit_limits + feedback_l10n_cross_verification 정합):

1. **Claude QA subagent** — 저자(MOKA)와 분리된 새 컨텍스트 에이전트로 register·문법·성수일치·음악용어·naming 적대적 1차.
2. **웹 사실검증 (모델 무관)** — 곡명/인명 표준 표기를 각 언어 Wikipedia 표제어·악보/오케스트라 사이트로 대조 (naming 축 = 모델 의존 0 확정).
3. **교차모델 (path ㄴ = 수동 paste)** — GPT·Gemini·Claude.ai 각 **새 대화**에 검수 프롬프트+현재 라이브본 붙여넣고 회수. API 미사용(코튼 토큰비용 통제 불가). 목적 = **다른 모델 계열이 Claude+GPT 공유 blind spot 적발**.

**★ adjudication 규칙:** 모델이 지적한 오류는 **모델 투표 집계가 아니라 반드시 라이브 바이트(또는 웹 ground truth)로 대조 후 적용.**

핵심 점검 지점 = 큐레이터 헌사/hook(LOCK 창의문장) + 작곡가 성 음역 + 음악용어 자연성.

### 실측 사례 (s398 · 차이콥스키 사탕요정)
- **line→note (적용)** — "down to the last line"의 literal 번역(última línea/letzten Zeile/dernière ligne)이 음악 아닌 *텍스트 줄*로 읽힘 → nota/Note/note(음악 자연 + "cada parte…última parte" 반복 회피). **Gemini 단독 적발, Claude+GPT+subagent 셋 다 놓침** = 상관오류 실측+포착.
- **pt "orquest ral" 유령오타** — 3모델이 다 지적했으나 라이브 바이트는 정상 "orquestral". 원인 = **paste 줄바꿈이 만든 가짜 오타**. ⚠️ **path ㄴ 함정 = 모델은 라이브가 아닌 paste를 검수** → ground-truth 대조 없으면 유령 수정 위험.

### custom_hook (bespoke hook 곡)
표준 "{N} Mikus sing it now" 템플릿을 벗어난 코튼 LOCK hook(예: 사탕요정 "첫 관현악/혹사 미쿠")은 `WORKS` dict에 **`custom_hook` {lang: 3줄블록}** 키 추가 → `build_description`가 curator/dedication 대신 그 블록 사용(count/sing/NUM 미사용). `curator`=None. EN/KO/JA는 release/ hand-sidecar가 정본, 7언어만 custom_hook 번역.

## 신곡 절차 (per-song)

1. **로케일 데이터 추가** — `localize_batch.py` `WORKS` 에 새 작품 dict 1건 append:
   `vid` · `slug` · `count`(미쿠 수) · `year` · `style`(`lead`/`inline`/`vivaldi`/`welcome_inline`) · `era` · `surname`/`full`/`piece`(7로케일 · `L()` 헬퍼=라틴4공유) · `painter`/`painting`(영어원제)/`p_year` · `cover_url` · `curator`(7로케일 idiomatic · None이면 Welcome형) · `tag_piece`. 위 Lock 정책 준수.
2. **검토** — `python Analytics/localize_batch.py gate` (제목·큐레이터 표) + `review`(전수 렌더 → `Analytics/_channel_l10n/REVIEW_l10n_*.txt`).
3. **3층 교차검수** — 위 「품질 게이트」 절차(Claude subagent → 웹 사실검증 → 교차모델 paste) + ground-truth adjudication. must-fix만 라이브 대조 후 반영.
4. **sidecar 생성** — `write --only <vid|slug>` → `works/<piece>/video/release/description.<lang>.txt` + `title.<lang>.txt`.
5. **푸시** — `push --only <vid>` (read-modify-write · en/ja/ko 보존 · 채널 자동 skip). `--dry-run` 먼저 권장.
6. **audit** — `audit --only <vid>` → 10개 로케일 존재 + 제목 일치 PASS 확인.

전체 일괄(7곡+채널 재적용)이 필요하면 `--only` 생략.

## Gotcha (실측 박힘 · s393)

- **채널 localizations** = `channels.update part="localizations"` **단독**. `brandingSettings` 동봉 시 `400 'branding_settings cannot be used with other parts'`. 채널 defaultLanguage(en) 이미 설정돼 있어 동봉 불필요.
- **read-after-write 전파 지연** — push 직후 audit 이 옛 데이터 읽어 false FAIL 가능(s355에서도 동일 lag). 잠시 후 재조회하면 정상. push 자체는 HttpError 없으면 성공.
- **성(性) 일치 함정 회피** — "{N} Mikus sing it now" 는 목적어 생략으로 번역(es/pt/fr/ru 명사 성 함정 회피). `sing()` 참조.

## 도구 명령 요약

```
python Analytics/localize_batch.py gate                    # 제목·큐레이터 검토표
python Analytics/localize_batch.py review                  # 전수 렌더 파일
python Analytics/localize_batch.py preview <slug> [--langs es,ru]
python Analytics/localize_batch.py write  [--only <vid>]   # sidecar 생성
python Analytics/localize_batch.py push   [--only <vid>] [--dry-run]
python Analytics/localize_batch.py audit  [--only <vid>]
python Analytics/localize_batch.py channel                 # 채널 설명 sidecar
```

`youtube_meta.py` 도 임의 로케일 지원: `set-title --loc <lang> "…"` · `set-description --loc-file <lang> <path>` · `set-channel` / `get-channel`.
