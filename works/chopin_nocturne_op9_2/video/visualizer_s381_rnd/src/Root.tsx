import { Composition } from "remotion";
import { VisualizerComposition, VisualizerProps } from "./VisualizerComposition";

const FPS = 30;
const DURATION_SECONDS = 219.0;

const chopinProps: VisualizerProps = {
  // letterbox B — Whistler "Nocturne: Blue and Silver — Chelsea" identity
  // deep twilight sky → steel-blue river → silver light (bars)
  letterboxColors: ["#2e4257", "#5b7d9b", "#93b3cb"],
  composerName: "Frédéric Chopin",
  pieceTitle: "Nocturne",
  pieceSubtitle: "Op. 9 No. 2 · in E-flat major",
  audioPath: "audio.wav",
  coverPath: "cover.png",
  // ABA' nocturne flows continuously — chapter labels disabled (s385 cotton decision).
  // single zero-start with empty label = no label ever rendered.
  variationStarts: [0],
  variationLabels: [""],
};

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="MuseChopinNocturneOp9No2"
        component={VisualizerComposition}
        durationInFrames={Math.round(FPS * DURATION_SECONDS)}
        fps={FPS}
        width={2560}
        height={1440}
        defaultProps={chopinProps}
      />
    </>
  );
};
