#!/usr/bin/env python3
"""Generate branded ASS subtitles from verified WhisperX word timing. No paid APIs."""
import argparse,json,pathlib
STYLES={"cinematic":("&H00FFFFFF","&H00FFFFFF"),"amber":("&H00FFFFFF","&H0000ADFF"),"karaoke":("&H00FFFFFF","&H0000ADFF")}
def t(sec):
 n=round(sec*100);h,n=divmod(n,360000);m,n=divmod(n,6000);s,cs=divmod(n,100)
 return f"{h}:{m:02}:{s:02}.{cs:02}"
MAX_WORDS=10
MAX_CHARS=65
MIN_MARGIN_V=135

def groups(words):
 """Prefer sentence punctuation and natural pauses, never split mid-scene."""
 out=[];current=[]
 for i,w in enumerate(words):
  if current and w.get("scene")!=current[-1].get("scene"):
   out.append(current);current=[]
  if current:
   span=" ".join(x["word"] for x in current+[w])
   gap=w["start"]-current[-1]["end"]
   previous=current[-1]["word"]
   natural=previous.endswith((".", "!", "?", ":", ";")) or (previous.endswith(",") and gap>=0.12)
   if gap>0.65 or (natural and len(current)>=3) or len(current)>=MAX_WORDS or len(span)>MAX_CHARS:
    out.append(current);current=[]
  current.append(w)
 if current:out.append(current)
 # Merge tiny orphan captions where safe and within the same scene.
 merged=[]
 for chunk in out:
  if merged and len(chunk)<=2 and merged[-1][-1].get("scene")==chunk[0].get("scene"):
   prev=merged[-1]
   candidate=prev+chunk
   if len(candidate)<=MAX_WORDS and len(" ".join(x["word"] for x in candidate))<=MAX_CHARS and chunk[0]["start"]-prev[-1]["end"]<0.4:
    merged[-1]=candidate;continue
  merged.append(chunk)
 return merged

def split_line(group):
 """Return index for balanced two-line layout without splitting source order."""
 content=[w["word"] for w in group]
 if len(" ".join(content))<=34:return None
 options=range(2,len(content)-1)
 return min(options,key=lambda i:abs(len(" ".join(content[:i]))-len(" ".join(content[i:])))) if options else None

def render(words,style):
 primary,secondary=STYLES[style]
 src=("[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\nWrapStyle: 2\nScaledBorderAndShadow: yes\n\n"
 "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
 f"Style: Main,Arial,60,{primary},{secondary},&H00101720,&H70000000,-1,0,0,0,100,100,0,0,1,3,2,2,140,140,{MIN_MARGIN_V},1\n\n"
 "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
 for g in groups(words):
  line_break=split_line(g)
  if style=="karaoke":
   pos=g[0]["start"];parts=[]
   for j,w in enumerate(g):
    if line_break is not None and j==line_break:parts.append(r"\N")
    gap=max(0,round((w["start"]-pos)*100))
    if gap:parts.append(r"{\k"+str(gap)+"}")
    parts.append(r"{\k"+str(max(1,round((w["end"]-w["start"])*100)))+"}"+w["word"]+" ")
    pos=w["end"]
   txt="".join(parts).rstrip()
  elif style=="amber":
   # Static keyword emphasis only; no claim of word-level karaoke.
   keywords={"boundaries","time","energy","attention","available","care","silence","reply"}
   txt=" ".join((r"{\c&H0000ADFF&}"+w["word"]+r"{\c&H00FFFFFF&}" if w["word"].lower().strip(".,!?") in keywords else w["word"]) for w in g)
  else:txt=" ".join(w["word"] for w in g)
  if style!="karaoke" and line_break is not None:
   raw=txt.split(" ")
   if len(raw)==len(g):txt=" ".join(raw[:line_break])+r"\N"+" ".join(raw[line_break:])
  src+=f"Dialogue: 0,{t(g[0]['start'])},{t(g[-1]['end'])},Main,,0,0,0,,{txt}\n"
 return src
def main():
 p=argparse.ArgumentParser();p.add_argument("--alignment",required=True);p.add_argument("--out",required=True)
 a=p.parse_args();d=json.loads(pathlib.Path(a.alignment).read_text(encoding="utf-8"));words=d.get("words",[])
 if not isinstance(words,list) or len(words)<50 or len(d.get("scenes",[]))!=6:raise ValueError("Alignment incomplete")
 for w in words:
  if not isinstance(w.get("start"),(float,int)) or not isinstance(w.get("end"),(float,int)) or w["end"]<=w["start"]:raise ValueError("Bad word timing")
 out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
 for name in STYLES:(out/(name+".ass")).write_text(render(words,name),encoding="utf-8")
 print("ASS CREATED",len(words),"words",out)
if __name__=="__main__":main()
