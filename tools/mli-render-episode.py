#!/usr/bin/env python3
"""Episode-agnostic renderer. Only accepted PNGs and recorded WAVs; no generation."""
import argparse,json,pathlib,subprocess,datetime,sys,hashlib
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
 clips=[];report=[];offset=0.0
 for i,(sid,img,wav,duration) in enumerate(entries):
  pause=args.pause if i<len(entries)-1 else 0
  target=folder/(sid+".mp4")
  run(["ffmpeg","-hide_banner","-loglevel","error","-y","-loop","1","-framerate","30","-i",img,"-i",wav,
       "-map","0:v:0","-map","1:a:0","-vf","scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p",
       "-af",f"aresample=24000,apad=pad_dur={pause:.3f}","-t",f"{duration+pause:.6f}",
       "-c:v","libx264","-preset","veryfast","-crf","20","-r","30","-c:a","aac","-b:a","192k","-ar","24000","-ac","1",target])
  measured=validate_media(target,duration+pause,full_decode=True)
  report.append({"scene":sid,"audio_seconds":duration,"clip_seconds":measured,"timeline_start":offset,"pause":pause})
  offset+=measured;clips.append(target)
 concat=folder/"segments.ffconcat"
 # use relative basenames, all clips in same folder
 concat.write_text("ffconcat version 1.0\n"+"\n".join(f"file '{clip.name}'" for clip in clips)+"\n",encoding="utf-8")
 master=folder/(contract["episode_id"]+"_CLEAN.mp4")
 run(["ffmpeg","-hide_banner","-loglevel","error","-y","-safe","0","-f","concat","-i",concat,"-c","copy","-movflags","+faststart",master],cwd=folder)
 master_duration=validate_media(master,offset,full_decode=True)
 manifest={"episode_id":contract["episode_id"],"status":"technical_render_only","editorial_approved":False,"publication_approved":False,"scene_count":len(clips),"scenes":report,"master":master.name,"duration":master_duration,"master_sha256":hashlib.sha256(master.read_bytes()).hexdigest()}
 (folder/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
 print("RENDER:",master);print("SCENES:",len(clips));print("NOT EDITORIALLY APPROVED")
if __name__=="__main__":
 try:main()
 except Exception as e:print("FAILED:",e,file=sys.stderr);sys.exit(1)

