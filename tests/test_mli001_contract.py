"""Executable acceptance contracts for the MLI-001 production manifest."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EPISODE = ROOT / "episodes" / "MLI-001"


def test_manifest_scene_count_and_classification() -> None:
    manifest = json.loads((EPISODE / "production_manifest.json").read_text(encoding="utf-8"))
    plan = json.loads((EPISODE / "visual_plan.json").read_text(encoding="utf-8"))
    scenes = manifest["scenes"]
    assert len(scenes) == 56
    assert len({scene["id"] for scene in scenes}) == 56
    assert sum(scene["visual_mode"] == "HERO" for scene in scenes) == 10
    assert sum(scene["visual_mode"] == "HYBRID" for scene in scenes) == 22
    assert sum(scene["visual_mode"] == "SYSTEM" for scene in scenes) == 24
    for scene in scenes:
        assert scene["visual_mode"] == plan["modes"][scene["id"]]
        assert ("base_image" in scene) == (scene["visual_mode"] != "SYSTEM")


def test_manifest_duration_matches_locked_narration() -> None:
    manifest = json.loads((EPISODE / "production_manifest.json").read_text(encoding="utf-8"))
    actual = sum(float(scene["duration_sec"]) for scene in manifest["scenes"])
    assert abs(actual - 447.948) < 0.02


def test_approved_assets_recorded_as_explicit_files() -> None:
    log = json.loads((EPISODE / "asset_review_log.json").read_text(encoding="utf-8"))
    expected = {"S001", "S007", "S017", "S023", "S027", "S032", "S037", "S054"}
    locked = {sid for sid, asset in log["assets"].items() if asset["status"] == "locked"}
    assert locked == expected
    for sid in expected:
        assert log["assets"][sid]["final_file"] == f"media/generated/{sid}.png"
