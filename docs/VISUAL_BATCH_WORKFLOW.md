# Visual Batch Production Workflow

## Canonical state

- `visual_asset_prompts.json`: required generated assets and prompts.
- `asset_review_log.json`: current review state.
- `media/generated/`: approved final assets using canonical scene IDs.
- `media/generated/_review/batch_NNN/`: generated candidates under review.
- `media/generated/_rejected/`: rejected candidates.

## Batch preparation

Prepare the next retention-priority batch:

```powershell
.\tools\prepare_visual_batch.ps1 -Size 4
```

The tool prioritizes HERO before HYBRID unless `-Mode` is supplied.

Examples:

```powershell
.\tools\prepare_visual_batch.ps1 -Mode HERO -Size 4
.\tools\prepare_visual_batch.ps1 -Mode HYBRID -Size 6
```

Each batch receives a `batch_manifest.json` containing exact scene IDs, prompts, candidate filenames and final filenames.

## Review decisions

After generation, each candidate receives one decision:

- approve: copy candidate to canonical final file
- lock: copy candidate to canonical final file and mark locked
- retry: keep scene pending for a new batch
- reject: move candidate into `_rejected`

Example:

```powershell
python .\tools\review_visual_asset.py --episode .\episodes\MLI-001 --id S001 --candidate "media/generated/_review/batch_001/S001_candidate_01.png" --decision lock --notes "Strong hook and correct hyperreal style."
```

The next batch automatically skips approved/locked assets and retries only pending ones.

## Completion gate

Run:

```powershell
.\tools\check_visual_assets.ps1
```

Generated visual production is complete when all required HERO/HYBRID assets exist in `media/generated/`.

SYSTEM scenes are produced by the renderer and do not require generated photographic assets.


## Google Drive staging

Google Drive is the persistent binary staging area for generated visual assets.

Canonical Drive structure:

- `/Google Drive/Modern Life Inc Production/MLI-001/review/`
- `/Google Drive/Modern Life Inc Production/MLI-001/approved/`
- `/Google Drive/Modern Life Inc Production/MLI-001/rejected/`
- `/Google Drive/Modern Life Inc Production/MLI-001/style_anchor_mli.png`

Workflow:

1. Generate a batch.
2. Upload candidates to `review/` immediately while the generated files are still available in the active session.
3. Review each candidate.
4. Approved assets are promoted to the canonical scene name in `approved/` (for example `S017.png`).
5. Rejected assets are moved to `rejected/`.
6. GitHub remains the canonical source for prompts, manifests, review state and batch metadata.
7. The local repo receives final approved assets for rendering under `episodes/<episode>/media/generated/`.

This avoids depending on transient chat/session storage for production assets.

## ChatGPT candidate intake — existing batch tool

When generated images are already available in the local review folder, reuse the same batch tool rather than manually copying them to final scene paths:

```powershell
python .\tools\prepare_visual_batch.py --episode .\episodes\MLI-001 --import-dir .\episodes\MLI-001\media\generated\_review\recovered --ids S014,S018,S019,S022
```

The importer accepts PNG filenames containing one scene token such as `MLI-001_S014.png` or `S014_candidate.png`. The optional `--ids` filter selects exactly the requested scenes so older rejected candidates are not re-imported. It searches below the selected source folder, validates the image files, rejects unknown, duplicate or approved scene IDs, and creates `_review/import_NNN/` candidate copies plus `output/visual_review/import_NNN/` composited previews. It updates the existing review log to `generated`, **not** `approved`, and never writes final `media/generated/SNNN.png` files. Inspect previews and use `review_visual_asset.py` for an explicit approval decision. Never treat a successful compositor test as proof of visual suitability.
