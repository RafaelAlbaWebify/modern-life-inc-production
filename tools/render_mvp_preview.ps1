param(
    [string]$Episode = "episodes/MLI-001",
    [int]$Limit = 6
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot

Push-Location $Root
try {
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        throw "Python is not available on PATH."
    }
    if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
        throw "FFmpeg is not available on PATH."
    }

    python -m pip install -r requirements.txt
    python .\renderer\render_episode.py --episode $Episode --limit $Limit --output output\mvp_preview.mp4

    $Out = Join-Path $Root "$Episode\output\mvp_preview.mp4"
    if (-not (Test-Path -LiteralPath $Out)) {
        throw "Expected preview not created: $Out"
    }

    Write-Host "[PASS] Production MVP preview created:" -ForegroundColor Green
    Write-Host $Out
}
finally {
    Pop-Location
}
