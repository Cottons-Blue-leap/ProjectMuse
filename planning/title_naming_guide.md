# Title Naming Guide

> Canonical rule for Atelier Miku Acappella release titles.
> **Locked 2026-06-06 (코튼 결단, s402)** — back bracket-badge `【初音ミク A Cappella】`.
> Supersedes the 2026-05-28 surname-suffix `Surname - Piece (feat. 初音ミク)` (history below).

## The format

```text
<Composer surname, locale-native> - <Piece> 【初音ミク A Cappella】
```

Composer surname + piece, then a trailing **bracket badge** `【初音ミク A Cappella】` that absorbs
the old `(feat. 初音ミク)` credit and adds the "A Cappella" differentiator. The badge is a
**constant wordmark, identical in every locale** (only composer + piece localize).

**Why the badge — and why this shape (s402 코튼 결단):**
- `【】` (lenticular brackets) = YouTube's most visually distinct *text* marker; reads as one unit,
  matching the channel name "Atelier Miku Acappella". `初音ミク` stays the universal credit wordmark.
- **Back-loaded, not front.** The badge is a *constant* across all videos, so the most valuable
  left-most slot is reserved for the *variable* (composer + piece) = in-list differentiation. Brand
  is already carried by the thumbnail (명화 + Miku); the title's job is to differentiate. A front
  badge `【…】 Composer - Piece` would make every title look identical on the left and fully forfeit
  the s355 reveal design — rejected.
- **`A Cappella` is Latin-universal** (a wordmark, like `初音ミク`) — locale spellings (アカペラ/아카펠라)
  live in tags, not the title.
- **Long-title fallback (reserved · not currently used):** if a title would exceed YouTube's
  100-char hard cap, abbreviate the badge to `【A Cappella】` (the `初音ミク` mark is still guaranteed
  by thumbnail + tags). No live title triggers this — even the longest (Mozart K.265, 79 chars)
  uses the **full** badge. (코튼 2026-06-06: 一貫性 우선 — Mozart도 풀 badge로 통일.)
- **What this trades:** the badge reverses the s355 *reveal/curiosity-gap* rule (acappella is now
  declared up front, not discovered inside the video). 코튼 accepted this trade: at the current
  stage (bottleneck = discovery), an upfront differentiator on the recommendation surface (≈most
  traffic) beats the in-video micro-reveal. The larger hook ("Classical, by Miku?!") still survives.
- **Not an SEO change (정직):** `初音ミク` was already in the title; "A Cappella" is not a query that
  finds us (inbound search = vocaloid + exact piece name only; ranking is behavioral, not keyword).
  The badge's job is CTR/identity on the recommendation surface — search SEO is carried by tags +
  description, not the title (s402).

**Title vs thumbnail vs description-body convention** (코튼 2026-05-28 · thumbnail rule 2026-05-31):
Surname abbreviation is *allowed* on two surfaces — the **title** (always surname-only, for
identification efficiency) and the **thumbnail** (full name by default, but abbreviate to surname
*when space runs short* — e.g. `W.A. Mozart` on the K.265 thumbnail, where the long piece name left
no room for `Wolfgang Amadeus Mozart`). The **description body** dedication (e.g. `에릭 사티 -
짐노페디 1번 (1888년)`) *always* keeps the full name — body is the formal first-mention surface.
So: title = surname; thumbnail = full name with surname space-fallback; body = full name always.

### Why the suffix shape (s355 rationale — HISTORICAL, superseded by the s402 badge above)

> Retained for the reasoning trail. The reveal/curiosity-gap argument (point 1) is the design the
> s402 badge knowingly trades away; the feat.-credit-as-identity argument (point 2) carries forward
> into the badge (`初音ミク` is still the universal credit mark, now inside `【…】`).

1. **Reveal / curiosity-gap design (코튼 핵심).** Front-loading every spec
   (`[Miku Acappella] …`) turns the title into a full spec-sheet → the viewer pre-judges
   before clicking ("as expected / not for me" = *evaluation mode*). Withholding "acappella"
   makes it a payoff discovered *inside* the video: "Classical, by Miku?!" (hook) → click →
   "ah — acappella!" (reward) = *discovery mode*. This optimizes for new viewers, who are ~all
   our traffic (recommendation ≈ 65%, s349/s351).
2. **The feat. credit's job = identity signal, not search.** Search ≈ 0 on this channel and the
   title is no longer the search lever (s352 web research: thumbnail >> title for CTR; end-of-title
   text is near-useless for search; recommendation is the driver). So keyword-position in the
   title barely matters. The credit's job is to *signal identity at the click moment* — and
   `初音ミク` is the most iconic, authentic, globally-recognized mark for that. The romaji/hangul
   spellings still serve search via tags + description.
