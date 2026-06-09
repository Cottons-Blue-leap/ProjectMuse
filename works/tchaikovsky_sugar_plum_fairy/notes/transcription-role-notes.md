# 사탕요정의 춤 — 채보 / Role 분배 노트

> 코튼 V6 직접 입력용 가이드. 채보(picking)는 코튼 몫이고, 본 노트는 **role 분배 + 텍스처 안내 + 게이트**다.
> 악보 = `music/source_scores/tchaikovsky_sugar_plum_fairy.pdf` (7p 발췌 · 원본 풀스코어 p48~54).
> 작성 = MOKA 2026-06-04 (p48 도입부 실측 + 곡 구조 통념).

## 곡 개요

- Tchaikovsky, 호두까기 모음곡 Op.71a, No.2(b) **Danse de la Fée-Dragée** (사탕요정의 춤)
- **Andante non troppo · 2/4 · e단조** (조표 #1)
- 길이 ~1:50–2:00 · 발췌 없이 통째
- 원편성 = **첼레스타 솔로**(주역) + **현 전체 pizz.**(피치카토 반주) + 베이스 클라리넷/저음 관악 보조

## 텍스처 실측 (p48 도입부)

- 상단 관악(Flauto·Oboe·Clarinetto 등) = 도입부 전부 쉼표 → 텍스처가 매우 얇음.
- **Celesta (ou Piano)** staff에 주선율 (R.H. 영롱한 16분 하행 + L.H. 화성).
- **Violini I/II(à Soli)·Viola·Celli·C-Bassi 전부 pizz.** = 짧고 건조한 staccato 반주.
- → 캐논·하이든 빠른악장 대비 **성부 수 적고 명료** = 채보 부담 낮음 (전환 사유 '리스크 분리' 실측 확인).

## Role 분배 (제안 · 코튼 최종 결단)

| V6 role | 담당 원성부 | 모음/주법 |
|---|---|---|
| **lead_miku** | 첼레스타 R.H. 주선율 | Ah/Oo · 영롱한 staccato 어택, 16분 또렷이 |
| **halo_high** | 첼레스타 L.H. 상단·반짝임 공명 | Oo/Mm · 가벼운 상단 글로우 |
| **mid_oo** | 현 pizz 화성 (Viola·Violini) | Oo · 짧은 스타카토 |
| **low_oo** | 현 pizz 베이스 (C-Bassi·Celli) | Oo · 건조한 저음 스타카토 |
| **air_mm** | glue | Mm · 전체 접착 |

## 게이트 (본 곡 핵심 challenge)

- **staccato 어택 명료도**: 첼레스타의 *영롱함* + 피치카토의 *짧고 건조한* 어택이 미쿠 모음(Ah/Oo) staccato에서 사는지.
- 캐논(레가토 성부 쌓기)과 **정반대 축** — 여기선 끊어치는 점묘(pointillism)가 곡의 정체성. 모음이 뭉개지면 사탕요정 특유의 반짝임이 죽는다.
- 첼레스타 16분 하행 주제 = 이 곡의 시그니처 → lead_miku 또렷함이 1순위.

## 진행 메모

- 명화 커버 = V6 입력 완주 후 무드 재결정 (캐논·하이든 선례). CSV 기본값 Degas는 무드 mismatch → 재선정.
- 발행 = (a) 지금 제작→지금 발행 확정 (에버그린 · 코튼 2026-06-04).
- 마스터링 = MOKA 계측 자문 축 (LUFS/TP/dropout sweep · 청취불가 보완).
