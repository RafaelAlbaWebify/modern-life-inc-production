# Production MVP v0.1

## Objective

Get Modern Life Inc. from script to uploadable video as quickly as possible, then improve from real audience feedback.

## What v0.1 automates

1. Read episode production manifest.
2. Render SYSTEM scenes procedurally.
3. Accept generated base images for HYBRID/HERO scenes.
4. Add simple overlays.
5. Assemble timed scene stills.
6. Encode MP4 with FFmpeg.

## What v0.1 deliberately does not solve yet

- sophisticated animation;
- character rigs;
- automatic image generation API;
- automatic voice generation;
- subtitles;
- music/SFX;
- complex transitions.

Those are added only after the first end-to-end preview works.

## Fast path

### Gate A — Technical preview
Render the first six SYSTEM scenes as a silent video.

Command:

```powershell
.\tools\render_mvp_preview.ps1
```

### Gate B — Hybrid proof
Drop one approved generated image into the episode media folder, reference it in the manifest, and render a short SYSTEM + HERO/HYBRID sequence.

### Gate C — Full visual cut
Render all 56 beats.

### Gate D — Voice
Add final narration and retime scene durations to the real audio.

### Gate E — Publish
Thumbnail + metadata + upload.

## Optimization rule

Publishability beats architectural completeness.

Any feature that does not materially improve the first upload is deferred.


## Narration-driven timing lock

After narration and the retention pass are approved, storyboard timing is synchronized automatically from the real chunk WAVs.

Run:

```powershell
.\tools\retime_storyboard_to_narration.ps1
```

The command:

1. reads every generated narration chunk WAV;
2. adds configured inter-chunk pauses;
3. accounts for the final global narration tempo;
4. derives the real duration of each narrative section;
5. redistributes that duration across the storyboard scenes assigned to the section while preserving their authored relative weights;
6. uses the assembled `narration.wav` duration as final authority;
7. rewrites exact `start_sec`, `end_sec`, and `duration_sec` values;
8. rebuilds the complete `production_manifest.json` from all storyboard scenes.

This replaces manual storyboard retiming and is the required timing-lock step before final visual production.
