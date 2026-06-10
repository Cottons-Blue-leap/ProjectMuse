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

// ──────────────────────────────────────────────────────────────────────────
// MuseShort — 9:16 Shorts composition (H2 cold-open format · 첫 파이프라인).
//
// 본편 엔진(VisualizerComposition = canonical ccf27a)은 건드리지 않는 별도
// 컴포지션. 스펙트럼은 본편과 동일한 s381 band-remap(60Hz–6kHz log · gain 2.0 ·
// temporal smoothing)을 단일 가로 행으로 변형해 쓴다 — 시리즈 시각 언어 유지.
//
// H2 구조: 0초 음악 시작(콜드오픈) → revealSec에 텍스트 반전 → endCardSec에
// 엔드 카드. 모션은 페이드만 (제안서 §6 모션 규칙 정합).
//
// 세이프존(1080×1920): 상단 240 / 하단 480 / 우측 200 회피.
// 타이포 = 시리즈 불변 토큰 (GFS Didot · cream #e8e0c8 · teal 강조) —
// 제안서 §6의 신규 토큰(#F2EFE6/#5DCAA5) 대신 시리즈 정합 우선.
// ──────────────────────────────────────────────────────────────────────────

const W = 1080;
const H = 1920;

const COVER_SIZE = 720;
const COVER_LEFT = (W - COVER_SIZE) / 2;
const COVER_TOP = 280;

const COVER_FADE_FRAMES = 18; // 0.6s — 콜드오픈이라 본편(3s)보다 빠르게

// s381 band-remap (본편과 동일 파라미터 · 단일 행 48 bars)
const FFT_SAMPLES = 2048;
const BAR_COUNT = 48;
const BAND_LOW_HZ = 60;
const BAND_HIGH_HZ = 6000;
const SPECTRUM_GAIN = 2.0;
const SMOOTH_RELEASE_FRAMES = 8;
const SMOOTH_DECAY = 0.82;
const AMPLIFICATION_LOW = 1.0;
const AMPLIFICATION_HIGH = 3.5;
const HEIGHT_SCALE_EXPONENT = 0.5;

const BAR_REGION_LEFT = 90;
const BAR_REGION_RIGHT = 870; // 우측 액션 레일(x≥880) 회피
const BAR_WIDTH = 6;
const BAR_MIN_HEIGHT = 6;
const BAR_MAX_AMPLITUDE_HEIGHT = 150;
const BAR_CENTER_Y = 1105; // 커버 하단(1000)과 텍스트(1220) 사이
const BAR_OPACITY = 0.6;

const TEXT_COLOR = "#e8e0c8";
const TEXT_SHADOW = "0 2px 12px rgba(0, 0, 0, 0.75)";
const ACCENT_TEAL = "rgb(40, 180, 175)";

const TEXT_FADE_FRAMES = 18; // 0.6s 페이드 단일 모션
const REVEAL_BLOCK_TOP = 1220;
const REVEAL_1_FONT = 46;
const REVEAL_2_FONT = 54; // 한 줄 유지 (1080 - 좌우 60 안에서 nowrap)

const END_SCRIM = "rgba(8, 12, 16, 0.72)";
const END_FADE_FRAMES = 24; // 0.8s

const hexToRgba = (hex: string, alpha: number): string => {
  const cleaned = hex.replace("#", "");
  const r = parseInt(cleaned.slice(0, 2), 16);
  const g = parseInt(cleaned.slice(2, 4), 16);
  const b = parseInt(cleaned.slice(4, 6), 16);
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
};

export type ShortsProps = {
  letterboxColors: [string, string, string];
  audioPath: string;
  coverPath: string;
  revealLine1: string;
  revealLine2: string;
  revealAccent: string; // revealLine2 안에서 teal 강조할 부분 문자열
  reveal1Sec: number;
  reveal2Sec: number;
  endCardSec: number;
  endCredit: string;
  endCta: string;
  durationSeconds: number;
} & Record<string, unknown>;

