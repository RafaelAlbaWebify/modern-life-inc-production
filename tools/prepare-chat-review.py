#!/usr/bin/env python3
"""Prepare a chat-review bundle from existing engine-gate PNGs. Offline; no API key."""
import argparse,hashlib,json,pathlib,struct,sys,zipfile
RULES={
"common":{"identity":"Iconic lead: minimal pale face, messy dark hair, orange headphones, teal hoodie","style":"Consistent illustrated look; no odd text or artifacts","anatomy":"Plausible hands, no duplicated limbs"},
"SC01":{"action":"Overwhelmed protagonist at desk","population":"No unintended people"},
"SC02":{"action":"Looking at phone while walking","population":"2-3 ordinary-faced passersby and distinct protagonist"},
"SC03":{"phone":"Phone on table, not in hand"},
"SC04":{"phone":"Phone on parapet away from hands"},
"SC05":{"hands":"Right hand writes with pen, left hand on notebook","phone":"One phone away on separate shelf, none in hands/on desk"},
"SC06":{"gaze":"Lead looks toward friend","props":"Two mugs and no phone in hands"}}
def main():
 p=argparse.ArgumentParser();p.add_argument("--source",required=True);p.add_argument("--out",default=None);a=p.parse_args()
 source=pathlib.Path(a.source).expanduser().resolve()
 out=pathlib.Path(a.out).expanduser().resolve() if a.out else pathlib.Path.home()/"Downloads"/"MLI_CHAT_REVIEW"
 out.mkdir(parents=True,exist_ok=True)
 images=[]
 if source.is_file() and zipfile.is_zipfile(source):
  with zipfile.ZipFile(source) as z:
   for item in z.infolist():
    if pathlib.Path(item.filename).name.startswith("SC") and "_attempt" in item.filename and item.filename.lower().endswith(".png"):
     name=pathlib.Path(item.filename).name;blob=z.read(item)
     (out/name).write_bytes(blob);images.append((name,blob))
 elif source.is_dir():
  for f in sorted(source.rglob("SC*_attempt*.png")):images.append((f.name,f.read_bytes()));(out/f.name).write_bytes(f.read_bytes())
 else:raise ValueError("Source must be prior ZIP or extracted folder")
 if not images:raise ValueError("No reviewable candidate PNGs found")
 request={"schema_version":1,"reviewer":"ChatGPT vision in conversation; human-confirmed where needed","status":"AWAITING_CHAT_REVIEW","results":[]}
 seen=set()
 for name,blob in sorted(images):
  if name in seen:raise ValueError("Duplicate image "+name)
  seen.add(name);scene=name.split("_")[0]
  if scene not in RULES:raise ValueError("Unknown scene "+scene)
  if blob[:8]!=b"\x89PNG\r\n\x1a\n" or blob[12:16]!=b"IHDR":raise ValueError("Bad PNG "+name)
  w,h=struct.unpack(">II",blob[16:24])
  if (w,h)!=(768,432):raise ValueError("Unexpected dimensions "+name)
  request["results"].append({"image":name,"sha256":hashlib.sha256(blob).hexdigest(),"criteria":dict(RULES["common"],**RULES[scene]),"checks":{},"status":"PENDING"})
 (out/"review_request.json").write_text(json.dumps(request,indent=2)+"\n",encoding="utf-8")
 package=out.with_suffix(".zip")
 with zipfile.ZipFile(package,"w",zipfile.ZIP_DEFLATED) as z:
  for name,_ in images:z.write(out/name,name)
  z.write(out/"review_request.json","review_request.json")
 print("Chat review ZIP:",package);print("Files:",len(images))
 return 0
if __name__=="__main__":sys.exit(main())
