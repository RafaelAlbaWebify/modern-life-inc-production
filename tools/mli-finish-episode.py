#!/usr/bin/env python3
"""Final export for an arbitrary episode using established Soft Karaoke."""
import argparse,datetime,hashlib,importlib.util,json,pathlib,subprocess,sys
def run(cmd,cwd=None):
 cmd=list(cmd)
 if str(cmd[0])=="ffmpeg":cmd.insert(1,"-nostdin")
 p=subprocess.run([str(x) for x in cmd],cwd=cwd,capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr[-2000:])
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--render-folder",required=True);ap.add_argument("--caption-script",required=True)
 args=ap.parse_args();folder=pathlib.Path(args.render_folder).resolve()
 m=json.loads((folder/"manifest.json").read_text(encoding="utf-8"))
 a=json.loads((folder/"alignment.json").read_text(encoding="utf-8"))
 if a.get("episode")!=m["episode_id"] or not a.get("word_aligned") or not a.get("words"):raise ValueError("Missing aligned words for this episode")
 file=pathlib.Path(args.caption_script).resolve()
 spec=importlib.util.spec_from_file_location("mli_caption_styles",str(file))
 mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 ass=folder/"SOFT_KARAOKE.ass"
 ass.write_text(mod.render(a["words"],"karaoke"),encoding="utf-8")
 clean=folder/m["master"];final=folder/(m["episode_id"]+"_SOFT_KARAOKE.mp4")
 run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(clean),"-vf","ass=SOFT_KARAOKE.ass","-map","0:v:0","-map","0:a:0","-c:v","libx264","-threads","2","-preset","veryfast","-crf","20","-c:a","copy","-movflags","+faststart",str(final)],cwd=folder)
 meta={"episode":m["episode_id"],"caption_style":"soft_karaoke","source_master":clean.name,"final_video":final.name,"sha256":hashlib.sha256(final.read_bytes()).hexdigest(),"technical_qc_pending":True,"editorial_approved":False,"publication_approved":False}
 (folder/"finishing_manifest.json").write_text(json.dumps(meta,indent=2)+"\n",encoding="utf-8")
 print("SOFT KARAOKE VIDEO:",final)
if __name__=="__main__":
 try:main()
 except Exception as e:print("FAILED:",e,file=sys.stderr);sys.exit(1)

