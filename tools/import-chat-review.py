#!/usr/bin/env python3
"""Validate chat-reviewed image JSON against source hash and required criteria; fail closed."""
import argparse,json,pathlib,sys,hashlib
def main():
 p=argparse.ArgumentParser();p.add_argument("--request",required=True);p.add_argument("--review",required=True);p.add_argument("--out",required=True);a=p.parse_args()
 req=json.loads(pathlib.Path(a.request).read_text(encoding="utf-8"))
 review=json.loads(pathlib.Path(a.review).read_text(encoding="utf-8"))
 expected={x["image"]:x for x in req["results"]}
 found={x["image"]:x for x in review.get("results",[])}
 if set(expected)!=set(found):raise ValueError("Image list mismatch")
 verified=[]
 for name,source in expected.items():
  result=found[name]
  if result.get("sha256")!=source["sha256"]:raise ValueError("Image hash changed "+name)
  if set(result.get("checks",{}))!=set(source["criteria"]):raise ValueError("Criteria incomplete "+name)
  for key,v in result["checks"].items():
   if not isinstance(v,dict) or v.get("status") not in ("PASS","FAIL","UNCERTAIN") or not str(v.get("evidence","")).strip():raise ValueError("Invalid judgment "+name+"/"+key)
  values=[v["status"] for v in result["checks"].values()]
  status="FAIL" if "FAIL" in values else ("PENDING" if "UNCERTAIN" in values else "CANDIDATE_PASS")
  verified.append({"image":name,"sha256":source["sha256"],"checks":result["checks"],"status":status})
 target=pathlib.Path(a.out).expanduser().resolve();target.parent.mkdir(parents=True,exist_ok=True)
 target.write_text(json.dumps({"source":"chat_review_import","publication_approved":False,"results":verified},indent=2)+"\n",encoding="utf-8")
 print("Imported",len(verified),"review decisions ->",target)
 return 0 if all(x["status"]=="CANDIDATE_PASS" for x in verified) else 3
if __name__=="__main__":sys.exit(main())
