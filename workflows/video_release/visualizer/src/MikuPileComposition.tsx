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
import { useEffect, useState } from "react";

// ──────────────────────────────────────────────────────────────────────────
// MikuPile — v3 어그로 범용 쇼츠 엔진 (s427).
//
// funnel §11.2 "어그로 템플릿 v3" 구현. 곡별 데이터(색·스프라이트·카피·N·타이밍)는
// 전부 props로 주입 = work-agnostic. 본편 VisualizerComposition(canonical ccf27a) ·
// ShortsComposition(A·폐기 잔존) · CanonStageComposition(교육형 변주)는 불가침 —
// MikuPile은 별도 신규 컴포지션이다.
//
// 연출: [솔로 잔잔] → buildStart에서 [미쿠 1→N 비트싱크 누적 + 노동력 카운터] →
// [N 떼창 화면 꽉 참] → 마지막=첫프레임 맞물려 무한 루프. 마지막 END_TAIL_SEC는 CTA.
//
// 설계 = workflows/shorts_first_proof/docs/v3_engine_design.md
// ──────────────────────────────────────────────────────────────────────────

export type MikuPileProps = {
  // 음악·오디오
  audioPath: string;
  bpm: number;
  beatsPerBar: number;
  buildStartSec: number; // 페이크 솔로 → 폭증 전환
  // 누적
  voiceCount: number; // N (= "미쿠 노동력 N명")
  spriteWait: string; // 대기(솔로 잔잔) PNG
  spriteSing: string; // 노래 PNG
  // 스킨 (곡별)
  gradient: [string, string, string]; // 본편 레터박스 3색
  // 텍스트 (회차 교체)
  episodeNo: number; // #N
  pieceLabel: string; // 부제 곡명
  hookCaption: string; // B층 훅 (코튼 요구 = 곡당 최소 1개 · 필수)
  cornerDetail: string; // 상시 작은 디테일
  endCta: string;
  durationSeconds: number;
} & Record<string, unknown>;

const W = 1080;
const H = 1920;

const CREAM = "#e8e0c8";
const TEAL = "rgb(40, 180, 175)";
const SHADOW = "0 2px 12px rgba(0,0,0,0.75)";

// 스프라이트 클러스터 밴드 (상단 타이틀/하단 캡션 회피)
const BAND_TOP = 560;
const BAND_BOTTOM = 1500;
const BAND_LEFT = 70;
const BAND_RIGHT = 1010;

const END_TAIL_SEC = 2; // 마지막 2s = CTA
const END_SCRIM = "rgba(8,12,16,0.72)";

const hexToRgba = (hex: string, a: number): string => {
  const c = hex.replace("#", "");
  return `rgba(${parseInt(c.slice(0, 2), 16)}, ${parseInt(c.slice(2, 4), 16)}, ${parseInt(c.slice(4, 6), 16)}, ${a})`;
};

