param([string]$RenderFolder="$HOME\Downloads\MLI_PILOT_001_20261027_062750")
$ErrorActionPreference="Stop"
$ProgressPreference="SilentlyContinue"
$venv=Join-Path $HOME "Downloads\MLI_WHISPERX_ENV"
$python=Join-Path $venv "Scripts\python.exe"
$audio="C:\AI\MLI-FluxTest-Vulkan\pilot_audio"
if(-not(Test-Path -LiteralPath $RenderFolder -PathType Container)){throw "Missing render folder"}
foreach($sid in @("SC01","SC02","SC03","SC04","SC05","SC06")){
 foreach($f in @((Join-Path $audio ($sid+".wav")),(Join-Path $RenderFolder ($sid+".mp4")))){
  if(-not(Test-Path -LiteralPath $f -PathType Leaf)){throw "Missing input: $f"}
 }
}
foreach($cmd in @("ffmpeg","ffprobe")){if(-not(Get-Command $cmd -ErrorAction SilentlyContinue)){throw "Missing: $cmd"}}
if(-not(Test-Path -LiteralPath $python)){
 if(-not(Get-Command py -ErrorAction SilentlyContinue)){throw "Install Python 3.11 with Windows launcher"}
 & py -3.11 -m venv $venv
 if($LASTEXITCODE -ne 0){throw "Install Python 3.11, then retry"}
}
if(-not(Test-Path $python)){throw "Python environment unavailable"}
& $python -c "import importlib.util,sys;sys.exit(0 if importlib.util.find_spec('whisperx') else 2)"
if($LASTEXITCODE -ne 0){
 Write-Host "Installing WhisperX in isolated environment..." -ForegroundColor Cyan
 & $python -m pip install --upgrade pip
 if($LASTEXITCODE -ne 0){throw "pip setup failed"}
 & $python -m pip install whisperx
 if($LASTEXITCODE -ne 0){throw "WhisperX installation failed"}
}
& $python -c "import whisperx;print('WhisperX import OK')"
if($LASTEXITCODE -ne 0){throw "WhisperX import failed"}
$repo="RafaelAlbaWebify/modern-life-inc-production"
$tools=Join-Path $env:TEMP "MLI-Pipeline\tools"
New-Item -ItemType Directory -Force -Path $tools | Out-Null
foreach($item in @("mli-align.py","build-mli-pilot-enhanced.py")){
 $uri="https://api.github.com/repos/$repo/contents/tools/$($item)?ref=main"
 $response=Invoke-RestMethod -Uri $uri -Headers @{Accept="application/vnd.github+json"}
 [IO.File]::WriteAllBytes((Join-Path $tools $item),[Convert]::FromBase64String(($response.content -replace '\s','')))
}
& $python (Join-Path $tools "mli-align.py") --audio-dir $audio --render-folder $RenderFolder --builder (Join-Path $tools "build-mli-pilot-enhanced.py")
if($LASTEXITCODE -ne 0){throw "Alignment failed; existing estimated SRT unchanged"}
Write-Host "ALIGNED SRT: $(Join-Path $RenderFolder 'MLI_PILOT_001_CAPTIONS_ALIGNED.srt')" -ForegroundColor Green
