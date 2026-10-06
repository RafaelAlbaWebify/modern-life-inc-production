# Hybrid Compositor Contract v2

## Objective

Compose Modern Life Inc. episodes from declarative scene JSON using three visual modes:

- SYSTEM
- HYBRID
- HERO

The compositor is responsible for assembly and motion. It is **not** expected to generate images itself.

## Visual modes

### SYSTEM
Scene built entirely from registered reusable assets, text, icons, diagrams and simple motion.

### HYBRID
Scene uses a generated or bespoke base image plus registered overlays.

Required:
- visual_mode = "HYBRID"
- base_image reference
- optional overlays

### HERO
Scene uses a unique high-impact illustration as the dominant visual.

Required:
- visual_mode = "HERO"
- base_image reference

Overlays should remain minimal.

## Pipeline

storyboard
→ visual classification
→ image generation / asset selection
→ scene JSON
→ validation
→ composition
→ motion
→ render
→ encode

## Scene fields

Required:
- id
- duration_sec
- visual_mode
- layout
- background
- layers

Optional:
- base_image
- transition_in
- transition_out
- notes

## Base images

Generated images are referenced by stable logical IDs, never absolute paths.

Examples:
- hero.mli001.s001
- hero.mli001.s012
- hybrid.mli001.s007

The asset registry resolves those IDs to actual files.

## Motion primitives

- fade
- slide
- slow_push
- pan
- pulse
- reveal
- highlight
- subtle_parallax
- none

## Scope rule

Do not add compositor features to solve one-off artistic problems.

If a scene needs something beyond the supported system:
1. simplify composition;
2. change scene classification;
3. bake complexity into the generated base image.

## Quality target

SYSTEM provides consistency and speed.
HYBRID provides variety.
HERO provides memorable visual peaks.
