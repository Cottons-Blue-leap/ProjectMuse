import { Composition } from "remotion";
import { VisualizerComposition, VisualizerProps } from "./VisualizerComposition";

const FPS = 30;
const DURATION_SECONDS = 189;

const gymnopedieProps: VisualizerProps = {
  letterboxColors: ["#1f2c3d", "#4a5a6e", "#b8a673"],
  composerName: "Erik Satie",
  pieceTitle: "Gymnopédie No. 1",
  pieceSubtitle: "(after 1888)",
  audioPath: "audio.wav",
  coverPath: "cover.png",
};

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="MuseGymnopedie1"
        component={VisualizerComposition}
        durationInFrames={FPS * DURATION_SECONDS}
        fps={FPS}
        width={1920}
        height={1080}
        defaultProps={gymnopedieProps}
      />
    </>
  );
};
