#!/usr/bin/env python3
"""Scene-count agnostic FFmpeg technical gate. Never authorizes publication."""
import argparse,pathlib,json,hashlib,subprocess,sys
def execute(args):
 p=subprocess.run([str(x) for x in args],capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr[-1200:])
 return p.stdout
def probe(path):
 return json.loads(execute(["ffprobe","-v","error","-of","json","-show_streams","-show_format",path]))
def main():
 p=argparse.ArgumentParser();p.add_argument("--folder",required=True);a=p.parse_args()
 folder=pathlib.Path(a.folder).resolve()
 manifest=json.loads((folder/"manifest.json").read_text(encoding="utf-8"))
 ids=[row["scene"] for row in manifest["scenes"]]
 issues=[];sizes=[]
 if not ids or len(ids)!=len(set(ids)) or len(ids)!=manifest["scene_count"]:issues.append("Inconsistent scene manifest")
 master=folder/manifest["master"]
 for sid in ids:
  file=folder/(sid+".mp4")
  if not file.is_file():issues.append(sid+" missing");continue
  try:
   info=probe(file)
   kinds={x["codec_type"] for x in info["streams"]}
   if not {"audio","video"}<=kinds:issues.append(sid+" missing stream")
   sizes.append(float(info["format"]["duration"]))
  except Exception as ex:issues.append(sid+" "+str(ex))
 if not master.is_file():issues.append("Master missing")
 else:
  try:
   info=probe(master);streams=info["streams"]
   video=next((x for x in streams if x["codec_type"]=="video"),None)
   audio=next((x for x in streams if x["codec_type"]=="audio"),None)
   if not video or not audio:issues.append("Master missing streams")
   elif (video["width"],video["height"])!=(1920,1080):issues.append("Master dimensions not 1920x1080")
   if abs(sum(sizes)-float(info["format"]["duration"]))>0.5:issues.append("Duration mismatch")
   if hashlib.sha256(master.read_bytes()).hexdigest()!=manifest["master_sha256"]:issues.append("Master SHA mismatch")
   execute(["ffmpeg","-hide_banner","-v","error","-i",master,"-f","null","-"])
  except Exception as ex:issues.append("Master "+str(ex))
 finishing=folder/"finishing_manifest.json"
 if finishing.exists():
  try:
   info=json.loads(finishing.read_text(encoding="utf-8"))
   output=folder/info["final_video"]
   if not output.is_file():issues.append("Soft Karaoke final MP4 missing")
   else:
    finalmeta=probe(output)
    if not any(x["codec_type"]=="audio" for x in finalmeta["streams"]):issues.append("Soft Karaoke MP4 missing audio")
    if hashlib.sha256(output.read_bytes()).hexdigest()!=info["sha256"]:issues.append("Soft Karaoke MP4 hash mismatch")
    execute(["ffmpeg","-hide_banner","-v","error","-i",output,"-f","null","-"])
   if not (folder/"SOFT_KARAOKE.ass").is_file():issues.append("Soft Karaoke ASS missing")
   if not (folder/"alignment.json").is_file():issues.append("Word-level alignment JSON missing")
  except Exception as exc:issues.append("Soft Karaoke verification "+str(exc))
 result={"technical_pass":not issues,"editorial_approved":False,"publication_approved":False,"scene_count":len(ids),"issues":issues}
 (folder/"technical_qc.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(result,indent=2))
 if issues:sys.exit(1)
if __name__=="__main__":
 try:main()
 except Exception as e:print("FAILED:",e,file=sys.stderr);sys.exit(1)
