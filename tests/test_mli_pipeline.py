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
 def test_mismatched_hash_blocks(self):
  pipeline.package(types.SimpleNamespace(work=str(self.work),zip=None))
  req=json.loads((self.work/"review_request.json").read_text())["results"][0]
  path=self.path/"review.json";path.write_text(json.dumps({"results":[{"image":req["image"],"sha256":"wrong","checks":{k:{"status":"PASS","evidence":"Visible fact"} for k in req["required_criteria"]}}]}))
  with self.assertRaises(ValueError):pipeline.ingest(types.SimpleNamespace(work=str(self.work),report=str(path)))
if __name__=="__main__":unittest.main()
