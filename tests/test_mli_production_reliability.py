"""Regression checks for render integrity gates and persistent voice reports."""
import importlib.util
import json
import pathlib
import tempfile
import unittest
from unittest.mock import patch
ROOT = pathlib.Path(__file__).resolve().parents[1]
def module(name, file):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'tools' / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
render = module('episode_renderer', 'mli-render-episode.py')
voice = module('episode_voice', 'mli-voicestudio-tts.py')
class ReliabilityTests(unittest.TestCase):
    def test_truncated_master_is_rejected(self):
        with patch.object(render, 'probe', return_value={'streams':[{'codec_type':'video'},{'codec_type':'audio'}], 'format':{'duration':'14.0'}}):
            with self.assertRaisesRegex(ValueError, 'Duration mismatch'):
                render.validate_media('master.mp4', 103.7)
    def test_missing_audio_is_rejected(self):
        with patch.object(render, 'probe', return_value={'streams':[{'codec_type':'video'}], 'format':{'duration':'5'}}):
            with self.assertRaisesRegex(ValueError, 'Missing audio/video'):
                render.validate_media('clip.mp4', 5)
    def test_decode_failure_blocks_valid_duration(self):
        with patch.object(render, 'probe', return_value={'streams':[{'codec_type':'video'},{'codec_type':'audio'}], 'format':{'duration':'5'}}), patch.object(render,'run',side_effect=RuntimeError('decode failed')):
            with self.assertRaisesRegex(RuntimeError, 'decode failed'):
                render.validate_media('clip.mp4', 5, full_decode=True)
    def test_voice_failure_survives_next_run(self):
        with tempfile.TemporaryDirectory() as folder:
            work=pathlib.Path(folder)
            first={'scenes':[{'scene':'SC15','status':'FAIL','error':'sidecar timeout 300s'}]}
            voice.save_progress(work,first,'first')
            second={'scenes':[{'scene':'SC15','status':'GENERATED'}]}
            voice.save_progress(work,second,'second')
            self.assertEqual(json.loads((work/'voice_history/first.json').read_text()),first)
            self.assertEqual(json.loads((work/'voice_production_report.json').read_text()),second)
    def test_valid_media_runs_full_decode(self):
        with patch.object(render,'probe',return_value={'streams':[{'codec_type':'video'},{'codec_type':'audio'}], 'format':{'duration':'5.04'}}), patch.object(render,'run',return_value='') as decode:
            self.assertEqual(render.validate_media('clip.mp4',5,True),5.04)
            self.assertIn('-xerror',decode.call_args.args[0])
if __name__=='__main__':
    unittest.main()
