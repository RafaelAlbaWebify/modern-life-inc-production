#!/usr/bin/env python3
"""Turn semantic image assessments into deterministic retry/accept/block decisions.
No image generation and no publication approvals; fails closed.
"""
import argparse,json,pathlib,re,sys
def decide(report,max_attempts=2):
 grouped={}
 for entry in report.get("results",[]):
  match=re.fullmatch(r"(SC\d{2})_attempt(\d+)\.png",str(entry.get("image","")))
  if not match:continue
  scene,n=match.group(1),int(match.group(2))
  grouped.setdefault(scene,[]).append((n,entry))
 results=[]
 for scene,items in sorted(grouped.items()):
  items.sort(key=lambda pair:pair[0])
  n,last=items[-1];status=last.get("status")
  if status=="CANDIDATE_PASS":
   action="REVIEW_CANDIDATE"
  elif status=="FAIL" and n<max_attempts:
   action="RETRY"
  else:
   action="BLOCK"
  failures=[k for k,v in last.get("checks",{}).items() if v.get("status")=="FAIL"]
  uncertainties=[k for k,v in last.get("checks",{}).items() if v.get("status")=="UNCERTAIN"]
  results.append({"scene":scene,"attempt":n,"image":last["image"],"decision":action,"failed_criteria":failures,"uncertain_criteria":uncertainties,"reason":last.get("error","")})
 return results
def main():
 p=argparse.ArgumentParser();p.add_argument("--report",required=True);p.add_argument("--out",required=True);p.add_argument("--max-attempts",type=int,default=2);a=p.parse_args()
 if a.max_attempts not in (1,2):p.error("Only 1 or 2 attempts permitted")
 source=json.loads(pathlib.Path(a.report).read_text(encoding="utf-8"))
 rows=decide(source,a.max_attempts)
 if not rows:print("No matching image results",file=sys.stderr);return 2
 dest=pathlib.Path(a.out).expanduser().resolve();dest.parent.mkdir(parents=True,exist_ok=True)
 dest.write_text(json.dumps({"policy":"FAIL_CLOSED","release_allowed":False,"decisions":rows},indent=2)+"\n",encoding="utf-8")
 for r in rows:print(r["scene"],r["decision"],"attempt",r["attempt"])
 return 0 if all(x["decision"]=="REVIEW_CANDIDATE" for x in rows) else 3
if __name__=="__main__":sys.exit(main())
