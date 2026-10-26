# SC05 targeted second attempt — immutable accepted SC01/SC02
param()
$ErrorActionPreference="Stop";$ProgressPreference="SilentlyContinue"
$downloads=Join-Path $HOME "Downloads"
$gate=Get-ChildItem $downloads -Directory -Filter "MLI_ENGINE_GATE_*" | Where-Object {
 $d=Join-Path $_.FullName "images"
 (Test-Path (Join-Path $d "SC01_attempt1.png")) -and
 (Test-Path (Join-Path $d "SC02_attempt1.png")) -and
 (Test-Path (Join-Path $d "SC05_attempt1.png"))
} | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if($gate){$images=Join-Path $gate.FullName "images"}
else{
 $archive=Get-ChildItem $downloads -File -Filter "MLI_ENGINE_GATE_*.zip" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
 if(-not $archive){throw "No MLI_ENGINE_GATE archive or extracted image folder found in Downloads"}
 $images=Join-Path $downloads ("MLI_SC05_SOURCE_"+$archive.BaseName)
 New-Item -ItemType Directory -Force -Path $images | Out-Null
 Add-Type -AssemblyName System.IO.Compression
 $z=[IO.Compression.ZipFile]::OpenRead($archive.FullName)
 try {
  foreach($n in @("SC01_attempt1.png","SC02_attempt1.png","SC05_attempt1.png")){
   $entry=$z.Entries | Where-Object {$_.Name -eq $n} | Select-Object -First 1
   if(-not $entry){throw "Archive missing $n : $($archive.FullName)"}
   [IO.Compression.ZipFileExtensions]::ExtractToFile($entry,(Join-Path $images $n),$true)
  }
 } finally {$z.Dispose()}
 Write-Host "Restored 3 original PNGs from $($archive.Name)"
}
$ref="C:\AI\MLI-FluxTest-Vulkan\story_consistency_revised\CHARACTER_REFERENCE.png"
$exe="C:\AI\MLI-FluxTest-Vulkan\sd-cli.exe";$models="C:\AI\MLI-FluxTest\models"
foreach($f in @($ref,$exe,(Join-Path $models "flux-2-klein-4b-q4_0.gguf"),(Join-Path $models "Qwen3-4B-Q4_K_S.gguf"),(Join-Path $models "flux2-vae.safetensors"))){if(-not(Test-Path -LiteralPath $f)){throw "Missing $f"}}
$out=Join-Path $downloads ("MLI_SC05_RETRY_"+(Get-Date -Format "yyyyMMdd_HHmmss"))
New-Item -ItemType Directory -Force -Path $out | Out-Null
$prompt=@'
Cinematic clean 2D storybook frame, 16:9. SAME ICONIC protagonist as reference: pale minimalist face, short messy dark hair, bright large round orange headphones, teal hoodie. Medium-wide TWO-AREA composition. LEFT TWO-THIRDS: protagonist seated at wooden writing DESK, writing in open notebook with a pen in RIGHT hand; LEFT hand flat against the paper. Desk has notebook, pen and a laptop ONLY. RIGHT THIRD: a freestanding narrow BOOKSHELF against a DIFFERENT wall, separated from desk by an obvious empty gap of visible floor. On the TOP SHELF of this separate freestanding bookshelf rests the scene's ONE black smartphone, screen down. Camera angle must reveal the physical gap and both separate furniture pieces; the desk and bookshelf must not meet or touch. Phone is NOT on the desk, NOT in either hand, and not on any object connected to the desk. No other phones, tablets, dark screen slabs, people, framed portraits or posters with faces. Cozy amber interior at sunset. Prioritize readable spatial separation over decoration.
'@
$promptPath=Join-Path $out "SC05_attempt2_prompt.txt"
[IO.File]::WriteAllText($promptPath,$prompt,[Text.UTF8Encoding]::new($false))
$target=Join-Path $out "SC05_attempt2.png";$log=Join-Path $out "SC05_attempt2.log"
$argsList=@("--diffusion-model",(Join-Path $models "flux-2-klein-4b-q4_0.gguf"),"--llm",(Join-Path $models "Qwen3-4B-Q4_K_S.gguf"),"--vae",(Join-Path $models "flux2-vae.safetensors"),"--backend","te=cpu,diffusion=vulkan0,vae=cpu","--params-backend","te=cpu,diffusion=cpu,vae=cpu","-r",$ref,"--ref-image-args","preset=flux2","-p",$prompt,"--cfg-scale","1","--sampling-method","euler","--steps","4","-W","768","-H","432","-t","4","--seed","3106","--output",$target)
Write-Host "Generating SC05 attempt 2 ONLY. Accepted SC01 and SC02 remain untouched."
& $exe @argsList *> $log
if($LASTEXITCODE -ne 0){throw "sd-cli error; see $log"}
if(-not(Test-Path -LiteralPath $target)){throw "No generated SC05 attempt 2"}
$all=@("SC01_attempt1.png","SC02_attempt1.png","SC05_attempt1.png")
foreach($n in $all){Copy-Item -LiteralPath (Join-Path $images $n) -Destination (Join-Path $out $n)}
$check=Join-Path $out "SC05_attempt2.png"
$bytes=[IO.File]::ReadAllBytes($check)
if($bytes.Length -lt 10000 -or $bytes[0] -ne 137 -or $bytes[1] -ne 80){throw "Invalid PNG"}
$zip=Join-Path $downloads "MLI_SC05_RETRY_REVIEW.zip"
Compress-Archive -Path (Join-Path $out "*") -DestinationPath $zip -Force
Write-Host "REVIEW ZIP: $zip" -ForegroundColor Green
