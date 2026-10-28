#!/usr/bin/env python3
"""Episode-agnostic renderer. Only accepted PNGs and recorded WAVs; no generation."""
import argparse,json,pathlib,subprocess,datetime,sys,hashlib,wave
def run(cmd,cwd=None):
 cmd=list(cmd)
 if str(cmd[0])=="ffmpeg":cmd.insert(1,"-nostdin")
 p=subprocess.run([str(x) for x in cmd],capture_output=True,text=True,cwd=cwd)
 if p.returncode:raise RuntimeError(p.stderr[-2000:])
 return p.stdout
def probe(p):
 return json.loads(run(["ffprobe","-v","error","-show_format","-show_streams","-of","json",p]))
def validate_media(path, expected_duration, full_decode=False):
 info=probe(path)
 kinds={x["codec_type"] for x in info["streams"]}
 if not {"video","audio"}<=kinds:raise ValueError(f"Missing audio/video stream: {path}")
 duration=float(info["format"]["duration"])
 if abs(duration-expected_duration)>0.15:raise ValueError(f"Duration mismatch: {path}: {duration} vs {expected_duration}")
 if full_decode:
  errors=run(["ffmpeg","-hide_banner","-v","error","-xerror","-i",path,"-f","null","-"])
 return duration

def archive_failed_render(target,error):
 folder=target.parent/"render_failures";folder.mkdir(exist_ok=True)
 token=target.stem+"_"+datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
 if target.exists():target.rename(folder/(token+".invalid.mp4"))
 (folder/(token+".json")).write_text(json.dumps({"file":target.name,"error":str(error)},indent=2)+"\n",encoding="utf-8")

def encode_clip(command,target,expected):
 if target.exists():
  try:return validate_media(target,expected,full_decode=True)
  except Exception as error:archive_failed_render(target,error)
 for attempt in range(2):
  try:
   run(command)
   return validate_media(target,expected,full_decode=True)
  except Exception as error:
   archive_failed_render(target,error)
   print("ENCODE FAILURE",target.name,"attempt",attempt+1,"- diagnostic saved in render_failures",flush=True)
   if attempt==1:raise RuntimeError("Clip encoding failed after two attempts: "+target.name) from error

def assemble_narration(entries, report, output):
 """Preserve source speech, placing it at measured clip offsets; encode AAC once."""
 with wave.open(str(output),"wb") as out:
  out.setparams((1,2,24000,0,"NONE","not compressed"))
  for (_,_,wav,_),clip in zip(entries,report):
   source=wav
   with wave.open(str(source),"rb") as original:
    compatible=(original.getnchannels(),original.getsampwidth(),original.getframerate(),original.getcomptype())==(1,2,24000,"NONE")
   if not compatible:
    source=output.parent/(clip["scene"]+"_narration_pcm.wav")
    run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",wav,"-ac","1","-ar","24000","-c:a","pcm_s16le",source])
   start=round(clip["timeline_start"]*24000)
   if abs(out.getnframes()-start)>1:raise ValueError("Narration offset mismatch: "+clip["scene"])
   with wave.open(str(source),"rb") as audio:out.writeframes(audio.readframes(audio.getnframes()))
   end=round((clip["timeline_start"]+clip["clip_seconds"])*24000)
   gap=end-out.getnframes()
   if gap<0:raise ValueError("Narration exceeds measured clip: "+clip["scene"])
   out.writeframes(b"\0"*(gap*2))
 return output

