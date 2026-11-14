"""Regress the talk structure and original-figure boundary, not just a page count."""
import hashlib,json,tempfile,unittest
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches
from build_slides import build,ROOT
from slide_story import STORY,QUESTIONS,SUBQUESTIONS,EXPERIMENT_DESIGNS,question_label,assert_slide_story

class SlideStoryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();cls.path=Path(cls.tmp.name)/'deck.pptx'
        build(cls.path);cls.deck=Presentation(cls.path)
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def test_positive_story(self):self.assertTrue(assert_slide_story(self.deck))
    def test_final_slide_is_explicit_takeaways(self):
        self.assertEqual(self.deck.slides[-1].shapes[0].text,'Takeaways')
        content='\n'.join(o.text for o in self.deck.slides[-1].shapes if o.has_text_frame)
        for phrase in ['Start from a familiar interface.','Train memory through the task.','Learn a behavior that can be reused.','liruiluo.github.io/agentmemorygym']:
            self.assertIn(phrase,content)
    def test_slogan_cannot_replace_takeaways_heading(self):
        d=Presentation(self.path);d.slides[-1].shapes[0].text='Familiar operations. Learned memory.'
        with self.assertRaisesRegex(AssertionError,'Final slide must be titled Takeaways'):assert_slide_story(d)
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
        self.assertNotIn('0%',visible)
        self.assertNotIn('illustration',visible.lower())
        self.assertNotIn('AGEMEM-TOOL BASELINE',visible)
        self.assertIn('OUR HYPOTHESIS',visible)
        self.assertEqual(sum(e['seconds'] for e in STORY),870)
    def test_background_before_technical_case(self):
        d=Presentation(self.path)
        self.assertEqual(d.slides[1].shapes[0].text,'The story in four questions')
        d.slides[1].shapes[0].text='What should survive a context boundary?'
        with self.assertRaises(AssertionError):assert_slide_story(d)
    def test_case_cannot_be_replaced_by_a_redraw(self):
        d=Presentation(self.path)
        case_index=next(i for i,e in enumerate(STORY) if e['role']=='Case study')
        pic=next(o for o in d.slides[case_index].shapes if o.name=='paper-figure:fig5_coding_case')
        pic.name='custom-redraw'
        with self.assertRaisesRegex(AssertionError,'Case must use the complete original'):assert_slide_story(d)
    def test_case_panels_cannot_be_cropped(self):
        d=Presentation(self.path)
        pic=next(o for o in d.slides[13].shapes if o.name=='paper-figure:fig5_coding_case')
        pic.crop_left=.1
        with self.assertRaisesRegex(AssertionError,'Do not crop the case figure'):assert_slide_story(d)
    def test_chapters_match_story(self):
        for s,entry in zip(self.deck.slides,STORY):
            if entry['phase']:
                self.assertIn(entry['phase'],'\n'.join(o.text for o in s.shapes if o.has_text_frame))
    def test_three_experimental_questions(self):
        self.assertEqual(list(QUESTIONS),['Q1','Q2','Q3'])
        self.assertEqual([e['phase'] for e in STORY[8:16]],['Q1']*2+['Q2.1','Q2.1','Q2.2','Q2']+['Q3']*2)
        self.assertEqual(STORY[13]['role'],'Case study')
        for i,entry in enumerate(STORY[8:16],8):
            q=next(o for o in self.deck.slides[i].shapes if o.name.startswith('result-question:'))
            self.assertEqual(q.text,question_label(entry['phase']))
            self.assertNotEqual(self.deck.slides[i].shapes[0].text,q.text)
            self.assertLess(q.top.inches,1)
        notes=(self.path.parent/'speaker-notes.md').read_text()
        for q,n in [('Q1',2),('Q2.1',2),('Q2.2',1),('Q2',1),('Q3',2)]:
            self.assertEqual(notes.count('**Experimental question:** '+question_label(q)),n)
    def test_two_distinct_q2_subquestions(self):
        self.assertEqual(list(SUBQUESTIONS),['Q2.1','Q2.2'])
        self.assertEqual(QUESTIONS['Q2'],'What drives CAMP’s gains?')
        self.assertEqual([e['experiment'] for e in STORY[10:14]],['ablation','intervention','prior',None])
        self.assertEqual([self.deck.slides[i].shapes[0].text for i in [10,11,12]],['Memory actions need the learning signal','The saved content changes what happens next','The file interface is familiar before RL'])
        self.assertEqual(STORY[13]['phase'],'Q2')
        self.assertNotIn('Q2.3',assert_slide_story(self.deck))
    def test_memory_slide_cannot_use_prior_subquestion(self):
        d=Presentation(self.path)
        q=next(o for o in d.slides[10].shapes if o.name.startswith('result-question:'))
        q.text=question_label('Q2.2')
        with self.assertRaisesRegex(AssertionError,'question text drift'):assert_slide_story(d)
    def test_case_must_close_parent_q2(self):
        d=Presentation(self.path)
        q=next(o for o in d.slides[13].shapes if o.name.startswith('result-question:'))
        q.name='result-question:Q2.3';q.text='Q2.3 · Case study'
        with self.assertRaisesRegex(AssertionError,'wrong experimental question label'):assert_slide_story(d)
    def test_navigation_above_prominent_title(self):
        for slide,entry in zip(self.deck.slides,STORY):
            if not entry['chapter']:continue
            title=slide.shapes[0]
            for marker in slide.shapes:
                if marker.name.startswith(('chapter-navigation:','result-question:')):
                    self.assertLess(marker.top+marker.height,title.top)
                    self.assertLess(marker.text_frame.paragraphs[0].runs[0].font.size,title.text_frame.paragraphs[0].runs[0].font.size)
            self.assertLessEqual(title.top+title.height,Inches(.99))
    def test_navigation_below_title_rejected(self):
        d=Presentation(self.path)
        nav=next(o for o in d.slides[5].shapes if o.name.startswith('chapter-navigation:'))
        nav.top=Inches(.79)
        with self.assertRaisesRegex(AssertionError,'Navigation must precede'):assert_slide_story(d)
    def test_question_below_title_rejected(self):
        d=Presentation(self.path)
        q=next(o for o in d.slides[8].shapes if o.name.startswith('result-question:'))
        q.top=Inches(.77)
        with self.assertRaisesRegex(AssertionError,'Navigation must precede'):assert_slide_story(d)
    def test_wrong_question_rejected(self):
        d=Presentation(self.path)
        q=next(o for o in d.slides[10].shapes if o.name.startswith('result-question:'))
        q.text=question_label('Q3')
        with self.assertRaisesRegex(AssertionError,'question text drift'):assert_slide_story(d)
    def test_case_after_transfer_rejected(self):
        d=Presentation(self.path);ids=d.slides._sldIdLst
        case=ids[13];ids.remove(case);ids.insert(15,case)
        with self.assertRaisesRegex(AssertionError,'technical case'):assert_slide_story(d)
    def test_experiment_design_is_on_stage(self):
        self.assertEqual([i+1 for i,e in enumerate(STORY) if e['experiment']],[9,10,11,12,13,15,16])
        for i,e in enumerate(STORY):
            shapes=[o for o in self.deck.slides[i].shapes if o.name.startswith('experiment-design:')]
            if not e['experiment']:
                self.assertFalse(shapes);continue
            self.assertEqual(shapes[0].text,EXPERIMENT_DESIGNS[e['experiment']])
            self.assertIn(shapes[0].text,self.deck.slides[i].notes_slide.notes_text_frame.text)
            self.assertIn(shapes[0].text,(self.path.parent/'speaker-notes.md').read_text())
    def test_missing_design_rejected(self):
        d=Presentation(self.path)
        o=next(o for o in d.slides[12].shapes if o.name.startswith('experiment-design:'))
        o.name='ordinary-text'
        with self.assertRaisesRegex(AssertionError,'Missing experiment design'):assert_slide_story(d)
    def test_key_control_omission_rejected(self):
        d=Presentation(self.path)
        o=next(o for o in d.slides[14].shapes if o.name.startswith('experiment-design:'))
        o.text=o.text.replace('task executor fixed','task executor trained')
        with self.assertRaisesRegex(AssertionError,'Experiment design text drift'):assert_slide_story(d)
    def test_design_cannot_be_buried_in_footer(self):
        d=Presentation(self.path)
        o=next(o for o in d.slides[12].shapes if o.name.startswith('experiment-design:'))
        o.top=Inches(5.3)
        with self.assertRaisesRegex(AssertionError,'Design must be visible'):assert_slide_story(d)
    def test_design_cannot_be_tiny(self):
        from pptx.util import Pt
        d=Presentation(self.path)
        o=next(o for o in d.slides[10].shapes if o.name.startswith('experiment-design:'))
        o.text_frame.paragraphs[0].runs[0].font.size=Pt(9)
        with self.assertRaisesRegex(AssertionError,'Experiment design must be readable'):assert_slide_story(d)
    def test_design_conditions_are_specific(self):
        self.assertIn('context and compaction differ',EXPERIMENT_DESIGNS['long_context'])
        self.assertIn('frozen Qwen3.5-4B',EXPERIMENT_DESIGNS['prior'])
        self.assertIn('keep rewards/critic',EXPERIMENT_DESIGNS['ablation'])
        self.assertIn('or use only CONTINUATION.md',EXPERIMENT_DESIGNS['ablation'])
        self.assertIn('same post-reset state',EXPERIMENT_DESIGNS['intervention'])
        self.assertIn('intact, blank or shuffled',EXPERIMENT_DESIGNS['intervention'])
        self.assertIn('replace only the memory policy',EXPERIMENT_DESIGNS['transfer'])
        self.assertIn('no further training',EXPERIMENT_DESIGNS['transfer'])
        self.assertIn('same 4B and 9B model scales',EXPERIMENT_DESIGNS['external'])
    def test_exact_original_figure_bindings(self):
        assets=json.loads((ROOT/'slides/figure-assets.json').read_text());seen=[]
        for s in self.deck.slides:
            for o in s.shapes:
                if o.name.startswith('paper-figure:'):
                    key=o.name.split(':',1)[1];seen.append(key);a=assets[key]
                    self.assertEqual(hashlib.sha256(o.image.blob).hexdigest(),a['png_sha256'])
                    for kind in ('png','pdf'):
                        self.assertEqual(hashlib.sha256((ROOT/a[kind]).read_bytes()).hexdigest(),a[kind+'_sha256'])
        self.assertEqual(seen,['fig1_context_only','fig2_environments','fig1_camg_teaser','fig2_camg_framework','fig5_coding_case'])
        crop=assets['fig1_context_only'];self.assertEqual(crop['clip_pt'],[0,0,1536,400])
        self.assertEqual(crop['pdf_sha256'],assets['fig1_camg_teaser']['pdf_sha256'])
        picture=next(o for o in self.deck.slides[2].shapes if o.name=='paper-figure:fig1_context_only')
        self.assertAlmostEqual(picture.crop_bottom,5/9,places=5)
    def test_case_original_is_bound_to_published_figure(self):
        from verify_release import verify_original_case_asset
        self.assertTrue(verify_original_case_asset(ROOT))
        a=json.loads((ROOT/'slides/figure-assets.json').read_text())['fig5_coding_case']
        self.assertNotIn('clip_pt',a)
        self.assertEqual([a['width_pt'],a['height_pt']],[1611.75,735.0])
    def test_case_figure_wrong_source_hash_is_rejected(self):
        from verify_release import verify_original_case_asset
        import shutil
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'slides').mkdir();(root/'assets/slides/figures').mkdir(parents=True)
            data=json.loads((ROOT/'slides/figure-assets.json').read_text());a=data['fig5_coding_case']
            shutil.copy2(ROOT/a['pdf'],root/a['pdf']);shutil.copy2(ROOT/a['source_paper'],root/a['source_paper'])
            a['source_paper_sha256']='0'*64
            (root/'slides/figure-assets.json').write_text(json.dumps(data))
            with self.assertRaisesRegex(AssertionError,'Case paper source drift'):verify_original_case_asset(root)
    def test_environment_panel_is_exact_crop(self):
        a=json.loads((ROOT/'slides/figure-assets.json').read_text())
        self.assertEqual(a['fig2_environments']['clip_pt'],[802,68,1140,480])
        self.assertEqual(a['fig2_environments']['pdf_sha256'],a['fig2_camg_framework']['pdf_sha256'])
        p=next(o for o in self.deck.slides[5].shapes if o.name=='paper-figure:fig2_environments')
        self.assertAlmostEqual(p.crop_left,802/1152,places=5)
        self.assertAlmostEqual(p.crop_top,68/768,places=5)
    def test_environment_text_remains_necessary(self):
        d=Presentation(self.path)
        for o in d.slides[5].shapes:
            if o.has_text_frame:o.text=o.text.replace('purchase history','details')
        with self.assertRaisesRegex(AssertionError,'Missing environment memory demand'):assert_slide_story(d)
    def test_defensive_motivation_labels_rejected(self):
        d=Presentation(self.path);d.slides[3].shapes[-1].text+=' (illustration)'
        with self.assertRaisesRegex(AssertionError,'defensive'):assert_slide_story(d)
    def test_zero_motivation_statistic_rejected(self):
        d=Presentation(self.path);d.slides[3].shapes[-1].text+=' 0%'
        with self.assertRaisesRegex(AssertionError,'zero statistic'):assert_slide_story(d)
    def test_generated_asset_binding(self):
        a=json.loads((ROOT/'slides/illustration-assets.json').read_text())['memory_tools_unused']
        o=next(o for o in self.deck.slides[3].shapes if o.name.startswith('generated-illustration:'))
        self.assertEqual(hashlib.sha256(o.image.blob).hexdigest(),a['image_sha256'])
        self.assertEqual(hashlib.sha256((ROOT/a['prompt']).read_bytes()).hexdigest(),a['prompt_sha256'])
        self.assertEqual(a['requested_model'],'gpt-image-2')
    def test_secondary_results_stay_off_stage(self):
        visible=assert_slide_story(self.deck)
        self.assertNotIn('55.3',visible);self.assertNotIn('20.9',visible)
        notes=(self.path.parent/'speaker-notes.md').read_text()
        self.assertIn('55.3 ± 2.9',notes);self.assertIn('20.9%',notes)

if __name__=='__main__':unittest.main()