export const ShortsComposition: React.FC<ShortsProps> = ({
  letterboxColors,
  audioPath,
  coverPath,
  revealLine1,
  revealLine2,
  revealAccent,
  reveal1Sec,
  reveal2Sec,
  endCardSec,
  endCredit,
  endCta,
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

  const binHz = audioData.sampleRate / (FFT_SAMPLES * 2);
  const rebucket = (spec: number[], fLo: number, fHi: number, n: number): number[] => {
    const out: number[] = [];
    for (let k = 0; k < n; k++) {
      const f0 = fLo * Math.pow(fHi / fLo, k / n);
      const f1 = fLo * Math.pow(fHi / fLo, (k + 1) / n);
      const iLo = Math.max(0, Math.floor(f0 / binHz));
      const iHi = Math.min(spec.length - 1, Math.ceil(f1 / binHz));
      let v = 0;
      for (let i = iLo; i <= iHi; i++) v = Math.max(v, spec[i]);
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

  const mkBars = (): number[] => {
    const cur = rebucket(specAt(frame), BAND_LOW_HZ, BAND_HIGH_HZ, BAR_COUNT);
    for (let b = 1; b <= SMOOTH_RELEASE_FRAMES; b++) {
      if (frame - b < 0) break;
      const past = rebucket(specAt(frame - b), BAND_LOW_HZ, BAND_HIGH_HZ, BAR_COUNT);
      const decay = Math.pow(SMOOTH_DECAY, b);
      for (let i = 0; i < BAR_COUNT; i++) cur[i] = Math.max(cur[i], past[i] * decay);
    }
    return cur.map((v) => Math.min(1, v * SPECTRUM_GAIN));
  };

  const bars = mkBars();
  const barGap = (BAR_REGION_RIGHT - BAR_REGION_LEFT - BAR_COUNT * BAR_WIDTH) / (BAR_COUNT + 1);
  const barColor = hexToRgba(letterboxColors[2], BAR_OPACITY);

  const coverOpacity = interpolate(frame, [0, COVER_FADE_FRAMES], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const fadeFrom = (startSec: number) =>
    interpolate(frame, [startSec * fps, startSec * fps + TEXT_FADE_FRAMES], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });

  const reveal1Opacity = fadeFrom(reveal1Sec);
  const reveal2Opacity = fadeFrom(reveal2Sec);
  const endOpacity = interpolate(
    frame,
    [endCardSec * fps, endCardSec * fps + END_FADE_FRAMES],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  const accentIdx = revealAccent ? revealLine2.indexOf(revealAccent) : -1;
  const line2Before = accentIdx >= 0 ? revealLine2.slice(0, accentIdx) : revealLine2;
  const line2Accent = accentIdx >= 0 ? revealAccent : "";
  const line2After = accentIdx >= 0 ? revealLine2.slice(accentIdx + revealAccent.length) : "";

  const letterboxGradient = `linear-gradient(180deg, ${letterboxColors[0]} 0%, ${letterboxColors[1]} 50%, ${letterboxColors[2]} 100%)`;

  return (
    <AbsoluteFill style={{ background: letterboxGradient }}>
      <Audio src={audioSrc} />

      {bars.map((amp, i) => {
        const t = i / Math.max(BAR_COUNT - 1, 1);
        const amplification = AMPLIFICATION_LOW + t * (AMPLIFICATION_HIGH - AMPLIFICATION_LOW);
        const amplified = Math.min(Math.max(0, amp) * amplification, 1);
        const scaled = Math.pow(amplified, HEIGHT_SCALE_EXPONENT);
        const height = BAR_MIN_HEIGHT + scaled * BAR_MAX_AMPLITUDE_HEIGHT;
        const left = BAR_REGION_LEFT + barGap + i * (BAR_WIDTH + barGap);
        return (
          <div
            key={`bar-${i}`}
            style={{
              position: "absolute",
              left,
              top: BAR_CENTER_Y - height / 2,
              width: BAR_WIDTH,
              height,
              backgroundColor: barColor,
              borderRadius: BAR_WIDTH / 2,
              opacity: coverOpacity,
            }}
          />
        );
      })}

      <div
        style={{
          position: "absolute",
          left: COVER_LEFT,
          top: COVER_TOP,
          width: COVER_SIZE,
          height: COVER_SIZE,
          opacity: coverOpacity,
        }}
      >
        <Img
          src={staticFile(coverPath)}
          style={{ width: "100%", height: "100%", objectFit: "cover" }}
        />
      </div>

      {fontLoaded && (
        <div
          style={{
            position: "absolute",
            left: 60,
            right: 60, // 커버와 같은 중심축 — 한 줄 폭이 우측 레일(x≥880) 안 닿음
            top: REVEAL_BLOCK_TOP,
            textAlign: "center",
            color: TEXT_COLOR,
            fontFamily: "GFSDidotLocal, serif",
            textShadow: TEXT_SHADOW,
            letterSpacing: "0.02em",
            lineHeight: 1.35,
            opacity: 1 - endOpacity, // 엔드 카드 진입 시 함께 사라짐
          }}
        >
          <div style={{ fontSize: REVEAL_1_FONT, opacity: reveal1Opacity * 0.9 }}>
            {revealLine1}
          </div>
          <div
            style={{
              fontSize: REVEAL_2_FONT,
              marginTop: 14,
              opacity: reveal2Opacity,
              whiteSpace: "nowrap",
            }}
          >
            <span>{line2Before}</span>
            {line2Accent && <span style={{ color: ACCENT_TEAL }}>{line2Accent}</span>}
            <span>{line2After}</span>
          </div>
        </div>
      )}

      {fontLoaded && endOpacity > 0 && (
        <AbsoluteFill style={{ background: END_SCRIM, opacity: endOpacity }}>
          <div
            style={{
              position: "absolute",
              left: 60,
              right: 60,
              top: 800,
              textAlign: "center",
              color: TEXT_COLOR,
              fontFamily: "GFSDidotLocal, serif",
              textShadow: TEXT_SHADOW,
              letterSpacing: "0.02em",
              lineHeight: 1.4,
            }}
          >
            <div style={{ fontSize: 44, opacity: 0.85 }}>{endCredit}</div>
            <div style={{ fontSize: 58, marginTop: 28 }}>{endCta}</div>
            <div style={{ fontSize: 38, marginTop: 90, whiteSpace: "nowrap" }}>
              <span>Atelier </span>
              <span style={{ color: ACCENT_TEAL }}>M</span>
              <span>iku Acappella</span>
            </div>
          </div>
        </AbsoluteFill>
      )}
    </AbsoluteFill>
  );
};
