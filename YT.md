# YT.md — Modern Life Inc. execution guardrails

Version: 6.4 (2026-10-27)
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


## 2026-10-25: User review and camera-direction correction (v1.4)
- User watched MLI_PILOT_001_ENHANCED.mp4 and rejected the repetitive/brusque zoom, experienced as seemingly constant zoom-out. This is explicit creative feedback: DO NOT automate alternating zoom-in/out, or add motion solely to make still pictures move.
- Narrative-first movement rule: default is a STILL frame. Any pan/zoom must have a declared narrative purpose, target subject/prop, approximate narration beat, intensity and easing. Subtle camera work is optional, not a quota. Prefer natural cuts, new image compositions and purposeful visual reveals over repetitive digital zoom.
- Changed tools/build-mli-pilot-enhanced.py to remove the generic alternating camera effect. SC01, SC02, SC03, SC05 and SC06 use static framing. Only SC04 ("The change begins when you put the phone down") applies a max 2% SMOOTHSTEP push aimed toward the lower-right placed phone after about 55% of that scene's speech duration. This is a PROPOSED editorial test, not visually or perceptually approved. It follows the six accepted existing images and original voice clips.
- The previous MLI_PILOT_001_ENHANCED.mp4 is an experimental rejected camera-motion version. Do not treat it as a master.
- Re-render command: download latest https://raw.githubusercontent.com/RafaelAlbaWebify/modern-life-inc-production/main/tools/build-mli-pilot-enhanced.py to $env:TEMP\build-mli-pilot-enhanced.py, run python $env:TEMP\build-mli-pilot-enhanced.py --pause 0.25. Creates a separate enhanced_MLI_PILOT_001_timestamp folder; retains originals and previous output.
- Source updated and read back in GitHub. The revised local MP4 is not yet rendered/visually verified; requires user execution and review before acceptance. Script SRT remains approximate external subtitle timing; optional soundtrack is only present if provided with proven usage rights.
- Later improvement: explicitly author scene/shot motion cues in a small JSON storyboard (e.g., hold / target / onset / speed / easing) rather than hardcoding per-scene camera rules. Introduce scene-internal cuts on actual story beats when justified, not automatic motion.

### 2026-10-25 local enhanced render receipt (user PowerShell)
- User executed latest tools/build-mli-pilot-enhanced.py --pause 0.25; command completed with no reported error and printed STATUS: RENDERED, NOT QC APPROVED.
- Folder: C:\AI\MLI-FluxTest-Vulkan\enhanced_MLI_PILOT_001_20261025_121249\
- Reported scenes: SC01 7.21s, SC02 6.05s, SC03 6.37s, SC04 5.51s, SC05 6.16s, SC06 5.71s. Sum 37.01s approximate (rounded per-scene console values).
- Reported artifacts: MLI_PILOT_001_ENHANCED.mp4; MLI_PILOT_001_CAPTIONS_ESTIMATED.srt; manifest.json under that folder.
- No new MP4 or manifest uploaded in this message: visual motion behavior and final file contents still require independent inspection. Do not claim approval.


## 2026-10-25: Local render output isolation (v1.5)
- User requested that all **new render output artifacts**, including MP4 and intermediary segments/manifest/SRT, be written under Windows user Downloads, not inside the source checkout / model workspace.
- Updated tools/build-mli-pilot-enhanced.py: by default uses Python pathlib.Path.home() / "Downloads", creates a run-specific folder MLI_PILOT_001_YYYYMMDD_HHMMSS with MP4, scene segments, SRT, concat manifest, QC JSON and other derived files. Optional `--output-dir "D:\\SomeFolder"` overrides this root.
- Input PNGs remain read-only in C:\\AI\\MLI-FluxTest-Vulkan\\story_consistency_*; narration WAVs remain read-only in C:\\AI\\MLI-FluxTest-Vulkan\\pilot_audio. This change relocates **output only**; it does not move/delete originals or prior test folders.
- Invocation remains: python "$env:TEMP\\build-mli-pilot-enhanced.py" --pause 0.25. Output now expected at C:\\Users\\<WindowsUser>\\Downloads\\MLI_PILOT_001_<timestamp>\\ (unless custom --output-dir).
- Verification: updated source was read back successfully from GitHub. Windows local execution of this revised version has NOT yet been verified.
- Older renderers/tools/build-mli-pilot-roughcut.ps1 and tools/build-mli-pilot-synced.ps1 retain their historical root-output defaults; use enhanced script for current production. When revising other active tools, apply the same output separation convention.
- Do not automatically delete previous outputs or user files. Offer a reviewed selective cleanup when requested.

## 2026-10-25: Workspace cleanup convention (v1.6)
- User requested latest MP4 moved to Windows Downloads and earlier test output cleanup. Verified mover in tools/move-latest-pilot-mp4.ps1; it selects newest enhanced_MLI_PILOT_001_*/MLI_PILOT_001_ENHANCED.mp4 and moves it into Downloads with run-folder-derived unique name. Only executed by user locally; not performed via GitHub.
- For local cleanup, use a strict allowlist of output folders: enhanced_MLI_PILOT_001_*, synced_MLI_PILOT_001_*, roughcut_MLI_PILOT_001_*. Never delete models, WAVs, story_consistency original/revised, CHARACTER_REFERENCE, sources or source code. Preview first, quarantine old render folders in Downloads; preserve latest run. Do not permanently delete without review. Cloud cleanup cannot be inferred from local naming.
- Google Drive production folder was inspected: contains scene assets and storyboard, rejected candidates and prior transfer/test assets. Do not bulk-delete: old scene images may be required for future episodes, and uploaded local FLUX2 final candidates were not independently verified there. No Drive deletions made.
- GitHub source, narration, scripts and evidence are retained. No confirmed obsolete code or large generated MP4 files identified via GitHub inventory, so no repository deletion was made. GitHub cleanup requires a targeted review/manifest, not blind deletion.


## 2026-10-25: Six-image V2 storyboard & local batch (v1.7)
- User wants greater narrative variety, secondary generic characters with ordinary stylized faces, and a fixed iconic original protagonist. Secondary faces should have normally drawn facial features; only the protagonist retains minimal face and orange headphones.
- Six V2 images generated (1672x941): SC01 desk notifications; SC02 urban street plus ordinary-faced passersby; SC03 café plus background patrons; SC04 rooftop sunset phone laid aside; SC05 desk writing but phone STILL in hand (known QC fail); SC06 sofa conversation with female friend and cat. The six-image ZIP was provided in ChatGPT, NOT confirmed uploaded to Drive or saved to local PC. No V2 video rendered yet. The protagonist's face and illustrated style are retained in candidates, but human final approval is pending.
- Exact visual + narrative map and open issues are in episodes/MLI_PILOT_001/V2-storyboard.md. These are candidates; do NOT overwrite first-generation source image folders or claim an approved master.
- tools/build-mli-pilot-enhanced.py now accepts --images-dir LOCATION containing SC01.png..SC06.png. Supports both legacy 768x432 and V2 1672x941. This script reads existing local WAV voice clips; outputs still go to Windows Downloads as agreed. SC04 legacy selective phone zoom is disabled for --images-dir because new scene's phone is at a different location: camera defaults STATIC in V2.
- V2 run: extract MLI_PILOT_001_V2_IMAGES.zip into $HOME\Downloads\MLI_PILOT_001_V2_IMAGES (files directly inside directory); download latest GitHub script; run python $env:TEMP\build-mli-pilot-enhanced.py --pause 0.25 --images-dir "$HOME\Downloads\MLI_PILOT_001_V2_IMAGES".
- Important: native size 1672x941 is near 16:9 but not exact; scale to 1920x1080 can cause slight aspect mismatch, check visually. Text-based caption SRT remains estimated; not aligned/embedded.
- Current status: script/source/metadata saved and verified in GitHub; image package produced in conversation, V2 local video execution, visual QA, Drive upload, release all pending.

