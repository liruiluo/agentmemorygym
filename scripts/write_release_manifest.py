#!/usr/bin/env python3
"""Bind the public pair and its sources after visual review, never before export."""
import hashlib,json
from pathlib import Path
from pptx import Presentation
from research_data import ROOT,load

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    folder=ROOT/'assets/slides';pptx=folder/'coding-agent-memory-post-training-slides.pptx';pdf=folder/'coding-agent-memory-post-training-slides.pdf'
    deck=Presentation(pptx);data_sha=sha(ROOT/'data/research.json');assert data_sha in deck.core_properties.comments,'Stale PPTX data'
    paths=['assets/paper.pdf','data/research.json','index.html','styles.css','script.js','scripts/build_slides.py','scripts/render_slides_pdf.py','scripts/build_website.py','scripts/site.template.html','scripts/research_data.py','scripts/presentation_policy.py','scripts/verify_release.py','scripts/test_research_data.py','AGENTS.md','slides/outline.md','slides/speaker-notes.md','assets/social-card.png',str(pptx.relative_to(ROOT)),str(pdf.relative_to(ROOT))]
    paths+=['scripts/slide_story.py','scripts/test_slide_story.py','scripts/write_release_manifest.py','slides/figure-assets.json','README.md','requirements-presentation.txt']
    figures=json.loads((ROOT/'slides/figure-assets.json').read_text())
    paths += [a[k] for a in figures.values() for k in ('pdf','png')]
    illustrations=json.loads((ROOT/'slides/illustration-assets.json').read_text())
    paths+=['slides/illustration-assets.json']+[a[k] for a in illustrations.values() for k in ('image','prompt')]
    manifest={'schema_version':1,'updated':load()['updated'],'slides':len(deck.slides),'data_sha256':data_sha,'files':{x:sha(ROOT/x) for x in paths}}
    (folder/'build-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('Release manifest written.')
if __name__=='__main__':main()
