from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path

from openai import OpenAI

try:
    from PIL import Image
except ImportError:
    Image = None


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_16x9(path: Path, width: int = 1920, height: int = 1080) -> None:
    if Image is None:
        print(f"[WARN] Pillow not installed; keeping native dimensions for {path.name}")
        return

    with Image.open(path) as im:
        im = im.convert("RGB")
        sw, sh = im.size
        target_ratio = width / height
        source_ratio = sw / sh

        if source_ratio > target_ratio:
            crop_w = int(sh * target_ratio)
            left = (sw - crop_w) // 2
            box = (left, 0, left + crop_w, sh)
        else:
            crop_h = int(sw / target_ratio)
            top = (sh - crop_h) // 2
            box = (0, top, sw, top + crop_h)

        im = im.crop(box).resize((width, height), Image.Resampling.LANCZOS)
        im.save(path, format="PNG", optimize=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", required=True)
    ap.add_argument("--batch", required=True)
    ap.add_argument("--model", default=os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-2"))
    ap.add_argument("--size", default=os.getenv("OPENAI_IMAGE_SIZE", "1536x1024"))
    ap.add_argument("--quality", default=os.getenv("OPENAI_IMAGE_QUALITY", "high"))
    args = ap.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        print("[FAIL] OPENAI_API_KEY is not set.")
        return 2

    episode = Path(args.episode).resolve()
    batch = load_json(Path(args.batch).resolve())
    review_log_path = episode / "asset_review_log.json"
    review_log = load_json(review_log_path)

    client = OpenAI()
    assets = batch.get("assets", [])
    failures = 0

    print(f"[START] {batch.get('batch_id')} assets={len(assets)} model={args.model}")

    for i, asset in enumerate(assets, 1):
        sid = asset["id"]
        relative_candidate = Path(asset["candidate_file"])
        out_path = episode / relative_candidate
        out_path.parent.mkdir(parents=True, exist_ok=True)

        if out_path.exists():
            print(f"[SKIP] {sid} already exists -> {out_path}")
            continue

        prompt = asset["prompt"].strip() + (
            " Generate exactly one standalone photographic frame for this scene. "
            "Do not create a collage, storyboard, contact sheet, split grid, title card, caption, label, "
            "symbol, icon, question mark, speech bubble, arrow, UI element, or baked text. "
            "Any explanatory graphics described in the brief will be added later by the compositor. "
            "Keep essential subjects inside a generous central safe area for a centered 16:9 crop."
        )

        print(f"[GEN {i}/{len(assets)}] {sid}")
        try:
            result = client.images.generate(
                model=args.model,
                prompt=prompt,
                size=args.size,
                quality=args.quality,
                n=1,
            )
            item = result.data[0]
            if not getattr(item, "b64_json", None):
                raise RuntimeError("No base64 image payload returned.")

            out_path.write_bytes(base64.b64decode(item.b64_json))
            normalize_16x9(out_path)

            row = review_log["assets"][sid]
            row["status"] = "generated"
            row["generated_candidate"] = str(relative_candidate).replace("\\", "/")
            row["notes"] = ""
            print(f"[PASS] {sid} -> {out_path}")

        except Exception as exc:
            failures += 1
            row = review_log["assets"][sid]
            row["status"] = "retry"
            row["notes"] = f"Generation failed: {exc}"
            print(f"[FAIL] {sid}: {exc}", file=sys.stderr)

        review_log_path.write_text(
            json.dumps(review_log, indent=2) + "\n",
            encoding="utf-8",
        )
        time.sleep(0.5)

    print(f"[DONE] generated={len(assets)-failures} failed={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
