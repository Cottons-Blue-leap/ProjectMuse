#!/usr/bin/env python3
"""Audio-production utilities for Project Muse.

The commands here are deliberately conservative: inspect stems, then optionally
make a light proof master by level-matching dry stems and summing them. No EQ,
compression, limiting, or reverb is applied.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
import wave

# Windows cp949 한글 깨짐 방어 (s355 광역 audit)
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


DEFAULT_FIRST_PROOF_STEMS = ["lead_miku_ah.wav", "mid_oo.wav", "low_oo.wav"]


def linear_to_db(value: float) -> float | None:
    if value <= 0:
        return None
    return round(20 * math.log10(value), 2)


def db_to_linear(value: float) -> float:
    return 10 ** (value / 20.0)


def iter_pcm_samples(raw: bytes, width: int):
    if width == 1:
        for byte in raw:
            yield byte - 128
    elif width == 2:
        for index in range(0, len(raw), 2):
            yield int.from_bytes(raw[index : index + 2], "little", signed=True)
    elif width == 3:
        for index in range(0, len(raw), 3):
            chunk = raw[index : index + 3]
            if len(chunk) < 3:
                break
            sign = b"\xff" if chunk[2] & 0x80 else b"\x00"
            yield int.from_bytes(chunk + sign, "little", signed=True)
    elif width == 4:
        for index in range(0, len(raw), 4):
            yield int.from_bytes(raw[index : index + 4], "little", signed=True)
    else:
        raise ValueError(f"Unsupported sample width: {width}")


def sample_to_float(value: int, width: int) -> float:
    if width == 1:
        return max(-1.0, min(1.0, value / 128.0))
    return max(-1.0, min(1.0, value / float(2 ** (width * 8 - 1))))


def float_to_pcm(value: float, width: int) -> bytes:
    clipped = max(-1.0, min(1.0, value))
    if width == 1:
        integer = int(round(clipped * 127.0 + 128.0))
        return bytes([max(0, min(255, integer))])

    max_positive = 2 ** (width * 8 - 1) - 1
    min_negative = -(2 ** (width * 8 - 1))
    integer = int(round(clipped * max_positive))
    integer = max(min_negative, min(max_positive, integer))
    if width == 3:
        return int(integer).to_bytes(4, "little", signed=True)[:3]
    return int(integer).to_bytes(width, "little", signed=True)


def read_wav(path: Path) -> tuple[dict, list[float]]:
    with wave.open(str(path), "rb") as handle:
        channels = handle.getnchannels()
        sample_width = handle.getsampwidth()
        sample_rate = handle.getframerate()
        frames = handle.getnframes()
        raw = handle.readframes(frames)

    if sample_width not in (1, 2, 3, 4):
        raise ValueError(f"Unsupported sample width: {sample_width}")

    samples = [sample_to_float(value, sample_width) for value in iter_pcm_samples(raw, sample_width)]
    info = wav_info_from_samples(path, samples, channels, sample_width, sample_rate, frames)
    return info, samples


def inspect_wav(path: Path) -> dict:
    info, _samples = read_wav(path)
    return info


def wav_info_from_samples(
    path: Path,
    samples: list[float],
    channels: int,
    sample_width: int,
    sample_rate: int,
    frames: int,
) -> dict:
    peak = 0.0
    square_sum = 0.0
    for sample in samples:
        abs_sample = abs(sample)
        peak = max(peak, abs_sample)
        square_sum += sample * sample
    rms = math.sqrt(square_sum / len(samples)) if samples else 0.0
    return {
        "file": path.name,
        "channels": channels,
        "sample_rate": sample_rate,
        "bit_depth": sample_width * 8,
        "duration_seconds": round(frames / sample_rate, 3) if sample_rate else 0,
        "peak_dbfs": linear_to_db(peak),
        "rms_dbfs": linear_to_db(rms),
    }


def write_wav(path: Path, samples: list[float], sample_rate: int, channels: int, bit_depth: int) -> None:
    if bit_depth not in (16, 24, 32):
        raise ValueError("Output bit depth must be 16, 24, or 32.")
    width = bit_depth // 8
    if len(samples) % channels != 0:
        raise ValueError("Sample count is not divisible by channel count.")

    path.parent.mkdir(parents=True, exist_ok=True)
    raw = bytearray()
    for sample in samples:
        raw.extend(float_to_pcm(sample, width))

    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(channels)
        handle.setsampwidth(width)
        handle.setframerate(sample_rate)
        handle.writeframes(bytes(raw))


def parse_expected(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def list_wavs(stem_dir: Path, include: list[str] | None = None) -> list[Path]:
    if include:
        return [stem_dir / name for name in include]
    return sorted(stem_dir.glob("*.wav"))


def build_stem_report(stem_dir: Path, expected: list[str] | None = None) -> dict:
    expected = expected or []
    report = {
        "stem_dir": str(stem_dir),
        "stems": [],
        "warnings": [],
    }

    wavs = sorted(stem_dir.glob("*.wav"))
    if not wavs:
        report["warnings"].append("No WAV files found.")

    for stem_name in expected:
        if not (stem_dir / stem_name).exists():
            report["warnings"].append(f"Expected stem missing: {stem_name}")

    sample_rates = set()
    channels = set()
    bit_depths = set()
    durations = []

    for wav_path in wavs:
        try:
            info = inspect_wav(wav_path)
            report["stems"].append(info)
            sample_rates.add(info["sample_rate"])
            channels.add(info["channels"])
            bit_depths.add(info["bit_depth"])
            durations.append(info["duration_seconds"])
            if info["peak_dbfs"] is not None and info["peak_dbfs"] > -0.1:
                report["warnings"].append(f"{wav_path.name} peaks near clipping: {info['peak_dbfs']} dBFS")
        except Exception as exc:  # noqa: BLE001
            report["warnings"].append(f"Could not inspect {wav_path.name}: {exc}")

    if len(sample_rates) > 1:
        report["warnings"].append(f"Mixed sample rates found: {sorted(sample_rates)}")
    if len(channels) > 1:
        report["warnings"].append(f"Mixed channel counts found: {sorted(channels)}")
    if len(bit_depths) > 1:
        report["warnings"].append(f"Mixed bit depths found: {sorted(bit_depths)}")
    if durations and max(durations) - min(durations) > 0.25:
        report["warnings"].append("Stem durations differ by more than 250 ms. Check same-start rendering.")

    return report


def check_stems(args: argparse.Namespace) -> int:
    expected = parse_expected(args.expected)
    report = build_stem_report(Path(args.stems), expected=expected)
    write_json(Path(args.out), report)
    print(f"Wrote stem report: {args.out}")
    if report["warnings"]:
        print("Warnings:")
        for warning in report["warnings"]:
            print(f"- {warning}")
    if args.strict and report["warnings"]:
        return 1
    return 0


def assert_compatible(infos: list[dict]) -> tuple[int, int, int]:
    if not infos:
        raise ValueError("No WAV stems were loaded.")
    sample_rates = {item["sample_rate"] for item in infos}
    channels = {item["channels"] for item in infos}
    bit_depths = {item["bit_depth"] for item in infos}
    if len(sample_rates) > 1:
        raise ValueError(f"Mixed sample rates found: {sorted(sample_rates)}")
    if len(channels) > 1:
        raise ValueError(f"Mixed channel counts found: {sorted(channels)}")
    if len(bit_depths) > 1:
        raise ValueError(f"Mixed bit depths found: {sorted(bit_depths)}")
    durations = [item["duration_seconds"] for item in infos]
    if max(durations) - min(durations) > 0.25:
        raise ValueError("Stem durations differ by more than 250 ms. Check same-start rendering.")
    return (int(next(iter(sample_rates))), int(next(iter(channels))), int(next(iter(bit_depths))))


def peak(samples: list[float]) -> float:
    return max((abs(sample) for sample in samples), default=0.0)


def pad_to(samples: list[float], length: int) -> list[float]:
    if len(samples) >= length:
        return samples
    return samples + [0.0] * (length - len(samples))


def assemble_proof(args: argparse.Namespace) -> int:
    stem_dir = Path(args.stems)
    include = parse_expected(args.include)
    wavs = list_wavs(stem_dir, include=include)
    missing = [path.name for path in wavs if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing included stems: " + ", ".join(missing))

    infos = []
    stem_samples = []
    for wav_path in wavs:
        info, samples = read_wav(wav_path)
        infos.append(info)
        stem_samples.append((wav_path.name, samples))

    sample_rate, channels, input_bit_depth = assert_compatible(infos)
    max_len = max(len(samples) for _name, samples in stem_samples)
    target_stem_peak = db_to_linear(float(args.target_stem_peak_dbfs))
    target_mix_peak = db_to_linear(float(args.target_mix_peak_dbfs))

    mix = [0.0] * max_len
    stem_gains = []
    for name, samples in stem_samples:
        current_peak = peak(samples)
        gain = target_stem_peak / current_peak if current_peak > 0 else 0.0
        stem_gains.append({"file": name, "gain_db": linear_to_db(gain) if gain > 0 else None})
        for index, sample in enumerate(pad_to(samples, max_len)):
            mix[index] += sample * gain

    mix_peak = peak(mix)
    mix_gain = target_mix_peak / mix_peak if mix_peak > target_mix_peak and mix_peak > 0 else 1.0
    if mix_gain != 1.0:
        mix = [sample * mix_gain for sample in mix]

    output_bit_depth = int(args.bit_depth or input_bit_depth)
    write_wav(Path(args.out), mix, sample_rate=sample_rate, channels=channels, bit_depth=output_bit_depth)

    output_info = inspect_wav(Path(args.out))
    report = {
        "source_stem_dir": str(stem_dir),
        "included_stems": [path.name for path in wavs],
        "target_stem_peak_dbfs": float(args.target_stem_peak_dbfs),
        "target_mix_peak_dbfs": float(args.target_mix_peak_dbfs),
        "stem_gains": stem_gains,
        "mix_gain_db": linear_to_db(mix_gain) if mix_gain > 0 else None,
        "output": output_info,
        "notes": [
            "Dry level-match proof only.",
            "No EQ, compression, limiting, or reverb was applied.",
        ],
    }
    if args.report:
        write_json(Path(args.report), report)

    print(f"Wrote proof master: {args.out}")
    if args.report:
        print(f"Wrote assembly report: {args.report}")
    print(f"Output peak: {output_info['peak_dbfs']} dBFS")
    return 0


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Project Muse audio production utilities")
    sub = parser.add_subparsers(dest="command", required=True)

    stems = sub.add_parser("check-stems", help="Inspect rendered WAV stems")
    stems.add_argument("--stems", required=True)
    stems.add_argument("--out", required=True)
    stems.add_argument(
        "--expected",
        default="",
        help="Comma-separated expected WAV filenames. Example: lead_miku_ah.wav,mid_oo.wav,low_oo.wav",
    )
    stems.add_argument("--strict", action="store_true", help="Exit non-zero when warnings are found")
    stems.set_defaults(func=check_stems)

    proof = sub.add_parser("assemble-proof", help="Level-match and sum compatible dry WAV stems")
    proof.add_argument("--stems", required=True)
    proof.add_argument("--out", required=True)
    proof.add_argument(
        "--include",
        default="",
        help="Comma-separated WAV filenames to include. Defaults to all WAV files in --stems.",
    )
    proof.add_argument("--report", default="", help="Optional JSON report path")
    proof.add_argument("--target-stem-peak-dbfs", type=float, default=-3.0)
    proof.add_argument("--target-mix-peak-dbfs", type=float, default=-1.0)
    proof.add_argument("--bit-depth", type=int, choices=(16, 24, 32), default=24)
    proof.set_defaults(func=assemble_proof)

    return parser


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    # blend-gate / calibrate-baseline live in the heavier blend_gate.py
    # (ffmpeg + numpy + scipy). Imported lazily so this module stays stdlib-only.
    if argv and argv[0] in ("blend-gate", "calibrate-baseline"):
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import blend_gate
        sub = "gate" if argv[0] == "blend-gate" else "calibrate"
        return blend_gate.main([sub, *argv[1:]])
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
