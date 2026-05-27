import { Composition } from "remotion";
import { VisualizerComposition, VisualizerProps } from "./VisualizerComposition";

const FPS = 30;
const DURATION_SECONDS = 361.5;

const mozartProps: VisualizerProps = {
  // tentative palette from van Gogh — Starry Night Over the Rhône (1888)
  // deep night sky → cobalt blue river → warm gold reflected starlight (bars)
  letterboxColors: ["#0c1a3a", "#1c3a6e", "#d4a85e"],
  composerName: "W.A. Mozart",
  pieceTitle: '12 Variations on "Ah! vous dirai-je, maman"',
  pieceSubtitle: "",
  audioPath: "audio.wav",
  coverPath: "cover.png",
  variationStarts: [
    0.0, 28.0, 53.0, 79.0, 104.0, 129.0, 155.0, 180.0, 205.0, 231.0, 256.0,
    281.0, 309.0,
  ],
  variationLabels: [
    "Theme",
    "Var. 1",
    "Var. 2",
    "Var. 3",
    "Var. 4",
    "Var. 5",
    "Var. 6",
    "Var. 7",
    "Var. 8",
    "Var. 9",
    "Var. 10",
    "Var. 11",
    "Var. 12",
  ],
};

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="MuseMozartTwinkleVariations"
        component={VisualizerComposition}
        durationInFrames={Math.round(FPS * DURATION_SECONDS)}
        fps={FPS}
        width={2560}
        height={1440}
        defaultProps={mozartProps}
      />
    </>
  );
};
