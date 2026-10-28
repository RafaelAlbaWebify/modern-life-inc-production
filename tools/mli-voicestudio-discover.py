#!/usr/bin/env python3
"""Read-only VoiceStudio voice/engine discovery. No GPU synthesis or changes."""
import argparse,json,pathlib,urllib.request,urllib.error,sys
BASE="http://127.0.0.1:3900"
PATHS={"/health":"health","/setup/status":"setup","/system/info":"system",
       "/v1/audio/voices":"voices","/.well-known/voicestudio-speech":"speech_capabilities"}
def read(path):
 try:
  with urllib.request.urlopen(urllib.request.Request(BASE+path,headers={"Accept":"application/json"}),timeout=7) as r:
   body=r.read(1024*1024).decode("utf-8","replace")
   try: return {"ok":True,"http":r.status,"body":json.loads(body)}
   except ValueError:return {"ok":True,"http":r.status,"body_excerpt":body[:500]}
 except Exception as e:return {"ok":False,"error":str(e)}
def main():
 p=argparse.ArgumentParser();p.add_argument("--work",required=True);a=p.parse_args()
 work=pathlib.Path(a.work).resolve();work.mkdir(parents=True,exist_ok=True)
 result={"api_base":BASE,"checks":{name:read(path) for path,name in PATHS.items()},"synthesized":False,
         "voice_selection":"NOT_CONFIRMED","models_ready_is_not_omnivoice_verification":True}
 target=work/"voice_studio_discovery.json";target.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
 print("DISCOVERY REPORT:",target)
 for name,check in result["checks"].items():print(name,"PASS" if check["ok"] else "FAIL",check.get("error",""))
 print("No speech was generated. Inspect available engine and voice IDs before a smoke test.")
if __name__=="__main__":
 try:main()
 except Exception as e:print("FAILED:",e,file=sys.stderr);sys.exit(1)