def main():
 a=argparse.ArgumentParser()
 a.add_argument("--work",required=True);a.add_argument("--audio-dir",required=True)
 a.add_argument("--out-root",default=str(pathlib.Path.home()/"Downloads"))
 a.add_argument("--pause",type=float,default=0.25)
 args=a.parse_args()
 if not 0<=args.pause<=2:raise ValueError("pause outside 0..2")
 work=pathlib.Path(args.work).resolve();audio=pathlib.Path(args.audio_dir).resolve()
 contract=json.loads((work/"contract.json").read_text(encoding="utf-8"))
 state=json.loads((work/"state.json").read_text(encoding="utf-8"))
 scene_ids=[s["id"] for s in contract["scenes"]]
 if not scene_ids or len(set(scene_ids))!=len(scene_ids):raise ValueError("Invalid scene IDs")
 if set(scene_ids)!=set(state["shots"]):raise ValueError("Contract and state disagree")
 entries=[]
 for sid in scene_ids:
  item=state["shots"][sid]
  if item["state"]!="CANDIDATE_PASS":raise ValueError(f"{sid}: not accepted")
  image=work/"accepted_images"/(sid+".png")
  wav=audio/(sid+".wav")
  for p in (image,wav):
   if not p.is_file():raise FileNotFoundError(p)
  meta=probe(wav);dur=float(meta["format"]["duration"])
  if dur<0.3:raise ValueError(f"Invalid WAV duration: {sid}")
  entries.append((sid,image,wav,dur))
 folder=pathlib.Path(args.out_root).resolve()/(contract["episode_id"]+"_RENDER_"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
 folder.mkdir(parents=True)
 clips=[];report=[];offset=0.0;commands={}
 for i,(sid,img,wav,duration) in enumerate(entries):
  pause=args.pause if i<len(entries)-1 else 0
  print("ENCODING",sid,f"{i+1}/{len(entries)}",flush=True)
  target=folder/(sid+".mp4")
  command=["ffmpeg","-hide_banner","-loglevel","error","-y","-loop","1","-framerate","30","-i",img,"-i",wav,
       "-map","0:v:0","-map","1:a:0","-vf","scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p",
       "-af",f"aresample=24000,apad=pad_dur={pause:.3f}","-t",f"{duration+pause:.6f}",
       "-c:v","libx264","-threads","2","-preset","veryfast","-crf","20","-r","30","-c:a","aac","-b:a","192k","-ar","24000","-ac","1",target]
  commands[target]=command
  measured=encode_clip(command,target,duration+pause)
  report.append({"scene":sid,"audio_seconds":duration,"clip_seconds":measured,"timeline_start":offset,"pause":pause,"audio_sha256":hashlib.sha256(wav.read_bytes()).hexdigest()})
  offset+=measured;clips.append(target)
 concat=folder/"segments.ffconcat"
 # use relative basenames, all clips in same folder
 concat.write_text("ffconcat version 1.0\n"+"\n".join(f"file '{clip.name}'" for clip in clips)+"\n",encoding="utf-8")
 master=folder/(contract["episode_id"]+"_CLEAN.mp4")
 print("VALIDATING ALL CLIPS BEFORE ASSEMBLY",flush=True)
 # Recheck every closed segment immediately before concatenation.
 offset=0.0
 for clip,row in zip(clips,report):
  measured=encode_clip(commands[clip],clip,row["clip_seconds"])
  row["timeline_start"]=offset;row["clip_seconds"]=measured;offset+=measured
 video_only=folder/"video_only.mp4"
 run(["ffmpeg","-hide_banner","-loglevel","error","-y","-safe","0","-f","concat","-i",concat,"-map","0:v:0","-an","-c:v","copy",video_only],cwd=folder)
 narration=assemble_narration(entries,report,folder/"continuous_narration.wav")
 run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",video_only,"-i",narration,"-map","0:v:0","-map","1:a:0","-c:v","copy","-c:a","aac","-b:a","192k","-ar","24000","-ac","1","-movflags","+faststart",master],cwd=folder)
 master_duration=validate_media(master,offset,full_decode=True)
 manifest={"episode_id":contract["episode_id"],"status":"technical_render_only","editorial_approved":False,"publication_approved":False,"scene_count":len(clips),"audio_assembly":"original PCM on measured clip timeline; one AAC encode","scenes":report,"master":master.name,"duration":master_duration,"master_sha256":hashlib.sha256(master.read_bytes()).hexdigest()}
 (folder/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
 print("RENDER:",master);print("SCENES:",len(clips));print("NOT EDITORIALLY APPROVED")
if __name__=="__main__":
 try:main()
 except Exception as e:print("FAILED:",e,file=sys.stderr);sys.exit(1)


