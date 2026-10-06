# Renderer Contract v1

## Objective

Render Modern Life Inc. episodes from declarative scene JSON using reusable vector/raster assets and a very small motion vocabulary.

The renderer must support the current MLI-001 storyboard without requiring:
- skeletal rigs;
- lip sync;
- 3D;
- frame-by-frame animation;
- per-scene bespoke code.

## Pipeline

scene JSON
→ validate schema
→ resolve assets/layout
→ compose frame graph
→ apply simple transforms over time
→ render frames
→ FFmpeg encode
→ MP4

## Required primitives

### Layers
- background
- figure
- icon
- text
- line/arrow
- shape
- image

### Transforms
- x/y position
- scale
- rotation
- opacity
- crop
- z-order

### Motions
- fade
- slide
- slow push
- pulse
- reveal
- highlight
- none

## Scene contract

Every scene must define:
- id
- duration
- layout
- background
- layers

Optional:
- transition_in
- transition_out
- notes

## Layouts v1

- single_focus
- two_person_conversation
- two_person_gaze
- split_contrast
- evidence_card
- three_item_heuristic
- convergence
- phone_message
- timeline
- group_vs_one
- brand_outro

## Asset IDs

Assets are referenced by stable logical IDs, never absolute paths.

Example:
- figure.standing.neutral
- figure.sitting.engaged
- icon.eye
- icon.message
- bg.cafe
- bg.office

The asset registry maps logical IDs to actual files.

## Rendering constraints

- 1920x1080 master
- 30 fps
- safe margins: 10% outer frame
- primary text max 2 lines
- no more than 2 simultaneous human figures in normal scenes
- no scene-specific code unless the primitive set genuinely cannot express the scene

## Determinism

Same scene JSON + same assets + same renderer version should produce the same visual output.

## Failure behavior

Validation must fail loudly on:
- unknown layout
- missing asset
- unsupported motion
- invalid duration
- invalid layer type

Do not silently substitute missing assets.

## Performance principle

Visual quality matters more than render speed, but architecture should remain simple enough to regenerate a full episode locally without manual editing.

## Scope boundary

v1 is only required to render the scene families already present in MLI-001.
Do not build features for hypothetical future episodes.
