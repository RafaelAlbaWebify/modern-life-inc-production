# Chat image production in the MLI pipeline

## Supported boundary

The integrated ChatGPT image tool is the preferred image producer for EP002. The assistant invokes it inside the conversation, supplies actual references, inspects every output and supplies real output files. PowerShell does not invoke this built-in tool. No separate paid API or user API key is used by these commands. Availability must be checked rather than assumed; never promise unlimited batches.

`contract.json` must select `image_generation_backend: chat_image_edit`. Local FLUX generation is then blocked. Existing local contracts are snapshots and are not silently migrated by updating GitHub. Preserve source contract/state/voice hashes when preparing a revised run; V2 is an independent run, not an overwrite of the original.

## 1. Prepare frozen jobs

From the existing launcher:

```powershell
& $script -Mode episode-chat-export -Work $work
# Optional explicit subset:
& $script -Mode episode-chat-export -Work $work -Scenes SC02,SC09
```

This writes `chat_image_jobs.json` with contract digest, per-scene prompt and its digest, narration, layout, previous failed visual evidence, and the reference path/hash when available. Omitting `-Scenes` means every scene in the episode, not the six-scene pilot default. It does not generate images, use a GPU, or transmit media. Attach the jobs plus the actual character/style references and source images needed for edits.

The assistant creates/edits separate complete scenes with the integrated image tool. Default is one continuous 16:9 composition. Multiple panels require explicit per-scene layout and a real narrative rationale. Review the whole sequence for repetitive composition, not only individual image checklists. Do not over-police harmless detail variations.

## 2. Return files and an import manifest

Return real PNG files and `image_manifest.json` in one extracted folder. Manifest format:

```json
{
  "format": "MLI_CHAT_IMAGES_V1",
  "episode": "MLI_EP002",
  "contract_sha256": "<exact digest from jobs>",
  "images": [{
    "scene": "SC02",
    "file": "SC02.png",
    "sha256": "<measured PNG hash>",
    "prompt_sha256": "<exact frozen source prompt digest from jobs>",
    "producer": "chat_imagegen",
    "source_artifact": "<actual generated output reference, not an invented URL>"
  }]
}
```

`prompt_sha256` links to the frozen scene prompt; job review corrections and reference inputs also inform the tool call. This is not a claim that the model received only that literal text. New imports require frozen jobs; do not manufacture retroactive job evidence for V2 assets created before this importer existed. Their existing revision receipts remain historical evidence.

## 3. Import and review

```powershell
& $script -Mode episode-chat-import -Work $work -Review "C:\absolute\image_manifest.json"
```

Before modifying any selection, the importer verifies episode, contract, requested scenes, current/frozen prompt hashes, image paths within the bundle, PNG dimensions and hashes, and declared producer/source reference. It accepts higher-resolution near-16:9 PNGs without forced downscaling. It backs up state and manifest, preserves originals, archives superseded exported copies, and writes an import receipt. A repeated identical import reuses files and does not create another attempt. Imported changes become `NEEDS_REVIEW`; prior acceptance is not carried onto a replacement image.

The launcher creates a normal chat review ZIP when images are pending. Existing `review` / `adopt`, `verify` and `export` remain the acceptance mechanisms. A chat-backed FAIL requests `CHAT_REVISION_REQUIRED` and exports only the rejected scene jobs, with failed visual evidence; it never launches FLUX. Two failed chat image candidates block further blind retries. Uncertainty remains blocking. Technical upload success is not editorial approval.

After accepted images and existing voices pass their gates, use `episode-render`, `episode-qc` and `episode-final` as before. Preserve valid voice WAVs and real alignment where the timeline/text/audio match. Final human screening and publication approval remain separate.

## Validation and limits

Python regression tests cover hashes, stale prompts/contracts, directory escape, idempotence, invalidation of old selections, preserved original exports, review-required imports and capped chat revision routing. PowerShell launcher additions have source inspection but require actual Windows execution; do not claim that wrapper exercised by the Python suite. No new image generation is required to test export/import.
