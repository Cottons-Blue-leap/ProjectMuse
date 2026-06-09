# 울게 하소서 — 가사 · 발음 · 편곡 설계

> ⑩ Handel, *Lascia ch'io pianga* (from Rinaldo HWV 7b, Act II, 1711)
> 가사 방향 = **(가) 이탈리아어 가사 시도** (코튼 결정 2026-06-08)
> 폴백 = 발음 품질 미달 시 **(나) 보칼리제(모음 Ah/Oo)**. 게이트에서 분리 판정.

---

## 1. 가사 원문 (PD · Giacomo Rossi 리브레토 1711)

**A절**
```
Lascia ch'io pianga
mia cruda sorte,
e che sospiri
la libertà.
```

**B절**
```
Il duolo infranga
queste ritorte
de' miei martiri
sol per pietà.
```

**구조 = da capo 아리아 (A – B – A)** : A절 → B절 → **A절 반복(da capo)**.
- 원곡은 da capo에서 소프라노가 즉흥 장식(ornamentation)을 얹지만, 미쿠 path에서는 **1차로 장식 없이 동일 반복** 권장(첫 가사 입력 곡 = 변수 최소화). 장식은 청취 후 별도 결단.

### 직역 (참고 · 영상 description 아님)
> 울게 하소서, 나의 잔혹한 운명을 / 그리고 자유를 향해 탄식하게 하소서.
> 이 비탄이 내 고통의 사슬을 부수기를 / 오직 자비로써.

---

## 2. V6 발음 음소 가이드 (이탈리아어)

미쿠 V6는 음소 직접 입력 가능. 이탈리아어는 **순수모음 5개(a·e·i·o·u)** 기반이라 일본어 모음과 가깝게 매핑됨 — 영어보다 오히려 미쿠에 유리할 수 있음. 핵심 주의 = **이중모음 활음(j/w)** 과 **r(탄설음)**.

| 단어 | 음절 분해 | 근사 발음(로마자) | IPA | 주의 |
|---|---|---|---|---|
| Lascia | La-scia | **LAH-sha** | ˈlaʃa | sci = ʃ(영어 sh) |
| ch'io | ch'io | **KYO** (1음절) | ˈkjo | ch=k · io 합쳐 1음절 활음 |
| pianga | pian-ga | **PYAHN-ga** | ˈpjaŋga | pi=활음 pj · g 경음 |
| mia | mi-a | **MEE-a** | ˈmia | 2모음 명확히 |
| cruda | cru-da | **KROO-da** | ˈkruda | r 탄설음 |
| sorte | sor-te | **SOR-teh** | ˈsɔrte | o 열린모음 |
| e | e | **EH** | e | 단모음 |
| che | che | **KEH** | ke | ch=k |
| sospiri | so-spi-ri | **so-SPEE-ree** | soˈspiri | |
| la | la | **LAH** | la | |
| libertà | li-ber-tà | **lee-ber-TAH** | liberˈta | 끝 강세 à |
| Il | il | **EEL** | il | |
| duolo | duo-lo | **DWOH-loh** | ˈdwɔlo | du=활음 dw |
| infranga | in-fran-ga | **een-FRAHN-ga** | inˈfraŋga | |
| queste | que-ste | **KWEH-steh** | ˈkweste | qu=kw |
| ritorte | ri-tor-te | **ree-TOR-teh** | riˈtorte | r 탄설음 |
| de' | de' | **DEH** | de | 생략형, 짧게 |
| miei | miei | **MYEH-ee** (1~2음절) | ˈmjɛi | mj 활음 + ɛi |
| martiri | mar-ti-ri | **mar-TEE-ree** | marˈtiri | |
| sol | sol | **SOL** | sɔl | |
| per | per | **PEHR** | per | |
| pietà | pie-tà | **pyeh-TAH** | pjeˈta | pj 활음 + 끝 강세 |

**발음 게이트 체크포인트** (V6 입력 후 코튼 청취):
1. `ʃ`(Lascia), `kj/pj/dw/kw`(ch'io·pianga·duolo·queste) 활음이 뭉개지지 않는가
2. `r` 탄설음이 영어식 접근음으로 흐려지지 않는가 (미쿠 약점 예상 1순위)
3. 끝 강세 `libertà·pietà` 의 모음이 살아있는가
→ 2~3 항목이 심하게 무너지면 **(나) 보칼리제 폴백** 발동.

---

## 3. 편곡 · 성부 설계 (잠정 — 청취 게이트 전)

원곡 = **소프라노 솔로 + 현악 + 콘티누오**, 느린 사라반드 풍(3/4, F장조, Largo). 정서 = 비탄·체념의 절제된 아름다움.

| 성부 | 원곡 라인 | 미쿠 처리 | 텍스트 |
|---|---|---|---|
| **Lead** | 소프라노 아리아 | lead_miku | **이탈리아어 가사 (full)** |
| **Mid** | 제1·2바이올린, 비올라 화성 | mid_oo (3~4성) | 모음 Ah/Oo 패드 |
| **Low** | 첼로 + 콘티누오 베이스 | low_oo (1~2성) | 모음 Oo |
| (glue) | — | air_mm | 약하게 |

**설계 의도**
- 가사는 **Lead만** 부르고 나머지는 모음 패드 — 아리아 텍스트의 명료성을 지키고, 다성부가 가사를 동시에 부를 때의 혼탁을 피함.
- 단, B절 클라이맥스나 da capo에서 **핵심 구절(예: "pietà")을 mid가 화음으로 합류**시키는 변주는 청취 후 실험 여지.
- 느린 곡 → 레가토·다이내믹이 생명. 갈랑 스타카토였던 ⑨ 보케리니와 정반대 캐릭터. 마스터링 시 LRA(다이내믹) 보존이 ⑨보다 더 중요.

**길이 예상** = da capo 포함 약 4:30~5:30 (largo 템포 · 반복 처리 따라 가변).

---

## 4. 미해결 결단 (코튼 confirm 대기)

1. **가사 vs 보칼리제** — V6 입력 후 발음 게이트 판정 (위 §2.3).
2. **da capo 장식** — 1차 무장식 반복 권장 / 장식은 청취 후.
3. **명화** — Tiepolo *Rinaldo and Armida*(default)는 '유혹' 주제라 '투옥된 비탄' 정서와 미세 어긋남. 음악 LOCK 단계에서 정서 직결 후보 재탐색 여지 (예: 비탄/체념의 단독 여인상). 화가맵 = Handel 첫 작품(중복 없음).
4. **재생목록** = Miku in the Baroque Era (비발디·파헬벨 공유).
