# Modern Life Inc. — Controlled Development Roadmap

Baseline: 2026-10-16. Target branch: `main`. Governance branch: `feature/controlled-development-context-20261016`.
Reference: VERIDRA controlled development roadmap. This roadmap concerns **development**, not publication or channel success.

## Fixed progress rules
- Weights in each phase sum to **100%**; each subphase is **0% or 100%** complete only.
- Completion requires the scoped implementation, relevant automated tests, successful CI at the final revision, and verified merge to `main`. Historical work is not automatically credited without scoped evidence.
- Phase progress = sum of weights of completed subphases. No unapproved global percentage.
- A green CI run, unmerged implementation, passing smoke tests, or local generation alone never counts as phase completion.
- Numbering and weights are fixed. Changing scope requires a documented rationale and explicit user approval.
- `EA`: output every subphase as `Phase N.M → Name → Verified description/status → X% complete → Weight: Y% of phase total.`; output each phase total.
- Keep code PRs small, run local Ruff/format/Pyright/pytest before PR, verify CI, require approval to merge; never use CI to debug.
- Preserve local images, WAVs and modified manifests. Keep private or binary data out of repository.

## Phase 1 — Controlled production governance (0%)
- **1.1 — Context and state (35%)**: `youtube.md` accurately identifies project, commands, main HEAD, branches, latest verified CI and NEXT. Evidence: file in main, reviewed content, green PR CI.
- **1.2 — Weighted roadmap and EA (35%)**: this file has stable numbering/weights, binary progress rules and demonstrable EA calculations. Evidence: review/test of sums and merged file plus green CI.
- **1.3 — Preflight and preservation (30%)**: recorded repeatable Windows preflight, no destructive operations, clear merge authorization process. Evidence: preflight output, CI and accepted merged governance workflow.
- **Total phase progress: 0%**; governance files in PR are not merged.

## Phase 2 — Minimal repeatable visual production (0%)
- **2.1 — Choose workflow from measured proof (25%)**: compare one local Forge SD 1.5 batch with reuse-first visual approach; log time, quality, coherence and costs. Evidence: measured local samples, decision, regression evidence and merged documentation.
- **2.2 — Asset consistency and editorial rules (25%)**: define reusable style/character continuity, remove unwanted compositor text/bubbles; keep approved asset state explicit. Evidence: visual acceptance sample, automated pixel/contract tests and merge.
- **2.3 — Batch creation and import (25%)**: proven no-cost batch workflow with checked outputs and no approval bypass. Evidence: local batch logs, automated tests, CI and merge of scoped acceptance requirements.
- **2.4 — Moving visual grammar (25%)**: deliver a 45–60 second sample with genuine motion/editing and suitable captions. Evidence: reviewed MP4, automated rendering checks, CI and merge. No assumption that a static MP4 passes.
- **Total phase progress: 0%**; existing importer is merged, but full scoped gates are not verified.

## Phase 3 — Publishable MLI-001 (0%)
- **3.1 — Editorially final script and narration (20%)**: confirm timing, voice intelligibility, factual support and usable audio. Evidence: reviewed artifact, audio validation, tests/CI and merged acceptance.
- **3.2 — Complete visual assets (30%)**: all actual visuals available with consistent style and explicit approval, no missing/rejected candidates. Evidence: strict inventory, reviewed images and merge.
- **3.3 — Strict final render and QA (30%)**: no placeholders, synced WAV, captions, coherent pacing and real visual review. Evidence: full MP4 acceptance report, automatic format/duration checks, green CI and merge.
- **3.4 — Publishing package (20%)**: title, thumbnail, description, evidence/licensing and upload readiness. Evidence: editorial approval, automated metadata checks where applicable, green CI and merge. Publishing itself is a separate authorized operation.
- **Total phase progress: 0%**; existing rough cut is not publication acceptance.

## Phase 4 — Repeatability and learning (0%)
- **4.1 — Episode template (30%)**: run a second episode through the same documented workflow without custom scene code. Evidence: repeatable test artifacts, automated checks, green CI and merge.
- **4.2 — Operator time/cost measurements (25%)**: record manual minutes, machine time, rework, and software charges per episode. Evidence: repeatable measurement log/tests and merge.
- **4.3 — Safe release and analytics (25%)**: documented private upload approval, post-publish learning at 24h/72h/7d/28d, without automatic publishing. Evidence: dry-run or real permissioned workflow, tests/CI and merge.
- **4.4 — Recovery and ongoing maintenance (20%)**: verify local media backup/recovery and regenerate a representative episode from its durable assets. Evidence: local restore test, regression checks, CI and merge.
- **Total phase progress: 0%**; no second episode or repeatability acceptance evidenced.

## NEXT
1. Verify governance branch and PR preflight/CI; merge only after approval, then recalculate Phase 1.
2. Complete the local SD 1.5 baseline without changing the production repo or promising GPU performance.
3. Compare real output against the channel reference, select one simpler workflow and deliver a short publish-quality proof.
