param(
    [string]$Episode = "episodes/MLI-001"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$EpisodePath = Join-Path $Root $Episode
$Python = "python"

& $Python (Join-Path $Root "tools\retime_storyboard_to_narration.py") --episode $EpisodePath
if ($LASTEXITCODE -ne 0) {
    throw "Storyboard retiming failed with exit code $LASTEXITCODE."
}

& $Python (Join-Path $Root "tools\build_production_manifest.py") --episode $EpisodePath
if ($LASTEXITCODE -ne 0) {
    throw "Production manifest rebuild failed with exit code $LASTEXITCODE."
}

Write-Host "[PASS] Storyboard and production manifest synchronized to narration." -ForegroundColor Green
