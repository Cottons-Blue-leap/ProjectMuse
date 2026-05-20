import { Composition } from "remotion";
import { VisualizerComposition, VisualizerProps } from "./VisualizerComposition";

const FPS = 30;
const DURATION_SECONDS = 219;

const joplinProps: VisualizerProps = {
  letterboxColors: ["#2a3540", "#6c7574", "#5a4838"],
  composerName: "Scott Joplin",
  pieceTitle: "The Entertainer",
  pieceSubtitle: "(1902)",
  audioPath: "audio.wav",
  coverPath: "cover.png",
};

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="MuseJoplinTheEntertainer"
        component={VisualizerComposition}
        durationInFrames={FPS * DURATION_SECONDS}
        fps={FPS}
        width={1920}
        height={1080}
        defaultProps={joplinProps}
      />
    </>
  );
};
