from __future__ import annotations

import argparse
import json
import wave
from collections import defaultdict
from pathlib import Path


SECTION_MAP = {
    "hook": {"Hook", "Thesis", "Transition"},
    "sign-1": {"Sign 1"},
    "sign-2": {"Sign 2"},
    "sign-3": {"Sign 3"},
    "sign-4": {"Sign 4"},
    "sign-5": {"Sign 5"},
    "sign-6": {"Sign 6"},
    "sign-7": {"Sign 7"},
    "pattern": {"Synthesis", "Caveat"},
    "closing": {"Conclusion", "End"},
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def wav_seconds(path: Path) -> float:
    with wave.open(str(path), "rb") as wav:
        return wav.getnframes() / wav.getframerate()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", required=True)
    args = ap.parse_args()

    episode = Path(args.episode)
    storyboard_path = episode / "storyboard.json"
    chunks_path = episode / "narration_chunks.json"
    chunks_dir = episode / "media" / "narration_chunks"
    narration_path = episode / "media" / "narration.wav"
    config_path = episode.parents[1] / "config" / "voice_production.json"

    storyboard = load_json(storyboard_path)
    narration_manifest = load_json(chunks_path)
    config = load_json(config_path)

    chunk_pause = int(config["chunking"]["chunk_pause_ms"]) / 1000.0
    tempo = float(config["postprocess"]["tempo"])

    # Raw duration per narration section. Each stored chunk already contains any
    # explicit intra-chunk group pause. Add the configured pause only between chunks.
    raw_by_section: dict[str, float] = defaultdict(float)
    chunks = narration_manifest["chunks"]
    for index, chunk in enumerate(chunks):
        cid = str(chunk["id"])
        wav_path = chunks_dir / f"chunk-{cid}.wav"
        if not wav_path.is_file():
            raise FileNotFoundError(f"Missing narration chunk WAV: {wav_path}")
        raw_by_section[str(chunk["section"])] += wav_seconds(wav_path)
        if index < len(chunks) - 1:
            raw_by_section[str(chunk["section"])] += chunk_pause

    # Rubber Band tempo is applied once to the complete narration.
    final_by_section = {key: value / tempo for key, value in raw_by_section.items()}

    # Allocate each narration section across its storyboard scenes in proportion
    # to their authored storyboard durations, preserving editorial emphasis.
    grouped_scenes: dict[str, list[dict]] = {}
    for narration_section, storyboard_sections in SECTION_MAP.items():
        grouped_scenes[narration_section] = [
            scene for scene in storyboard if scene["section"] in storyboard_sections
        ]
        if not grouped_scenes[narration_section]:
            raise RuntimeError(f"No storyboard scenes mapped for {narration_section}")

    for narration_section, scenes in grouped_scenes.items():
        target = final_by_section.get(narration_section)
        if target is None:
            raise RuntimeError(f"No narration duration for section {narration_section}")
        old_total = sum(float(scene["duration_sec"]) for scene in scenes)
        for scene in scenes:
            weight = float(scene["duration_sec"]) / old_total
            scene["duration_sec"] = target * weight

    # Use the actual assembled narration as the final authority. Small rounding /
    # Rubber Band differences are corrected globally.
    computed_total = sum(float(scene["duration_sec"]) for scene in storyboard)
    if narration_path.is_file():
        narration_total = wav_seconds(narration_path)
        correction = narration_total / computed_total
        for scene in storyboard:
            scene["duration_sec"] *= correction
    else:
        narration_total = computed_total

    # Rebuild exact timeline and round only at serialization time.
    cursor = 0.0
    for index, scene in enumerate(storyboard):
        duration = float(scene["duration_sec"])
        if index == len(storyboard) - 1:
            duration = narration_total - cursor
        scene["start_sec"] = round(cursor, 3)
        scene["duration_sec"] = round(duration, 3)
        cursor += duration
        scene["end_sec"] = round(cursor, 3)

    storyboard_path.write_text(json.dumps(storyboard, indent=2) + "\n", encoding="utf-8")

    print(f"[PASS] retimed {len(storyboard)} scenes")
    print(f"[PASS] narration duration: {narration_total:.3f}s")
    print(f"[PASS] storyboard duration: {storyboard[-1]['end_sec']:.3f}s")
    for key in SECTION_MAP:
        total = sum(
            float(scene["duration_sec"])
            for scene in storyboard
            if scene["section"] in SECTION_MAP[key]
        )
        print(f"  {key:8s} {total:7.3f}s")


if __name__ == "__main__":
    main()
