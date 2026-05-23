# Title Naming Guide

> Canonical rule for Atelier Miku Acappella release titles.
> Locked s348 (2026-05-23, 코튼 결단). Supersedes the old "Canon in Miku" playful-substitution
> draft (that predated the channel's faithful/serious direction).

## The format

```text
[<Miku keyword> Acappella] <Composer full name> - <Piece>
```

The Miku keyword is **front-loaded in brackets** so Vocaloid fans scanning a feed see it
first (scan + branding). Faithful titles only — no playful substitution.

### Per-locale fields

YouTube serves each viewer the title matching their account language (localizations are set
on every video; `defaultLanguage = en`). So we keep **three clean native titles** and never
mix scripts inside one title.

| field | EN (default) | KO | JA |
|---|---|---|---|
| Miku keyword | `Miku Acappella` | `미쿠 아카펠라` | `初音ミク アカペラ` |
| composer | full name, Latin | full name, Hangul | full name, Katakana |
| piece | see below | see below | see below |

**Why JA keeps `初音ミク` but EN/KO drop "Hatsune"/"하츠네":** `初音ミク` is the exact term the
Japanese audience searches, and Japan is our biggest untapped market — the title is the
highest-weighted search field, so we keep the full term where it matters most. EN/KO stay
concise ("Miku" is iconic enough); the full name still lives in the description + tags + channel
name for those locales.

### Piece name policy

Use the name **the local audience actually searches**:

- If the original-language title is the global standard, keep it in every locale:
  `Salut d'Amour`, `Gymnopédie No. 1`, `Eine kleine Nachtmusik`.
- If a market has its own canonical name, localize it: Vivaldi Spring →
  JA `四季 春 第1楽章`, KO `사계 '봄' 1악장`.

### Rules

1. `[<Miku keyword> Acappella]` prefix on every title, every locale.
2. Composer full name + ` - ` + piece. One consistent structure across locales (no surname-only
   or alternate framing — this was the Vivaldi outlier, fixed s348).
3. `Acappella` spelling matches the channel name (one word, double-p).
4. `defaultLanguage = en`; set localizations for en/ko/ja on every video.
5. Never imply an altered title is the historical title; credit the source in the description
   (`Composer - Piece (year)`).

## Current catalog (live, s348)

```text
[Miku Acappella] Erik Satie - Gymnopédie No. 1
  KO  [미쿠 아카펠라] 에릭 사티 - 짐노페디 1번
  JA  [初音ミク アカペラ] エリック・サティ - ジムノペディ第1番

[Miku Acappella] Antonio Vivaldi - Spring, Mvt. I
  KO  [미쿠 아카펠라] 안토니오 비발디 - 사계 '봄' 1악장
  JA  [初音ミク アカペラ] アントニオ・ヴィヴァルディ - 四季 春 第1楽章

[Miku Acappella] Scott Joplin - The Entertainer
  KO  [미쿠 아카펠라] 스콧 조플린 - 디 엔터테이너
  JA  [初音ミク アカペラ] スコット・ジョプリン - ジ・エンターテイナー

[Miku Acappella] Edward Elgar - Salut d'Amour
  KO  [미쿠 아카펠라] 에드워드 엘가 - 사랑의 인사
  JA  [初音ミク アカペラ] エドワード・エルガー - 愛の挨拶
```

## Applying titles

Write access is automated via `Analytics/youtube_meta.py` (OAuth `youtube.force-ssl`,
read-modify-write so other fields are preserved):

```text
python Analytics/youtube_meta.py get <video_id>
python Analytics/youtube_meta.py set-title <video_id> --default "..." --en "..." --ko "..." --ja "..."
```

The same tool uploads custom thumbnails (`set-thumbnail`).
