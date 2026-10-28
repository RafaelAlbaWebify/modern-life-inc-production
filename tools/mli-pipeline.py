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
 layout=s.get("visual_layout","single_frame")
 if layout not in ("single_frame","multi_panel"):raise ValueError("Unknown visual_layout")
 if layout=="multi_panel" and not str(s.get("layout_rationale","")).strip():raise ValueError("Multi-panel scene requires explicit narrative layout_rationale")
 layout_instruction=("One continuous 16:9 scene. No split panels, collage, inset frames, white gutters or repeated protagonist views. Preserve coherent framing and do not cut through heads or necks with artificial borders." if layout=="single_frame" else "Multiple panels explicitly authorized for this scene only. Narrative purpose: "+s["layout_rationale"])
 return "\n".join((spec["style"],spec["character"],spec["supporting"],"LOCATION: "+s["location"],"SHOT: "+s["framing"],"COMPOSITION: "+s.get("composition","Narrative-first framing; split panels permitted."),"VISIBLE ACTION: "+s["action"],"REQUIRED: "+"; ".join(s["required"]),"EXCLUDE: "+"; ".join(s["forbidden"]), "SUPPORTING CHARACTERS: "+str(s["secondaries"]),"NARRATIVE BEAT: "+s["beat"],"LAYOUT (mandatory): "+layout_instruction,"FORMAT: no captions, logos or watermarks."))
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
 narration=" ".join(scene["beat"].strip() for scene in spec["scenes"] if scene["id"] in chosen)
 word_count=len(narration.split())
 write_json(run/"planning_summary.json",{"episode":spec["episode_id"],"scene_count":len(chosen),"narration_word_count":word_count,"estimated_voice_seconds_at_140_wpm":round(word_count*60/140,1),"planned_duration_range":spec.get("target_seconds"),"generation_authorized":False,"gpu_used":False,"editing_note":"Before generation, review all prompt and narration beats; durations omit scene gaps and pauses."})
 (run/"narration_draft.txt").write_text("\n\n".join(f"{s['id']}: {s['beat']}" for s in spec["scenes"] if s["id"] in chosen)+"\n",encoding="utf-8")
 state={"episode":spec["episode_id"],"created":datetime.datetime.now(datetime.timezone.utc).isoformat(),"source_contract_sha256":sha(json.dumps(spec,sort_keys=True).encode()),"shots":{sid:{"attempts":[],"state":"UNGENERATED"} for sid in chosen},"history":[{"event":"PREPARED"}],"release_approved":False}
 save(run,state);print("PREPARED",run,"shots:",",".join(chosen))
def png(p):
 b=p.read_bytes()
 if len(b)<10000 or b[:8]!=b"\x89PNG\r\n\x1a\n" or b[12:16]!=b"IHDR":raise ValueError("Invalid PNG "+str(p))
 width,height=struct.unpack(">II",b[16:24])
 if width<768 or height<432 or max(width,height)>4096 or abs(width/height-16/9)>0.01:raise ValueError("Invalid landscape PNG dimensions "+str(p))
 return sha(b)
def generate(a):
 run=root(a);state=load(run);spec=json.loads((run/"contract.json").read_text(encoding="utf-8"))
 if spec.get("image_generation_backend","local_flux")!="local_flux":raise ValueError("This episode uses chat image production. Import reviewed assets; local FLUX generation is not the selected backend.")
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
  backend=json.loads((run/"contract.json").read_text(encoding="utf-8")).get("image_generation_backend","local_flux")
  if backend=="chat_image_edit":
   chat_count=sum(x.get("producer")=="chat_imagegen" or x.get("method")=="built_in_image_edit" for x in entry["attempts"])
   entry["state"]="CANDIDATE_PASS" if decision=="CANDIDATE_PASS" else ("CHAT_REVISION_REQUIRED" if decision=="FAIL" and chat_count<2 else "BLOCKED")
  else:
   entry["state"]="CANDIDATE_PASS" if decision=="CANDIDATE_PASS" else ("RETRY_AUTHORIZED" if decision=="FAIL" and len(entry["attempts"])<2 else "BLOCKED")
  state["history"].append({"event":"REVIEW","shot":sid,"decision":entry["state"]})
 save(run,state);print("Imported:",[(sid,state["shots"][sid]["state"]) for sid,_,_ in pending])
