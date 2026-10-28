param(
    [string]$AudioWork = (Join-Path $HOME 'Downloads\MLI_EP003_AUDIO_V1'),
    [string]$Work = (Join-Path $HOME 'Downloads\MLI_EP003_ALIGNMENT_V1'),
    [string]$AlignmentPython = (Join-Path $HOME 'Downloads\MLI_WHISPERX_ENV\Scripts\python.exe')
)
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$revision = '2b1b0a3b8dc425a20b60d900c620e18c179089ba'
$repository = 'RafaelAlbaWebify/modern-life-inc-production'
if (-not (Test-Path -LiteralPath $AlignmentPython -PathType Leaf)) {
    throw "No encuentro el Python de WhisperX existente: $AlignmentPython. Indica su ruta con -AlignmentPython."
}
New-Item -ItemType Directory -Force -Path $Work | Out-Null
function Fetch([string]$Remote, [string]$Local, [bool]$PreserveDifferent) {
    $uri = "https://api.github.com/repos/$repository/contents/$($Remote)?ref=$revision"
    $response = Invoke-RestMethod -Uri $uri -Headers @{Accept='application/vnd.github+json'}
    $bytes = [Convert]::FromBase64String(($response.content -replace '\s',''))
    if ($PreserveDifferent -and (Test-Path -LiteralPath $Local)) {
        $hash = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($bytes))
        if ((Get-FileHash -LiteralPath $Local -Algorithm SHA256).Hash -ne $hash) {
            throw "Existing work differs: $Local. Preserved; use a new -Work folder."
        }
    }
    [IO.File]::WriteAllBytes($Local,$bytes)
}
Fetch 'episodes/MLI_EP003/shots.json' (Join-Path $Work 'contract.json') $true
Fetch 'episodes/MLI_EP003/alignment/manifest.json' (Join-Path $Work 'manifest.json') $true
Fetch 'episodes/MLI_EP003/alignment/verify_alignment_inputs.py' (Join-Path $Work 'verify_alignment_inputs.py') $false
Fetch 'tools/mli-align-episode.py' (Join-Path $Work 'mli-align-episode.py') $false
$started = [DateTimeOffset]::UtcNow
$clock = [Diagnostics.Stopwatch]::StartNew()
& $AlignmentPython (Join-Path $Work 'verify_alignment_inputs.py') --audio-work $AudioWork --kit $Work
if ($LASTEXITCODE -ne 0) { throw 'El guion o los WAV no corresponden al montaje. No se ha alineado nada.' }
& $AlignmentPython (Join-Path $Work 'mli-align-episode.py') --work $AudioWork --render-folder $Work
if ($LASTEXITCODE -ne 0) { throw 'Alineacion interrumpida. Conserva el error; no se han generado voces ni imagenes.' }
$clock.Stop()
@{episode='MLI_EP003';started_utc=$started.ToString('o');finished_utc=[DateTimeOffset]::UtcNow.ToString('o');elapsed_seconds=$clock.Elapsed.TotalSeconds;word_times='real_whisperx_alignment';source_revision=$revision;publication_approved=$false} | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $Work 'alignment_timing.json') -Encoding utf8
$zip = Join-Path $HOME ('Downloads\MLI_EP003_ALIGNMENT_' + (Get-Date -Format 'yyyyMMdd_HHmmss_fff') + '.zip')
$files = @('alignment.json','captions_words.srt','alignment_timing.json','contract.json','manifest.json') | ForEach-Object { Join-Path $Work $_ }
Compress-Archive -LiteralPath $files -DestinationPath $zip
Write-Host "ADJUNTA ESTE ZIP EN EL CHAT: $zip"
Write-Host ('Tiempo de alineacion: {0:N1} minutos' -f $clock.Elapsed.TotalMinutes)
