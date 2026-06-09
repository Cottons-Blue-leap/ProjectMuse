import { Composition } from "remotion";
import { VisualizerComposition, VisualizerProps } from "./VisualizerComposition";

// ──────────────────────────────────────────────────────────────────────────
// GENERIC shared visualizer root — work-agnostic (s412 통합 양식 B).
//
// 단일 Composition "MuseVisualizer"가 모든 곡을 처리한다. work별 데이터(props +
// durationSeconds)는 렌더 시점에 `--props=<work>/props.json`으로 주입되고, 영상 길이는
// props.durationSeconds로부터 calculateMetadata에서 산출된다. 그래서 work마다 Root를
// 복제할 필요가 없다.
//
// 엔진 VisualizerComposition = canonical ccf27a — 한 글자도 고치지 않음 (출력 1:1 보존).
// 설계 = workflows/video_release/docs/shared_visualizer_design.md
// ──────────────────────────────────────────────────────────────────────────

const FPS = 30;
const WIDTH = 2560;
const HEIGHT = 1440;

// 렌더 시 --props로 항상 덮어쓰인다. Studio 프리뷰/타입 안전을 위한 fallback일 뿐.
const FALLBACK_PROPS: VisualizerProps = {
  letterboxColors: ["#1A2A2C", "#262019", "#7E6A42"],
  composerName: "Composer",
  pieceTitle: "Title",
  pieceSubtitle: "",
  audioPath: "audio.wav",
  coverPath: "cover.png",
  variationStarts: [0],
  variationLabels: [""],
  durationSeconds: 60,
};

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="MuseVisualizer"
      component={VisualizerComposition}
      fps={FPS}
      width={WIDTH}
      height={HEIGHT}
      durationInFrames={Math.round(FPS * 60)}
      defaultProps={FALLBACK_PROPS}
      calculateMetadata={async ({ props }) => ({
        durationInFrames: Math.round(FPS * Number(props.durationSeconds ?? 60)),
      })}
    />
  );
};
