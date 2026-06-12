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
// MikuDiscovery — "창작자 발견 delight" 쇼츠 rig (s421 락 포맷).
//
// 연출: 미쿠 N체가 일렬(악보 마디에 정렬)로 서고, 아래 악보를 재생. 플레이헤드가
// 각 미쿠의 진입 마디를 지나면 그 미쿠가 대기→노래로 깨어남(+글로우+♪). 캐논 =
// "같은 선율 2마디 간격 돌림노래"를 눈으로 전달.
//
// 설계 원칙 = 로직 vs 스킨 분리. 디자인 면(미쿠 PNG·색·간격·카피·타이밍·악보)은
// 전부 props로 빠진다. 2차창작 미쿠 나오면 public PNG만 교체하면 끝 (본편 B
// 비주얼라이저 props.json+public 주입 양식 동일). 본편 엔진 불가침.
// ──────────────────────────────────────────────────────────────────────────

export type StageVoice = {
  entryBar: number;     // 진입 마디 (1-indexed)
  waitPath: string;     // public 상대경로 (대기 상태 PNG)
  singPath: string;     // public 상대경로 (노래 상태 PNG)
};

export type CanonStageProps = {
  audioPath: string;
  // 음악↔시각 매핑
  bpm: number;
  beatsPerBar: number;
  scoreStartSec: number; // bar 1 다운비트가 오디오에서 시작하는 시각
  barsVisible: number;   // 화면 악보에 보이는 마디 수
  voices: StageVoice[];
  // 스킨
  bgStops: [string, string];
  tealActive: string;
  tealDim: string;
  cream: string;
  title: string;
  subtitle: string;
  gapLabel: string;       // 미쿠 사이 간격 라벨 (예: "2 bars")
  footText: string;
  mikuWidth: number;      // 미쿠 렌더 폭(px)
  scoreImagePath?: string; // 있으면 인라인 스태프 대신 실제 악보 이미지 사용
  scoreScroll?: boolean;   // true = 악보가 흐름(고정 플레이헤드) · false = 정지 악보+sweep 플레이헤드
  barsTotal?: number;      // 스크롤 스태프 총 마디 (가시 구간보다 길게)
  playheadFrac?: number;   // 고정 플레이헤드 위치 (악보 폭 0~1 · 기본 0.30)
  entryFromRight?: boolean; // true = 첫 성부=우측 미쿠, 캐스케이드 우→좌 (스크롤 방향 정합)
  durationSeconds: number;
} & Record<string, unknown>;

const W = 1080;
const H = 1920;
const SCORE_L = 90;
const SCORE_R = 990;
const STAGE_BASELINE = 1060; // 미쿠 발 y
const SCORE_TOP = 1180;
const SCORE_H = 280;

