param(
    [string]$Episode = "episodes/MLI-001",
    [int]$StartAt = 1,
    [int]$MaxAttempts = 2,
    [int]$TimeoutSec = 240,
    [switch]$Force,
    [switch]$NoAssemble
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot

Push-Location $Root
try {
    $ManifestPath = Join-Path $Episode "narration_chunks.json"
    if (-not (Test-Path -LiteralPath $ManifestPath)) {
        throw "Narration manifest not found: $ManifestPath"
    }

    $Manifest = Get-Content -LiteralPath $ManifestPath -Raw | ConvertFrom-Json
    $ChunksDir = Join-Path $Episode "media\narration_chunks"
    $NarrationOut = Join-Path $Episode "media\narration.wav"
    New-Item -ItemType Directory -Force -Path $ChunksDir | Out-Null

    try {
        $Info = Invoke-RestMethod "http://127.0.0.1:3900/system/info" -TimeoutSec 10
        Write-Host "[READY] VoiceStudio $($Info.app_version) on $($Info.device)" -ForegroundColor Green
    }
    catch {
        throw "VoiceStudio backend is not reachable on http://127.0.0.1:3900. Start VoiceStudio first."
    }

    $Ffmpeg = $Info.ffmpeg_path
    if (-not $Ffmpeg -or -not (Test-Path -LiteralPath $Ffmpeg)) {
        throw "VoiceStudio FFmpeg was not found: $Ffmpeg"
    }

    $Selected = @($Manifest.chunks | Where-Object { [int]$_.id -ge $StartAt })
    if ($Selected.Count -eq 0) {
        throw "No chunks selected. StartAt=$StartAt"
    }

    foreach ($Chunk in $Selected) {
        $Id = [string]$Chunk.id
        $Out = Join-Path $ChunksDir ("chunk-{0}.wav" -f $Id)

        if ((Test-Path -LiteralPath $Out) -and -not $Force) {
            Write-Host "[SKIP] $Id already exists" -ForegroundColor DarkGray
            continue
        }

        $Succeeded = $false
        for ($Attempt = 1; $Attempt -le $MaxAttempts; $Attempt++) {
            Write-Host "[GEN] $Id ($($Chunk.section)) attempt $Attempt/$MaxAttempts" -ForegroundColor Cyan
            try {
                $Temp = "$Out.part"
                Remove-Item -LiteralPath $Temp -Force -ErrorAction SilentlyContinue

                Invoke-WebRequest `
                    -Uri "http://127.0.0.1:3900/generate" `
                    -Method Post `
                    -TimeoutSec $TimeoutSec `
                    -Form @{
                        text       = [string]$Chunk.text
                        language   = [string]$Manifest.language
                        instruct   = [string]$Manifest.instruct
                        engine     = [string]$Manifest.engine
                        num_step   = "16"
                        speed      = "1.0"
                    } `
                    -OutFile $Temp

                if (-not (Test-Path -LiteralPath $Temp)) {
                    throw "VoiceStudio returned without creating audio."
                }

                $Size = (Get-Item -LiteralPath $Temp).Length
                if ($Size -lt 4096) {
                    throw "Generated WAV is unexpectedly small ($Size bytes)."
                }

                Move-Item -LiteralPath $Temp -Destination $Out -Force
                Write-Host "[PASS] $Id -> $Out" -ForegroundColor Green
                $Succeeded = $true
                break
            }
            catch {
                Remove-Item -LiteralPath "$Out.part" -Force -ErrorAction SilentlyContinue
                Write-Warning "Chunk $Id failed: $($_.Exception.Message)"
                if ($Attempt -lt $MaxAttempts) {
                    Start-Sleep -Seconds 3
                }
            }
        }

        if (-not $Succeeded) {
            throw "Chunk $Id failed after $MaxAttempts attempts. Stop here; rerun later with -StartAt $([int]$Id)."
        }

        Start-Sleep -Milliseconds 750
    }

    if ($NoAssemble) {
        Write-Host "[DONE] Chunk generation complete; assembly skipped." -ForegroundColor Green
        return
    }

    $Missing = @()
    foreach ($Chunk in $Manifest.chunks) {
        $ChunkPath = Join-Path $ChunksDir ("chunk-{0}.wav" -f $Chunk.id)
        if (-not (Test-Path -LiteralPath $ChunkPath)) {
            $Missing += $Chunk.id
        }
    }
    if ($Missing.Count -gt 0) {
        throw "Cannot assemble narration. Missing chunks: $($Missing -join ', ')"
    }

    $ConcatPath = Join-Path $ChunksDir "concat.txt"
    $ConcatLines = foreach ($Chunk in $Manifest.chunks) {
        "file 'chunk-$($Chunk.id).wav'"
    }
    Set-Content -LiteralPath $ConcatPath -Value $ConcatLines -Encoding utf8

    Push-Location $ChunksDir
    try {
        & $Ffmpeg -y -f concat -safe 0 -i "concat.txt" -c:a pcm_s16le -ar 24000 -ac 1 "..\narration.wav"
        if ($LASTEXITCODE -ne 0) {
            throw "FFmpeg concat failed with exit code $LASTEXITCODE."
        }
    }
    finally {
        Pop-Location
    }

    if (-not (Test-Path -LiteralPath $NarrationOut)) {
        throw "Expected narration was not created: $NarrationOut"
    }

    Write-Host "[PASS] Final narration created:" -ForegroundColor Green
    Write-Host (Resolve-Path -LiteralPath $NarrationOut)
}
finally {
    Pop-Location
}
