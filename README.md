# Coding Agent Memory Post-training

The public **CAMP V1 / CAMG-RL** research page and editable 16-slide talk.

- [Website](https://liruiluo.github.io/agentmemorygym/)
- [Paper and version history](https://arxiv.org/abs/2609.34422)
- [Slides PDF](https://liruiluo.github.io/agentmemorygym/assets/slides/coding-agent-memory-post-training-slides.pdf) · [Editable PowerPoint](https://liruiluo.github.io/agentmemorygym/assets/slides/coding-agent-memory-post-training-slides.pptx)
- [Shared code repository](https://github.com/jd-opensource/CodingAgentMemoryGym)

## Build and check

Use Python 3.9+ with the packages in `requirements-presentation.txt`. The default
headless PDF exporter uses the macOS Arial and Menlo font files. On another OS,
export the generated PPTX with PowerPoint/LibreOffice or adapt the renderer's font
registration to licensed local equivalents, then repeat the visual and font checks.
No frontend dependencies, external fonts or CDN scripts are needed at runtime.

```bash
python3 scripts/build_website.py
python3 scripts/build_social_card.py
python3 scripts/build_slides.py --out /tmp/camp-talk/deck.pptx
python3 scripts/render_slides_pdf.py /tmp/camp-talk/deck.pptx /tmp/camp-talk/deck.pdf
python3 scripts/build_website.py --check
python3 scripts/verify_release.py \
  --pptx /tmp/camp-talk/deck.pptx --pdf /tmp/camp-talk/deck.pdf \
  --out /tmp/camp-talk/checks.json
python3 scripts/check_browser.py --out /tmp/camp-talk/browser
python3 -m unittest discover -s scripts -p 'test_*.py'
```

Browser scripts use headless Chrome, with Playwright Chromium as fallback.
Install a browser with `python3 -m playwright install chromium` if needed.
Open `index.html` directly, or use a loopback-only preview:

```bash
python3 -m http.server 4173 --bind 127.0.0.1
```

## Source of truth

[`data/research.json`](data/research.json) feeds both the website and the slides.
Edit it, the HTML template, and the builders; do not hand-edit generated `index.html`
or a chart inside a released deck. The shared loader checks the schema and important
scientific boundaries. Displayed paper averages are retained rather than recomputed
from rounded environment values.

- `scripts/site.template.html` + `build_website.py`: semantic, responsive static page.
- `scripts/build_slides.py`: native editable text, diagrams and charts, plus speaker notes.
- `scripts/render_slides_pdf.py`: deterministic vector/text PDF export, fail on text overflow.
- `scripts/build_social_card.py`: source-generated social preview, no research data fabrication.
- `slides/outline.md`, `slides/speaker-notes.md`: the current talk, not an older release's outline.
- `assets/slides/build-manifest.json`: data, PDF and PPTX hashes for the released pair.
- `scripts/check_browser.py`: responsive widths, no-JS content, keyboard, clipboard and reduced motion.
- `scripts/verify_release.py`: data/build freshness, anchors, local links, geometry, notes and fonts.

## Evidence versions

**Published** figures and main results refer to [arXiv v2, 30 September 2026](https://arxiv.org/abs/2609.34422v2).
The main result table is **Table 2** in that release; it is Table 1 in the revised
manuscript. The archived `assets/paper.pdf` remains the original **v1** for compatibility;
the primary Paper link goes to arXiv, not this historical copy.

**November 2026 additions** are author-reported revised-manuscript results: constrained
decoding, fixed-executor memory-interface transfer, the long-context reference, model-family replication, and the Coding workspace-chain
clarification. Five-run robustness was already published in Appendix D.8.
They are explicitly labelled as additions, not as already part of the September arXiv
release. Raw run receipts were not independently re-verified for this presentation update.
Protocol boundaries are included in the data file, page captions and speaker notes.
Only the interface-transfer portion of the additional memory-quality study is included.

This is the **four-environment RL** project. CAMP-II and its five-environment dataset are
linked only as a separate related release; their methods, data and results are not merged here.

## Release procedure

1. Rebuild and run the checks above. Inspect **all 16 slides** and desktop/mobile screenshots;
   passing structural checks alone does not establish visual quality.
2. Copy the checked PDF/PPTX together into `assets/slides/` using their existing filenames.
3. Copy the generated `speaker-notes.md` into `slides/`, update `slides/outline.md`, then run
   `python3 scripts/write_release_manifest.py`.
4. Re-run `verify_release.py` on the release pair. Commit source, data and outputs together.
5. Push `main`; verify the GitHub Pages build is for that exact commit, then verify live HTML,
   data, PDF and PPTX hashes against the local release. Browser checks accept `--url` for a live page.

Build products and screenshots belong outside the repository; only public delivery assets
are committed. Interrupted builds can be rerun safely. Do not publish one half of a PDF/PPTX pair.
