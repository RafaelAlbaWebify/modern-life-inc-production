#!/usr/bin/env python3
"""Execute only permitted visual-QC retries. Never more than two attempts per shot.
No renderer invoked unless --execute supplied; source models read-only.
"""
import argparse,json,pathlib,subprocess,sys,os
def main():
 p=argparse.ArgumentParser();p.add_argument("--plan",required=True);p.add_argument("--prompts",required=True);p.add_argument("--images",required=True);p.add_argument("--logs",required=True);p.add_argument("--execute",action="store_true")
 a=p.parse_args();plan=json.loads(pathlib.Path(a.plan).read_text(encoding="utf-8"))
 root=pathlib.Path(r"C:\AI\MLI-FluxTest-Vulkan");models=pathlib.Path(r"C:\AI\MLI-FluxTest\models")
 exe=root/"sd-cli.exe";ref=root/"story_consistency_revised"/"CHARACTER_REFERENCE.png"
 files=[exe,ref,models/"flux-2-klein-4b-q4_0.gguf",models/"Qwen3-4B-Q4_K_S.gguf",models/"flux2-vae.safetensors"]
 tasks=[r for r in plan["decisions"] if r["decision"]=="RETRY"]
 for r in tasks:
  if r["attempt"]!=1:raise ValueError("Only attempt 1 may be retried")
 if not a.execute:
  print("DRY RUN",len(tasks),"scenes would retry; no GPU used")
  return 0
 for f in files:
  if not f.is_file():raise FileNotFoundError(f)
 images=pathlib.Path(a.images).expanduser().resolve();images.mkdir(parents=True,exist_ok=True)
 logs=pathlib.Path(a.logs).expanduser().resolve();logs.mkdir(parents=True,exist_ok=True)
 for r in tasks:
  scene=r["scene"]
  promptfile=pathlib.Path(a.prompts).expanduser().resolve()/(scene+".txt")
  prompt=promptfile.read_text(encoding="utf-8")
  outfile=images/(scene+"_attempt2.png")
  if outfile.exists():raise FileExistsError(f"Refusing to overwrite existing attempt2: {outfile}")
  seed=3100+int(scene[2:])+1
  args=[str(exe),"--diffusion-model",str(files[2]),"--llm",str(files[3]),"--vae",str(files[4]),"--backend","te=cpu,diffusion=vulkan0,vae=cpu","--params-backend","te=cpu,diffusion=cpu,vae=cpu","-r",str(ref),"--ref-image-args","preset=flux2","-p",prompt,"--cfg-scale","1","--sampling-method","euler","--steps","4","-W","768","-H","432","-t","4","--seed",str(seed),"--output",str(outfile)]
  print("RETRY",scene,"seed",seed,flush=True)
  with (logs/(scene+"_attempt2.log")).open("w",encoding="utf-8") as stream:
   status=subprocess.run(args,stdout=stream,stderr=subprocess.STDOUT).returncode
  if status:raise RuntimeError(f"Generator failed {scene}, status {status}")
 print("Completed bounded retries; RE-RUN semantic evaluation. Publication remains blocked.")
 return 0
if __name__=="__main__":sys.exit(main())
