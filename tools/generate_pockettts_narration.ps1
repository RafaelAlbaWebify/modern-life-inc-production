param(
    [string]$Episode = "episodes/MLI-001",
    [string]$Reference = "",
    [int]$StartAt = 1,
    [int]$EndAt = 0,
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

$ArgsList = @(
    (Join-Path $Root "tools\generate_pockettts_narration.py"),
    "--episode", (Join-Path $Root $Episode),
    "--config", $ConfigPath,
    "--start-at", [string]$StartAt
)

if ($EndAt -gt 0) {
    $ArgsList += @("--end-at", [string]$EndAt)
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
