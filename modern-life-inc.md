# MODERN LIFE INC. — Operating Context

## GUARDRAILS
- Respond in concise, natural English; prioritize verified results and actionable next steps.
- If my English sounds unnatural, suggest a native-sounding alternative with one brief explanation.
- At the start of a new chat, read this file; check repository, branch, latest commit and latest CI.
- “Continue” means perform the next pending task, not simply propose one.
- Act autonomously; request essential information or risky-action authorization only.
- Label implemented, locally tested, CI-pending, CI-passed and merged separately.
- Never invent functionality, measurements, image quality acceptance or readiness percentages.
- Preserve user-local media, modified manifests, installation settings and unpublished content.
- Keep credentials, tokens, private analytics and local binaries out of commits and chat.
- Never discard local changes, remove assets, publish, or merge important branches without approval.
- Update STATE after meaningful work with the actual branch/commit/CI evidence.
- Include the active PR link in reports so checks can be monitored directly.
- Keep this context short; replace stale facts instead of accumulating history.
- Follow docs/operations/controlled-development-roadmap.md; EA uses fixed binary merge gates.
- Local Ruff lint, Ruff format, Pyright and pytest preflight precedes PR for Python changes.
- CI confirms preflight; do not use CI as an iterative debugger.
- Optimize for producing a repeatable publishable video, not maximizing infrastructure or PR count.

## PROJECT
- Purpose: Modern Life Inc., an English-language faceless YouTube channel on modern-life psychology.
- Goal: original, engaging, low-cost, as-automated-as-practical episodes with human editorial QA.
- Reference direction: simple reusable visual language; avoid unneeded photorealistic continuity burden.
- Repository: RafaelAlbaWebify/modern-life-inc-production; protected target branch: main.
- Working review branch: feature/controlled-development-context-20261016; active PR #15.
- Windows workspace: C:\ModernLifeInc; preserve uncommitted production_manifest.json and media/.
- Canonical episode: episodes/MLI-001; storyboard and production_manifest.json contain 56 timed scenes.
- Composition: 10 HERO, 22 HYBRID, 24 SYSTEM; classification does NOT imply animation.
- Renderer: Python/Pillow static scene PNGs plus FFmpeg assembly; no true motion system.
- Voice: local PocketTTS WAV approximately 447.947 seconds; generated outside Git.
- Visual tools: prepare_visual_batch.py, review_visual_asset.py and local staging/import.
- Local experimentation: Forge with SD 1.5 on GTX 1060 3 GB, 32 GB RAM; image batch quality unverified.
- Project checks: python -m ruff check .; python -m ruff format --check .;
  python -m pyright; python -m pytest -q.
- Main CI workflows: .github/workflows/preflight.yml, production-mvp.yml, mli001-render-smoke.yml.

## STATE
- Verified main HEAD: be7116d09e3823538fe76cfb1f49c23c47cb3135 (PR #14 merged 2026-10-13).
- Open PR inventory on 2026-10-16 before this work: none.
- Latest observed CI overall: preflight run 38437852866, green on unmerged
  feature/clean-photographic-scenes commit 0794b933 (2026-10-13).
- Main render smoke observed green at ab25857, run 38420189513; not proof of current main full QA.
- 14 historical PRs merged; MLI-001 placeholder-enabled audio MP4 technically verified locally.
- Eight local locked scene assets reported; remaining photographic quality/availability not fully verified.
- Known blockers: no publishable strict-render acceptance; 32-photo strategy labor-intensive;
  still-frame compositor lacks moving visual grammar, captions and editorial continuity.
- Clean-photo renderer fix resides on separate unmerged feature branch; do not assume in main.
- NEXT: verify this governance PR CI, collect Windows preflight if necessary, request merge approval.
- AFTER: freeze scope, benchmark local Forge SD 1.5 quality/time against reuse-first visual method;
  choose one production workflow, create short reference-quality sample, then publish MLI-001.
- Never equate a successful render or CI with an audience-ready or monetizable episode.
