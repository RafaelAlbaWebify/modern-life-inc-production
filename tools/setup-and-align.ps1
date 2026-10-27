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
 $candidates=@()
 if(Get-Command py -ErrorAction SilentlyContinue){
  foreach($version in @("3.11","3.12","3.13","3.10")){
   & py "-$version" -c "import sys;print(sys.executable)" 2>$null
   if($LASTEXITCODE -eq 0){$candidates+=@("py","-$version");break}
  }
 }
 if($candidates.Count -eq 0){
  $command=Get-Command python -ErrorAction SilentlyContinue
  if($command){
   & python -c "import sys;v=sys.version_info;sys.exit(0 if (3,10)<=v[:2]<(3,14) else 1)" 2>$null
   if($LASTEXITCODE -eq 0){$candidates=@("python")}
  }
 }
 if($candidates.Count -eq 0){throw "No compatible Python 3.10-3.13 installed. Run: py --list-paths; python --version. Install Python 3.11 only if needed."}
 Write-Host "Creating isolated WhisperX environment using $($candidates -join ' ')" -ForegroundColor Cyan
 if($candidates.Count -eq 2){& py $candidates[1] -m venv $venv}else{& python -m venv $venv}
 if($LASTEXITCODE -ne 0){throw "Python virtual environment creation failed"}
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
