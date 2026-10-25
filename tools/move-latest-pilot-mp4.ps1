# Move the latest enhanced pilot MP4 from the source workspace to Downloads.
# PowerShell 7. Uses only enhanced_MLI_PILOT_001_* run folders, never deletes source.
$ErrorActionPreference="Stop"
$root="C:\AI\MLI-FluxTest-Vulkan"
$downloads=Join-Path $HOME "Downloads"
New-Item -ItemType Directory -Force -Path $downloads | Out-Null
$files=@(Get-ChildItem -LiteralPath $root -Directory -Filter "enhanced_MLI_PILOT_001_*" |
  ForEach-Object { Get-ChildItem -LiteralPath $_.FullName -File -Filter "MLI_PILOT_001_ENHANCED.mp4" } |
  Sort-Object LastWriteTime -Descending)
if($files.Count -eq 0){throw "No enhanced pilot MP4 found under $root"}
$file=$files[0]
$target=Join-Path $downloads ("MLI_PILOT_001_ENHANCED_"+$file.Directory.Name+".mp4")
if(Test-Path -LiteralPath $target){throw "Destination already exists: $target"}
Move-Item -LiteralPath $file.FullName -Destination $target -ErrorAction Stop
if(-not(Test-Path -LiteralPath $target) -or (Get-Item -LiteralPath $target).Length -ne $file.Length){throw "Move failed verification"}
Write-Host "Moved latest MP4 to: $target" -ForegroundColor Green
