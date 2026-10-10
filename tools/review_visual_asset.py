from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", required=True)
    ap.add_argument("--id", required=True)
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--decision", required=True, choices=["approve", "retry", "reject", "lock"])
    ap.add_argument("--notes", default="")
    args = ap.parse_args()

    episode = Path(args.episode)
    log_path = episode / "asset_review_log.json"
    log = load(log_path)

    sid = args.id
    if sid not in log["assets"]:
        raise SystemExit(f"Unknown asset ID: {sid}")

    row = log["assets"][sid]
    candidate = episode / args.candidate
    if not candidate.is_file():
        raise FileNotFoundError(candidate)

    final_path = episode / row["final_file"]
    rejected_dir = episode / log["workflow"]["rejected_directory"]
    rejected_dir.mkdir(parents=True, exist_ok=True)
    final_path.parent.mkdir(parents=True, exist_ok=True)

    if args.decision in {"approve", "lock"}:
        shutil.copy2(candidate, final_path)
        row["status"] = "locked" if args.decision == "lock" else "approved"
        row["selected_candidate"] = args.candidate.replace("\\", "/")
    elif args.decision == "retry":
        row["status"] = "retry"
    else:
        target = rejected_dir / candidate.name
        shutil.move(str(candidate), str(target))
        row["status"] = "rejected"
        row["rejected_file"] = str(target.relative_to(episode)).replace("\\", "/")

    if args.notes:
        row["notes"] = args.notes

    log_path.write_text(json.dumps(log, indent=2) + "\n", encoding="utf-8")
    print(f"[PASS] {sid} -> {row['status']}")
    if args.decision in {"approve", "lock"}:
        print(f"[FINAL] {final_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
