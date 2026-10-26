# Run from any PowerShell location. Fresh MLI image pipeline: prepare > generate > package.
param([string[]]$Scenes=@("SC01","SC02","SC05"),[string]$Work="")
$ErrorActionPreference="Stop";$ProgressPreference="SilentlyContinue"
if(-not $Work){$Work=Join-Path $HOME ("Downloads\MLI_PIPELINE_"+(Get-Date -Format "yyyyMMdd_HHmmss"))}
$uri="https://api.github.com/repos/RafaelAlbaWebify/modern-life-inc-production/contents/tools/mli-pipeline.py?ref=main"
$res=Invoke-RestMethod -Uri $uri -Headers @{"Accept"="application/vnd.github+json";"Cache-Control"="no-cache"}
$dest=Join-Path $env:TEMP "mli-pipeline.py"
[IO.File]::WriteAllBytes($dest,[Convert]::FromBase64String(($res.content -replace '\s','')))
if(-not (Select-String -LiteralPath $dest -SimpleMatch -Pattern 'CANDIDATE_PASS' -Quiet)){throw "Pipeline download failed integrity preflight"}
Write-Host "PREFLIGHT AND PREPARE" -ForegroundColor Cyan
& python $dest prepare --work $Work --scenes @Scenes
if($LASTEXITCODE -ne 0){throw "Prepare failed"}
Write-Host "GENERATE" -ForegroundColor Cyan
& python $dest generate --work $Work
if($LASTEXITCODE -ne 0){throw "Generate failed"}
Write-Host "PACKAGE FOR CHAT" -ForegroundColor Cyan
& python $dest package --work $Work
if($LASTEXITCODE -ne 0){throw "Package failed"}
& python $dest status --work $Work
Write-Host "RUN: $Work" -ForegroundColor Green
Write-Host "UPLOAD ZIP: $($Work)_CHAT_REVIEW.zip" -ForegroundColor Green
