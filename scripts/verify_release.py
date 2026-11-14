#!/usr/bin/env python3
"""Fail closed on stale data, absent links, slide overflow and artifact drift."""
import argparse,hashlib,json,re,subprocess
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import fitz
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from research_data import load,stats,ROOT
from build_website import build
from presentation_policy import assert_public_story
from slide_story import STORY,question_label,assert_slide_story

class Page(HTMLParser):
    def __init__(self):super().__init__();self.ids=[];self.links=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if 'id' in d:self.ids.append(d['id'])
        if 'href' in d:self.links.append(d['href'])
        if 'src' in d:self.links.append(d['src'])

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def verify(root,pptx,pdf):
    d=load(root);k=stats(d);html=(root/'index.html').read_text();assert html==build(),'Stale website'
    p=Page();p.feed(html);assert not [i for i,n in Counter(p.ids).items() if n>1],'Duplicate IDs'
    for href in p.links:
        if href.startswith('#'):assert href[1:] in p.ids,href
        elif not re.match(r'\w+://',href):assert (root/href.split('#')[0]).is_file(),href
    for anchor in ['top','idea','gym','method','evidence','paper']:assert anchor in p.ids
    assert 'unpkg.com' not in html and 'AgeMem completes no chain' not in html
    assert_public_story(html)
    assert d['sources']['additional']['independently_run_verified'] is False
    assert 'no separate reasoning' not in html.lower()
    assert not any(x in html for x in ['/Users/','/dev/shm','teacher.key','18.0%'])
    deck=Presentation(pptx);assert len(deck.slides)==len(STORY);assert_slide_story(deck)
    assert sha(root/'data/research.json') in deck.core_properties.comments
    shapes=0;min_font=100;pictures=0;paper_pictures=0;generated_pictures=0
    figure_assets=json.loads((root/'slides/figure-assets.json').read_text())
    illustration_assets=json.loads((root/'slides/illustration-assets.json').read_text())
    for i,s in enumerate(deck.slides,1):
        assert s.notes_slide.notes_text_frame.text.strip(),f'Missing notes {i}'
        assert not any(x in s.notes_slide.notes_text_frame.text for x in ['/Users/','/dev/shm','18.0 baseline'])
        for o in s.shapes:
            shapes+=1
            if o.shape_type==MSO_SHAPE_TYPE.PICTURE:
                pictures+=1
                if o.name.startswith('paper-figure:'):
                    paper_pictures+=1;asset=figure_assets[o.name.split(':',1)[1]]
                    assert hashlib.sha256(o.image.blob).hexdigest()==asset['png_sha256']
                    for kind in ('pdf','png'):assert sha(root/asset[kind])==asset[kind+'_sha256']
                    x0,y0,x1,y1=asset.get('clip_pt',[0,0,asset['width_pt'],asset['height_pt']])
                    expected=[x0/asset['width_pt'],y0/asset['height_pt'],1-x1/asset['width_pt'],1-y1/asset['height_pt']]
                    assert all(abs(a-b)<1e-5 for a,b in zip([o.crop_left,o.crop_top,o.crop_right,o.crop_bottom],expected)),'Figure crop drift'
                elif o.name=='generated-illustration:memory_tools_unused':
                    assert i==4,'Illustration belongs on the memory-use background page'
                    generated_pictures+=1;asset=illustration_assets['memory_tools_unused']
                    assert hashlib.sha256(o.image.blob).hexdigest()==asset['image_sha256']
                    assert sha(root/asset['image'])==asset['image_sha256']
                    assert sha(root/asset['prompt'])==asset['prompt_sha256']
                    assert asset['requested_model']=='gpt-image-2'
                    assert not any([o.crop_left,o.crop_top,o.crop_right,o.crop_bottom]),'Unexpected raster crop'
                else:raise AssertionError('Unexpected picture: '+o.name)
            assert min(o.left,o.top)>=0 and o.left+o.width<=deck.slide_width+5 and o.top+o.height<=deck.slide_height+5,(i,o.name)
            if o.has_text_frame:
                for pa in o.text_frame.paragraphs:
                    for run in pa.runs:
                        if run.font.size:min_font=min(min_font,run.font.size.pt)
    doc=fitz.open(pdf);assert len(doc)==len(STORY);assert (paper_pictures,generated_pictures,pictures)==(4,1,5)
    alltext='\n'.join(p.get_text() for p in doc)
    for page,entry in zip(doc,STORY):
        if entry['phase']:
            assert question_label(entry['phase']) in page.get_text(),'Missing experimental question in PDF'
    assert '54.4' in alltext and '+6.4 pp' in alltext and '+11.4 pp' in alltext
    assert '18.0 baseline' not in alltext and '\ufffd' not in alltext
    raster_counts=[len(p.get_images()) for p in doc]
    assert raster_counts==[1 if i==3 else 0 for i in range(len(doc))],('Unexpected PDF raster image',raster_counts)
    font_report=subprocess.check_output(['pdffonts',str(pdf)],text=True)
    assert 'Type 3' not in font_report
    for row in font_report.splitlines()[2:]:
        fields=row.split();assert fields[-5]=='yes',row
    manifest_path=root/'assets/slides/build-manifest.json'
    if pptx.resolve().parent==(root/'assets/slides').resolve():
        manifest=json.loads(manifest_path.read_text())
        for file,digest in manifest['files'].items():assert sha(root/file)==digest,('Release drift',file)
        assert manifest['data_sha256']==sha(root/'data/research.json')
    # Test source-derived chart wiring, not only one frozen numerical coincidence.
    from copy import deepcopy
    from research_data import stats as get_stats
    other=deepcopy(d);other['main']['rows'][-1][-1]+=1
    assert float(get_stats(other)['MAIN_AVG'])==float(k['MAIN_AVG'])+1
    return {'passed':True,'slides':len(STORY),'native_shapes':shapes-pictures,'paper_figure_pictures':paper_pictures,'generated_illustrations':generated_pictures,'pdf_raster_images':sum(raster_counts),'minimum_font_pt':min_font,'data_sha256':sha(root/'data/research.json'),'pptx_sha256':sha(pptx),'pdf_sha256':sha(pdf),'html_sha256':sha(root/'index.html'),'local_links':len(p.links),'fonts':font_report}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--pptx',type=Path,required=True);ap.add_argument('--pdf',type=Path,required=True);ap.add_argument('--out',type=Path);a=ap.parse_args()
    result=verify(ROOT,a.pptx,a.pdf)
    if a.out:a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
