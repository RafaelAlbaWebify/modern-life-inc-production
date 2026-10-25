# Modern Life Inc — Deterministic production contract (proposed v0.1)

Status: **design proposal, not yet experimentally validated**. Built after V1/V2 pilot postmortem, 2026-10-25.

## Fundamental shift
One video = script -> event-based shot list -> structured visual contracts -> scene prompts -> images -> automated validation + bounded retries -> fixed voice -> duration-aligned assembly -> editorial acceptance.

Do **not** equate one narration paragraph with exactly one image or add zoom to every still. There are six narration chunks but as many *meaningful shots* as the story requires.

## Shot record (JSON)
- id, scene_id, narration_beat (verbatim text portion), narrative_purpose, composition (wide/medium/close/over-shoulder), subjects, primary_action, required_props, forbidden_props, identity_refs, supporting_character_policy, eyeline, emotion_as_visible_behavior, shot_duration_strategy, optional camera_action with justification, engine_settings, seed.
- Example SC05:
  - Scene: protagonist writing priority list at desk.
  - Hands: pen in RIGHT hand; left hand resting on notebook. **No phone in either hand.**
  - Phone: screen down on a separate shelf, at least forearm's length away.
  - Required: visible notebook and pen, protagonist's orange headphones and teal hoodie.
  - Reject if phone is held or face drifts.
- Example SC06:
  - Protagonist turned toward supporting friend, mutual eye contact, gentle relaxed smile, hands around cup, phone not visible; secondary is a normally featured stylized face, not the lead's iconic simplified face.
  - Reject if protagonist looking at floor/phone.

## Reproducible assets and limits
- Protagonist character sheet: reference with front, profile, seated and upper-body versions; approved banner/avatar is the ultimate identity source. Do not equate provisional cropped SC01 with a full turnaround sheet.
- Style sheet: linework, color palette, lighting and framing. Supporting cast have conventional simplified human facial features, visibly distinct from icon-face lead.
- Engine settings and reference hashes stored per-shot so reruns are traceable.
- FLUX.2 Klein 4B on GTX1060 3GB is a baseline; do not promise hard prop-position adherence or reliable identity. If repeated failure, simplify composition, edit only offending region if tool supports it, or compare a stronger engine on the same shot. Do NOT blindly add more prompt text.
- Use a small fixed evaluation panel of 3 shots: lead alone, lead with two supporting characters, hand/phone on table with exact spatial constraints. Test each engine with same specs and seeds where meaningful, scoring identity, prop accuracy, layout, style, speed and failures. Decide on data, not reputation.
- Generation has a retry budget (e.g. 2 attempts per shot). If both fail, flag for human/art-director choice; don't silently consume endless generation cycles.

## Gate separation
1. **Narrative gate**: script coherence, hook, beat and shot-list coverage, supporting characters where meaningful.
2. **Asset gate**: correct character, hand-object relationships, secondary faces, scene-specific required and forbidden attributes. Machine checks can catch dimensions/missing files; visual semantic check requires image-capable reviewer or targeted detection; do not claim perfect automatic validation.
3. **Audio gate**: existing working VoiceStudio profile, verify each WAV and non-silence; no research detour.
4. **Assembly gate**: per-WAV durations, only specified camera movement, controlled subtitle alignment, output outside repo in Downloads.
5. **Delivery gate**: verify actual final MP4 and subjective playthrough, then publish only with approval.

## Architectural next implementation
- `episodes/<episode>/shots.json` = single source of truth for shots, dialogue beat, identity, props and editing.
- `tools/plan-shots.py` validates schema, beat coverage, naming, referential integrity and emits model-oriented prompts; no image generation until plan passes.
- `tools/generate-shots.ps1` batches model calls, saves prompts/seeds/logs, respects bounded retry; later phase.
- `tools/validate-shots.py` measures technical metadata, records human semantic QC separately, never fabricates pass/fail.
- `tools/render-episode.py` consumes `shots.json`, existing voice clips, optional captions/music; no hard-coded six images and no generic motion.
- Run full pilot only after a 3-shot acceptance test. Then freeze engine/prompt config for production episodes; reopen only on real regression.
