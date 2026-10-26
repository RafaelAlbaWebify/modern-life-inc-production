#!/usr/bin/env python3
"""Image-based semantic assessment via OpenAI Responses API; never grants publication approval."""
import argparse,base64,datetime,hashlib,json,os,pathlib,struct,sys,urllib.request
CHECKS={"common":{"identity":"Lead has minimal pale face, orange over-ear headphones, dark messy hair and teal hoodie","style":"Clean consistent 2D illustration without unwanted text","anatomy":"No malformed or extra limbs"},"SC01":{"action":"Lead overwhelmed by incoming notifications","population":"No unwanted background people"},"SC02":{"action":"Lead distracted by smartphone","population":"Two or three normally-faced supporting pedestrians"},"SC03":{"phone":"Phone on table, not held"},"SC04":{"phone":"Phone away on parapet, hands in pockets"},"SC05":{"hands":"RIGHT hand holds pen, LEFT hand on notebook","phone":"Exactly one phone on separate shelf, none in hands or on desk"},"SC06":{"gaze":"Lead looks at friend with mutual engagement","props":"Two mugs and no phone held"}}
def evaluate(path,model):
 data=path.read_bytes()
 if len(data)<10000 or data[:8]!=b"\x89PNG\r\n\x1a\n" or data[12:16]!=b"IHDR" or struct.unpack(">II",data[16:24])!=(768,432):raise ValueError("PNG failed technical gate")
 scene=path.name.split("_")[0];spec=dict(CHECKS["common"],**CHECKS[scene])
 question="Analyze the IMAGE ONLY. Return JSON object with checks dictionary. For EACH named key return status PASS, FAIL, or UNCERTAIN and evidence describing what you actually see. Never infer compliance from instructions. If occluded, use UNCERTAIN. Required checks: "+json.dumps(spec)
 payload={"model":model,"input":[{"role":"user","content":[{"type":"input_text","text":question},{"type":"input_image","image_url":"data:image/png;base64,"+base64.b64encode(data).decode("ascii")}]}],"max_output_tokens":1400}
 req=urllib.request.Request("https://api.openai.com/v1/responses",data=json.dumps(payload).encode(),headers={"Authorization":"Bearer "+os.environ["OPENAI_API_KEY"],"Content-Type":"application/json"},method="POST")
 with urllib.request.urlopen(req,timeout=120) as response:body=json.load(response)
 txt=body.get("output_text") or "\n".join(c.get("text","") for item in body.get("output",[]) for c in item.get("content",[]) if c.get("type")=="output_text")
 txt=txt.strip()
 if txt.startswith(chr(96)*3):txt=txt.strip(chr(96)).removeprefix("json").strip()
 checks=json.loads(txt)["checks"]
 if set(checks)!=set(spec):raise ValueError("Unexpected or missing check IDs")
 for k,v in checks.items():
  if not isinstance(v,dict) or v.get("status") not in ("PASS","FAIL","UNCERTAIN") or len(str(v.get("evidence","")).strip())<8:raise ValueError("Invalid criterion "+k)
 states=[v["status"] for v in checks.values()]
 return {"image":path.name,"sha256":hashlib.sha256(data).hexdigest(),"checks":checks,"status":"FAIL" if "FAIL" in states else ("PENDING" if "UNCERTAIN" in states else "CANDIDATE_PASS"),"response_id":body.get("id")}
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--images",required=True);ap.add_argument("--out",default=None);ap.add_argument("--model",default="gpt-4.1-mini");a=ap.parse_args()
 folder=pathlib.Path(a.images).expanduser().resolve();out=pathlib.Path(a.out).expanduser().resolve() if a.out else pathlib.Path.home()/"Downloads"/"MLI_SEMANTIC_QC";out.mkdir(parents=True,exist_ok=True)
 imgs=sorted(folder.glob("SC*_attempt*.png"));results=[]
 if not imgs:print("No candidate images",file=sys.stderr);return 2
 for path in imgs:
  try:
   if not os.environ.get("OPENAI_API_KEY"):raise RuntimeError("OPENAI_API_KEY not set")
   r=evaluate(path,a.model)
  except Exception as exc:r={"image":path.name,"status":"PENDING","error":str(exc)}
  results.append(r);print(path.name,r["status"],flush=True)
 report={"reviewer":"remote_vision","model":a.model,"publication_approved":False,"timestamp":datetime.datetime.now(datetime.timezone.utc).isoformat(),"results":results}
 (out/"semantic_report.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
 print(out/"semantic_report.json")
 return 0 if all(r["status"]=="CANDIDATE_PASS" for r in results) else 3
if __name__=="__main__":sys.exit(main())