### 2026-10-25 V2 local render receipt
- User extracted six V2 images successfully into C:\Users\ralba\Downloads\MLI_PILOT_001_V2_IMAGES. Console confirmed all SC01.png..SC06.png present.
- User ran latest Python enhanced builder with `--pause 0.25 --images-dir $images` successfully (zero exit status) on 2026-10-25 17:41.
- MP4: C:\Users\ralba\Downloads\MLI_PILOT_001_20261025_174118\MLI_PILOT_001_ENHANCED.mp4
- SRT and manifest.json are in the same folder. Reported scene render lengths: SC01 7.21, SC02 6.05, SC03 6.37, SC04 5.51, SC05 6.16, SC06 5.71 seconds (37.01 seconds summed, rounded).
- STATUS: RENDERED, NOT QC APPROVED. No new MP4 from this run uploaded to this chat yet; audiovisual inspection, captions, story flow and acceptance remain pending. Original PNGs and WAVs were not overwritten.

### 2026-10-25 V2 archive and video inspection receipt
- User uploaded MLI_PILOT_001_20261025_174118.zip. Archive examined: manifest.json; external MLI_PILOT_001_CAPTIONS_ESTIMATED.srt; final MLI_PILOT_001_ENHANCED.mp4; interim MLI_PILOT_001_MOTION_NO_MUSIC.mp4; six SC01..SC06.mp4; segments.ffconcat. All six scene videos supplied.
- ffprobe final: duration 37.041016 s; 1920x1080 H.264 30fps and AAC audio; manifest status rendered_not_approved; no music; external SRT estimated not burned.
- Six frames extracted at 3, 10, 16, 22, 28, 34 s visually checked; foreground iconic lead stays consistent and secondary supporting figures present in SC02, SC03, SC06. Visual story is improved over V1 but NOT approved for release.
- SC05 still actively holds phone while writing, contradicting intentional boundaries. SC06 friend adds warmth, but lead gaze is downward and engagement with friend could be stronger. Each of six still images lasts ~5-7 seconds, limiting narrative variety despite new background characters. Proposed: SC05 phone aside, SC06 protagonist responsive, a few additional meaningful story-beat cuts rather than arbitrary zoom.
- Do not claim subjective voice quality audited by human listening. Final release must review SRT real-word timing and any captions burned in. Preserve this V2 render as baseline, not master.

## 2026-10-25: Production reproducibility redesign (v1.8)
- Postmortem: repeated visual corrections are not just weak prompts. Root cause is narration-to-six-images coupling, no explicit shot grammar, vague prop/eyeline/hand constraints, no semantic QC, generic movement and probabilistic image editing; FLUX.2 Klein can violate complex instructions. The four-step low-memory setup is a feasibility baseline, not guaranteed production quality.
- New production design recorded in docs/production-pipeline-contract.md; it is a **proposal, not yet implemented or validated**. Includes structured shots.json, character/style references, precise required/forbidden actions, bounded generation attempts, targeted test panel, configurable renderer, QA gates and explicit human acceptance.
- Example SC05: phone must be on separate shelf and never in protagonist's hands; SC06: lead must make eye contact with friend. Define observable visual facts, not vague mood adjectives.
- Do not repeatedly re-render 6-scene videos just to discover failed shots. Validate the plan and image candidates before montage; pilot 3 representative difficult shots, assess engine quality before locking.

## 2026-10-25: Structured pipeline implementation (v1.9)
- Created episodes/MLI_PILOT_001/shots.json with six structured visual shot contracts, exact existing scene narration, explicit required/forbidden props, secondary characters, canonical identity instructions, framing and seeds. Scene movement defaults to hold.
- Created tools/plan-shots.py: checks schema, duplicate IDs, nonempty contract fields, constraints, and bounded attempt setting; generates prompts and SHA256 manifest with pending visual QC status. It does not generate images or certify that an image obeys instructions.
- Created tests/test_shot_contract.py: regression tests for schema errors, duplicate IDs, unapproved movement, SC05 phone positioning and SC06 eye contact. Committed but not yet executed on user's Windows machine.
- Run from local repo: python -m unittest discover -s tests -p test_shot_contract.py -v ; python tools/plan-shots.py --shots episodes/MLI_PILOT_001/shots.json --out C:\Users\ralba\Downloads\MLI_PILOT_001_PROMPTS
- Next gate: generate only 3 difficult proof shots with <=2 attempts each, score observable adherence (especially props/gaze/supporting cast), then choose engine. Do not launch whole video until passing this gate.
- Not yet implemented: batch FLUX generation, reference hashing, semantic image QA, multi-shot timeline renderer, accurate subtitles and full integration. Enhanced renderer remains legacy six-scene prototype.

## 2026-10-25: Universal working-directory independence (v2.0)
- Mandatory convention for ALL current and future scripts: callable from any PowerShell/CMD working directory. Never assume current directory contains repository, assets, inputs or output. Resolve repository paths from Python __file__ / PowerShell $PSScriptRoot; use absolute paths for externally supplied roots and explicit flags when a script is downloaded standalone.
- tools/plan-shots.py now defaults shots.json to the parent of its OWN physical script path (`Path(__file__).resolve().parents[1]/episodes/MLI_PILOT_001/shots.json`) and output to user Downloads/MLI_PILOT_001_PROMPTS; optional --shots/--out override these. Executing from C:\Users\ralba or C:\Windows\Temp is supported when the script remains in the full checkout. Standalone downloaded Python source requires --shots ABSOLUTE_PATH.
- tests/test_shot_contract.py added test_invocation_from_unrelated_cwd using a temporary working directory. Test is committed but NOT yet executed on user PC or CI; do not claim passed.
- Correct invocation from anywhere, using absolute path to script: `python "C:\path\to\modern-life-inc-production\tools\plan-shots.py"`. Or supply `--shots "C:\path\to\shots.json"` for a standalone script. No `cd` or assumption of current directory.
- Existing render scripts already use anchored C:\AI paths / their --root flags rather than relying on CWD; audit future scripts and strengthen tests to catch regressions. Avoid vague instructions 'run from repo root'.

### 2026-10-25 shot-planner Windows execution receipt
- User executed the self-contained PowerShell downloader from C:\Users\ralba and successfully obtained `PASS: 6 shot contracts validated` from tools/plan-shots.py; test step returned exit code 0 (full individual test output not supplied).
- Generated seven files at C:\Users\ralba\Downloads\MLI_PILOT_001_PROMPTS: SC01.txt..SC06.txt and prompt_manifest.json (sizes 1102, 1084, 1084, 1074, 1163, 1185, 1462 bytes respectively).
- Confirms CWD-independent downloader + planner prompt output on user's PC; does NOT demonstrate image quality, semantic validation, engine reliability or end-to-end automation. Next stage is a bounded 3-shot engine trial against the prompt contracts.

## 2026-10-25: Single-command FLUX engine acceptance batch (v2.1)
- Created tools/run-mli-engine-gate.ps1 (saved and fetched in GitHub) for PowerShell 7 from ANY working directory. It downloads current shot contract, planner and tests into $env:TEMP/MLI-Pipeline, runs tests, validates all six prompts, and generates SC01/SC02/SC05 using local FLUX2 Klein CLI and canonical character reference. Seed and model flags are fixed; at most 2 attempts PER SHOT on technical failure. FLUX flags use --diffusion-model, --llm, --vae, reference -r, Vulkan backend, 4 Euler steps, CFG1, 768x432.
- Local inputs: C:\AI\MLI-FluxTest-Vulkan\sd-cli.exe, C:\AI\MLI-FluxTest\models\{flux-2-klein-4b-q4_0.gguf,Qwen3-4B-Q4_K_S.gguf,flux2-vae.safetensors}, reference C:\AI\MLI-FluxTest-Vulkan\story_consistency_revised\CHARACTER_REFERENCE.png.
- Outputs: $HOME\Downloads\MLI_ENGINE_GATE_timestamp\ with prompts, images, invocation logs, tests log, engine_gate_results.json, README. Also ZIP in Downloads for review. Never writes render files inside repo or model folders; no model download or modification.
- Gate checks technical PNG signature, nontrivial file length, 768x432 dimensions and exit code. Semantic compliance of people/hands/phone and character consistency NEEDS VISUAL REVIEW. The tool does NOT claim semantic auto-QC or produce complete episode. IMPORTANT: script committed but has not yet been run on user's GPU; errors/CLI compatibility still subject to live execution.
- From ANY PowerShell path: `& { $s=Join-Path $env:TEMP 'run-mli-engine-gate.ps1'; Invoke-WebRequest 'https://raw.githubusercontent.com/RafaelAlbaWebify/modern-life-inc-production/main/tools/run-mli-engine-gate.ps1' -OutFile $s; & $s }`

