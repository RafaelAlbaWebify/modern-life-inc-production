# Architecture

```text
Research -> Script -> VoiceBox/Nova narration
                  -> Visual beats -> Authored scenes
Approved atomic assets ----------^
Authored scenes + narration -> Python/FFmpeg renderer -> QC -> Packaging -> Publish
```

## Modules
1. Editorial/research
2. Asset library
3. Scene authoring
4. Renderer/build
5. QC/integration

## Renderer boundary
The renderer may translate, scale-pop, rotate slightly, hide/show, swap pose/state, hard-cut, mux audio, and produce QC artifacts. It must not invent layout or storytelling.

## Persistence model
- `C:\ModernLifeInc` = active local production workspace.
- GitHub = versioned authoritative source/history.
- `.ai/` = canonical AI project memory.
- Local-only working assets/renders remain excluded until approved/promoted.
