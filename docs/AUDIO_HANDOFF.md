# Audio handoff v1

## Goal

Keep the first upload moving without blocking on VoiceBox automation.

VoiceBox/Nova is currently the only manual production step.

## Input

Generate the final narration from:

`episodes/MLI-001/narration.txt`

Save it locally as:

`episodes/MLI-001/media/narration.wav`

The audio file is intentionally ignored by Git.

## One-command continuation

From the repository root:

```powershell
.\tools\render_with_narration.ps1
```

The command will:

1. validate that narration exists;
2. inspect the audio with ffprobe;
3. reject obviously wrong duration;
4. rebuild the 56-scene production manifest;
5. render the full visual rough cut;
6. mux narration into MP4.

Output:

`episodes/MLI-001/output/rough_cut_with_voice.mp4`

## Current rule

Do not spend time automating VoiceBox before MLI-001 publishes.

After the first upload, measure whether manual narration generation is a meaningful bottleneck. If it is, automate or replace it with a CLI/API-capable TTS system.
