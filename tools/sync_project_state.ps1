param(
    [string]$Root = "C:\ModernLifeInc",
    [switch]$Push
)
$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath (Join-Path $Root ".git"))) { throw "Not a Git repository: $Root" }

$Builder = Join-Path $Root "tools\build_ai_context.ps1"
if (Test-Path -LiteralPath $Builder) {
    & powershell -ExecutionPolicy Bypass -File $Builder -Root $Root
    if ($LASTEXITCODE -ne 0) { throw "AI context refresh failed." }
}

& git -C $Root fetch origin --prune
if ($LASTEXITCODE -ne 0) { throw "git fetch failed." }

$Branch = (& git -C $Root branch --show-current).Trim()
$RemoteRef = "origin/$Branch"
$Counts = (& git -C $Root rev-list --left-right --count "$RemoteRef...$Branch").Trim()
$Behind = 0; $Ahead = 0
if ($Counts -match '^\s*(\d+)\s+(\d+)\s*$') {
    $Behind = [int]$Matches[1]
    $Ahead = [int]$Matches[2]
}
if ($Behind -gt 0) {
    throw "Local branch is behind $RemoteRef by $Behind commit(s). Review/pull before continuing."
}

# Guard GitHub's practical limit.
$Danger = Get-ChildItem -LiteralPath $Root -Recurse -File -Force -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch '\\.git\\' -and $_.Length -ge 95MB }
if ($Danger) {
    Write-Host "[STOP] Files >=95 MB:" -ForegroundColor Red
    $Danger | ForEach-Object { Write-Host ("  {0:N1} MB  {1}" -f ($_.Length/1MB), $_.FullName) }
    exit 2
}

# Canonical project state only. Working/temp/render binaries remain ignored.
$Canonical = @(
    ".ai",".gitignore",".gitattributes",
    "00_admin\docs","00_admin\registries","00_admin\sync\DUAL_SYSTEM_POLICY.md",
    "docs","tools","engine",
    "episodes\MLI-001\01_research","episodes\MLI-001\02_script",
    "episodes\MLI-001\03_audio\VOICEBOX_NOVA_INPUT.txt",
    "episodes\MLI-001\04_storyboard",
    "episodes\MLI-001\05_scenes",
    "episodes\MLI-001\07_packaging","episodes\MLI-001\08_qc"
)
foreach ($Rel in $Canonical) {
    if (Test-Path -LiteralPath (Join-Path $Root $Rel)) {
        & git -C $Root add -- $Rel
        if ($LASTEXITCODE -ne 0) { throw "Failed staging $Rel" }
    }
}

$Staged = @(& git -C $Root diff --cached --name-only)
if ($Staged.Count -gt 0) {
    & git -C $Root commit -m "chore: sync canonical project state $(Get-Date -Format yyyy-MM-dd)"
    if ($LASTEXITCODE -ne 0) { throw "commit failed" }
}

if ($Push) {
    & git -C $Root push origin $Branch
    if ($LASTEXITCODE -ne 0) { throw "push failed" }
    & git -C $Root fetch origin --prune | Out-Null
}

$Commit = (& git -C $Root rev-parse HEAD).Trim()
$Status = @(& git -C $Root status --porcelain)
$Counts = (& git -C $Root rev-list --left-right --count "origin/$Branch...$Branch").Trim()
Write-Host ""
Write-Host "[PASS] Modern Life Inc. canonical sync complete." -ForegroundColor Green
Write-Host "Branch : $Branch"
Write-Host "Commit : $Commit"
Write-Host "Remote delta (behind ahead): $Counts"
Write-Host "Working tree changes: $($Status.Count)"
