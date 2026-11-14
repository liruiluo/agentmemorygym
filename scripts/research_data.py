"""Shared result access and validation for the website and talk."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]

def load(root=ROOT):
    data=json.loads((root/'data/research.json').read_text())
    validate(data)
    return data

def validate(d):
    assert d['schema_version']==1
    assert len(d['domains'])==4 and d['domains']==['Shop','Coding','DeepResearch','AutoResearch']
    assert len(d['main']['rows'])==6
    for key in ['main','constrained','transfer','long_context','family','external','prior','intervention','coding_memory']:
        section=d[key]
        assert all(len(r)==len(section['columns']) for r in section['rows']),key
        assert section['source'] in d['sources'],key
    assert d['sources']['additional']['independently_run_verified'] is False
    assert d['robustness']['runs_per_method']==5
    assert all(0<=v<=100 for row in d['main']['rows'] for v in row[1:])
    assert all(v<=0 for row in d['intervention']['rows'] for v in row[1:3])
    assert 'quality_rows' not in d['transfer']

def stats(d):
    main={r[0]:r[1:] for r in d['main']['rows']};camg=main['CAMG-RL'];comp=main['CompactionRL']
    tr=d['transfer']['rows'];cd=d['constrained']['rows'];lc=d['long_context']['rows'];rb=d['robustness']['rows'];fa=d['family']['rows']
    return {k:f'{v:.1f}' for k,v in {
        'MAIN_AVG':camg[-1],'MAIN_GAP':camg[-1]-comp[-1],
        'CI_LO':d['main']['gap_paired_ci95_pp'][0],'CI_HI':d['main']['gap_paired_ci95_pp'][1],
        'CODING_GAIN':camg[1]-comp[1],'AUTO_GAIN':camg[3]-comp[3],
        'CD_GAP':cd[1][-1]-cd[3][-1],
        'TRANSFER_FILE_GAIN':tr[1][-1]-tr[0][-1],'TRANSFER_TOOL_GAIN':tr[3][-1]-tr[2][-1],
        'CONTEXT_GAIN':lc[1][-1]-lc[0][-1],
        'ROBUST_GAIN':rb[1][1]-rb[0][1],
        'FAMILY_BASE':fa[0][-1],'FAMILY_TRAINED':fa[1][-1],
        'BLANK_DROP':-d['intervention']['equal_environment_mean'][0],
        'SHUFFLED_DROP':-d['intervention']['equal_environment_mean'][1]
    }.items()}

def source_caption(d,key,slide=False):
    section=d[key];ref=section['reference'].split(' (')[0]
    if section['source']=='paper':return 'Published · '+ref
    if slide:return 'ADDITIONAL · November 2026 · '+ref+' · author-reported'
    return 'Additional experiments · Nov 2026'
