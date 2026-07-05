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

// s381 PROTOTYPE — Miku-matched band remap (60Hz–6kHz, log-spaced).
// Pull a fine LINEAR FFT, then re-bucket into 64 log-spaced display bars.
const FFT_SAMPLES = 2048; // sampleSize 4096 -> ~10.8 Hz/bin
const BAR_COUNT_PER_SIDE = 32;
const TOTAL_BARS = BAR_COUNT_PER_SIDE * 2;
const BAND_LOW_HZ = 60; // ~B1/C2, just below catalog lowest note F#2 (92 Hz)
const BAND_SPLIT_HZ = 1000; // L=fundamentals 60–1k, R=harmonics/sibilance 1k–6k (~energy median)
const BAND_HIGH_HZ = 6000;
const SPECTRUM_GAIN = 2.0; // chopin LOCK (코튼 결단: 3.0 → 2.0 · restrained minimal per album aesthetic)
// s381b temporal smoothing: fast attack + gradual release (decaying-max over recent
// frames) so bars FADE OUT smoothly instead of popping on/off ("없다 있다" 어색 제거).
const SMOOTH_RELEASE_FRAMES = 8; // ~0.27s release tail @30fps
const SMOOTH_DECAY = 0.82; // per-frame release factor (0.82^8 ≈ 0.20)
const LEFT_LETTERBOX_WIDTH = COVER_LEFT;
const RIGHT_LETTERBOX_WIDTH = FRAME_WIDTH - COVER_RIGHT;

const BAR_WIDTH = 3;
const BAR_MIN_HEIGHT = 8; // s381b: gentle resting baseline (bars never fully vanish)
const BAR_MAX_AMPLITUDE_HEIGHT = 400;
const BAR_CENTER_Y = FRAME_HEIGHT / 2;
const BAR_OPACITY = 0.6;

const AMPLIFICATION_LOW = 1.0;
const AMPLIFICATION_HIGH = 3.5; // spectral tilt: lift highs to visual parity (counters low-skew)
const AMPLIFICATION_CURVE = 1.0;

const HEIGHT_SCALE_EXPONENT = 0.5;

const TEXT_COLOR = "#e8e0c8";
const TEXT_SHADOW = "0 2px 12px rgba(0, 0, 0, 0.75)";
// Thin solid outline on all on-screen text (코튼 2026-06-17). paintOrder draws
// the stroke behind the fill so glyph faces stay full while a crisp edge defines
// them against any letterbox tone. Applied to every text block (inherited by
// webkit-text-stroke). Forward-only: already-published works are not re-rendered.
const TEXT_STROKE_WIDTH = "0.8px"; // 코튼 LOCK 2026-06-17
const TEXT_STROKE_COLOR = "rgba(0, 0, 0, 0.5)";
const TEXT_OUTLINE: React.CSSProperties = {
  WebkitTextStrokeWidth: TEXT_STROKE_WIDTH,
  WebkitTextStrokeColor: TEXT_STROKE_COLOR,
  paintOrder: "stroke fill",
};
const WORDMARK_TEAL = "rgb(40, 180, 175)";
const WORDMARK_RIGHT = 81;
const WORDMARK_BOTTOM = 90;
const WORDMARK_FONT_SIZE = 40;

const CHAPTER_LABEL_LEFT = 80;
const CHAPTER_LABEL_TOP = 320;
const CHAPTER_LABEL_FONT_SIZE = 56;
const CHAPTER_LABEL_OPACITY_MAX = 0.75;
const CHAPTER_LABEL_FADE_FRAMES = 12;

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

// CC cue (s-current): "captions available" prompt for vocal/lyric songs only.
// Gated by hasCaptions prop (default false) — instrumental→vocalise works never
// set it, so existing 6 works are untouched (forward-only). Placed bottom-right,
// right-aligned, directly above the "Atelier Miku Acappella" wordmark (코튼 2026-06-17).
const CC_CUE_RIGHT = WORDMARK_RIGHT; // align right edge with the wordmark
const CC_CUE_BOTTOM = WORDMARK_BOTTOM + 66; // sits just above the wordmark line
const CC_CUE_FONT_SIZE = 26;

