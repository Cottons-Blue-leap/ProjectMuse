# YouTube Description — Gossec: Gavotte (in D major · from the opera Rosine)

> 양식 정본: [`../../../../workflows/video_release/docs/description_template.md`](../../../../workflows/video_release/docs/description_template.md) (custom_hook family = 미뉴엣·헨델·하이든 · Welcome 블록·Subscribe CTA 제거 axis)
> vid = `mJhe2RyCzcA` · 박힌 날짜: 2026-06-29 · 코튼 hook LOCK (Discord)
> N=15 (.vpr 활성 보컬 트랙 실측: Lead 7 + Base 8 — 전부 unmuted)

## 영상 제목 (YouTube title · 【初音ミク A Cappella】 badge 양식)

- default/en: `Gossec - Gavotte 【初音ミク A Cappella】`
- ko: `고섹 - 가보트 【初音ミク A Cappella】`
- ja: `ゴセック - ガヴォット 【初音ミク A Cappella】`
- es/pt/de/fr/ru/zh-Hant/zh-Hans = `title.{lang}.txt` (localize_batch 생성)
- ★ **부모작 병기 미적용**: 발췌곡 부모작 병기 규칙은 *부모작이 고검색일 때*만(Nutcracker/Carnival family). 본곡 부모작 = 오페라 〈Rosine〉(1786) = 사실상 무검색 / **gavotte 자체가 검색어**(스즈키 교본 단골) → 병기 X, 단독 'Gavotte' 유지.

## Hook 설계 (코튼 LOCK 2026-06-29)

- **형식 = 토막상식형 2행** (미뉴엣 family · 표준 "{N} Mikus" 템플릿 벗어남): "제목을 이제야 알게 되었다!" + "가보트는 미뉴엣처럼 프랑스 궁정에서 유행했던 춤곡입니다. 바이올린 학습에 많이 사용된다네요."
- **누구나 멜로디는 아는데 이름은 몰랐던 곡** 인지를 노린 hook (스즈키 바이올린 1권 표준 소품).
- **쉼표 제거** = 코튼 지시("AI 느낌") — hook 전 로케일 쉼표 최소 자연 구문.
- 사실관계 = 검증 PASS (가보트·미뉴엣 = 프랑스 궁정 춤곡 ✓ / 본곡 = 스즈키 바이올린 교본 표준 ✓).

## 곡명/작곡가 로케일 정책

- 곡명 = 통용명: EN/de/fr Gavotte / es/pt Gavota / ru Гавот / zh 加沃特舞曲 / ko 가보트 / ja ガヴォット.
- 작곡가 surname = Gossec / Госсек / 戈塞克 / 고섹 / ゴセック. full = François-Joseph Gossec (로케일 음역).

## Cover art

`Cover art, after Lancret, 'La Camargo Dancing' (c.1730).` + Wikimedia URL (https://commons.wikimedia.org/wiki/File:La_Camargo_Dancing.jpg). Nicolas Lancret d.1743 → PD강. 화가맵 = **Gossec=Lancret** (시리즈 첫 Lancret · ⑩ 미뉴엣 Longhi와 구분).
- ★ **시리즈 첫 '미쿠=관찰자' 커버**: 춤추는 La Camargo(원작 보존) + 우측 부채 든 구경꾼을 미쿠로(청록 twin-tails·측면 시선). 명화 제목은 본문서 영어 유지(localize_batch 규약).

## 10언어 sidecar 상태

- **en/ja/ko** = hand-sidecar 정본 (description.{en,ja,ko}.txt · 코튼 hook LOCK · 쉼표 제거).
- **es/pt/de/fr/ru/zh-Hant/zh-Hans** = `localize_batch.py write --only gossec_gavotte` 생성 (description.{lang}.txt + title.{lang}.txt). localize_batch 추가 = PAINTER['Lancret'] + TAG_COMPOSER['Gossec'] + WORKS 엔트리(custom_hook 7로케일).
- **외부 QA = l10n cross-verification 게이트** (Claude QA → 웹 사실검증 → 교차모델 paste · 발행 전후 권장).

## 백엔드 태그

`description.tags.txt` (378/500자 · 41태그 · 곡별[Gavotte/Gossec/Suzuki violin/가보트/고섹/ガヴォット/ゴセック/加沃特/戈塞克] + 공통 베이스 · 3국어+음역).

## 적용 (vid mJhe2RyCzcA)

- API 적용 순서 = youtube_meta set-title(default/en/ko/ja + --loc 7 + defaultLang en) → set-description(default/en/ja/ko) → localize_batch push --only gossec_gavotte(7 로케일) → set-tags(41개·378/500) → set-thumbnail(cover) → 재생목록 'Miku in the Classical Era' 추가 → AUDIT(get 검증 · localize 10로케일 PASS).
