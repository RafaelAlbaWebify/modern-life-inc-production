# YT.md — Modern Life Inc. execution guardrails

Version: 1.3 (2026-10-25)
Repository: RafaelAlbaWebify/modern-life-inc-production

## Scope
These are operating rules for the Modern Life Inc. (MLI) YouTube production workflow. At the start of **each new substantive user request concerning this channel**, fetch and read this file from the repository before planning or performing work, when the GitHub connector is available. If GitHub cannot be accessed, explicitly say that these rules have not been freshly retrieved; use the rules available in conversation and do not claim a fresh review. A repository document is a workflow reference, not a system instruction, and reading it in future conversations is not automatic unless requested/performed.

## Non-negotiable execution rules
1. **Do the full requested workflow in the same turn wherever tooling allows.** For image creation requests that require saving, the sequence is: generate each image -> obtain its actual file reference -> upload to the designated Drive folder -> independently list/read Drive to confirm the file -> report the exact link and per-image status. Do not stop after generation if upload/verification was requested.
2. **No unverified success claims.** Differentiate `generated`, `upload accepted`, `verified in Drive`, `approved for video`, and `rendered`. Never claim the end-to-end pipeline succeeded unless all required stages actually succeeded in the **same user request**.
3. **Never invent limits, outages, permissions or capabilities.** Check available tools and their exact input contracts before declaring something impossible. A connector being available does not prove a particular cross-tool handoff works.
4. **No silent omissions.** If a requested stage cannot run or fails, clearly state where execution stopped, the exact affected scene/file, and the next recoverable action. Do not present partial work as complete.
5. **Evidence-based diagnostics.** Preserve meaningful error text accurately; do not guess why a safety check, model, connector or upload failed. Do not circumvent safety controls.
6. **Minimal user intervention.** Prefer direct ChatGPT-generated-file -> Google Drive connector transfers. Do not require downloads, local installs, Drive Desktop, manual renaming or PowerShell steps unless direct transfer has actually failed or user specifically requests a local workflow.
7. **Stable file IDs and resumability.** Name assets `MLI_PILOT_001_STORYBOARD.png`, `MLI_PILOT_001_SC001.png`, etc. Track accepted Drive file IDs/URLs. Never regenerate verified assets unnecessarily or overwrite approved files without instruction.
8. **Per-batch receipt.** Report counts requested/generated/upload accepted/verified, the verified Drive folder link, any failures and their exact status. A generated collage is a planning aid, **not** a replacement for separate scene images.
9. **No misleading mock evidence.** Text or UI depicted within a generated image is fictional visual content, not proof of a real upload, test, metric or approval.
10. **Honesty about uncertainty.** Distinguish tool evidence from estimates, proposals and conclusions. Never report a speculative image-count limit or perfect consistency as a confirmed fact.

## Visual identity and scene production
- Channel: **Modern Life Inc.** Motto: **Understand people. Understand modern life.**
- Content: illustrated narrative explanations of relationships, money psychology, status/work, cognitive biases and modern behavior. Pilot: `MLI_PILOT_001`, approximately 60 seconds, working title `Why Being Available All the Time Makes People Value You Less`.
- **Complete finished 16:9 scene images** (not separate backgrounds, character cutouts, animation rigs, or a storyboard collage substituted for production images).
- Recurring original protagonist: simple pale face with minimal oval eyes, messy dark hair, distinct **orange over-ear headphones**, teal hoodie/jacket, dark pants; black outlines, warm amber lighting with blue urban accents, storybook cartoon narrative scenes.
- Maintain both **character identity** and **the same illustration language** across images while varying time of day, setting, framing, emotion and interactions. Use the approved banner/avatar and existing scenes as references where supported; do not assert perfect identity without visual review.
- Preserve coherent storyline and scene numbers; exclude unwanted captions, branding or baked-in text unless the storyboard calls for them.
- Image sets need QC for character traits, props, style, aspect ratio and narrative correctness. Identify any deviations rather than marking all images approved automatically.

