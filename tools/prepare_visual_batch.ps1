param(
    [string]$Episode = "episodes/MLI-001",
    [int]$Size = 4,
    [ValidateSet("HERO","HYBRID")]
    [string]$Mode = ""
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$EpisodePath = Join-Path $Root $Episode

$ArgsList = @(
    (Join-Path $Root "tools\prepare_visual_batch.py"),
    "--episode", $EpisodePath,
    "--size", [string]$Size
)
if ($Mode) {
    $ArgsList += @("--mode", $Mode)
}

python @ArgsList
if ($LASTEXITCODE -ne 0) {
    throw "Visual batch preparation failed with exit code $LASTEXITCODE."
}
