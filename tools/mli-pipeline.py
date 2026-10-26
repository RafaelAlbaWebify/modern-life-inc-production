#!/usr/bin/env python3
"""MLI production image pipeline: prepare/generate/package/import/retry/status.
No paid APIs, no CWD dependency, no silent approvals. Python 3.10+ stdlib.
Images are evaluated via a chat-uploaded signed-by-hash JSON report.
"""
import argparse,base64,datetime,hashlib,json,os,pathlib,re,subprocess,sys,urllib.request,zipfile,struct
OWNER="RafaelAlbaWebify/modern-life-inc-production"
BASE="https://api.github.com/repos/"+OWNER+"/contents/"
SCENE=re.compile(r"^SC[0-9]{2}$")
def sha(data):return hashlib.sha256(data).hexdigest()
def write_json(path,data):path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
def fetch(path):
 req=urllib.request.Request(BASE+path+"?ref=main",headers={"Accept":"application/vnd.github+json","Cache-Control":"no-cache","User-Agent":"MLI-pipeline"})
 with urllib.request.urlopen(req,timeout=30) as r:content=json.load(r)
 return base64.b64decode("".join(content["content"].split()))
def root(a):return pathlib.Path(a.work).expanduser().resolve()
def load(run):return json.loads((run/"state.json").read_text(encoding="utf-8"))
def save(run,state):write_json(run/"state.json",state)
def images(run):return run/"images"
def prompt(spec,s):
 return "\n".join((spec["style"],spec["character"],spec["supporting"],"LOCATION: "+s["location"],"SHOT: "+s["framing"],"COMPOSITION: "+s.get("composition","Narrative-first framing; split panels permitted."),"VISIBLE ACTION: "+s["action"],"REQUIRED: "+"; ".join(s["required"]),"EXCLUDE: "+"; ".join(s["forbidden"]), "SUPPORTING CHARACTERS: "+str(s["secondaries"]),"NARRATIVE BEAT: "+s["beat"],"FORMAT: no captions, logos or watermarks."))
def prepare(a):
 run=root(a)
 if (run/"state.json").exists():raise ValueError("Existing run; use new --work or another command")
 run.mkdir(parents=True,exist_ok=True);images(run).mkdir()
 spec=json.loads(pathlib.Path(a.shots).read_text(encoding="utf-8") if a.shots else fetch("episodes/MLI_PILOT_001/shots.json").decode("utf-8"))
 if spec.get("schema_version")!=1 or not isinstance(spec.get("scenes"),list):raise ValueError("Invalid shots.json")
 chosen=a.scenes or [s["id"] for s in spec["scenes"]]
 if len(set(chosen))!=len(chosen) or not all(SCENE.fullmatch(i) for i in chosen):raise ValueError("Bad or repeated shot ID")
 scenes={s["id"]:s for s in spec["scenes"]}
 if not set(chosen)<=set(scenes):raise ValueError("Scene missing from contract")
 (run/"prompts").mkdir()
 for sid in chosen:(run/"prompts"/(sid+".txt")).write_text(prompt(spec,scenes[sid])+"\n",encoding="utf-8")
 write_json(run/"contract.json",spec)
 state={"episode":spec["episode_id"],"created":datetime.datetime.now(datetime.timezone.utc).isoformat(),"source_contract_sha256":sha(json.dumps(spec,sort_keys=True).encode()),"shots":{sid:{"attempts":[],"state":"UNGENERATED"} for sid in chosen},"history":[{"event":"PREPARED"}],"release_approved":False}
 save(run,state);print("PREPARED",run,"shots:",",".join(chosen))
def png(p):
 b=p.read_bytes()
 if len(b)<10000 or b[:8]!=b"\x89PNG\r\n\x1a\n" or b[12:16]!=b"IHDR" or struct.unpack(">II",b[16:24])!=(768,432):raise ValueError("Invalid PNG "+str(p))
 return sha(b)