## 2026-10-25: Profiling before further image generation (v2.2)
- Parsed existing engine-gate run 20261025_180715: diffusion seconds SC01 58.38, SC02 54.06, SC05 53.03; VAE decode 59.57, 59.31, 56.40; total 166.21, 160.14, 152.02. Residual (NOT solely model load): 48.26, 46.77, 42.59 seconds. Approximate means: diffusion 55.16, VAE 58.43, residual 45.87, total 159.46.
- Main bottleneck is not only diffusion: current CPU VAE decode ~58.4s/image, ~36.6% of measured total. Do NOT infer precise model-loading time from residual or claim persistent CLI reuse works before confirming actual local `sd-cli --help`/server capability.
- Added tools/profile-flux-logs.py offline profiler for ZIP, directory or individual log. Produces profile.csv and profile.json to Downloads/MLI_PROFILE (or --out) with timings, residual and parsing warnings, independent of working directory. Reuses prior data; no GPU run required. A new local integration test is still pending.
- Gate stays unapproved semantically: SC02 protagonist lacks orange headphones; semantic QC and bounded retries needed. Next performance test should isolate model load/encode and compare alternative VAE/backend only if VRAM feasibility and CLI compatibility are verified, preserving source models/config.

## 2026-10-25: Persistent server discovery and comparison benchmark (v2.3)
- User ran profiler successfully from C:\Users\ralba, timings matched historical log breakdown exactly: SC01 total 166.21, diffusion 58.38, VAE 59.57, residual 48.26; SC02 total 160.14, diffusion 54.06, VAE 59.31, residual 46.77; SC05 total 152.02, diffusion 53.03, VAE 56.40, residual 42.59 (seconds).
- Confirmed installed binary `C:\AI\MLI-FluxTest-Vulkan\sd-server.exe`. This is evidence of executable availability ONLY, not of exact flags, API compatibility, model persistence benefits or backend performance.
- New tools/benchmark-sd-server.ps1 committed. From any working directory it checks files, captures server --help, checks flags, starts isolated localhost service on port 7861, submits SC01 and SC05 via sdapi/v1/txt2img with base64 character reference, measures cold server startup + separate request times, retains images and logs in Downloads, stops only spawned server, outputs benchmark.json. Important: script itself and API parity have NOT been run on user's specific build; reference semantic equivalence of CLI -r versus server extra_images is not yet verified. A PASS here means only a runtime benchmark and generated bytes, not final-quality proof.
- Goal: compare baseline CLI mean 159.46s with server requests measured after one load, then separately optimize VAE. Do not claim speedups before benchmark result. Render scene pipeline remains blocked on semantic QC.

## 2026-10-25: sd-server benchmark compatibility fix (v2.4)
- Windows user run of tools/benchmark-sd-server.ps1 failed at preflight: installed sd-server help does not list --port, no server process started and no benchmark/image generated. Log path: Downloads/MLI_SERVER_BENCH_20261025_183532/server-help.txt.
- Verified upstream sd-server docs advertise --listen-ip and --listen-port, while older builds may use --host/--port. Updated benchmark to inspect local executable help for either pair and select compatible flags dynamically; HTTP readiness now checks GET / instead of assuming GET /v1/models. GitHub file update verified by commit. Current environment's exact help and API semantics still unknown; next user run is required before claiming operational success.
- The image endpoint /sdapi/v1/txt2img and reference field extra_images remain exploratory; a successful launch does not establish compatibility or measured speedup. If endpoint fails, inspect generated logs instead of adding arbitrary new rendering tests. Original FLUX models left untouched.

## 2026-10-25: sd-server finished benchmark evidence (v2.5)
- User supplied complete MLI_SERVER_BENCH_20261025_184025.zip. benchmark.json status COMPLETE_NOT_VISUALLY_APPROVED, startup 13.48 seconds, request times SC01 287.49s and SC05 202.68s, completed 18:48:52 Europe/Madrid.
- Server internal logs: SC01 reference encode 42.39s, conditioning 49.87s, sampling 103.22s, VAE 91.18s, generation 287.03s; SC05 reference encode 35.41s, conditioning 18.30s, sampling 58.21s, VAE 74.46s, generation 201.83s. Distinguish per-request durations from internal totals.
- Same two shots prior CLI: SC01 166.21s, SC05 152.02s. Persistent server 54.0% slower per-image on average for these two cases (245.085s vs 159.115s), even excluding cold startup. SC05 faster than SC01 server, but still above CLI. No measured speedup proven; do not adopt sd-server for production on this setup.
- Images SC01 and SC05 rendered 768x432 with coherent lead, but SC01 contains unintended background faces and SC05 displays two phone-like rectangular devices despite one phone on separated shelf requirement. Server not editorially approved; default CLI remains performance baseline. Preserve test evidence and revisit with controlled identical request/input API tests only if justified. Next major priorities: semantic image QC and VAE optimization with reproducible identical settings.

## 2026-10-26: Visual acceptance gate and isolated VAE A/B trial (v2.6)
- New tools/visual-qc.py: verifies real PNG signature/size/dimensions/SHA256; creates per-scene observable review criteria (lead orange headphones/teal hoodie, hands, phone count/location, gaze, extras); produces visual_qc.json and review_template.json. It FAILS CLOSED with exit code 3 for pending/unreviewed semantic judgments. Reviewer must supply evidence and identity in decisions JSON; there is **NO automatic image understanding or false claim of semantic certification**.
- New tools/run-visual-qc-vae.ps1: cwd-independent downloader via GitHub REST content to avoid stale raw-cache; locates most recent existing extracted MLI_ENGINE_GATE images in Downloads; runs offline visual technical QC, captures installed sd-cli --help and VAE feature support to new Downloads/MLI_QC_VAE_timestamp folder. Optional -RunVaeTrial generates SC05 baseline and SC05 --vae-conv-direct with same model, seed, resolution, reference, steps, backend and prompt. It only trials when option is advertised in installed local CLI. Logs both runs and elapsed timings, never changes/deletes original models, and does not replace the standard CLI configuration.
- Caveat: this uses two generations and may take several minutes; baseline comparable to prior SC05 but paired same-session baseline is needed for fair A/B. VAE optimization isn't accepted unless total, decode duration and image quality improve reproducibly. CLI may fail due to build-specific flags; inspect logs and stop rather than guessing. Both scripts saved in GitHub, **not yet run on user's Windows installation**.
- Current video generation stays BLOCKED until explicit visual QC approval. Previous engine gate's three output PNGs remain technically valid but semantically unapproved. Pipeline is integrated at acceptance/reporting level; automatic computer vision semantic scoring remains FUTURE work.