export const MikuPileComposition: React.FC<MikuPileProps> = ({
  audioPath,
  bpm,
  beatsPerBar,
  buildStartSec,
  voiceCount,
  spriteWait,
  spriteSing,
  gradient,
  episodeNo,
  pieceLabel,
  hookCaption,
  cornerDetail,
  endCta,
  durationSeconds,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const sec = frame / fps;

  const [fontLoaded, setFontLoaded] = useState(false);
  const [handle] = useState(() => delayRender("font"));
  useEffect(() => {
    const f = new FontFace("GFSDidotLocal", `url(${staticFile("fonts/GFSDidot-Regular.ttf")})`);
    f.load()
      .then((l) => {
        document.fonts.add(l);
        setFontLoaded(true);
        continueRender(handle);
      })
      .catch(() => continueRender(handle));
  }, [handle]);

  const didot = { fontFamily: "GFSDidotLocal, serif" } as const;
  const secPerBeat = 60 / Math.max(bpm, 1);
  const secPerBar = secPerBeat * Math.max(beatsPerBar, 1);

  const N = Math.max(1, Math.round(voiceCount));

  // ── 누적 타이밍: solo(j=0)는 상시, j>=1은 buildStart부터 균등 진입
  const buildWindow = Math.max(2, durationSeconds * 0.55);
  const entryStep = N > 2 ? buildWindow / (N - 1) : secPerBar;
  const tOf = (j: number) => (j === 0 ? 0 : buildStartSec + (j - 1) * entryStep);

  // ── downbeat pulse (활성 미쿠 글로우)
  const beatPhase = (sec / secPerBeat) % 1;
  const beatPulse = Math.max(0, 1 - beatPhase * 2.2);

  // ── 중앙 정렬 그리드 + 중앙→바깥 reveal 순서
  const cols = Math.min(N, Math.max(1, Math.ceil(Math.sqrt(N * 1.5))));
  const rows = Math.ceil(N / cols);
  const cellW = (BAND_RIGHT - BAND_LEFT) / cols;
  const cellH = (BAND_BOTTOM - BAND_TOP) / rows;
  const cx0 = W / 2;
  const cy0 = (BAND_TOP + BAND_BOTTOM) / 2;

  // 전체 셀 중심 좌표 → 화면중앙 거리순 정렬 → 앞 N개 = reveal 순 슬롯
  const cells: { x: number; y: number; d: number }[] = [];
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const x = BAND_LEFT + (c + 0.5) * cellW;
      const y = BAND_TOP + (r + 0.5) * cellH;
      cells.push({ x, y, d: Math.hypot(x - cx0, y - cy0) });
    }
  }
  cells.sort((a, b) => a.d - b.d);
  const slots = cells.slice(0, N); // slots[j] = j번째 등장 미쿠 자리

  const boxW = Math.min(260, cellW * 0.92);
  const boxH = Math.min(cellH * 0.96, boxW * 1.7);

  const liveCount = slots.filter((_, j) => sec >= tOf(j)).length;
  const inEnd = sec >= durationSeconds - END_TAIL_SEC;

  const gradientBg = `linear-gradient(160deg, ${gradient[0]} 0%, ${gradient[1]} 52%, ${gradient[2]} 100%)`;

  // ── 텍스트 페이드 헬퍼
  const fadeIn = (start: number, dur = 0.5) =>
    interpolate(sec, [start, start + dur], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  const endOpacity = inEnd ? fadeIn(durationSeconds - END_TAIL_SEC, 0.6) : 0;
  // 훅 캡션 = 첫 0.3s 즉시 → buildStart 직후 사라짐(폭증에 자리 양보)
  const hookOpacity = interpolate(sec, [0.3, 0.6, buildStartSec + 0.4, buildStartSec + 1.0], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ background: gradientBg }}>
      <Audio src={staticFile(audioPath)} />

      {/* ── 미쿠 클러스터 (1→N 누적) ── */}
      {slots.map((slot, j) => {
        const t = tOf(j);
        if (sec < t) return null;
        const fade = interpolate(sec, [t, t + 0.28], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
        const perk = interpolate(sec, [t, t + 0.16, t + 0.4], [0.7, 1.12, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });
        // solo(j=0) 는 buildStart 전 잔잔(wait), 이후 노래(sing). 나머지는 등장 즉시 노래.
        const singing = j !== 0 || sec >= buildStartSec;
        const glow = singing ? 0.3 + beatPulse * 0.5 : 0.12;
        return (
          <div
            key={`m${j}`}
            style={{
              position: "absolute",
              left: slot.x,
              top: slot.y,
              width: boxW,
              height: boxH,
              transform: `translate(-50%, -50%) scale(${perk})`,
              opacity: fade,
            }}
          >
            <Img
              src={staticFile(singing ? spriteSing : spriteWait)}
              style={{
                width: "100%",
                height: "100%",
                objectFit: "contain",
                filter: `drop-shadow(0 0 ${24 * glow}px ${TEAL})`,
              }}
            />
          </div>
        );
      })}

      {/* ── 제목 밈 프레임 (상단) ── */}
      {fontLoaded && (
        <div style={{ position: "absolute", top: 120, left: 50, right: 50, textAlign: "center", ...didot }}>
          <div style={{ fontSize: 46, color: CREAM, textShadow: SHADOW, lineHeight: 1.25 }}>
            클래식을 미쿠에 싸서 드셔보세요 <span style={{ color: TEAL }}>#{episodeNo}</span>
          </div>
          <div style={{ fontSize: 34, color: CREAM, opacity: 0.78, textShadow: SHADOW, marginTop: 10 }}>
            {pieceLabel}
          </div>
        </div>
      )}

      {/* ── 노동력 카운터 (상시 · 라이브 증가) ── */}
      {fontLoaded && (
        <div
          style={{
            position: "absolute",
            top: 300,
            left: 0,
            right: 0,
            textAlign: "center",
            fontSize: 40,
            color: TEAL,
            letterSpacing: "0.04em",
            textShadow: SHADOW,
            ...didot,
          }}
        >
          미쿠 노동력 {liveCount}명
        </div>
      )}

      {/* ── B층 훅 캡션 (첫 0.5s 즉시 · 무음 스크롤 정지력) ── */}
      {fontLoaded && hookOpacity > 0.01 && (
        <div
          style={{
            position: "absolute",
            left: 60,
            right: 60,
            top: 1540,
            textAlign: "center",
            fontSize: 60,
            color: CREAM,
            textShadow: SHADOW,
            lineHeight: 1.3,
            opacity: hookOpacity,
            ...didot,
          }}
        >
          {hookCaption}
        </div>
      )}

      {/* ── 상시 구석 디테일 (눈썰미 · 깜빡 X) ── */}
      {fontLoaded && cornerDetail && (
        <div
          style={{
            position: "absolute",
            left: 64,
            bottom: 360,
            fontSize: 30,
            color: hexToRgba("#e8e0c8", 0.32),
            letterSpacing: "0.1em",
            ...didot,
          }}
        >
          {cornerDetail}
        </div>
      )}

      {/* ── 엔드 CTA (마지막 2s · 퍼널 다리) ── */}
      {fontLoaded && endOpacity > 0 && (
        <AbsoluteFill style={{ background: END_SCRIM, opacity: endOpacity }}>
          <div
            style={{
              position: "absolute",
              left: 60,
              right: 60,
              top: 820,
              textAlign: "center",
              color: CREAM,
              textShadow: SHADOW,
              ...didot,
            }}
          >
            <div style={{ fontSize: 58 }}>{endCta}</div>
            <div style={{ fontSize: 38, marginTop: 90, whiteSpace: "nowrap" }}>
              <span>Atelier </span>
              <span style={{ color: TEAL }}>M</span>
              <span>iku Acappella</span>
            </div>
          </div>
        </AbsoluteFill>
      )}
    </AbsoluteFill>
  );
};
