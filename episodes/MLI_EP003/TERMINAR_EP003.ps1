param(
    [string]$AudioWork = (Join-Path $HOME 'Downloads\MLI_EP003_AUDIO_V1'),
    [string]$AlignmentPython = (Join-Path $HOME 'Downloads\MLI_WHISPERX_ENV\Scripts\python.exe')
)
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$root = $PSScriptRoot
$work = Join-Path $root 'work'
$tools = Join-Path $root 'tools'
$python = (Get-Command python -ErrorAction Stop).Source
foreach ($command in @('ffmpeg','ffprobe')) { Get-Command $command -ErrorAction Stop | Out-Null }
if (-not (Test-Path -LiteralPath $AlignmentPython -PathType Leaf)) {
    throw "No encuentro el entorno WhisperX existente: $AlignmentPython. Usa -AlignmentPython con la ruta correcta; no se ha instalado nada."
}
function Run-Python([string]$Executable, [string[]]$Arguments) {
    & $Executable @Arguments
    if ($LASTEXITCODE -ne 0) { throw "Fallo en $($Arguments[0]); los archivos previos se conservan." }
}
$started = [DateTimeOffset]::UtcNow
$clock = [Diagnostics.Stopwatch]::StartNew()
$stages = [Collections.Generic.List[object]]::new()
Push-Location $root
try {
    $phase = [Diagnostics.Stopwatch]::StartNew()
    Run-Python -Executable $python -Arguments @((Join-Path $tools 'prepare_audio.py'), '--work', $work, '--audio-work', $AudioWork)
    Run-Python -Executable $python -Arguments @((Join-Path $tools 'mli-audio-episode.py'), '--work', $work)
    Run-Python -Executable $python -Arguments @((Join-Path $tools 'mli-pipeline.py'), 'verify', '--work', $work)
    Run-Python -Executable $python -Arguments @((Join-Path $tools 'mli-pipeline.py'), 'export', '--work', $work)
    $stages.Add(@{stage='preflight_audio_and_images';seconds=$phase.Elapsed.TotalSeconds})
    $phase.Restart()
    $renders = Join-Path $root 'renders'
    New-Item -ItemType Directory -Force -Path $renders | Out-Null
    Run-Python -Executable $python -Arguments @((Join-Path $tools 'mli-render-episode.py'), '--work', $work, '--audio-dir', (Join-Path $work 'audio'), '--out-root', $renders)
    $folder = Get-ChildItem -LiteralPath $renders -Directory | Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName 'manifest.json') } | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if (-not $folder) { throw 'No hay un render completo con manifest.json.' }
    $stages.Add(@{stage='render_and_strict_master_validation';seconds=$phase.Elapsed.TotalSeconds;folder=$folder.FullName})
    $phase.Restart()
    Run-Python -Executable $AlignmentPython -Arguments @((Join-Path $tools 'mli-align-episode.py'), '--work', $work, '--render-folder', $folder.FullName)
    $stages.Add(@{stage='new_real_word_alignment';seconds=$phase.Elapsed.TotalSeconds})
    $phase.Restart()
    Run-Python -Executable $python -Arguments @((Join-Path $tools 'mli-finish-episode.py'), '--render-folder', $folder.FullName, '--caption-script', (Join-Path $tools 'mli-caption-styles.py'))
    Run-Python -Executable $python -Arguments @((Join-Path $tools 'mli-qc-episode.py'), '--folder', $folder.FullName)
    $final = Join-Path $folder.FullName 'MLI_EP003_SOFT_KARAOKE.mp4'
    & ffmpeg -nostdin -hide_banner -v error -xerror -i $final -f null -
    if ($LASTEXITCODE -ne 0) { throw 'El MP4 final no ha pasado la decodificacion estricta.' }
    $stages.Add(@{stage='soft_karaoke_and_final_qc';seconds=$phase.Elapsed.TotalSeconds})
    $clock.Stop()
    @{episode='MLI_EP003';started_utc=$started.ToString('o');finished_utc=[DateTimeOffset]::UtcNow.ToString('o');elapsed_seconds=$clock.Elapsed.TotalSeconds;stages=@($stages);native_windows_execution=$true;technical_pass=$true;listening_review_pending=$true;publication_approved=$false} | ConvertTo-Json -Depth 7 | Set-Content -LiteralPath (Join-Path $folder.FullName 'local_finishing_timing.json') -Encoding utf8
    Write-Host "VIDEO: $final"
    Write-Host 'Montaje y comprobacion tecnica terminados. Pendiente visionado completo, escucha y aprobacion editorial.'
} finally { Pop-Location }
