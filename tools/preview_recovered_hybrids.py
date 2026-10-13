"""Build QA stills for recovered candidates without promoting unapproved assets."""
from __future__ import annotations
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from PIL import Image
from renderer.render_episode import render_scene

ROOT = Path(__file__).resolve().parents[1]
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
        source = STAGING / filename
        if not source.is_file():
            raise FileNotFoundError(f"Download candidate ZIP into {STAGING}: {filename}")
        with Image.open(source) as image:
            image.verify()
        scene = {**scenes[sid], "base_image": filename}
        render_scene(scene, STAGING, OUTPUT / f"{sid}_hybrid_preview.png", False)
        print(f"[PASS] {sid} composite -> {OUTPUT / (sid + '_hybrid_preview.png')}")
    print("[INFO] Preview only: no files promoted, no QA status modified.")

if __name__ == "__main__":
    main()
