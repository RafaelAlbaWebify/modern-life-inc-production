#!/usr/bin/env python3
"""VoiceStudio local-only TTS: one-scene smoke, then explicit resumable batch."""
import argparse, hashlib, json, pathlib, sys, urllib.request, urllib.error, wave, datetime, time, shutil
BASE="http://127.0.0.1:3900"
VOICE="e46c2df1"
ENGINE="omnivoice"
def get(path):
 with urllib.request.urlopen(BASE+path,timeout=12) as r:return json.load(r)
def validate(wav):
 with wave.open(str(wav),"rb") as w:
  assert w.getnchannels()==1 and w.getnframes()>0 and w.getframerate()>0, "Invalid mono WAV"
  return round(w.getnframes()/w.getframerate(),3)
def generate(text, path):
 payload=json.dumps({"model":ENGINE,"voice":VOICE,"input":text,"response_format":"wav"}).encode()
 req=urllib.request.Request(BASE+"/v1/audio/speech",data=payload,headers={"Content-Type":"application/json","Accept":"audio/wav"},method="POST")
 try:
  with urllib.request.urlopen(req,timeout=660) as r:
   if "audio" not in r.headers.get("Content-Type",""):raise ValueError("Non-audio speech response")
   data=r.read(30_000_000)
 except urllib.error.HTTPError as e:raise RuntimeError("VoiceStudio HTTP %s: %s"%(e.code,e.read(3000).decode("utf-8","replace"))) from e
 if len(data)<1024 or data[:4]!=b"RIFF" or data[8:12]!=b"WAVE":raise ValueError("VoiceStudio returned invalid WAV")
 temp=path.with_suffix(".pending.wav");temp.write_bytes(data)
 try:duration=validate(temp);temp.replace(path)
 finally:temp.unlink(missing_ok=True)
 return {"duration":duration,"sha256":hashlib.sha256(data).hexdigest()}
def save_progress(work, report, run_id):
 text=json.dumps(report,indent=2)+"\n"
 history=work/"voice_history";history.mkdir(exist_ok=True)
 snapshot=history/(run_id+".json")
 for path in (snapshot,work/"voice_production_report.json"):
  temporary=path.with_suffix(".pending.json")
  temporary.write_text(text,encoding="utf-8")
  temporary.replace(path)

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--work",required=True);p.add_argument("--mode",choices=["smoke","batch"],required=True)
 p.add_argument("--approved",action="store_true",help="Required to generate entire episode")
 a=p.parse_args()
 work=pathlib.Path(a.work).resolve()
 run_id=datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
 history=work/"voice_history";history.mkdir(exist_ok=True)
 previous=work/"voice_production_report.json"
 if previous.exists():shutil.copy2(previous,history/(run_id+"_previous.json"))
 contract=json.loads((work/"contract.json").read_text(encoding="utf-8"))
 scenes=contract["scenes"];audio=work/"audio";audio.mkdir(exist_ok=True)
 voices=get("/v1/audio/voices");entries=voices.get("voices",[]);engines=voices.get("engines",[])
 if not any(v.get("voice_id")==VOICE and v.get("type")=="profile" for v in entries):raise ValueError("Canonical voice profile missing")
 engine=next((e for e in engines if e.get("id")==ENGINE),None)
 if not engine or not engine.get("available"):raise ValueError("OmniVoice not available")
 if a.mode=="batch" and not a.approved:raise ValueError("Batch requires explicit --approved after listening to smoke WAV")
 if a.mode=="batch" and not (audio/"SC01.wav").is_file():raise ValueError("Run smoke and listen first")
 targets=scenes[:1] if a.mode=="smoke" else scenes
 results=[]
 report={"engine":ENGINE,"profile":VOICE,"mode":a.mode,"run_id":run_id,"scenes":results}
 generated_in_run=0
 save_progress(work,report,run_id)
 for scene in targets:
  sid=scene["id"];path=audio/(sid+".wav")
  if path.exists():
   duration=validate(path)
   results.append({"scene":sid,"status":"REUSED","duration":duration,"sha256":hashlib.sha256(path.read_bytes()).hexdigest()})
   save_progress(work,report,run_id)
   continue
  started=time.monotonic()
  requested_at=datetime.datetime.now(datetime.timezone.utc).isoformat()
  try:
   info=generate(scene["beat"],path);generated_in_run+=1
   results.append({"scene":sid,"status":"GENERATED","requested_at":requested_at,"request_seconds":round(time.monotonic()-started,3),"generation_index_in_run":generated_in_run,**info})
   save_progress(work,report,run_id)
  except Exception as e:
   results.append({"scene":sid,"status":"FAIL","requested_at":requested_at,"request_seconds":round(time.monotonic()-started,3),"generation_index_in_run":generated_in_run+1,"error":str(e)})
   save_progress(work,report,run_id)
   print("FAILED",sid,str(e),flush=True)
   break
  print("VOICE",sid,results[-1]["status"],flush=True)
 save_progress(work,report,run_id)
 if any(x["status"]=="FAIL" for x in results):sys.exit(2)
 print("VOICE PRODUCTION",a.mode,"OK",len(results))
if __name__=="__main__":
 try:main()
 except Exception as e:print("FAILED:",e,file=sys.stderr);sys.exit(1)