## 2026-10-26: VAE A/B and visual QC run receipt (v2.7)
- Uploaded archive MLI_QC_VAE_20261026_081621.zip verified. Baseline: PowerShell wall 176.25s, internal generation 164.35s, sampling 54.05s, VAE decode 65.37s, reference encode 26.31s. `--vae-conv-direct`: wall 176.76s, internal 173.70s, sampling 54.55s, VAE decode 68.46s, reference encode 32.65s. Both exit_code 0.
- Both images exactly binary-identical (SHA-256 149fee0e2c9855b94cea95271ece29a47118df244653ee185f4de2b18aaa1225), also same as earlier SC05 attempt; no semantic improvement. Do not enable option. Experimental log warns: deprecated --vae-conv-direct; suggested replacement --conv-direct auto,vae=on; replacement not benchmarked.
- visual_qc.json validates SC01, SC02, SC05 as technical PASS but each semantic criterion remains PENDING because evidence-based image interpretation is not automated and reviewer decisions were not provided. FAIL_CLOSED behavior working as intended; this is not full visual auto-QC.
- Preserve sd-cli baseline; stop VAE flag trials without evidence of a different meaningful backend. Next deliverable should integrate actual independent semantic image analysis or reviewer-signed acceptance in production, rather than claiming that an unevaluated checklist is automation. No full episode authorized yet.

## 2026-10-26: Actual image-based semantic assessment foundation (v2.8)
- New tools/semantic-qc.py sends existing 768x432 PNG images to the OpenAI Responses API using image input with OPENAI_API_KEY from Windows environment (not recorded). Checks iconic lead identity, hands, phone positions, gazes and secondary character counts, with per-scene PASS/FAIL/UNCERTAIN plus visible evidence text. Uses gpt-4.1-mini default (model/account access must be confirmed locally). API charges/online use apply. On missing key, any API error, malformed response or uncertainty, status PENDING and no approval. No user images are transmitted unless the local command is deliberately executed with a configured API key.
- New tools/semantic-retry-plan.py consumes semantic_report.json and determines REVIEW_CANDIDATE, RETRY or BLOCK per scene, max 2 attempts. REVIEW_CANDIDATE never means publish approved; script never generates images or changes original assets.
- New tools/run-semantic-gate.ps1 downloads latest tools through GitHub REST and locates existing gate images in Downloads from ANY current path, runs remote vision (only if key available), then generates retry_plan.json. Outputs in Downloads/MLI_SEMANTIC_GATE_timestamp. Scripts committed in GitHub; NOT YET EXECUTED against user's GPU or a live model API; no visual benchmark/cost/reliability established. In particular, the retry plan is implemented but actual selective generation execution is not yet wired. Full episode remains BLOCKED.
- Command using existing extracted images: download tools/run-semantic-gate.ps1 from GitHub API and invoke. If no OPENAI_API_KEY, report explicitly records PENDING rather than pretending vision took place. Production policy requires human review of CANDIDATE_PASS images and checks semantic performance of model against known defects (SC02 missing headphones) before unattended use.

### 2026-10-26: Capped selective regeneration integrated (v2.9)
- tools/execute-semantic-retries.py now executes only RETRY decisions returned by semantic-retry-plan.py, and ONLY when latest attempt was 1. It reuses frozen sd-cli model/backend, prompt, reference, four steps, 768x432, and increments the seed by one for attempt 2; never overwrites existing attempt2 or originals. Dry-run by default, --execute explicit.
- tools/run-semantic-gate.ps1 updated: optional -ExecuteRetries performs first remote image QC, decision plan, selective FLUX retry (only FAIL, never PENDING), second remote QC and final decision plan. Without switch: assess and plan only, no GPU. From any PowerShell working directory; gets tools via REST API to avoid stale raw caching. No publication approved automatically; remaining BLOCK and REVIEW_CANDIDATE require human acceptance.
- IMPORTANT: this requires OPENAI_API_KEY configured in the local Windows process environment, and paid OpenAI API access separate from ChatGPT subscription. No key is stored in scripts. If absent, semantic_report.json is PENDING and no attempts are generated. API/schema compatibility and visual accuracy have NOT YET been validated in user's Windows setup; cost and image transfer must be explicitly understood before execution. No model credentials invented. Tool source committed but not verified by running live API or GPU. Never declare fully operational before user runtime receipt and quality evaluation.

## 2026-10-26: Archived engine-gate input support (v3.0)
- User executed `run-semantic-gate.ps1` from `C:\Users\ralba` and got `No extracted engine gate images`; previous engine-gate run was shared as `MLI_ENGINE_GATE_20261025_180715.zip`, and no extracted engine folder was found by the runner.
- Updated runner to search for extracted engine gate candidates first, then newest `Downloads\MLI_ENGINE_GATE_*.zip`. When ZIP exists, it extracts ONLY `SCxx_attempt1.png`/`SCxx_attempt2.png` entries into a temporary staging folder based on ZIP basename. It does not require manual extraction or modify archived source files. Still cwd-independent.
- API-based vision evaluation requires `OPENAI_API_KEY` to be set by user; without it reports PENDING (no billable requests, no retries). No claim of successful live model evaluation yet.

## 2026-10-26: Chat-based visual review (v3.1)
- No paid API services will be used. The previous remote vision runner is not the default workflow.
- Added tools/prepare-chat-review.py to collect existing PNG files from the engine test ZIP, check dimensions and hashes, and produce a chat review package and JSON checklist in Downloads.
- Added tools/import-chat-review.py to verify the review report has matching image hashes and complete per-scene PASS/FAIL/UNCERTAIN assessments before the retry planner reads it.
- User uploads review ZIP to this chat. Vision review happens within the conversation and the resulting evidence-bearing JSON is supplied back to the Windows workflow. This is human-in-the-loop, not fully unattended machine automation. Uncertain cases block; selective second attempts use existing frozen FLUX settings. Scripts committed but not yet locally exercised.

## 2026-10-26: Hardened prompt test correction (v3.2)
- User ran previous hardened-prompt block. It created `Downloads/MLI_PILOT_001_PROMPTS` but failed during Github REST downloader with HTTP 404 before image generation. PowerShell URL interpolation used `$Name?ref=...`; replace with `${Name}?ref=...` to delimit variables.
- More importantly, old tools/run-mli-engine-gate.ps1 regenerated all prompts internally, silently overwriting hardened external prompts. Updated script now supports `-PromptsDir ABSOLUTE_PATH`: after validating original contract, copies user-supplied SC01, SC02, SC05 prompts into the run-specific prompts folder and explicitly reports override. Generation therefore uses actual hardened prompts. Defaults remain unchanged for ordinary runs.
- Next command must download updated script, validate `-PromptsDir` exists in its content, invoke with Downloads/MLI_PILOT_001_PROMPTS, then use latest gate ZIP for offline chat review. This correction is committed, not yet executed on user's machine. No new images from failed 404 run.

## 2026-10-26: Hardened-prompt visual review receipt (v3.3)
- User submitted MLI_CHAT_REVIEW(1).zip containing SC01_attempt1.png, SC02_attempt1.png, SC05_attempt1.png and review_request.json; hash-matched visual inspection performed in this chat.
- SC01 image candidate PASS for five listed criteria: iconic protagonist, clean style/anatomy, exhausted desk action, no secondary people or portraits. SC02 candidate PASS for lead identity, style/anatomy, looking at phone while walking, and exactly three clearly depicted outdoor pedestrians (distant silhouettes visible indoors but are not additional passersby).
- SC05 FAIL on phone position, though character, illustration/anatomy and writing hands PASS: exactly one phone is clearly on the SAME DESK to the right of laptop, contrary to required separate shelf/location. Single targeted retry on SC05 only is appropriate; do NOT regenerate accepted SC01/SC02. A visible evidence JSON has been generated for download in chat and can be imported via import-chat-review.py to drive bounded retry decision.
- Insight: stronger prompts corrected excess persons and duplicate phones, but complex object-placement instruction still failed. Prefer modifying SC05 composition by moving shelf into distinct plane or controlled image edit, not repeated generic negative prompts. This is candidate review, not final video approval.

