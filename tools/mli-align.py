#!/usr/bin/env python3
"""Forced-align existing MLI script to actual WAV files using local WhisperX (CPU).
Install separately: python -m pip install whisperx
No ASR transcript substitution, no paid API, no silent estimated subtitle fallback.
"""
import argparse, json, pathlib, re, subprocess, sys
from importlib.util import spec_from_file_location, module_from_spec
SCENES=[f"SC{i:02}" for i in range(1,7)]
def duration(p):
 r=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",str(p)],capture_output=True,text=True)
 if r.returncode:raise RuntimeError("ffprobe failed for "+str(p))
 return float(r.stdout.strip())
def stamp(s):
 m=round(s*1000);h,m=divmod(m,3600000);minute,m=divmod(m,60000);sec,ms=divmod(m,1000)
 return f"{h:02}:{minute:02}:{sec:02},{ms:03}"
def groups(words,max_words=7,max_chars=49):
 current=[];out=[]
 for w in words:
  candidate=current+[w]
  if current and (len(candidate)>max_words or len(" ".join(x["word"] for x in candidate))>max_chars):
   out.append(current);current=[w]
  else:current=candidate
 if current:out.append(current)
 return out
def build(whisperx,audio,scene_text,clipdurations):
 align_model,metadata=whisperx.load_align_model(language_code="en",device="cpu")
 all_words=[];offset=0.0;summary=[]
 for i,sid in enumerate(SCENES):
  wav=audio/(sid+".wav")
  if not wav.is_file():raise FileNotFoundError(wav)
  sound=whisperx.load_audio(str(wav))
  length=duration(wav)
  sample=[{"start":0.0,"end":length,"text":scene_text[sid]}]
  aligned=whisperx.align(sample,align_model,metadata,sound,"cpu",return_char_alignments=False)
  words=[{"word":w.get("word","").strip(),"start":w.get("start"),"end":w.get("end")} for w in aligned["word_segments"] if w.get("word","").strip()]
  if not words or any(not isinstance(w["start"],(float,int)) or not isinstance(w["end"],(float,int)) or w["end"]<=w["start"] for w in words):
   raise ValueError("Missing/invalid word alignment for "+sid)
  for w in words:
   if w["start"]<0 or w["end"]>length+0.2:raise ValueError("Out-of-range word: "+sid)
   all_words.append({"scene":sid,"word":w["word"],"start":offset+w["start"],"end":offset+w["end"]})
  summary.append({"scene":sid,"words_aligned":len(words),"audio_duration":length,"timeline_offset":offset})
  offset+=clipdurations[i]
 return all_words,summary
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--audio-dir",required=True);p.add_argument("--render-folder",required=True)
 p.add_argument("--builder",required=True,help="Exact existing narration dictionary source")
 a=p.parse_args()
 try:import whisperx
 except ImportError as e:raise RuntimeError("Install local WhisperX first: python -m pip install whisperx") from e
 src=pathlib.Path(a.builder);spec=spec_from_file_location("mli_builder",str(src));mod=module_from_spec(spec);spec.loader.exec_module(mod)
 audio=pathlib.Path(a.audio_dir);render=pathlib.Path(a.render_folder)
 clipdurations=[duration(render/(sid+".mp4")) for sid in SCENES]
 words,scenes=build(whisperx,audio,mod.NARRATION,clipdurations)
 chunks=[]
 for sid in SCENES:
  scene_words=[w for w in words if w["scene"]==sid]
  chunks.extend(groups(scene_words))
 lines=[]
 for i,chunk in enumerate(chunks,1):
  start=chunk[0]["start"];end=chunk[-1]["end"]
  lines.append(f"{i}\n{stamp(start)} --> {stamp(end)}\n"+" ".join(w["word"] for w in chunk)+"\n\n")
 srt=render/"MLI_PILOT_001_CAPTIONS_ALIGNED.srt"
 srt.write_text("".join(lines),encoding="utf-8")
 record={"method":"WhisperX forced alignment of known script against scene WAV","word_aligned":True,"source_audio_dir":str(audio),"scenes":scenes,"words":words,"srt":str(srt),"editorial_approved":False}
 (render/"alignment.json").write_text(json.dumps(record,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
 print("ALIGNED",len(words),"words;",len(chunks),"captions;",str(srt))
if __name__=="__main__":
 try:main()
 except Exception as exc:print("FAILED:",exc,file=sys.stderr);sys.exit(1)
