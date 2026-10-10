param(
    [string]$Episode = "episodes/MLI-001"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$EpisodePath = Join-Path $Root $Episode

python (Join-Path $Root "tools\check_visual_assets.py") --episode $EpisodePath
exit $LASTEXITCODE
