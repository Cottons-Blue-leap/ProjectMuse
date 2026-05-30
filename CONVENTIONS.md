# Project Muse — Conventions (명명 · 아카이빙 · 일회성 파일)

> 전 프로젝트 단일 소스. 워크플로우 양식 = [`workflows/README.md`](workflows/README.md) · 파일 명명 = [`workflows/naming_convention.md`](workflows/naming_convention.md).
> 박힌 날짜: 2026-05-30 (reorg P3).

## 1. 디렉토리별 `_archive/` 독트린

`planning/_archive/` + `planning/_keepers/` (s371) 모델을 전 디렉토리로 일반화한다.

| 폴더 | 자리 | 채우는 시점 |
|---|---|---|
| `<dir>/_archive/` | 닫힌 cycle 산출물 (1회용 스크립트 · 백업 사이드카 · audit dump) · **직접 호출 X** | cycle 종료 시점 |
| `<dir>/_keepers/` | 미래 reference 가치 있는 cycle 산출물 (audit baseline · 결단 draft · R&D 자료) | 가치 약해지면 `_archive/`로 강등 |

- 재사용 도구는 **부모 디렉토리 root에 keep** (아카이브 X). 예: `planning/_apply_tier_review.py`·`_renumber_csv.py`·`_audit_new_pdfs.py`.
- 즉시 삭제 X — 폐기 자료는 `_archive/`로 이동 ([[feedback-unknown-dir-investigate]] + 백업 사이드카 보존 독트린).

## 2. 일회성 스크립트 표식

1회용(특정 cycle·특정 곡 전용, 재사용 의도 없음) 스크립트는 docstring/헤더 첫 줄에 표식:

```python
# ONE-OFF (2026-05-29 · s380 · Mozart K.265 publish 직후 stats snapshot)
```

- `muse_tidy.py`(루트)가 `_`프리픽스 스크립트를 스캔 → ONE-OFF 표식/위치로 분류 → **목록만 제시** (자동 이동·삭제 X).
- 코튼이 승인한 것만 해당 디렉토리 `_archive/`로 이동.

## 3. 명명 위생

- **piece_id / 파일 양식**: `workflows/naming_convention.md` (v1 · s332) 정본.
- **폴더·파일명**: ASCII snake_case 권장 · 공백 X (cmd line escape risk). 한글 문서명은 허용(콘텐츠 자료).
- **세션 표식(sXXX)**: 파일명 증식 대신 **본문 s-notation + 단일 정본 파일명 + git 히스토리**. (cycle 산출물·백업은 예외적으로 `_*_sXXX` 표식 허용 — 추적성.)
- **스크립트 prefix**: 워크플로우 실행 스크립트 = `muse_*.py`. 1회용·내부 = `_*` prefix.

## 4. 바이너리 / 산출물

`.gitignore` axis 정합: 음악(wav/mp3/vpr/mid) · 영상(mp4/mov) · 이미지(png/jpg, assets 예외) · Office(pptx/docx) · PDF · node_modules · 렌더/마스터 = git 제외. source-of-truth(md/json/csv/py/tsx/ts)만 commit.

## 5. works 정본 골격

`workflows/project_setup/README.md` *Created Contract* 정본. `muse_project.py doctor`로 검사. 레거시는 `_LEGACY.md` 표식.
