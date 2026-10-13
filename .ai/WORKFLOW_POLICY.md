# Development and acceptance policy — effective 2026-10-13

## Mandatory operating rules
1. Deliver complete functional increments; avoid one PR/commit per minor component. Define deliverable and acceptance criteria before work.
2. Before opening a PR, run Ruff lint, Ruff format check, Pyright, and pytest. A PR is blocked if any fails; if a tool is not configured, set it up in the existing project rather than claiming preflight passed. Record exact results. Preflight was verified green on 2026-10-13 (PR #12 / run 38414510274). Re-run and record results for every new PR.
3. Minimize manual user intervention. Request local/browser checks only when access to the PC, Chrome, or an external service makes them essential; combine operations into one operator step.
4. Reuse existing architecture and files; no parallel scripts, duplicate state stores, or alternative pipelines without a demonstrated requirement.
5. Measure progress by usable, verified functionality and publication readiness, not commit count, PR count, or chat turns.
6. Require real end-to-end acceptance for Chrome- or third-party-dependent features. Unit tests or mocks alone never close a phase.

## MLI-001 current acceptance gates
- The 56-scene narration rough cut passed local encoding/probing checks, but placeholder-assisted output is not a publishable episode.
- All 32 required photo assets must be present, reviewed, and correctly incorporated before strict rendering without placeholders.
- HYBRID compositions require visual QA beyond automated tests.
- Final narrated render must be checked for story fit, readability, pacing, and sound before marking publishable.
- Do not mark CI green without observing its actual run result.

## Change discipline
Group related fixes into one feature branch and one reviewable PR, with preflight evidence attached. If direct-main changes were previously used, do not represent them as reviewed PRs. Avoid speculative busywork.