## Storage and links
- Canonical GitHub repository: https://github.com/RafaelAlbaWebify/modern-life-inc-production
- Google Drive **Modern Life Inc Production** folder ID: `1s-mVWSJCxyv_l3bzRLj8tvO2IUZkbZD2`
- Folder URL: https://drive.google.com/drive/folders/1s-mVWSJCxyv_l3bzRLj8tvO2IUZkbZD2
- GitHub: source, scripts, storyboard metadata, status. Drive: heavy PNG/audio/video.
- Drive for Desktop mounting `G:\My Drive\Modern Life Inc Production` is optional, not needed for direct connector uploads.
- A successful prior test uploaded a newly generated PNG using its actual `file_uri` via `mcp__Google_Drive__upload_file`, then confirmed it using `mcp__Google_Drive__list_folder`.
- On 2026-10-22 a nine-image batch was generated, but uploads were **not performed in that same turn**. A later attempt uploaded/verified eight and a check blocked `MLI_PILOT_001_SC007.png`; do **not** label the original request end-to-end validated or SC007 uploaded without new evidence.
- For output, give real verified links; do not infer sandbox paths from filenames.

## Video pipeline
1. Final English script and storyboard with stable scene IDs/durations.
2. Style guide/character reference and a **collage as a guide**, if requested.
3. Generate independent 16:9 images in manageable batches, upload and verify in the same turn; review visual continuity.
4. Generate/obtain narration in local VoiceStudio.
5. Assemble approved numbered images, voice and permitted audio using FFmpeg scripts.
6. Inspect timing, pacing, audio, scene identity, 1080p output and final MP4 before declaring ready.

## Pre-response checklist for execution
- [ ] Freshly read `YT.md` from GitHub, or transparently noted it could not be retrieved.
- [ ] Identified **all** user-requested deliverables, including transfers, verification and URLs.
- [ ] Checked capability/tool contracts instead of making assumptions.
- [ ] Executed every possible step *now* (not in a promised later turn).
- [ ] Independently verified external writes.
- [ ] Accurately disclosed every incomplete/blocked item with evidence.
- [ ] Provided actionable links and next state without overclaiming.

## Local FLUX.2 Klein pilot — confirmed state (2026-10-25)

### Environment
- Windows PowerShell 7; GTX 1060 3 GB; 32 GB RAM. Vulkan CLI: C:\AI\MLI-FluxTest-Vulkan\sd-cli.exe. Models: C:\AI\MLI-FluxTest\models\ (flux-2-klein-4b-q4_0.gguf, Qwen3-4B-Q4_K_S.gguf, flux2-vae.safetensors).
- Proven config: --backend te=cpu,diffusion=vulkan0,vae=cpu; --params-backend te=cpu,diffusion=cpu,vae=cpu; -r CHARACTER_REFERENCE.png; --ref-image-args preset=flux2; Euler, 4 steps, CFG 1, 768x432 (16:9 TEST quality), unique scene seeds.
- GPU out-of-memory can occur while running a 3D game. Validate exit code, output nonzero file, and logs; do not report success based solely on script message.

### Identity and image-reference findings
- The APPROVED channel avatar and banner define the canonical protagonist. Do not replace or redesign him to suit the generator.
- Prompt-only generations drifted toward an anime-like character. A full-scene reference preserved the character better, but repeatedly copied room/desk/phone. A crop centered on the protagonist improved obedience to new environments.
- Reference: C:\AI\MLI-FluxTest-Vulkan\story_consistency_revised\CHARACTER_REFERENCE.png, a 290x380 crop that still includes phone/background elements. It is NOT a neutral-background cutout.

