"""Audience-facing talk structure; scientific provenance stays in research.json/notes."""
import re


def entry(chapter,role,exhibit,source,phase=None):
    return dict(chapter=chapter,role=role,exhibit=exhibit,source=source,phase=phase)

STORY=[
    entry(None,'Identity','Full title, authors, affiliation and links','CAMP · arXiv:2609.34422'),
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
    entry('Results & analysis','Case study','Scrapy saved note + read/check actions + successful finish','Scrapy case · Figure 5 · recorded training episode','Case study'),
    entry(None,'Conclusion','Three takeaways and project link','CAMP · paper, code and slides'),
]

# Fourteen and a half minutes of speaking plus transitions.
for row,seconds in zip(STORY,[45,20,80,50,55,25,55,85,60,45,55,60,60,50,85,40]):
    row['seconds']=seconds

def visible_source(number):
    return STORY[number-1]['source']

def assert_slide_story(deck):
    assert len(deck.slides)==len(STORY),'Talk length and outline drift'
    visible='\n'.join(o.text for s in deck.slides for o in s.shapes if o.has_text_frame)
    for pattern in [r'author.reported',r'November additions',r'ADDITIONAL',r'evidence versions?',r'five runs per method',r'raw run receipts',r'published results']:
        assert not re.search(pattern,visible,re.I),f'Report-style audience text: {pattern}'
    text_at=lambda n:'\n'.join(o.text for o in deck.slides[n-1].shapes if o.has_text_frame)
    page_for=lambda role:next(i+1 for i,e in enumerate(STORY) if e['role']==role)
    assert STORY[1]['role']=='Roadmap' and STORY[2]['role']=='Why CAMP'
    for word in ['Background','Environments','Method','Results & analysis']:
        assert word in text_at(page_for('Roadmap')),f'Missing roadmap chapter {word}'
    for word in ['Long tasks outgrow','memory-tool interface','training setting','CAMP’S QUESTION']:
        assert word in text_at(page_for('Why CAMP')),f'Missing work-specific motivation {word}'
    for word in ['CAMG','CAMG-RL','Empirical study']:
        assert word in text_at(page_for('Contributions')),f'Missing contribution {word}'
    assert 'Fully asynchronous PPO' in text_at(page_for('Learning mechanism'))
    for role,key in [('Core idea','fig1_camg_teaser'),('Learning mechanism','fig2_camg_framework')]:
        assert [o.name for o in deck.slides[page_for(role)-1].shapes if o.name.startswith('paper-figure:')]==['paper-figure:'+key]
    case=page_for('Case study')
    assert case>max(i+1 for i,e in enumerate(STORY) if e['role']=='Transfer')
    assert [n for n in range(1,len(STORY)+1) if 'Scrapy' in text_at(n)]==[case],'The technical case must appear once, after the results'
    assert 'What should survive a context boundary?' not in visible
    for word in ['CONTINUATION.md','objective: fix response logging','Hidden tests passed','1.00','pytest']:
        assert word in text_at(case),f'Merged case is incomplete: {word}'
    return visible
