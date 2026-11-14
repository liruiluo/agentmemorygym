"""Regress the talk structure and original-figure boundary, not just a page count."""
import hashlib,json,tempfile,unittest
from pathlib import Path
from pptx import Presentation
from build_slides import build,ROOT
from slide_story import STORY,assert_slide_story

class SlideStoryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();cls.path=Path(cls.tmp.name)/'deck.pptx'
        build(cls.path);cls.deck=Presentation(cls.path)
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def test_positive_story(self):self.assertTrue(assert_slide_story(self.deck))
    def test_report_labels_rejected(self):
        d=Presentation(self.path);d.slides[6].shapes[0].text='ADDITIONAL November additions'
        with self.assertRaises(AssertionError):assert_slide_story(d)
    def test_missing_contribution_rejected(self):
        d=Presentation(self.path)
        for o in d.slides[6].shapes:
            if o.has_text_frame:o.text=o.text.replace('Empirical study','Study')
        with self.assertRaises(AssertionError):assert_slide_story(d)
    def test_chapters_match_story(self):
        for s,entry in zip(self.deck.slides,STORY):
            if entry['phase']:
                self.assertIn(entry['phase'],'\n'.join(o.text for o in s.shapes if o.has_text_frame))
    def test_exact_original_figure_bindings(self):
        assets=json.loads((ROOT/'slides/figure-assets.json').read_text());seen=[]
        for s in self.deck.slides:
            for o in s.shapes:
                if o.name.startswith('paper-figure:'):
                    key=o.name.split(':',1)[1];seen.append(key);a=assets[key]
                    self.assertEqual(hashlib.sha256(o.image.blob).hexdigest(),a['png_sha256'])
                    for kind in ('png','pdf'):
                        self.assertEqual(hashlib.sha256((ROOT/a[kind]).read_bytes()).hexdigest(),a[kind+'_sha256'])
        self.assertEqual(seen,['fig1_camg_teaser','fig2_camg_framework'])
    def test_secondary_results_stay_off_stage(self):
        visible=assert_slide_story(self.deck)
        self.assertNotIn('55.3',visible);self.assertNotIn('20.9',visible)
        notes=(self.path.parent/'speaker-notes.md').read_text()
        self.assertIn('55.3 ± 2.9',notes);self.assertIn('20.9%',notes)

if __name__=='__main__':unittest.main()
