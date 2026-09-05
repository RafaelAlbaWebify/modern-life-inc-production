param([string]$Root = "C:\ModernLifeInc")
$ErrorActionPreference = "Stop"
$Ai = Join-Path $Root ".ai"
$StatePath = Join-Path $Ai "PROJECT_STATE.json"
$State = Get-Content -LiteralPath $StatePath -Raw | ConvertFrom-Json
$Branch = (& git -C $Root branch --show-current).Trim()
$Commit = (& git -C $Root rev-parse HEAD).Trim()
$StatusLines = @(& git -C $Root status --porcelain)
$Status = if ($StatusLines.Count -eq 0) { "clean" } else { $StatusLines -join "`n" }
$Origin = (& git -C $Root remote get-url origin 2>$null)

if (-not $State.git) { $State | Add-Member -NotePropertyName git -NotePropertyValue ([pscustomobject]@{}) }
$State.git | Add-Member -NotePropertyName available -NotePropertyValue $true -Force
$State.git | Add-Member -NotePropertyName branch -NotePropertyValue $Branch -Force
$State.git | Add-Member -NotePropertyName current_commit -NotePropertyValue $Commit -Force
$State.git | Add-Member -NotePropertyName origin -NotePropertyValue $Origin -Force
$State.git | Add-Member -NotePropertyName status_at_snapshot -NotePropertyValue $Status -Force
$State.last_update_date = Get-Date -Format "yyyy-MM-dd"
$State | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $StatePath -Encoding UTF8

$Snapshot = @"
# AI Context Snapshot
Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss K")
Branch: $Branch
Commit: $Commit
Origin: $Origin
Milestone: $($State.current_milestone)
Operability: $($State.operability_percentage)%
Production ready: $($State.readiness.production_ready)

## Blockers
$((@($State.current_blockers) | ForEach-Object { "- $_" }) -join "`n")

## Next
$((@($State.next_recommended_actions) | ForEach-Object { "- $_" }) -join "`n")
"@
$Snapshot | Set-Content -LiteralPath (Join-Path $Ai "AI_CONTEXT_SNAPSHOT.md") -Encoding UTF8
Write-Host "[PASS] AI context refreshed: $Commit" -ForegroundColor Green
