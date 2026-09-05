# Modern Life Inc. — AI Bootstrap Context

## Purpose
English-language YouTube production project for satirical economics / personal-finance explainers.

## Product direction
- Channel: Modern Life Inc.
- Recurring everyman: Dave.
- Narration: VoiceBox using the Nova voice.
- Assembly: Python/Pillow + FFmpeg/FFprobe.
- Visual benchmark: Los Ecomonos mechanics and pacing, without copying protected artwork or characters.
- Current production doctrine: authored limited-animation scenes, not automatic infographic layouts.

## Current milestone
Build and verify a clean modular v6.1 asset kit, then rerender a narration-aligned 15-second benchmark.

## Critical architecture rules
- One reusable asset file = one semantic thing.
- Dave pose files contain Dave only; no embedded paycheck, bills, wallet, text, or background.
- Props are separate transparent assets.
- Backgrounds are independent.
- Scene composition/timing are authored explicitly.
- Renderer executes; renderer does not invent composition.
- Normal scene grammar: illustrated scene + 2–4 cheap state/motion events + hard cut.
- Do not use storyboard/contact sheets as video assets.
- Do not use constant Ken Burns motion as the primary motion language.

## Current state
Development/internal testing are usable. External/publishing/production readiness have NOT passed.

## Start every fresh session
1. Read `.ai/CONTEXT.md`.
2. Read `.ai/PROJECT_STATE.json`.
3. Read `.ai/KNOWN_ISSUES.md`.
4. Read `.ai/OPERABILITY.md`.
5. Inspect Git status/current commit.
6. Load only files relevant to the active workstream.
7. Verify assumptions before changing code/assets.
