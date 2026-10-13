from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

from PIL import Image


PRIORITY = {"HERO": 0, "HYBRID": 1}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def import_staged_candidates(episode: Path, source: Path) -> int:
    """Import scene-labelled PNGs, build previews and keep editorial approval explicit."""
    import importlib
    import sys

    source = source.resolve()
    if not source.is_dir():
        raise ValueError(f"Candidate directory does not exist: {source}")
    log_path = episode / "asset_review_log.json"
    log = load(log_path)
    manifest = load(episode / "production_manifest.json")
    scenes = {scene["id"]: scene for scene in manifest["scenes"]}
    final = (episode / "media" / "generated").resolve()
    if source == final or source == episode.resolve():
        raise ValueError("Import from a staging directory, never from the final asset directory")
    discovered: dict[str, Path] = {}
    for png in sorted(source.rglob("*.png")):
        match = re.search(r"(?<![A-Za-z0-9])S\\d{3}(?!\\d)", png.stem, flags=re.I)
        if not match:
            continue
        sid = match.group(0).upper()
        if sid not in log["assets"] or sid not in scenes:
            raise ValueError(f"Unrecognized scene ID {sid}: {png}")
        if sid in discovered:
            raise ValueError(f"Multiple candidates for {sid}: {discovered[sid]} and {png}")
        if log["assets"][sid]["status"] in {"locked", "approved"}:
            raise ValueError(f"{sid} is already approved/locked; refusing to replace it")
        with Image.open(png) as image:
            image.verify()
        discovered[sid] = png
    if not discovered:
        raise ValueError(f"No scene-labelled PNG candidates found in {source}")

    review = final / "_review"
    n = 1
    while (review / f"import_{n:03d}").exists():
        n += 1
    batch_dir = review / f"import_{n:03d}"
    preview_dir = episode / "output" / "visual_review" / f"import_{n:03d}"
    batch_dir.mkdir(parents=True)
    preview_dir.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    render_episode = importlib.import_module("renderer.render_episode")
    for sid, original in discovered.items():
        dest = batch_dir / f"{sid}_candidate.png"
        shutil.copy2(original, dest)
        scene = {**scenes[sid], "base_image": dest.name}
        render_episode.render_scene(scene, batch_dir, preview_dir / f"{sid}_preview.png", False)
        row = log["assets"][sid]
        row["status"] = "generated"
        row["source_candidate"] = str(dest.relative_to(episode)).replace("\\\\", "/")
        row["notes"] = "Staged and composited for editorial review; not approved."
        print(f"[STAGED] {sid}: {dest.name} -> {preview_dir / (sid + '_preview.png')}")
    log_path.write_text(json.dumps(log, indent=2) + "\\n", encoding="utf-8")
    print(f"[REVIEW] {len(discovered)} candidate(s); no final files overwritten or approved.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", required=True)
    ap.add_argument("--size", type=int, default=4)
    ap.add_argument("--mode", choices=["HERO", "HYBRID"])
    ap.add_argument("--import-dir", type=Path, help="Import already generated candidate PNGs and preview them")
    args = ap.parse_args()

    episode = Path(args.episode).resolve()
    if args.import_dir is not None:
        return import_staged_candidates(episode, args.import_dir)
    prompts = load(episode / "visual_asset_prompts.json")
    log_path = episode / "asset_review_log.json"
    log = load(log_path)

    generated = episode / "media" / "generated"
    review = generated / "_review"
    rejected = generated / "_rejected"
    review.mkdir(parents=True, exist_ok=True)
    rejected.mkdir(parents=True, exist_ok=True)

    # Approval is an explicit editorial decision. File presence must never promote status.

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
        batch_assets.append(
            {
                "id": sid,
                "mode": row["mode"],
                "section": row["section"],
                "candidate_file": str((batch_dir / candidate_name).relative_to(episode)).replace(
                    "\\", "/"
                ),
                "final_file": row["final_file"],
                "prompt": p["prompt"],
            }
        )

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
