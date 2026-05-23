import { Composition } from "remotion";
import { VisualizerComposition, VisualizerProps } from "./VisualizerComposition";

const FPS = 30;
const DURATION_SECONDS = 140.0; // re-export 2026-05-23 (음량 ↑ · 2:20.0) = 4200 frames @30fps · covers full tail

const elgarProps: VisualizerProps = {
  // measured from final cover (Miku_waterhouse_soul_of_the_rose.png · 2026-05-22)
  // deep warm umber (shadow) → warm olive-gold (dominant) → terracotta (roof/pots/roses accent · bars)
  letterboxColors: ["#241a11", "#63552f", "#9e5c40"],
  composerName: "Edward Elgar",
  pieceTitle: "Salut d'Amour",
  pieceSubtitle: "(1888)",
  audioPath: "audio.wav",
  coverPath: "cover.png",
};

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="MuseElgarSalutDAmour"
        component={VisualizerComposition}
        durationInFrames={Math.round(FPS * DURATION_SECONDS)}
        fps={FPS}
        width={1920}
        height={1080}
        defaultProps={elgarProps}
      />
    </>
  );
};
