from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    Image = None

API_URL = "https://api.openai.com/v1/images/generations"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def post_json(url: str, payload: dict, api_key: str) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Image API HTTP {exc.code}: {detail}") from exc


def save_image_result(item: dict, out_path: Path) -> None:
    if item.get("b64_json"):
        out_path.write_bytes(base64.b64decode(item["b64_json"]))
        return
    if item.get("url"):
        with urllib.request.urlopen(item["url"], timeout=300) as resp:
            out_path.write_bytes(resp.read())
        return
    raise RuntimeError("Image API returned neither b64_json nor url.")


def normalize_16x9(path: Path, width: int = 1920, height: int = 1080) -> None:
    if Image is None:
        print(f"[WARN] Pillow not installed; keeping native image dimensions for {path.name}")
        return

    with Image.open(path) as im:
        im = im.convert("RGB")
        src_w, src_h = im.size
        target_ratio = width / height
        src_ratio = src_w / src_h

        if src_ratio > target_ratio:
            crop_w = int(src_h * target_ratio)
            left = (src_w - crop_w) // 2
            box = (left, 0, left + crop_w, src_h)
        else:
            crop_h = int(src_w / target_ratio)
            top = (src_h - crop_h) // 2
            box = (0, top, src_w, top + crop_h)

        im = im.crop(box).resize((width, height), Image.Resampling.LANCZOS)
        im.save(path, format="PNG", optimize=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", required=True)
    ap.add_argument("--batch", required=True, help="Path to batch_manifest.json")
    ap.add_argument("--model", default=os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-2"))
    ap.add_argument("--size", default=os.getenv("OPENAI_IMAGE_SIZE", "1536x1024"))
    ap.add_argument("--quality", default=os.getenv("OPENAI_IMAGE_QUALITY", "high"))
    ap.add_argument("--delay", type=float, default=0.5)
    args = ap.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("[FAIL] OPENAI_API_KEY is not set.")
        print("Set it for the current PowerShell session, then rerun this command.")
        return 2

    episode = Path(args.episode).resolve()
    batch_path = Path(args.batch).resolve()
    batch = load_json(batch_path)

    review_log_path = episode / "asset_review_log.json"
    review_log = load_json(review_log_path)

    assets = batch.get("assets", [])
    if not assets:
        print("[PASS] Batch has no assets.")
        return 0

    print(f"[START] {batch.get('batch_id')} assets={len(assets)} model={args.model}")

    failures = 0
    for index, asset in enumerate(assets, start=1):
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
            "question mark, speech bubble, arrow, icon, UI element, or any baked text. "
            "Any graphic explanation described in the scene brief will be added later by the compositor. "
            "Compose with generous safe margins so the essential subjects survive a centered 16:9 crop."
        )

        payload = {
            "model": args.model,
            "prompt": prompt,
            "size": args.size,
            "quality": args.quality,
            "n": 1,
        }

        print(f"[GEN {index}/{len(assets)}] {sid}")
        try:
            result = post_json(API_URL, payload, api_key)
            data = result.get("data") or []
            if not data:
                raise RuntimeError(f"No image data returned: {result}")
            save_image_result(data[0], out_path)
            normalize_16x9(out_path)
            row = review_log["assets"][sid]
            row["status"] = "generated"
            row["generated_candidate"] = str(relative_candidate).replace("\\", "/")
            print(f"[PASS] {sid} -> {out_path}")
        except Exception as exc:
            failures += 1
            review_log["assets"][sid]["status"] = "retry"
            review_log["assets"][sid]["notes"] = f"Generation failed: {exc}"
            print(f"[FAIL] {sid}: {exc}", file=sys.stderr)

        review_log_path.write_text(json.dumps(review_log, indent=2) + "\n", encoding="utf-8")
        if index < len(assets):
            time.sleep(max(args.delay, 0))

    print(f"[DONE] generated={len(assets)-failures} failed={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
