# Modern Life Inc. — Visual Grammar v1

## Goal

Create a repeatable faceless visual system that is:
- visually coherent;
- fast to author;
- easy to automate;
- readable on mobile;
- expressive without character rigging.

## Core palette

- Background: #0F0F0F
- Secondary charcoal: #2A2A2A
- Primary figure/text: #F4EFE6
- Accent amber: #FFB020
- Accent orange: #FF7A00

## Visual primitives

The renderer should only need these primitives at first:

1. **Figure**
   - full-body simplified silhouette
   - front / 3-quarter / side
   - standing / sitting / walking
   - neutral / engaged / withdrawn

2. **Face focus**
   - head/profile crop
   - eyes / gaze direction
   - simple expression markers

3. **Speech bubble**
   - short phrases only
   - max 5–7 words where possible

4. **Icon**
   - heart
   - eye
   - message
   - clock
   - arrow
   - chair
   - phone
   - question mark
   - warning
   - people

5. **Diagram**
   - arrows
   - circles/highlights
   - two-column contrast
   - 3-part heuristic
   - signal cluster / convergence

6. **Text card**
   - 1–5 words
   - centered or left aligned
   - used sparingly for emphasis

## Motion primitives

Only:
- fade in/out
- slide
- scale/push
- simple position shift
- line/arrow reveal
- highlight pulse
- opacity emphasis
- subtle parallax
- gaze direction change by swapping whole asset

No:
- skeletal rigs
- lip sync
- frame-by-frame character animation
- cloth/hair simulation
- 3D camera
- complex morphing

## Composition rules

- One dominant idea per shot.
- Maximum 2 human figures in most scenes.
- Use 3 figures only when comparison is essential.
- Keep focal content inside the central 70% of frame.
- Important text stays inside the central 60%.
- Avoid tiny props.
- Use contrast before detail.
- Prefer silhouettes and symbols over decorative backgrounds.

## Shot families

### A. Human interaction
Two figures with proximity, gaze, posture or speech.

### B. Contrast
Same scenario split into weak signal vs stronger pattern.

### C. Abstract concept
Icons/arrows/diagram for research concepts.

### D. Evidence card
Minimal citation cue: paper icon + short claim, never long academic text.

### E. Pattern build
One signal appears, then a second, then a third; arrows converge.

### F. Heuristic card
Bold words:
CONSISTENCY
SELECTIVITY
RECIPROCITY

## Rhythm

Target major visual refresh every 6–10 seconds.

Within a scene, subtle motion may continue, but each refresh should introduce at least one of:
- new composition;
- new figure arrangement;
- new icon/diagram;
- new text emphasis;
- new visual metaphor.

## Reuse strategy

Create canonical reusable assets:
- 8–12 generic figures/poses
- 10–15 icons
- 5 diagram templates
- 3 conversation layouts
- 3 contrast layouts
- 2 evidence-card layouts
- 3 title/text layouts

The channel should look richer through composition, not through asset count.
