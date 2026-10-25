# MLI_PILOT_001 rough-cut builder. PowerShell 7; ffmpeg and ffprobe required.
param(
  [string]$Root = "C:\AI\MLI-FluxTest-Vulkan",
  [string]$NarrationWav = "",
  [int]$SilentDurationSec = 60
)
$ErrorActionPreference = "Stop"
$original = Join-Path $Root "story_consistency_20261024_210606"
$revised = Join-Path $Root "story_consistency_revised"
$scenes = @(
  @{Id="SC01";Source=(Join-Path $original "SC01.png")},
  @{Id="SC02";Source=(Join-Path $original "SC02.png")},
  @{Id="SC03";Source=(Join-Path $revised "SC03_V2.png")},
  @{Id="SC04";Source=(Join-Path $revised "SC04_V2.png")},
  @{Id="SC05";Source=(Join-Path $original "SC05.png")},
  @{Id="SC06";Source=(Join-Path $revised "SC06_V2.png")}
)
foreach($cmd in @("ffmpeg","ffprobe")) {
  if(-not (Get-Command $cmd -ErrorAction SilentlyContinue)) { throw "Missing $cmd; no render attempted" }
}
foreach($s in $scenes) {
  if(-not (Test-Path -LiteralPath $s.Source -PathType Leaf)) { throw "Missing image $($s.Id): $($s.Source)" }
  if((Get-Item -LiteralPath $s.Source).Length -eq 0) { throw "Empty image: $($s.Id)" }
  $res = (& ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 $s.Source) | Select-Object -First 1
  if($LASTEXITCODE -ne 0 -or $res.Trim() -ne "768,432") { throw "Invalid dimensions for $($s.Id): $res" }
}
$hasAudio = -not [string]::IsNullOrWhiteSpace($NarrationWav)
if($hasAudio) {
  if(-not (Test-Path -LiteralPath $NarrationWav -PathType Leaf)) { throw "WAV not found: $NarrationWav" }
  $raw = (& ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $NarrationWav) | Select-Object -First 1
  if($LASTEXITCODE -ne 0) { throw "Cannot probe WAV" }
  $duration = 0.0
  if(-not [double]::TryParse(($raw -replace ",","."),[Globalization.NumberStyles]::Float,[Globalization.CultureInfo]::InvariantCulture,[ref]$duration)) { throw "Invalid WAV duration: $raw" }
} else {
  $duration = [double]$SilentDurationSec
}
if($duration -le 0) { throw "Invalid duration" }
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$dest = Join-Path $Root "roughcut_MLI_PILOT_001_$stamp"
if(Test-Path $dest) { throw "Folder already exists: $dest" }
New-Item -ItemType Directory -Path $dest | Out-Null
$staged = Join-Path $dest "frames"
New-Item -ItemType Directory -Path $staged | Out-Null
$concat = Join-Path $dest "scenes.ffconcat"
$lines = @("ffconcat version 1.0")
$manifest = @()
$seconds = $duration / $scenes.Count
foreach($s in $scenes) {
  $target = Join-Path $staged "$($s.Id).png"
  Copy-Item -LiteralPath $s.Source -Destination $target
  $unixPath = $target.Replace("\","/")
  if($unixPath.Contains("'")) { throw "Unsupported apostrophe in output path" }
  $lines += "file '$unixPath'"
  $lines += "duration $($seconds.ToString('0.000000',[Globalization.CultureInfo]::InvariantCulture))"
  $manifest += [pscustomobject]@{scene=$s.Id;source=$s.Source;staged=$target;duration_sec=[math]::Round($seconds,3)}
}
$last = (Join-Path $staged "SC06.png").Replace("\","/")
$lines += "file '$last'"
$lines | Set-Content -LiteralPath $concat -Encoding utf8
$manifest | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $dest "manifest.json") -Encoding utf8
$mp4 = Join-Path $dest "MLI_PILOT_001_ROUGHCUT.mp4"
$argsVideo = @("-hide_banner","-loglevel","error","-y","-safe","0","-f","concat","-i",$concat)
if($hasAudio) {
  $argsVideo += @("-i",$NarrationWav,"-map","0:v:0","-map","1:a:0")
} else {
  $argsVideo += @("-map","0:v:0")
}
$argsVideo += @("-vf","scale=1920:1080:flags=lanczos,setsar=1,fps=30,format=yuv420p","-c:v","libx264","-preset","veryfast","-crf","20","-t",$duration.ToString("0.000",[Globalization.CultureInfo]::InvariantCulture))
if($hasAudio) { $argsVideo += @("-c:a","aac","-b:a","192k","-shortest") }
$argsVideo += @($mp4)
& ffmpeg @argsVideo
if($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $mp4 -PathType Leaf) -or (Get-Item $mp4).Length -le 0) { throw "FFmpeg render failed, staging preserved at $dest" }
$actual = (& ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $mp4) | Select-Object -First 1
if($LASTEXITCODE -ne 0) { throw "MP4 exists but ffprobe could not validate duration" }
Write-Host "ROUGH CUT CREATED; NOT FINAL QC" -ForegroundColor Green
Write-Host "MP4: $mp4"
Write-Host "Duration: $actual seconds"
Write-Host "Narration included: $hasAudio"
Write-Host "Manifest: $(Join-Path $dest 'manifest.json')"
