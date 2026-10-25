#!/usr/bin/env python3
"""Modern Life Inc pilot: narratively directed selective movement, optional licensed music, SRT captions.
Windows Python 3.10+ standard library, FFmpeg + FFprobe in PATH.
Existing VoiceStudio SC01.wav .. SC06.wav; no speech/image regeneration.
"""
import argparse
import datetime
import json
import math
import pathlib
import re
import subprocess
import sys

NARRATION = {
 "SC01": "Every notification feels urgent. A friend needs a favor. A client wants a quick answer. So you reply, even when you're exhausted.",
 "SC02": "Soon you're checking your phone everywhere, afraid that taking too long to respond might disappoint someone.",
 "SC03": "But being reachable every minute can quietly turn your time into something people expect rather than appreciate.",
 "SC04": "The change begins when you put the phone down. You don't have to explain every moment of silence.",
 "SC05": "Decide what deserves your attention. Reply when you're available, not simply whenever a message arrives.",
 "SC06": "Boundaries aren't about caring less. They're how you protect the time and energy that let you care well.",
}
SCENES = (
 ("SC01", "story_consistency_20261024_210606/SC01.png"),
 ("SC02", "story_consistency_20261024_210606/SC02.png"),
 ("SC03", "story_consistency_revised/SC03_V2.png"),
 ("SC04", "story_consistency_revised/SC04_V2.png"),
 ("SC05", "story_consistency_20261024_210606/SC05.png"),
 ("SC06", "story_consistency_revised/SC06_V2.png"),
)

def run(*args):
    proc = subprocess.run([str(x) for x in args], text=True, capture_output=True)
    if proc.returncode:
        raise RuntimeError(f"Command failed ({proc.returncode}): {' '.join(map(str,args))}\n{proc.stderr[-4000:]}")
    return proc.stdout.strip()

def media_info(path):
    return json.loads(run("ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", path))