## 2026-10-26: SC05 retry runner restored source ZIP support (v3.4)
- Windows run failed before GPU execution because retry-sc05-once.ps1 checked malformed concatenated paths (`imagesSC01_attempt1.png`) instead of `images/SC01_attempt1.png`.
- Fixed path joins and added fallback: recover SC01/SC02/SC05 original attempt1 PNG files from newest `Downloads/MLI_ENGINE_GATE_*.zip` when extracted engine gate folders are unavailable. Only the three named PNG members are extracted to a separate staging directory, preserving originals; only SC05 attempt2 is generated.
- Script committed; no local Windows run yet. Do not state that an image was regenerated until console evidence. Acceptance rate remains only 2/3 in the most recent review, with SC05 spatial phone placement failing.

## 2026-10-26: SC05 targeted second attempt review (v3.5)
- User uploaded MLI_SC05_RETRY_REVIEW.zip. It contained SC01_attempt1.png, SC02_attempt1.png, SC05_attempt1.png, SC05_attempt2.png, prompt and CLI log. New SC05 attempt2 SHA256 0c1afa9df79c554371c2223827f05483ceab9cbf0f5f478f6f50be7a72464a5b.
- Actual visual inspection SC05 attempt2: recognizable protagonist with orange headphones and teal hoodie, writes in notebook with right hand and left hand on desk; exactly one black smartphone upright on physically separate bookshelf at right. Objective phone count/location and basic action criteria PASS.
- Editorial caveat: severe vertical white panel divider divides image into two compositions; not the intended continuous cinematic scene. SC05 is a semantic candidate, not unquestioned editorial approval. Do not blindly regenerate SC05 beyond two attempts; consider alternative composition-controlled rendering later.
- Original SC01/SC02 included in ZIP and not regenerated by this script. Technical filenames alone don't prove byte-for-byte match with the prior acceptance set; verify source provenance when folding into master.
- Production learning: reaching this point required three rounds and multiple script corrections. Measure candidate acceptance after 1st try and quality per wall-time, enforce preflight tests and signed asset manifests before rendering. No final MP4 produced or approved.

## 2026-10-26: Unified local image-production pipeline (v3.6)
- Corrected creative policy: split panels/two vignettes are ALLOWED when motivated by the script. Never call a split-panel composition inherently defective. Scene design, including shot arrangement, is story-driven.
- Added tools/mli-pipeline.py: independent of PowerShell CWD, supports `prepare`, `generate`, `package`, `ingest`, `status` with `--work` state directory. `prepare` reads local shots.json or GitHub content and generates reproducible scene prompts; `generate` uses frozen local sd-cli FLUX backend with two-attempt maximum, never overwrites existing image and only generates UNGENERATED or RETRY_AUTHORIZED shots; `package` creates ZIP with PNGs and scene-specific acceptance criteria; `ingest` validates file names, hashes and evidence-bearing PASS/FAIL/UNCERTAIN, preserving CANDIDATE_PASS states; all snapshots go to state.json. Default status never approves video publication.
- Added tools/run-mli-pipeline.ps1 to fetch fresh script via GitHub REST and run prepare/generate/package in one PowerShell invocation from any directory, output isolated in Downloads/MLI_PIPELINE_timestamp. Defaults to SC01 SC02 SC05 pilot gate; `-Scenes` parameter accepts any known shot IDs from contract. No paid API calls.
- Added tests/test_mli_pipeline.py for no-GPU state/package/hash/retry behavior. Source files committed; **not yet executed against Windows GPU or test environment**. Do not claim QA complete or video pipeline fully integrated. This is the image pipeline; audio, shot timing and renderer integration are still independent.
- Production efficiency: fail closed on uncertain review; accepted assets are not regenerated; after 2 failures block and change method. Composition controls must be explicit in shot contracts, never imposed by arbitrary aesthetic rules. Next practical step: execute unit tests and one complete prepare/generate/chat-review/import round, then integrate release gate with multi-shot renderer.

## 2026-10-26: First unified pipeline GPU review receipt (v3.7)
- User uploaded MLI_PIPELINE_20261026_181922_CHAT_REVIEW.zip with SC01/SC02/SC05 attempt1 PNGs and specific review_request.json. Chat visual evaluation produced MLI_PIPELINE_20261026_CHAT_REVIEW_RESULT.json with exactly six evidence-supported checks per image and hash match to request.
- SC01 CANDIDATE_PASS: recognizable exhausted lead, phone held, hand to temple, laptop; extra people appear but THIS version of SC01 contract does not prohibit them. Extra people may detract editorially; do not silently impose prior prompt constraints that are absent from current contract.
- SC02 FAIL: more than two or three passersby visible, although lead identity/action maintained.
- SC05 FAIL: writing hands correct, but two phones visible on desk, zero on separate shelf; foreground also includes two others despite prior desire for solitary decision. Current JSON contract lacks exact 'no extras' constraint. No automatic editorial ban on multi-panel composition; creative policy remains script-first.
- Result 1/3 first-attempt candidate acceptance (33%). Do NOT trigger automatic 2nd attempts until contract is corrected to include proven scene-specific composition/layout instructions; otherwise second attempts likely repeat known failures. Technical image generation is working, semantic accuracy remains major bottleneck. Review JSON downloadable in conversation; source files on user's PC remain separate.

## 2026-10-26: Persistent composition constraints and review-driven retry (v3.8)
- Canonical pilot shots.json now explicitly includes scene-specific composition requirements: SC01 no extraneous figures or portraits; SC02 exactly three or fewer background pedestrians; SC05 single phone on physically separate shelf with visible gap and optional narratively purposeful panels. Previous learned constraints no longer disappear between runs.
- tools/mli-pipeline.py now includes shot composition in generated prompts and incorporates actual failed-criterion evidence into attempt2 prompts. It continues to preserve accepted scenes, enforce two attempts and keep full-image QC as a separate chat step.
- Both changes committed to GitHub, but have not yet been executed in the user's Windows runtime. No new MP4 or generated images claimed. Further automated testing and complete six-scene acceptance are still required.

## 2026-10-26: Operational image production entrypoint (v3.9)
- New tools/mli-production.ps1 is the single PowerShell entrypoint for `start`, `review`, `status`, `verify` from any CWD. It downloads mli-pipeline.py plus test_mli_pipeline.py directly via GitHub API, runs tests before GPU, creates a run in Downloads, packages first-attempt images for chat; review mode ingests returned JSON, never regenerates candidate-pass images, generates only RETRY_AUTHORIZED shots, repackages and enforces strict review round; verify mode checks all accepted candidates and hashes. The user must explicitly bridge ZIP and JSON with the chat, not a paid API.
- Canonical shots.json now preserves scene composition constraints from historical accepted tests. The Python generator now uses composition field; attempt2 prompt includes evidence of failed criteria. Automatic publication is never asserted. Binary setup still local stable-diffusion.cpp sd-cli, with known frozen Vulkan configuration.
- Added verify command to tools/mli-pipeline.py: checks selected shots candidate-pass, image hashes and review evidence, writes acceptance_gate.json and blocks on any missing/failed item. This is an image gate, not yet a complete voice/edit/render/publish pipeline.
- Source committed, but PowerShell entrypoint has NOT been tested on user's PC yet; run-based tests are the next validation. Avoid promising fully working until live execution returns PASS.

## 2026-10-26: End-to-end connection to narrated pilot renderer (v4.0)
- Extended tools/mli-pipeline.py with `export` command: copies ONLY candidate-pass PNGs with verified SHA256 and review evidence to accepted_images/SCxx.png; refuses incomplete or failed review. Writes accepted_manifest.json.
- tools/mli-production.ps1 now defaults `start` to all six pilot scenes (SC01..SC06) rather than the earlier 3-shot gate; review mode resumes existing run and selectively retries only failed scenes; `render` mode requires all six scenes accepted, calls verify/export, checks existing SC01..SC06.wav and invokes existing build-mli-pilot-enhanced.py using accepted_images. Output is still in Downloads; render status is not audiovisual release approval.
- This is a coherent local production path: prepare -> generate -> ZIP review in chat -> import review JSON -> retry only failed -> verify/export -> narrated MP4. No paid API. Every operation independent of current PowerShell directory; history and images persisted per run.
- IMPORTANT: repository changes committed but automated tests/runtime on the user's Windows PC still pending. The earlier V2 production exposed repeated bugs, so do not assert end-to-end success before unit tests and actual execution. Online sources on stable-diffusion.cpp confirm FLUX.2 editing/reference support and model-specific preprocessing; retaining current proven sd-cli flags rather than changing backend/vae speculatively.

