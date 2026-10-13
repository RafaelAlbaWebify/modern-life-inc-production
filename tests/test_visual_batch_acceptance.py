"""Regression: a file on disk must not silently approve a visual asset."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_batch_preparation_does_not_auto_approve_existing_final_file(tmp_path: Path) -> None:
    episode = tmp_path / "episode"
    episode.mkdir()
    final = episode / "media" / "generated" / "S014.png"
    final.parent.mkdir(parents=True)
    final.write_bytes(b"not-reviewed")
    log = {
        "episode_id": "test",
        "workflow": {"rejected_directory": "media/generated/_rejected"},
        "assets": {
            "S014": {
                "mode": "HYBRID",
                "section": "Sign 2",
                "status": "missing",
                "final_file": "media/generated/S014.png",
                "attempts": 0,
            }
        },
    }
    prompts = {
        "style_contract": "test",
        "assets": [{"id": "S014", "prompt": "Two people share direct eye contact"}],
    }
    (episode / "asset_review_log.json").write_text(json.dumps(log), encoding="utf-8")
    (episode / "visual_asset_prompts.json").write_text(json.dumps(prompts), encoding="utf-8")
    script = Path(__file__).resolve().parents[1] / "tools" / "prepare_visual_batch.py"
    run = subprocess.run(
        [sys.executable, str(script), "--episode", str(episode), "--size", "1"],
        capture_output=True,
        text=True,
        check=True,
    )
    updated = json.loads((episode / "asset_review_log.json").read_text(encoding="utf-8"))
    assert updated["assets"]["S014"]["status"] == "queued"
    assert "[QUEUE] S014" in run.stdout
    assert final.read_bytes() == b"not-reviewed"
