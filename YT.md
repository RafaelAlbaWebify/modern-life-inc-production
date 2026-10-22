# YT.md — Modern Life Inc. execution guardrails

Version: 1.0 (2026-10-22)
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
