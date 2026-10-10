param(
    [string]$Episode = "episodes/MLI-001",
    [string]$Batch = "",
    [string]$Model = $env:OPENAI_IMAGE_MODEL
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$EpisodePath = Join-Path $Root $Episode

if (-not $Batch) {
    $ReviewRoot = Join-Path $EpisodePath "media\generated\_review"
    $Latest = Get-ChildItem $ReviewRoot -Directory -Filter "batch_*" |
        Sort-Object Name -Descending |
        Select-Object -First 1

    if (-not $Latest) {
        throw "No visual batch found under $ReviewRoot"
    }

    $Batch = Join-Path $Latest.FullName "batch_manifest.json"
}

$ArgsList = @(
    (Join-Path $Root "tools\generate_visual_batch.py"),
    "--episode", $EpisodePath,
    "--batch", $Batch
)

if ($Model) {
    $ArgsList += @("--model", $Model)
}

python @ArgsList
if ($LASTEXITCODE -ne 0) {
    throw "Visual generation failed with exit code $LASTEXITCODE."
}
