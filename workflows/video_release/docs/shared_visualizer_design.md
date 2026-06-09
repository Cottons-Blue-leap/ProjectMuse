# Shared Visualizer 통합 설계 (B) — s412

> **상태 = ✅ 구현 완료 (s412)**. 공유 프로젝트 라이브 · `python muse.py render <work_id>` 동작 ·
> 검증 게이트 통과(보케리니 프레임 45·3500·7019 md5 = per-work와 비트 단위 일치) ·
> 디스크 회수 ~6.6GB (node_modules 9×~590MB ≈ 5.2GB + 발행작 spent WAV 1.41GB) ·
> ccf27a 4곡(boccherini·chopin·pachelbel·sugarplum) props.json 마이그레이션 완료 ·
> 전 work per-work src/config 삭제 · `muse doctor` 전체 PASS.
> mozart = `renders/Miku_Ah!…wav`가 발행 영상 오디오와 md5 일치 → masters/ 컨벤션 이전
> 레거시 배치의 사실상 master로 확인·보존(정리 불필요).
>
> 목표 = 곡마다 독립 Remotion 프로젝트(~590MB node_modules) 복제를 제거하고,
> **단일 canonical 엔진 + work별 입력(props + audio + cover)** 양식으로 전환.
> 원칙 = **forward-only** (과거 발행분 재렌더 X · ⑩ 헨델부터 신 양식 적용).
> canonical 엔진 = **ccf27a (라이브 검증)** — 코튼 결단 (s412).

---

## 1. 현 상태 (실측 · s412)

- **9 works × ~590MB node_modules ≈ 5.3GB 중복** (메모리 기록 2.4GB는 과소)
  - 내역: `chrome-headless-shell.exe` 194MB + `webpack .cache` ~90MB(재생성 가능) + deps
- **엔진(`VisualizerComposition.tsx`) 4버전 드리프트**:
  | hash | works | 비고 |
  |------|-------|------|
  | `ccf27a` ×4 | 쇼팽·파헬벨·사탕요정·보케리니 | **최신 · 라이브/예약 검증 → canonical** |
  | `6eeda4` ×3 | 엘가·조플린·비발디 | |
  | `8376f5` ×1 | 짐노페디 | 첫 작품 |
  | `c96a8b` ×1 | 모차르트 | |
  | (`95f7f5`) | templates/visualizer-composition.s381-bandremap.tsx | **어느 라이브에도 미사용 → superseded 처리** |
- **work별 진짜 차이 = `Root.tsx`의 props 1덩어리 + `public/{audio.wav, cover.png}`**
  - 엔진 / `index.ts` / `remotion.config.ts` / `tsconfig.json` = 사실상 동일
- Remotion 버전도 work마다 제각각(4.0.460~467) — 엔진 드리프트와 동반

## 2. 아키텍처

### 2.1 공유 프로젝트 = `workflows/video_release/visualizer/`
```
visualizer/
  package.json          # 단일 deps (remotion ^4.0.446 · react 19) — 한 번 설치
  remotion.config.ts
  tsconfig.json
  node_modules/         # THE single install (유일)
  src/
    index.ts
    Root.tsx            # GENERIC — id="MuseVisualizer" · calculateMetadata로 길이/치수 산출
    VisualizerComposition.tsx   # canonical ccf27a 1:1 복사 (한 글자도 안 고침 = 출력 보존)
  public/
    fonts/GFSDidot-Regular.ttf  # studio 프리뷰용 fallback (실렌더는 work public 사용)
```

### 2.2 work별 잔존 = 입력만
```
works/<id>/video/visualizer/
  props.json            # VisualizerProps + durationSeconds (기존 Root.tsx props 이관)
  public/
    audio.wav
    cover.png
    fonts/GFSDidot-Regular.ttf   # staticFile 폰트 (~수백KB · dup 허용 = node_modules 대비 무시 가능)
```
→ **src / node_modules / package.json / config 전부 제거** (회수 대상)

