"""Keep internal reporting out of the public project-page narrative."""
from html.parser import HTMLParser
import re

class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__();self.parts=[];self.hidden=0
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style'):self.hidden+=1
    def handle_endtag(self,tag):
        if tag in ('script','style'):self.hidden=max(0,self.hidden-1)
    def handle_data(self,data):
        if not self.hidden:self.parts.append(data)

REPORT_PATTERNS=(
    r'evidence versions?',r'published results?',r'additional experiments?',
    r'November additions?',r'author.reported',r'raw run receipts?',
    r'independently.{0,20}verified',r'five training runs?',r'multi.seed',
    r'standard deviation',r'confidence interval',r'\bCI\b',
    r'Appendix\b',r'not reconstructed',r'not statistically significant',
    r'without JavaScript',r'all comparisons visible at once',
)

def assert_public_story(html):
    page=VisibleText();page.feed(html);text=' '.join(page.parts)
    for pattern in REPORT_PATTERNS:
        assert not re.search(pattern,text,re.I),f'Report prose in public page: {pattern}'
    for obsolete in ['source-tag','version-note','stability-plot']:
        assert obsolete not in html,f'Retired report UI: {obsolete}'
    return text
