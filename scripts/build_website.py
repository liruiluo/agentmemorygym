#!/usr/bin/env python3
"""Build a dependency-free, progressively enhanced research page from shared data."""
import argparse
import hashlib
import json
import re
from html import escape as e
from pathlib import Path
from research_data import load, stats

ROOT = Path(__file__).resolve().parents[1]

def f(v):
    return f'{v:.1f}' if isinstance(v,(int,float)) else e(v)

def table(section, caption):
    return '<p class="table-hint">Swipe or scroll horizontally to see all columns →</p><div class="table-scroll" tabindex="0" role="region" aria-label="'+e(caption)+'"><table><caption>'+e(caption)+'</caption><thead><tr>'+''.join('<th scope="col">'+e(x)+'</th>' for x in section['columns'])+'</tr></thead><tbody>'+''.join(('<tr class="trained">' if any('CAMG-RL' in str(v) for v in row[:2]) else '<tr>')+''.join(('<th scope="row">' if i==0 else '<td>')+f(v)+('</th>' if i==0 else '</td>') for i,v in enumerate(row))+'</tr>' for row in section['rows'])+'</tbody></table></div>'

def bars(rows, maximum=60, unit='%', colors=None):
    out='<div class="bar-chart" role="list">'
    for i,(name,val) in enumerate(rows):
        color=(colors[i] if colors else ('blue' if 'CAMG' in name else 'gray'))
        out+=f'<div class="bar-row {color}" role="listitem"><span class="bar-name">{e(name)}</span><div class="bar-track" aria-hidden="true"><span style="width:{val/maximum*100:.4f}%"></span></div><strong>{val:.1f}{unit}</strong></div>'
    return out+'</div>'

def pairs(labels,series,maximum,decimal=1):
    out='<div class="pair-chart">'
    for i,label in enumerate(labels):
        out+=f'<div class="pair-group"><h4>{e(label)}</h4>'
        for name,values,color in series:
            v=values[i]
            out+=f'<div class="pair-row {color}"><span class="pair-name">{e(name)}</span><div class="bar-track" aria-hidden="true"><span style="width:{v/maximum*100:.4f}%"></span></div><strong>{v:.{decimal}f}</strong></div>'
        out+='</div>'
    return out+'</div>'

def build():
    raw=(ROOT/'data/research.json').read_bytes(); d=load(ROOT)
    c=d['case']; main=d['main']; transfer=d['transfer']['rows']
    external={row[0]:row[1:] for row in d['external']['rows']}
    values={
      'DATA_HASH':hashlib.sha256(raw).hexdigest(), 'TITLE':e(d['project']),'SUBTITLE':e(d['subtitle']),
      'AUTHORS':' · '.join(e(a) for a in d['authors']),
      'MAIN_CHART':bars([(r[0],r[-1]) for r in main['rows']]),
      'MAIN_TABLE':table(main,'Task success (%)'),
      'PRIOR_CHART':pairs([r[0] for r in d['prior']['rows']], [('File operations',[r[1] for r in d['prior']['rows']],'blue'),('Dedicated tools',[r[2] for r in d['prior']['rows']],'gray')],1.5,2),
      'TRANSFER_CHART':pairs(['Claude Code file tools','AgeMem memory tools'],[('Before training',[transfer[0][-1],transfer[2][-1]],'gray'),('Learned memory',[transfer[1][-1],transfer[3][-1]],'blue')],30),
      'CONTEXT_CHART':bars([(r[0],r[-1]) for r in d['long_context']['rows']]),
      'CASE_NOTE':e(c['note']), 'CASE_COMMANDS':e('\n'.join(c['commands'])),
    }
    for i,key in enumerate(['EXTERNAL_SWE_CHART','EXTERNAL_MLE_CHART']):
        values[key]=pairs(['4B','9B'],[('Base model',[external['Qwen3.5-4B'][i],external['Qwen3.5-9B'][i]],'gray'),('CAMG-RL',[external['CAMG-RL-4B'][i],external['CAMG-RL-9B'][i]],'blue')],30)
    out='<div class="delta-chart"><div class="legend"><span><i class="blue-dot"></i>Empty file</span><span><i class="gray-dot"></i>Shuffled content</span></div>'
    for name,blank,shuffled,_ in d['intervention']['rows']:
        out+=f'<div class="delta-group"><h4>{e(name)}</h4>'
        for v,color in [(blank,'blue'),(shuffled,'gray')]:
            out+=f'<div class="delta-row {color}"><div class="delta-track" aria-hidden="true"><span style="width:{abs(v)/32*100:.3f}%"></span></div><strong>{v:.1f}</strong></div>'
        out+='</div>'
    values['INTERVENTION_CHART']=out+'<p class="axis-label">← Lower success &nbsp; · &nbsp; right edge = no change</p></div>'
    values.update(stats(d))
    template=(ROOT/'scripts/site.template.html').read_text()
    for key,value in values.items():template=template.replace('{{'+key+'}}',str(value))
    unknown=re.findall(r'\{\{.*?\}\}',template)
    if unknown:raise ValueError(unknown)
    return template

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');args=ap.parse_args()
    content=build(); target=ROOT/'index.html'
    if args.check:
        if not target.exists() or target.read_text()!=content:raise SystemExit('index.html is stale; run scripts/build_website.py')
        print('Generated website is current.')
    else:
        target.write_text(content);print('Built index.html')
