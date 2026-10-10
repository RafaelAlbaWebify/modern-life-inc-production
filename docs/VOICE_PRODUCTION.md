# Voice Production — Modern Life Narrator v1

## Canonical production voice

**Modern Life Narrator v1**

This file is the human-readable source of truth for narration production. Machine-readable settings live in `config/voice_production.json`.

### Validated production path

- Engine: PocketTTS 2.1.0
- Runtime: direct PocketTTS sidecar, kept alive for the whole batch
- Language: English
- Voice profile name in VoiceStudio: `Modern Life Narrator v1`
- VoiceStudio profile ID observed during validation: `e46c2df1`
- VoiceStudio profile kind: `design`
- Canonical reference asset at runtime: `ModernLifeNarrator_reference.wav`
- Reference source: VoiceStudio profile audio for `Modern Life Narrator v1`
- Output: 24 kHz, mono, PCM16 WAV
- Post-processing tempo: 0.94
- Post-processing pitch: -1 semitone
- Typical deliberate pause range: 350–650 ms, chosen by semantic emphasis

The profile ID is an implementation detail of the current local VoiceStudio database and may change if the profile is recreated. Production code should prefer the configured profile name and resolve/export its audio when needed.

## Production architecture

VoiceStudio is used to design and manage the voice. It is **not** the preferred production runtime.

For production narration:

1. Resolve/export the reference WAV for `Modern Life Narrator v1`.
2. Launch the PocketTTS sidecar directly:
   `%APPDATA%\VoiceStudio\runtime\project\backend\engines\pockettts\main.py`.
3. Keep one sidecar process alive for the entire narration batch.
4. Generate semantic chunks with the same reference audio.
5. Insert deliberate silence between chunks.
6. Assemble the raw narration.
7. Apply final Rubber Band processing:
   - tempo `0.94`
   - pitch ratio `0.9438743127` (-1 semitone)
8. Save the final narration as 24 kHz mono PCM16 WAV.

The VoiceStudio `POST /generate` route is currently considered unreliable for this production path. It has timed out for 120–600 seconds while direct PocketTTS sidecar generation remained healthy. Do not use `/generate` as the default narration path unless it is revalidated.

## Validated performance

A direct eight-segment test produced:

- 39.42 s raw audio
- 31.35 s total generation time, including first model load
- ~0.80 generation-time / audio-time ratio for the whole batch
- 41.94 s after final tempo/pitch processing
- post-processing took about one second

Typical steady-state segment generation after model load was roughly 1.2–4.7 seconds for segments of about 2–8 seconds of speech.

This is fast enough for full-episode production on the validated machine.

## Quality target

Delivery should remain:

- adult female narrator
- calm
- intelligent
- conversational
- thoughtful
- documentary-like
- warm and confident
- understated rather than theatrical
- no motivational/sales cadence

The validated voice is intentionally processed slightly slower and slightly lower to add weight without making it sound artificially deep.

## Chunking and pauses

Chunk on semantic units, not arbitrary character counts. Prefer complete thoughts and short paragraphs.

Typical pause guidance:

- 350 ms: minor transition
- 500 ms: normal sentence/block emphasis
- 600–650 ms: stronger rhetorical transition or conclusion

These are defaults, not hard rules. Natural delivery takes precedence.

## Chunk synthesis policy

The WPM-based time-stretch experiment was rejected because it introduced audible artifacts and made chunk 002 unacceptable.

By default, each authored manifest chunk is synthesized as **one PocketTTS request** instead of splitting every paragraph into separate micro-requests. This gives PocketTTS more linguistic context and avoids the artificial timbre observed with aggressive micro-segmentation.

For a specific chunk that is naturally rushed, the manifest may define a small number of explicit `synthesis_groups`. These are human-reviewed semantic groups, not automatic WPM correction. The groups are synthesized independently and joined with a short configured pause. No time stretching is used.

Between manifest chunks, the pipeline inserts the configured pause (currently 650 ms). No per-chunk tempo normalization is applied. The only tempo/pitch processing retained is the final global post-process after assembly.

## Known failure modes and rejected paths

### VoiceStudio /generate

Observed after restart:

- PocketTTS correctly selected as active engine
- `pocket_tts` import succeeded in the VoiceStudio venv
- `POST /generate` still timed out
- no orphan PocketTTS sidecar was present
- direct sidecar generation succeeded

Conclusion: direct sidecar is the production path until `/generate` is revalidated.

### CosyVoice 3 local

