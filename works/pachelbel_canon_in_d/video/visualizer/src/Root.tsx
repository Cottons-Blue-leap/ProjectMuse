import { Composition } from "remotion";
import { VisualizerComposition, VisualizerProps } from "./VisualizerComposition";

const FPS = 30;
const DURATION_SECONDS = 348.0; // 5:48.0 — master 실측 (Miku_pachelbel_canon_in_d_master.wav)

const pachelbelProps: VisualizerProps = {
  // letterbox — Vermeer "A Young Woman seated at a Virginal" (NG2568) identity · Option B (코튼 s389).
  // dark teal accent (echoes Miku twin-tails + blue curtain) → dark warm → muted antique gold (bars).
  // 어두운 커버 가장자리(near-black warm)와 cohesive · 기존 cream bottom 밝기충돌 supersede.
  letterboxColors: ["#1A2A2C", "#262019", "#7E6A42"],
  composerName: "Johann Pachelbel",
  pieceTitle: "Canon in D",
  pieceSubtitle: "P.37 · in D major",
  audioPath: "audio.wav",
  coverPath: "cover.png",
  // canon = continuous variations over a ground bass — no discrete chapter labels.
  // single zero-start with empty label = no label ever rendered (chopin precedent).
  variationStarts: [0],
  variationLabels: [""],
};

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="MusePachelbelCanonInD"
        component={VisualizerComposition}
        durationInFrames={Math.round(FPS * DURATION_SECONDS)}
        fps={FPS}
        width={2560}
        height={1440}
        defaultProps={pachelbelProps}
      />
    </>
  );
};