3. **`初音ミク` universal ≠ inconsistent with s351 locale-pure hashtags.** Different surfaces,
   different jobs: hashtags = *search/discovery* (locale-native names help locale search) →
   `#HatsuneMiku` (EN) / `#하츠네미쿠` (KO) / `#初音ミク` (JP); title credit = *identity mark*
   (the "logo" moment) → `初音ミク` everywhere. The two surfaces intentionally differ by function.

### Per-locale fields

YouTube serves each viewer the title matching their account language (localizations are set on
every video; `defaultLanguage = en`). Composer + piece are localized; the `【初音ミク A Cappella】`
badge is identical/universal in all locales.

| field | EN (default) | KO | JA |
|---|---|---|---|
| composer | surname only, Latin (e.g. `Mozart`) | surname only, Hangul (e.g. `모차르트`) | surname only, Katakana (e.g. `モーツァルト`) |
| piece | see policy below | see policy below | see policy below |
| badge | `【初音ミク A Cappella】` | `【初音ミク A Cappella】` | `【初音ミク A Cappella】` |

**Disambiguation family**: when more than one composer shares a surname (Bach family — J.S. / C.P.E. /
J.C.; Strauss — Johann II vs Richard; Haydn — Joseph vs Michael; Mendelssohn — Felix vs Fanny), attach
an identifying prefix at the point the first conflict candidate enters the catalog. Prefix form to be
decided at that moment (코튼 decision). No premature doctrine for hypothetical cases.

### Piece name policy

Use the name **the local audience actually searches**:

- If the original-language title is the global standard, keep it in every locale:
  `Salut d'Amour`, `Gymnopédie No. 1`, `Eine kleine Nachtmusik`.
- If a market has its own canonical name, localize it: Vivaldi Spring →
  JA `四季 春 第1楽章`, KO `사계 '봄' 1악장`.

**s411 enrich (2026-06-09 · JP 유입 SEO 사이클)** — 곡명을 *청중이 실제 검색하는 이름* 쪽으로 보강:
- **부모작 병기 (가산식 · 전 로케일)**: 발췌곡은 부모작 정식명을 괄호 병기 (검색량 압도). 선례 = Tchaikovsky
  사탕요정의 춤 → `… (The Nutcracker)` / JA `…（くるみ割り人形）` / 발레 정식명 각 로케일
  (El Cascanueces · O Quebra-Nozes · Der Nussknacker · Casse-Noisette · Щелкунчик · 胡桃鉗/胡桃夹子).
  본문 dedication/hook 은 깨끗한 단독 곡명 유지 (title=발견 / body=정식 dedication).
- **검색-별칭 (Mozart JA/KO · s393 JA/KO-정식 sub-choice 갱신)**: K.265 제목 곡명을 학술명
  「ああ…」12の変奏曲 → JA `きらきら星変奏曲` / KO `작은별 변주곡`. 사유 = 학술명이 해당 시장에서 사실상
  무검색(해시태그에만 존재) → s393 의 *zh 별칭 예외* 와 **동일 논리**(정식명 무검색 시 발견성 우선)를
  JA/KO 로 확장. EN/default + 유럽 5로케일은 정식명 유지(기존 zh 별칭은 그대로). 학술 풀네임은 설명
  본문에 보존 (title=recognition / body=formal). 코튼 enrich go (2026-06-09 디스코드).

### Rules

1. `<Composer surname> - <Piece> 【初音ミク A Cappella】`. The badge on every title, every locale
   (composer surname + piece localized; badge identical/universal).
2. `A Cappella` is **Latin-universal in the title badge** (a wordmark) — never localize it to
   アカペラ/아카펠라 in the title; locale spellings live in tags only. Long-title fallback (reserved,
   >100 chars only) = abbreviate badge to `【A Cappella】`; no live title currently triggers it.
3. Composer surname only (locale-native) + ` - ` + piece + ` ` + badge. One consistent structure
   across locales.
   Disambiguation family (Bach, Strauss, etc.) → identifying prefix at point of first conflict
   (see above). Description body dedications keep the full name — body is the formal first-mention
   surface, title is the recognition surface (2026-05-28 결단).
4. `defaultLanguage = en`; set localizations for en/ko/ja on every video.
5. Never imply an altered title is the historical title; credit the source in the description
   (`Composer full name - Piece (year)`).

## New-format example (s402 canonical)