### 2.3 렌더 호출
- 신규 스크립트 `workflows/video_release/scripts/muse_render.py` → `muse.py` SCRIPTS에 `"render"` 등록
- 호출: `python muse.py render <work_id>`
  - work의 `props.json` 로드
  - 공유 프로젝트 디렉토리에서 실행:
    ```
    npx remotion render src/index.ts MuseVisualizer \
      ../../../works/<id>/video/exports/<id>_final.mp4 \
      --props=<work>/video/visualizer/props.json \
      --public-dir=<work>/video/visualizer/public
    ```
  - 기존 per-work `npm run render` 대체

### 2.4 핵심 코드 변경 = `Root.tsx` 1곳만
- **현재**: props·`durationInFrames` 하드코딩 (work마다 다른 파일)
- **신규 generic** (work 무관 · 단일 파일):
  ```tsx
  export const RemotionRoot = () => (
    <Composition
      id="MuseVisualizer"
      component={VisualizerComposition}
      fps={30}
      width={2560}
      height={1440}
      defaultProps={FALLBACK_PROPS}
      calculateMetadata={async ({ props }) => ({
        durationInFrames: Math.round(30 * props.durationSeconds),
      })}
    />
  );
  ```
  - `durationSeconds`를 props로 받아 길이를 렌더 시점에 산출 (Remotion 4.0.x `calculateMetadata` 지원)
- **`VisualizerComposition.tsx` = ccf27a 그대로** → 출력 1:1 보존

## 3. 검증 게이트 (적용 전 필수 · feedback_workflow_verify_axes + self_audit_limits)

1. 이미 렌더된 ccf27a work 1개 선택 (예: **보케리니** — 최근·ccf27a)
2. 공유 프로젝트 + 그 work의 props/public으로 재렌더
3. 기존 출력과 대조 — **md5 아닌 시각+스펙 패리티**:
   - 치수 2560×1440 · 총 프레임 수 · 샘플 프레임 픽셀(시작/중간/끝) · 오디오 스트림 동일
   - ⚠️ 인코더 비결정성으로 컨테이너 md5는 다를 수 있음 → 시각 패리티로 판정
4. **통과 시에만** ⑩ 적용 + 디스크 회수 진입

## 4. 실행 시퀀스

1. 공유 프로젝트 생성 (ccf27a 엔진 복사 + generic Root 작성 + `npm install` 1회 + 폰트 배치)
2. `muse_render.py` 작성 + `muse.py` 등록
3. **보케리니로 검증 게이트** (§3)
4. ⑩ 헨델 = 신 양식 첫 제작 (props.json + audio + cover만 — node_modules X)
5. **디스크 회수** = 9개 per-work `node_modules` + webpack cache 삭제 (~5.3GB)
   - per-work `src/`는 `_archive/`로 (엔진 히스토리 보존) 또는 삭제
6. 문서 갱신 (`video_workflow.md` · templates supersede 표기 · `CONVENTIONS.md`) + 커밋

## 5. 리스크 레지스터

| 리스크 | 처리 |
|--------|------|
| 폰트: `staticFile("fonts/...")` → public-dir에 폰트 필요 | work `public/`에 `fonts/` 유지 (확인됨) |
| `calculateMetadata` 길이 구동 | Remotion 4.0.x 지원 ✓ · 게이트서 검증 |
| audio/cover 경로 해소 | `--public-dir`로 `audio.wav`/`cover.png` 경로 일치 ✓ |
| 인코더 비결정성 | 컨테이너 md5 X → 시각+스펙 패리티 판정 |
| 라이브/예약 영상 | **절대 재렌더 X** (forward-only 불가침) |

## 6. 부수 발견 (별도 축 · 묶음 가능)

- per-work `music/renders/`에 88MB 중간 WAV 다수(test1~5 · `Miku_*.wav` · `.bak`) → **추가 수 GB 회수 가능**. visualizer와 다른 정리 축이라 별도 cleanup으로 분리.

## 7. 미해결 결정 (코튼)

- per-work `src/` 처리: `_archive/` 보존 vs 삭제 (엔진 4버전 히스토리 = 기록 가치 vs 잡음)
- §6 음원 중간 WAV cleanup을 이 사이클에 묶을지 별도로 둘지
