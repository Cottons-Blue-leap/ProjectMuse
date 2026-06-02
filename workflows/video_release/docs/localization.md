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

## 품질 게이트 (필수 · 못 읽는 언어 doctrine)

우리가 검증 못 하는 6개 언어 → **외부/독립 교차검증 1회 이상** (feedback_self_audit_limits 정합). s393 = Gemini + 서브에이전트 2회. 큐레이터 헌사(LOCK 창의문장) + 작곡가 성 음역이 핵심 점검 지점.

## 신곡 절차 (per-song)

1. **로케일 데이터 추가** — `localize_batch.py` `WORKS` 에 새 작품 dict 1건 append:
   `vid` · `slug` · `count`(미쿠 수) · `year` · `style`(`lead`/`inline`/`vivaldi`/`welcome_inline`) · `era` · `surname`/`full`/`piece`(7로케일 · `L()` 헬퍼=라틴4공유) · `painter`/`painting`(영어원제)/`p_year` · `cover_url` · `curator`(7로케일 idiomatic · None이면 Welcome형) · `tag_piece`. 위 Lock 정책 준수.
2. **검토** — `python Analytics/localize_batch.py gate` (제목·큐레이터 표) + `review`(전수 렌더 → `Analytics/_channel_l10n/REVIEW_l10n_*.txt`).
3. **외부 QA** — review 파일을 독립 검수(품질 게이트). must-fix 반영.
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