def generate(a):
 run=root(a);state=load(run);spec=json.loads((run/"contract.json").read_text(encoding="utf-8"))
 models=pathlib.Path(a.models);home=pathlib.Path(a.engine)
 exe=home/"sd-cli.exe";ref=pathlib.Path(spec["reference"]);files=[exe,ref,models/"flux-2-klein-4b-q4_0.gguf",models/"Qwen3-4B-Q4_K_S.gguf",models/"flux2-vae.safetensors"]
 for f in files:
  if not f.is_file():raise FileNotFoundError(str(f))
 (run/"logs").mkdir(exist_ok=True)
 for sid,shot in state["shots"].items():
  if shot["state"] not in ("UNGENERATED","RETRY_AUTHORIZED"):continue
  attempt=len(shot["attempts"])+1
  if attempt>2:shot["state"]="BLOCKED";save(run,state);continue
  target=images(run)/(sid+"_attempt"+str(attempt)+".png")
  if target.exists():raise FileExistsError(str(target))
  seed=next(s["seed"] for s in spec["scenes"] if s["id"]==sid)+(attempt-1)
  prompt_text=(run/"prompts"/(sid+".txt")).read_text(encoding="utf-8")
  if attempt==2:
   failures=[(key,val.get("evidence","")) for key,val in shot.get("review",{}).items() if val.get("status")=="FAIL"]
   if not failures:raise ValueError("Attempt 2 requires explicit prior failed visual evidence")
   prompt_text+="\nRETRY CORRECTIONS FROM VISUAL REVIEW:\n"+"\n".join("Correct "+key+": "+note for key,note in failures)
   (run/"prompts"/(sid+"_attempt2.txt")).write_text(prompt_text+"\n",encoding="utf-8")
  args=[str(exe),"--diffusion-model",str(files[2]),"--llm",str(files[3]),"--vae",str(files[4]),"--backend","te=cpu,diffusion=vulkan0,vae=cpu","--params-backend","te=cpu,diffusion=cpu,vae=cpu","-r",str(ref),"--ref-image-args","preset=flux2","-p",prompt_text,"--cfg-scale","1","--sampling-method","euler","--steps","4","-W","768","-H","432","-t","4","--seed",str(seed),"--output",str(target)]
  logfile=run/"logs"/(sid+"_attempt"+str(attempt)+".log")
  print("GENERATING",sid,"attempt",attempt,flush=True)
  with logfile.open("w",encoding="utf-8") as log:code=subprocess.run(args,stdout=log,stderr=subprocess.STDOUT).returncode
  record={"number":attempt,"file":target.name,"seed":seed,"exit_code":code,"prompt_sha256":sha(prompt_text.encode()),"log":logfile.name}
  try:
   if code:raise ValueError("generator exit "+str(code))
   record["sha256"]=png(target);shot["state"]="NEEDS_REVIEW"
  except Exception as e:
   record["error"]=str(e);shot["state"]="BLOCKED"
  shot["attempts"].append(record);state["history"].append({"event":"GENERATED","shot":sid,"attempt":attempt})
  save(run,state)
 print("Generation finished. Create review package next.")
def package(a):
 run=root(a);state=load(run);todo=[]
 for sid,shot in state["shots"].items():
  if shot["state"]=="NEEDS_REVIEW":
   last=shot["attempts"][-1];todo.append({"image":last["file"],"sha256":last["sha256"],"scene":sid,"attempt":last["number"],"required_criteria":["identity","style","anatomy","action","objects","composition"],"criteria_descriptions":{"identity":json.loads((run/"contract.json").read_text(encoding="utf-8"))["character"],"style":json.loads((run/"contract.json").read_text(encoding="utf-8"))["style"],"anatomy":"Plausible hands and limbs","action":next(x["action"] for x in json.loads((run/"contract.json").read_text(encoding="utf-8"))["scenes"] if x["id"]==sid),"objects":"Required: "+"; ".join(next(x["required"] for x in json.loads((run/"contract.json").read_text(encoding="utf-8"))["scenes"] if x["id"]==sid))+" | Forbidden: "+"; ".join(next(x["forbidden"] for x in json.loads((run/"contract.json").read_text(encoding="utf-8"))["scenes"] if x["id"]==sid)),"composition":next(x.get("composition","Narrative-first layout") for x in json.loads((run/"contract.json").read_text(encoding="utf-8"))["scenes"] if x["id"]==sid)},"status":"PENDING"})
 if not todo:raise ValueError("No pending images to review")
 request={"format":"MLI_CHAT_QC_V1","episode":state["episode"],"results":todo,"guidance":"Inspect actual PNG; each criterion requires PASS/FAIL/UNCERTAIN and visible evidence. Allow multiple-panel composition if narratively appropriate. Never infer from prompt."}
 write_json(run/"review_request.json",request)
 dest=pathlib.Path(a.zip).expanduser().resolve() if a.zip else run.with_name(run.name+"_CHAT_REVIEW.zip")
 with zipfile.ZipFile(dest,"w",zipfile.ZIP_DEFLATED) as z:
  z.write(run/"review_request.json","review_request.json")
  for item in todo:z.write(images(run)/item["image"],item["image"])
 print("REVIEW ZIP:",dest)
