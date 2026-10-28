"""Regression checks for render integrity gates and persistent voice reports."""
import importlib.util
import json
import pathlib
import tempfile
import unittest
import wave
import hashlib
import copy
from unittest.mock import patch
ROOT = pathlib.Path(__file__).resolve().parents[1]
def module(name, file):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'tools' / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
render = module('episode_renderer', 'mli-render-episode.py')
voice = module('episode_voice', 'mli-voicestudio-tts.py')
align = module('episode_alignment', 'mli-align-episode.py')
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
    def test_continuous_narration_preserves_samples_and_offsets(self):
        with tempfile.TemporaryDirectory() as folder:
            base=pathlib.Path(folder);entries=[]
            for sid,frames,value in [('SC01',960,1),('SC02',720,2)]:
                path=base/(sid+'.wav')
                with wave.open(str(path),'wb') as w:
                    w.setparams((1,2,24000,0,'NONE','not compressed'));w.writeframes(value.to_bytes(2,'little')*frames)
                entries.append((sid,None,path,frames/24000))
            rows=[{'scene':'SC01','timeline_start':0,'clip_seconds':0.05},{'scene':'SC02','timeline_start':0.05,'clip_seconds':0.03}]
            render.assemble_narration(entries,rows,base/'joined.wav')
            with wave.open(str(base/'joined.wav')) as w:
                self.assertEqual(w.getnframes(),1920);data=w.readframes(1920)
            self.assertEqual(data[:1920],b'\x01\x00'*960)
            self.assertEqual(data[1920:2400],b'\0'*480)
            self.assertEqual(data[2400:],b'\x02\x00'*720)
    def alignment_fixture(self,base):
        (base/'audio').mkdir();wav=base/'audio/SC01.wav';wav.write_bytes(b'unchanged-audio-fixture')
        digest=hashlib.sha256(wav.read_bytes()).hexdigest()
        contract={'episode_id':'TEST','scenes':[{'id':'SC01','beat':'Hello.'}]}
        manifest={'scenes':[{'scene':'SC01','audio_seconds':1,'timeline_start':0,'audio_sha256':digest}]}
        data={'episode':'TEST','word_aligned':True,'scenes':[{'scene':'SC01','offset':0,'audio_duration':1,'audio_sha256':digest}],'words':[{'scene':'SC01','word':'Hello.','start':0.1,'end':0.7}]}
        return contract,manifest,data
    def test_real_alignment_reuse_keeps_word_times(self):
        with tempfile.TemporaryDirectory() as folder:
            base=pathlib.Path(folder);c,m,data=self.alignment_fixture(base);source=base/'source.json';source.write_text(json.dumps(data));target=base/'render';target.mkdir()
            with patch.object(align,'probe',return_value=1):result=align.reuse_alignment(source,target,c,m,base)
            self.assertEqual(result['words'],data['words'])
            self.assertTrue((target/'captions_words.srt').exists())
    def test_alignment_reuse_rejects_different_transcript(self):
        with tempfile.TemporaryDirectory() as folder:
            base=pathlib.Path(folder);c,m,data=self.alignment_fixture(base);data['words'][0]['word']='Different'
            with patch.object(align,'probe',return_value=1), self.assertRaisesRegex(ValueError,'Transcript mismatch'):
                align.validate_alignment(data,c,m,base)
    def test_alignment_reuse_rejects_changed_audio(self):
        with tempfile.TemporaryDirectory() as folder:
            base=pathlib.Path(folder);c,m,data=self.alignment_fixture(base);(base/'audio/SC01.wav').write_bytes(b'changed-voice')
            with patch.object(align,'probe',return_value=1), self.assertRaisesRegex(ValueError,'Audio hash mismatch'):
                align.validate_alignment(data,c,m,base)
    def test_alignment_reuse_rejects_timeline_shift(self):
        with tempfile.TemporaryDirectory() as folder:
            base=pathlib.Path(folder);c,m,data=self.alignment_fixture(base);data['scenes'][0]['offset']=0.2
            with patch.object(align,'probe',return_value=1), self.assertRaisesRegex(ValueError,'Timeline mismatch'):
                align.validate_alignment(data,c,m,base)
    def test_clip_encode_retries_once_without_source_generation(self):
        with tempfile.TemporaryDirectory() as folder:
            target=pathlib.Path(folder)/'SC01.mp4'
            with patch.object(render,'run',side_effect=[RuntimeError('incomplete encode'),None]) as encode, patch.object(render,'validate_media',return_value=5):
                self.assertEqual(render.encode_clip(['ffmpeg'],target,5),5)
                self.assertEqual(encode.call_count,2)
            self.assertEqual(len(list((target.parent/'render_failures').glob('*.json'))),1)
    def test_clip_encode_is_bounded_on_persistent_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            target=pathlib.Path(folder)/'SC01.mp4'
            with patch.object(render,'run',side_effect=RuntimeError('encoder failed')) as encode:
                with self.assertRaisesRegex(RuntimeError,'two attempts'):
                    render.encode_clip(['ffmpeg'],target,5)
                self.assertEqual(encode.call_count,2)
if __name__=='__main__':
    unittest.main()

