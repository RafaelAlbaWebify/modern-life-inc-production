param([ValidateSet("start","review","status","verify","render","recover","qc","finish")][string]$Mode="start",[string]$Work="",[string]$Review="",[string]$RenderFolder="",[string]$Scene06Image="",[string[]]$Scenes=@("SC01","SC02","SC03","SC04","SC05","SC06"))
$ErrorActionPreference="Stop";$ProgressPreference="SilentlyContinue"
$repo="RafaelAlbaWebify/modern-life-inc-production"
$storage=Join-Path $env:TEMP "MLI-Pipeline"
$toolsDir=Join-Path $storage "tools";$testsDir=Join-Path $storage "tests"
New-Item -ItemType Directory -Force -Path $toolsDir,$testsDir | Out-Null
function FetchFile([string]$remote,[string]$dest){
 $uri="https://api.github.com/repos/$repo/contents/$($remote)?ref=main"
 $response=Invoke-RestMethod -Uri $uri -Headers @{"Accept"="application/vnd.github+json";"Cache-Control"="no-cache"}
 if(-not $response.content){throw "Empty GitHub content for $remote"}
 [IO.File]::WriteAllBytes($dest,[Convert]::FromBase64String(($response.content -replace '\s','')))
 if((Get-Item $dest).Length -lt 100){throw "Empty download: $dest"}
}
$script=Join-Path $toolsDir "mli-pipeline.py";$test=Join-Path $testsDir "test_mli_pipeline.py"
FetchFile "tools/mli-pipeline.py" $script
FetchFile "tests/test_mli_pipeline.py" $test
Write-Host "Preflight: unit tests..." -ForegroundColor Cyan
& python $test -v
if($LASTEXITCODE -ne 0){throw "Unit tests failed. No GPU executed."}
$finishingTest=Join-Path $testsDir "test_mli_finishing.py"
FetchFile "tests/test_mli_finishing.py" $finishingTest
FetchFile "tools/mli-align.py" (Join-Path $toolsDir "mli-align.py")
FetchFile "tools/mli-finish.py" (Join-Path $toolsDir "mli-finish.py")
& python $finishingTest -v
if($LASTEXITCODE -ne 0){throw "Finishing regression tests failed."}
if(-not $Work -and $Mode -eq "start"){$Work=Join-Path $HOME ("Downloads\MLI_PIPELINE_"+(Get-Date -Format "yyyyMMdd_HHmmss"))}
if(-not $Work -and $Mode -notin @("qc","finish")){throw "-Work required for review/status/verify"}
$Work=if($Work){[IO.Path]::GetFullPath($Work)}else{""}
function RunPipeline([string[]]$argList){
 & python $script @argList
 if($LASTEXITCODE -ne 0){throw "Pipeline failed at $($argList[0]); check $Work"}
}
if($Mode -eq "start"){
 RunPipeline -argList (@("prepare","--work",$Work,"--scenes") + $Scenes)
 RunPipeline -argList @("generate","--work",$Work)
 RunPipeline -argList @("package","--work",$Work)
 Write-Host "UPLOAD: $($Work)_CHAT_REVIEW.zip" -ForegroundColor Green
}
elseif($Mode -eq "review"){
 if(-not(Test-Path -LiteralPath $Review -PathType Leaf)){throw "Review JSON missing: $Review"}
 RunPipeline -argList @("ingest","--work",$Work,"--report",$Review)
 $state=Get-Content (Join-Path $Work "state.json") -Raw | ConvertFrom-Json
 $retry=@($state.shots.PSObject.Properties | Where-Object {$_.Value.state -eq "RETRY_AUTHORIZED"})
 if($retry.Count -gt 0){
  Write-Host "Retry only: $($retry.Name -join ', ')" -ForegroundColor Cyan
  RunPipeline -argList @("generate","--work",$Work)
  RunPipeline -argList @("package","--work",$Work)
  Write-Host "UPLOAD: $($Work)_CHAT_REVIEW.zip" -ForegroundColor Yellow
 }else{
  & python $script verify --work $Work
  if($LASTEXITCODE -ne 0){Write-Warning "Blocked: see acceptance_gate.json"}
 }
}
elseif($Mode -eq "finish"){
 if(-not $RenderFolder -or -not $Scene06Image){throw "Need -RenderFolder and -Scene06Image"}
 if(-not (Test-Path -LiteralPath $Scene06Image -PathType Leaf)){throw "Missing chosen SC06 image"}
 $align=Join-Path $toolsDir "mli-align.py"
 $finish=Join-Path $toolsDir "mli-finish.py"
 $builder=Join-Path $toolsDir "build-mli-pilot-enhanced.py"
 FetchFile "tools/mli-align.py" $align
 FetchFile "tools/mli-finish.py" $finish
 FetchFile "tools/build-mli-pilot-enhanced.py" $builder
 $audio="C:\AI\MLI-FluxTest-Vulkan\pilot_audio"
 Write-Host "Forced-aligning narration to six WAVs (CPU)..." -ForegroundColor Cyan
 & python $align --audio-dir $audio --render-folder $RenderFolder --builder $builder
 if($LASTEXITCODE -ne 0){throw "Word alignment failed; no estimated captions substituted"}
 $srt=Join-Path $RenderFolder "MLI_PILOT_001_CAPTIONS_ALIGNED.srt"
 Write-Host "Building final review cut with chosen SC06 and aligned captions..." -ForegroundColor Cyan
 & python $finish --source-folder $RenderFolder --scene06-image $Scene06Image --aligned-srt $srt
 if($LASTEXITCODE -ne 0){throw "Final cut failed"}
}
elseif($Mode -eq "qc"){
 if(-not $RenderFolder){throw "-RenderFolder is required for qc"}
 $qc=Join-Path $toolsDir "mli-qc.py"
 FetchFile "tools/mli-qc.py" $qc
 & python $qc --folder $RenderFolder
 if($LASTEXITCODE -ne 0){throw "Technical QC failed; read technical_qc.json"}
}
elseif($Mode -eq "recover"){RunPipeline -argList @("recover","--work",$Work)}
elseif($Mode -eq "verify"){RunPipeline -argList @("verify","--work",$Work)}
elseif($Mode -eq "render"){
 RunPipeline -argList @("verify","--work",$Work)
 $state=Get-Content (Join-Path $Work "state.json") -Raw | ConvertFrom-Json
 $sceneIDs=@($state.shots.PSObject.Properties.Name)
 if($sceneIDs.Count -ne 6 -or (@("SC01","SC02","SC03","SC04","SC05","SC06") | Where-Object {$_ -notin $sceneIDs}).Count -gt 0){
  throw "Render requires all SC01..SC06 reviewed and accepted in this run."
 }
 RunPipeline -argList @("export","--work",$Work)
 $builder=Join-Path $toolsDir "build-mli-pilot-enhanced.py"
 FetchFile "tools/build-mli-pilot-enhanced.py" $builder
 $audio="C:\AI\MLI-FluxTest-Vulkan\pilot_audio"
 foreach($sid in @("SC01","SC02","SC03","SC04","SC05","SC06")){
  if(-not(Test-Path (Join-Path $audio ($sid+".wav")))){throw "Missing WAV for ${sid}: $audio"}
 }
 & python $builder --images-dir (Join-Path $Work "accepted_images") --audio-dir $audio --pause 0.25
 if($LASTEXITCODE -ne 0){throw "Renderer failed"}
 Write-Host "VIDEO RENDERED, FINAL AUDIOVISUAL QC STILL REQUIRED" -ForegroundColor Green
}
else{RunPipeline -argList @("status","--work",$Work)}