def stamp(seconds):
    milliseconds = round(seconds * 1000)
    h, r = divmod(milliseconds, 3600000)
    m, r = divmod(r, 60000)
    s, ms = divmod(r, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def captions(text):
    # Scene-level estimated split, NOT forced word alignment.
    words = text.split()
    mid = len(words) // 2
    return (" ".join(words[:mid]), " ".join(words[mid:]))

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=r"C:\AI\MLI-FluxTest-Vulkan")
    ap.add_argument("--audio-dir", default=None)
    ap.add_argument("--output-dir", default=None, help="Render output parent; defaults to Windows Downloads")
    ap.add_argument("--images-dir", default=None, help="Optional V2 images folder with SC01.png through SC06.png")
    ap.add_argument("--pause", type=float, default=0.25)
    ap.add_argument("--music", default=None, help="Optional locally licensed music file")
    ap.add_argument("--music-volume", type=float, default=0.08, help="Linear amplitude, only if music supplied")
    args = ap.parse_args()
    if not 0 <= args.pause <= 2:
        ap.error("--pause must be 0..2 seconds")
    if not 0 <= args.music_volume <= 0.3:
        ap.error("--music-volume must be 0..0.3")
    root = pathlib.Path(args.root)
    audio = pathlib.Path(args.audio_dir) if args.audio_dir else root / "pilot_audio"
    if args.music and not pathlib.Path(args.music).is_file():
        ap.error("--music file not found")
    # Preflight ALL inputs before rendering.
    items = []
    for scene, img_relative in SCENES:
        image = (pathlib.Path(args.images_dir) / f"{scene}.png") if args.images_dir else (root / img_relative)
        wav = audio / f"{scene}.wav"
        for file in (image, wav):
            if not file.is_file() or file.stat().st_size < 1000:
                raise FileNotFoundError(f"Missing or empty: {file}")
        iv = [s for s in media_info(image)["streams"] if s["codec_type"] == "video"][0]
        if (iv["width"],iv["height"]) not in ((768,432),(1672,941)):
            raise ValueError(f"Unexpected source dimensions: {image}")
        av = media_info(wav)
        streams = [s for s in av["streams"] if s["codec_type"] == "audio"]
        if not streams:
            raise ValueError(f"No audio: {wav}")
        length = float(av["format"]["duration"])
        if not math.isfinite(length) or length < 0.2:
            raise ValueError(f"Invalid duration: {wav}")
        items.append(dict(id=scene,image=image,wav=wav,audio_seconds=length))
    # Output isolation: never create test renders inside the source/model workspace.
    # On Windows, respect OneDrive Known Folder redirection when configured by allowing
    # --output-dir; the default below is the normal user Downloads location.
    output_parent = pathlib.Path(args.output_dir) if args.output_dir else pathlib.Path.home() / "Downloads"
    output_parent.mkdir(parents=True, exist_ok=True)
    folder = output_parent / ("MLI_PILOT_001_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    folder.mkdir(parents=True, exist_ok=False)
    clips = []
    subtitles = []
    position = 0.0
    report = []
    for i, item in enumerate(items):
        scene = item["id"]
        pause = args.pause if i != 5 else 0
        duration = item["audio_seconds"] + pause
        clip = folder / f"{scene}.mp4"
        # Directional motion is editorial, NOT decoration.
        # Only SC04 visually marks "put the phone down": hold still, then
        # make a slow 2% push toward the phone on the rooftop (lower right).
        # Do not animate the other five scenes without a narrative beat map.
        frames = math.ceil(duration * 30)
        if scene == "SC04":
            onset = math.floor(item["audio_seconds"] * 0.55 * 30)
            progress = f"min(max((on-{onset})/{max(1,frames-onset-1)},0),1)"
            # Smoothstep interpolation eliminates abrupt changes in speed.
            ease = f"({progress})*({progress})*(3-2*({progress}))"
            zoom = f"1+0.02*({ease})"
            vf = (
                "scale=1920:1080:flags=lanczos,"
                f"zoompan=z='{zoom}':"
                "x='(iw-iw/zoom)*0.67':y='(ih-ih/zoom)*0.75':"
                "d=1:s=1920x1080:fps=30,format=yuv420p"
            )
        else:
            vf = "scale=1920:1080:flags=lanczos,setsar=1,format=yuv420p"
        run("ffmpeg","-hide_banner","-loglevel","error","-y",
            "-loop","1","-framerate","30","-i",item["image"],
            "-i",item["wav"],"-map","0:v:0","-map","1:a:0",
            "-vf",vf,"-af",f"aresample=24000,apad=pad_dur={pause:.3f}",
            "-t",f"{duration:.6f}","-frames:v",str(frames),
            "-c:v","libx264","-preset","veryfast","-crf","20",
            "-r","30","-pix_fmt","yuv420p",
            "-c:a","aac","-b:a","192k","-ar","24000","-ac","1",clip)
        if not clip.is_file() or clip.stat().st_size < 1000:
            raise RuntimeError(f"Empty segment: {scene}")
        clips.append(clip)
        chunks = captions(NARRATION[scene])
        # Caption timing is estimated within each audio scene, not ASR-aligned.
        t0 = position + 0.15
        t1 = position + 0.50*item["audio_seconds"]
        t2 = position + max(0.2,item["audio_seconds"] - 0.1)
        if t0 < t1 < t2:
            subtitles.extend([(t0,t1,chunks[0]),(t1,t2,chunks[1])])
        report.append(dict(scene=scene,image=str(item["image"]),wav=str(item["wav"]),
            wav_duration=round(item["audio_seconds"],3),pause=round(pause,3),
            estimated_start=round(position,3),expected_scene_duration=round(duration,3)))
        position += duration
        print(f"Rendered {scene}: {duration:.2f}s",flush=True)
    concat = folder/"segments.ffconcat"
    def escape_concat(p):
        value = p.as_posix()
        if "'" in value: raise ValueError("Apostrophe in file path not supported")
        return f"file '{value}'"
    concat.write_text("ffconcat version 1.0\n"+"\n".join(map(escape_concat,clips))+"\n",encoding="utf-8")
    silent_musicless = folder/"MLI_PILOT_001_MOTION_NO_MUSIC.mp4"
    run("ffmpeg","-hide_banner","-loglevel","error","-y","-safe","0",
        "-f","concat","-i",concat,"-c","copy","-movflags","+faststart",silent_musicless)
    srt=folder/"MLI_PILOT_001_CAPTIONS_ESTIMATED.srt"
    srt.write_text("".join(f"{i}\n{stamp(s)} --> {stamp(e)}\n{txt}\n\n"
                           for i,(s,e,txt) in enumerate(subtitles,1)),encoding="utf-8")
    final = folder/"MLI_PILOT_001_ENHANCED.mp4"
    if args.music:
        run("ffmpeg","-hide_banner","-loglevel","error","-y",
            "-i",silent_musicless,"-stream_loop","-1","-i",args.music,
            "-filter_complex",f"[0:a]aresample=48000[voice];[1:a]aresample=48000,volume={args.music_volume:.3f}[music];[voice][music]amix=inputs=2:duration=first:dropout_transition=0[a]",
            "-map","0:v:0","-map","[a]","-c:v","copy","-c:a","aac",
            "-b:a","192k","-movflags","+faststart","-shortest",final)
    else:
        # Keep actual program audio; no fictitious 'music' claim.
        run("ffmpeg","-hide_banner","-loglevel","error","-y",
            "-i",silent_musicless,"-map","0:v:0","-map","0:a:0",
            "-c","copy","-movflags","+faststart",final)
    result = media_info(final)
    if not any(s["codec_type"]=="audio" for s in result["streams"]):
        raise RuntimeError("Final output has no audio")
    metadata=dict(status="rendered_not_approved",source="existing local WAVs and PNGs",
                  total_measured_duration=float(result["format"]["duration"]),
                  estimated_total_duration=round(position,3),pause_seconds=args.pause,
                  music=str(args.music) if args.music else None,
                  captions="estimated scene-based timings, external SRT; not burnt in",
                  source_resolution="768x432 upscaled to 1920x1080",
                  scenes=report)
    (folder/"manifest.json").write_text(json.dumps(metadata,indent=2),encoding="utf-8")
    print("VIDEO:",final)
    print("SRT:",srt)
    print("MANIFEST:",folder/"manifest.json")
    print("STATUS: RENDERED, NOT QC APPROVED")

if __name__=="__main__":
    try: main()
    except Exception as exc:
        print(f"FAILED: {exc}",file=sys.stderr)
        sys.exit(1)
