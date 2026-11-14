#!/usr/bin/env python3
"""Build a dependency-free, progressively enhanced research page from shared data."""
import argparse
import hashlib
import json
import re
from html import escape as e
from pathlib import Path
from research_data import load, stats, source_caption

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
    c=d['case']; main=d['main']; transfer=d['transfer']['rows']; con=d['constrained']['rows']
    values={
      'DATA_HASH':hashlib.sha256(raw).hexdigest(), 'TITLE':e(d['project']),'SUBTITLE':e(d['subtitle']),
      'AUTHORS':' · '.join(e(a) for a in d['authors']),
      'MAIN_CHART':bars([(r[0],r[-1]) for r in main['rows']]),
      'MAIN_TABLE':table(main,'Published main results · task success (%)'),
      'PRIOR_CHART':pairs([r[0] for r in d['prior']['rows']], [('File operations',[r[1] for r in d['prior']['rows']],'blue'),('Dedicated tools',[r[2] for r in d['prior']['rows']],'gray')],1.5,2),
      'CONSTRAINED_CHART':pairs(['Unconstrained','Constrained decoding'],[('Bash',[con[0][-1],con[1][-1]],'blue'),('AgeMem',[con[2][-1],con[3][-1]],'gray')],25),
      'CONSTRAINED_TABLE':table(d['constrained'],'Frozen-base interface comparison · task success (%)'),
      'TRANSFER_CHART':pairs(['Claude Code file tools','AgeMem memory tools'],[('Frozen memory policy',[transfer[0][-1],transfer[2][-1]],'gray'),('Trained memory policy',[transfer[1][-1],transfer[3][-1]],'blue')],30),
      'TRANSFER_TABLE':table(d['transfer'],'Fixed-executor interface transfer · task success (%)'),
      'CONTEXT_CHART':bars([(r[0],r[-1]) for r in d['long_context']['rows']]),
      'CONTEXT_TABLE':table(d['long_context'],'Long-context reference · task success (%)'),
      'ABLATION_CHART':bars(d['ablation']['rows']),
      'INTERVENTION_TABLE':table(d['intervention'],'Same-state memory interventions · change in success (pp)'),
      'EXTERNAL_TABLE':table(d['external'],'External benchmark transfer · success (%)'),
      'FAMILY_TABLE':table(d['family'],'Model-family replication · task success (%)'),
      'CASE_NOTE':e(c['note']), 'CASE_COMMANDS':e('\n'.join(c['commands'])),
      'ROBUSTNESS':'', 'INTERVENTION_CHART':'', 'FAMILY_CHART':bars([(r[0],r[-1]) for r in d['family']['rows']],60,colors=['gray','blue']),
      'ACQUISITION_START':f(d['acquisition']['camg'][0]), 'ACQUISITION_END':f(d['acquisition']['camg'][1]),
    }
    # The axis spans zero to sixty; error whiskers represent supplied SD, never CI.
    svg=['<svg class="stability-plot" viewBox="0 0 640 190" role="img" aria-labelledby="stability-title stability-desc"><title id="stability-title">Average success across five training runs</title><desc id="stability-desc">CompactionRL 47.1 plus or minus 3.5 standard deviation. CAMG-RL 55.3 plus or minus 2.9. Scale zero to sixty percent.</desc>']
    for tick in [0,20,40,60]:
        x=154+tick/60*435
        svg.append(f'<line x1="{x}" x2="{x}" y1="30" y2="135" stroke="#e2e5e9"/><text x="{x}" y="169" text-anchor="middle" fill="#56616c" font-size="15">{tick}</text>')
    for i,(name,mean,sd) in enumerate(d['robustness']['rows']):
        y=52+i*66; x=154+mean/60*435; lo=x-sd/60*435; hi=x+sd/60*435; color='#2066a4' if i else '#6b7681'
        svg.append(f'<text x="0" y="{y+5}" font-size="17" fill="#202931">{e(name)}</text><line x1="{lo}" x2="{hi}" y1="{y}" y2="{y}" stroke="{color}" stroke-width="3"/><line x1="{lo}" x2="{lo}" y1="{y-7}" y2="{y+7}" stroke="{color}"/><line x1="{hi}" x2="{hi}" y1="{y-7}" y2="{y+7}" stroke="{color}"/><circle cx="{x}" cy="{y}" r="6" fill="{color}"/><text x="{x}" y="{y-16}" text-anchor="middle" font-size="17" fill="{color}">{mean} ± {sd}</text>')
    compact='<dl class="compact-stats">'+''.join(f'<div><dt>{e(name)}</dt><dd>{mean:.1f} ± {sd:.1f}</dd></div>' for name,mean,sd in d['robustness']['rows'])+'</dl>'
    values['ROBUSTNESS']=''.join(svg)+'</svg>'+compact
    out='<div class="delta-chart"><div class="legend"><span><i class="blue-dot"></i>Blank</span><span><i class="gray-dot"></i>Shuffled</span></div>'
    for name,blank,shuffled,n in d['intervention']['rows']:
        out+=f'<div class="delta-group"><h4>{name}<small>n = {n}</small></h4>'
        for v,color in [(blank,'blue'),(shuffled,'gray')]:
            out+=f'<div class="delta-row {color}"><div class="delta-track" aria-hidden="true"><span style="width:{abs(v)/32*100:.3f}%"></span></div><strong>{v:.1f}</strong></div>'
        out+='</div>'
    values['INTERVENTION_CHART']=out+'<p class="axis-label">← Lower success &nbsp; · &nbsp; change from intact memory (pp); right edge = 0</p></div>'
    for key in ['main','prior','constrained','intervention','ablation','transfer','long_context','robustness','family','external']:
        css='source-tag new' if d[key]['source']=='additional' else 'source-tag'
        values['SOURCE_'+key.upper()]=f'<p class="{css}">{e(source_caption(d,key))}</p>'
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
