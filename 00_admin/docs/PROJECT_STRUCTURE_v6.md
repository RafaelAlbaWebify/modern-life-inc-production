# Modern Life Inc. — Production Structure v6

## Core production rule
The primary video system is now scene-based limited animation.

Each visual beat should normally use:
- one simple background,
- one or two characters,
- one meaningful prop/metaphor,
- 2–4 pose/state changes,
- cheap 2D motion only where useful,
- hard cuts between scenes.

## Shared assets

assets/
  characters/
    dave/
      model/       Canonical Dave reference/model sheets
      poses/       Approved reusable pose cutouts
    cast/          Approved recurring supporting characters
  props/           Reusable transparent props
  backgrounds/     Simple reusable environments/backgrounds
  overlays/        Arrows, symbols, number cards, masks, etc.
  shared/          Other approved reusable assets

## Episode structure

episodes/MLI-001/
  01_research/
  02_script/
  03_audio/
  04_storyboard/
    legacy/        Old storyboard kept only as reference
  05_scenes/
    scene_001/
    scene_002/
    ...
  06_renders/
    tests/
    reference/
    final/
  07_packaging/
  08_qc/

## Scene folder standard

Each scene should eventually look like:

scene_003_rent/
  background.png
  dave_happy.png
  dave_shocked.png
  rent_idle.png
  rent_attack.png
  paycheck.png
  scene.json

`scene.json` is the source of truth for timing and limited-animation events.

## Renderer role

FFmpeg/Python should:
- assemble scenes,
- perform simple translations/scales/rotations,
- swap pose/state images,
- handle visibility and timing,
- mux narration,
- create QC contact sheets.

The renderer should NOT invent scene composition automatically.
