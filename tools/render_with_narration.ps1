param(
    [string]$Episode = "episodes/MLI-001",
    [string]$Audio = ""
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot

Push-Location $Root
try {
    if (-not $Audio) {
        $Audio = Join-Path $Episode "media\narration.wav"
    }

    if (-not (Test-Path -LiteralPath $Audio)) {
        throw "Narration file not found: $Audio"
    }

    python .\tools\validate_audio.py --audio $Audio
    if ($LASTEXITCODE -ne 0) { throw "Narration validation failed" }
    python .\tools\build_production_manifest.py --episode $Episode
    if ($LASTEXITCODE -ne 0) { throw "Manifest generation failed" }
    python .\renderer\render_episode.py --episode $Episode --allow-placeholders --audio $Audio --output output\rough_cut_with_voice.mp4
    if ($LASTEXITCODE -ne 0) { throw "Renderer failed" }

    $Out = Join-Path $Root "$Episode\output\rough_cut_with_voice.mp4"
    if (-not (Test-Path -LiteralPath $Out)) {
        throw "Expected output not created: $Out"
    }

    @'
import json, subprocess, sys
from pathlib import Path
ep = Path(sys.argv[1])
wav = Path(sys.argv[2])
out = ep / "output" / "rough_cut_with_voice.mp4"
manifest = json.loads((ep / "production_manifest.json").read_text(encoding="utf-8"))
expected = sum(float(s["duration_sec"]) for s in manifest["scenes"])
def probe(p):
    return json.loads(subprocess.check_output(["ffprobe","-v","error","-show_format","-show_streams","-of","json",str(p)]))
v = probe(out)
a = probe(wav)
vs = [s for s in v["streams"] if s["codec_type"] == "video"]
aus = [s for s in v["streams"] if s["codec_type"] == "audio"]
actual = float(v["format"]["duration"])
source = float(a["format"]["duration"])
assert len(manifest["scenes"]) == 56
assert len(vs) == 1 and len(aus) == 1
assert int(vs[0]["width"]) == 1920 and int(vs[0]["height"]) == 1080
assert aus[0]["codec_name"] == "aac"
assert abs(source-expected) <= 1.0, f"Narration {source:.3f}s vs manifest {expected:.3f}s"
assert abs(actual-expected) <= 1.0, f"MP4 {actual:.3f}s vs manifest {expected:.3f}s"
print(f"[PASS] 56 scenes, WAV {source:.3f}s, MP4 {actual:.3f}s, AAC, 1920x1080")
'@ | python - $Episode $Audio
    if ($LASTEXITCODE -ne 0) { throw "Final audio/video verification failed" }

    Write-Host "[PASS] Rough cut with narration created:" -ForegroundColor Green
    Write-Host $Out
}
finally {
    Pop-Location
}
