#!/usr/bin/env python3
"""Validate an MLI shot contract and emit auditable prompts; NEVER calls a model."""
import argparse,json,pathlib,re,sys,hashlib
REQUIRED={"schema_version","episode_id","reference","style","character","supporting","max_attempts","scenes"}
SHOT={"id","beat","purpose","location","framing","action","required","forbidden","secondaries","motion","seed"}
def check(d):
 errors=[]
 missing=REQUIRED-set(d)
 if missing:errors.append("Missing root: "+str(sorted(missing)))
 if d.get("schema_version")!=1:errors.append("Unsupported schema_version")
 if not isinstance(d.get("max_attempts"),int) or not 1<=d["max_attempts"]<=3:errors.append("max_attempts must be 1..3")
 ids=set()
 for i,s in enumerate(d.get("scenes",[])):
  k=f"scene {i+1}"
  if not isinstance(s,dict):errors.append(k+" not object");continue
  if SHOT-set(s):errors.append(k+" missing "+str(sorted(SHOT-set(s))));continue
  if not re.fullmatch(r"SC\d{2}",str(s["id"])):errors.append(k+" invalid ID")
  if s["id"] in ids:errors.append(k+" duplicate ID")
  ids.add(s["id"])
  for field in ["beat","purpose","location","framing","action"]:
   if not isinstance(s[field],str) or not s[field].strip():errors.append(k+" empty "+field)
  for field in ["required","forbidden"]:
   if not isinstance(s[field],list) or not s[field] or not all(isinstance(x,str) and x.strip() for x in s[field]):errors.append(k+" invalid "+field)
  if s["motion"]!="hold":errors.append(k+" camera must be hold unless a separately reviewed plan exists")
  if not isinstance(s["seed"],int) or s["seed"]<0:errors.append(k+" invalid seed")
  if not isinstance(s["secondaries"],int) or s["secondaries"]<0:errors.append(k+" invalid secondaries")
 if not d.get("scenes"):errors.append("No scenes")
 return errors
def render(d,s):
 sections=[
  d["style"],d["character"],f"Location: {s['location']}. Shot: {s['framing']}.",
  "NARRATIVE BEAT: "+s["beat"],"VISIBLE ACTION: "+s["action"],
  "NON-NEGOTIABLE VISUAL FACTS: "+"; ".join(s["required"])+".",
  "DO NOT SHOW: "+"; ".join(s["forbidden"])+".",
  f"Number of secondary people: {s['secondaries']}. "+d["supporting"],
  "Purpose: "+s["purpose"],"No titles, text, logos, speech balloons or watermarks.",
  "Do not assume words in prompt guarantee the facts: visual QC is required."
 ]
 return "\n".join(sections)
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--shots",required=True)
 p.add_argument("--out",required=True)
 a=p.parse_args();d=json.loads(pathlib.Path(a.shots).read_text(encoding="utf-8"))
 errors=check(d)
 if errors:
  for e in errors:print("FAIL:",e,file=sys.stderr)
  return 2
 out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
 manifest={"episode_id":d["episode_id"],"schema_version":1,"shots":[]}
 for s in d["scenes"]:
  prompt=render(d,s)
  (out/(s["id"]+".txt")).write_text(prompt+"\n",encoding="utf-8")
  manifest["shots"].append({"id":s["id"],"seed":s["seed"],"attempt_budget":d["max_attempts"],"prompt_sha256":hashlib.sha256(prompt.encode()).hexdigest(),"status":"awaiting_generation_and_visual_QC"})
 (out/"prompt_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
 print(f"PASS: {len(d['scenes'])} shot contracts validated; prompts in {out}")
 return 0
if __name__=="__main__":sys.exit(main())
