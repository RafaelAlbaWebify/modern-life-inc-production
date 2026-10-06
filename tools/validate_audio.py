from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def probe(path: Path) -> dict:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration:stream=codec_type,codec_name,sample_rate,channels",
        "-of", "json", str(path),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio", required=True)
    ap.add_argument("--min-duration", type=float, default=300)
    ap.add_argument("--max-duration", type=float, default=720)
    args = ap.parse_args()

    path = Path(args.audio)
    if not path.exists():
        raise FileNotFoundError(path)

    data = probe(path)
    duration = float(data["format"]["duration"])
    audio_streams = [s for s in data.get("streams", []) if s.get("codec_type") == "audio"]

    if len(audio_streams) != 1:
        raise ValueError(f"Expected exactly one audio stream, got {len(audio_streams)}")
    if not (args.min_duration <= duration <= args.max_duration):
        raise ValueError(
            f"Narration duration {duration:.2f}s outside expected range "
            f"{args.min_duration:.0f}-{args.max_duration:.0f}s"
        )

    stream = audio_streams[0]
    print(f"[PASS] audio: {path}")
    print(f"[PASS] duration: {duration:.2f}s")
    print(f"[PASS] codec: {stream.get('codec_name')}")
    print(f"[PASS] sample_rate: {stream.get('sample_rate')}")
    print(f"[PASS] channels: {stream.get('channels')}")


if __name__ == "__main__":
    main()
