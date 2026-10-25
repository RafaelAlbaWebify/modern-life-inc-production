# YT.md — Modern Life Inc. execution guardrails

Version: 1.1 (2026-10-25)
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
