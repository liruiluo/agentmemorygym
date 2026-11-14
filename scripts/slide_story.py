"""Audience-facing talk structure; scientific provenance stays in research.json/notes."""
import re


def entry(chapter,role,exhibit,source,phase=None):
    return dict(chapter=chapter,role=role,exhibit=exhibit,source=source,phase=phase)

STORY=[
    entry(None,'Identity','Full title, authors, affiliation and links','CAMP · arXiv:2609.34422'),
    entry(None,'Roadmap','Four chapters and the questions they answer','CAMP · talk roadmap'),
    entry('Background','Memory need','Figure 1 upper row: context lost → repeated work → unfinished task','Figure 1 · context-only row'),
    entry('Background','Research problem','Unused memory tools → lost constraint → failure; prior-mismatch hypothesis → question','Memory use · the research problem'),
    entry(None,'Contributions','Environment suite / learning method / empirical study','CAMP · three contributions'),
    entry('Environments','Task demands','Figure 2 environment panel + what each task family must remember','CAMG · Figure 2 · environment panel'),
    entry('Method','Core idea','Original Figure 1, both contrast rows','Figure 1 · conceptual illustration'),
    entry('Method','Learning mechanism','Original Figure 2 + shared policy/reward/PPO callouts','CAMG-RL · Figure 2 · fully asynchronous PPO'),
    entry('Results & analysis','Effectiveness','Six-method main comparison','Task success · Qwen3.5-4B · 128 held-out tasks per environment','Effectiveness'),
    entry('Results & analysis','Effectiveness','262K-context practical reference','Same base, PPO, rewards and updates; context and compaction differ','Effectiveness'),
    entry('Results & analysis','Prior evidence','Frozen-model file vs. dedicated-tool likelihood','Interface familiarity · Figure 3a · frozen Qwen3.5-4B','Mechanism'),
    entry('Results & analysis','Mechanism','Memory-action gradient and continuation ablations','Ablations · Figure 4 · average task success','Mechanism'),
    entry('Results & analysis','Mechanism','Blank/shuffled memory from the same state','Memory-content intervention · same-state continuations · eligible tasks','Mechanism'),
    entry('Results & analysis','Transfer','New memory interfaces, fixed task executor','Frozen task executor · memory policy changed · no further training','Transfer'),
    entry('Results & analysis','Transfer','Matched base vs. trained external results','SWE-bench Verified / MLE-bench Lite · matched model scales','Transfer'),
    entry('Results & analysis','Case study','Scrapy saved note + read/check actions + successful finish','Scrapy case · Figure 5 · recorded training episode','Case study'),
    entry(None,'Conclusion','Three takeaways and project link','CAMP · paper, code and slides'),
]

# Fourteen and a half minutes of speaking plus transitions.
for row,seconds in zip(STORY,[35,20,45,80,25,50,60,75,60,40,50,50,55,55,50,80,40]):
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
    assert STORY[1]['role']=='Roadmap' and STORY[2]['role']=='Memory need'
    for word in ['Background','Environments','Method','Results & analysis']:
        assert word in text_at(page_for('Roadmap')),f'Missing roadmap chapter {word}'
    for word in ['Earlier findings','leave the prompt','Without memory']:
        assert word in text_at(page_for('Memory need')),f'Missing memory need {word}'
    for word in ['OUR HYPOTHESIS','pre-trained behavioral priors','How can post-training teach effective memory use?']:
        assert word in text_at(page_for('Research problem')),f'Missing causal motivation {word}'
    problem=text_at(page_for('Research problem'))
    assert '0%' not in problem,'Do not foreground a zero statistic in the motivation'
    for phrase in ['illustration','illustrative','not a real','not a recorded','not a measured']:
        assert phrase not in problem.lower(),'No defensive labels on the visual motivation'
    assert [o.name for o in deck.slides[page_for('Research problem')-1].shapes if o.name.startswith('generated-illustration:')]==['generated-illustration:memory_tools_unused']
    background='\n'.join(text_at(i+1) for i,e in enumerate(STORY) if e['chapter']=='Background')
    for term in ['CONTINUATION.md','filesystem','file operations','task reward','PPO','A narrow training setting']:
        assert term.lower() not in background.lower(),f'Background must stop at the problem, not the solution: {term}'
    assert STORY[page_for('Core idea')-1]['chapter']=='Method'
    assert STORY[page_for('Learning mechanism')-1]['chapter']=='Method'
    assert STORY[page_for('Prior evidence')-1]['chapter']=='Results & analysis'
    assert page_for('Research problem')<page_for('Contributions')<page_for('Core idea')
    for word in ['CAMG','CAMG-RL','Empirical study']:
        assert word in text_at(page_for('Contributions')),f'Missing contribution {word}'
    assert 'Fully asynchronous PPO' in text_at(page_for('Learning mechanism'))
    for role,key in [('Memory need','fig1_context_only'),('Task demands','fig2_environments'),('Core idea','fig1_camg_teaser'),('Learning mechanism','fig2_camg_framework')]:
        assert [o.name for o in deck.slides[page_for(role)-1].shapes if o.name.startswith('paper-figure:')]==['paper-figure:'+key]
    environment=text_at(page_for('Task demands'))
    for term in ['Shop','Coding','DeepResearch','AutoResearch','purchase history','test progress','intermediate findings','Hypotheses','Later decisions depend on information gathered earlier.']:
        assert term in environment,f'Missing environment memory demand: {term}'
    case=page_for('Case study')
    assert case>max(i+1 for i,e in enumerate(STORY) if e['role']=='Transfer')
    assert [n for n in range(1,len(STORY)+1) if 'Scrapy' in text_at(n)]==[case],'The technical case must appear once, after the results'
    assert 'What should survive a context boundary?' not in visible
    for word in ['CONTINUATION.md','objective: fix response logging','Hidden tests passed','1.00','pytest']:
        assert word in text_at(case),f'Merged case is incomplete: {word}'
    return visible
