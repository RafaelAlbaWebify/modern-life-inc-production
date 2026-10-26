#!/usr/bin/env python3
"""MLI visual gate: technical PNG preflight plus explicitly recorded semantic decisions.
NO claim of automatic AI vision. Zero exit only after every mandatory review PASS.
CWD independent. Python 3.10+ stdlib.
"""
import argparse,hashlib,json,pathlib,struct,sys,datetime
def image_info(p):
 b=p.read_bytes()
 if len(b)<10000 or b[:8]!=b"\x89PNG\r\n\x1a\n" or b[12:16]!=b"IHDR":raise ValueError("PNG signature/IHDR/size invalid")
 w,h=struct.unpack(">II",b[16:24])
 if (w,h)!=(768,432):raise ValueError(f"dimensions {w}x{h} not 768x432")
 return {"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest(),"width":w,"height":h}
def criteria(scene):
 common={"identity":"Lead has pale minimal face, messy dark hair, orange headphones and teal hoodie","style":"Consistent 2D illustration, no text/watermarks","anatomy":"Plausible hands and limbs"}
 specific={
 "SC01":{"action":"Lead visibly exhausted by notifications","population":"No unwanted extra figures"},
 "SC02":{"action":"Lead distracted by smartphone","population":"2-3 background people with ordinary illustrated faces; no second lead"},
 "SC03":{"action":"Phone placed on cafe table, not in hand","population":"Background guests distinct from lead"},
 "SC04":{"action":"Hands in pockets and phone away on parapet","gaze":"Lead not staring at phone"},
 "SC05":{"hands":"RIGHT hand pen, LEFT hand on notebook","phone":"Exactly one phone on a separate shelf, none in either hand"},
 "SC06":{"gaze":"Lead looking at friend, with mutual engagement","props":"Two mugs, no phone in either hand"},
 }
 return dict(common,**specific.get(scene,{}))
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--images",required=True,help="Existing engine gate images directory")
 p.add_argument("--out",default=None,help="QC output; defaults Downloads/MLI_VISUAL_QC")
 p.add_argument("--decisions",default=None,help="Optional human decisions JSON; keys per shot and criterion")
 a=p.parse_args()
 images=pathlib.Path(a.images).expanduser().resolve()
 out=pathlib.Path(a.out).expanduser().resolve() if a.out else pathlib.Path.home()/"Downloads"/"MLI_VISUAL_QC"
 out.mkdir(parents=True,exist_ok=True)
 decisions={}
 if a.decisions:
  decisions=json.loads(pathlib.Path(a.decisions).read_text(encoding="utf-8"))
 entries=[]
 for f in sorted(images.glob("SC*_attempt*.png")):
  shot=f.name.split("_")[0]
  record={"shot":shot,"file":str(f),"technical":"FAIL","semantic":"PENDING","criteria":[]}
  try:record["image"]=image_info(f);record["technical"]="PASS"
  except Exception as e:record["technical_error"]=str(e)
  for key,description in criteria(shot).items():
   decision=decisions.get(f.name,{}).get(key,{})
   status=decision.get("status","PENDING")
   reviewer=decision.get("reviewer","")
   evidence=decision.get("notes","")
   if status not in ("PASS","FAIL","PENDING"):status="PENDING"
   if status!="PENDING" and (not reviewer.strip() or not evidence.strip()):
    status="PENDING"
   record["criteria"].append({"criterion":key,"description":description,"status":status,"reviewer":reviewer,"notes":evidence})
  values=[c["status"] for c in record["criteria"]]
  record["semantic"]="FAIL" if "FAIL" in values else ("PASS" if record["technical"]=="PASS" and all(x=="PASS" for x in values) else "PENDING")
  entries.append(record)
 if not entries:
  print("No SC*_attempt*.png images found",file=sys.stderr);return 2
 report={"generated_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"policy":"FAIL_CLOSED","note":"Semantic decisions require visual inspection and reviewer evidence, not image filename or program inference","images":entries}
 (out/"visual_qc.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
 (out/"review_template.json").write_text(json.dumps({pathlib.Path(e["file"]).name:{c["criterion"]:{"status":"PENDING","reviewer":"","notes":""} for c in e["criteria"]} for e in entries},indent=2)+"\n",encoding="utf-8")
 for e in entries:print(f"{e['shot']} {pathlib.Path(e['file']).name}: technical={e['technical']} semantic={e['semantic']}")
 print("QC report:",out/"visual_qc.json")
 return 0 if all(e["semantic"]=="PASS" for e in entries) else 3
if __name__=="__main__":sys.exit(main())
