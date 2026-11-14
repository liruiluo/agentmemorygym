# Coding Agent Memory Post-training

The public **CAMP V1 / CAMG-RL** research page and editable 17-slide talk.

- [Website](https://liruiluo.github.io/agentmemorygym/)
- [Paper and version history](https://arxiv.org/abs/2609.34422)
- [Slides PDF](https://liruiluo.github.io/agentmemorygym/assets/slides/coding-agent-memory-post-training-slides.pdf) · [Editable PowerPoint](https://liruiluo.github.io/agentmemorygym/assets/slides/coding-agent-memory-post-training-slides.pptx)
- [Shared code repository](https://github.com/jd-opensource/CodingAgentMemoryGym)

## Build and check

Use Python 3.9+ with the packages in `requirements-presentation.txt`. The default
headless PDF exporter uses the macOS Arial and Menlo font files and the three
hash-bound vector figure PDFs in `assets/slides/figures/`. It checks that the
PPTX pictures and crop rectangles match those originals before placing the vectors. The memory-underuse background image is a separately hash-bound raster asset. On another OS,
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
- `scripts/build_slides.py` + `slide_story.py`: the story order, chapter trail, native editable charts and text, plus speaker notes.
- `slides/figure-assets.json`: exact hashes of the three original paper figures and the focused crop rectangles used in Background and Environments. Five placements use pictures in PPTX and original vectors in PDF.
- `slides/illustration-assets.json`: the GPT-image-2 memory-underuse image, prompt and generation metadata. This one asset remains raster in both formats; other text and charts are editable native content.
- `scripts/render_slides_pdf.py`: deterministic vector/text PDF export, fail on text overflow.
- `scripts/build_social_card.py`: source-generated social preview, no research data fabrication.
- `slides/outline.md`, `slides/speaker-notes.md`: the current talk, not an older release's outline.
- `assets/slides/build-manifest.json`: data, PDF and PPTX hashes for the released pair.
- `scripts/check_browser.py`: responsive widths, no-JS content, keyboard, clipboard and reduced motion.
- `scripts/verify_release.py`: data/build freshness, anchors, local links, geometry, notes and fonts.

## Public presentation

The website follows a story: familiar file operations → learning useful memory →
stronger task execution → a skill that travels → one real task carried to completion.
Use a small set of figures with clear takeaways. Keep provenance/version checks,
seed accounting and acceptance notes in the data and internal verification rather
than the rendered page. Project editing rules are in `AGENTS.md`.

The talk opens with title → roadmap → background: why memory is needed, why available
memory tools may remain underused, the prior-mismatch hypothesis and the research
question. Background uses the upper row of Figure 1 and a memory-underuse failure graphic rather than a zero statistic; it stops at the problem. A separate contribution overview follows.
The environment page uses Figure 2’s right-hand panel, paired with what each task family must remember. CAMG environments then lead into Method, where original Figures 1 and 2 explain the
file-memory idea and learning mechanism. The frozen-model interface-prior experiment
appears within Q2 of Results. The experimental story is Q1: does CAMP improve
long-horizon task performance; Q2: what drives its gains; Q3: does the learned memory
behavior generalize. Within Q2, Q2.1 groups the memory-learning ablations and same-state
content intervention; Q2.2 follows with the frozen-model file-operation prior. These are
small question labels, not divider pages or replacements for the conclusion titles. The complete original Figure 5 shows the Scrapy case and closes Q2 before the two transfer
slides in Q3. Each result page keeps its conclusion-led title and chart, with a
small question header; no divider pages are added. Chapter navigation and questions
sit above the larger slide title. Each experimental plot now has one readable
comparison/intervention line below its title: what is compared, what changes and
which factors are held fixed. The chart remains dominant and the takeaway states
the finding. The recorded case uses the complete original Figure 5 at full width, with all four
panels and the context-replacement boundary intact. It has no added protocol line. The final slide is titled **Takeaways** and retains the three
summary points and project link. Secondary checks stay in speaker notes. Visuals are selected by explanatory value, not an image quota: the roadmap, contribution preview and conclusion retain concise text.

The shared result file retains the source references for each experiment. Website
selection does not change the data used by the 17-slide talk. The paper link leads
to arXiv; `assets/paper.pdf` remains available for existing links. CAMP-II is linked
as related work and keeps its own methods and five-environment suite.

## Release procedure

1. Rebuild and run the checks above. Inspect **all 17 slides** and desktop/mobile screenshots;
   passing structural checks alone does not establish visual quality.
2. Copy the checked PDF/PPTX together into `assets/slides/` using their existing filenames.
3. Copy the generated `speaker-notes.md` and `outline.md` into `slides/`, then run
   `python3 scripts/write_release_manifest.py`.
4. Re-run `verify_release.py` on the release pair. Commit source, data and outputs together.
5. Push `main`; verify the GitHub Pages build is for that exact commit, then verify live HTML,
   data, PDF and PPTX hashes against the local release. Browser checks accept `--url` for a live page.

Build products and screenshots belong outside the repository; only public delivery assets
are committed. Interrupted builds can be rerun safely. Do not publish one half of a PDF/PPTX pair.
