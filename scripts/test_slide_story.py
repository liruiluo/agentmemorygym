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
        d=Presentation(self.path);d.slides[0].shapes[0].text='ADDITIONAL November additions'
        with self.assertRaises(AssertionError):assert_slide_story(d)
    def test_missing_contribution_rejected(self):
        d=Presentation(self.path)
        index=next(i for i,e in enumerate(STORY) if e['role']=='Contributions')
        for o in d.slides[index].shapes:
            if o.has_text_frame:o.text=o.text.replace('Empirical study','Study')
        with self.assertRaises(AssertionError):assert_slide_story(d)
    def test_background_does_not_explain_solution(self):
        d=Presentation(self.path);d.slides[2].shapes[0].text='Use file operations with task reward'
        with self.assertRaisesRegex(AssertionError,'Background must stop'):assert_slide_story(d)
    def test_background_must_end_at_research_question(self):
        d=Presentation(self.path)
        index=next(i for i,e in enumerate(STORY) if e['role']=='Research problem')
        for o in d.slides[index].shapes:
            if o.has_text_frame:o.text=o.text.replace('How can post-training teach effective memory use?','Our solution follows now')
        with self.assertRaisesRegex(AssertionError,'Missing causal motivation'):assert_slide_story(d)
    def test_hypothesis_and_underuse_are_scoped(self):
        index=next(i for i,e in enumerate(STORY) if e['role']=='Research problem')
        visible='\n'.join(o.text for o in self.deck.slides[index].shapes if o.has_text_frame)
        self.assertIn('OBSERVED IN OUR AGEMEM-TOOL BASELINE',visible)
        self.assertIn('OUR HYPOTHESIS',visible)
        self.assertEqual(sum(e['seconds'] for e in STORY),870)
    def test_background_before_technical_case(self):
        d=Presentation(self.path)
        self.assertEqual(d.slides[1].shapes[0].text,'The story in four questions')
        d.slides[1].shapes[0].text='What should survive a context boundary?'
        with self.assertRaises(AssertionError):assert_slide_story(d)
    def test_merged_case_must_keep_the_memory_read(self):
        d=Presentation(self.path)
        case_index=next(i for i,e in enumerate(STORY) if e['role']=='Case study')
        for o in d.slides[case_index].shapes:
            if o.has_text_frame:o.text=o.text.replace('CONTINUATION.md','state-file')
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
