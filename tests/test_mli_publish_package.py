import importlib.util,pathlib,tempfile,unittest,json,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('publish',ROOT/'tools/mli-publish-package.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class PublicationGuards(unittest.TestCase):
    def plan(self):return {'format':'MLI_PUBLISH_PLAN_V1','title':'An honest title','description':'A description','thumbnail_source':'thumbnail.jpg'}
    def test_title_limit(self):
        p=self.plan();p['title']='x'*101
        with self.assertRaises(ValueError):m.validate_text(p)
    def test_description_limit(self):
        p=self.plan();p['description']='x'*5001
        with self.assertRaises(ValueError):m.validate_text(p)
    def test_chapter_offsets_use_real_timeline(self):
        p={'chapters':[{'scene':s,'title':s} for s in ['SC01','SC09','SC17']]};manifest={'scenes':[{'scene':s,'timeline_start':t} for s,t in [('SC01',0),('SC09',83.353333),('SC17',180.086666)]]}
        self.assertEqual([x['seconds'] for x in m.chapters(p,manifest,200)],[0,83,180])
    def test_short_chapters_rejected(self):
        p={'chapters':[{'scene':s,'title':s} for s in ['SC01','SC02','SC03']]};manifest={'scenes':[{'scene':s,'timeline_start':t} for s,t in [('SC01',0),('SC02',4),('SC03',20)]]}
        with self.assertRaises(ValueError):m.chapters(p,manifest,50)
    def test_path_escape_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):m.safe(pathlib.Path(d),'../outside')
    def test_unknown_word_scene_rejected(self):
        a={'episode':'EP','word_aligned':True,'scenes':[{'scene':'SC01'}],'words':[{'scene':'SC99','word':'Hello','start':0,'end':1}]};c={'episode_id':'EP','scenes':[{'id':'SC01','beat':'Hello'}]};manifest={'scenes':[{'scene':'SC01'}]}
        with self.assertRaises(ValueError):m.alignment_words(a,c,manifest,10)
    def test_wrong_transcript_rejected(self):
        a={'episode':'EP','word_aligned':True,'scenes':[{'scene':'SC01'}],'words':[{'scene':'SC01','word':'Wrong','start':0,'end':1}]};c={'episode_id':'EP','scenes':[{'id':'SC01','beat':'Hello'}]};manifest={'scenes':[{'scene':'SC01'}]}
        with self.assertRaises(ValueError):m.alignment_words(a,c,manifest,10)
    def test_tampered_package_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=pathlib.Path(d);(p/'title.txt').write_text('changed');m.write(p/'package_manifest.json',{'format':'MLI_PUBLISH_PACKAGE_V1','files':{'title.txt':hashlib.sha256(b'original').hexdigest()}})
            with self.assertRaises(ValueError):m.check_folder(p)

if __name__=='__main__':unittest.main()