```text
Satie - Gymnopédie No. 1 【初音ミク A Cappella】
  KO  사티 - 짐노페디 1번 【初音ミク A Cappella】
  JA  サティ - ジムノペディ第1番 【初音ミク A Cappella】

# longest live title (Mozart K.265, 79 chars) — still full badge (fallback reserved for >100 chars):
Mozart - Twelve Variations on "Ah, vous dirai-je, maman" K.265 【初音ミク A Cappella】
```

## Live catalog — **retrofit DONE (2026-06-06, s402)**

> 코튼 chose rollout (a): all live videos retrofitted to the badge now. Applied to **8 videos ×
> 11 locales** (default + en/ko/ja/es/pt/de/fr/ru/zh-Hant/zh-Hans) via
> `Analytics/_retrofit_acappella_badge_s402.py` (read-modify-write; descriptions/tags/category/
> playlist/schedule preserved) → full audit PASS (no `(feat.)` suffix left, badge present).
> All 8 = full `【初音ミク A Cappella】` (Mozart K.265 initially abbreviated, then unified to full
> per 코튼 2026-06-06 — consistency; 79 chars is well under the 100-char cap).
> Repo synced: `localize_batch.py` generator (badge + Mozart `badge_abbrev`), 7-locale title
> sidecars (`write`), `series_history.csv` release_title, per-work `status.json`.
> The block below is the **pre-retrofit snapshot (historical)** — live now carries the badge.

```text
Satie - Gymnopédie No. 1 (feat. 初音ミク)
  KO  사티 - 짐노페디 1번 (feat. 初音ミク)
  JA  サティ - ジムノペディ第1番 (feat. 初音ミク)

Vivaldi - Spring, Mvt. I (feat. 初音ミク)
  KO  비발디 - 사계 '봄' 1악장 (feat. 初音ミク)
  JA  ヴィヴァルディ - 四季 春 第1楽章 (feat. 初音ミク)

Joplin - The Entertainer (feat. 初音ミク)
  KO  조플린 - 디 엔터테이너 (feat. 初音ミク)
  JA  ジョプリン - ジ・エンターテイナー (feat. 初音ミク)

Elgar - Salut d'Amour (feat. 初音ミク)
  KO  엘가 - 사랑의 인사 (feat. 初音ミク)
  JA  エルガー - 愛の挨拶 (feat. 初音ミク)

Mozart - Twelve Variations on "Ah, vous dirai-je, maman" K.265 (feat. 初音ミク)
  KO  모차르트 - '아, 어머니께 말씀드릴게요' 주제에 의한 12개의 변주곡 K.265 (feat. 初音ミク)
  JA  モーツァルト - 「ああ、お母さん、あなたに申しましょう」による12の変奏曲 K.265 (feat. 初音ミク)
```

## Applying titles

Write access is automated via `Analytics/youtube_meta.py` (OAuth `youtube.force-ssl`,
read-modify-write so other fields are preserved). `set-title` writes the default + en/ko/ja
localizations in one call:

```text
python Analytics/youtube_meta.py get <video_id>
python Analytics/youtube_meta.py set-title <video_id> --default "..." --en "..." --ko "..." --ja "..."
```

Note: the post-update `get` printed by `set-title` can show a stale `[default title]` for a few
seconds (read-after-write lag); re-run `get` to confirm. The same tool uploads custom thumbnails
(`set-thumbnail`).

## Format history

- (launch, s282) `Composer - Piece (feat. Hatsune Miku)` — original Gymnopédie title.
- v9 (s340) → `Composer - Piece (Hatsune Miku Acappella)` — SEO cycle, surface the "Acappella" keyword.
- v10/s348 → `[Miku Acappella] Composer - Piece` — front-bracket keyword front-load (+ Vivaldi format fix).
- **s355 → `Composer - Piece (feat. 初音ミク)`** — reveal/curiosity-gap design + feat.-credit-as-identity;
  data (s352) showed the front-load SEO bet was weak (search ≈ 0, thumbnail drives CTR). Returns to the
  suffix shape of the launch title, with `初音ミク` as the universal credit. All 4 live videos retrofitted.
- **2026-05-28 → `Surname - Piece (feat. 初音ミク)`** — surname-only short form (코튼 결단:
  *식별력 높은 부분만 남기자*). Classical-music convention default (Mozart / Chopin / Bach not
  *Wolfgang Amadeus Mozart*); saves chars (esp. Mozart K.265 ~18 chars), keeps recognition
  efficiency. Description body dedications keep full name — body is the formal surface. 4 live
  videos + 1 scheduled (Mozart K.265, 2026-05-28 20:00 KST) retrofitted.
