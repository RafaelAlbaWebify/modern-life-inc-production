from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", required=True)
    args = ap.parse_args()

    episode = Path(args.episode)
    prompt_manifest = json.loads((episode / "visual_asset_prompts.json").read_text(encoding="utf-8"))

    missing = []
    present = []
    for asset in prompt_manifest["assets"]:
        path = episode / asset["output"]
        row = {"id": asset["id"], "mode": asset["mode"], "path": str(path)}
        (present if path.is_file() else missing).append(row)

    print(f"[ASSETS] present={len(present)} missing={len(missing)} total={len(prompt_manifest['assets'])}")
    for row in missing:
        print(f"[MISSING] {row['id']} {row['mode']} -> {row['path']}")

    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
