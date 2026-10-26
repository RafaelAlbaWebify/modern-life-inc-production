param([string]$Images="",[switch]$ExecuteRetries)
$ErrorActionPreference="Stop";$ProgressPreference="SilentlyContinue"
$base="https://api.github.com/repos/RafaelAlbaWebify/modern-life-inc-production/contents/tools/"
$work=Join-Path $env:TEMP "MLI-Pipeline";New-Item -ItemType Directory -Force $work|Out-Null
foreach($name in @("semantic-qc.py","semantic-retry-plan.py","execute-semantic-retries.py")){
 $r=Invoke-RestMethod -Uri ($base+$name+"?ref=main&v="+[DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()) -Headers @{"Accept"="application/vnd.github+json"}
 [IO.File]::WriteAllBytes((Join-Path $work $name),[Convert]::FromBase64String(($r.content -replace '\s','')))
}
if(-not $Images){
 $g=Get-ChildItem (Join-Path $HOME "Downloads") -Directory -Filter "MLI_ENGINE_GATE_*" |Where-Object {Test-Path (Join-Path $_.FullName "images\SC01_attempt1.png")} |Sort-Object LastWriteTime -Descending|Select-Object -First 1
 if(-not $g){throw "No extracted engine gate images; supply -Images ABSOLUTE_PATH"}
 $Images=Join-Path $g.FullName "images"
}
if(-not(Test-Path -LiteralPath $Images -PathType Container)){throw "Missing images directory $Images"}
$out=Join-Path $HOME ("Downloads\MLI_SEMANTIC_GATE_"+(Get-Date -Format "yyyyMMdd_HHmmss"))
New-Item -ItemType Directory -Force $out|Out-Null
Write-Host "Semantic image evaluation: $Images" -ForegroundColor Cyan
& python (Join-Path $work "semantic-qc.py") --images $Images --out $out
$qcExit=$LASTEXITCODE
$report=Join-Path $out "semantic_report.json"
if(-not(Test-Path $report)){throw "No semantic QC report generated"}
& python (Join-Path $work "semantic-retry-plan.py") --report $report --out (Join-Path $out "retry_plan.json")
if($ExecuteRetries){
 $prompts=Join-Path $HOME "Downloads\MLI_PILOT_001_PROMPTS"
 if(-not(Test-Path (Join-Path $prompts "SC01.txt"))){throw "Prompts missing"}
 & python (Join-Path $work "execute-semantic-retries.py") --plan (Join-Path $out "retry_plan.json") --prompts $prompts --images $Images --logs $out --execute
 if($LASTEXITCODE -ne 0){throw "Selective retry failed; see logs $out"}
 & python (Join-Path $work "semantic-qc.py") --images $Images --out $out
 & python (Join-Path $work "semantic-retry-plan.py") --report (Join-Path $out "semantic_report.json") --out (Join-Path $out "retry_plan.json")
}
Write-Host "Decision and evidence: $out"
Write-Host "Vision code $qcExit ; release remains BLOCKED until human approval."
