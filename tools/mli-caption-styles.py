#!/usr/bin/env python3
"""Generate branded ASS subtitles from verified WhisperX word timing. No paid APIs."""
import argparse,json,pathlib
STYLES={"cinematic":("&H00FFFFFF","&H00FFFFFF"),"amber":("&H00FFFFFF","&H0000ADFF"),"karaoke":("&H00FFFFFF","&H0000ADFF")}
def t(sec):
 n=round(sec*100);h,n=divmod(n,360000);m,n=divmod(n,6000);s,cs=divmod(n,100)
 return f"{h}:{m:02}:{s:02}.{cs:02}"
def groups(words):
 out=[];cur=[]
 for w in words:
  if cur and (len(cur)>=7 or len(" ".join(x["word"] for x in cur+[w]))>43 or w["start"]-cur[-1]["end"]>0.6):
   out.append(cur);cur=[]
  cur.append(w)
 if cur:out.append(cur)
 return out
def render(words,style):
 primary,secondary=STYLES[style]
 src=("[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\nWrapStyle: 2\nScaledBorderAndShadow: yes\n\n"
 "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
 f"Style: Main,Arial,60,{primary},{secondary},&H00101720,&H70000000,-1,0,0,0,100,100,0,0,1,3,2,2,140,140,85,1\n\n"
 "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
 for g in groups(words):
  if style=="karaoke":
   pos=g[0]["start"];parts=[]
   for w in g:
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