def export(a):
 run=root(a);state=load(run)
 accepted=run/"accepted_images";accepted.mkdir(exist_ok=True)
 problems=[]
 for sid,shot in state["shots"].items():
  if shot["state"]!="CANDIDATE_PASS":
   problems.append(sid+": "+shot["state"]);continue
  last=next((x for x in shot["attempts"] if x["file"]==shot.get("editorial_choice",{}).get("file")),shot["attempts"][-1])
  source=images(run)/last["file"]
  if png(source)!=last["sha256"] or not shot.get("review"):
   problems.append(sid+": review/hash invalid");continue
  dest=accepted/(sid+".png")
  if dest.exists() and png(dest)!=last["sha256"]:raise ValueError("Conflicting accepted copy "+str(dest))
  if not dest.exists():dest.write_bytes(source.read_bytes())
 manifest={"episode":state["episode"],"status":"EXPORTED_NOT_PUBLISHED" if not problems else "BLOCKED","accepted":sorted(p.name for p in accepted.glob("SC*.png")),"blockers":problems}
 write_json(run/"accepted_manifest.json",manifest)
 if problems:raise ValueError("Export blocked: "+"; ".join(problems))
 print("EXPORTED:",accepted,"scenes",len(state["shots"]))
def recover(a):
 run=root(a);state=load(run);log=[]
 for sid,shot in state["shots"].items():
  known={record["number"] for record in shot["attempts"]}
  for attempt in (1,2):
   file=images(run)/(sid+"_attempt"+str(attempt)+".png")
   if not file.exists() or attempt in known:continue
   try:
    digest=png(file)
    promptfile=run/"prompts"/(sid+"_attempt2.txt" if attempt==2 else sid+".txt")
    record={"number":attempt,"file":file.name,"sha256":digest,"seed":next(x["seed"] for x in json.loads((run/"contract.json").read_text(encoding="utf-8"))["scenes"] if x["id"]==sid)+attempt-1,"recovered":True,"prompt_sha256":sha(promptfile.read_bytes()) if promptfile.exists() else None}
    if len(shot["attempts"])>=attempt:raise ValueError("Untracked attempt clashes with existing attempt history")
    shot["attempts"].append(record)
    shot["state"]="NEEDS_REVIEW"
    log.append({"scene":sid,"action":"RECOVERED","file":file.name})
   except Exception as exc:
    quarantine=run/"quarantine";quarantine.mkdir(exist_ok=True)
    dest=quarantine/file.name
    if dest.exists():raise ValueError("Quarantine collision "+str(dest))
    file.rename(dest)
    shot["state"]="BLOCKED"
    log.append({"scene":sid,"action":"QUARANTINED","reason":str(exc)})
  for record in shot["attempts"]:
   file=images(run)/record["file"]
   if file.exists():
    try:
     digest=png(file)
     if record.get("sha256") and digest!=record["sha256"]:raise ValueError("hash mismatch")
    except Exception as exc:
     shot["state"]="BLOCKED";log.append({"scene":sid,"action":"BLOCKED_INTEGRITY","reason":str(exc)})
 # Stop automatic retries authorized by an obsolete review policy; user must re-review.
 for sid,shot in state["shots"].items():
  if shot["state"]=="RETRY_AUTHORIZED":
   shot["state"]="REVIEW_POLICY_HOLD"
   log.append({"scene":sid,"action":"HOLD_OLD_RETRY"})
 state["history"].extend({"event":"RECOVERY","detail":x} for x in log)
 save(run,state)
 write_json(run/"recovery_report.json",{"operations":log,"states":{k:v["state"] for k,v in state["shots"].items()},"gpu_used":False})
 print(json.dumps({"states":{k:v["state"] for k,v in state["shots"].items()},"operations":log},indent=2))
def adopt(a):
 run=root(a);state=load(run)
 d=json.loads(pathlib.Path(a.report).read_text(encoding="utf-8"))
 if d.get("run")!=run.name or d.get("policy")!="narrative-first":raise ValueError("Wrong run/policy")
 rows=d.get("decisions",[])
 if len(rows)!=len(state["shots"]) or set(x["scene"] for x in rows)!=set(state["shots"]):raise ValueError("All scene decisions required exactly once")
 for row in rows:
  sid=row["scene"];entry=state["shots"][sid]
  if row["decision"] not in ("ACCEPT","LOCAL_REPAIR","BLOCK"):raise ValueError("Unsupported decision")
  record=next((x for x in entry["attempts"] if x["file"]==row["image"]),None)
  if record is None:raise ValueError("Unrecorded attempt "+row["image"])
  if png(images(run)/row["image"])!=row["sha256"] or row["sha256"]!=record["sha256"]:raise ValueError("Image digest mismatch "+sid)
 for row in rows:
  entry=state["shots"][row["scene"]]
  entry["editorial_choice"]={"file":row["image"],"sha256":row["sha256"],"decision":row["decision"],"notes":row.get("note","")}
  entry["state"]={"ACCEPT":"CANDIDATE_PASS","LOCAL_REPAIR":"LOCAL_REPAIR","BLOCK":"BLOCKED"}[row["decision"]]
  entry["review"]={"narrative":{"status":"PASS" if row["decision"]=="ACCEPT" else "PENDING","evidence":row.get("note","editorial decision")}}
 state["history"].append({"event":"EDITORIAL_ADOPTION","policy":"narrative-first"})
 save(run,state)
 write_json(run/"editorial_adoption.json",d)
 print("Adopted",[(x["scene"],x["decision"]) for x in rows])
