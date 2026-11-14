#!/usr/bin/env python3
"""Headless responsive, progressive-enhancement and interaction checks.

Uses local Chrome if available, otherwise Playwright Chromium. No public server.
"""
import argparse,json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]

def run(url,out):
    out.mkdir(parents=True,exist_ok=True);report=[]
    with sync_playwright() as pw:
        try:b=pw.chromium.launch(channel='chrome',headless=True)
        except Exception:b=pw.chromium.launch(headless=True)
        for width in [1440,1024,768,390,320]:
            p=b.new_page(viewport={'width':width,'height':960},device_scale_factor=1,reduced_motion='reduce')
            errors=[];p.on('pageerror',lambda err:errors.append(str(err)))
            p.goto(url,wait_until='networkidle')
            assert p.locator('h1').count()==1
            assert p.locator('#evidence .bar-row').count()==6
            assert p.locator('.case-panel').count()==3
            assert p.locator('[data-case]').count()==3
            metrics=p.evaluate('''() => ({width:innerWidth,scroll:document.documentElement.scrollWidth,
              brokenImages:[...document.images].filter(i=>!i.complete||!i.naturalWidth).length,
              heroMetricsBottom:document.querySelector('.hero-result').getBoundingClientRect().bottom,
              missingAnchors:[...document.querySelectorAll('a[href^="#"]')].filter(a=>!document.getElementById(a.hash.slice(1))).map(a=>a.hash)})''')
            assert metrics['scroll']<=width,metrics
            assert not metrics['brokenImages'] and not metrics['missingAnchors'],metrics
            if width<=390:assert metrics['heroMetricsBottom']<800,metrics
            if width in [1440,390,320]:
                p.screenshot(path=str(out/f'hero-{width}.png'))
                p.screenshot(path=str(out/f'full-{width}.png'),full_page=True)
                # Element screenshots exclude the sticky header so evidence is not obscured.
                p.add_style_tag(content='.topbar{position:relative!important}.case-nav{position:relative!important;top:auto!important}html{scroll-behavior:auto!important}')
                for sid in ['evidence','idea','memory','transfer','case','paper']:
                    p.locator('#'+sid).screenshot(path=str(out/f'{sid}-{width}.png'))
            # Expand all tables; they may scroll locally, never widen the page.
            p.locator('details').evaluate_all('(els)=>els.forEach(el=>el.open=true)')
            assert p.evaluate('document.documentElement.scrollWidth')<=width
            p.locator('[data-case="case-read"]').click()
            assert p.locator('#case-read').evaluate('(el)=>el.classList.contains("selected")')
            assert p.locator('[data-case="case-read"]').get_attribute('aria-pressed')=='true'
            assert p.locator('[data-case][aria-pressed="true"]').count()==1
            p.locator('#copy-citation').click()
            p.wait_for_function("document.getElementById('copy-status').textContent.length > 0",timeout=5000)
            assert p.locator('#copy-status').inner_text() in ['BibTeX copied.','Text selected. Use your system’s Copy command.']
            assert not errors,errors
            report.append({'viewport':width,'passed':True,'metrics':metrics,'page_errors':errors});p.close()
        # No-JS content and native details remain usable.
        ctx=b.new_context(java_script_enabled=False,viewport={'width':390,'height':960});p=ctx.new_page();p.goto(url)
        assert p.locator('.case-panel').count()==3
        assert p.locator('#evidence .bar-row').count()==6
        p.locator('details summary').first.click()
        assert p.locator('details').first.get_attribute('open') is not None
        report.append({'javascript':False,'passed':True});ctx.close()
        # Native keyboard behavior and reduced motion.
        p=b.new_page(reduced_motion='reduce');p.goto(url);p.keyboard.press('Tab')
        assert p.locator(':focus').inner_text()=='Skip to content'
        p.keyboard.press('Enter');assert p.evaluate('location.hash')=='#main'
        assert p.evaluate('getComputedStyle(document.documentElement).scrollBehavior')=='auto'
        report.append({'keyboard_and_reduced_motion':True,'passed':True});b.close()
    (out/'browser-checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--url',default=(ROOT/'index.html').as_uri());ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();run(a.url,a.out)
