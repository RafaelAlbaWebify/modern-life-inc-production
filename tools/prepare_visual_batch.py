from __future__ import annotations

import argparse
import json
from pathlib import Path


PRIORITY = {"HERO": 0, "HYBRID": 1}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", required=True)
    ap.add_argument("--size", type=int, default=4)
    ap.add_argument("--mode", choices=["HERO", "HYBRID"])
    args = ap.parse_args()

    episode = Path(args.episode)
    prompts = load(episode / "visual_asset_prompts.json")
    log_path = episode / "asset_review_log.json"
    log = load(log_path)

    generated = episode / "media" / "generated"
    review = generated / "_review"
    rejected = generated / "_rejected"
    review.mkdir(parents=True, exist_ok=True)
    rejected.mkdir(parents=True, exist_ok=True)

    # Final files on disk always win: if present, mark approved unless already locked.
    for sid, row in log["assets"].items():
        final_path = episode / row["final_file"]
        if final_path.is_file() and row["status"] not in {"locked"}:
            row["status"] = "approved"

    candidates = []
    prompt_by_id = {row["id"]: row for row in prompts["assets"]}
    for sid, row in log["assets"].items():
        if row["status"] not in {"missing", "retry"}:
            continue
        if args.mode and row["mode"] != args.mode:
            continue
        candidates.append((sid, row))

    candidates.sort(key=lambda item: (PRIORITY.get(item[1]["mode"], 99), item[0]))
    selected = candidates[: args.size]

    existing_batches = sorted(review.glob("batch_*"))
    batch_num = 1
    if existing_batches:
        nums = []
        for p in existing_batches:
            try:
                nums.append(int(p.name.split("_")[-1]))
            except ValueError:
                pass
        if nums:
            batch_num = max(nums) + 1

    batch_dir = review / f"batch_{batch_num:03d}"
    batch_dir.mkdir(parents=True, exist_ok=True)

    batch_assets = []
    for sid, row in selected:
        p = prompt_by_id[sid]
        row["status"] = "queued"
        row["attempts"] = int(row.get("attempts", 0)) + 1
        candidate_name = f"{sid}_candidate_{row['attempts']:02d}.png"
        batch_assets.append({
            "id": sid,
            "mode": row["mode"],
            "section": row["section"],
            "candidate_file": str((batch_dir / candidate_name).relative_to(episode)).replace("\\", "/"),
            "final_file": row["final_file"],
            "prompt": p["prompt"],
        })

    batch_manifest = {
        "episode_id": log["episode_id"],
        "batch_id": f"batch_{batch_num:03d}",
        "style_contract": prompts["style_contract"],
        "assets": batch_assets,
    }
    (batch_dir / "batch_manifest.json").write_text(
        json.dumps(batch_manifest, indent=2) + "\n", encoding="utf-8"
    )
    log_path.write_text(json.dumps(log, indent=2) + "\n", encoding="utf-8")

    print(f"[BATCH] {batch_manifest['batch_id']} assets={len(batch_assets)}")
    for item in batch_assets:
        print(f"[QUEUE] {item['id']} {item['mode']} -> {item['candidate_file']}")
    print(f"[PASS] manifest -> {batch_dir / 'batch_manifest.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
