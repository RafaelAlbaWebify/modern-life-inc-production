param(
    [string]$Episode = "episodes/MLI-001",
    [string]$Audio = ""
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot

Push-Location $Root
try {
    python -m pip install -r requirements.txt
    python .\tools\build_production_manifest.py --episode $Episode

    $Args = @(
        ".\renderer\render_episode.py",
        "--episode", $Episode,
        "--allow-placeholders",
        "--output", "output\rough_cut.mp4"
    )
    if ($Audio) {
        $Args += @("--audio", $Audio)
    }

    python @Args

    $Out = Join-Path $Root "$Episode\output\rough_cut.mp4"
    if (-not (Test-Path -LiteralPath $Out)) {
        throw "Expected rough cut not created: $Out"
    }

    Write-Host "[PASS] Full rough cut created:" -ForegroundColor Green
    Write-Host $Out
}
finally {
    Pop-Location
}
