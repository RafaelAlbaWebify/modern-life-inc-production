# Publication pipeline

The final MP4 is followed by a publication-package stage. Package preparation/checking never uploads, schedules, posts a comment, changes channel settings or publishes. Positive video feedback is recorded separately from permission to release a specific title/thumbnail on a specific channel.

## Stages

1. Lock the final video and technical-QC hash. Preserve the accepted film; do not rerender for metadata changes.
2. Prepare a truthful title and complementary thumbnail. Inspect full size and mobile size; no fabricated CTR/SEO scores. Use the approved channel character. Freeze source/provenance and selected files.
3. Write a unique description, research credits where relevant, chapter labels mapped to the measured render timeline, a pinned-comment draft and relevant tags. Do not insert nonexistent URLs, shops or playlists.
4. Export English phrase-level SRT from verified real word alignment using the existing caption grouper. Burned-in karaoke does not replace a separately uploaded caption track. The sidecar preserves actual timing; no estimated words.
5. Confirm the actual upload account, target visibility/schedule, intended audience, AI-use disclosure including narrator provenance, promotion/rights and monetization eligibility. These remain explicit Studio decisions, not inferred account facts. Tags are secondary metadata, not an SEO guarantee.
6. Upload privately when instructed, attach thumbnail/SRT, select real playlist and preview chapters/end-screen placement. Check platform processing/checks. A proposed end screen may be omitted if it obscures faces/captions or lacks an appropriate destination.
7. Publish/schedule only under explicit user instruction for the concrete package. Independently verify the actual URL and visible title/thumbnail/audio/captions, then record the publication receipt. Posting the pinned comment also requires authorization.
8. Review comparable-age analytics (24h/72h/7d when available): impressions, CTR, first-30-second retention, average minutes viewed, traffic and subscribers; revenue only if available. These checkpoints do not create automations.

## Canonical commands

```powershell
& $script -Mode episode-publish-prepare -Work $work -RenderFolder $render -PublishPlan $plan -PublishFolder $package
& $script -Mode episode-publish-check -PublishFolder $package
```

Python equivalents:

```text
python tools/mli-publish-package.py prepare --work WORK --render-folder RENDER --plan PLAN.json --out NEW_EMPTY_PACKAGE
python tools/mli-publish-package.py check --out PACKAGE
```

Use a new empty output directory so revisions preserve prior files. The plan format is `MLI_PUBLISH_PLAN_V1`; concrete EP003 plan lives in `episodes/MLI_EP003/publication/publish_plan.json`. Stage its referenced thumbnail beside it. The exporter checks final video hash, QC, episode/transcript alignment, metadata lengths, real chapter timing and thumbnail file. The checker detects modified package files. It reports assets ready for review, never release authorization. No YouTube API call exists in this module.

Output: title.txt, description.txt, thumbnail, phrase SRT, chapters.json, pinned_comment.txt, proposed YouTube settings/end-screen plan, publication checklist, post-publication guide and hashed package receipt. Video source is referenced by path/hash rather than duplicated. Keep the separately delivered final MP4.

## Current platform guidance checked 29 October 2026

- Title: up to 100 characters; description including chapters: up to 5,000. https://support.google.com/youtube/answer/57404
- Chapters start 00:00, have at least three entries and spans of at least 10s. Account feature availability still applies. https://support.google.com/youtube/answer/9884579
- YouTube currently recommends larger thumbnail sources; limits vary by upload surface. Our conservative portable output profile is 1280x720 JPEG/PNG, near 16:9 and <=2MiB, not a claim that all desktop uploads are limited to 2MiB. https://support.google.com/youtube/answer/72431
- End screens use the final 5–20s and need placement preview. https://support.google.com/youtube/answer/6388789
- Unrealistic drawn scenes alone do not require the same disclosure as realistic fabricated events; examine actual narration and current AI-use field. Do not automatically infer disclosure from tool brand. https://support.google.com/youtube/answer/14328491

## Website and merchandise — deferred

User decision, 29 October 2026: validate the YouTube channel first. Website creation, domain purchase, shop/merch setup and episode-card preparation are postponed. Focus on published videos, audience response and a sustainable production cadence. No numeric traction threshold is agreed; revisit only with evidence and an explicit user decision. The following reference architecture is historical/future context, not an active work order.

The channel's confirmed reference is Beanie Survives: https://www.beaniesurvives.com/ . It links story episodes to YouTube, routes short parts to Instagram/TikTok and merchandise checkout to Printify. This is a reference for distribution architecture, not permission to copy characters, artwork, text or products.

For Modern Life Inc., a later owned hub can list episodes by relationships/work/money/biases with real YouTube links, brief synopses, channel links and contact. A shop is a separate optional business task requiring an actual provider/catalogue, pricing, fulfillment and user approval; it never blocks a video. Do not create a website, connect a store, buy a domain or publish placeholder offers merely because this pipeline mentions them. Only after this expansion is explicitly reopened, prepare episode-card records from verified video IDs/URLs. Cross-platform excerpts remain optional, separately reviewed assets.


## Windows launch convention (v7.15)

For downloaded unsigned MLI scripts, do not present Unblock-File followed by direct invocation as the complete universal solution. Unblock-File only removes the downloaded-file marker; it does not remove an AllSigned requirement.

Launch a reviewed script in a separate PowerShell process with a process-only policy:

```powershell
& (Get-Process -Id $PID).Path -NoProfile -ExecutionPolicy Bypass -File "$HOME\Downloads\ALINEAR_EP004.ps1"
```

Use the current host executable to preserve PowerShell version/runtime. Substitute the actual script path and forward its normal arguments. This does not persist a CurrentUser/LocalMachine policy change and needs no administrator session. Keep normal script checks, WAV reuse and real alignment guards.

Offer a companion .cmd launcher beside downloaded .ps1 files; canonical pipeline companion is tools/mli-production.cmd. The companion selects installed PowerShell 7 and invokes only its adjacent known script with -NoProfile -ExecutionPolicy Bypass, preserving exit code. It does not download/execute arbitrary remote code.

MachinePolicy/UserPolicy Group Policy settings take precedence. If the process-only launch is still blocked, request Get-ExecutionPolicy -List and diagnose; do not claim the exact effective policy from the error alone, override organization policy, or recommend repeated Unblock-File, model reinstall, or global unrestricted policies. An internal self-relaunch cannot solve a script blocked before its first line executes.

Reference: https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_execution_policies
