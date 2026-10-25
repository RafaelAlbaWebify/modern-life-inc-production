# YT.md — Modern Life Inc. execution guardrails

Version: 2.4 (2026-10-25)
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