// Temporal grain dither (2026-06-22 · 보기 대령 행진곡부터).
// 프레임마다 노이즈 seed를 바꿔 시간적으로 평균(temporal dithering)되게 하여, 8bit
// 그라디언트 배경의 밴딩(층)을 풀어준다. 배경 그라디언트 위·콘텐츠 아래에 깔려 배경에만
// 작용하고, 영상 재생 시 grain 자체는 매 프레임 달라져 눈에는 거의 보이지 않는다.
// 강도(GRAIN_OPACITY)·결(baseFrequency)은 gate 렌더로 튜닝.
// 기본값 — props로 곡별 오버라이드 가능 (grainOpacity / grainBaseFrequency / grainOctaves / grainBlendMode).
// 주력 밴딩 제거는 사전 디더링 배경(muse background · IGN 디더 PNG)이 담당하고, 이 temporal
// grain은 인코딩(유튜브 재양자화) 손실분을 시간적으로 메우는 약한 보조 레이어다. 그래서 강도를
// 낮게(0.05) 둔다. 배경 PNG가 없는 구 work는 CSS 그라디언트 폴백 — 이땐 grain이 유일 디더원.
const GRAIN_OPACITY = 0.05;
const GRAIN_BASE_FREQUENCY = 0.7; // 약간 낮춰 인코딩 생존↑ + 저주파 밴딩 경계에 더 효과
const GRAIN_OCTAVES = 3;
const GRAIN_BLEND: React.CSSProperties["mixBlendMode"] = "soft-light";
const GrainOverlay: React.FC<{
  opacity: number;
  baseFrequency: number;
  octaves: number;
  blendMode: React.CSSProperties["mixBlendMode"];
}> = ({ opacity, baseFrequency, octaves, blendMode }) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill
      style={{
        pointerEvents: "none",
        mixBlendMode: blendMode,
        opacity,
      }}
    >
      <svg
        width="100%"
        height="100%"
        style={{ width: "100%", height: "100%" }}
        preserveAspectRatio="none"
      >
        <filter id="muse-grain" x="0%" y="0%" width="100%" height="100%">
          <feTurbulence
            type="fractalNoise"
            baseFrequency={baseFrequency}
            numOctaves={octaves}
            seed={frame}
            stitchTiles="stitch"
          />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width="100%" height="100%" filter="url(#muse-grain)" />
      </svg>
    </AbsoluteFill>
  );
};

export type VisualizerProps = {
  letterboxColors: [string, string, string];
  composerName: string;
  pieceTitle: string;
  pieceSubtitle: string;
  audioPath: string;
  coverPath: string;
  variationStarts: number[];
  variationLabels: string[];
  hasCaptions?: boolean;
  grainOpacity?: number;
  grainBaseFrequency?: number;
  grainOctaves?: number;
  grainBlendMode?: string;
  backgroundPath?: string;
} & Record<string, unknown>;

