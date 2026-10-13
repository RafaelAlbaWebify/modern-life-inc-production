# MLI-001 Visual asset audit (reconciled 2026-10-13)

Required photographic scenes: 32 (10 HERO, 22 HYBRID); remaining 24 SYSTEM scenes are rendered without photos.

Verified from local user PowerShell inventory: 8 approved locked assets S001, S007, S017, S023, S027, S032, S037, S054.
Candidate composites successfully rendered locally: S002, S004, S010 (not visually approved).
Additional candidates extracted to local review staging: S008 and S009 (both require regeneration).
Newly downloaded visual batch: S014, S018, S019, S022 — 4 candidates reported installed in review staging, **not yet verified by a local inventory or accepted**.
Previously approved originals S012 and S052 remain unavailable in final local media directory.
Retry: S013, S008, S009. Other never-generated IDs: S024, S025, S028, S029, S033, S036, S038, S039, S045, S047, S049, S050.
The static renderer passed the placeholder-assisted CI smoke test; this is not final editorial acceptance. Locked narration duration 447.947 seconds. Final strict render and audiovisual acceptance remain blocked.

Contract: local file existence never constitutes approval. Only explicit review decisions in asset_review_log.json authorize promotion. The existing prepare_visual_batch.py, review_visual_asset.py, and renderer must be reused; do not create a duplicate asset workflow.
