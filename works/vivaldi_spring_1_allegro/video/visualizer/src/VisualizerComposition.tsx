import {
  AbsoluteFill,
  Audio,
  Img,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  delayRender,
  continueRender,
} from "remotion";
import { useAudioData, visualizeAudio } from "@remotion/media-utils";
import { useEffect, useState } from "react";

const FRAME_WIDTH = 1920;
const FRAME_HEIGHT = 1080;

const COVER_SIZE = 720;
const COVER_LEFT = (FRAME_WIDTH - COVER_SIZE) / 2;
const COVER_RIGHT = COVER_LEFT + COVER_SIZE;
const COVER_TOP = (FRAME_HEIGHT - COVER_SIZE) / 2;

const FADE_IN_FRAMES = 90;

const NUMBER_OF_SAMPLES = 64;
const BAR_COUNT_PER_SIDE = 32;
const LEFT_LETTERBOX_WIDTH = COVER_LEFT;
const RIGHT_LETTERBOX_WIDTH = FRAME_WIDTH - COVER_RIGHT;

const BAR_WIDTH = 3;
const BAR_MIN_HEIGHT = 4;
const BAR_MAX_AMPLITUDE_HEIGHT = 400;
const BAR_CENTER_Y = FRAME_HEIGHT / 2;
const BAR_OPACITY = 0.6;

const AMPLIFICATION_LOW = 1.0;
const AMPLIFICATION_HIGH = 6.0;
const AMPLIFICATION_CURVE = 1.4;

const HEIGHT_SCALE_EXPONENT = 0.5;

const TEXT_COLOR = "#e8e0c8";
const TEXT_SHADOW = "0 2px 12px rgba(0, 0, 0, 0.75)";
const WORDMARK_TEAL = "rgb(40, 180, 175)";  // banner *M* color · 시리즈 brand color (s320 v3)
const WORDMARK_RIGHT = 81;                   // 좌측 title margin axis mirror
const WORDMARK_BOTTOM = 90;                  // 좌측 title margin axis mirror
const WORDMARK_FONT_SIZE = 40;               // 시그너처 §3 v3 default · 좌측 piece_title 56 의 ~70%

const hexToRgba = (hex: string, alpha: number): string => {
  const cleaned = hex.replace("#", "");
  const r = parseInt(cleaned.slice(0, 2), 16);
  const g = parseInt(cleaned.slice(2, 4), 16);
  const b = parseInt(cleaned.slice(4, 6), 16);
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
};

const computeAmplification = (globalIndex: number, totalBars: number) => {
  const t = globalIndex / Math.max(totalBars - 1, 1);
  return (
    AMPLIFICATION_LOW +
    Math.pow(t, AMPLIFICATION_CURVE) * (AMPLIFICATION_HIGH - AMPLIFICATION_LOW)
  );
};

const LEFT_BAR_GAP =
  (LEFT_LETTERBOX_WIDTH - BAR_COUNT_PER_SIDE * BAR_WIDTH) /
  (BAR_COUNT_PER_SIDE + 1);
const RIGHT_BAR_GAP =
  (RIGHT_LETTERBOX_WIDTH - BAR_COUNT_PER_SIDE * BAR_WIDTH) /
  (BAR_COUNT_PER_SIDE + 1);

type BarSide = "left" | "right";

interface BarProps {
  amplitude: number;
  side: BarSide;
  index: number;
  globalIndex: number;
  totalBars: number;
  color: string;
}

const Bar: React.FC<BarProps> = ({
  amplitude,
  side,
  index,
  globalIndex,
  totalBars,
  color,
}) => {
  const amplification = computeAmplification(globalIndex, totalBars);
  const amplified = Math.min(Math.max(0, amplitude) * amplification, 1);
  const scaled = Math.pow(amplified, HEIGHT_SCALE_EXPONENT);
  const height = BAR_MIN_HEIGHT + scaled * BAR_MAX_AMPLITUDE_HEIGHT;
  const gap = side === "left" ? LEFT_BAR_GAP : RIGHT_BAR_GAP;
  const offsetFromEdge = gap + index * (BAR_WIDTH + gap);
  const left =
    side === "left" ? offsetFromEdge : COVER_RIGHT + offsetFromEdge;

  return (
    <div
      style={{
        position: "absolute",
        left,
        top: BAR_CENTER_Y - height / 2,
        width: BAR_WIDTH,
        height,
        backgroundColor: color,
        borderRadius: BAR_WIDTH / 2,
      }}
    />
  );
};

