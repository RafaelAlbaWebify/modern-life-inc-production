#!/usr/bin/env python3
"""Repeatable, non-destructive final cut of an accepted six-scene render.
SC06 replacement is explicit; never silently approve creative artwork.
Optional aligned subtitle burn-in requires an existing aligned SRT.
"""
import argparse,datetime,hashlib,json,pathlib,shutil,subprocess,sys,importlib.util
SCENES=[f"SC{i:02}" for i in range(1,7)]
def run(*cmd):
 p=subprocess.run([str(x) for x in cmd],capture_output=True,text=True)
 if p.returncode:raise RuntimeError(str(cmd[0])+": "+p.stderr[-1600:])
 return p.stdout
def media(p):
 return json.loads(run("ffprobe","-v","error","-of","json","-show_format","-show_streams",p))
def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--source-folder",required=True)
 ap.add_argument("--scene06-image",required=True)
 ap.add_argument("--aligned-srt",required=True)
 ap.add_argument("--alignment",required=True)
 ap.add_argument("--caption-style",choices=["karaoke","amber","cinematic"],default="karaoke")
 ap.add_argument("--caption-script",required=True)
 ap.add_argument("--output-root",default=str(pathlib.Path.home()/"Downloads"))
 a=ap.parse_args()
 origin=pathlib.Path(a.source_folder).resolve()
 replacement=pathlib.Path(a.scene06_image).resolve()
 captions=pathlib.Path(a.aligned_srt).resolve()
 word_alignment=pathlib.Path(a.alignment).resolve()
 for p in [replacement,captions,word_alignment,pathlib.Path(a.caption_script)]+[origin/(sid+".mp4") for sid in SCENES]:
  if not p.is_file():raise FileNotFoundError(p)
 image_stream=[x for x in media(replacement)["streams"] if x["codec_type"]=="video"]
 if not image_stream:raise ValueError("SC06 image has no visual stream")
 if len(captions.read_text(encoding="utf-8-sig").strip())<40:raise ValueError("Aligned SRT empty")
 folder=pathlib.Path(a.output_root).expanduser().resolve()/("MLI_FINAL_"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
 folder.mkdir(parents=True)
 clips=[]
 for sid in SCENES:
  source=origin/(sid+".mp4");dest=folder/(sid+".mp4")
  if sid!="SC06":shutil.copy2(source,dest)
  else:
   dur=float(media(source)["format"]["duration"])
   run("ffmpeg","-hide_banner","-loglevel","error","-y","-loop","1","-framerate","30","-i",replacement,"-i",source,
       "-map","0:v:0","-map","1:a:0","-vf","scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p",
       "-t",f"{dur:.6f}","-c:v","libx264","-crf","20","-preset","veryfast","-r","30","-c:a","copy",dest)
  clips.append(dest)
 concat=folder/"segments.ffconcat"
 concat.write_text("ffconcat version 1.0\n"+"\n".join("file '"+p.as_posix().replace("'","\\'")+"'" for p in clips)+"\n",encoding="utf-8")
 clean=folder/"MLI_PILOT_FINAL_CLEAN.mp4"
 run("ffmpeg","-hide_banner","-loglevel","error","-y","-safe","0","-f","concat","-i",concat,"-c","copy","-movflags","+faststart",clean)
 aligned=folder/"MLI_PILOT_FINAL_ALIGNED.srt";shutil.copy2(captions,aligned)
 spec=importlib.util.spec_from_file_location("mli_captions",a.caption_script)
 capmodule=importlib.util.module_from_spec(spec);spec.loader.exec_module(capmodule)
 timing=json.loads(word_alignment.read_text(encoding="utf-8"))
 words=timing.get("words",[])
 if len(words)<50 or len(timing.get("scenes",[]))!=6:raise ValueError("Incomplete word timing")
 ass=folder/"MLI_CAPTIONS.ass"
 ass.write_text(capmodule.render(words,a.caption_style),encoding="utf-8")
 master=folder/"MLI_PILOT_FINAL_SUBTITLED.mp4"
 # FFmpeg subtitle filter escaping is difficult on Windows; use current directory for safely relative filter path.
 p=subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(clean),"-vf","ass=MLI_CAPTIONS.ass",
                   "-c:v","libx264","-preset","veryfast","-crf","20","-c:a","copy",str(master)],cwd=str(folder),capture_output=True,text=True)
 if p.returncode:raise RuntimeError("Subtitle burn failed. Check ffmpeg libass support: "+p.stderr[-1500:])
 meta=media(master)
 if not any(x["codec_type"]=="audio" for x in meta["streams"]):raise ValueError("Rendered master missing audio")
 record={"rendered":True,"technical_qc_pending":True,"editorial_approved":False,"publication_approved":False,
         "source_folder":str(origin),"SC06_override":str(replacement),"SC06_sha256":hashlib.sha256(replacement.read_bytes()).hexdigest(),
         "captions_method":"WhisperX word-level ASS","caption_style":a.caption_style,"caption_ass":str(ass),"source_srt":str(captions),"render":str(master)}
 (folder/"final_manifest.json").write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8")
 print("FINAL PREVIEW:",master,"\nMANIFEST:",folder/"final_manifest.json")
if __name__=="__main__":
 try:main()
 except Exception as exc:print("FAILED:",exc,file=sys.stderr);sys.exit(1)
