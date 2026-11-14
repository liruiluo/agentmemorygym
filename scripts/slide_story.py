"""Audience-facing talk structure; scientific provenance stays in research.json/notes."""
import re


def entry(chapter,role,exhibit,source,phase=None):
    return dict(chapter=chapter,role=role,exhibit=exhibit,source=source,phase=phase)

STORY=[
    entry(None,'Identity','Full title, authors, affiliation and links','CAMP · arXiv:2609.34422'),
    entry('Background','Opening case','Recorded Scrapy continuation write/read','Scrapy case · Figure 5 · shortened training-episode excerpts'),
    entry(None,'Roadmap','Four chapters and the questions they answer','CAMP · talk roadmap'),
    entry('Background','Why CAMP','Interface and training-setting gaps → research question','Motivation · Introduction'),
    entry('Background','Why files','Frozen-model file vs. dedicated-tool likelihood','Interface familiarity · Figure 3a · frozen Qwen3.5-4B'),
    entry('Background','Core idea','Original Figure 1, both contrast rows','Figure 1 · conceptual illustration'),
    entry('Background','Contributions','Environment suite / learning method / empirical study','CAMP · three contributions'),
    entry('Environments','Task demands','Four task families and the state each must retain','CAMG · Shop / Coding / DeepResearch / AutoResearch'),
    entry('Method','Learning mechanism','Original Figure 2 + shared policy/reward/PPO callouts','CAMG-RL · Figure 2 · fully asynchronous PPO'),
    entry('Results & analysis','Effectiveness','Six-method main comparison','Task success · Qwen3.5-4B · 128 held-out tasks per environment','Effectiveness'),
    entry('Results & analysis','Effectiveness','262K-context practical reference','Same base, PPO, rewards and updates; context and compaction differ','Effectiveness'),
    entry('Results & analysis','Mechanism','Memory-action gradient and continuation ablations','Ablations · Figure 4 · average task success','Mechanism'),
    entry('Results & analysis','Mechanism','Blank/shuffled memory from the same state','Memory-content intervention · same-state continuations · eligible tasks','Mechanism'),
    entry('Results & analysis','Transfer','New memory interfaces, fixed task executor','Frozen task executor · memory policy changed · no further training','Transfer'),
    entry('Results & analysis','Transfer','Matched base vs. trained external results','SWE-bench Verified / MLE-bench Lite · matched model scales','Transfer'),
    entry('Results & analysis','Case payoff','Scrapy edit → write → read → successful finish','Scrapy case · Figure 5 · recorded training episode','Case study'),
    entry(None,'Conclusion','Three takeaways and project link','CAMP · paper, code and slides'),
]

# Fourteen and a half minutes of speaking plus transitions.
for row,seconds in zip(STORY,[45,55,20,65,50,55,25,55,85,60,45,55,60,60,50,45,40]):
    row['seconds']=seconds

def visible_source(number):
    return STORY[number-1]['source']

def assert_slide_story(deck):
    assert len(deck.slides)==len(STORY),'Talk length and outline drift'
    visible='\n'.join(o.text for s in deck.slides for o in s.shapes if o.has_text_frame)
    for pattern in [r'author.reported',r'November additions',r'ADDITIONAL',r'evidence versions?',r'five runs per method',r'raw run receipts',r'published results']:
        assert not re.search(pattern,visible,re.I),f'Report-style audience text: {pattern}'
    text_at=lambda n:'\n'.join(o.text for o in deck.slides[n-1].shapes if o.has_text_frame)
    for word in ['Background','Environments','Method','Results & analysis']:
        assert word in text_at(3),f'Missing roadmap chapter {word}'
    for word in ['memory-tool interface','training setting','CAMP’S QUESTION']:
        assert word in text_at(4),f'Missing work-specific motivation {word}'
    for word in ['CAMG','CAMG-RL','Empirical study']:
        assert word in text_at(7),f'Missing contribution {word}'
    assert 'Fully asynchronous PPO' in text_at(9)
    for n,key in [(6,'fig1_camg_teaser'),(9,'fig2_camg_framework')]:
        assert [o.name for o in deck.slides[n-1].shapes if o.name.startswith('paper-figure:')]==['paper-figure:'+key]
    assert 'Scrapy' in text_at(2) and 'Hidden tests passed' in text_at(16)
    return visible
