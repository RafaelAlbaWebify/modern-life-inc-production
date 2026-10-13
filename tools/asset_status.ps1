param([string]$Episode = "episodes/MLI-001")
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Push-Location $Root
try {
    $log = Get-Content -LiteralPath (Join-Path $Episode "asset_review_log.json") -Raw | ConvertFrom-Json
    $manifest = Get-Content -LiteralPath (Join-Path $Episode "production_manifest.json") -Raw | ConvertFrom-Json
    $rows = foreach ($scene in $manifest.scenes) {
        if ($scene.visual_mode -eq "SYSTEM") { continue }
        $path = Join-Path $Episode $scene.base_image
        $asset = $log.assets.PSObject.Properties[$scene.id].Value
        [pscustomobject]@{
            Scene = $scene.id
            Mode = $scene.visual_mode
            Review = $asset.status
            Present = (Test-Path -LiteralPath $path -PathType Leaf)
            Path = $path
        }
    }
    $rows | Format-Table Scene,Mode,Review,Present -AutoSize
    $ready = @($rows | Where-Object { $_.Present -and $_.Review -in @("locked","approved") }).Count
    $missing = @($rows | Where-Object { -not $_.Present }).Count
    Write-Host "[SUMMARY] ready-approved=$ready / 32; missing-local=$missing; review-needed=$(@($rows | Where-Object { $_.Review -notin @('locked','approved') }).Count)"
    if ($missing -gt 0) { Write-Host "[GATE] Strict final render blocked; placeholders are not acceptable in a publishable cut." }
}
finally { Pop-Location }
