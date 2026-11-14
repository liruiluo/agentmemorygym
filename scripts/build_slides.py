#!/usr/bin/env python3
"""Build the 16-slide CAMP talk from data/research.json.

All charts, diagrams and text are native PowerPoint objects. No chart screenshots,
invented observations or private research paths are embedded. PDF export is a
separate, checked step; see render_slides_pdf.py.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from research_data import load, stats, source_caption
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


def build(out,root=ROOT):
    raw=(root/'data/research.json').read_bytes();d=load(root);k=stats(d);sha=hashlib.sha256(raw).hexdigest()
    prs=Presentation();prs.slide_width=Inches(10);prs.slide_height=Inches(5.625)
    prs.core_properties.title=d['project']+': '+d['subtitle'];prs.core_properties.author=', '.join(d['authors'])
    prs.core_properties.subject='CAMP V1 · published results and November 2026 additions'
    prs.core_properties.keywords='CAMG, CAMG-RL, reinforcement learning, file memory'
    prs.core_properties.comments='Shared research data SHA256: '+sha
    outline=[]
    def slide(heading,source,notes):
        s=prs.slides.add_slide(prs.slide_layouts[6]);num=len(prs.slides)
        text(s,heading,.42,.18,8.65,.65,24,INK,bold=False)
        text(s,'JD.com',8.96,.23,.68,.25,11,RED,bold=True,align=PP_ALIGN.RIGHT)
        footer(s,source,num)
        s.notes_slide.notes_text_frame.text=notes+'\n\nSource: '+source+'\nData SHA256: '+sha
        outline.append((num,heading,source,notes))
        return s

    # 1. Opening: complete identity, not an acronym-only poster.
    s=slide('','CAMP V1 · 14 November 2026 · arXiv:2609.34422',
       'The thesis is that ordinary file operations offer a familiar starting point, and task reward teaches a shared policy to use those files as useful memory. This is CAMP V1: four environments and reinforcement learning. Blue-labelled November additions are author-reported revised-manuscript results, not already part of the September arXiv release.')
    label(s,'REINFORCEMENT LEARNING FOR LONG-HORIZON AGENTS',.5,.55,8.7,BLUE)
    text(s,'Coding Agent Memory\nPost-training',.5,1.02,7.0,1.28,34,bold=True)
    text(s,d['subtitle'],.52,2.42,7.0,1.0,18,MID)
    text(s,'Familiar file operations → learned, useful memory',.52,3.62,8.9,.47,21,BLUE,bold=True)
    text(s,' · '.join(d['authors']),.52,4.2,8.9,.7,10.5,MID)
    for i,(t,st) in enumerate([('Files','pre-trained interface'),('RL','native task reward'),('Memory','persistent state')]):
        y=1.1+i*.79;rect(s,8.05,y,1.42,.56,PALE if i==2 else WHITE,BLUE if i==2 else LINE)
        text(s,t,8.12,y+.1,1.28,.3,17,BLUE,bold=i==2,align=PP_ALIGN.CENTER)
        if i<2:line(s,8.76,y+.57,8.76,y+.77,BLUE,1,True)
    b=text(s,'Project · code · slides',.52,4.97,4,.23,10,BLUE);b.text_frame.paragraphs[0].runs[0].hyperlink.address=d['project_url']

    # 2. Motivate with the real sequence, no invented counterfactual.
    s=slide('What should survive a context boundary?','Published · Figure 5 / Appendix A.4.3 · recorded training trajectory',
       'Start with the real Scrapy episode. The agent has already edited scheduler.py. At round 18 it writes a continuation record. At round 19, after context replacement, it reads that record. The excerpts are shortened. Do not imply a measured failure of the same task without memory; that counterfactual was not run.')
    text(s,'Task: fix response logging in Scrapy',.5,.99,9,.42,21)
    filebox(s,'ROUND 18 / SAVE THE STATE',d['case']['note'],.5,1.65,4.15,2.65,13)
    line(s,5.04,1.62,5.04,4.32,GRAY,1,dash=True)
    text(s,'context replaced',4.23,4.37,1.65,.22,9,MID,align=PP_ALIGN.CENTER)
    filebox(s,'ROUND 19 / PICK UP THE WORK',d['case']['commands'][0]+'\n\n# resume the next checks',5.45,1.65,4.05,2.65,11.3)
    takeaway(s,'Preserve the diagnosis, the evidence, and the next action.')

    # 3. Interface prior.
    s=slide('The file interface is familiar before RL','Published · Figure 3a · frozen Qwen3.5-4B · rounded point estimates',
       'Lower negative log-likelihood means these valid action tokens are more likely under the frozen model. The strongest contrast here is retrieval. This is evidence of interface familiarity, not proof of which pre-training corpus caused it. No uncertainty bars have been reconstructed.')
    label(s,'NEGATIVE LOG-LIKELIHOOD · NATS PER ACTION TOKEN · LOWER IS BETTER',.55,.99)
    r=d['prior']['rows'];grouped(s,[x[0] for x in r],[('File operations',[x[1] for x in r],BLUE),('Dedicated tools',[x[2] for x in r],GRAY)],y=1.83,h=2.35,maximum=1.5,ticks=[0,.5,1,1.5],decimals=2)
    big(s,'0.08','Retrieval NLL with files\nvs. 0.47 with dedicated tools',y=2.05)
    takeaway(s,'Build on an interface the model already knows.')

    # 4. Environment identity.
    s=slide('One shared policy, four kinds of work','CAMG environments · V1 suite · four domains',
       'CAMG is the environment suite, CAMG-RL is the learning method, and fully asynchronous PPO is its system implementation. Native task semantics and grading remain with the environments. The final policy is shared, not four separately deployed environment policies. Do not substitute CAMP-II’s General/Visual domains.')
    domains=[('Shop','WebShop','Preferences, budget,\nproduct evidence'),('Coding','SWE-smith','Diagnosis, patches,\ntest status'),('DeepResearch','LiteResearcher','Sources, findings,\nopen questions'),('AutoResearch','OpenMLE packages','Hypotheses, trials,\nintermediate results')]
    for i,(name,sub,mem) in enumerate(domains):
        x=.5+i*2.28;line(s,x,1.35,x+2.05,1.35,INK,1.4);label(s,f'0{i+1}',x,1.51,2)
        text(s,name,x,1.92,2.08,.4,19,bold=True);label(s,sub,x,2.39,2.08,BLUE);text(s,mem,x,2.91,2.08,.85,14,MID)
    rect(s,1.55,4.02,6.9,.46,PALE,PALE,0);text(s,'Shared policy  +  episode-persistent workspace',1.7,4.1,6.6,.3,17,BLUE,bold=True,align=PP_ALIGN.CENTER)
    takeaway(s,'Learn a memory behavior across heterogeneous tasks.')

    # 5. One learning path.
    s=slide('Task reward trains both acting and remembering','CAMG-RL method · ordinary file operations · fully asynchronous PPO',
       'The policy samples task and file actions as part of one trajectory; a shell action can contain both. Native task rewards supply credit through PPO. The environment owns context-replacement timing and the mechanical reset. Before reset the policy writes the bounded continuation file, and after reset it gets only the path and reads it normally. There is no separate memory-writing reward and the reset has no policy token or optimizer row. Responses may include free-form reasoning; do not reintroduce the obsolete no-thinking claim.')
    stages=[('Policy','task + file actions'),('Environment','persistent workspace'),('Task outcome','native reward'),('PPO update','shared parameters')]
    for i,(a,b) in enumerate(stages):
        x=.5+i*2.31;rect(s,x,1.65,1.98,1.1,PALE if i==0 else WHITE,BLUE if i==0 else LINE)
        text(s,a,x+.12,1.84,1.74,.3,18,BLUE if i==0 else INK,bold=True,align=PP_ALIGN.CENTER)
        text(s,b,x+.08,2.28,1.82,.3,11,MID,align=PP_ALIGN.CENTER)
        if i<3:line(s,x+2,2.2,x+2.29,2.2,BLUE,1.4,True)
    line(s,8.4,2.9,8.4,3.28,BLUE,1);line(s,8.4,3.28,1.5,3.28,BLUE,1);line(s,1.5,3.28,1.5,2.9,BLUE,1,True)
    text(s,'At a context boundary:',.55,3.8,2.7,.35,16,bold=True)
    text(s,'write continuation  →  reset context  →  read the file',3.15,3.8,6.2,.35,16,BLUE)
    takeaway(s,'No separate reward for writing a memory file.')

    # 6. Main result.
    s=slide(f"CAMG-RL reaches {k['MAIN_AVG']}% average task success",source_caption(d,'main',slide=True)+' · 4 × 128 held-out tasks · equal-weight environment average',
       'All six original comparisons are visible. The same Qwen3.5-4B backbone reaches 54.4, compared with CompactionRL 48.0; paired 95% CI for the 6.4-point gap is 3.3 to 9.5. Shop is saturated and slightly favors CompactionRL; the largest improvements are Coding and AutoResearch. DeepResearch’s gap is not statistically significant. Displayed averages are from unrounded paper scores.')
    label(s,'AVERAGE TASK SUCCESS (%)',.55,.99);hbars(s,[(r[0],r[-1]) for r in d['main']['rows']],y=1.5,row_h=.48)
    big(s,f"+{k['MAIN_GAP']} pp",f"vs. CompactionRL\nPaired 95% CI\n[{k['CI_LO']}, {k['CI_HI']}] pp",y=1.9)
    takeaway(s,f"Largest gains: Coding +{k['CODING_GAIN']} pp · AutoResearch +{k['AUTO_GAIN']} pp")

    # 7. Syntax-controlled probe, new not published.
    s=slide('Fixing syntax does not eliminate the interface gap',source_caption(d,'constrained',slide=True),
       d['constrained']['boundary']+' Constrained decoding gives AgeMem a larger boost, 6.6 points versus Bash 2.9. After both get masking, Bash remains at 20.3 versus AgeMem 16.0, a 4.3-point residual. Do not infer significance or an all-confounds-removed causal conclusion. These results are November additions, not already in the September arXiv release.')
    label(s,'SUCCESS (%) · FROZEN QWEN3.5-4B · NO RL · 512 TASKS',.55,.99,8.8,BLUE)
    rows=d['constrained']['rows'];grouped(s,['Unconstrained','Constrained\ndecoding'],[('Bash',[rows[0][-1],rows[1][-1]],BLUE),('AgeMem',[rows[2][-1],rows[3][-1]],GRAY)],x=.9,y=1.83,w=5.7,h=2.35,maximum=25,ticks=[0,10,20,25])
    big(s,f"{k['CD_GAP']} pp",'Bash advantage after\nboth interfaces receive\ngrammar + schema masks',y=1.9)
    takeaway(s,'Both improve with valid syntax; a residual gap remains.')

    # 8. Chains, accurately scoped.
    s=slide('Training increases complete memory chains','Published · Figure 3b · designated-interface metric · continuation writes excluded',
       d['acquisition']['boundary']+' CAMG-RL rises from 7.97% to 20.9% over its first and last training quarters. AgeMem’s designated six-tool chain rate is zero. This does not mean no memory use: the additional Coding-only analysis reports AgeMem workspace chains in 80.5% of episodes and CAMG-RL workspace chains in 20.3%. Do not mix those with these pooled training-quarter values.')
    label(s,'COMPLETE DESIGNATED MEMORY CHAINS (% OF EPISODES)',.55,.99)
    grouped(s,['First quarter\nupdates 1–50','Last quarter\nupdates 151–200'],[('CAMG-RL',d['acquisition']['camg'],BLUE),('AgeMem',d['acquisition']['agemem'],GRAY)],x=.9,y=1.83,w=5.7,h=2.35,maximum=25,ticks=[0,10,20,25])
    text(s,'Store → retrieve\n→ use',7.05,1.93,2.45,.85,21,BLUE,bold=True)
    text(s,'Measured through the\ndesignated memory interface.\n\nNative workspace behavior\nis a separate metric.',7.05,2.88,2.45,1.5,13,MID)
    takeaway(s,'Count a complete chain, not just a file write.')

    # 9. Same-state intervention, zero anchored.
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

    # 10. Resolve the unresolved content table by using established ablations.
    s=slide('Memory actions need the learning signal',source_caption(d,'ablation',slide=True)+' · average task success (%)',
       d['ablation']['boundary']+' The four rows are distinct interventions. Full training reaches 54.4, no memory-action actor gradients reaches 21.1, restricting to continuation during both training and evaluation gives 41.8, and restricting only at evaluation gives 28.1.')
    label(s,'AVERAGE TASK SUCCESS (%)',.55,.99)
    hbars(s,[(name,row[1]) for name,row in zip(['CAMG-RL','No memory-action\nactor gradients','Continuation only:\ntrain + evaluate','Continuation only:\nevaluate'],d['ablation']['rows'])],y=1.53,w=8.7,row_h=.67,label_w=2.6)
    takeaway(s,'Task reward can train what to save—and how to use it.')

    # 11. Interface transfer with fixed task executor.
    s=slide('The learned memory policy transfers across interfaces',source_caption(d,'transfer',slide=True),
       d['transfer']['boundary']+' The gains are 11.4 points with Claude Code file tools and 6.4 with AgeMem memory tools. Only the memory-writing and reading policy changes. This is not a claim about changing the entire task actor, and no uncertainty or sample size should be invented.')
    label(s,'AVERAGE SUCCESS (%) · FROZEN EXECUTOR · NO FURTHER TRAINING',.55,.99,8.8,BLUE)
    r=d['transfer']['rows'];grouped(s,['Claude Code\nfile tools','AgeMem\nmemory tools'],[('Frozen memory policy',[r[0][-1],r[2][-1]],GRAY),('Trained memory policy',[r[1][-1],r[3][-1]],BLUE)],x=.9,y=1.83,w=5.7,h=2.35,maximum=32,ticks=[0,10,20,30])
    big(s,f"+{k['TRANSFER_FILE_GAIN']} pp",'Claude Code file tools',y=1.75,caption_h=.42);text(s,f"+{k['TRANSFER_TOOL_GAIN']} pp",7.25,3.43,2.25,.6,30,BLUE,bold=True);text(s,'AgeMem memory tools',7.25,4.04,2.25,.35,13,MID)
    takeaway(s,'Keep task execution fixed; change only who manages memory.')

    # 12. Practical long-context reference, not single-factor causal evidence.
    s=slide('Learned file memory beats a 262K-context reference',source_caption(d,'long_context',slide=True),
       d['long_context']['boundary']+' The reference scores 49.2 average and CAMG-RL scores 54.4 with 30,720 active tokens, a 5.2-point advantage. Do not describe this as strict isolation of memory, because compaction and context settings differ. Do not claim a cost advantage without cost measurements.')
    label(s,'AVERAGE SUCCESS (%) · SAME BASE, PPO, REWARDS AND 200 UPDATES',.55,.99,8.8,BLUE)
    hbars(s,[('262K + automatic\ncompaction',d['long_context']['rows'][0][-1]),('CAMG-RL\n30,720 active tokens',d['long_context']['rows'][1][-1])],y=2.03,w=6.3,row_h=.88,label_w=2.45)
    big(s,f"+{k['CONTEXT_GAIN']} pp",'Average task success\n\nA practical comparison,\nnot a one-factor test.',y=1.85)
    takeaway(s,'More context and learned file memory solve different constraints.')

    # 13. Robustness with SD, not fake seed dots.
    s=slide('The advantage persists across training runs',source_caption(d,'robustness',slide=True),
       d['robustness']['boundary']+' CAMG-RL averages 55.3 with SD 2.9, CompactionRL 47.1 with SD 3.5. The original 54.4 and 48.0 values are individual main-table runs, not the means. A separate model-family replication on the website trains Gemma 3 4B from 15.0 to 47.7; this is not zero-shot transfer of Qwen weights.')
    label(s,'AVERAGE TASK SUCCESS (%) · FIVE RUNS PER METHOD',.55,.99,8.8,BLUE)
    x0=2.1;w=4.5;y0=1.8;y1=3.9
    for tick in [0,20,40,60]:
        x=x0+tick/60*w;line(s,x,y0,x,y1,LINE,.7);text(s,str(tick),x-.15,y1+.12,.35,.22,10,MID,align=PP_ALIGN.CENTER)
    for i,(name,m,sd) in enumerate(d['robustness']['rows']):
        y=2.3+i*1.1;x=x0+m/60*w;lo=x0+(m-sd)/60*w;hi=x0+(m+sd)/60*w;col=BLUE if i else MID
        text(s,name,.5,y-.12,1.5,.35,14,INK,bold=i==1);line(s,lo,y,hi,y,col,2.2);line(s,lo,y-.1,lo,y+.1,col,1.4);line(s,hi,y-.1,hi,y+.1,col,1.4);rect(s,x-.055,y-.055,.11,.11,col,col,0,True)
        text(s,f'{m:.1f} ± {sd:.1f}',x-.7,y-.46,1.4,.3,17,col,bold=i==1,align=PP_ALIGN.CENTER)
    big(s,f"+{k['ROBUST_GAIN']} pp",'Difference of means\n\nWhiskers show SD,\nnot confidence intervals.',y=1.85)
    takeaway(s,'The headline result is not a single-run observation.')

    # 14. External table with editable grouped bars, small and large base scales.
    s=slide('Gains carry over to external benchmarks','Published · Table 3 · benchmark success (%) · no compute-equivalence claim',
       d['external']['boundary']+' Focus on matched base-to-trained gains at each scale: SWE-bench Verified 7.6 to 15.8 for 4B and 14.8 to 27.6 for 9B; MLE-bench Lite 0.0 to 4.5 and 4.5 to 9.1. Larger frozen MoE models remain capability references, visible in the website’s full table.')
    label(s,'FROZEN BASE VS. CAMG-RL · SAME MODEL SCALE',.55,.99)
    er=d['external']['rows']
    for j,(lab,col) in enumerate([('Frozen base',GRAY),('CAMG-RL',BLUE)]):
        rect(s,.9+j*2.1,1.32,.13,.13,col,col,0);text(s,lab,1.12+j*2.1,1.28,1.8,.3,12,MID)
    grouped(s,['4B','9B'],[('Frozen base',[er[0][1],er[3][1]],GRAY),('CAMG-RL',[er[1][1],er[4][1]],BLUE)],x=.9,y=1.84,w=3.7,h=2.25,maximum=30,ticks=[0,10,20,30],legend=False,label_h=.24)
    grouped(s,['4B','9B'],[('Frozen base',[er[0][2],er[3][2]],GRAY),('CAMG-RL',[er[1][2],er[4][2]],BLUE)],x=5.85,y=1.84,w=3.65,h=2.25,maximum=10,ticks=[0,5,10],legend=False,label_h=.24)
    text(s,'SWE-bench Verified',.85,4.45,3.9,.3,14,INK,bold=True,align=PP_ALIGN.CENTER)
    text(s,'MLE-bench Lite',5.75,4.45,3.9,.3,14,INK,bold=True,align=PP_ALIGN.CENTER)
    takeaway(s,'Improve the trained policy’s own base on both benchmarks.')

    # 15. Resolve the opening story, without making it a causal control.
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

    # 16. End on the scientific takeaways, not an unasked appendix.
    s=slide('Familiar operations. Learned memory.','CAMP V1 · published paper + labelled November additions · data/research.json',
       'Close with three scoped statements. Familiarity is measured before training. Task reward teaches useful memory behaviors, supported by acquisition, ablation and local content intervention. The benefits extend to external benchmarks and, in November additions, new memory interfaces. Do not claim universal causality or compute savings. Full experiment tables, protocol boundaries, source/version labels and editable slides are on the project page.')
    for i,(a,b) in enumerate([('Start from a familiar interface.','Use ordinary file operations instead of inventing a new memory language.'),('Train memory through the task.','Preserve and reuse useful state with downstream reward.'),('Test the behavior beyond its original form.','Probe content, new interfaces, larger contexts and external tasks.')]):
        y=1.23+i*1.05;text(s,f'0{i+1}',.55,y,.55,.38,19,BLUE);text(s,a,1.35,y,8.0,.42,23,bold=True);text(s,b,1.35,y+.52,8.0,.4,14,MID)
    b=text(s,'liruiluo.github.io/agentmemorygym',1.35,4.67,7.8,.38,18,BLUE,bold=True);b.text_frame.paragraphs[0].runs[0].hyperlink.address=d['project_url']

    out.parent.mkdir(parents=True,exist_ok=True);prs.save(out)
    notes='# CAMP V1 · 16-slide research talk\n\nUpdated 2026-11-14. Approximately 15 minutes. White academic house style; all exhibits are native editable objects. Results are loaded from `data/research.json`. November additions are author-reported revised-manuscript results, separately labelled from published September results.\n\n'
    for n,t,src,body in outline:notes+=f'## {n:02}. {t or d["project"]}\n\n**Source:** {src}\n\n{body}\n\n'
    (out.parent/'speaker-notes.md').write_text(notes)
    (out.parent/'deck-manifest.json').write_text(json.dumps({'slides':len(prs.slides),'data_sha256':sha,'raster_images':0,'updated':d['updated'],'slides_outline':[{'number':n,'title':t or d['project'],'source':src} for n,t,src,_ in outline]},indent=2)+'\n')
    print(json.dumps({'pptx':str(out),'slides':len(prs.slides),'raster_images':0,'data_sha256':sha}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--site-root',type=Path,default=ROOT);a=p.parse_args();build(a.out,a.site_root)
