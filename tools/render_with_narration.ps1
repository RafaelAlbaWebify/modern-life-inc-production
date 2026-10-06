param(
    [string]$Episode = "episodes/MLI-001",
    [string]$Audio = ""
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot

Push-Location $Root
try {
    if (-not $Audio) {
        $Audio = Join-Path $Episode "media\narration.wav"
    }

    if (-not (Test-Path -LiteralPath $Audio)) {
        throw "Narration file not found: $Audio"
    }

    python .\tools\validate_audio.py --audio $Audio
    python .\tools\build_production_manifest.py --episode $Episode
    python .\renderer\render_episode.py --episode $Episode --allow-placeholders --audio $Audio --output output\rough_cut_with_voice.mp4

    $Out = Join-Path $Root "$Episode\output\rough_cut_with_voice.mp4"
    if (-not (Test-Path -LiteralPath $Out)) {
        throw "Expected output not created: $Out"
    }

    Write-Host "[PASS] Rough cut with narration created:" -ForegroundColor Green
    Write-Host $Out
}
finally {
    Pop-Location
}
