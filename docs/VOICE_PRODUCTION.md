# Voice Production — CosyVoice 3

## Locked production voice

**Modern Life Narrator v1**

- Engine: CosyVoice 3
- Voice: built-in female voice
- Language: English
- Delivery: calm, intelligent, conversational documentary narration
- Target chunk size: roughly 15–25 seconds
- Hardware validated: GTX 1060 3 GB for short chunks

Long single requests are deliberately avoided. On the validated machine a 60–90 second request stalled, while ~15 second chunks completed successfully and retained the desired delivery.

## Source of truth

`episodes/MLI-001/narration_chunks.json` contains:

- exact spoken text;
- stable chunk IDs;
- narrative section;
- engine/language;
- the locked narration instruction.

WAV files are local production artifacts and are not committed.

## Generate

Start VoiceStudio first, then from the repository root:

```powershell
.\tools\generate_cosyvoice_narration.ps1
```

The script:

1. verifies the VoiceStudio backend is reachable;
2. generates each missing chunk through `POST /generate`;
3. leaves successful chunks in place so the run is resumable;
4. retries a failed chunk;
5. stops on a persistent failure rather than silently skipping audio;
6. concatenates all chunks to `episodes/MLI-001/media/narration.wav`.

## Resume

If a run stops at chunk 17:

```powershell
.\tools\generate_cosyvoice_narration.ps1 -StartAt 17
```

Existing WAVs are skipped unless `-Force` is supplied.

To generate/review chunks without assembling the final narration:

```powershell
.\tools\generate_cosyvoice_narration.ps1 -NoAssemble
```

## Quality gate

Automation success is not artistic approval.

Before rendering the episode, listen to the generated chunks and regenerate any take with bad pronunciation, pacing, emphasis, glitches or tonal drift. Once approved, assemble `narration.wav` and use:

```powershell
.\tools\render_with_narration.ps1
```
