import { Config } from "@remotion/cli/config";

// 영상 화질 패키지 (2026-06-22 · 보기 대령 행진곡부터 적용 · forward-only).
// 그라디언트 밴딩을 줄이기 위한 인코딩 측 레버 3종:
//  - 중간 프레임 jpeg → png: 프레임마다 JPEG 손실(블록/밴딩)이 한 번 더 얹히던 걸 제거 (무손실).
//  - crf 16: 기본(18)보다 비트를 더 줘 평평한 배경에서 압축 밴딩을 줄임 (구 발행본 ~730kbps → 상향).
//  - audio 320k 명시: 음악 채널 안전장치 (구 발행본 실측 ~317k라 사실상 동일, 못 박기).
// temporal grain 디더는 소스 측(VisualizerComposition GrainOverlay)에서 담당.
Config.setVideoImageFormat("png");
Config.setCrf(10); // 기본(18/16)보다 낮춰 평평한 배경에 비트를 더 배분 (8bit 유지 = 범용 재생 호환)
Config.setAudioBitrate("320k");
Config.setOverwriteOutput(true);
Config.setConcurrency(6);
