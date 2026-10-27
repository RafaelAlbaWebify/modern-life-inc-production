#!/usr/bin/env python3
"""General episode alignment, using existing WAVs, rendered clip timing and known scripts.
Requires local WhisperX in its isolated virtualenv; never replaces failed alignment with guesses.
"""
import argparse,json,pathlib,subprocess,sys
def probe(p):
 c=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",str(p)],capture_output=True,text=True)
 if c.returncode:raise RuntimeError(c.stderr)
 return float(c.stdout.strip())
def stamp(sec):
 n=round(sec*1000);h,n=divmod(n,3600000);m,n=divmod(n,60000);s,ms=divmod(n,1000)
 return f"{h:02}:{m:02}:{s:02},{ms:03}"
def main():
 a=argparse.ArgumentParser();a.add_argument("--work",required=True);a.add_argument("--render-folder",required=True)
 args=a.parse_args();work=pathlib.Path(args.work).resolve();folder=pathlib.Path(args.render_folder).resolve()
 contract=json.loads((work/"contract.json").read_text(encoding="utf-8"))
 manifest=json.loads((folder/"manifest.json").read_text(encoding="utf-8"))
 scenes=contract["scenes"]
 if [s["id"] for s in scenes]!=[s["scene"] for s in manifest["scenes"]]:raise ValueError("Scene order mismatch")
 try:import whisperx
 except ImportError as e:raise RuntimeError("WhisperX not installed in selected Python environment") from e
 model,meta=whisperx.load_align_model(language_code="en",device="cpu")
 words=[];report=[]
 for scene,clip in zip(scenes,manifest["scenes"]):
  sid=scene["id"];wav=work/"audio"/(sid+".wav")
  length=probe(wav)
  sound=whisperx.load_audio(str(wav))
  result=whisperx.align([{"start":0,"end":length,"text":scene["beat"]}],model,meta,sound,"cpu",return_char_alignments=False)
  segment_words=[x for x in result["word_segments"] if x.get("word","").strip()]
  if not segment_words:raise ValueError(f"Missing aligned words for {sid}")
  for w in segment_words:
   start=w.get("start");end=w.get("end")
   if not isinstance(start,(int,float)) or not isinstance(end,(int,float)) or not 0<=start<end<=length+0.25:
    raise ValueError(f"Unaligned or invalid word for {sid}: {w}")
   words.append({"scene":sid,"word":w["word"].strip(),"start":round(start+clip["timeline_start"],4),"end":round(end+clip["timeline_start"],4)})
  report.append({"scene":sid,"word_count":len(segment_words),"audio_duration":length,"offset":clip["timeline_start"]})
  print("ALIGNED",sid,len(segment_words),"words",flush=True)
 data={"episode":contract["episode_id"],"word_aligned":True,"scenes":report,"words":words,"publication_approved":False}
 (folder/"alignment.json").write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
 # SRT kept as accessible companion; ASS styling uses word timings directly.
 lines=[]
 for i,word in enumerate(words,1):
  lines.append(f"{i}\n{stamp(word['start'])} --> {stamp(word['end'])}\n{word['word']}\n\n")
 (folder/"captions_words.srt").write_text("".join(lines),encoding="utf-8")
 print("ALIGNED TOTAL",len(words),"words")
if __name__=="__main__":
 try:main()
 except Exception as e:print("FAILED:",e,file=sys.stderr);sys.exit(1)