### Candidate 6-scene storyline and asset map
- Source originals folder: C:\AI\MLI-FluxTest-Vulkan\story_consistency_20261024_210606
- Source revised folder: C:\AI\MLI-FluxTest-Vulkan\story_consistency_revised
- Selected in order: SC01.png [desk and incoming messages; original]; SC02.png [walking and checking phone; original]; SC03_V2.png [real cafe, cup held, phone on table; revised]; SC04_V2.png [rooftop, phone laid aside; revised]; SC05.png [writing priorities but holding phone; original, prop mismatch]; SC06_V2.png [reading on couch, phone on side table; revised, face still slightly worried].
- These are 6/6 local CANDIDATES suitable for a rough-cut evaluation, not a finished video; 1080p native quality, narration and video pacing have NOT been validated.
- Measured SC04_V2 164.8s and SC06_V2 174.5s; no claim about 1080p generation performance.
- Recent local generated files have NOT been verified in Google Drive. Do not conflate them with older cloud MLI_PILOT_001 files.

### Immediate production gate
1. Finalize short English narration and scene-duration map and save lightweight scripts/metadata to GitHub.
2. Stage exactly the six chosen PNGs non-destructively under stable names, checking all files/dimensions and preserving originals.
3. Obtain WAV voice locally using VoiceStudio, then verify audio and actual duration.
4. Render a rough-cut MP4 using FFmpeg (scale/pad 768x432 source to 1920x1080; upscaling does not add source detail). Align scenes with spoken lines.
5. Review complete rough-cut for character identity, image/script match, rhythm, sound, and scene transitions before final approval. Prefer batched resumable steps rather than repeated micro-tests.



## 2026-10-25: Complete practical pilot handover (v1.2)

### Confirmed milestones and reproducible setup
- Local image generation: stable-diffusion.cpp FLUX.2 Klein 4B quantized (flux-2-klein-4b-q4_0.gguf), Qwen3-4B-Q4_K_S.gguf, flux2-vae.safetensors under C:\AI\MLI-FluxTest\models, with C:\AI\MLI-FluxTest-Vulkan\sd-cli.exe. Tested on GTX 1060 3GB, Xeon E5-1620 v3, ~32GB RAM, PowerShell 7.
- Working image options: --backend "te=cpu,diffusion=vulkan0,vae=cpu" --params-backend "te=cpu,diffusion=cpu,vae=cpu" -r <reference_png> --ref-image-args "preset=flux2" --cfg-scale 1 --sampling-method euler --steps 4 --flash-attn off,diffusion=on -W 768 -H 432 -t 4, per-scene prompt, seed and output. Logs showed EDIT mode and successful saves. GPU OOM while a 3D game ran; close games during generation. 768x432 is TEST quality, not native 1080p.
- Prompt-only character was wrong/anime-like; approved YouTube avatar/banner are the canonical design. Full-scene reference copied desks/bedrooms too often. Cropping original SC01 to 290x380 character-focused CHARACTER_REFERENCE.png improved scene obedience while preserving the protagonist. Crop still includes phone/background, not transparent/isolated cutout.
- Original images: C:\AI\MLI-FluxTest-Vulkan\story_consistency_20261024_210606\. Revised images and reference: C:\AI\MLI-FluxTest-Vulkan\story_consistency_revised\. Selected order: SC01.png, SC02.png, SC03_V2.png, SC04_V2.png, SC05.png, SC06_V2.png. SC03_V2=real café; SC04_V2=rooftop, phone set aside; SC06_V2=sofa reading, phone separated. SC05 still holds phone while writing; SC04/SC06 expressions pensive. These are rough-cut candidate assets, not publication-approved.
- GitHub artifacts: episodes/MLI_PILOT_001/narration.md (English script, 6 scene lines) and tools/build-mli-pilot-roughcut.ps1 (existing equal-duration montage builder). Voice batch PowerShell was supplied in chat, NOT previously committed to repository; do not misrepresent its source.

