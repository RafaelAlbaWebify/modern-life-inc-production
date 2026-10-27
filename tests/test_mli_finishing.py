#!/usr/bin/env python3
"""Fast pure-function regression tests for finishing logic (no WhisperX download / GPU)."""
import importlib.util, pathlib, sys, tempfile, unittest
BASE=pathlib.Path(__file__).resolve().parents[1]/"tools"
def module(name, filename):
 spec=importlib.util.spec_from_file_location(name,BASE/filename)
 obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj);return obj
align=module("mli_align","mli-align.py")
finish=module("mli_finish","mli-finish.py")
caption=module("mli_caption_styles","mli-caption-styles.py")
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
 def test_karaoke_safe_margin(self):
  w=[{"word":"Hello","start":0.0,"end":0.3,"scene":"SC01"},{"word":"there.","start":0.31,"end":0.7,"scene":"SC01"}]
  ass=caption.render(w,"karaoke")
  self.assertIn(",135,1",ass)
  self.assertIn(r"{\k",ass)
 def test_semantic_group_boundaries(self):
  w=[{"word":word,"start":i*0.32,"end":i*0.32+0.25,"scene":"SC01"} for i,word in enumerate(["We","set","boundaries.","Then","we","recover","our","time.","Finally","we","relax."])]
  chunks=caption.groups(w)
  self.assertEqual([w for c in chunks for w in c],w)
  self.assertTrue(any(c[-1]["word"]=="boundaries." for c in chunks))
  self.assertTrue(all(len(c)<=caption.MAX_WORDS for c in chunks))
 def test_two_line_balance_avoids_single_word_orphans(self):
  words="Setting personal boundaries can help reclaim the time and attention that matter every day".split()
  items=[{"word":w,"start":i*0.2,"end":i*0.2+0.15,"scene":"SC01"} for i,w in enumerate(words)]
  for chunk in caption.groups(items):
   pos=caption.split_line(chunk)
   if pos is not None:
    self.assertGreaterEqual(pos,2)
    self.assertGreaterEqual(len(chunk)-pos,2)
 def test_multi_scene_caption_generator(self):
  words=[{"word":"Hello","start":0,"end":0.2,"scene":"SC01"},{"word":"world","start":0.25,"end":0.5,"scene":"SC01"},{"word":"Again","start":1.0,"end":1.2,"scene":"SC02"}]
  self.assertEqual(len(caption.groups(words)),2)
  self.assertIn("MarginV",caption.render(words,"karaoke"))
 def test_line_break_max_two_lines(self):
  w=[{"word":word,"start":i*0.2,"end":i*0.2+0.15,"scene":"SC01"} for i,word in enumerate("Choosing your own boundaries helps you recover the attention and time that really matter".split())]
  for chunk in caption.groups(w):
   text=caption.render(chunk,"karaoke")
   self.assertLessEqual(text.count(r"\N"),1)
if __name__=="__main__":unittest.main()
