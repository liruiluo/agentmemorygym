"""Audience-facing talk structure; scientific provenance stays in research.json/notes."""
import re
from pptx.util import Inches

QUESTIONS = {
    'Q1': 'Does CAMP improve long-horizon task performance?',
    'Q2': 'What drives CAMP’s gains?',
    'Q3': 'Does the learned memory behavior generalize?',
}


SUBQUESTIONS = {
    'Q2.1': 'Do the gains come from better memory?',
    'Q2.2': 'Do pre-trained file-operation skills help?',
}


def question_label(phase):
    return f"{phase} · {(QUESTIONS | SUBQUESTIONS)[phase]}"


# One audience-facing line identifies the comparison, not a protocol inventory.
EXPERIMENT_DESIGNS = {
    'main': 'Compare six approaches with Qwen3.5-4B on the same held-out tasks.',
    'long_context': 'Same base, PPO, task rewards and 200 updates; context and compaction differ.',
    'prior': 'Score file and dedicated-tool memory actions with frozen Qwen3.5-4B.',
    'ablation': 'Remove memory-action actor gradients (keep rewards/critic), or use only CONTINUATION.md.',
    'intervention': 'Resume from the same post-reset state with intact, blank or shuffled memory.',
    'transfer': 'Keep the task executor fixed; replace only the memory policy, with no further training.',
    'external': 'Compare frozen base and trained policies at the same 4B and 9B model scales.',
}


def entry(chapter,role,exhibit,source,phase=None,experiment=None):
    return dict(chapter=chapter,role=role,exhibit=exhibit,source=source,phase=phase,experiment=experiment)

STORY=[
    entry(None,'Identity','Full title, authors, affiliation and links','CAMP · arXiv:2609.34422'),
    entry(None,'Roadmap','Four chapters and the questions they answer','CAMP · talk roadmap'),
    entry('Background','Memory need','Figure 1 upper row: context lost → repeated work → unfinished task','Figure 1 · context-only row'),
    entry('Background','Research problem','Unused memory tools → lost constraint → failure; prior-mismatch hypothesis → question','Memory use · the research problem'),
    entry(None,'Contributions','Environment suite / learning method / empirical study','CAMP · three contributions'),
    entry('Environments','Task demands','Figure 2 environment panel + what each task family must remember','CAMG · Figure 2 · environment panel'),
    entry('Method','Core idea','Original Figure 1, both contrast rows','Figure 1 · conceptual illustration'),
    entry('Method','Learning mechanism','Original Figure 2 + shared policy/reward/PPO callouts','CAMG-RL · Figure 2 · fully asynchronous PPO'),
    entry('Results & analysis','Effectiveness','Six-method main comparison','Task success · Qwen3.5-4B · 128 held-out tasks per environment','Q1','main'),
    entry('Results & analysis','Effectiveness','262K-context practical reference','Same base, PPO, rewards and updates; context and compaction differ','Q1','long_context'),
    entry('Results & analysis','Mechanism','Memory-action gradient and continuation ablations','Ablations · Figure 4 · average task success','Q2.1','ablation'),
    entry('Results & analysis','Mechanism','Blank/shuffled memory from the same state','Memory-content intervention · same-state continuations · eligible tasks','Q2.1','intervention'),
    entry('Results & analysis','Prior evidence','Frozen-model file vs. dedicated-tool likelihood','Interface familiarity · Figure 3a · frozen Qwen3.5-4B','Q2.2','prior'),
    entry('Results & analysis','Case study','Complete original Figure 5: error, repair, memory write and readback, success','Scrapy case · Figure 5 · recorded training episode','Q2'),
    entry('Results & analysis','Transfer','New memory interfaces, fixed task executor','Frozen task executor · memory policy changed · no further training','Q3','transfer'),
    entry('Results & analysis','Transfer','Matched base vs. trained external results','SWE-bench Verified / MLE-bench Lite · matched model scales','Q3','external'),
    entry(None,'Conclusion','Three takeaways and project link','CAMP · paper, code and slides'),
]

