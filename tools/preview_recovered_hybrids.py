"""Build QA stills for recovered candidates without promoting unapproved assets."""

from __future__ import annotations
import json
import importlib
from pathlib import Path
import sys
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
render_episode = importlib.import_module("renderer.render_episode")
EPISODE = ROOT / "episodes" / "MLI-001"
STAGING = EPISODE / "media" / "generated" / "_review" / "recovered"
OUTPUT = EPISODE / "output" / "hybrid_review"
CANDIDATES = {
    "S002": "MLI-001_S002_candidate_03.png",
    "S004": "MLI-001_S004_candidate_01.png",
    "S010": "MLI-001_S010_candidate_02.png",
}


def main() -> None:
    manifest = json.loads((EPISODE / "production_manifest.json").read_text(encoding="utf-8"))
    scenes = {scene["id"]: scene for scene in manifest["scenes"]}
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for sid, filename in CANDIDATES.items():
        matches = list(STAGING.rglob(filename))
        if len(matches) != 1:
            found = [str(p.relative_to(STAGING)) for p in STAGING.rglob("*.png")]
            raise FileNotFoundError(
                f"Expected exactly one {filename} under {STAGING}; found {len(matches)}. "
                f"PNG inventory: {found}"
            )
        source = matches[0]
        with Image.open(source) as image:
            image.verify()
        scene = {**scenes[sid], "base_image": source.name}
        render_episode.render_scene(
            scene, source.parent, OUTPUT / f"{sid}_hybrid_preview.png", False
        )
        print(f"[PASS] {sid} composite -> {OUTPUT / (sid + '_hybrid_preview.png')}")
    print("[INFO] Preview only: no files promoted, no QA status modified.")


if __name__ == "__main__":
    main()