## 2026-10-26: Critical PowerShell launcher bugfix (v4.1)
- User launched mli-production.ps1 and PowerShell parser failed before execution on `"Missing WAV for $sid: $audio"`; `$sid:` is not valid PowerShell variable syntax. Fixed to `${sid}:`.
- Also fixed `RunPipeline @(...)` and `RunPipeline (...)` argument calls to explicit `RunPipeline -argList @(...)` so the full argument vector reaches the Python subprocess. This could otherwise cause subsequent launch errors.
- Refetched updated script from GitHub and checked patched content. No PowerShell runtime/actual GPU test performed in this environment. User must rerun same main bootstrap command; no images or run folder were created by the original parse failure.

## 2026-10-26: Six-scene production QA receipt (v4.2)
- Received and inspected MLI_PIPELINE_20261026_201214_CHAT_REVIEW.zip with all six PNGs and review_request.json. All six SHA256 hashes matched the request. Created MLI_PIPELINE_20261026_201214_REVIEW.json for ingest with all six criteria per image and visible evidence.
- SC01 CANDIDATE_PASS: exhausted lead alone at desk, phone in hand. SC04 CANDIDATE_PASS: narratively useful side-by-side composition, hands in pockets and phone apart on parapet. Split panels allowed; don't reject them as a matter of style.
- SC02 FAIL: more than 3 supporting pedestrians and shop-window figures. SC03 FAIL: right-hand panel shows lead holding phone, contrary to required phone on cafe table. SC05 FAIL: phone appropriately on separate shelf but upright with visibly illuminated screen rather than lying screen down. SC06 FAIL: garbled speech bubbles, and only protagonist clearly holds mug, whereas both characters should hold mugs.
- First pass scene-specific acceptance 2/6. Full video release remains blocked. Import review JSON into exact run folder MLI_PIPELINE_20261026_201214 to trigger at most one second attempt for ONLY SC02, SC03, SC05 and SC06; SC01 and SC04 MUST remain unchanged. Inspect next ZIP before rendering.

## 2026-10-26: Narrative-first acceptance correction (v4.3)
- Earlier rejection 4/6 was a strict literal-prompt compliance score, NOT a meaningful editorial failure rate. User correctly challenged excessive failures. New policy docs/image-acceptance-rubric.md: blockers = story contradiction, character drift, serious anatomy, distracting text/artifacts; minor count/angle details nonblocking; prefer localized repair for generated gibberish text; split panels are fine when narratively useful.
- Reassessment: SC01 ACCEPT, SC02 ACCEPT despite pedestrian count, SC03 requires narrative review of held phone, SC04 ACCEPT, SC05 ACCEPT because phone is away from desk, SC06 prefer localized repair of illegible speech bubbles and evaluate human interaction. Do NOT execute old import report blindly: it would trigger unnecessary GPU retries.
- This is an editorial decision-policy change; legacy Python ingest currently uses FAIL on any criterion. It needs migration to severity-tagged acceptance before automatic retries can be trusted.

## 2026-10-27: Safe recovery after Windows reboot (v4.4)
- User halted interrupted `mli-production.ps1 -Mode review` on run `Downloads/MLI_PIPELINE_20261026_201214` after SC02 attempt2 and during SC03 attempt2. Existing review had marked SC01 and SC04 CANDIDATE_PASS; SC02/03/05/06 RETRY_AUTHORIZED under old overstrict rubric. Actual completion states after reboot unknown; do NOT assume SC03 finished.
- Implemented `recover` in tools/mli-pipeline.py and `-Mode recover` in tools/mli-production.ps1: inspect run/ images and state without GPU, recover intact untracked PNG attempt records with hashes, quarantine corrupt/untracked PNG, verify hashes of recorded assets, place obsolete RETRY_AUTHORIZED states on REVIEW_POLICY_HOLD. Writes `recovery_report.json`. Does not run generation, restart old retries or overwrite accepted images.
- Added no-GPU regression tests for untracked valid PNG recovery and obsolete retry holding. Committed, but must still be run in user's Windows context. Standard launcher downloads current code and runs tests before recovery.
- Next step: user runs safe -Mode recover command using exact run folder; inspect resulting states and adopt narrative-first acceptance without regenerating merely for pedestrian counts or phone angle. Do NOT import old stricter JSON again. Assess SC03 and SC06 for story-critical defects, repair only if required. Full rendering is not yet approved.

## 2026-10-27: Recovery editorial re-evaluation (v4.5)
- User supplied MLI_RECOVERED_REVIEW.zip. Contains seven PNGs: original attempt1 SC01..SC06 and SC02_attempt2; state matches Windows recovery receipt. Images visually inspected under narrative-first rubric. SC01, SC02 attempt1, SC03, SC04, SC05 usable; SC06 has illegible invented speech/text and needs localized text cleanup, not full-scene regeneration. SC02 attempt2 is technically valid but not a narrative improvement.
- Created image-hash-bound editorial decision JSON in chat. Added `adopt` to tools/mli-pipeline.py: validates complete set of scene decisions and each asset SHA256 against recorded attempts, selects earlier attempt where better, saves state with CANDIDATE_PASS or LOCAL_REPAIR, blocks release until repair. Export and verify prefer editorial-selected attempt. No GPU needed for adoption.
- Do not reject split panels per se; prioritize comprehensible narrative. Full release still blocked on SC06 text cleanup and final audiovisual QC. Do not run old 4-scene retry report.

## 2026-10-27: SC06 localized cleanup path (v4.6)
- User confirmed editorial adoption: SC01..SC05 CANDIDATE_PASS, SC06 LOCAL_REPAIR, no publication approval. Prepared chat-exported localized SC06 candidate from original SC06_attempt1.png: removed invented balloon lettering and hoodie lettering without FLUX; picture keeps original triple-panel cartoon but a blank dialogue balloon persists. Image requires final human viewing and may still be editorially inferior to a professionally redrawn version; do not call this final approval.
- Added `repair-import --work --scene SC06 --image <path>` to tools/mli-pipeline.py; validates image PNG/hash, requires LOCAL_REPAIR, preserves original, writes SC06_repaired.png and provenance into state; selected asset is used by verify/export. No GPU.
- Existing tools/build-mli-pilot-enhanced.py accepts `--images-dir` with SC01.png..SC06.png, WAVs from local pilot_audio and produces a reviewable narrated MP4 in Downloads. Render is not a release gate and audiovisual QC remains necessary.

## 2026-10-27: First pilot finishing edit produced in chat (v4.7)
- User supplied narrated pilot ZIP `MLI_PILOT_001_20261027_062750.zip`; six original per-scene MP4s and final master verified. Edited only SC06: selected the existing lower-right conversational vignette from the already accepted source and reframed to 768x432 to omit blank speech balloon; does not regenerate with FLUX. Result SC06 still shows teal hoodie and interpersonal engagement but orange headphones are not visible in this subpanel. User must evaluate creative acceptability before final signoff.
- Re-rendered SC06 clip with FFmpeg and source clip audio copied, reused original SC01–SC05 clips unchanged, concatenated to `MLI_PILOT_001_FINAL_REVIEW.mp4`, output duration 37.042 s; full decode succeeded. Mean audio -17.8 dB, peak -1.8 dB. Measured inter-scene silences ~0.64-0.71 s including embedded source audio silence; retained original pacing, not automatically changed. Existing scene-level estimated SRT preserved externally.
- Delivered sandbox files `MLI_PILOT_FINAL_REVIEW/MLI_PILOT_001_FINAL_REVIEW.mp4` and `MLI_PILOT_001_FINISHING_REVIEW.zip` with MP4, SC06 crop, SRT, QC_REPORT.json. This is local chat product only; NOT imported to Windows run state, not committed as binary to GitHub, not yet user editorial-approved/published. No speech recognition/forced subtitle alignment or listening-based narration proof was performed.
- Next step: user watches new MP4, approves or identifies exact issues; only then mark editorial complete and create reproducible local edit procedure. Avoid falsely claiming full production system automation from this one-off chat edit.