export const CanonStageComposition: React.FC<CanonStageProps> = ({
  audioPath,
  bpm,
  beatsPerBar,
  scoreStartSec,
  barsVisible,
  voices,
  bgStops,
  tealActive,
  tealDim,
  cream,
  title,
  subtitle,
  gapLabel,
  footText,
  mikuWidth,
  scoreImagePath,
  scoreScroll = false,
  barsTotal = 14,
  playheadFrac = 0.3,
  entryFromRight = true,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const sec = frame / fps;

  const [fontLoaded, setFontLoaded] = useState(false);
  const [handle] = useState(() => delayRender("font"));
  useEffect(() => {
    const f = new FontFace("GFSDidotLocal", `url(${staticFile("fonts/GFSDidot-Regular.ttf")})`);
    f.load().then((l) => { document.fonts.add(l); setFontLoaded(true); continueRender(handle); })
      .catch(() => continueRender(handle));
  }, [handle]);

  const secPerBeat = 60 / bpm;
  const secPerBar = secPerBeat * beatsPerBar;
  const barW = (SCORE_R - SCORE_L) / barsVisible;
  const W_CENTER = W / 2;

  const entryBars = voices.map((v) => v.entryBar);
  const minBar = Math.min(...entryBars);
  const maxBar = Math.max(...entryBars);
  const midBar = (minBar + maxBar) / 2;

  // 미쿠 무대 x: 그룹 중점 = 화면 중앙. 낮은 bar(첫 성부)가 우측(entryFromRight).
  const mikuX = (bar: number) =>
    entryFromRight ? W_CENTER + (midBar - bar) * barW : W_CENTER - (midBar - bar) * barW;
  const entrySec = (bar: number) => scoreStartSec + (bar - minBar) * secPerBar;
  const barFloat = (sec - scoreStartSec) / secPerBar;

  // downbeat 펄스 (활성 미쿠 글로우)
  const beatPhase = ((sec - scoreStartSec) / secPerBeat) % 1;
  const beatPulse = beatPhase >= 0 ? Math.max(0, 1 - beatPhase * 2.2) : 0;

  const bg = `linear-gradient(160deg, ${bgStops[0]} 0%, ${bgStops[1]} 100%)`;
  const didot = { fontFamily: "GFSDidotLocal, serif" } as const;

  const innerW = SCORE_R - SCORE_L;
  const staffW = barsTotal * barW;
  // 스크롤 앵커: 첫 성부(minBar) 음표가 scoreStartSec에 첫(우측) 미쿠 바로 아래 오고,
  // 좌로 흐르며 다음 미쿠들 아래를 차례로 지난다 = 각 미쿠가 *자기 아래 음표*와 동기.
  const xAnchor = mikuX(minBar);
  const notesLeft = (xAnchor - SCORE_L) - barFloat * barW; // notes 레이어 left (local0 = 첫 음표)
  const playX = Math.max(SCORE_L, Math.min(SCORE_R, SCORE_L + barFloat * barW)); // 정지 모드 sweep 폴백

  // 고정 5선 (스크롤 X — 무대처럼 깔린다)
  const renderStaffLines = (totalW: number) => {
    const lines = [];
    for (let i = 0; i < 5; i++) {
      const y = 60 + i * 26;
      lines.push(<line key={`l${i}`} x1={0} y1={y} x2={totalW} y2={y} stroke="#5c6470" strokeWidth={2} />);
    }
    return (
      <svg width={totalW} height={SCORE_H} viewBox={`0 0 ${totalW} ${SCORE_H}`}>
        {lines}
        <text x={6} y={120} fontSize={78} fill="#cfc9bb" fontFamily="serif">&#x1D11E;</text>
      </svg>
    );
  };

  // 흐르는 음표 + 마디선 레이어 (local0 = 첫 음표). bars 마디 · 폭 totalW.
  const renderNotes = (bars: number, totalW: number) => {
    const barLines = [];
    for (let b = 0; b <= bars; b++) {
      const x = b * barW;
      barLines.push(<line key={`b${b}`} x1={x} y1={60} x2={x} y2={164} stroke="#4a525c" strokeWidth={2} />);
    }
    const phrase = [3, 2, 1, 2, 3, 4, 3, 2]; // 마디당 2종 · 4음/마디
    const notesPerBar = 4;
    const notes = [];
    for (let n = 0; n < bars * notesPerBar; n++) {
      const p = phrase[n % phrase.length];
      const x = (n + 0.5) * (barW / notesPerBar);
      const y = 60 + (4 - p * 0.9) * 26 * 0.9 + 20;
      notes.push(
        <g key={`n${n}`}>
          <ellipse cx={x} cy={y} rx={11} ry={8} fill="#d8d2c4" transform={`rotate(-18 ${x} ${y})`} />
          <line x1={x + 10} y1={y} x2={x + 10} y2={y - 44} stroke="#d8d2c4" strokeWidth={2.5} />
        </g>
      );
    }
    return (
      <svg width={totalW} height={SCORE_H} viewBox={`0 0 ${totalW} ${SCORE_H}`}>
        {barLines}{notes}
      </svg>
    );
  };

  return (
    <AbsoluteFill style={{ background: bg }}>
      <Audio src={staticFile(audioPath)} />

      {/* 타이틀 */}
      {fontLoaded && (
        <div style={{ position: "absolute", top: 130, left: 0, right: 0, textAlign: "center", ...didot }}>
          <div style={{ fontSize: 84, color: cream, letterSpacing: "0.08em" }}>{title}</div>
          <div style={{ fontSize: 36, color: tealActive, letterSpacing: "0.18em", marginTop: 12 }}>{subtitle}</div>
        </div>
      )}

      {/* 미쿠 일렬 */}
      {voices.map((v, i) => {
        const eSec = entrySec(v.entryBar);
        const active = sec >= eSec;
        const cx = mikuX(v.entryBar);
        const fade = interpolate(sec, [eSec, eSec + 0.3], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
        // perk-up: 진입 순간 살짝 튀어오름
        const perk = interpolate(sec, [eSec, eSec + 0.18, eSec + 0.42], [1, 1.14, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
        const glow = active ? 0.35 + beatPulse * 0.5 : 0;
        const mH = mikuWidth * 1.75;
        return (
          <div key={`v${i}`} style={{ position: "absolute", left: cx, top: STAGE_BASELINE - mH, width: mikuWidth, height: mH, transform: `translateX(-50%) scale(${perk})`, transformOrigin: "50% 100%" }}>
            {/* ♪ note pop on entry */}
            {active && (
              <div style={{ position: "absolute", bottom: "100%", left: "55%", fontSize: 56, color: tealActive, opacity: fade, ...didot }}>&#9834;</div>
            )}
            {/* wait (dim) */}
            <Img src={staticFile(v.waitPath)} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "contain", opacity: (1 - fade) * 0.9 }} />
            {/* sing (active + glow) */}
            <Img src={staticFile(v.singPath)} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "contain", opacity: fade, filter: `drop-shadow(0 0 ${26 * glow}px ${tealActive})` }} />
          </div>
        );
      })}

      {/* 간격 라벨 (미쿠 사이) */}
      {fontLoaded && voices.slice(1).map((v, i) => {
        const xMid = (mikuX(voices[i].entryBar) + mikuX(v.entryBar)) / 2;
        return (
          <div key={`g${i}`} style={{ position: "absolute", left: xMid, top: STAGE_BASELINE - mikuWidth * 1.75 - 60, transform: "translateX(-50%)", fontSize: 30, color: tealActive, letterSpacing: "0.08em", whiteSpace: "nowrap", ...didot }}>
            {entryFromRight ? <>&#8612; {gapLabel}</> : <>{gapLabel} &#8614;</>}
          </div>
        );
      })}

      {/* 각 미쿠 ↔ 바로 아래 음표 동기 가이드 (미쿠 발 ~ 악보 하단) */}
      {voices.map((v, i) => {
        const x = mikuX(v.entryBar);
        const active = sec >= entrySec(v.entryBar);
        return (
          <div key={`gd${i}`} style={{ position: "absolute", left: x - 1.5, top: STAGE_BASELINE - 10, width: 3, height: SCORE_TOP + 150 - (STAGE_BASELINE - 10), background: active ? "rgba(60,200,190,0.45)" : "rgba(143,217,196,0.12)" }} />
        );
      })}

      {/* 악보 */}
      <div style={{ position: "absolute", left: SCORE_L, top: SCORE_TOP, width: innerW, height: SCORE_H, overflow: "hidden" }}>
        {/* 고정 5선 */}
        {!scoreImagePath && renderStaffLines(innerW)}
        {scoreScroll ? (
          // 흐르는 음표 (우→좌)
          <div style={{ position: "absolute", left: notesLeft, top: 0, width: staffW, height: SCORE_H }}>
            {scoreImagePath ? (
              <Img src={staticFile(scoreImagePath)} style={{ width: staffW, height: "100%", objectFit: "fill" }} />
            ) : (
              renderNotes(barsTotal, staffW)
            )}
          </div>
        ) : (
          scoreImagePath
            ? <Img src={staticFile(scoreImagePath)} style={{ width: "100%", height: "100%", objectFit: "contain" }} />
            : renderNotes(barsVisible, innerW)
        )}
        {/* 활성 미쿠 아래 음표 글로우 (지금 부르는 음) */}
        {voices.map((v, i) => {
          if (sec < entrySec(v.entryBar)) return null;
          const x = mikuX(v.entryBar) - SCORE_L;
          const g = 0.5 + beatPulse * 0.5;
          return <div key={`ng${i}`} style={{ position: "absolute", left: x - 16, top: 84, width: 32, height: 32, borderRadius: "50%", background: tealActive, opacity: 0.25 + g * 0.4, filter: `blur(2px)`, boxShadow: `0 0 ${18 * g}px ${tealActive}` }} />;
        })}
      </div>

      {/* 푸터 */}
      {fontLoaded && (
        <div style={{ position: "absolute", left: 60, right: 60, bottom: 320, textAlign: "center", fontSize: 54, color: cream, letterSpacing: "0.03em", ...didot }}>{footText}</div>
      )}
    </AbsoluteFill>
  );
};