def repair_import(a):
 run=root(a);state=load(run);sid=a.scene
 if sid not in state["shots"]:raise ValueError("Unknown scene")
 entry=state["shots"][sid]
 if entry["state"]!="LOCAL_REPAIR":raise ValueError("Not awaiting localized repair: "+sid)
 source=pathlib.Path(a.image).expanduser().resolve()
 digest=png(source)
 original=entry.get("editorial_choice",{})
 if not original:raise ValueError("Missing prior editorial selection")
 target=images(run)/(sid+"_repaired.png")
 if target.exists():
  if png(target)!=digest:raise ValueError("Existing repaired asset is different")
 else:target.write_bytes(source.read_bytes())
 entry["attempts"].append({"number":len(entry["attempts"])+1,"file":target.name,"sha256":digest,"localized_repair":True,"source_file":original["file"],"source_sha256":original["sha256"]})
 entry["editorial_choice"]={"file":target.name,"sha256":digest,"decision":"ACCEPT","notes":"Localized text cleanup; subject to final video QC"}
 entry["review"]={"narrative":{"status":"PASS","evidence":"Editor-chosen localized text repair; source preserved"}}
 entry["state"]="CANDIDATE_PASS"
 state["history"].append({"event":"LOCAL_REPAIR_IMPORTED","scene":sid,"sha256":digest})
 save(run,state);print("Repair imported",sid,target.name,digest)
def contract_digest(spec):return sha(json.dumps(spec,sort_keys=True).encode())
def chat_export(a):
 run=root(a);state=load(run);spec=json.loads((run/"contract.json").read_text(encoding="utf-8"))
 if spec.get("image_generation_backend")!="chat_image_edit":raise ValueError("Episode is not configured for chat image production")
 digest=contract_digest(spec)
 if state.get("source_contract_sha256")!=digest:raise ValueError("Contract changed; migrate with provenance before exporting jobs")
 selected=a.scenes or list(state["shots"])
 if not selected or len(selected)!=len(set(selected)) or not set(selected)<=set(state["shots"]):raise ValueError("Invalid chat scene selection")
 scene_map={s["id"]:s for s in spec["scenes"]};jobs=[]
 for sid in selected:
  text=(run/"prompts"/(sid+".txt")).read_text(encoding="utf-8")
  jobs.append({"scene":sid,"prompt":text,"prompt_sha256":sha(text.encode()),"narration":scene_map[sid]["beat"],"visual_layout":scene_map[sid].get("visual_layout","single_frame"),"layout_rationale":scene_map[sid].get("layout_rationale"),"current_state":state["shots"][sid]["state"],"review_corrections":{k:v for k,v in state["shots"][sid].get("review",{}).items() if v.get("status")=="FAIL"}})
 ref=pathlib.Path(spec["reference"]).expanduser()
 payload={"format":"MLI_CHAT_IMAGE_JOBS_V1","episode":spec["episode_id"],"contract_sha256":digest,"backend":"chat_image_edit","reference":{"path":str(ref),"sha256":sha(ref.read_bytes()) if ref.is_file() else None},"jobs":jobs,"instructions":"Create/edit images with the chat integrated image tool. Supply actual source images/references as needed. Return real image files plus MLI_CHAT_IMAGES_V1 manifest; do not fabricate file references or acceptance. Generation is chat-mediated, not a local paid API.","publication_approved":False}
 write_json(run/"chat_image_jobs.json",payload)
 print("CHAT IMAGE JOBS:",run/"chat_image_jobs.json","scenes",len(jobs),"NO GPU OR NETWORK GENERATION")
