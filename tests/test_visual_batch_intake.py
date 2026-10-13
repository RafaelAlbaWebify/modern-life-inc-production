"""End-to-end local intake contract: previews exist, but photos are never auto-approved."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from PIL import Image


def test_import_staged_four_scene_batch(tmp_path: Path) -> None:
    episode = tmp_path / "MLI-001"
    episode.mkdir()
    staging = tmp_path / "incoming"
    staging.mkdir()
    ids = ("S014", "S018", "S019", "S022")
    records = {}
    scenes = []
    for sid in ids:
        Image.new("RGB", (640, 360), (96, 80, 60)).save(staging / f"MLI-001_{sid}.png")
        records[sid] = {
            "status": "missing",
            "final_file": f"media/generated/{sid}.png",
            "mode": "HYBRID",
            "section": "test",
        }
        scenes.append(
            {
                "id": sid,
                "visual_mode": "HYBRID",
                "base_image": f"media/generated/{sid}.png",
                "layout": "interaction",
                "on_screen_text": "",
            }
        )
    log = {"episode_id": "MLI-001", "assets": records}
    (episode / "asset_review_log.json").write_text(json.dumps(log), encoding="utf-8")
    (episode / "production_manifest.json").write_text(
        json.dumps({"scenes": scenes}), encoding="utf-8"
    )
    script = Path(__file__).resolve().parents[1] / "tools" / "prepare_visual_batch.py"
    subprocess.run(
        [sys.executable, str(script), "--episode", str(episode), "--import-dir", str(staging)],
        check=True,
        capture_output=True,
        text=True,
    )
    updated = json.loads((episode / "asset_review_log.json").read_text(encoding="utf-8"))
    for sid in ids:
        assert updated["assets"][sid]["status"] == "generated"
        assert not (episode / "media" / "generated" / f"{sid}.png").exists()
        assert (
            episode / "media" / "generated" / "_review" / "import_001" / f"{sid}_candidate.png"
        ).is_file()
        assert (
            episode / "output" / "visual_review" / "import_001" / f"{sid}_preview.png"
        ).is_file()
