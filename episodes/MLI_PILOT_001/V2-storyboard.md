# MLI_PILOT_001 — V2 scene direction (2026-10-25)

Status: **candidates, not accepted / not rendered**. Existing voice remains unchanged. V2 images 1672x941, six individual images, staged through a ZIP uploaded in conversation; **not verified in Drive**.

| Scene | Narrative beat | Visual | Secondary character | QC |
| --- | --- | --- | --- | --- |
| SC01 | Incoming requests overwhelm | Desk, many notification bubbles | None | Notifications are fictional visual metaphors, not actual UI |
| SC02 | Pressure follows you everywhere | City pavement while staring at phone | Several urban passersby with ordinary stylized faces | Check distinct faces, visual continuity |
| SC03 | Others live while protagonist stays distracted | Cafe, cup, reflective pose | People talking/working in background | Voice text is about expected availability, not cafe specifically |
| SC04 | Put phone down; breathe | Rooftop at sunset; phone off to protagonist's side | None | New phone position differs from previous SC04; avoid old automatic camera target |
| SC05 | Decide priorities | Writing at desk | None | **Phone still in hand**: known contradiction, candidate only |
| SC06 | Boundaries allow presence and connection | Sofa and relaxed conversation, cat | Friend with normal stylized face | Support character emotional expression should not outshine lead |

**Canon character**: pale minimal face (oval eyes), messy dark hair, large orange headphones, teal hoodie, dark trousers. Secondary faces are normally drawn (eyes/nose/mouth), within same illustration style and less visually dominant.

**Editing rule**: no obligatory zoom/pan. Static default; only purpose-designed movements on a narrative beat. Legacy rooftop zoom SC04 is **disabled when --images-dir is supplied**. No fresh narration or model generation needed to evaluate these V2 images.

**Local render**: unzip all six SC01.png..SC06.png to `$HOME\Downloads\MLI_PILOT_001_V2_IMAGES`. Use tools/build-mli-pilot-enhanced.py with `--images-dir "$HOME\Downloads\MLI_PILOT_001_V2_IMAGES"`. Existing WAVs remain at `C:\AI\MLI-FluxTest-Vulkan\pilot_audio`. Outputs in `$HOME\Downloads\MLI_PILOT_001_<timestamp>`. Render should be inspected for image fit, narration timing, engagement, and cover-to-cover edit; MP4 not yet rendered.
