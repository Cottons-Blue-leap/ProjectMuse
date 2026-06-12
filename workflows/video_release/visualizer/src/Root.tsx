import { Composition } from "remotion";
import { VisualizerComposition, VisualizerProps } from "./VisualizerComposition";
import { ShortsComposition, ShortsProps } from "./ShortsComposition";
import { CanonStageComposition, CanonStageProps } from "./CanonStageComposition";

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

// Shorts (9:16) — 본편과 같은 props 주입 양식. works/<id>/shorts/<slug>/props.json
const FALLBACK_SHORTS_PROPS: ShortsProps = {
  letterboxColors: ["#1f2c3d", "#4a5a6e", "#b8a673"],
  audioPath: "audio.wav",
  coverPath: "cover.png",
  revealLine1: "This is not an instrument.",
  revealLine2: "Sung entirely by Hatsune Miku.",
  revealAccent: "Hatsune Miku",
  reveal1Sec: 12,
  reveal2Sec: 15.5,
  endCardSec: 27,
  endCredit: "Erik Satie — Gymnopédie No. 1",
  endCta: "Full version on the channel",
  durationSeconds: 30,
};

// MikuDiscovery (9:16) — "창작자 발견 delight" 쇼츠 rig (s421). 디자인 전부 props.
const FALLBACK_DISCOVERY_PROPS: CanonStageProps = {
  audioPath: "audio.wav",
  bpm: 56,
  beatsPerBar: 4,
  scoreStartSec: 0.5,
  barsVisible: 6,
  voices: [
    { entryBar: 1, waitPath: "miku_wait.png", singPath: "miku_sing.png" },
    { entryBar: 3, waitPath: "miku_wait.png", singPath: "miku_sing.png" },
    { entryBar: 5, waitPath: "miku_wait.png", singPath: "miku_sing.png" },
  ],
  bgStops: ["#181d24", "#0c0e12"],
  tealActive: "rgb(60,200,190)",
  tealDim: "#7fb8b2",
  cream: "#f0ead8",
  title: "CANON",
  subtitle: "A ROUND, 2 BARS APART",
  gapLabel: "2 bars",
  footText: "sung by Hatsune Miku",
  mikuWidth: 200,
  durationSeconds: 24,
};

export const RemotionRoot: React.FC = () => {
  return (
    <>
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
      <Composition
        id="MuseShort"
        component={ShortsComposition}
        fps={FPS}
        width={1080}
        height={1920}
        durationInFrames={Math.round(FPS * 30)}
        defaultProps={FALLBACK_SHORTS_PROPS}
        calculateMetadata={async ({ props }) => ({
          durationInFrames: Math.round(FPS * Number(props.durationSeconds ?? 30)),
        })}
      />
      <Composition
        id="MikuDiscovery"
        component={CanonStageComposition}
        fps={FPS}
        width={1080}
        height={1920}
        durationInFrames={Math.round(FPS * 24)}
        defaultProps={FALLBACK_DISCOVERY_PROPS}
        calculateMetadata={async ({ props }) => ({
          durationInFrames: Math.round(FPS * Number(props.durationSeconds ?? 24)),
        })}
      />
    </>
  );
};
