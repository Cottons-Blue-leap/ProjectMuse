# Title Naming Guide

> Canonical rule for Atelier Miku Acappella release titles.
> Locked s355 (2026-05-25, 코튼 결단). Supersedes the s348 front-bracket format
> `[Miku Acappella] Composer - Piece`.

## The format

```text
<Composer full name> - <Piece> (feat. 初音ミク)
```

Minimal. The composer + piece, then the featured-artist credit as a suffix. No "Acappella"
in the title — that lives in the channel name + tags, and the video *reveals* itself as
acappella. The feat. credit uses `初音ミク` (the canonical Japanese wordmark) in **every locale**.

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
| composer | full name, Latin | full name, Hangul | full name, Katakana |
| piece | see policy below | see policy below | see policy below |
| credit | `(feat. 初音ミク)` | `(feat. 初音ミク)` | `(feat. 初音ミク)` |

### Piece name policy

Use the name **the local audience actually searches**:

- If the original-language title is the global standard, keep it in every locale:
  `Salut d'Amour`, `Gymnopédie No. 1`, `Eine kleine Nachtmusik`.
- If a market has its own canonical name, localize it: Vivaldi Spring →
  JA `四季 春 第1楽章`, KO `사계 '봄' 1악장`.

### Rules

1. `<Composer full name> - <Piece> (feat. 初音ミク)`. The `(feat. 初音ミク)` suffix on every
   title, every locale (composer + piece localized; credit identical).
2. No "Acappella" / "アカペラ" / "아카펠라" in the title — channel name + tags carry it; the
   video reveals it. (This is the design, not an omission.)
3. Composer full name + ` - ` + piece. One consistent structure across locales (no surname-only
   or alternate framing — this was the Vivaldi outlier, fixed s348 and kept).
4. `defaultLanguage = en`; set localizations for en/ko/ja on every video.
5. Never imply an altered title is the historical title; credit the source in the description
   (`Composer - Piece (year)`).

## Current catalog (live, s355)

```text
Erik Satie - Gymnopédie No. 1 (feat. 初音ミク)
  KO  에릭 사티 - 짐노페디 1번 (feat. 初音ミク)
  JA  エリック・サティ - ジムノペディ第1番 (feat. 初音ミク)

Antonio Vivaldi - Spring, Mvt. I (feat. 初音ミク)
  KO  안토니오 비발디 - 사계 '봄' 1악장 (feat. 初音ミク)
  JA  アントニオ・ヴィヴァルディ - 四季 春 第1楽章 (feat. 初音ミク)

Scott Joplin - The Entertainer (feat. 初音ミク)
  KO  스콧 조플린 - 디 엔터테이너 (feat. 初音ミク)
  JA  スコット・ジョプリン - ジ・エンターテイナー (feat. 初音ミク)

Edward Elgar - Salut d'Amour (feat. 初音ミク)
  KO  에드워드 엘가 - 사랑의 인사 (feat. 初音ミク)
  JA  エドワード・エルガー - 愛の挨拶 (feat. 初音ミク)
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
