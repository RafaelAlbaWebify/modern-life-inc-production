param([switch]$SkipGeneration)
$ErrorActionPreference="Stop"
$ProgressPreference="SilentlyContinue"
$base="https://raw.githubusercontent.com/RafaelAlbaWebify/modern-life-inc-production/main"
$src=Join-Path $env:TEMP "MLI-Pipeline"
$root="C:\AI\MLI-FluxTest-Vulkan"
$modelRoot="C:\AI\MLI-FluxTest\models"
$exe=Join-Path $root "sd-cli.exe"
$diff=Join-Path $modelRoot "flux-2-klein-4b-q4_0.gguf"
$llm=Join-Path $modelRoot "Qwen3-4B-Q4_K_S.gguf"
$vae=Join-Path $modelRoot "flux2-vae.safetensors"
$ref=Join-Path $root "story_consistency_revised\CHARACTER_REFERENCE.png"
$run=Join-Path $HOME ("Downloads\MLI_ENGINE_GATE_"+(Get-Date -Format "yyyyMMdd_HHmmss"))
$prompts=Join-Path $run "prompts"
$images=Join-Path $run "images"
$logs=Join-Path $run "logs"
foreach($dir in @($src,$run,$prompts,$images,$logs)){New-Item -ItemType Directory -Force -Path $dir|Out-Null}
$files=@{
 "tools\plan-shots.py"="tools/plan-shots.py"
 "tests\test_shot_contract.py"="tests/test_shot_contract.py"
 "episodes\MLI_PILOT_001\shots.json"="episodes/MLI_PILOT_001/shots.json"
}
foreach($f in $files.Keys){
 $p=Join-Path $src $f
 New-Item -ItemType Directory -Force -Path (Split-Path $p -Parent)|Out-Null
 Invoke-WebRequest -Uri "$base/$($files[$f])" -OutFile $p
 if((Get-Item $p).Length -lt 100){throw "Downloaded source empty: $p"}
}
& python (Join-Path $src "tests\test_shot_contract.py") 2>&1|Tee-Object -FilePath (Join-Path $logs "tests.log")
if($LASTEXITCODE -ne 0){throw "Unit tests failed"}
& python (Join-Path $src "tools\plan-shots.py") --shots (Join-Path $src "episodes\MLI_PILOT_001\shots.json") --out $prompts
if($LASTEXITCODE -ne 0){throw "Prompt contract validation failed"}
$shots=@("SC01","SC02","SC05")
$results=@()
if(-not $SkipGeneration){
 foreach($p in @($exe,$diff,$llm,$vae,$ref)){if(-not(Test-Path -LiteralPath $p -PathType Leaf)){throw "Required local model or binary missing: $p"}}
}
$seeds=@{SC01=3101;SC02=3102;SC05=3105}
foreach($id in $shots){
 $prompt=(Get-Content -LiteralPath (Join-Path $prompts "$id.txt") -Raw -Encoding UTF8)
 $passed=$false;$reason="not-run";$output=""
 if($SkipGeneration){$reason="generation skipped"}
 else{
  for($attempt=1;$attempt -le 2 -and -not $passed;$attempt++){
   $output=Join-Path $images ("{0}_attempt{1}.png" -f $id,$attempt)
   $stdout=Join-Path $logs ("{0}_attempt{1}.log" -f $id,$attempt)
   $seed=$seeds[$id]+$attempt-1
   Write-Host "FLUX generating $id attempt $attempt / 2" -ForegroundColor Cyan
   $arguments=@("--diffusion-model",$diff,"--llm",$llm,"--vae",$vae,"--backend","te=cpu,diffusion=vulkan0,vae=cpu","--params-backend","te=cpu,diffusion=cpu,vae=cpu","-r",$ref,"--ref-image-args","preset=flux2","-p",$prompt,"--cfg-scale","1","--sampling-method","euler","--steps","4","-W","768","-H","432","-t","4","--seed",$seed,"--output",$output)
   & $exe @arguments *> $stdout
   $exit=$LASTEXITCODE
   $reason="ExitCode=$exit"
   if($exit -eq 0 -and (Test-Path -LiteralPath $output -PathType Leaf)){
    $f=Get-Item -LiteralPath $output
    $b=[IO.File]::ReadAllBytes($output)
    if($f.Length -gt 10000 -and $b.Length -gt 24 -and $b[0] -eq 137 -and $b[1] -eq 80 -and $b[2] -eq 78 -and $b[3] -eq 71){
     [Array]::Reverse($b,16,4);[Array]::Reverse($b,20,4)
     $w=[BitConverter]::ToUInt32($b,16);$h=[BitConverter]::ToUInt32($b,20)
     if($w -eq 768 -and $h -eq 432){$passed=$true;$reason="PNG verified 768x432"}
     else{$reason="Unexpected PNG size "+$w+"x"+$h}
    } else{$reason="File too small or invalid PNG signature"}
   }
   if(-not $passed){Write-Warning "$id attempt $attempt failed: $reason"}
  }
 }
 $results+= [pscustomobject]@{scene=$id;technical_status=$(if($passed){"PASS"}else{"NOT_PASS"});visual_status="PENDING_HUMAN_REVIEW";reason=$reason;image=$output}
}
$results | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $run "engine_gate_results.json") -Encoding UTF8
$readme="MLI engine gate: technical PNG integrity ONLY. Review SC01 lead identity, SC02 secondary normal faces, SC05 phone AWAY from BOTH hands. Max 2 attempts per shot. No full-video generation."
$readme | Set-Content -LiteralPath (Join-Path $run "REVIEW.txt")
$zip=Join-Path $HOME ("Downloads\"+(Split-Path $run -Leaf)+".zip")
Compress-Archive -Path (Join-Path $run "*") -DestinationPath $zip -CompressionLevel Optimal
$results|Format-Table -AutoSize
Write-Host "QA package: $zip" -ForegroundColor Green
Write-Host "Semantic visual validation pending; no engine approval inferred."