export interface VisualizerProps {
  letterboxColors: [string, string, string];
  composerName: string;
  pieceTitle: string;
  pieceSubtitle: string;
  audioPath: string;
  coverPath: string;
}

export const VisualizerComposition: React.FC<VisualizerProps> = ({
  letterboxColors,
  composerName,
  pieceTitle,
  pieceSubtitle,
  audioPath,
  coverPath,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const audioSrc = staticFile(audioPath);
  const audioData = useAudioData(audioSrc);

  const [fontLoaded, setFontLoaded] = useState(false);
  const [handle] = useState(() => delayRender("Loading GFS Didot font"));

  useEffect(() => {
    const fontUrl = staticFile("fonts/GFSDidot-Regular.ttf");
    const fontFace = new FontFace("GFSDidotLocal", `url(${fontUrl})`);
    fontFace
      .load()
      .then((loaded) => {
        document.fonts.add(loaded);
        setFontLoaded(true);
        continueRender(handle);
      })
      .catch((err) => {
        console.error("Font load failed:", err);
        continueRender(handle);
      });
  }, [handle]);

  if (!audioData) {
    return null;
  }

  const visualization = visualizeAudio({
    fps,
    frame,
    audioData,
    numberOfSamples: NUMBER_OF_SAMPLES,
  });

  const leftBarAmplitudes = visualization.slice(0, BAR_COUNT_PER_SIDE);
  const rightBarAmplitudes = visualization.slice(
    BAR_COUNT_PER_SIDE,
    BAR_COUNT_PER_SIDE * 2
  );

  const fadeOpacity = interpolate(frame, [0, FADE_IN_FRAMES], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const letterboxGradient = `linear-gradient(180deg, ${letterboxColors[0]} 0%, ${letterboxColors[1]} 50%, ${letterboxColors[2]} 100%)`;
  const barColor = hexToRgba(letterboxColors[2], BAR_OPACITY);

  return (
    <AbsoluteFill style={{ background: letterboxGradient, opacity: fadeOpacity }}>
      <Audio src={audioSrc} />

      {leftBarAmplitudes.map((amp, i) => (
        <Bar
          key={`left-${i}`}
          amplitude={amp}
          side="left"
          index={i}
          globalIndex={i}
          totalBars={NUMBER_OF_SAMPLES}
          color={barColor}
        />
      ))}
      {rightBarAmplitudes.map((amp, i) => (
        <Bar
          key={`right-${i}`}
          amplitude={amp}
          side="right"
          index={i}
          globalIndex={BAR_COUNT_PER_SIDE + i}
          totalBars={NUMBER_OF_SAMPLES}
          color={barColor}
        />
      ))}

      <div
        style={{
          position: "absolute",
          left: COVER_LEFT,
          top: COVER_TOP,
          width: COVER_SIZE,
          height: COVER_SIZE,
        }}
      >
        <Img
          src={staticFile(coverPath)}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
          }}
        />
      </div>

      {fontLoaded && (
        <div
          style={{
            position: "absolute",
            left: 80,
            bottom: 60,
            color: TEXT_COLOR,
            fontFamily: "GFSDidotLocal, serif",
            lineHeight: 1.3,
            textShadow: TEXT_SHADOW,
            letterSpacing: "0.02em",
          }}
        >
          <div style={{ fontSize: 32, opacity: 0.85 }}>{composerName}</div>
          <div style={{ fontSize: 56, marginTop: 4, fontWeight: 400 }}>
            {pieceTitle}
          </div>
          {pieceSubtitle && (
            <div style={{ fontSize: 26, opacity: 0.7, marginTop: 6, fontStyle: "italic" }}>
              {pieceSubtitle}
            </div>
          )}
        </div>
      )}

      {fontLoaded && (
        <div
          style={{
            position: "absolute",
            right: WORDMARK_RIGHT,
            bottom: WORDMARK_BOTTOM,
            color: TEXT_COLOR,
            fontFamily: "GFSDidotLocal, serif",
            fontSize: WORDMARK_FONT_SIZE,
            fontWeight: 400,
            lineHeight: 1.3,
            textShadow: TEXT_SHADOW,
            letterSpacing: "0.02em",
            whiteSpace: "nowrap",
          }}
        >
          <span>Atelier </span>
          <span style={{ color: WORDMARK_TEAL }}>M</span>
          <span>iku Acappella</span>
        </div>
      )}
    </AbsoluteFill>
  );
};
