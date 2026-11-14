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
    paths=['data/research.json','index.html','styles.css','script.js','scripts/build_slides.py','scripts/render_slides_pdf.py','scripts/build_website.py','scripts/site.template.html','scripts/research_data.py','slides/outline.md','slides/speaker-notes.md','assets/social-card.png',str(pptx.relative_to(ROOT)),str(pdf.relative_to(ROOT))]
    manifest={'schema_version':1,'updated':load()['updated'],'slides':len(deck.slides),'data_sha256':data_sha,'files':{x:sha(ROOT/x) for x in paths}}
    (folder/'build-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('Release manifest written.')
if __name__=='__main__':main()
