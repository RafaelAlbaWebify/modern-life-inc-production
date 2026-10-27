#!/usr/bin/env python3
"""Audit every episode WAV without exiting early. Also export per-scene voice job manifest."""
import argparse,hashlib,json,pathlib,subprocess,sys,wave
def main():
 p=argparse.ArgumentParser();p.add_argument("--work",required=True);a=p.parse_args()
 work=pathlib.Path(a.work).resolve();c=json.loads((work/"contract.json").read_text(encoding="utf-8"))
 audio=work/"audio";audio.mkdir(exist_ok=True)
 findings=[];jobs=[]
 for scene in c["scenes"]:
  sid=scene["id"];wav=audio/(sid+".wav")
  job={"id":sid,"text":scene["beat"],"output_wav":str(wav),"speaker":"canonical MLI narrator, consistent across scenes","voice_review_required":True}
  jobs.append(job)
  if not wav.is_file():
   findings.append({"scene":sid,"status":"MISSING","reason":"Narration WAV not found"});continue
  try:
   with wave.open(str(wav),"rb") as f:
    seconds=f.getnframes()/f.getframerate()
    if f.getnchannels()!=1 or f.getsampwidth() not in (2,4) or seconds<0.3:raise ValueError("Expected mono PCM 16/32-bit WAV, duration >=0.3s")
   findings.append({"scene":sid,"status":"PASS","duration":round(seconds,3),"sha256":hashlib.sha256(wav.read_bytes()).hexdigest()})
  except Exception as e:findings.append({"scene":sid,"status":"INVALID","reason":str(e)})
 record={"episode":c["episode_id"],"scene_count":len(jobs),"ready":all(x["status"]=="PASS" for x in findings),"checks":findings,"voice_generation_automated":False}
 (work/"voice_jobs.json").write_text(json.dumps({"episode":c["episode_id"],"jobs":jobs},indent=2)+"\n",encoding="utf-8")
 (work/"audio_audit.json").write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({"ready":record["ready"],"passed":sum(x["status"]=="PASS" for x in findings),"total":len(findings),"report":str(work/"audio_audit.json")},indent=2))
 if not record["ready"]:sys.exit(2)
if __name__=="__main__":
 try:main()
 except Exception as e:print("FAILED:",e,file=sys.stderr);sys.exit(1)
