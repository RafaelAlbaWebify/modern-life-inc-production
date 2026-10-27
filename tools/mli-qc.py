#!/usr/bin/env python3
"""Verify an existing MLI render; no GPU, no paid API, no implicit publication approval."""
import argparse, hashlib, json, pathlib, subprocess, sys
SCENES=tuple(f"SC{i:02}" for i in range(1,7))
def probe(path):
 p=subprocess.run(["ffprobe","-v","error","-show_format","-show_streams","-of","json",str(path)],capture_output=True,text=True)
 if p.returncode:raise RuntimeError("ffprobe failed: "+p.stderr[-1000:])
 return json.loads(p.stdout)
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--folder",required=True,help="Render folder with segments and MP4")
 p.add_argument("--master",default="MLI_PILOT_001_ENHANCED.mp4")
 p.add_argument("--json",default="technical_qc.json")
 a=p.parse_args();folder=pathlib.Path(a.folder).expanduser().resolve()
 master=folder/a.master
 if not master.is_file():raise FileNotFoundError(master)
 issues=[];details={}
 def check(path,label):
  if not path.is_file() or path.stat().st_size<1000:
   issues.append(label+": missing/empty");return None
  try:return probe(path)
  except Exception as e:issues.append(label+": "+str(e));return None
 for sid in SCENES:
  info=check(folder/(sid+".mp4"),sid)
  if info:
   vs=[s for s in info["streams"] if s["codec_type"]=="video"]
   aud=[s for s in info["streams"] if s["codec_type"]=="audio"]
   if not vs or not aud:issues.append(sid+": missing audio/video")
   details[sid]={"duration":float(info["format"].get("duration",0)),"has_audio":bool(aud),"has_video":bool(vs)}
 m=check(master,"master")
 if m:
  aud=[s for s in m["streams"] if s["codec_type"]=="audio"]
  vs=[s for s in m["streams"] if s["codec_type"]=="video"]
  if not aud or not vs:issues.append("master: missing audio/video")
  elif (vs[0].get("width"),vs[0].get("height"))!=(1920,1080):issues.append("master: not 1080p")
  duration=float(m["format"]["duration"])
  if duration<5 or duration>600:issues.append("master: implausible duration")
  if details and abs(sum(x["duration"] for x in details.values())-duration)>0.4:issues.append("master: segment duration mismatch")
  decode=subprocess.run(["ffmpeg","-hide_banner","-v","error","-i",str(master),"-f","null","-"],capture_output=True,text=True)
  if decode.returncode:issues.append("master: decode failed "+decode.stderr[-1000:])
  details["master"]={"duration":duration,"sha256":hashlib.sha256(master.read_bytes()).hexdigest(),"video_codec":vs[0].get("codec_name") if vs else None,"audio_codec":aud[0].get("codec_name") if aud else None}
 srt=folder/"MLI_PILOT_001_CAPTIONS_ESTIMATED.srt"
 if not srt.exists():issues.append("subtitles: missing")
 manifest=folder/"manifest.json"
 if not manifest.exists():issues.append("manifest: missing")
 result={"technical_pass":not issues,"editorial_approved":False,"publication_approved":False,"issues":issues,"media":details,"known_editorial_risks":["SC06 is not yet creatively approved","Subtitles are estimated, not word-aligned","Narration subjective listening not verified"]}
 (folder/a.json).write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
 print(json.dumps(result,indent=2,ensure_ascii=False))
 if issues:sys.exit(1)
if __name__=="__main__":
 try:main()
 except Exception as e:print("FAILED:",e,file=sys.stderr);sys.exit(1)
