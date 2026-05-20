# gymnopedie_1_first_proof

> **Status**: published 2026-05-14 (YouTube: https://youtu.be/rRnl8RZ3EjY)
> **Legacy structure note**: 본 작품은 *Project Muse* 첫 dogfood 통과 자리 (s275~s300).
> `naming_convention.md` v1 (s332) + workflow 양식 (s302~) 자체엔 이전 박힘.
> 구 구조 (`music/analysis/`, `music/arrangement/`, `music/midi/`, `music/source_scores/`, `music/vocaloid/`) keep · publish 통과 doctrine 정합 retrofit X.
> 신축 작품은 `joplin_the_entertainer` family 양식 참조.

First dogfood piece (s275 진입, canon_in_d_first_proof 폐기 후 교체):

```text
piece: Gymnopédie No. 1 (Erik Satie, 1888)
release title: TBD (title_naming_guide 참조)
composer credit: after Erik Satie, Gymnopédie No. 1
section: 통째 (~80마디 ABA 구조)
```

설계 한 줄 (코튼 s275 결단):

> 멜로디는 노래하게, 베이스는 걷게, 내성은 색만 남기고, 침묵은 악기로 취급하기.

Source MusicXML:

```text
music/source_scores/gymnopedie_1.musicxml
```

Audiveris OCR (5/12 통과) 결과를 작업 사본으로 가져옴. 원본 OCR 출력은
`works/musicxml/satie_gymnopedies/musicxml/`에 그대로 보존.

Score 분석 → arrangement 초안 → role-design 정합 → MIDI → V6 렌더 순서.
중간 단계 산출물은 `music/analysis/`, `music/arrangement/`,
`music/vocaloid/`, `music/midi/`에 차례로 등재.

## 캐논 폴더 폐기 사유

- 8성 카논 구조라 entry 중첩 처리부터 복잡 → 첫 dogfood 검증 부담
- 짐노페디 1번 = sparse 텍스처라 role 분할 효과를 깔끔히 검증 가능
- "간단한 것에서부터 차근차근 퀄리티를 높여나가자" (코튼 s275)
