#!/usr/bin/env python3
"""No-GPU regression tests for the single-file MLI image pipeline."""
import importlib.util,json,pathlib,struct,tempfile,types,unittest
here=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("pipeline",here/"tools"/"mli-pipeline.py")
pipeline=importlib.util.module_from_spec(spec);spec.loader.exec_module(pipeline)
def fake_png():return b"\x89PNG\r\n\x1a\n"+struct.pack(">I",13)+b"IHDR"+struct.pack(">II",768,432)+b"\x08\x02\x00\x00\x00"+b"\x00"*10010
class PipelineTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
  self.path=pathlib.Path(self.tmp.name);self.work=self.path/"run"
  self.shots=self.path/"shots.json"
  self.shots.write_text(json.dumps({"schema_version":1,"episode_id":"TEST","reference":"C:/fake/ref.png","style":"2D","character":"protagonist","supporting":"background","scenes":[{"id":"SC01","seed":123,"beat":"hello","location":"desk","framing":"medium","action":"writing","required":["pen"],"forbidden":["phone"],"secondaries":0}]}))
  pipeline.prepare(types.SimpleNamespace(work=str(self.work),shots=str(self.shots),scenes=["SC01"]))
  (self.work/"images"/"SC01_attempt1.png").write_bytes(fake_png())
  state=pipeline.load(self.work);state["shots"]["SC01"]={"state":"NEEDS_REVIEW","attempts":[{"number":1,"file":"SC01_attempt1.png","sha256":pipeline.png(self.work/"images"/"SC01_attempt1.png")}]};pipeline.save(self.work,state)
 def test_chat_backend_does_not_start_local_generation(self):
  contract=json.loads((self.work/"contract.json").read_text());contract["image_generation_backend"]="chat_image_edit"
  (self.work/"contract.json").write_text(json.dumps(contract))
  with self.assertRaisesRegex(ValueError,"chat image production"):
   pipeline.generate(types.SimpleNamespace(work=str(self.work)))
 def test_high_resolution_landscape_preserved(self):
  data=bytearray(fake_png());data[16:24]=struct.pack(">II",1672,941)
  file=self.path/"highres.png";file.write_bytes(data)
  self.assertEqual(pipeline.png(file),pipeline.sha(data))
 def test_square_source_rejected(self):
  data=bytearray(fake_png());data[16:24]=struct.pack(">II",768,768)
  file=self.path/"square.png";file.write_bytes(data)
  with self.assertRaises(ValueError):pipeline.png(file)
 def test_multi_panel_requires_story_rationale(self):
  contract=json.loads(self.shots.read_text());scene=dict(contract["scenes"][0],visual_layout="multi_panel")
  with self.assertRaises(ValueError):pipeline.prompt(contract,scene)
  scene["layout_rationale"]="Contrast the same choice before and after a boundary"
  self.assertIn(scene["layout_rationale"],pipeline.prompt(contract,scene))
 def chat_fixture(self):
  spec=json.loads((self.work/"contract.json").read_text());spec["image_generation_backend"]="chat_image_edit"
  (self.work/"contract.json").write_text(json.dumps(spec))
  state=pipeline.load(self.work);state["source_contract_sha256"]=pipeline.contract_digest(spec)
  entry=state["shots"]["SC01"];entry["state"]="CANDIDATE_PASS";entry["review"]={"narrative":{"status":"PASS","evidence":"old selected image"}};entry["editorial_choice"]={"file":"SC01_attempt1.png","sha256":entry["attempts"][0]["sha256"]}
  pipeline.save(self.work,state);pipeline.export(types.SimpleNamespace(work=str(self.work)))
  pipeline.chat_export(types.SimpleNamespace(work=str(self.work),scenes=None))
  jobs=json.loads((self.work/"chat_image_jobs.json").read_text())
  bundle=self.path/"chat_bundle";bundle.mkdir();image=bundle/"new.png";image.write_bytes(fake_png()+b"newchatimage")
  report={"format":"MLI_CHAT_IMAGES_V1","episode":"TEST","contract_sha256":jobs["contract_sha256"],"images":[{"scene":"SC01","file":"new.png","sha256":pipeline.png(image),"prompt_sha256":jobs["jobs"][0]["prompt_sha256"],"producer":"chat_imagegen","source_artifact":"test-fixture-output"}]}
  manifest=bundle/"images.json";manifest.write_text(json.dumps(report))
  return manifest,report
 def test_chat_import_requires_review_and_preserves_old_assets(self):
  manifest,report=self.chat_fixture()
  pipeline.chat_import(types.SimpleNamespace(work=str(self.work),report=str(manifest)))
  state=pipeline.load(self.work);entry=state["shots"]["SC01"]
  self.assertEqual(entry["state"],"NEEDS_REVIEW")
  self.assertNotIn("editorial_choice",entry)
  self.assertTrue(entry["editorial_history"])
  self.assertTrue((self.work/"images/SC01_attempt1.png").exists())
  self.assertFalse((self.work/"accepted_images/SC01.png").exists())
  self.assertEqual(len(list((self.work/"superseded_exports").glob("*/SC01.png"))),1)
  self.assertFalse(state["release_approved"])
 def test_chat_import_hash_failure_does_not_modify_state(self):
  manifest,report=self.chat_fixture();before=(self.work/"state.json").read_bytes()
  report["images"][0]["sha256"]="wrong";manifest.write_text(json.dumps(report))
  with self.assertRaisesRegex(ValueError,"digest mismatch"):
   pipeline.chat_import(types.SimpleNamespace(work=str(self.work),report=str(manifest)))
  self.assertEqual(before,(self.work/"state.json").read_bytes())
  self.assertTrue((self.work/"accepted_images/SC01.png").exists())
  self.assertFalse((self.work/"chat_import_history").exists())
 def test_chat_import_is_idempotent(self):
  manifest,_=self.chat_fixture();args=types.SimpleNamespace(work=str(self.work),report=str(manifest))
  pipeline.chat_import(args);pipeline.chat_import(args)
  self.assertEqual(len(pipeline.load(self.work)["shots"]["SC01"]["attempts"]),2)
  self.assertEqual(json.loads((self.work/"chat_import_receipt.json").read_text())["reused"],["SC01"])
 def test_chat_import_rejects_stale_prompt(self):
  manifest,_=self.chat_fixture();before=(self.work/"state.json").read_bytes()
  (self.work/"prompts/SC01.txt").write_text("changed after export")
  with self.assertRaisesRegex(ValueError,"Prompt digest mismatch"):
   pipeline.chat_import(types.SimpleNamespace(work=str(self.work),report=str(manifest)))
  self.assertEqual(before,(self.work/"state.json").read_bytes())
 def test_chat_import_rejects_path_escape(self):
  manifest,report=self.chat_fixture();report["images"][0]["file"]="../outside.png";manifest.write_text(json.dumps(report))
  with self.assertRaisesRegex(ValueError,"escapes bundle"):
   pipeline.chat_import(types.SimpleNamespace(work=str(self.work),report=str(manifest)))
 def test_chat_export_rejects_untracked_contract_change(self):
  self.chat_fixture();spec=json.loads((self.work/"contract.json").read_text());spec["style"]="new style"
  (self.work/"contract.json").write_text(json.dumps(spec))
  with self.assertRaisesRegex(ValueError,"Contract changed"):
   pipeline.chat_export(types.SimpleNamespace(work=str(self.work),scenes=None))
 def chat_reject_latest(self):
  pipeline.package(types.SimpleNamespace(work=str(self.work),zip=None))
  row=json.loads((self.work/"review_request.json").read_text())["results"][0]
  decision={"results":[{"image":row["image"],"sha256":row["sha256"],"checks":{k:{"status":"FAIL" if k=="composition" else "PASS","evidence":"Visible repeated panel layout"} for k in row["required_criteria"]}}]}
  path=self.path/"chat_review.json";path.write_text(json.dumps(decision));pipeline.ingest(types.SimpleNamespace(work=str(self.work),report=str(path)))
 def test_chat_rejection_requests_chat_revision_not_local_retry(self):
  manifest,_=self.chat_fixture();pipeline.chat_import(types.SimpleNamespace(work=str(self.work),report=str(manifest)))
  self.chat_reject_latest()
  self.assertEqual(pipeline.load(self.work)["shots"]["SC01"]["state"],"CHAT_REVISION_REQUIRED")
  pipeline.chat_export(types.SimpleNamespace(work=str(self.work),scenes=["SC01"]))
  jobs=json.loads((self.work/"chat_image_jobs.json").read_text())
  self.assertIn("composition",jobs["jobs"][0]["review_corrections"])
 def test_second_chat_rejection_blocks_repeated_generation(self):
  manifest,report=self.chat_fixture();args=types.SimpleNamespace(work=str(self.work),report=str(manifest))
  pipeline.chat_import(args);self.chat_reject_latest()
  pipeline.chat_export(types.SimpleNamespace(work=str(self.work),scenes=["SC01"]))
  image=manifest.parent/"new.png";image.write_bytes(fake_png()+b"different second image");report["images"][0]["sha256"]=pipeline.png(image);manifest.write_text(json.dumps(report))
  pipeline.chat_import(args);self.chat_reject_latest()
  self.assertEqual(pipeline.load(self.work)["shots"]["SC01"]["state"],"BLOCKED")
 def test_cwd_independent_and_package(self):
  pipeline.package(types.SimpleNamespace(work=str(self.work),zip=None))
  self.assertTrue(self.work.with_name(self.work.name+"_CHAT_REVIEW.zip").exists())
  req=json.loads((self.work/"review_request.json").read_text())
  self.assertIn("Required: pen",req["results"][0]["criteria_descriptions"]["objects"])
 def test_fail_only_retries_and_does_not_approve(self):
  pipeline.package(types.SimpleNamespace(work=str(self.work),zip=None))
  req=json.loads((self.work/"review_request.json").read_text())["results"][0]
  report={"results":[{"image":req["image"],"sha256":req["sha256"],"checks":{k:{"status":"FAIL" if k=="objects" else "PASS","evidence":"Visible assessment"} for k in req["required_criteria"]}}]}
  path=self.path/"review.json";path.write_text(json.dumps(report))
  pipeline.ingest(types.SimpleNamespace(work=str(self.work),report=str(path)))
  state=pipeline.load(self.work)
  self.assertEqual(state["shots"]["SC01"]["state"],"RETRY_AUTHORIZED")
  self.assertFalse(state["release_approved"])
 def test_recover_untracked_valid_png_without_regeneration(self):
  state=pipeline.load(self.work)
  state["shots"]["SC01"]["attempts"]=[]
  state["shots"]["SC01"]["state"]="RETRY_AUTHORIZED"
  pipeline.save(self.work,state)
  pipeline.recover(types.SimpleNamespace(work=str(self.work)))
  recovered=pipeline.load(self.work)["shots"]["SC01"]
  self.assertEqual(recovered["state"],"NEEDS_REVIEW")
  self.assertEqual(len(recovered["attempts"]),1)
  self.assertTrue(recovered["attempts"][0]["recovered"])
 def test_recover_does_not_authorize_obsolete_retries(self):
  state=pipeline.load(self.work)
  state["shots"]["SC01"]["state"]="RETRY_AUTHORIZED"
  pipeline.save(self.work,state)
  pipeline.recover(types.SimpleNamespace(work=str(self.work)))
  self.assertEqual(pipeline.load(self.work)["shots"]["SC01"]["state"],"REVIEW_POLICY_HOLD")
 def test_mismatched_hash_blocks(self):
  pipeline.package(types.SimpleNamespace(work=str(self.work),zip=None))
  req=json.loads((self.work/"review_request.json").read_text())["results"][0]
  path=self.path/"review.json";path.write_text(json.dumps({"results":[{"image":req["image"],"sha256":"wrong","checks":{k:{"status":"PASS","evidence":"Visible fact"} for k in req["required_criteria"]}}]}))
  with self.assertRaises(ValueError):pipeline.ingest(types.SimpleNamespace(work=str(self.work),report=str(path)))
if __name__=="__main__":unittest.main()