Rejected for local production on the validated GTX 1060 3 GB system.

With reference audio, persistent-sidecar inference remained around 44–54x RTF for short phrases. Keeping the model loaded did not solve the bottleneck. Local CosyVoice is not a practical production runtime on this hardware.

### PocketTTS with old CosyVoice-derived reference

The older `MLI001_Chunk01.wav` reference produced an undesirably child-like voice in PocketTTS. That reference is rejected for production.

The current `Modern Life Narrator v1` design reference is the approved reference path.

### Hugging Face access

PocketTTS voice cloning requires approved access to `kyutai/pocket-tts` and local Hugging Face authentication. If cloning unexpectedly falls back to `kyutai/pocket-tts-without-voice-cloning`, verify gated-repository access before debugging synthesis.

## Windows / VoiceStudio runtime

Validated paths:

- VoiceStudio project:
  `%APPDATA%\VoiceStudio\runtime\project`
- Python:
  `%APPDATA%\VoiceStudio\runtime\project\.venv\Scripts\python.exe`
- PocketTTS sidecar:
  `%APPDATA%\VoiceStudio\runtime\project\backend\engines\pockettts\main.py`

Do not hard-code the Windows username in repository scripts.

## Current episode

MLI-001:

**7 Quiet Signs Someone Is More Attracted to You Than They Let On**

Current narration inputs:

- `episodes/MLI-001/narration.txt`
- `episodes/MLI-001/narration_chunks.json`

The previous CosyVoice narration pipeline is legacy. The active generator is now:

`tools/generate_pockettts_narration.ps1`

From the repository root, run:

```powershell
.\\tools\\generate_pockettts_narration.ps1
```

The generator reads `config/voice_production.json`, resolves/exports the `Modern Life Narrator v1` reference when needed, keeps one PocketTTS sidecar alive across the batch, synthesizes each manifest chunk as one contextual request, inserts the configured between-chunk pause, writes resumable per-chunk WAVs, assembles `narration_raw.wav`, applies the locked global Rubber Band tempo/pitch processing, and produces:

`episodes/MLI-001/media/narration.wav`

Resume from a chunk with:

```powershell
.\\tools\\generate_pockettts_narration.ps1 -StartAt 17
```

Existing chunk WAVs are skipped unless `-Force` is supplied. Use `-NoAssemble` to generate/review chunks without creating the final narration. For a bounded acceptance test, use for example `-StartAt 1 -EndAt 2 -Force -NoAssemble`.

## Operator rule

Before changing narration engines, voice identity, tempo, pitch, sample rate, chunking strategy, pause strategy, or recovery procedure, read this file and `config/voice_production.json`.

If a new voice configuration is approved, update both files in the same change so the repository remains the canonical external memory for voice production.

## Acceptance note — 2026-10-09

A two-chunk test with WPM normalization was rejected: chunk 001 still sounded somewhat artificial, and chunk 002 was audibly degraded by time stretching. The WPM-normalization approach was removed. Full-episode generation must not proceed until the single-request-per-chunk test passes.

### Chunk 002 pacing experiment

Chunk 002 remained naturally faster even after switching to single-request synthesis. Because PocketTTS does not expose a native speech-rate control in the validated VoiceStudio integration, chunk 002 is being tested with two explicit semantic synthesis groups separated by 600 ms. Chunk 001 remains a single request. This preserves natural voice quality while testing whether a small contextual split can reduce rushed delivery without time stretching.

## Acceptance note — 2026-10-10

The revised PocketTTS strategy is accepted for production after reviewing MLI-001 chunks 001 and 002. Single contextual synthesis removed the artificial timbre. Chunk 002 remains the explicit exception: two semantic synthesis groups joined by a 600 ms pause to avoid rushed delivery. No per-chunk time stretching is used.

### Fast production workflow

Generate the full episode in one resumable run:

```powershell
.\\tools\\generate_pockettts_narration.ps1
```

Existing approved chunks are skipped. Review the assembled `episodes/MLI-001/media/narration.wav`; regenerate only chunks with an audible defect. This is the preferred workflow over pre-testing every chunk individually.

## Automatic runtime repair

VoiceStudio may recreate or resync its Python runtime after a PC/app restart and drop the optional `pockettts` extra. The production wrapper now checks `import pocket_tts` before every run. If the import fails, it automatically restores the package using VoiceStudio's bundled `uv` with the `pockettts` extra, verifies the import, and only then starts synthesis. Manual reinstall should no longer be necessary.
