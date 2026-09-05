# Modern Life Inc. — Dual Local + GitHub Policy

## Principle

LOCAL = active production workspace  
GITHUB = versioned authoritative source/history

## GitHub-authoritative
Track and commit:
- `.ai/`
- architecture / roadmap / decisions / issues / operability state
- renderer/build scripts
- config and templates
- research and script text
- scene JSON / manifests
- approved asset registry
- approved reusable source assets when reasonably sized
- selected small reference artifacts when useful

## Local-authoritative / not normally committed
Keep local:
- raw image-generation outputs before approval
- temporary render frames
- transient contact sheets
- test MP4 renders
- large intermediates
- discarded experiments
- temporary exports
- working assets not yet approved

## Promotion rule
An asset or scene should move from `working` to `approved` only when:
1. visually inspected;
2. semantically atomic if reusable;
3. consistent with current visual grammar;
4. referenced by a current scene/manifest or intentionally retained;
5. approved for reuse.

## Session-end protocol
1. Refresh `.ai` deterministic context.
2. Inspect Git status.
3. Check oversized files.
4. Review untracked files.
5. Commit canonical state changes.
6. Push when requested.
7. Confirm local branch vs remote branch status.

Never use GitHub as a dumping ground for every generated render.