def chat_import(a):
 run=root(a);state=load(run);spec=json.loads((run/"contract.json").read_text(encoding="utf-8"))
 if spec.get("image_generation_backend")!="chat_image_edit":raise ValueError("Episode is not configured for chat image production")
 report_path=pathlib.Path(a.report).expanduser().resolve();bundle=report_path.parent
 report=json.loads(report_path.read_text(encoding="utf-8-sig"));jobs=json.loads((run/"chat_image_jobs.json").read_text(encoding="utf-8"))
 digest=contract_digest(spec)
 if state.get("source_contract_sha256")!=digest or jobs.get("contract_sha256")!=digest or report.get("contract_sha256")!=digest:raise ValueError("Contract digest mismatch")
 if report.get("format")!="MLI_CHAT_IMAGES_V1" or report.get("episode")!=spec["episode_id"] or jobs.get("episode")!=spec["episode_id"]:raise ValueError("Wrong chat image manifest format/episode")
 rows=report.get("images");expected={j["scene"]:j for j in jobs["jobs"]}
 if not isinstance(rows,list) or not rows or len({r.get("scene") for r in rows})!=len(rows):raise ValueError("Empty or duplicate scene import")
 validated=[]
 for row in rows:
  sid=row.get("scene")
  if sid not in expected or sid not in state["shots"]:raise ValueError("Unrequested scene")
  if row.get("producer")!="chat_imagegen" or not str(row.get("source_artifact","")).strip():raise ValueError("Missing chat image provenance")
  text=(run/"prompts"/(sid+".txt")).read_text(encoding="utf-8")
  if row.get("prompt_sha256")!=expected[sid]["prompt_sha256"] or sha(text.encode())!=expected[sid]["prompt_sha256"]:raise ValueError("Prompt digest mismatch "+sid)
  source=(bundle/row["file"]).resolve()
  if not source.is_relative_to(bundle):raise ValueError("Image path escapes bundle")
  digest_image=png(source)
  if digest_image!=row.get("sha256"):raise ValueError("Image digest mismatch "+sid)
  dest=images(run)/(sid+"_chat_"+digest_image[:16]+".png")
  if dest.exists() and png(dest)!=digest_image:raise ValueError("Conflicting imported image")
  accepted=run/"accepted_images"/(sid+".png")
  if accepted.exists():png(accepted)
  validated.append((row,source,dest,digest_image))
 # All validation completes before files, selections or state are modified.
 import_id=datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
 backup=run/"chat_import_history";backup.mkdir(exist_ok=True)
 (backup/(import_id+"_state_before.json")).write_bytes((run/"state.json").read_bytes())
 write_json(backup/(import_id+"_manifest.json"),report)
 imported=[];reused=[]
 for row,source,dest,digest_image in validated:
  sid=row["scene"];entry=state["shots"][sid]
  if entry["attempts"] and entry["attempts"][-1].get("sha256")==digest_image:
   reused.append(sid);continue
  if not dest.exists():dest.write_bytes(source.read_bytes())
  accepted=run/"accepted_images"/(sid+".png")
  if accepted.exists():
   archive=run/"superseded_exports"/import_id;archive.mkdir(parents=True,exist_ok=True)
   accepted.rename(archive/(sid+".png"))
  if entry.get("editorial_choice"):entry.setdefault("editorial_history",[]).append(entry.pop("editorial_choice"))
  if entry.get("review"):entry.setdefault("review_history",[]).append(entry.pop("review"))
  entry["attempts"].append({"number":len(entry["attempts"])+1,"file":dest.name,"sha256":digest_image,"prompt_sha256":row["prompt_sha256"],"producer":"chat_imagegen","source_artifact":row["source_artifact"],"import_id":import_id})
  entry["state"]="NEEDS_REVIEW";imported.append(sid)
 state["history"].append({"event":"CHAT_IMAGES_IMPORTED","import_id":import_id,"scenes":imported,"reused":reused});state["release_approved"]=False
 temp=run/"state.chat_import.pending.json";write_json(temp,state);temp.replace(run/"state.json")
 write_json(run/"chat_import_receipt.json",{"import_id":import_id,"imported":imported,"reused":reused,"publication_approved":False})
 print("CHAT IMPORT:",len(imported),"new;",len(reused),"reused; visual review still required")

def status(a):
 state=load(root(a));print(json.dumps({"shots":{k:v["state"] for k,v in state["shots"].items()},"release_approved":False},indent=2))
def verify(a):
 run=root(a);state=load(run)
 summary={}
 bad=[]
 for sid,shot in state["shots"].items():
  if shot["state"]=="CANDIDATE_PASS":
   last=next((x for x in shot["attempts"] if x["file"]==shot.get("editorial_choice",{}).get("file")),shot["attempts"][-1])
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
 p=argparse.ArgumentParser();p.add_argument("command",choices=["prepare","generate","package","ingest","status","verify","export","recover","adopt","repair-import","chat-export","chat-import"]);p.add_argument("--work",required=True)
 p.add_argument("--shots");p.add_argument("--scenes",nargs="*");p.add_argument("--models",default=r"C:\AI\MLI-FluxTest\models");p.add_argument("--engine",default=r"C:\AI\MLI-FluxTest-Vulkan");p.add_argument("--zip");p.add_argument("--report");p.add_argument("--image");p.add_argument("--scene")
 a=p.parse_args()
 try:
  {"prepare":prepare,"generate":generate,"package":package,"ingest":ingest,"status":status,"verify":verify,"export":export,"recover":recover,"adopt":adopt,"repair-import":repair_import,"chat-export":chat_export,"chat-import":chat_import}[a.command](a)
 except Exception as e:print("FAILED:",e,file=sys.stderr);return 1
 return 0
if __name__=="__main__":sys.exit(main())