def ingest(a):
 run=root(a);state=load(run)
 request=json.loads((run/"review_request.json").read_text(encoding="utf-8"))
 review=json.loads(pathlib.Path(a.report).read_text(encoding="utf-8"))
 expected={i["image"]:i for i in request["results"]}
 received={i["image"]:i for i in review.get("results",[])}
 if set(expected)!=set(received):raise ValueError("Report image set differs from pending review")
 pending=[]
 for name,original in expected.items():
  row=received[name];sid=original["scene"]
  if row.get("sha256")!=original["sha256"] or png(images(run)/name)!=original["sha256"]:raise ValueError("Image hash mismatch "+name)
  checks=row.get("checks")
  if not isinstance(checks,dict) or set(checks)!=set(original["required_criteria"]):raise ValueError("Incomplete criteria "+name)
  for key,v in checks.items():
   if not isinstance(v,dict) or v.get("status") not in ("PASS","FAIL","UNCERTAIN") or not str(v.get("evidence","")).strip():raise ValueError("Invalid result "+name+"/"+key)
  statuses=[v["status"] for v in checks.values()]
  decision="FAIL" if "FAIL" in statuses else ("PENDING" if "UNCERTAIN" in statuses else "CANDIDATE_PASS")
  pending.append((sid,decision,checks))
 for sid,decision,checks in pending:
  entry=state["shots"][sid];entry["review"]=checks
  entry["state"]="CANDIDATE_PASS" if decision=="CANDIDATE_PASS" else ("RETRY_AUTHORIZED" if decision=="FAIL" and len(entry["attempts"])<2 else "BLOCKED")
  state["history"].append({"event":"REVIEW","shot":sid,"decision":entry["state"]})
 save(run,state);print("Imported:",[(sid,state["shots"][sid]["state"]) for sid,_,_ in pending])
def status(a):
 state=load(root(a));print(json.dumps({"shots":{k:v["state"] for k,v in state["shots"].items()},"release_approved":False},indent=2))
def verify(a):
 run=root(a);state=load(run)
 summary={}
 bad=[]
 for sid,shot in state["shots"].items():
  if shot["state"]=="CANDIDATE_PASS":
   last=shot["attempts"][-1]
   try:
    if png(images(run)/last["file"])!=last["sha256"]:raise ValueError("hash mismatch")
    if not shot.get("review"):raise ValueError("missing verified review")
   except Exception as e:bad.append(sid+": "+str(e))
  else:bad.append(sid+": "+shot["state"])
  summary[sid]=shot["state"]
 result={"ready_for_editorial":not bad,"publication_approved":False,"shots":summary,"blockers":bad}
 write_json(run/"acceptance_gate.json",result)
 print(json.dumps(result,indent=2))
 if bad:raise ValueError("Acceptance gate blocked")
def main():
 p=argparse.ArgumentParser();p.add_argument("command",choices=["prepare","generate","package","ingest","status","verify"]);p.add_argument("--work",required=True)
 p.add_argument("--shots");p.add_argument("--scenes",nargs="*");p.add_argument("--models",default=r"C:\AI\MLI-FluxTest\models");p.add_argument("--engine",default=r"C:\AI\MLI-FluxTest-Vulkan");p.add_argument("--zip");p.add_argument("--report")
 a=p.parse_args()
 try:
  {"prepare":prepare,"generate":generate,"package":package,"ingest":ingest,"status":status,"verify":verify}[a.command](a)
 except Exception as e:print("FAILED:",e,file=sys.stderr);return 1
 return 0
if __name__=="__main__":sys.exit(main())
