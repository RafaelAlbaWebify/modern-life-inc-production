#!/usr/bin/env python3
"""Unit tests for stage-agnostic audio audit and Soft Karaoke production pieces."""
import importlib.util,json,pathlib,tempfile,unittest,wave
BASE=pathlib.Path(__file__).resolve().parents[1]/"tools"
def mod(n,path):
 spec=importlib.util.spec_from_file_location(n,BASE/path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
align=mod("mli_align_episode","mli-align-episode.py")
styles=mod("mli_caption_styles","mli-caption-styles.py")
class EpisodeProductionTests(unittest.TestCase):
 def test_srt_clock(self):
  self.assertEqual(align.stamp(62.345),"00:01:02,345")
 def test_more_than_six_scenes_karaoke(self):
  words=[{"scene":f"SC{i:02}","word":"hello","start":i*2.0,"end":i*2.0+0.5} for i in range(1,19)]
  ass=styles.render(words,"karaoke")
  self.assertEqual(ass.count("Dialogue:"),18)
  self.assertIn(r"{\k",ass)
 def test_natural_grouping_no_cross_scene(self):
  w=[{"scene":"SC01","word":"hello","start":0,"end":0.4},{"scene":"SC02","word":"there","start":1,"end":1.4}]
  self.assertEqual(len(styles.groups(w)),2)
if __name__=="__main__":unittest.main()
