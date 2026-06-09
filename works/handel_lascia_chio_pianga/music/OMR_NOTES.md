# OMR 채보 노트 — Handel, Lascia ch'io pianga (HWV 7, Rinaldo / arr. Michel Rondeau)

## 소스
- `planning/candidates_opus/게오르크 프리드리히 헨델_울게 하소서.pdf` (5p · 벡터 인그레이빙 · 스캔 아님 · 래스터 0)

## 엔진
- **Audiveris 5.10.2** (winget `audiveris.org.Audiveris` · 번들 JRE 21 · `C:\Program Files\Audiveris\Audiveris.exe`)
- 배치 명령: `Audiveris.exe -batch -export -output <dir> -- <pdf>`
- 재엔진 산출: `MuseScore4.exe -o omr.png <musicxml>` (검증 렌더용)

## 산출물
- `handel_lascia_chio_pianga.musicxml` — 비압축 MusicXML (정본 deliverable)
- `handel_lascia_chio_pianga.mxl` — 압축본
- `omr_out/*.omr` — Audiveris 프로젝트 파일 (재편집/재인식 가능)

## 인식 구조 (검증 PASS)
- 5 파트: Soprano / Violin I / Violin II / Viola / Double Bass
- 음자리표: S·VlnI·VlnII = 높은음 / Vla = 알토(C) / DB = 낮은음 ✓
- 조표 = 내림표 1개 (F장조) · 박자 = **3/2** · 템포 = **♩(2분음표)=60 Largo** (PDF 원본 확대 확인 — 4분음표 아님)
- 42마디 (페이지별 마디수 원본과 정확 일치)
- 캡처된 음악 요소: 강약 46(p/pp/mp) · 슬러 68 · 트릴 5 · 페르마타 2 · 쉼표/임시표/머리·길이

## 검증 방법
- Audiveris MusicXML → MuseScore4 재엔진 PNG → 원본 PDF 렌더와 페이지별 대조 (p1, p5 정밀 / 구조 전체)
- music21 파싱으로 파트/마디/조표/박자 수치 확인

## ⚠️ 미캡처 (Tesseract OCR 언어팩 부재 — 음표 데이터엔 영향 없음)
1. **가사 (이탈리아어)** — 미캡처. ⑩ 가사는 별도 (가) 이탈리아어 트랙으로 처리하므로 무방.
2. **`D.C. al Fine` (다 카포 알 피네)** — 미캡처. ★ 이 곡은 ABA 다카포 형식 = A부 → B부 → 처음으로 돌아가 Fine까지. MusicXML엔 음표만 있고 이 반복 지시가 없음. V6 입력 시 형식 반영 필수.
3. 템포 단어("Largo")·재생용 metronome 마크 — 미캡처 (값 ♩=60은 위에 기록).

## 재실행 옵션
- 텍스트(가사/지시어)까지 박으려면 Tesseract `eng`+`ita` traineddata 설치 후 `-force` 재인식.
