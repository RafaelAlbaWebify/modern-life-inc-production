#!/usr/bin/env python3
"""Profile sd.cpp FLUX run logs from an engine-gate ZIP or extracted directory."""
import argparse,csv,json,pathlib,re,sys,zipfile,statistics
PATTERNS={
 "diffusion_seconds":r"sampling completed, taking\s+([\d.]+)s",
 "vae_seconds":r"decode_first_stage completed, taking\s+([\d.]+)s",
 "total_seconds":r"generate_image completed in\s+([\d.]+)s",
}
def parse(text,name):
 result={"shot":pathlib.Path(name).stem,"source":name}
 for key,pat in PATTERNS.items():
  m=re.search(pat,text)
  result[key]=float(m.group(1)) if m else None
 a,b,c=(result[k] for k in ("diffusion_seconds","vae_seconds","total_seconds"))
 result["other_seconds"]=round(c-a-b,3) if None not in (a,b,c) else None
 result["vae_share_pct"]=round(100*b/c,1) if b is not None and c else None
 result["warning"]=None if None not in (a,b,c) and result["other_seconds"]>=0 else "Missing timings or inconsistent log"
 return result
def collect(path):
 if zipfile.is_zipfile(path):
  with zipfile.ZipFile(path) as z:
   return [parse(z.read(i).decode("utf-8","replace"),i) for i in z.namelist() if re.search(r"SC\d+_attempt\d+\.log$",i,re.I)]
 if path.is_dir():
  return [parse(p.read_text(encoding="utf-8",errors="replace"),str(p)) for p in path.rglob("SC*_attempt*.log")]
 if path.is_file():return [parse(path.read_text(encoding="utf-8",errors="replace"),str(path))]
 return []
def main():
 p=argparse.ArgumentParser()
 p.add_argument("source",type=pathlib.Path,help="ZIP or extracted directory with logs")
 p.add_argument("--out",type=pathlib.Path,help="Results dir; default Downloads/MLI_PROFILE")
 a=p.parse_args()
 rows=collect(a.source)
 if not rows:print("No matching generation logs found",file=sys.stderr);return 2
 out=a.out or pathlib.Path.home()/"Downloads"/"MLI_PROFILE"
 out.mkdir(parents=True,exist_ok=True)
 fields=["shot","total_seconds","diffusion_seconds","vae_seconds","other_seconds","vae_share_pct","warning","source"]
 with (out/"profile.csv").open("w",newline="",encoding="utf-8") as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
 valid=[r for r in rows if not r["warning"]]
 summary={"sources":len(rows),"valid":len(valid),"averages_seconds":{k:round(statistics.mean(r[k] for r in valid),3) if valid else None for k in ("total_seconds","diffusion_seconds","vae_seconds","other_seconds")},"notes":["'other' is residual, not exclusively model-loading time","Each CLI run is a separate process; logs do not prove a persistent reuse mode","Only reported timing phases are independently measured; text encoding and loading require finer instrumentation"]}
 (out/"profile.json").write_text(json.dumps({"summary":summary,"runs":rows},indent=2)+"\n",encoding="utf-8")
 for r in rows:print(f"{r['shot']}: total={r['total_seconds']} diffusion={r['diffusion_seconds']} VAE={r['vae_seconds']} other={r['other_seconds']}")
 print("Output:",out)
 return 0 if len(valid)==len(rows) else 1
if __name__=="__main__":sys.exit(main())
