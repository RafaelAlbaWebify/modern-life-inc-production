param([ValidateSet("start","review","status","verify")][string]$Mode="start",[string]$Work="",[string]$Review="",[string[]]$Scenes=@("SC01","SC02","SC05"))
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
if(-not $Work -and $Mode -eq "start"){$Work=Join-Path $HOME ("Downloads\MLI_PIPELINE_"+(Get-Date -Format "yyyyMMdd_HHmmss"))}
if(-not $Work){throw "-Work required for review/status/verify"}
$Work=[IO.Path]::GetFullPath($Work)
function RunPipeline([string[]]$argList){
 & python $script @argList
 if($LASTEXITCODE -ne 0){throw "Pipeline failed at $($argList[0]); check $Work"}
}
if($Mode -eq "start"){
 RunPipeline (@("prepare","--work",$Work,"--scenes") + $Scenes)
 RunPipeline @("generate","--work",$Work)
 RunPipeline @("package","--work",$Work)
 Write-Host "UPLOAD: $($Work)_CHAT_REVIEW.zip" -ForegroundColor Green
}
elseif($Mode -eq "review"){
 if(-not(Test-Path -LiteralPath $Review -PathType Leaf)){throw "Review JSON missing: $Review"}
 RunPipeline @("ingest","--work",$Work,"--report",$Review)
 $state=Get-Content (Join-Path $Work "state.json") -Raw | ConvertFrom-Json
 $retry=@($state.shots.PSObject.Properties | Where-Object {$_.Value.state -eq "RETRY_AUTHORIZED"})
 if($retry.Count -gt 0){
  Write-Host "Retry only: $($retry.Name -join ', ')" -ForegroundColor Cyan
  RunPipeline @("generate","--work",$Work)
  RunPipeline @("package","--work",$Work)
  Write-Host "UPLOAD: $($Work)_CHAT_REVIEW.zip" -ForegroundColor Yellow
 }else{
  & python $script verify --work $Work
  if($LASTEXITCODE -ne 0){Write-Warning "Blocked: see acceptance_gate.json"}
 }
}
elseif($Mode -eq "verify"){RunPipeline @("verify","--work",$Work)}
else{RunPipeline @("status","--work",$Work)}
