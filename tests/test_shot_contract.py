#!/usr/bin/env python3
"""Unit tests for contract validation; no model or network required."""
import importlib.util,json,pathlib,unittest
root=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("planner",root/"tools"/"plan-shots.py")
planner=importlib.util.module_from_spec(spec);spec.loader.exec_module(planner)
shots=root/"episodes"/"MLI_PILOT_001"/"shots.json"
class ContractTests(unittest.TestCase):
 def setUp(self):self.d=json.loads(shots.read_text(encoding="utf-8"))
 def test_valid_contract(self):self.assertEqual(planner.check(self.d),[])
 def test_duplicate_shot_fails(self):
  self.d["scenes"].append(dict(self.d["scenes"][0]))
  self.assertTrue(any("duplicate" in e for e in planner.check(self.d)))
 def test_missing_action_fails(self):
  del self.d["scenes"][0]["action"]
  self.assertTrue(any("missing" in e for e in planner.check(self.d)))
 def test_unreviewed_motion_fails(self):
  self.d["scenes"][3]["motion"]="zoom"
  self.assertTrue(any("camera" in e for e in planner.check(self.d)))
 def test_SC05_props(self):
  prompt=planner.render(self.d,self.d["scenes"][4])
  self.assertIn("pen right hand",prompt)
  self.assertIn("phone in any hand",prompt)
 def test_SC06_gaze(self):
  prompt=planner.render(self.d,self.d["scenes"][5])
  self.assertIn("protagonist looking at friend",prompt)
if __name__=="__main__":unittest.main()
