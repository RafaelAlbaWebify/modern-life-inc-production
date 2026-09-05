# Session Protocol

## Start
Read `.ai/CONTEXT.md`, `PROJECT_STATE.json`, `KNOWN_ISSUES.md`, `OPERABILITY.md`, then inspect Git status/commit.

## During
Bound changes to the active milestone. Preserve contracts. Update tests/QC. Record durable decisions/issues/rejections. Do not claim completion without evidence.

## End
Update `.ai/PROJECT_STATE.json`, `TEST_STATUS.json`, `KNOWN_ISSUES.md`, and roadmap/decisions/rejections/operability if changed. Then run:

`powershell -ExecutionPolicy Bypass -File "C:\ModernLifeInc\tools\sync_project_state.ps1" -Push`

A chat ending must not cause state loss.
