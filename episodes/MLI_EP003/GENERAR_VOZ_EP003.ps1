param([string]$Work = (Join-Path $HOME 'Downloads\MLI_EP003_AUDIO_V1'))
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$revision = '1947ecca7f60d82cd110c0f91b1ca3d4a02ab766'
$repository = 'RafaelAlbaWebify/modern-life-inc-production'
$started = [DateTimeOffset]::UtcNow
$clock = [Diagnostics.Stopwatch]::StartNew()
$python = (Get-Command python -ErrorAction Stop).Source
New-Item -ItemType Directory -Force -Path $Work | Out-Null
$toolFolder = Join-Path $Work 'tools'
New-Item -ItemType Directory -Force -Path $toolFolder | Out-Null
function Get-RepoBytes([string]$Path) {
    $uri = "https://api.github.com/repos/$repository/contents/$($Path)?ref=$revision"
    $response = Invoke-RestMethod -Uri $uri -Headers @{Accept='application/vnd.github+json'}
    return [Convert]::FromBase64String(($response.content -replace '\s',''))
}
$contract = Join-Path $Work 'contract.json'
$bytes = Get-RepoBytes 'episodes/MLI_EP003/shots.json'
$incomingHash = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($bytes))
if (Test-Path -LiteralPath $contract) {
    if ((Get-FileHash -LiteralPath $contract -Algorithm SHA256).Hash -ne $incomingHash) {
        throw 'Existing work has a different script. Use a new -Work folder; existing audio was preserved.'
    }
} else { [IO.File]::WriteAllBytes($contract, $bytes) }
foreach ($name in @('mli-voicestudio-tts.py','mli-audio-episode.py')) {
    [IO.File]::WriteAllBytes((Join-Path $toolFolder $name), (Get-RepoBytes "tools/$name"))
}
$failure = $null
try {
    Write-Host 'VoiceStudio debe estar abierto, con OmniVoice y Modern Life Narrator v1 disponibles.'
    Write-Host '48 segmentos. Se conservan y reutilizan los WAV ya generados en esta carpeta.'
    & $python (Join-Path $toolFolder 'mli-voicestudio-tts.py') --work $Work --mode smoke
    if ($LASTEXITCODE -ne 0) { throw 'First voice segment failed. See voice_production_report.json.' }
    # The canonical narrator was already accepted for production in EP002.
    # This batch still needs complete listening review before publication.
    & $python (Join-Path $toolFolder 'mli-voicestudio-tts.py') --work $Work --mode batch --approved
    if ($LASTEXITCODE -ne 0) { throw 'Voice batch interrupted. Successful files retained; rerun this script to resume.' }
    & $python (Join-Path $toolFolder 'mli-audio-episode.py') --work $Work
    if ($LASTEXITCODE -ne 0) { throw 'Audio audit failed.' }
} catch { $failure = $_.Exception.Message }
$clock.Stop()
$timing = [ordered]@{episode='MLI_EP003';started_utc=$started.ToString('o');finished_utc=[DateTimeOffset]::UtcNow.ToString('o');elapsed_seconds=$clock.Elapsed.TotalSeconds;success=($null -eq $failure);error=$failure;revision=$revision;publication_approved=$false}
$timing | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $Work 'local_voice_timing.json') -Encoding utf8
$items = @('contract.json','audio','voice_production_report.json','audio_audit.json','local_voice_timing.json','voice_history') | ForEach-Object { Join-Path $Work $_ } | Where-Object { Test-Path -LiteralPath $_ }
$zip = Join-Path (Split-Path -Parent $Work) ('MLI_EP003_AUDIO_' + (Get-Date -Format 'yyyyMMdd_HHmmss_fff') + '.zip')
Compress-Archive -LiteralPath $items -DestinationPath $zip
Write-Host "Paquete de voz: $zip"
Write-Host ('Tiempo local medido: {0:N1} minutos' -f ($clock.Elapsed.TotalMinutes))
if ($failure) { throw $failure }
Write-Host '48 voces verificadas tecnicamente. Comparte el ZIP para continuar el montaje; revision auditiva pendiente.'
