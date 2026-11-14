#!/usr/bin/env python3
from pathlib import Path
from html import escape
from playwright.sync_api import sync_playwright
from research_data import load,stats,ROOT

def main():
    d=load();k=stats(d)
    html='''<html><style>*{box-sizing:border-box}body{margin:0;background:white;color:#17232d;font-family:Arial,sans-serif;width:1200px;height:630px;padding:62px 72px}.brand{font-size:23px;font-weight:700;color:#2066a4}h1{font-size:67px;line-height:1.04;letter-spacing:-3px;margin:37px 0 22px;font-weight:700}h1 span{color:#2066a4}p{font-size:22px;color:#586773;margin:0;line-height:1.5}.bottom{display:flex;align-items:end;justify-content:space-between;border-top:1px solid #dce3e8;margin-top:37px;padding-top:24px}.metric{font-size:38px;color:#2066a4;font-weight:bold}.metric small{font-size:16px;color:#586773;display:block;font-weight:normal;margin-top:5px}.link{font-size:17px;color:#586773}</style><body><div class="brand">CAMG-RL · Coding Agent Memory Post-training</div><h1>Teaching agents<br>to remember <span>with files.</span></h1><p>Familiar file operations. Learned long-horizon memory.</p><div class="bottom"><div class="metric">'''+k['MAIN_AVG']+'''%<small>average task success · 4 environments</small></div><div class="metric">+'''+k['MAIN_GAP']+''' pp<small>vs. CompactionRL · published result</small></div><div class="link">liruiluo.github.io/agentmemorygym</div></div></body></html>'''
    with sync_playwright() as pw:
        try:b=pw.chromium.launch(channel='chrome',headless=True)
        except Exception:b=pw.chromium.launch(headless=True)
        p=b.new_page(viewport={'width':1200,'height':630},device_scale_factor=1);p.set_content(html)
        p.screenshot(path=str(ROOT/'assets/social-card.png'));b.close()
if __name__=='__main__':main()
