#!/usr/bin/env python3
"""Fast pure-function regression tests for finishing logic (no WhisperX download / GPU)."""
import importlib.util, pathlib, sys, tempfile, unittest
BASE=pathlib.Path(__file__).resolve().parents[1]/"tools"
def module(name, filename):
 spec=importlib.util.spec_from_file_location(name,BASE/filename)
 obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj);return obj
align=module("mli_align","mli-align.py")
finish=module("mli_finish","mli-finish.py")
class FinishingTests(unittest.TestCase):
 def test_srt_millisecond_time(self):
  self.assertEqual(align.stamp(62.345),"00:01:02,345")
 def test_word_grouping_preserves_content(self):
  words=[{"word":f"word{i}","start":float(i),"end":i+0.3} for i in range(22)]
  chunks=align.groups(words)
  self.assertEqual([w for c in chunks for w in c],words)
  self.assertTrue(all(len(c)<=7 for c in chunks))
 def test_scene_coverage(self):
  self.assertEqual(finish.SCENES,["SC01","SC02","SC03","SC04","SC05","SC06"])
if __name__=="__main__":unittest.main()
