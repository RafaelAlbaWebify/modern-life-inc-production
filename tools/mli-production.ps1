param([ValidateSet("start","review","status","verify","render","recover","qc","finish","plan","episode-render","episode-qc")][string]$Mode="start",[string]$Work="",[string]$Episode="MLI_PILOT_001",[string]$Review="",[string]$RenderFolder="",[string]$Scene06Image="",[ValidateSet("karaoke","cinematic","amber")][string]$CaptionStyle="karaoke",[string[]]$Scenes=@("SC01","SC02","SC03","SC04","SC05","SC06"))
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
$script:preflightFindings=[System.Collections.Generic.List[object]]::new()
function Check([string]$name,[bool]$ok,[string]$detail){
 $status=if($ok){"PASS"}else{"FAIL"}
 $script:preflightFindings.Add([pscustomobject]@{Check=$name;Status=$status;Detail=$detail})
}
function CheckFile([string]$name,[string]$path){
 Check $name (Test-Path -LiteralPath $path -PathType Leaf) $path
}
function Preflight([string]$stage){
 Write-Host "MLI PRE-FLIGHT [$stage] - comprehensive checks" -ForegroundColor Cyan
 $script:preflightFindings.Clear()
 $script:runtimePython=$null
 $candidates=@()
 $current=Get-Command python -ErrorAction SilentlyContinue
 if($current){$candidates+=,$current.Source}
 $launcher=Get-Command py -ErrorAction SilentlyContinue
 if($launcher){
  foreach($version in @("3.12","3.11","3.13","3.10")){
   $found=(& py "-$version" -c "import sys;print(sys.executable)" 2>$null | Select-Object -Last 1)
   if($LASTEXITCODE -eq 0 -and $found){$candidates+=,[string]$found}
  }
 }
 foreach($candidate in ($candidates | Select-Object -Unique)){
  $result=& $candidate -c "import sys;sys.exit(0 if (3,10)<=sys.version_info[:2]<(3,14) else 1)" 2>$null
  if($LASTEXITCODE -eq 0){$script:runtimePython=$candidate;break}
 }
 Check "Compatible Python" ($null -ne $script:runtimePython) $(if($script:runtimePython){"Selected: $script:runtimePython"}else{"No compatible Python; checked: $($candidates -join ', ')"})
 if($stage -in @("start","render","finish","qc","episode-render","episode-qc")){
  foreach($name in @("ffmpeg","ffprobe")){
   Check "$name executable" ($null -ne (Get-Command $name -ErrorAction SilentlyContinue)) "$name in PATH"
  }
 }
 if($stage -eq "start"){
  $engine="C:\AI\MLI-FluxTest-Vulkan"
  $models="C:\AI\MLI-FluxTest\models"
  foreach($f in @("$engine\sd-cli.exe","$engine\story_consistency_revised\CHARACTER_REFERENCE.png",
    "$models\flux-2-klein-4b-q4_0.gguf","$models\Qwen3-4B-Q4_K_S.gguf","$models\flux2-vae.safetensors")){
   CheckFile "Image generation asset" $f
  }
 }
 if($stage -eq "render"){
  $audio="C:\AI\MLI-FluxTest-Vulkan\pilot_audio"
  foreach($n in 1..6){CheckFile ("Narration SC{0:00}" -f $n) (Join-Path $audio ("SC{0:00}.wav" -f $n))}
 }
 if($stage -eq "finish"){
  Check "Render folder" (-not [string]::IsNullOrWhiteSpace($RenderFolder) -and (Test-Path -LiteralPath $RenderFolder -PathType Container)) $RenderFolder
  if($RenderFolder){
   CheckFile "Word alignment" (Join-Path $RenderFolder "alignment.json")
   CheckFile "Aligned captions" (Join-Path $RenderFolder "MLI_PILOT_001_CAPTIONS_ALIGNED.srt")
   foreach($n in 1..6){CheckFile ("Rendered SC{0:00}" -f $n) (Join-Path $RenderFolder ("SC{0:00}.mp4" -f $n))}
  }
  CheckFile "Selected SC06" $Scene06Image
 }
 if($stage -eq "plan"){
  Check "Episode ID" ($Episode -match '^MLI_[A-Z0-9_]+$') $Episode
 }
 if($stage -notin @("start","plan","qc","finish")){
  Check "Work folder" (-not [string]::IsNullOrWhiteSpace($Work) -and (Test-Path -LiteralPath $Work -PathType Container)) $Work
 }
 $fails=@($script:preflightFindings | Where-Object {$_.Status -eq "FAIL"})
 $script:preflightFindings | Format-Table -AutoSize | Out-Host
 $report=[pscustomobject]@{mode=$stage;checked=$script:preflightFindings.Count;failures=$fails.Count;checks=@($script:preflightFindings);can_proceed=($fails.Count -eq 0)}
 $reportPath=Join-Path $storage "preflight_$stage.json"
 $report | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $reportPath -Encoding utf8
 Write-Host "PREFLIGHT REPORT: $reportPath"
 if($fails.Count){throw "PREFLIGHT FAILED: $($fails.Count) requirements failed out of $($script:preflightFindings.Count). No production tasks started."}
 Write-Host "PREFLIGHT PASS [$stage]" -ForegroundColor Green
}
Preflight $Mode
$script=Join-Path $toolsDir "mli-pipeline.py";$test=Join-Path $testsDir "test_mli_pipeline.py"
FetchFile "tools/mli-pipeline.py" $script
FetchFile "tests/test_mli_pipeline.py" $test
Write-Host "Preflight: unit tests..." -ForegroundColor Cyan
& $script:runtimePython $test -v
if($LASTEXITCODE -ne 0){throw "Unit tests failed. No GPU executed."}
$finishingTest=Join-Path $testsDir "test_mli_finishing.py"
FetchFile "tests/test_mli_finishing.py" $finishingTest
FetchFile "tools/mli-align.py" (Join-Path $toolsDir "mli-align.py")
FetchFile "tools/mli-finish.py" (Join-Path $toolsDir "mli-finish.py")
FetchFile "tools/mli-caption-styles.py" (Join-Path $toolsDir "mli-caption-styles.py")
& $script:runtimePython $finishingTest -v
if($LASTEXITCODE -ne 0){throw "Finishing regression tests failed."}
if(-not $Work -and $Mode -in @("start","plan")){$Work=Join-Path $HOME ("Downloads\$($Episode)_PIPELINE_"+(Get-Date -Format "yyyyMMdd_HHmmss"))}
if(-not $Work -and $Mode -notin @("qc","finish")){throw "-Work required for review/status/verify"}
$Work=if($Work){[IO.Path]::GetFullPath($Work)}else{""}
function RunPipeline([string[]]$argList){
 & $script:runtimePython $script @argList
 if($LASTEXITCODE -ne 0){throw "Pipeline failed at $($argList[0]); check $Work"}
}
if($Mode -eq "plan"){
 if($Episode -notmatch '^MLI_[A-Z0-9_]+$'){throw "Invalid episode ID"}
 $contract=Join-Path $storage ($Episode+"_shots.json")
 FetchFile "episodes/$Episode/shots.json" $contract
 RunPipeline -argList @("prepare","--work",$Work,"--shots",$contract)
 Write-Host "PLAN READY: $Work (no GPU used)" -ForegroundColor Green
}
elseif($Mode -eq "start"){
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
elseif($Mode -eq "episode-render"){
 if(-not $Work){throw "-Work required for episode-render"}
 $audio=Join-Path $Work "audio"
 $renderer=Join-Path $toolsDir "mli-render-episode.py"
 FetchFile "tools/mli-render-episode.py" $renderer
 RunPipeline -argList @("verify","--work",$Work)
 RunPipeline -argList @("export","--work",$Work)
 & $script:runtimePython $renderer --work $Work --audio-dir $audio
 if($LASTEXITCODE -ne 0){throw "Episode render failed"}
}
elseif($Mode -eq "episode-qc"){
 if(-not $RenderFolder){throw "-RenderFolder required"}
 $qc=Join-Path $toolsDir "mli-qc-episode.py"
 FetchFile "tools/mli-qc-episode.py" $qc
 & $script:runtimePython $qc --folder $RenderFolder
 if($LASTEXITCODE -ne 0){throw "Episode QC failed"}
}
elseif($Mode -eq "finish"){
 if(-not $RenderFolder -or -not $Scene06Image){throw "Need -RenderFolder and -Scene06Image"}
 if(-not (Test-Path -LiteralPath $Scene06Image -PathType Leaf)){throw "Missing chosen SC06 image"}
 $align=Join-Path $toolsDir "mli-align.py"
 $finish=Join-Path $toolsDir "mli-finish.py"
 $builder=Join-Path $toolsDir "build-mli-pilot-enhanced.py"
 $captionScript=Join-Path $toolsDir "mli-caption-styles.py"
 FetchFile "tools/mli-caption-styles.py" $captionScript
 FetchFile "tools/mli-align.py" $align
 FetchFile "tools/mli-finish.py" $finish
 FetchFile "tools/build-mli-pilot-enhanced.py" $builder
 $audio="C:\AI\MLI-FluxTest-Vulkan\pilot_audio"
 $srt=Join-Path $RenderFolder "MLI_PILOT_001_CAPTIONS_ALIGNED.srt"
 $alignment=Join-Path $RenderFolder "alignment.json"
 if(-not(Test-Path -LiteralPath $srt) -or -not(Test-Path -LiteralPath $alignment)){throw "Verified alignment missing; run setup-and-align.ps1 first"}
 $alignmentData=Get-Content -LiteralPath $alignment -Raw | ConvertFrom-Json
 if($alignmentData.words.Count -lt 50 -or $alignmentData.scenes.Count -ne 6){throw "Alignment incomplete: expected six scenes and word timing"}
 Write-Host "Reusing existing aligned subtitles ($($alignmentData.words.Count) words)" -ForegroundColor Green
 Write-Host "Building final review cut with chosen SC06 and aligned captions..." -ForegroundColor Cyan
 & $script:runtimePython $finish --source-folder $RenderFolder --scene06-image $Scene06Image --aligned-srt $srt --alignment $alignment --caption-script $captionScript --caption-style $CaptionStyle
 if($LASTEXITCODE -ne 0){throw "Final cut failed"}
}
elseif($Mode -eq "qc"){
 if(-not $RenderFolder){throw "-RenderFolder is required for qc"}
 $qc=Join-Path $toolsDir "mli-qc.py"
 FetchFile "tools/mli-qc.py" $qc
 & $script:runtimePython $qc --folder $RenderFolder
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
 & $script:runtimePython $builder --images-dir (Join-Path $Work "accepted_images") --audio-dir $audio --pause 0.25
 if($LASTEXITCODE -ne 0){throw "Renderer failed"}
 Write-Host "VIDEO RENDERED, FINAL AUDIOVISUAL QC STILL REQUIRED" -ForegroundColor Green
}
else{RunPipeline -argList @("status","--work",$Work)}