## 2026-10-27: Reusable post-render technical QC (v4.8)
- User rated pilot acceptable overall but SC06 remains creatively unsatisfactory. Do not mark editorial approved or published. Continue hardening the workflow rather than regenerating blindly.
- Added tools/mli-qc.py: verifies six source MP4 clips, master video/audio streams and 1080p dimensions, duration consistency, FFmpeg full master decode, SRT and manifest; writes technical_qc.json with distinct technical_pass, editorial_approved and publication_approved flags (latter two never automatically true). No GPU or paid services.
- Added `-Mode qc -RenderFolder` to tools/mli-production.ps1 so quality control can run independently on original render folder from any CWD. The chat-produced finishing ZIP does not include six original segments, so QC targets original render folder, not finishing ZIP.
- Remaining work: improve SC06 without losing character identity, upgrade estimated SRT timing to proven transcript alignment, manual audiovisual acceptance and reusable final-cut/repair integration. Do not claim fully automatic production system complete on strength of technical checks alone.

## 2026-10-27: Reusable final-cut workflow with word-level local alignment (v5.0)
- User requested three changes: SC06 with retained protagonist identity, word-aligned subtitles from real narration, and reproducible final edits. Added `tools/mli-align.py`, `tools/mli-finish.py`, `tests/test_mli_finishing.py`; launcher `-Mode finish -RenderFolder <old folder> -Scene06Image <approved PNG>`.
- Alignment uses local WhisperX phoneme forced alignment on six existing WAVs with the canonical narrator text from `build-mli-pilot-enhanced.py`; returns word timestamps, strict failure if any word lacks timing, outputs `MLI_PILOT_001_CAPTIONS_ALIGNED.srt` and `alignment.json`; does not substitute estimated timestamps or run transcription in place of canonical text. Requires separate local `python -m pip install whisperx` and first-use model downloads; no paid API. Windows CPU model alignment compatibility/performance not yet proven.
- Finisher preserves SC01-SC05 rendered segment videos without re-encode (copies), explicitly substitutes one selected SC06 still over original SC06 audio, combines clips and burns aligned captions via ffmpeg/libass. Writes result in a new timestamped Downloads folder and final_manifest.json; does NOT auto-approve publication.
- Fast isolated tests added for SRT timestamp/grouping/scene coverage and wired into launch preflight, alongside existing tests. Integration not yet run on user's Windows and no claim that final MP4 generated.
- Creative SC06 attempt through image-generation looks appealing but protagonist face is too detailed and deviates from canonical minimal-face design; NOT accepted as source until actual character fidelity verified. Do not silently swap. Existing crop also has identity weakness due missing headphones. Need an approved new or edited SC06 image to finish creatively.
- External verification: WhisperX documented word-level alignment (m-bain/whisperX); stable-diffusion.cpp FLUX.2 reference mode flux2 can edit, but does not guarantee character consistency. Further production work: validate forced alignment on user PC; smoke-test final rendering/FFmpeg subtitle support, assess revised SC06 visually, then run final technical QC.

## 2026-10-27: Isolated alignment bootstrap and final-cut integration (v5.1)
- Added tools/setup-and-align.ps1 to check exact six WAV+MP4 inputs and ffmpeg, use isolated Python 3.11 venv in Downloads/MLI_WHISPERX_ENV, install CPU-compatible PyPI whisperx only when absent, download current mli-align.py and source builder, perform forced alignment without modifying existing estimated SRT. Models may download on first run; no paid API or GPU required.
- Corrected tools/mli-production.ps1 -Mode finish so alignment runs using isolated WhisperX venv rather than system Python. It still needs explicitly chosen approved SC06 image, existing render folder, and FFmpeg with subtitle/libass support.
- SC06 experimental generated replacement has stylistic/identity drift and is NOT automatically approved. The user needs either an acceptable image-based edit consistent with pale minimal face/headphones, or a creative decision about one compromise; do not claim SC06 closed. Word alignment and final-cut not yet executed on user PC; await local bootstrap output before claim.

## 2026-10-27: Python version detection fix (v5.2)
- User ran setup-and-align.ps1; Windows Python launcher reported no Python 3.11 runtime. WhisperX never installed/aligned; existing WAV/render state unaffected.
- Confirmed stable WhisperX 3.8.6 requires Python >=3.10,<3.14 (PyPI). Updated setup-and-align.ps1 to discover Python 3.11,3.12,3.13,3.10 via `py`, or compatible `python` command, and create isolated virtualenv without assuming 3.11. On no compatible runtime, fail explicitly and ask for Python version inspection instead of installing a duplicate blindly.
- Script remains untested on user's host. Next launch should fetch fresh script and complete installation/alignment or reveal next concrete blocker. Creative SC06 and finishing render still pending.

## 2026-10-27: WhisperX installation and alignment validated on user's Windows (v5.3)
- User supplied complete setup log. Existing Python 3.12 discovered; separate Downloads/MLI_WHISPERX_ENV venv created. WhisperX 3.8.6 installed successfully and imported, CPU acoustic model wav2vec2 base 360MB downloaded. Aligned exactly 106 words into 19 captions; generated aligned SRT path Downloads/MLI_PILOT_001_20261027_062750/MLI_PILOT_001_CAPTIONS_ALIGNED.srt and alignment.json. Do not reinstall or repeat alignment unnecessarily.
- Updated tools/mli-production.ps1 -Mode finish to reuse existing alignment.json/SRT rather than repeat forced-alignment. Checks 6 scenes and >50 word timestamps before final edit. Final cut still not executed on user system; SC06 identity/creative approval remains pending. Previous SC06 local-crop candidate may be used ONLY to test render, not approval.

## 2026-10-27: Branded subtitle style comparisons (v5.5)
- Produced 3 nine-second sample videos in chat from the actual clean master: cinematic (white), amber (channel colour emphasis), soft karaoke (progressive amber). Demonstration only: ZIP supplied SRT but no alignment.json; preview per-word timings interpolated within SRT segments and are NOT evidence of final accuracy. Do not misrepresent these as true word-aligned renders.
- Added tools/mli-caption-styles.py to GitHub: generates cinematic.ass, amber.ass with selected keyword emphasis, and karaoke.ass using actual WhisperX alignment.json with word timestamps. Local ASS generation via standard Python, no paid services. Use FFmpeg libass for final burn. Production script not yet wired to chosen style; user should select after preview. Correctness and native Windows final render not yet verified.

## 2026-10-27: Soft Karaoke selected as standard captions (v5.6)
- User selected Soft Karaoke as the canonical subtitle style for Modern Life Inc. Existing tools/mli-caption-styles.py generates word-level ASS from alignment.json. Do not use the interpolated SRT demo for final production.
- Updated tools/mli-finish.py: requires original WhisperX alignment.json and caption generator, produces MLI_CAPTIONS.ass, burns its word-level karaoke styling using FFmpeg/libass, preserves SRT export and records caption_style in final_manifest.json. Default caption style is karaoke; cinematic and amber still supported as explicit alternatives. Updated tools/mli-production.ps1 -Mode finish to download caption generator and forward `-CaptionStyle`, default karaoke, and word-alignment path. No new GPU or TTS.
- Source committed but freshly changed karaoke final render not yet executed on user's Windows; next test must validate karaoke motion, actual word timing, and FFmpeg libass output. SC06 remains editorially pending; prior selected repaired candidate usable as technical fixture only, not creative approval.

