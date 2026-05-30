# Title Naming Guide

> Canonical rule for Atelier Miku Acappella release titles.
> Locked 2026-05-28 (코튼 결단). Supersedes the s355 full-name format
> `Composer full name - Piece (feat. 初音ミク)`.

## The format

```text
<Composer surname, locale-native> - <Piece> (feat. 初音ミク)
```

Minimal. The composer surname + piece, then the featured-artist credit as a suffix. No "Acappella"
in the title — that lives in the channel name + tags, and the video *reveals* itself as
acappella. The feat. credit uses `初音ミク` (the canonical Japanese wordmark) in **every locale**.

**Title vs description-body convention** (코튼 2026-05-28 결단): Titles use the surname-only short
form for identification efficiency. Description body dedications (e.g. `에릭 사티 - 짐노페디 1번
(1888년)`) keep the full name — body is the formal first-mention surface, title is the recognition
surface.

### Why this shape (s355 rationale)

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
every video; `defaultLanguage = en`). Composer + piece are localized; the `(feat. 初音ミク)`
credit is identical in all three.

| field | EN (default) | KO | JA |
|---|---|---|---|
| composer | surname only, Latin (e.g. `Mozart`) | surname only, Hangul (e.g. `모차르트`) | surname only, Katakana (e.g. `モーツァルト`) |
| piece | see policy below | see policy below | see policy below |
| credit | `(feat. 初音ミク)` | `(feat. 初音ミク)` | `(feat. 初音ミク)` |

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

### Rules

1. `<Composer surname> - <Piece> (feat. 初音ミク)`. The `(feat. 初音ミク)` suffix on every
   title, every locale (composer surname + piece localized; credit identical).
2. No "Acappella" / "アカペラ" / "아카펠라" in the title — channel name + tags carry it; the
   video reveals it. (This is the design, not an omission.)
3. Composer surname only (locale-native) + ` - ` + piece. One consistent structure across locales.
   Disambiguation family (Bach, Strauss, etc.) → identifying prefix at point of first conflict
   (see above). Description body dedications keep the full name — body is the formal first-mention
   surface, title is the recognition surface (2026-05-28 결단).
4. `defaultLanguage = en`; set localizations for en/ko/ja on every video.
5. Never imply an altered title is the historical title; credit the source in the description
   (`Composer full name - Piece (year)`).

## Current catalog (live, 2026-05-28)

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
