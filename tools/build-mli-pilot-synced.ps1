param([string]$Root="C:\AI\MLI-FluxTest-Vulkan",[string]$AudioDir="",[double]$PauseSeconds=0.35)
$ErrorActionPreference="Stop"
if(-not $AudioDir){$AudioDir=Join-Path $Root "pilot_audio"}
if($PauseSeconds -lt 0 -or $PauseSeconds -gt 3){throw "PauseSeconds out of range"}
foreach($c in @("ffmpeg","ffprobe")){if(-not(Get-Command $c -ErrorAction SilentlyContinue)){throw "Missing $c"}}
$orig=Join-Path $Root "story_consistency_20261024_210606"
$rev=Join-Path $Root "story_consistency_revised"
$scenes=@(
@{id="SC01";img=(Join-Path $orig "SC01.png")},
@{id="SC02";img=(Join-Path $orig "SC02.png")},
@{id="SC03";img=(Join-Path $rev "SC03_V2.png")},
@{id="SC04";img=(Join-Path $rev "SC04_V2.png")},
@{id="SC05";img=(Join-Path $orig "SC05.png")},
@{id="SC06";img=(Join-Path $rev "SC06_V2.png")}
)
$ci=[Globalization.CultureInfo]::InvariantCulture
foreach($s in $scenes){
 $s.wav=Join-Path $AudioDir "$($s.id).wav"
 foreach($f in @($s.img,$s.wav)){if(-not(Test-Path -LiteralPath $f -PathType Leaf) -or (Get-Item $f).Length -lt 1000){throw "Missing or empty: $f"}}
 $wh=& ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 $s.img
 if($LASTEXITCODE -ne 0 -or $wh.Trim() -ne "768,432"){throw "Wrong image: $($s.id), $wh"}
 $raw=(& ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $s.wav | Select-Object -First 1)
 $d=0.0
 if($LASTEXITCODE -ne 0 -or -not [double]::TryParse($raw,[Globalization.NumberStyles]::Float,$ci,[ref]$d) -or $d -le 0){throw "Invalid WAV: $($s.wav)"}
 $s.duration=$d
}
$folder=Join-Path $Root ("synced_MLI_PILOT_001_"+(Get-Date -Format "yyyyMMdd_HHmmss"))
New-Item -ItemType Directory -Path $folder -ErrorAction Stop | Out-Null
$lines=@("ffconcat version 1.0")
$report=@()
for($i=0;$i -lt $scenes.Count;$i++){
 $s=$scenes[$i]
 $pause=if($i -eq 5){0.0}else{$PauseSeconds}
 $length=($s.duration+$pause).ToString("0.000000",$ci)
 $gap=$pause.ToString("0.000000",$ci)
 $segment=Join-Path $folder "$($s.id).mp4"
 Write-Host "Rendering $($s.id) : $length seconds"
 & ffmpeg -hide_banner -loglevel error -y -framerate 30 -loop 1 -i $s.img -i $s.wav -map 0:v:0 -map 1:a:0 -vf "scale=1920:1080:flags=lanczos,setsar=1,format=yuv420p" -af "aresample=24000,aformat=sample_fmts=fltp:channel_layouts=mono,apad=pad_dur=$gap" -t $length -r 30 -c:v libx264 -preset veryfast -crf 20 -c:a aac -b:a 192k -ar 24000 -ac 1 $segment
 if($LASTEXITCODE -ne 0 -or -not(Test-Path $segment) -or (Get-Item $segment).Length -le 1000){throw "Failed $($s.id); files preserved in $folder"}
 $p=$segment.Replace("\","/")
 if($p.Contains("'")){throw "Quote in path unsupported"}
 $lines+="file '$p'"
 $report += [pscustomobject]@{scene=$s.id;image=$s.img;wav=$s.wav;audio_seconds=[math]::Round($s.duration,3);pause_seconds=$pause;total_seconds=[math]::Round($s.duration+$pause,3)}
}
$concat=Join-Path $folder "segments.ffconcat"
$lines|Set-Content -LiteralPath $concat -Encoding utf8
$report|ConvertTo-Json -Depth 4|Set-Content -LiteralPath (Join-Path $folder "synced_manifest.json") -Encoding utf8
$mp4=Join-Path $folder "MLI_PILOT_001_SYNCED.mp4"
& ffmpeg -hide_banner -loglevel error -y -f concat -safe 0 -i $concat -map 0:v:0 -map 0:a:0 -c copy -movflags +faststart $mp4
if($LASTEXITCODE -ne 0 -or -not(Test-Path $mp4) -or (Get-Item $mp4).Length -le 1000){throw "Concat failed; segments preserved"}
$actual=(& ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $mp4|Select-Object -First 1)
if($LASTEXITCODE -ne 0 -or -not $actual){throw "MP4 probe failed"}
Write-Host "SYNCED ROUGH CUT CREATED - NOT FINAL QC" -ForegroundColor Green
Write-Host "MP4: $mp4"
Write-Host "Duration: $actual seconds"
$report|Format-Table -AutoSize
