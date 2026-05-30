<!--
name: <workflow_name>            # 폴더명과 동일 (snake_case)
stage: <N · 한 줄 설명>
type: cli | manual | reference | cli+manual
entry: <진입 명령 또는 진입 파일>
inputs: [<상위 산출물 경로>, ...]
outputs: [<이 워크플로우 산출물 경로>, ...]
depends_on: [<선행 워크플로우>, ...]
owner: MOKA | Cotton | Cotton+MOKA
-->

# <Workflow Name> Workflow

> 한 줄 목적. (이 워크플로우가 파이프라인에서 담당하는 자리)

## Inputs

```text
<상위 워크플로우 산출물 경로>
```

## Entry

```text
<진입 명령(cli) 또는 작성 파일(manual) 또는 참고 자료(reference)>
```

## Outputs

```text
<이 워크플로우가 만드는 산출물 경로>
```

## Notes

- 상세 절차는 `docs/`에.
- 실행 스크립트는 `scripts/`에 (`muse_*.py` prefix).
- 단독 양식은 `templates/`에 · 공유 양식은 `../shared/templates/`에.

---
*신축 절차: 본 폴더를 복사 → front-matter 채움 → 불필요한 하위 폴더(docs/scripts/templates) 삭제 → `../registry.json` 등재. 상세 = `../README.md`.*
