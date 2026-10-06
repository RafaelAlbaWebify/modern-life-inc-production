from __future__ import annotations

import argparse
import json
from pathlib import Path


def normalize_layout(raw: str) -> str:
    value = raw.lower().strip().replace(" ", "_")
    aliases = {
        "interaction": "two_person_conversation",
        "face_focus": "two_person_gaze",
        "split_interaction": "split_contrast",
        "conversation_progression": "two_person_conversation",
        "conversation_layout": "two_person_conversation",
        "visual_metaphor": "single_focus",
        "micro_gag": "single_focus",
        "pattern_build": "convergence",
        "heuristic_card": "three_item_heuristic",
        "text_card": "single_focus",
        "brand_outro": "brand_outro",
        "phone_scene": "phone_message",
        "timeline/progression": "timeline",
        "group_vs_one_person_contrast": "group_vs_one",
    }
    return aliases.get(value, value)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", required=True)
    args = ap.parse_args()

    episode = Path(args.episode)
    storyboard = json.loads((episode / "storyboard.json").read_text(encoding="utf-8"))
    visual_plan = json.loads((episode / "visual_plan.json").read_text(encoding="utf-8"))
    modes = visual_plan["modes"]

    scenes = []
    for item in storyboard:
        sid = item["id"]
        mode = modes.get(sid, "SYSTEM")
        scene = {
            "id": sid,
            "duration_sec": float(item["duration_sec"]),
            "visual_mode": mode,
            "layout": normalize_layout(item.get("layout", "single_focus")),
            "visual": item.get("visual", ""),
            "on_screen_text": item.get("on_screen_text", ""),
        }
        if mode in {"HYBRID", "HERO"}:
            scene["base_image"] = f"media/generated/{sid}.png"
        scenes.append(scene)

    manifest = {
        "version": "0.2",
        "episode_id": visual_plan.get("episode_id", episode.name),
        "width": 1920,
        "height": 1080,
        "fps": 30,
        "scenes": scenes,
    }
    out = episode / "production_manifest.json"
    out.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"[PASS] {len(scenes)} scenes -> {out}")


if __name__ == "__main__":
    main()
