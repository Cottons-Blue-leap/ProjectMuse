# YouTube Description — Saint-Saëns: The Swan (Le Cygne · Carnival of the Animals No.13)

> 양식 정본: [`../../../../workflows/video_release/docs/description_template.md`](../../../../workflows/video_release/docs/description_template.md) (custom_hook 경로 = 사탕요정·미뉴엣·헨델 family · Welcome 블록·Subscribe CTA 제거 axis)
> 박힌 날짜: 2026-06-22 · 코튼 hook LOCK (Discord)
> N=15 (.vpr 활성 보컬 트랙 실측: Violoncelle soprano+tenor 2 · Piano 1 high/high_mid×2/low/low_mid 5 · Piano 2 high×4/low×4 8 — 전부 unmuted)
> ★ 사육제 14연작 **앵커곡** · 시리즈 시그니처 '미쿠 컬러 동물'(미쿠=청록 백조) 첫 구현

## 영상 제목 (YouTube title · 【初音ミク A Cappella】 badge 양식)

- default/en: `Saint-Saëns - The Swan (The Carnival of the Animals) 【初音ミク A Cappella】`
- ko: `생상스 - 백조 (동물의 사육제) 【初音ミク A Cappella】`
- ja: `サン＝サーンス - 白鳥（動物の謝肉祭） 【初音ミク A Cappella】`
- es/pt/de/fr/ru/zh-Hant/zh-Hans = `title.{lang}.txt` (localize_batch 생성 · 부모작 병기 포함)
- ★ **부모작 병기 (s411 enrich · 2026-06-25 코튼 적발·수정)**: 발췌곡 = 부모작 정식명 괄호 병기(검색량 압도 · 사탕요정→(The Nutcracker) family). 백조=《동물의 사육제》 13악장이라 라이브 10로케일 retro-fit. 괄호 = ja/zh 전각（）·라틴/키릴 반각. **title=병기 / body(custom_hook)=단독 곡명 'El cisne (1886)' 유지**(localize_batch `piece` 필드만 수정 · custom_hook 불변).

## Hook 설계 (코튼 LOCK 2026-06-22)

- **형식 = 1행 epithet** (코튼 지정): "미쿠가 백조가 되었습니다!" / EN "Miku has become a swan!" / JA "ミクが白鳥になりました！" — 커버(미쿠=청록 백조) + 시리즈 시그니처 정합. Handel/Mozart family.
- 2행 = N 미쿠 라인 "열다섯 명의 미쿠가 노래합니다 —" / "Now fifteen Mikus sing —" / "いま、15人のミクが歌います —".
- 3행 = 작곡가 풀네임 - 곡 - 1886.
- 생상스 '생전 〈백조〉만 출판 허락' 일화 = description 제외 → **고정댓글 후보**(코튼 publish 직후 확정 예정).

## 곡명 로케일 정책 (코튼 원칙: 세계 표준 / 로케일 통용명)

- EN The Swan / KO 백조 / JA 白鳥 / es El cisne / pt O cisne / de Der Schwan / **fr Le Cygne(원제)** / ru Лебедь / zh-Hant 天鵝 / zh-Hans 天鹅.
- 작곡가 = EN/es/pt/de/fr `Camille Saint-Saëns` (성 Saint-Saëns) / ru Камиль Сен-Санс / zh-Hant 卡米爾·聖桑 / zh-Hans 卡米尔·圣桑.

## Cover art

`Cover art, after Friedrich, 'Swans in the Reeds' (c.1820).` + Wikimedia URL (https://commons.wikimedia.org/wiki/File:Friedrich_schwaene-im-schilf.jpg). Caspar David Friedrich d.1840 PD강. 화가맵 = **Saint-Saëns=Friedrich**. ※커버 = 두 백조 중 좌측을 미쿠 청록 채색(얼굴 X · §1 미쿠 컬러 동물).

## 9언어 sidecar 상태

- **en/ja/ko** = hand-sidecar 정본 (description.{en,ja,ko}.txt · 코튼 hook LOCK).
- **es/pt/de/fr/ru/zh-Hant/zh-Hans** = `localize_batch.py` WORKS custom_hook 생성 (description.{lang}.txt + title.{lang}.txt). localize_batch 추가 = PAINTER['Friedrich'] 음역 + TAG_COMPOSER['Saint-Saëns'](하이픈 회피).
- **외부 QA subagent 게이트** = l10n cross-verification (적용 결과는 아래 기록).

## 백엔드 태그

`description.tags.txt` (434/500자 · 곡별 앞 + 공통 베이스 · 3국어+음역).

## 적용 (vid 2nK8fOWxqxU · 구 RXqDKd3fvlc 재믹스로 삭제·교체)

- 코튼 업로드+예약 완료 (2026-06-22 · 첼로 묻힘 재믹스 재업로드본).
- API 적용 = youtube_meta set-title(default/en/ko/ja + --loc 7 + defaultLang en) → set-description(default/en/ja/ko) → localize_batch push --only saint_saens_the_swan(7 로케일) → set-tags(47개·434/500) → set-thumbnail(v5). **AUDIT PASS (2026-06-22)** = localize 10로케일 PASS + get 검증. 메타 콘텐츠 = 구영상 동일(오디오만 첼로부각본 교체).
