param([string]$Root = "C:\ModernLifeInc")
$ErrorActionPreference = "Stop"

$Ai = Join-Path $Root ".ai"
$StatePath = Join-Path $Ai "PROJECT_STATE.json"
if (-not (Test-Path -LiteralPath $StatePath)) { throw "Missing $StatePath" }

$State = Get-Content -LiteralPath $StatePath -Raw | ConvertFrom-Json
$Branch = (& git -C $Root branch --show-current).Trim()
$Commit = (& git -C $Root rev-parse HEAD).Trim()
$Origin = (& git -C $Root remote get-url origin 2>$null).Trim()
$StatusLines = @(& git -C $Root status --porcelain)
$Status = if ($StatusLines.Count -eq 0) { "clean" } else { $StatusLines -join "`n" }

$Ahead = "unknown"
$Behind = "unknown"
& git -C $Root fetch origin --prune 2>$null | Out-Null
if ($LASTEXITCODE -eq 0) {
    $RemoteRef = "origin/$Branch"
    & git -C $Root rev-parse --verify $RemoteRef *> $null
    if ($LASTEXITCODE -eq 0) {
        $Counts = (& git -C $Root rev-list --left-right --count "$RemoteRef...$Branch").Trim()
        if ($Counts -match '^\s*(\d+)\s+(\d+)\s*$') {
            $Behind = [int]$Matches[1]
            $Ahead = [int]$Matches[2]
        }
    }
}

$Snapshot = @"
# AI Context Snapshot

Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss K")

## Live Git provenance
- Branch: $Branch
- Commit: $Commit
- Origin: $Origin
- Ahead: $Ahead
- Behind: $Behind
- Working tree: $(if ($Status -eq "clean") { "clean" } else { "dirty" })

```
$Status
```

## Project state
- Phase: $($State.current_phase)
- Milestone: $($State.current_milestone)
- Overall completion: $($State.overall_completion_percentage)%
- Operability: $($State.operability_percentage)%
- Testing: $($State.testing_percentage)%
- Production ready: $($State.readiness.production_ready)
- Publishable episode ready: $($State.readiness.publishable_episode_ready)

## Blockers
$((@($State.current_blockers) | ForEach-Object { "- $_" }) -join "`n")

## Next actions
$((@($State.next_recommended_actions) | ForEach-Object { "- $_" }) -join "`n")

## Provenance rule
The live Git values above are authoritative. `.ai/PROJECT_STATE.json` intentionally does not persist its own containing commit SHA.
"@

$Snapshot | Set-Content -LiteralPath (Join-Path $Ai "AI_CONTEXT_SNAPSHOT.md") -Encoding UTF8
Write-Host "[PASS] AI context snapshot refreshed: $Commit" -ForegroundColor Green