# Fourteen and a half minutes of speaking plus transitions.
for row,seconds in zip(STORY,[35,20,45,80,25,50,60,75,60,40,50,55,50,80,55,50,40]):
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
    assert max(i+1 for i,e in enumerate(STORY) if e['role']=='Mechanism')<case<min(i+1 for i,e in enumerate(STORY) if e['role']=='Transfer'),'Case study closes Q2 before transfer'
    assert [n for n in range(1,len(STORY)+1) if 'Scrapy' in text_at(n)]==[case],'The technical case must appear once, at the end of Q2'
    case_pictures=[o for o in deck.slides[case-1].shapes if o.name.startswith('paper-figure:')]
    assert len(case_pictures)==1 and case_pictures[0].name=='paper-figure:fig5_coding_case','Case must use the complete original Figure 5'
    pic=case_pictures[0]
    assert not any([pic.crop_left,pic.crop_top,pic.crop_right,pic.crop_bottom]),'Do not crop the case figure panels'
    assert pic.width>=Inches(9) and pic.top>=Inches(.99) and pic.top+pic.height<Inches(5.23),'Original case figure must fill the body without colliding with header/footer'
    assert [e['phase'].split('.')[0] for e in STORY if e['chapter']=='Results & analysis']==['Q1']*2+['Q2']*4+['Q3']*2,'Experimental questions must form three contiguous groups'
    assert [e['phase'] for e in STORY[10:14]]==['Q2.1','Q2.1','Q2.2','Q2'],'Memory evidence, prior evidence and whole-Q2 case must remain distinct'
    assert [e['experiment'] for e in STORY[10:14]]==['ablation','intervention','prior',None],'Q2 subquestions must match the evidence they explain'
    for i,e in enumerate(STORY):
        design=[o for o in deck.slides[i].shapes if o.name.startswith('experiment-design:')]
        if e['experiment']:
            assert len(design)==1 and design[0].name=='experiment-design:'+e['experiment'],'Missing experiment design line'
            box=design[0]
            assert box.text==EXPERIMENT_DESIGNS[e['experiment']],'Experiment design text drift'
            title=deck.slides[i].shapes[0]
            assert title.top+title.height<box.top and box.top+box.height<=Inches(1.31),'Design must be visible between title and exhibit'
            runs=[r for p in box.text_frame.paragraphs for r in p.runs]
            assert runs and all(r.font.size is not None and r.font.size.pt>=14 for r in runs),'Experiment design must be readable'
        else:
            assert not design,'Do not impose experimental design on a case or non-experimental page'
        labels=[o for o in deck.slides[i].shapes if o.name.startswith('result-question:')]
        if e['phase']:
            assert len(labels)==1 and labels[0].name=='result-question:'+e['phase'],'Missing or wrong experimental question label'
            assert labels[0].text==question_label(e['phase']),'Experimental question text drift'
        else:
            assert not labels,'Question labels belong to experimental slides only'
        navigation=[o for o in deck.slides[i].shapes if o.name.startswith('chapter-navigation:')]
        if e['chapter']:
            title=deck.slides[i].shapes[0]
            assert len(navigation)==(1 if e['phase'] else 4),'Missing chapter navigation'
            for marker in navigation+labels:
                assert marker.top+marker.height<title.top,'Navigation must precede the slide title'
                marker_size=marker.text_frame.paragraphs[0].runs[0].font.size
                title_size=title.text_frame.paragraphs[0].runs[0].font.size
                assert marker_size is not None and title_size is not None and marker_size<title_size,'Title must dominate navigation'
            assert title.top+title.height<=Inches(.99),'Header must not displace the slide body'
        else:
            assert not navigation,'Do not add navigation to non-chapter pages'
    assert STORY[-1]['role']=='Conclusion' and deck.slides[-1].shapes[0].text=='Takeaways','Final slide must be titled Takeaways'
    assert 'What should survive a context boundary?' not in visible
    return visible