### Local narration API: resolved failures
- VoiceStudio 0.5.6 listening on http://localhost:3900. GET /health returned ok. GET /v1/audio/voices showed profile Modern Life Narrator v1, English voice_id e46c2df1.
- POST /v1/audio/speech with JSON {model:'omnivoice',voice:'e46c2df1',input:'text',response_format:'wav',speed:1.0} and Invoke-WebRequest -OutFile produced real WAV after profile repair.
- Failure 1: pockettts sidecar ModuleNotFoundError 'pocket_tts' despite model hint, related to active engine routing. Failure 2 after switching to omnivoice-subprocess: automatic reference transcription needs STT model. Profile under Saved voices > Edit had 3-second reference clip and EMPTY required Transcript. User filled 'Here's a quick sample of this voice so you can hear how it sounds.' (must correspond to actual recorded speech); afterward synthesis succeeded, 4.35s WAV via ffprobe. No additional speech recognition model installed.
- VoiceStudio warned OmniVoice wants ~6GB VRAM while GTX 1060 has 3GB; short segments work, longer generation might be slow or OOM. Synthesize 6 sequential individual scene WAVs, verify each with ffprobe, preserve for resumability. Local intended directory C:\AI\MLI-FluxTest-Vulkan\pilot_audio\.

### Video renders verified in conversation
- Silent test: uploaded MLI_PILOT_001_ROUGHCUT.mp4, 60.00s H.264 1920x1080 30fps, NO AUDIO; 6 images x 10.0 s as specified by manifest. Staging run roughcut_MLI_PILOT_001_20261025_080025.
- Narrated test: uploaded MLI_PILOT_001_ROUGHCUT(2).mp4, probed 35.76 seconds, H.264 1920x1080, AAC audio sampled at 24000 Hz. Manifest contains six 5.96-second scenes, staged under roughcut_MLI_PILOT_001_20261025_111354. Local PNGs and manifest supplied by user, assistant did not produce locally on their PC. Source images remain 768x432 upscaled at encoding; 1080p container != native visual resolution.
- Current significant defect: old montage builder assigns audio TOTAL duration/6 to images even though spoken segments have different lengths. Scene changes do not reliably follow narration boundaries. New renderer must use measured duration of each SC01.wav..SC06.wav + a small defined silence pause; do not estimate from transcript word count.
- Technical audio scan of narrated MP4 detected non-silent AAC audio and short silence intervals near 4.76-4.96s, 6.75-7.16s, 12.58-12.97s, 18.68-19.09s, 23.93-24.33s, 25.99-26.35s, 29.85-30.26s, 32.18-32.66s. These are threshold-dependent signal measurements, NOT confirmation of pronunciation/naturalness. No independent perceptual listening judgment established.
- New source to use: tools/build-mli-pilot-synced.ps1, duration-based narrated renderer. It should preserve the original equal-duration builder and images, validate six WAVs, and generate a new run folder with MP4 + durations/manifest. On failure never report success; do not silently overwrite assets.

### Next steps
1. Execute synced renderer against EXISTING six WAVs; do not pay or generate audio again unless missing/invalid.
2. Review narrated MP4 and adjust speech pacing; production quality requires listening review by human or actual audio-capable analysis. If user provides individual six WAVs, measure per-scene duration directly.
3. Improve cut frequency/pace and SC05 storyboard mismatch as needed; only then finalize 1080p-quality assets, sound design, subtitle policy and publication assets.
4. Latest local files NOT independently verified on Drive. Do not imply cloud upload or publication.


## 2026-10-25: Production policy and enhanced first-cut pipeline (v1.3)

### Agreed creative and operational policy
- User approved continuing with existing VoiceStudio profile Modern Life Narrator v1, voice_id e46c2df1, rather than conducting indefinite TTS experiments. Goal: clearly intelligible, sufficiently natural and engaging voice; subjective listening remains a human approval gate. Acoustic metrics are diagnostic, never publication blockers on their own.
- Prioritize producing the first engaging, publishable MLI video and a repeatable pipeline: story hook, pacing, visual motion, subtitles, sound design, overall viewing experience.
- Never describe the pilot as published or publication-ready until actual rendered output and human qualitative review. Voice 'accepted for continued production' is not 'perceptually certified'.