export const VisualizerComposition: React.FC<VisualizerProps> = ({
  letterboxColors,
  composerName,
  pieceTitle,
  pieceSubtitle,
  audioPath,
  coverPath,
  variationStarts,
  variationLabels,
  hasCaptions = false,
  grainOpacity = GRAIN_OPACITY,
  grainBaseFrequency = GRAIN_BASE_FREQUENCY,
  grainOctaves = GRAIN_OCTAVES,
  grainBlendMode = GRAIN_BLEND,
  backgroundPath,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
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

  // Re-bucket a linear FFT into log-spaced display bars over [fLo, fHi] (no gain yet).
  const binHz = audioData.sampleRate / (FFT_SAMPLES * 2);
  const rebucket = (
    spec: number[],
    fLo: number,
    fHi: number,
    n: number
  ): number[] => {
    const out: number[] = [];
    for (let k = 0; k < n; k++) {
      const f0 = fLo * Math.pow(fHi / fLo, k / n);
      const f1 = fLo * Math.pow(fHi / fLo, (k + 1) / n);
      const iLo = Math.max(0, Math.floor(f0 / binHz));
      const iHi = Math.min(spec.length - 1, Math.ceil(f1 / binHz));
      let v = 0;
      for (let i = iLo; i <= iHi; i++) v = Math.max(v, spec[i]);
      // linear interp at band center for sub-bin-width (low) bars
      const c = (f0 + f1) / 2 / binHz;
      const ci = Math.floor(c);
      if (ci + 1 < spec.length) {
        const frac = c - ci;
        v = Math.max(v, spec[ci] * (1 - frac) + spec[ci + 1] * frac);
      }
      out.push(v);
    }
    return out;
  };

  const specAt = (f: number) =>
    visualizeAudio({
      fps,
      frame: Math.max(0, f),
      audioData,
      numberOfSamples: FFT_SAMPLES,
    });

  // Fast attack (current frame) + gradual release (decaying-max over recent frames).
  const mkBars = (fLo: number, fHi: number, n: number): number[] => {
    const cur = rebucket(specAt(frame), fLo, fHi, n);
    for (let b = 1; b <= SMOOTH_RELEASE_FRAMES; b++) {
      if (frame - b < 0) break;
      const past = rebucket(specAt(frame - b), fLo, fHi, n);
      const decay = Math.pow(SMOOTH_DECAY, b);
      for (let i = 0; i < n; i++) cur[i] = Math.max(cur[i], past[i] * decay);
    }
    return cur.map((v) => Math.min(1, v * SPECTRUM_GAIN));
  };

  const leftBarAmplitudes = mkBars(BAND_LOW_HZ, BAND_SPLIT_HZ, BAR_COUNT_PER_SIDE);
  const rightBarAmplitudes = mkBars(BAND_SPLIT_HZ, BAND_HIGH_HZ, BAR_COUNT_PER_SIDE);

  const fadeOpacity = interpolate(frame, [0, FADE_IN_FRAMES], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // CC cue (only when hasCaptions): a steady, always-on badge so viewers at any
  // point — including mid-roll/late arrivals — see captions exist. No blink/pulse
  // (코튼 2026-06-17). It rides the global FADE_IN with the rest of the frame.
  const CC_STEADY_OPACITY = 0.92; // near wordmark strength (코튼: Lyrics 시인성 ↑)
  const ccCueOpacity = CC_STEADY_OPACITY;

  const letterboxGradient = `linear-gradient(180deg, ${letterboxColors[0]} 0%, ${letterboxColors[1]} 50%, ${letterboxColors[2]} 100%)`;
  const barColor = hexToRgba(letterboxColors[2], BAR_OPACITY);

  let currentVarIdx = 0;
  for (let i = variationStarts.length - 1; i >= 0; i--) {
    if (frame >= variationStarts[i] * fps) {
      currentVarIdx = i;
      break;
    }
  }
  const currentVarStartFrame = variationStarts[currentVarIdx] * fps;
  const nextVarStartFrame =
    currentVarIdx + 1 < variationStarts.length
      ? variationStarts[currentVarIdx + 1] * fps
      : durationInFrames;
  const framesSinceStart = frame - currentVarStartFrame;
  const framesUntilNext = nextVarStartFrame - frame;
  const labelFadeInOpacity = interpolate(
    framesSinceStart,
    [0, CHAPTER_LABEL_FADE_FRAMES],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );
  const labelFadeOutOpacity = interpolate(
    framesUntilNext,
    [0, CHAPTER_LABEL_FADE_FRAMES],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );
  const chapterLabelOpacity =
    Math.min(labelFadeInOpacity, labelFadeOutOpacity) *
    CHAPTER_LABEL_OPACITY_MAX;
  const currentChapterLabel = variationLabels[currentVarIdx];

  return (
    <AbsoluteFill
      style={{
        opacity: fadeOpacity,
        // 사전 디더링 배경 PNG가 있으면 그것을, 없으면 CSS 그라디언트로 폴백.
        background: backgroundPath ? undefined : letterboxGradient,
      }}
    >
      {backgroundPath && (
        <Img
          src={staticFile(backgroundPath)}
          style={{ position: "absolute", inset: 0, width: "100%", height: "100%" }}
        />
      )}
      <Audio src={audioSrc} />
      <GrainOverlay
        opacity={grainOpacity}
        baseFrequency={grainBaseFrequency}
        octaves={grainOctaves}
        blendMode={grainBlendMode as React.CSSProperties["mixBlendMode"]}
      />

      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: FRAME_WIDTH,
          height: FRAME_HEIGHT,
          transform: "scale(1.3333333333333333)",
          transformOrigin: "top left",
        }}
      >
      {leftBarAmplitudes.map((amp, i) => (
        <Bar
          key={`left-${i}`}
          amplitude={amp}
          side="left"
          index={i}
          globalIndex={i}
          totalBars={TOTAL_BARS}
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
          totalBars={TOTAL_BARS}
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
            left: CHAPTER_LABEL_LEFT,
            top: CHAPTER_LABEL_TOP,
            color: TEXT_COLOR,
            fontFamily: "GFSDidotLocal, serif",
            fontSize: CHAPTER_LABEL_FONT_SIZE,
            fontWeight: 400,
            lineHeight: 1.3,
            textShadow: TEXT_SHADOW,
            letterSpacing: "0.02em",
            opacity: chapterLabelOpacity,
            ...TEXT_OUTLINE,
          }}
        >
          {currentChapterLabel}
        </div>
      )}

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
            maxWidth: LEFT_LETTERBOX_WIDTH - 100,
            ...TEXT_OUTLINE,
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

      {fontLoaded && hasCaptions && (
        <div
          style={{
            position: "absolute",
            right: CC_CUE_RIGHT,
            bottom: CC_CUE_BOTTOM,
            display: "flex",
            alignItems: "center",
            justifyContent: "flex-end",
            gap: 10,
            opacity: ccCueOpacity,
          }}
        >
          <div
            style={{
              fontFamily: "GFSDidotLocal, serif",
              fontSize: CC_CUE_FONT_SIZE - 4,
              fontWeight: 400,
              color: "#ECECEC",
              background: "#141414",
              borderRadius: 5,
              padding: "1px 9px",
              letterSpacing: "0.10em",
              lineHeight: 1.35,
            }}
          >
            CC
          </div>
          <div
            style={{
              color: TEXT_COLOR,
              fontFamily: "GFSDidotLocal, serif",
              fontSize: CC_CUE_FONT_SIZE + 2,
              fontWeight: 400,
              lineHeight: 1.3,
              textShadow: TEXT_SHADOW,
              letterSpacing: "0.02em",
              whiteSpace: "nowrap",
              ...TEXT_OUTLINE,
            }}
          >
            <span style={{ color: WORDMARK_TEAL }}>▸</span> Lyrics
          </div>
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
            ...TEXT_OUTLINE,
          }}
        >
          <span>Atelier </span>
          <span style={{ color: WORDMARK_TEAL }}>M</span>
          <span>iku Acappella</span>
        </div>
      )}
      </div>
    </AbsoluteFill>
  );
};
