#!/usr/bin/env python3
"""Build the 17-slide CAMP story from data/research.json.

Text, charts and case diagrams are native PowerPoint objects. Two original paper
figures are high-resolution pictures in PPTX and original vectors in PDF. No
invented observations or private research paths are embedded. PDF export is a
separate, checked step; see render_slides_pdf.py.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from research_data import load, stats, source_caption
from slide_story import STORY, visible_source, assert_slide_story
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Inches, Pt

ROOT=Path(__file__).resolve().parents[1]
INK,MID,LIGHT,LINE='17232D','586773','667580','DCE3E8'
BLUE,PALE,RED,GRAY,WHITE='2066A4','EDF4FA','B43437','A9B6C1','FFFFFF'
FONT,CODE='Arial','Menlo'


def text(s,content,x,y,w,h,size=18,color=INK,bold=False,align=PP_ALIGN.LEFT,font=FONT):
    box=s.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h))
    tf=box.text_frame;tf.clear();tf.word_wrap=True
    tf.margin_left=tf.margin_right=tf.margin_top=tf.margin_bottom=0
    for i,row in enumerate(str(content).split('\n')):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph();p.text=row or ' ';p.alignment=align
        p.line_spacing=1.12;p.space_after=Pt(0)
        for r in p.runs:
            r.font.name=font;r.font.size=Pt(size);r.font.bold=bold;r.font.color.rgb=RGBColor.from_string(color)
    return box


def rect(s,x,y,w,h,fill=WHITE,stroke=LINE,width=1,oval=False):
    o=s.shapes.add_shape(MSO_SHAPE.OVAL if oval else MSO_SHAPE.RECTANGLE,Inches(x),Inches(y),Inches(w),Inches(h))
    o.fill.solid();o.fill.fore_color.rgb=RGBColor.from_string(fill);o.line.color.rgb=RGBColor.from_string(stroke);o.line.width=Pt(width)
    return o


def line(s,x1,y1,x2,y2,color=LINE,width=1,arrow=False,dash=False):
    o=s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,Inches(x1),Inches(y1),Inches(x2),Inches(y2))
    o.line.color.rgb=RGBColor.from_string(color);o.line.width=Pt(width)
    if dash:o.line.dash_style=MSO_LINE_DASH_STYLE.DASH
    if arrow:
        tail=OxmlElement('a:tailEnd');tail.set('type','triangle');tail.set('w','med');tail.set('len','med');o.line._get_or_add_ln().append(tail)
    return o


def label(s,copy,x,y,w=8.8,color=MID):return text(s,copy,x,y,w,.23,10,color)

def footer(s,copy,num):
    line(s,.45,5.23,9.55,5.23)
    text(s,copy,.45,5.34,8.65,.19,8.5,MID)
    text(s,f'{num:02}',9.15,5.32,.4,.23,10,MID,align=PP_ALIGN.RIGHT)


def takeaway(s,copy):text(s,copy,.5,4.72,9,.42,17,BLUE,bold=True)

def big(s,value,caption,x=7.25,y=1.9,w=2.25,caption_h=1.1):
    text(s,value,x,y,w,.67,36,BLUE,bold=True)
    text(s,caption,x,y+.83,w,caption_h,14,MID)


def filebox(s,title,body,x,y,w,h,size=13):
    rect(s,x,y,w,h,'F6F8FA',LINE)
    rect(s,x,y,.035,h,BLUE,BLUE,0)
    label(s,title,x+.18,y+.13,w-.36,BLUE)
    line(s,x+.15,y+.47,x+w-.15,y+.47)
    text(s,body,x+.2,y+.66,w-.4,h-.8,size,INK,font=CODE)


def hbars(s,rows,x=.55,y=1.45,w=6.3,row_h=.49,maxval=60,label_w=1.8,colors=None,unit=''):
    plot_x=x+label_w;plot_w=w-label_w-.65
    n=len(rows)
    for tick in range(0,int(maxval)+1,20 if maxval>=40 else 10):
        xx=plot_x+tick/maxval*plot_w
        line(s,xx,y-.04,xx,y+n*row_h-.12,'E5E9ED',.6)
        text(s,str(tick),xx-.12,y+n*row_h+.03,.3,.2,9,MID,align=PP_ALIGN.CENTER)
    for i,(name,v) in enumerate(rows):
        yy=y+i*row_h;col=colors[i] if colors else (BLUE if 'CAMG' in name else GRAY)
        text(s,name,x,yy+.025,label_w-.12,row_h-.06,12.5,INK,bold=col==BLUE)
        if v>0:rect(s,plot_x,yy+.035,v/maxval*plot_w,.24,col,col,0)
        text(s,f'{v:.1f}{unit}',plot_x+v/maxval*plot_w+.09,yy+.015,.6,.3,13,col if col==BLUE else MID,bold=col==BLUE)


def grouped(s,groups,series,x=.8,y=1.6,w=6.0,h=2.65,maximum=100,ticks=None,decimals=1,legend=True,label_h=.44):
    """Zero-based native bars; series = [(name, values, color), ...]."""
    ticks=ticks if ticks is not None else [0,maximum/2,maximum]
    for t in ticks:
        yy=y+h-t/maximum*h
        line(s,x,yy,x+w,yy,'E5E9ED',.6)
        text(s,f'{t:g}',x-.46,yy-.09,.33,.2,9,MID,align=PP_ALIGN.RIGHT)
    cell=w/len(groups);barw=min(.38,cell*.23)
    for i,g in enumerate(groups):
        center=x+cell*(i+.5)
        text(s,g,center-cell/2,y+h+.12,cell,label_h,12,INK,align=PP_ALIGN.CENTER)
        for j,(_,vs,col) in enumerate(series):
            v=vs[i];xx=center+(j-(len(series)-1)/2)*(barw+.09)-barw/2;hh=v/maximum*h
            if hh>0:rect(s,xx,y+h-hh,barw,hh,col,col,0)
            text(s,f'{v:.{decimals}f}',xx-.16,y+h-hh-.31,barw+.32,.27,12,col if col==BLUE else MID,bold=col==BLUE,align=PP_ALIGN.CENTER)
    pos=x
    for name,_,col in (series if legend else []):
        rect(s,pos,y-.56,.13,.13,col,col,0);text(s,name,pos+.22,y-.61,2.8,.3,12,MID);pos+=3.05


def paper_figure(s,key,x,y,w,root=ROOT):
    assets=json.loads((root/'slides/figure-assets.json').read_text());a=assets[key]
    for kind in ('pdf','png'):
        path=root/a[kind]
        assert hashlib.sha256(path.read_bytes()).hexdigest()==a[kind+'_sha256'],f'Figure drift: {key} {kind}'
    h=w*a['height_pt']/a['width_pt']
    pic=s.shapes.add_picture(str(root/a['png']),Inches(x),Inches(y),width=Inches(w),height=Inches(h))
    pic.name='paper-figure:'+key
    return pic


def chapter_trail(s,chapter,phase=None):
    for i,(name,x,w) in enumerate([('Background',.5,1.35),('Environments',2.1,1.65),('Method',4.04,1.12),('Results & analysis',5.46,2.2)]):
        active=name==chapter
        text(s,f'{i+1:02}  {name}',x,.79,w,.18,8.5,BLUE if active else LIGHT,bold=active)
        if active:line(s,x,.98,x+w-.08,.98,BLUE,1.3)
    if phase:text(s,phase,7.65,.79,1.85,.18,8.5,BLUE,align=PP_ALIGN.RIGHT)


def build(out,root=ROOT):
    raw=(root/'data/research.json').read_bytes();d=load(root);k=stats(d);sha=hashlib.sha256(raw).hexdigest()
    prs=Presentation();prs.slide_width=Inches(10);prs.slide_height=Inches(5.625)
    prs.core_properties.title=d['project']+': '+d['subtitle'];prs.core_properties.author=', '.join(d['authors'])
    prs.core_properties.subject='CAMP · motivation, contributions, environments, method and results'
    prs.core_properties.keywords='CAMG, CAMG-RL, reinforcement learning, file memory'
    prs.core_properties.comments='Shared research data SHA256: '+sha
    outline=[]
    def slide(heading,source,notes):
        s=prs.slides.add_slide(prs.slide_layouts[6]);num=len(prs.slides)
        text(s,heading,.42,.18,8.65,.57,23,INK,bold=False)
        text(s,'JD.com',8.96,.23,.68,.25,11,RED,bold=True,align=PP_ALIGN.RIGHT)
        footer(s,visible_source(num),num)
        s.notes_slide.notes_text_frame.text=notes+'\n\nSource: '+source+'\nData SHA256: '+sha
        outline.append((num,heading,source,notes))
        return s

    # Opening: complete identity, not an acronym-only poster.
    s=slide('','CAMP V1 · 14 November 2026 · arXiv:2609.34422',
       'The thesis is that ordinary file operations offer a familiar starting point, and task reward teaches a shared policy to use those files as useful memory. This is CAMP V1: four environments and reinforcement learning. Result provenance is retained in the notes and shared data; the spoken story is motivation, contributions, environments, learning and outcomes.')
    label(s,'REINFORCEMENT LEARNING FOR LONG-HORIZON AGENTS',.5,.55,8.7,BLUE)
    text(s,'Coding Agent Memory\nPost-training',.5,1.02,7.0,1.28,34,bold=True)
    text(s,d['subtitle'],.52,2.42,7.0,1.0,18,MID)
    text(s,'Familiar file operations → learned, useful memory',.52,3.62,8.9,.47,21,BLUE,bold=True)
    text(s,' · '.join(d['authors']),.52,4.2,8.9,.58,10.5,MID)
    text(s,d['affiliation'],.52,4.82,2,.22,11,RED,bold=True)
    for i,(t,st) in enumerate([('Files','pre-trained interface'),('RL','native task reward'),('Memory','persistent state')]):
        y=1.1+i*.79;rect(s,8.05,y,1.42,.56,PALE if i==2 else WHITE,BLUE if i==2 else LINE)
        text(s,t,8.12,y+.1,1.28,.3,17,BLUE,bold=i==2,align=PP_ALIGN.CENTER)
        if i<2:line(s,8.76,y+.57,8.76,y+.77,BLUE,1,True)
    b=text(s,'Project · code · slides',.52,4.97,4,.23,10,BLUE);b.text_frame.paragraphs[0].runs[0].hyperlink.address=d['project_url']


    # Motivate with the real sequence, no invented counterfactual.
    s=slide('What should survive a context boundary?','Published · Figure 5 / Appendix A.4.3 · recorded training trajectory',
       'Start with the real Scrapy episode. The agent has already edited scheduler.py. At round 18 it writes a continuation record. At round 19, after context replacement, it reads that record. The excerpts are shortened. Do not imply a measured failure of the same task without memory; that counterfactual was not run.')
    text(s,'Task: fix response logging in Scrapy',.5,1.12,9,.42,21)
    filebox(s,'ROUND 18 / SAVE THE STATE',d['case']['note'],.5,1.65,4.15,2.65,13)
    line(s,5.04,1.62,5.04,4.32,GRAY,1,dash=True)
    text(s,'context replaced',4.23,4.37,1.65,.22,9,MID,align=PP_ALIGN.CENTER)
    filebox(s,'ROUND 19 / PICK UP THE WORK',d['case']['commands'][0]+'\n\n# resume the next checks',5.45,1.65,4.05,2.65,11.3)
    takeaway(s,'Preserve the diagnosis, the evidence, and the next action.')


    # Roadmap: four chapters, phrased as questions the talk will answer.
    s=slide('The story in four questions','Talk roadmap',
       'Keep this to about twenty seconds. Background explains why this work is needed, not just why memory matters. Environments explain what makes the task suite demand memory. Method explains how ordinary file operations learn from task reward. Results answer effectiveness, mechanism and transfer. Return to the Scrapy episode before closing.')
    rows=[('01','Background','Why CAMP?','Need → gap → familiar file operations'),
          ('02','Environments','What must the agent remember?','Four domains, one persistent workspace'),
          ('03','Method','How does memory become a learned skill?','Task reward + fully asynchronous PPO'),
          ('04','Results & analysis','Does it help, why, and does it transfer?','Effectiveness → mechanism → transfer')]
    for i,(n,name,q,detail) in enumerate(rows):
        y=1.2+i*.84
        text(s,n,.55,y,.55,.37,21,BLUE,bold=True)
        text(s,name,1.35,y,2.4,.35,17.5,bold=True)
        text(s,q,3.9,y,5.6,.37,18)
        text(s,detail,3.9,y+.4,5.6,.28,12.5,MID)
        if i<3:line(s,1.35,y+.69,9.5,y+.69)
    takeaway(s,'From a context-boundary problem to reusable memory behavior.')


    # Motivation: explain the specific research gap, not only context length.
    s=slide('Why learn memory through familiar file operations?','Introduction · motivation and research question',
       'Long tasks lose useful working state at context boundaries. The paper identifies two gaps in prior learned-memory work: it often introduces specialized memory tools and trains in domain-specific, relatively short-horizon settings. This is not a claim that all prior work has those limitations. CAMP asks whether task-reward RL can build on familiar file operations to learn memory across diverse long-horizon tasks. Coding agent describes the form of memory operations, not a restriction to programming tasks.')
    label(s,'STARTING POINT IN PRIOR LEARNED-MEMORY WORK',.55,1.18,8.8)
    for i,(title,detail) in enumerate([
        ('A new memory-tool interface','The agent must learn how to store, retrieve and revise through dedicated tools.'),
        ('A narrow training setting','Memory learned in one domain or short horizon may not carry over to longer tasks.')]):
        x=.55+i*4.65
        line(s,x,1.65,x+4.2,1.65,INK,1.4)
        text(s,title,x,1.88,4.2,.44,21,bold=True)
        text(s,detail,x,2.5,4.2,.98,17,MID)
    label(s,'CAMP’S QUESTION',.55,3.68,8.8,BLUE)
    text(s,'Can task reward turn familiar file operations\ninto a reusable long-horizon memory skill?',.55,4.06,8.9,.87,25,BLUE,bold=True)


    # Interface prior.
    s=slide('The file interface is familiar before RL','Published · Figure 3a · frozen Qwen3.5-4B · rounded point estimates',
       'Lower negative log-likelihood means these valid action tokens are more likely under the frozen model. The strongest contrast here is retrieval. This is evidence of interface familiarity, not proof of which pre-training corpus caused it. No uncertainty bars have been reconstructed.')
    label(s,'NEGATIVE LOG-LIKELIHOOD · NATS PER ACTION TOKEN · LOWER IS BETTER',.55,.99)
    r=d['prior']['rows'];grouped(s,[x[0] for x in r],[('File operations',[x[1] for x in r],BLUE),('Dedicated tools',[x[2] for x in r],GRAY)],y=1.83,h=2.35,maximum=1.5,ticks=[0,.5,1,1.5],decimals=2)
    big(s,'0.08','Retrieval NLL with files\nvs. 0.47 with dedicated tools',y=2.05)
    takeaway(s,'Build on an interface the model already knows.')


    # Paper Figure 1 keeps both rows of the conceptual comparison.
    s=slide('Use files to carry working state beyond the context','Figure 1 · conceptual illustration',
       'Read the original paper figure from top to bottom. The top row illustrates how relying on active context can lead to repeated work. The bottom row shows ordinary file writes and reads preserving working state. This figure is a conceptual explanation, not a measured matched failure/success pair. It retains both rows and every original label. Files are available throughout the episode, not only at reset.')
    paper_figure(s,'fig1_camg_teaser',.5,1.08,6.05,root)
    for i,(verb,detail) in enumerate([('Write','Plans, evidence,\nintermediate results'),('Keep','Files survive\ncontext replacement'),('Read','Recover state and\ncontinue the task')]):
        y=1.28+i*1.08
        text(s,verb,6.95,y,2.5,.4,22,BLUE,bold=True)
        text(s,detail,6.95,y+.45,2.5,.65,15,MID)
    takeaway(s,'A familiar interface gives RL somewhere useful to start.')


    # Explicit contribution summary, separate from the talk directory.
    s=slide('Three contributions to learning reusable memory','Introduction · three contributions',
       'This is the actual three-part contribution structure of the paper. CAMG is the environment suite; CAMG-RL is the learning method; the empirical study establishes useful and reusable memory behavior. Fully asynchronous PPO is the implementation, not a claim to a new optimizer. This page is a twenty-to-thirty-second preview; the next pages explain each contribution.')
    items=[('01','CAMG','A long-horizon environment suite','Four domains with native tools, shell access and persistent files.'),
           ('02','CAMG-RL','Learning memory from task reward','One policy learns task actions and ordinary file-memory operations.'),
           ('03','Empirical study','Useful memory that can be reused','Stronger task execution, content-sensitive behavior and transfer.')]
    for i,(n,name,title,detail) in enumerate(items):
        y=1.25+i*1.10
        text(s,n,.55,y,.6,.4,21,BLUE,bold=True)
        text(s,name,1.4,y,2.4,.4,22,BLUE,bold=True)
        text(s,title,4.0,y,5.5,.42,20,bold=True)
        text(s,detail,4.0,y+.45,5.5,.52,14.5,MID)
        if i<2:line(s,1.4,y+1.01,9.5,y+1.01)
    takeaway(s,'Environment suite → learning method → reusable behavior.')


    # Environment identity.
    s=slide('One shared policy, four kinds of work','CAMG environments · V1 suite · four domains',
       'CAMG is the environment suite, CAMG-RL is the learning method, and fully asynchronous PPO is its system implementation. Native task semantics and grading remain with the environments. The final policy is shared, not four separately deployed environment policies. Do not substitute CAMP-II’s General/Visual domains.')
    domains=[('Shop','WebShop','Six linked sessions:\nretain preferences\nand purchase history'),('Coding','SWE-smith','Repo repair:\nretain diagnosis,\npatches and test status'),('DeepResearch','LiteResearcher','Multi-step research:\nretain sources and\nintermediate findings'),('AutoResearch','OpenMLE packages','ML experiments:\nretain hypotheses,\ntrials and results')]
    for i,(name,sub,mem) in enumerate(domains):
        x=.5+i*2.28;line(s,x,1.35,x+2.05,1.35,INK,1.4);label(s,f'0{i+1}',x,1.51,2)
        text(s,name,x,1.92,2.08,.4,19,bold=True);label(s,sub,x,2.39,2.08,BLUE);text(s,mem,x,2.91,2.08,.95,14,MID)
    rect(s,1.55,4.02,6.9,.46,PALE,PALE,0);text(s,'Shared policy  +  episode-persistent workspace',1.7,4.1,6.6,.3,17,BLUE,bold=True,align=PP_ALIGN.CENTER)
    takeaway(s,'Learn a memory behavior across heterogeneous tasks.')


    # Paper Figure 2: the actual system picture, not generic workflow boxes.
    s=slide('Task reward trains both acting and remembering','Figure 2 · CAMG-RL · fully asynchronous PPO',
       'Start at the shared CAMG-RL policy, follow ordinary task/file actions into the four environments, then trace task reward through the episode queue and PPO learner back to the weights. Rollout and learning proceed concurrently. A shell action may combine task and file operations. The environment owns context-replacement timing; the policy writes a bounded continuation file before reset, gets its path after reset, and reads it normally. Reset is not a policy action. No separate memory-writing reward is added. Free-form reasoning is permitted.')
    paper_figure(s,'fig2_camg_framework',.5,1.08,6.0,root)
    for i,(title,body) in enumerate([
        ('Shared task policy','Task and file actions in\none trajectory.'),
        ('Task reward','Learn what to retain\nand reuse.'),
        ('Fully asynchronous PPO','Rollout and learning\nproceed concurrently.')]):
        y=1.26+i*1.08
        text(s,title,6.9,y,2.6,.53,17,BLUE,bold=True)
        text(s,body,6.9,y+.58,2.6,.62,14,MID)
    text(s,'No extra reward for\nwriting a memory file.',6.9,4.58,2.6,.54,14,BLUE,bold=True)


    # Main result.
    s=slide(f"CAMG-RL reaches {k['MAIN_AVG']}% average task success",source_caption(d,'main',slide=True)+' · 4 × 128 held-out tasks · equal-weight environment average',
       'All six original comparisons are visible. The same Qwen3.5-4B backbone reaches 54.4, compared with CompactionRL 48.0; paired 95% CI for the 6.4-point gap is 3.3 to 9.5. Shop is saturated and slightly favors CompactionRL; the largest improvements are Coding and AutoResearch. DeepResearch’s gap is not statistically significant. Displayed averages are from unrounded paper scores.')
    label(s,'AVERAGE TASK SUCCESS (%)',.55,.99);hbars(s,[(r[0],r[-1]) for r in d['main']['rows']],y=1.5,row_h=.48)
    big(s,f"+{k['MAIN_GAP']} pp",'vs. CompactionRL\non held-out tasks',y=1.9)
    takeaway(s,f"Largest gains: Coding +{k['CODING_GAIN']} pp · AutoResearch +{k['AUTO_GAIN']} pp")


    # Practical long-context reference, not single-factor causal evidence.
    s=slide('Learned file memory beats a 262K-context reference',source_caption(d,'long_context',slide=True),
       d['long_context']['boundary']+' The reference scores 49.2 average and CAMG-RL scores 54.4 with 30,720 active tokens, a 5.2-point advantage. Do not describe this as strict isolation of memory, because compaction and context settings differ. Do not claim a cost advantage without cost measurements.')
    label(s,'AVERAGE SUCCESS (%) · SAME BASE, PPO, REWARDS AND 200 UPDATES',.55,.99,8.8,BLUE)
    hbars(s,[('262K + automatic\ncompaction',d['long_context']['rows'][0][-1]),('CAMG-RL\n30,720 active tokens',d['long_context']['rows'][1][-1])],y=2.03,w=6.3,row_h=.88,label_w=2.45)
    big(s,f"+{k['CONTEXT_GAIN']} pp",'Average task success\nwith 30,720 active tokens',y=1.85)
    text(s,'The context budget and compaction procedure both differ.',.55,4.23,8.8,.24,11,MID)
    takeaway(s,'A larger window alone is not the only route to stronger execution.')


    # Learning signal: distinct memory-action and continuation ablations.
    s=slide('Memory actions need the learning signal',source_caption(d,'ablation',slide=True)+' · average task success (%)',
       d['ablation']['boundary']+' The four rows are distinct interventions. Full training reaches 54.4, no memory-action actor gradients reaches 21.1, restricting to continuation during both training and evaluation gives 41.8, and restricting only at evaluation gives 28.1.')
    label(s,'AVERAGE TASK SUCCESS (%)',.55,.99)
    hbars(s,[(name,row[1]) for name,row in zip(['CAMG-RL','No memory-action\nactor gradients','Continuation only:\ntrain + evaluate','Continuation only:\nevaluate'],d['ablation']['rows'])],y=1.53,w=8.7,row_h=.67,label_w=2.6)
    takeaway(s,'Task reward can train what to save—and how to use it.')


    # Same-state intervention, zero anchored.
    s=slide('The saved content changes what happens next','Published · Appendix D.3 · same-state continuations · eligible tasks only',
       d['intervention']['boundary']+' Negative bars are percentage-point changes relative to intact files. The eligible counts are 128, 29, 60, and 23. Equal-environment mean losses are 14.1 for blank and 11.5 for shuffled memory. This is stronger local evidence than an uncontrolled correlation between writing and success, but not a population-wide treatment effect.')
    label(s,'CHANGE IN SUCCESS FROM INTACT MEMORY (PERCENTAGE POINTS)',.55,.99)
    for j,(lab,col) in enumerate([('Blank',BLUE),('Shuffled',GRAY)]):
        rect(s,1.95+j*2,1.43,.12,.12,col,col,0);text(s,lab,2.15+j*2,1.39,1.7,.27,12,MID)
    left,right,top,bottom=1.95,6.5,1.93,4.32
    for t in [-30,-20,-10,0]:
        x=right+t/32*(right-left);line(s,x,top-.1,x,bottom,LINE,.7);text(s,str(t),x-.18,bottom+.08,.42,.2,10,MID,align=PP_ALIGN.CENTER)
    for i,(name,b,sh,n) in enumerate(d['intervention']['rows']):
        y=top+i*.58;text(s,name,.5,y-.03,1.36,.3,12.5);text(s,f'n = {n}',.5,y+.24,1.36,.2,9,MID)
        for j,(v,col) in enumerate([(b,BLUE),(sh,GRAY)]):
            x=right+v/32*(right-left);rect(s,x,y+j*.23,right-x,.17,col,col,0);text(s,f'{v:.1f}',right+.13,y+j*.23-.03,.55,.23,11,col if col==BLUE else MID)
    big(s,f"−{k['BLANK_DROP']} pp",'Equal-environment mean\nwhen memory is blanked',x=7.35,y=2.05,w=2.1)
    takeaway(s,'Erase or shuffle the memory: success falls in every domain.')


    # Interface transfer with fixed task executor.
    s=slide('The learned memory policy transfers across interfaces',source_caption(d,'transfer',slide=True),
       d['transfer']['boundary']+' The gains are 11.4 points with Claude Code file tools and 6.4 with AgeMem memory tools. Only the memory-writing and reading policy changes. This is not a claim about changing the entire task actor, and no uncertainty or sample size should be invented.')
    label(s,'AVERAGE SUCCESS (%) · FROZEN EXECUTOR · NO FURTHER TRAINING',.55,.99,8.8,BLUE)
    r=d['transfer']['rows'];grouped(s,['Claude Code\nfile tools','AgeMem\nmemory tools'],[('Frozen memory policy',[r[0][-1],r[2][-1]],GRAY),('Trained memory policy',[r[1][-1],r[3][-1]],BLUE)],x=.9,y=1.83,w=5.7,h=2.35,maximum=32,ticks=[0,10,20,30])
    big(s,f"+{k['TRANSFER_FILE_GAIN']} pp",'Claude Code file tools',y=1.75,caption_h=.42);text(s,f"+{k['TRANSFER_TOOL_GAIN']} pp",7.25,3.43,2.25,.6,30,BLUE,bold=True);text(s,'AgeMem memory tools',7.25,4.04,2.25,.35,13,MID)
    takeaway(s,'Keep task execution fixed; change only who manages memory.')


    # External table with editable grouped bars, small and large base scales.
    s=slide('Gains carry over to external benchmarks','Published · Table 3 · benchmark success (%) · no compute-equivalence claim',
       d['external']['boundary']+' Focus on matched base-to-trained gains at each scale: SWE-bench Verified 7.6 to 15.8 for 4B and 14.8 to 27.6 for 9B; MLE-bench Lite 0.0 to 4.5 and 4.5 to 9.1. Larger frozen MoE models remain capability references in the paper; this slide shows only matched base-to-trained comparisons.')
    label(s,'FROZEN BASE VS. CAMG-RL · SAME MODEL SCALE',.55,.99)
    er=d['external']['rows']
    for j,(lab,col) in enumerate([('Frozen base',GRAY),('CAMG-RL',BLUE)]):
        rect(s,.9+j*2.1,1.32,.13,.13,col,col,0);text(s,lab,1.12+j*2.1,1.28,1.8,.3,12,MID)
    grouped(s,['4B','9B'],[('Frozen base',[er[0][1],er[3][1]],GRAY),('CAMG-RL',[er[1][1],er[4][1]],BLUE)],x=.9,y=1.84,w=3.7,h=2.25,maximum=30,ticks=[0,10,20,30],legend=False,label_h=.24)
    grouped(s,['4B','9B'],[('Frozen base',[er[0][2],er[3][2]],GRAY),('CAMG-RL',[er[1][2],er[4][2]],BLUE)],x=5.85,y=1.84,w=3.65,h=2.25,maximum=10,ticks=[0,5,10],legend=False,label_h=.24)
    text(s,'SWE-bench Verified',.85,4.45,3.9,.3,14,INK,bold=True,align=PP_ALIGN.CENTER)
    text(s,'MLE-bench Lite',5.75,4.45,3.9,.3,14,INK,bold=True,align=PP_ALIGN.CENTER)
    takeaway(s,'Improve the trained policy’s own base on both benchmarks.')


    # Resolve the opening story, without making it a causal control.
    s=slide('The remembered state becomes the next action','Published · Figure 5 / Appendix A.4.3 · shortened training-episode excerpts',
       d['case']['boundary']+' Timeline: edit scheduler.py at round 12, write CONTINUATION.md at round 18, reset, read at round 19, later run test_spider.py and pytest tests/test_crawl.py -v, terminal round 30 within a 40-round budget with return 1.00 and hidden tests passed. Test commands are subsequent actions, not all asserted to occur at round 19.')
    steps=[('12','Edit','Add _mqpush'),('18','Write','Preserve the state'),('19','Read','Recover the state'),('30','Finish','Hidden tests passed')]
    for i,(n,t,desc) in enumerate(steps):
        x=.65+i*2.36;rect(s,x,1.42,.48,.48,PALE,BLUE,1,True);text(s,n,x+.02,1.53,.44,.25,13,BLUE,bold=True,align=PP_ALIGN.CENTER)
        if i<3:line(s,x+.52,1.66,x+2.2,1.66,LINE,1,True)
        text(s,t,x,2.06,2.12,.35,21,bold=True);text(s,desc,x,2.54,2.1,.53,13,MID)
    filebox(s,'SUBSEQUENT CHECKS','\n'.join(d['case']['commands'][1:]),.65,3.24,6.22,1.22,13)
    text(s,'1.00',7.6,3.25,1.8,.63,37,BLUE,bold=True);label(s,'TERMINAL RETURN',7.6,4.02,1.8)
    takeaway(s,'The file carries the work forward; the agent still has to do it.')


    # End on the scientific takeaways, not an unasked appendix.
    s=slide('Familiar operations. Learned memory.','CAMP V1 · published paper + labelled November additions · data/research.json',
       'Close with three scoped statements. Familiarity is measured before training. Task reward teaches useful memory behaviors, supported by acquisition, ablation and local content intervention. The benefits extend to external benchmarks and, in November additions, new memory interfaces. Do not claim universal causality or compute savings. The project page links the paper, code and slides. Detailed protocol and source-version boundaries stay in these speaker notes and shared data, not the audience-facing story.')
    for i,(a,b) in enumerate([('Start from a familiar interface.','Use ordinary file operations instead of inventing a new memory language.'),('Train memory through the task.','Preserve and reuse useful state with downstream reward.'),('Learn a behavior that can be reused.','Stronger execution across environments, interfaces and external tasks.')]):
        y=1.23+i*1.05;text(s,f'0{i+1}',.55,y,.55,.38,19,BLUE);text(s,a,1.35,y,8.0,.42,23,bold=True);text(s,b,1.35,y+.52,8.0,.4,14,MID)
    b=text(s,'liruiluo.github.io/agentmemorygym',1.35,4.67,7.8,.38,18,BLUE,bold=True);b.text_frame.paragraphs[0].runs[0].hyperlink.address=d['project_url']

    assert len(prs.slides)==len(STORY)
    for s,entry in zip(prs.slides,STORY):
        if entry['chapter']:chapter_trail(s,entry['chapter'],entry.get('phase'))
    assert_slide_story(prs)
    out.parent.mkdir(parents=True,exist_ok=True);prs.save(out)
    notes='# CAMP · 17-slide research story\n\nUpdated 2026-11-14. Approximately 15 minutes (14.5 minutes of speaking plus transitions). White academic house style. Text, charts and case diagrams are editable; Figures 1 and 2 are faithful paper-figure pictures in PPTX and vector originals in PDF. Results come from `data/research.json`. Source-version boundaries below are speaker preparation, not slide labels.\n\n'
    for (n,t,src,body),entry in zip(outline,STORY):
        notes+=f'## {n:02}. {t or d["project"]}\n\n**Chapter:** {entry["chapter"] or "Opening / roadmap"} · **Role:** {entry["role"]} · **Target:** {entry["seconds"]} seconds\n\n**Source:** {src}\n\n{body}\n\n'
    notes+='## Additional Q&A material (not extra slides)\n\nThe shared data also retains the designated-interface acquisition metric (7.97% to 20.9%), the syntax-constrained frozen-model comparison (Bash 20.3% vs. AgeMem 16.0%), and five-run robustness (CAMG-RL 55.3 ± 2.9 vs. CompactionRL 47.1 ± 3.5, mean ± SD). These are omitted from the main talk to preserve the motivation → method → effectiveness → mechanism → transfer story. Refer to each experiment’s own protocol before using these numbers.\n'
    (out.parent/'speaker-notes.md').write_text(notes)
    outline_md='# CAMP · 17-slide public research talk\n\nUpdated 2026-11-14. English, approximately 15 minutes.\n\nStory: why memory → why CAMP → contributions → task environments → learning method → effectiveness → mechanism → transfer → the case carried to completion.\n\nThe roadmap follows the opening Scrapy case. A lightweight four-chapter trail marks progress; result pages also name the question they answer. There are no full-page chapter dividers, references or appendix tail.\n\n| # | Chapter | Role | Action title | Exhibit |\n|---|---|---|---|---|\n'
    for (n,t,src,body),entry in zip(outline,STORY):
        outline_md+=f'| {n} | {entry["chapter"] or "Opening / roadmap"} | {entry["role"]} | {t or d["project"]} | {entry["exhibit"]} |\n'
    outline_md+='\n## Speaking and source notes\n\nThe contribution overview follows the paper’s actual suite / method / empirical-study structure. Figures 1 and 2 retain their original content; the conceptual comparison is not presented as a measured counterfactual. Results use unchanged source values and essential on-slide comparison conditions. Full provenance and scientific qualifications are in [speaker notes](speaker-notes.md) and [shared data](../data/research.json). Multi-run robustness, chain counts and the syntax-only probe are optional Q&A material, not additional talk pages.\n'
    (out.parent/'outline.md').write_text(outline_md)
    manifest={'slides':len(prs.slides),'data_sha256':sha,'paper_figure_pictures':2,'pdf_figures':'original vectors','updated':d['updated'],'slides_outline':[dict(number=n,title=t or d['project'],provenance=src,**entry) for (n,t,src,_),entry in zip(outline,STORY)]}
    (out.parent/'deck-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'pptx':str(out),'slides':len(prs.slides),'paper_figure_pictures':2,'data_sha256':sha}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--site-root',type=Path,default=ROOT);a=p.parse_args();build(a.out,a.site_root)