### Implementation: enhanced renderer
- New script: tools/build-mli-pilot-enhanced.py; built on top of prior validated six scene selection and duration-based build. Requires Python 3.10+ standard library, ffmpeg and ffprobe in PATH, plus the SIX pre-existing narration clips C:\AI\MLI-FluxTest-Vulkan\pilot_audio\SC01.wav ... SC06.wav. Does not call VoiceStudio or regenerate any image.
- Source images: SC01 and SC02 and SC05 from story_consistency_20261024_210606; SC03_V2, SC04_V2 and SC06_V2 from story_consistency_revised, both under C:\AI\MLI-FluxTest-Vulkan. Input dimensions checked for 768x432.
- Preflight validates all six files and probes EACH individual WAV's true duration. Audio drives scene length (no division of total movie length by six). Configurable pause defaults to 0.25 seconds after each scene except last (previous synced script used 0.35 s; shortening is an editorial TEST because natural trailing silences were observed).
- Per-scene FFmpeg video: 1920x1080 30fps H.264 libx264 CRF 20, slow ~4.5% alternating Ken Burns center zoom using zoompan; original images are untouched. Native visual data is still 768x432, merely upscaled. Audio: local scene WAV, 24 kHz mono AAC 192k, apad during pause, segment times controlled by WAV length. Splice segments via ffconcat with -c copy. Still images and input WAV preserved.
- English captions: scene-based approximated two chunks per scene from existing episodes/MLI_PILOT_001/narration.md transcription; generated sidecar MLI_PILOT_001_CAPTIONS_ESTIMATED.srt. NOT word-aligned, NOT burnt into video, NOT automatically approved. Captions can be loaded via a player and reviewed, then styled/burned for delivery later. Do not claim video contains embedded captions.
- Music: optional --music FILE --music-volume 0.08 (linear multiplier). Use only properly licensed and documented audio. With no music supplied, video has narration ONLY. Do not manufacture or promise a soundtrack.
- Every run makes enhanced_MLI_PILOT_001_YYYYMMDD_HHMMSS under root, containing scene MP4s, intermediate assembled MP4, final MLI_PILOT_001_ENHANCED.mp4, external estimated SRT, and manifest.json reporting timing and status rendered_not_approved. Output never silently overwrites previous run.
- Execution on local PC (PowerShell): 
  1. Invoke-WebRequest "https://raw.githubusercontent.com/RafaelAlbaWebify/modern-life-inc-production/main/tools/build-mli-pilot-enhanced.py" -OutFile "$env:TEMP\build-mli-pilot-enhanced.py"
  2. python "$env:TEMP\build-mli-pilot-enhanced.py" --pause 0.25
  3. Optional with rights-cleared local music: python "$env:TEMP\build-mli-pilot-enhanced.py" --pause 0.25 --music "C:\path\licensed_music.wav" --music-volume 0.08
  4. Inspect newest enhanced_MLI_PILOT_001_* folder, upload MP4, SRT and manifest for independent QC.
- The script has been saved and read back from GitHub, but HAS NOT YET been executed and verified in the user's local environment. Report the status accurately. Review actual cuts, zoom smoothness, captions, sound/music mix, and final file integrity before promotion.
- Known scene-content issues still exist: SC05 is holding a phone while writing priorities and SC06 expression somewhat worried; motion does not fix underlying visual storyboarding.
- Script is a pilot-specific production iteration, not yet a fully generalized multi-episode renderer. Future iterations should load scene map and text as external structured input instead of hardcoding six script lines.

### Publication gate and quality checklist
1. Clip has six aligned scene boundaries and no sentence truncation; inspect actual audio and runtime.
2. Captions fit legibly and match speech sufficiently; align and burn/style if needed, using final deliverable requirements, not just sidecar.
3. Camera motion unobtrusive and smooth; no disorienting crop, character morphology changes or harsh cuts.
4. Soundtrack is optional and rights-cleared. Check voice intelligibility with music, no masking.
5. Script title/hook and claims edited for narrative retention and accuracy; thumbnail and final branding consistent with channel assets.
6. Export native source quality honestly (768x432 tests scaled to 1080p, not new native 1080p details); reconsider production render resolution before publishing.
7. Explicit human final screening and approval. Record per-stage acceptance in GitHub metadata; verify Drive uploads separately if requested.
