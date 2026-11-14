import unittest
from copy import deepcopy
from research_data import load,stats,validate
from build_website import build

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
        self.assertIn('Published · Appendix D.8',build())
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
