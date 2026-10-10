param(
    [string]$Episode = "episodes/MLI-001",
    [string]$Reference = "",
    [int]$StartAt = 1,
    [int]$EndAt = 0,
    [string]$Only = "",
    [switch]$Force,
    [switch]$NoAssemble
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$ConfigPath = Join-Path $Root "config\voice_production.json"

if (-not (Test-Path -LiteralPath $ConfigPath)) {
    throw "Voice production config not found: $ConfigPath"
}

$Config = Get-Content -LiteralPath $ConfigPath -Raw | ConvertFrom-Json
$Python = [Environment]::ExpandEnvironmentVariables([string]$Config.engine.python_path)

if (-not (Test-Path -LiteralPath $Python)) {
    throw "VoiceStudio Python not found: $Python"
}

# VoiceStudio may recreate/sync its runtime after reboot and drop optional extras.
# Self-heal PocketTTS before starting narration production.
& $Python -c "import pocket_tts" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "[REPAIR] PocketTTS missing from VoiceStudio runtime. Restoring..." -ForegroundColor Yellow

    $Uv = "C:\Program Files\VoiceStudio\resources\tools\uv.exe"
    if (-not (Test-Path -LiteralPath $Uv)) {
        throw "VoiceStudio uv was not found: $Uv"
    }

    $VSRoot = Split-Path -Parent (Split-Path -Parent $Python)

    & $Uv sync --project $VSRoot --extra pockettts
    if ($LASTEXITCODE -ne 0) {
        throw "Automatic PocketTTS restore failed."
    }

    & $Python -c "import pocket_tts"
    if ($LASTEXITCODE -ne 0) {
        throw "PocketTTS is still unavailable after automatic restore."
    }

    Write-Host "[READY] PocketTTS restored." -ForegroundColor Green
}
else {
    Write-Host "[READY] PocketTTS import OK." -ForegroundColor Green
}

$ArgsList = @(
    (Join-Path $Root "tools\generate_pockettts_narration.py"),
    "--episode", (Join-Path $Root $Episode),
    "--config", $ConfigPath,
    "--start-at", [string]$StartAt
)

if ($EndAt -gt 0) {
    $ArgsList += @("--end-at", [string]$EndAt)
}
if ($Only) {
    $ArgsList += @("--only", $Only)
}

if ($Reference) {
    $ArgsList += @("--reference", $Reference)
}
if ($Force) {
    $ArgsList += "--force"
}
if ($NoAssemble) {
    $ArgsList += "--no-assemble"
}

& $Python @ArgsList
if ($LASTEXITCODE -ne 0) {
    throw "PocketTTS narration generation failed with exit code $LASTEXITCODE."
}