## 2026-10-27: Karaoke readability stabilization and next-scale gate (v5.7)
- User approved Soft Karaoke and requested final stabilization before going longer. Existing caption generator already had MarginV=135, semantic/punctuation grouping, short-caption merge, and <=2-line splitting, so changes focus on strengthening rather than restyling.
- Improved tools/mli-caption-styles.py two-line split selection using 38-character target per line and explicit >=2 words on either side; tightened word time validation for non-finite/negative stamps. Removed six-scene-only restriction in caption ASS CLI to allow arbitrary episode-scene counts (other pilot-specific stages still explicitly require six scenes).
- Added regression checks for split balance, scene boundary and retained original margin tests in tests/test_mli_finishing.py. Fixed tools/mli-production.ps1 preflight to fetch mli-caption-styles.py before executing tests, including from cold TEMP.
- These changes are committed, but final Windows render with revised ASS has NOT been validated yet; user should rerun existing finish pipeline once and inspect. No GPU, WhisperX re-alignment, image or voice regeneration needed.
- Recommended next step: a deliberate 2-3 minute narrative integration pilot (not yet full 8-12 minute episode), using reusable story beats, scene-to-scene character consistency, narrator duration budget, timing, QC and sustainable generation-cost tracking. Only scale further once 2-3 minute pilot passes full editorial and technical gates. Current pipeline has several hardcoded SC01-SC06 and pilot file names, so generalize contracts/render/technical QC before attempting longer episode. SC06 creative defect is still unapproved and must be resolved independently.

## 2026-10-27: EP002 scaling experiment scaffold (v5.8)
- Created episodes/MLI_EP002/shots.json with 18 beats and 302 narration words (~2m10s at 140 wpm without pauses), titled "Who Owns Your Attention?". Explicit canonical character reference and no-dialogue-bubble rules. Creative DRAFT, not GPU approved.
- Added -Mode plan -Episode MLI_EP002 to tools/mli-production.ps1: downloads the episode contract from GitHub and invokes prepare with --shots. Creates prompts and state without GPU use.
- Important limits: start, render, build-mli-pilot-enhanced.py and mli-qc.py still assume six pilot scenes; never use those on EP002 until generalized. Next phases: dynamic scene-count renderer and audio alignment, scene-agnostic QC, measured GPU generation in small batches.
- Soft Karaoke was stabilized with margin 135 and balanced two-line grouping; latest Windows render still unverified.

## 2026-10-27: EP002 planning operational refinement (v5.9)
- Fixed malformed intermediate PowerShell launcher plan insertion and restored original start block; checked rendered source around branches. Removed duplicated caption file preflight download.
- Updated tools/mli-pipeline.py prepare: writes narration_draft.txt and planning_summary.json with actual scene count, word count, estimated speaking seconds at 140 wpm, planned duration range and explicit GPU not used/release not approved. Works for other shot contracts passed by --shots.
- Plan mode downloads 18-shot MLI_EP002 contract into TEMP and initializes a separate timestamped Downloads run; it does NOT generate, render or publish assets. Still needs Windows runtime smoke test and editorial review, then dynamic rendering/voice/QC generalization before GPU operation.

## 2026-10-27: Preflight and broken launcher repair (v6.0)
- User tried `-Mode plan -Episode MLI_EP002` and got ParserError at line 112. Inspected live GitHub file: trailing duplicate malformed block after initial launcher end; removed tail after primary status fallback. Root cause was corrupt source commit, NOT a missing Windows dependency. Avoid claiming smoke-tested on user PC.
- Added mode-scoped Preflight to launcher: Python availability/version for all stages; ffmpeg+ffprobe for GPU render/final/qc; FLUX executable, identity reference and model files for start; pilot narration WAV for render; alignment SRT, word timestamps and explicit SC06 file for finish. Checks avoid starting unneeded heavy dependencies during plan and fail with concrete missing file. Unit tests continue after preflight.
- Plan still only produces 18 prompts, 302-word narrator draft and summary, without GPU. Next immediate step is fetch + PowerShell ParseFile validation before invocation, then local success output. Full dynamic 18-scene narrator/render/qc and staged GPU generation still pending.

## 2026-10-27: Python runtime selection fix (v6.2)
- User diagnosed `python` command resolving to C:\Python314\python.exe (Python 3.14.0) while Python 3.12 exists under AppData Local Programs. Previous preflight incorrectly blocked on default PATH interpreter despite suitable existing runtime.
- Updated tools/mli-production.ps1 preflight to collect interpreter candidates from PATH and Windows `py` launcher, prefer compatible 3.12 among alternatives, and reuse selected interpreter for unit tests, main pipeline, finishing, rendering and QC. Existing checks remain aggregate-report style, not fail-fast. No Python installation or WhisperX reinstallation needed.
- This selection code is committed but awaiting Windows execution verification. Be careful when altering launcher; protect against duplicate source tails and parse failures.

## 2026-10-27: EP002 planned locally, variable-scene render and QC added (v6.3)
- User ran -Mode plan -Episode MLI_EP002 successfully at 2026-10-27 18:28:25. Preflight selected installed Python 3.12; 5 pipeline unit tests and 8 finishing tests passed. Created C:\Users\ralba\Downloads\MLI_EP002_PIPELINE_20261027_182825 with 18 scenes and no GPU use.
- Added tools/mli-render-episode.py: renders variable scene counts from contract.json, accepted_images and WAVs in <work>/audio, concatenates a clean episode master and emits manifests; no image or voice generation, no release approval.
- Added tools/mli-qc-episode.py: scene-agnostic MP4 codec/stream/duration/hash/decode verification against render manifest; publication remains blocked.
- Launcher now exposes -Mode episode-render -Work <work> and -Mode episode-qc -RenderFolder <render>, while preserving pilot-specific commands. Source committed but NOT yet locally tested on Windows; no WAVs/images for EP002 have been generated or accepted. More work needed on narration voice generation, generalized word alignment and final Soft Karaoke burn in variable-scene exports. Do not run episode-render until all accepted images and per-scene WAVs are ready.

## 2026-10-27: Pipeline-wide EP002 postproduction stages (v6.4)
- User requested all production activities be integrated into single pipeline with comprehensive phase-appropriate preflight. Added tools/mli-audio-episode.py: writes voice_jobs.json and audio_audit.json, checks all 18 WAVs with hash/duration/mono PCM format, never stops at first missing file, returns incomplete status without generating voice.
- Added tools/mli-align-episode.py: local WhisperX word-level alignment using canonical beat texts from work/contract.json, scene order and clip timeline from render manifest, dynamic scene count. Outputs alignment.json and captions_words.srt. Does NOT use estimated fallback.
- Added tools/mli-finish-episode.py: uses actual word timing to burn standard Soft Karaoke ASS over clean episode MP4 and record finishing_manifest.json, preserves original master.
- Added tools/mli-qc-episode.py checks for Soft Karaoke final video, valid audio, SHA256, ASS/alignment sidecars, full FFmpeg decode (when finishing manifest exists) while retaining clean-master checks and publication_approved false.
- Extended launcher mli-production.ps1 with modes episode-audio, episode-render (existing), episode-final and episode-qc; episode-final chains align->burn->QC. Added episode preflight for work/contract/state, final render folder and WhisperX environment. Added tests/test_mli_episode_stages.py (18-scene karaoke and scene boundaries) in preflight. Fixed episode-qc to require only render folder.
- Important honest limit: VoiceStudio voice synthesis has not been API/CLI-integrated. Pipeline produces a complete per-scene voice job manifest and verifies WAVs, but missing WAVs remain blocking, not silently synthesized. Requires investigation/validation of real locally installed VoiceStudio interface and access. No GPU images or WAVs generated for EP002; newly added episode stages committed but not yet exercised on user Windows; do not claim full operability. The final episode still needs editorial approval.
