param([switch]$RunVaeTrial)
# From any working directory; default is zero-GPU QC + CLI capability review.
$ErrorActionPreference="Stop";$ProgressPreference="SilentlyContinue"
$repo="https://api.github.com/repos/RafaelAlbaWebify/modern-life-inc-production/contents/tools/visual-qc.py?ref=main&v=$([DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds())"
$work=Join-Path $env:TEMP "MLI-Pipeline";New-Item -ItemType Directory -Force -Path $work|Out-Null
$qc=Join-Path $work "visual-qc.py";$res=Invoke-RestMethod -Uri $repo -Headers @{"Accept"="application/vnd.github+json"}
[IO.File]::WriteAllBytes($qc,[Convert]::FromBase64String(($res.content -replace '\s','')))
$gate=Get-ChildItem (Join-Path $HOME "Downloads") -Directory -Filter "MLI_ENGINE_GATE_*" |Where-Object {Test-Path (Join-Path $_.FullName "images\SC01_attempt1.png")} |Sort-Object LastWriteTime -Descending |Select-Object -First 1
if(-not $gate){throw "Cannot find extracted engine gate images; supply previously extracted images folder."}
$out=Join-Path $HOME ("Downloads\MLI_QC_VAE_"+(Get-Date -Format "yyyyMMdd_HHmmss"))
New-Item -ItemType Directory -Force -Path $out |Out-Null
& python $qc --images (Join-Path $gate.FullName "images") --out $out
Write-Host "Visual QC returned $LASTEXITCODE (3=PENDING, intentionally blocked)"
$sd="C:\AI\MLI-FluxTest-Vulkan\sd-cli.exe"
$help=(& $sd --help 2>&1 |Out-String)
$help|Set-Content (Join-Path $out "sd-cli-help.txt")
$flags=[ordered]@{vae_conv_direct=$help.Contains("--vae-conv-direct");vae_tiling=$help.Contains("--vae-tiling");backend=$help.Contains("--backend")}
$flags|ConvertTo-Json |Set-Content (Join-Path $out "vae_capabilities.json")
if($RunVaeTrial){
 if(-not $flags.vae_conv_direct){Write-Warning "No --vae-conv-direct in this local build; no benchmark run"}
 else{
  $root="C:\AI\MLI-FluxTest-Vulkan";$model="C:\AI\MLI-FluxTest\models"
  $ref=Join-Path $root "story_consistency_revised\CHARACTER_REFERENCE.png"
  $promptFile=Join-Path $HOME "Downloads\MLI_PILOT_001_PROMPTS\SC05.txt"
  $diff=Join-Path $model "flux-2-klein-4b-q4_0.gguf"
  $llm=Join-Path $model "Qwen3-4B-Q4_K_S.gguf"
  $vae=Join-Path $model "flux2-vae.safetensors"
  foreach($f in @($sd,$ref,$promptFile,$diff,$llm,$vae)){if(-not(Test-Path $f)){throw "Missing $f"}}
  $prompt=Get-Content $promptFile -Raw -Encoding UTF8
  $args=@("--diffusion-model",$diff,"--llm",$llm,"--vae",$vae,"--backend","te=cpu,diffusion=vulkan0,vae=cpu","--params-backend","te=cpu,diffusion=cpu,vae=cpu","-r",$ref,"--ref-image-args","preset=flux2","-p",$prompt,"--cfg-scale","1","--sampling-method","euler","--steps","4","-W","768","-H","432","-t","4","--seed","3105")
  $measure=@()
  foreach($variant in @("baseline","vae_conv_direct")){
   $target=Join-Path $out "$variant.png";$log=Join-Path $out "$variant.log"
   $argv=$args+@("--output",$target)
   if($variant -eq "vae_conv_direct"){$argv+=@("--vae-conv-direct")}
   Write-Host "Generating $variant (source models unchanged)..." -ForegroundColor Cyan
   $sw=[Diagnostics.Stopwatch]::StartNew()
   & $sd @argv *> $log
   $sw.Stop()
   $measure+= [pscustomobject]@{variant=$variant;elapsed_seconds=[math]::Round($sw.Elapsed.TotalSeconds,2);exit_code=$LASTEXITCODE;image=$target;log=$log}
   if($LASTEXITCODE -ne 0){Write-Warning "$variant failed: review $log";break}
  }
  $measure|ConvertTo-Json |Set-Content (Join-Path $out "vae_trial.json")
 }
}
Write-Host "QC and VAE report: $out" -ForegroundColor Green
