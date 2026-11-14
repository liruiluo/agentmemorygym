import unittest
from copy import deepcopy
from research_data import load,stats,validate
from build_website import build
from presentation_policy import assert_public_story

class ResearchTests(unittest.TestCase):
    def setUp(self):self.d=load()
    def test_paired_figures(self):
        k=stats(self.d)
        self.assertEqual((k['MAIN_GAP'],k['CD_GAP'],k['CONTEXT_GAIN']),('6.4','4.3','5.2'))
        self.assertEqual((k['TRANSFER_FILE_GAIN'],k['TRANSFER_TOOL_GAIN']),('11.4','6.4'))
    def test_source_versions(self):
        self.assertIn('v2',self.d['sources']['paper']['url'])
        self.assertIn('Table 2',self.d['main']['reference'])
        self.assertFalse(self.d['sources']['additional']['independently_run_verified'])
    def test_robustness_is_already_published(self):
        self.assertEqual(self.d['robustness']['source'],'paper')
        self.assertIn('Appendix D.8',self.d['robustness']['reference'])
    def test_public_page_is_a_story(self):
        text=assert_public_story(build())
        for key in ['Read. Write. Search. Revise.','Erase the memory.','A saved note becomes']:
            self.assertIn(key,text)
    def test_hidden_line_breaks_keep_word_spacing(self):
        # Mobile hides selected br elements; adjacent words must still separate.
        self.assertNotRegex(build(), r'<br>(?=\S)')
    def test_report_prose_rejected_even_in_details(self):
        for phrase in ['Two evidence versions','Across five training runs','Raw run receipts were not independently re-verified','Published results','95% confidence interval']:
            with self.subTest(phrase=phrase):
                with self.assertRaises(AssertionError):
                    assert_public_story('<details><summary>More</summary><p>'+phrase+'</p></details>')
    def test_story_keeps_comparison_conditions(self):
        text=assert_public_story(build())
        self.assertIn('task-execution policy is held fixed',text)
        self.assertIn('different context-management strategies',text)
        self.assertIn('real training episode',text)
    def test_external_values_come_from_shared_data(self):
        html=build()
        for value in ['7.6','15.8','14.8','27.6','4.5','9.1']:
            self.assertIn('<strong>'+value+'</strong>',html)
    def test_no_unverified_quality_panel(self):self.assertNotIn('quality_rows',self.d['transfer'])
    def test_wrong_domain_rejected(self):
        other=deepcopy(self.d);other['domains'][-1]='Visual'
        with self.assertRaises(AssertionError):validate(other)
    def test_missing_numeric_cell_rejected(self):
        other=deepcopy(self.d);other['main']['rows'][0].pop()
        with self.assertRaises(AssertionError):validate(other)
    def test_unresolved_tokens(self):self.assertNotIn('{{',build())
    def test_original_anchors(self):
        page=build()
        for name in ['top','idea','gym','method','evidence','paper']:self.assertIn('id="'+name+'"',page)
    def test_intervention_negative(self):
        for row in self.d['intervention']['rows']:
            self.assertLess(row[1],0);self.assertLess(row[2],0)
    def test_standard_deviation_not_ci(self):
        self.assertIn('not confidence',self.d['robustness']['boundary'])
        self.assertEqual(self.d['robustness']['runs_per_method'],5)
    def test_all_results_without_javascript(self):
        html=build()
        for name in ['Qwen3.5-4B','CompactionRL','AgeMem','CAMG-RL','Claude Code']:
            self.assertIn(name,html)
        for panel in ['case-write','case-read','case-test']:self.assertIn('id="'+panel+'"',html)

if __name__=='__main__':unittest.main()
