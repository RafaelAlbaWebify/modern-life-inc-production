param([string]$Remote = "gdrive")
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Target = Join-Path $Root "episodes/MLI-001/media/generated"
$Assets = [ordered]@{
 S001 = "1qHa2U8QUU9zvH6i6kAjaiNs6NjxAQcf2"
 S007 = "1r6nxuqBhwgp8TH2SffGYofrLdXXEDzOd"
 S017 = "1spz7rR3EaNs8whhg_byP0uPctNrAMCzF"
 S023 = "1ZaYwtKoYdWnK2DkAsiDnjwWNrmUtNu_9"
 S027 = "1r9iiBEqZXMjU5vN0aMBp2HJnZL0_-H3O"
 S032 = "12g4xgGNWmq7NJTvS1yZ46mW7XvWiufff"
 S037 = "1KMZq345UCp8yFSMBDFQ7CR26nqeIX_8w"
 S054 = "1pd7Tlu4cvEAjiTZ8hLs50g7R5K2lydx9"
}
if (-not (Get-Command rclone -ErrorAction SilentlyContinue)) {
 throw "rclone is required. Install once: winget install Rclone.Rclone ; restart PowerShell."
}
$Remotes = @(rclone listremotes)
if ($LASTEXITCODE -ne 0) { throw "rclone remote query failed" }
if ("$($Remote):" -notin $Remotes) {
 Write-Host "One-time Google OAuth configuration required; create remote named '$Remote' with storage type 'drive'."
 rclone config
 if ($LASTEXITCODE -ne 0) { throw "rclone config failed" }
 $Remotes = @(rclone listremotes)
 if ("$($Remote):" -notin $Remotes) { throw "Remote '$Remote' not configured" }
}
New-Item -ItemType Directory -Path $Target -Force | Out-Null
$Downloaded = 0
foreach ($Id in $Assets.Keys) {
 $Destination = Join-Path $Target "$Id.png"
 if (Test-Path -LiteralPath $Destination) {
    $Bytes = [System.IO.File]::ReadAllBytes($Destination)
    if ($Bytes.Length -gt 8 -and [System.Convert]::ToHexString($Bytes[0..7]) -eq "89504E470D0A1A0A") {
        Write-Host "[SKIP] $Id is already present (PNG)"
        continue
    }
    throw "Existing local file is not a valid PNG: $Destination (will not overwrite)"
 }
 $Temp = Join-Path $Target "$Id.download.png"
 if (Test-Path -LiteralPath $Temp) { Remove-Item -LiteralPath $Temp -Force }
 & rclone backend copyid "$($Remote):" $Assets[$Id] $Temp
 if ($LASTEXITCODE -ne 0) { throw "Drive download failed for $Id" }
 if (-not (Test-Path -LiteralPath $Temp)) { throw "Download missing for $Id" }
 $Bytes = [System.IO.File]::ReadAllBytes($Temp)
 if ($Bytes.Length -le 8 -or [System.Convert]::ToHexString($Bytes[0..7]) -ne "89504E470D0A1A0A") {
   throw "Invalid PNG downloaded for $Id"
 }
 Move-Item -LiteralPath $Temp -Destination $Destination
 $Downloaded++
 Write-Host "[PASS] $Id installed ($( [math]::Round($Bytes.Length / 1MB,2) ) MiB)"
}
Write-Host "[PASS] 8 locked assets available; $Downloaded downloaded this run"
