import { Composition } from "remotion";
import { VisualizerComposition, VisualizerProps } from "./VisualizerComposition";

const FPS = 30;
const DURATION_SECONDS = 198;

const vivaldiProps: VisualizerProps = {
  letterboxColors: ["#3a4a32", "#b8a06e", "#5e4a3a"],
  composerName: "Antonio Vivaldi",
  pieceTitle: "Spring, Mvt. I",
  pieceSubtitle: "(after 1725)",
  audioPath: "audio.wav",
  coverPath: "cover.png",
};

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="MuseVivaldiSpring1Allegro"
        component={VisualizerComposition}
        durationInFrames={FPS * DURATION_SECONDS}
        fps={FPS}
        width={1920}
        height={1080}
        defaultProps={vivaldiProps}
      />
    </>
  );
};
