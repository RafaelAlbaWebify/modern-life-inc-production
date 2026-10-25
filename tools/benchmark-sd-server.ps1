# Single-command, cwd-independent FLUX sd-server 2-shot performance benchmark.
# Runs local-only HTTP; original models, ZIPs, source assets left unchanged.
param([int]$Port=7861)
$ErrorActionPreference="Stop"
$ProgressPreference="SilentlyContinue"
$root="C:\AI\MLI-FluxTest-Vulkan";$models="C:\AI\MLI-FluxTest\models"
$server=Join-Path $root "sd-server.exe"
$diff=Join-Path $models "flux-2-klein-4b-q4_0.gguf"
$llm=Join-Path $models "Qwen3-4B-Q4_K_S.gguf"
$vae=Join-Path $models "flux2-vae.safetensors"
$reference=Join-Path $root "story_consistency_revised\CHARACTER_REFERENCE.png"
$prompts=Join-Path $HOME "Downloads\MLI_PILOT_001_PROMPTS"
$run=Join-Path $HOME ("Downloads\MLI_SERVER_BENCH_"+(Get-Date -Format "yyyyMMdd_HHmmss"))
New-Item -ItemType Directory -Force -Path $run|Out-Null
$report=[ordered]@{status="NOT_STARTED";started=(Get-Date).ToString("o");exe=$server;port=$Port;server_load_seconds=$null;shots=@();error=$null}
$process=$null
try{
 foreach($f in @($server,$diff,$llm,$vae,$reference,(Join-Path $prompts "SC01.txt"),(Join-Path $prompts "SC05.txt"))){
  if(-not (Test-Path -LiteralPath $f -PathType Leaf)){throw "Missing prerequisite: $f"}
 }
 $help=Join-Path $run "server-help.txt"
 $helpText=(& $server --help 2>&1|Out-String)
 $helpText|Set-Content -LiteralPath $help -Encoding UTF8
 # Avoid guessing: stop before generation if this local build lacks required CLI and HTTP options.
 foreach($flag in @("--diffusion-model","--llm","--vae","--backend","--params-backend","--port")){
  if(-not $helpText.Contains($flag)){throw "Server binary does not advertise required option $flag; inspect $help (no changes made)"}
 }
 # Never kill/attach to an unrelated service.
 $client=[Net.Sockets.TcpClient]::new()
 try{$client.Connect("127.0.0.1",$Port);throw "Port $Port already in use. No process killed; use -Port 7862."}
 catch [Net.Sockets.SocketException] {}
 finally{$client.Dispose()}
 $stdout=Join-Path $run "sd-server.stdout.log"
 $stderr=Join-Path $run "sd-server.stderr.log"
 $args=@("--diffusion-model",$diff,"--llm",$llm,"--vae",$vae,"--backend","te=cpu,diffusion=vulkan0,vae=cpu","--params-backend","te=cpu,diffusion=cpu,vae=cpu","--host","127.0.0.1","--port","$Port")
 $t0=[Diagnostics.Stopwatch]::StartNew()
 $process=Start-Process -FilePath $server -ArgumentList $args -RedirectStandardOutput $stdout -RedirectStandardError $stderr -PassThru -NoNewWindow
 $url="http://127.0.0.1:$Port"
 $ready=$false
 while($t0.Elapsed.TotalSeconds -lt 300){
  if($process.HasExited){throw "sd-server exited early code $($process.ExitCode). Review $stderr"}
  try{
   $null=Invoke-RestMethod -Uri "$url/v1/models" -Method Get -TimeoutSec 5
   $ready=$true;break
  }catch{Start-Sleep -Seconds 2}
 }
 if(-not $ready){throw "Server not ready after 300s; inspect stdout/stderr logs"}
 $t0.Stop();$report.server_load_seconds=[math]::Round($t0.Elapsed.TotalSeconds,2)
 $refBase64=[Convert]::ToBase64String([IO.File]::ReadAllBytes($reference))
 foreach($id in @("SC01","SC05")){
  $prompt=Get-Content -LiteralPath (Join-Path $prompts "$id.txt") -Raw -Encoding utf8
  $seed=if($id -eq "SC01"){3101}else{3105}
  # sdapi supports extra_images; on this binary API may differ, so record errors explicitly.
  $payload=@{prompt=$prompt;width=768;height=432;steps=4;cfg_scale=1;seed=$seed;sampler_name="euler";batch_size=1;extra_images=@($refBase64)}|ConvertTo-Json -Depth 8 -Compress
  $clock=[Diagnostics.Stopwatch]::StartNew()
  try{
   $response=Invoke-RestMethod -Uri "$url/sdapi/v1/txt2img" -Method Post -ContentType "application/json" -Body $payload -TimeoutSec 600
   $clock.Stop()
   if(-not $response.images -or $response.images.Count -lt 1){throw "No images in response"}
   $data=[Convert]::FromBase64String(($response.images[0] -replace '^data:image/\w+;base64,',''))
   $dst=Join-Path $run "$id.png"
   [IO.File]::WriteAllBytes($dst,$data)
   $report.shots+=@{scene=$id;seconds=[math]::Round($clock.Elapsed.TotalSeconds,2);output=$dst;bytes=$data.Length;status="GENERATED_NOT_VISUALLY_APPROVED"}
  }catch{
   $clock.Stop();$report.shots+=@{scene=$id;seconds=[math]::Round($clock.Elapsed.TotalSeconds,2);status="FAILED";error=$_.Exception.Message}
   throw
  }
 }
 $report.status="COMPLETE_NOT_VISUALLY_APPROVED"
}catch{
 $report.status="FAILED";$report.error=$_.Exception.Message
 Write-Warning $report.error
}finally{
 if($process -and -not $process.HasExited){Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue}
 $report.finished=(Get-Date).ToString("o")
 $report|ConvertTo-Json -Depth 8|Set-Content -LiteralPath (Join-Path $run "benchmark.json") -Encoding UTF8
 Write-Host "Benchmark folder: $run"
 Write-Host "Server load seconds: $($report.server_load_seconds)"
 foreach($s in $report.shots){Write-Host "$($s.scene): $($s.seconds)s $($s.status)"}
 Write-Host "Final status: $($report.status)"
}
if($report.status -ne "COMPLETE_NOT_VISUALLY_APPROVED"){exit 1}
