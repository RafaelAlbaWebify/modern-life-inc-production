param([Parameter(Mandatory=$true)][string]$DownloadedFolder)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Target = Join-Path $Root "episodes/MLI-001/media/generated"
$Required = @("S001","S007","S017","S023","S027","S032","S037","S054")
if (-not (Test-Path -LiteralPath $DownloadedFolder -PathType Container)) { throw "Missing downloaded folder: $DownloadedFolder" }
New-Item -ItemType Directory -Path $Target -Force | Out-Null
$Installed = 0
foreach ($Id in $Required) {
    $Files = @(Get-ChildItem -LiteralPath $DownloadedFolder -Recurse -File | Where-Object { $_.Name -eq "$Id.png" })
    if ($Files.Count -ne 1) { throw "Expected exactly one $Id.png in $DownloadedFolder; found $($Files.Count)" }
    $Destination = Join-Path $Target "$Id.png"
    Copy-Item -LiteralPath $Files[0].FullName -Destination $Destination -Force
    $Info = Get-Item -LiteralPath $Destination
    if ($Info.Length -le 0) { throw "Empty image: $Destination" }
    $Installed++
    Write-Host "[PASS] $Id -> $Destination"
}
Write-Host "[PASS] Installed $Installed approved/locked images; 24 photographic scenes remain outside this approved set."
