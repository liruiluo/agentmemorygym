# CAMG-RL project website

Static project page for **Coding Agent Memory Post-training: Unlocking the Memory Potential of Pre-trained File Operations for Long-Horizon Tasks via Reinforcement Learning**.

Live page: <https://liruiluo.github.io/agentmemorygym/>

Paper: <https://arxiv.org/abs/2609.34422>

Slides: [PDF](https://liruiluo.github.io/agentmemorygym/assets/slides/coding-agent-memory-post-training-slides.pdf) · [Editable PowerPoint](https://liruiluo.github.io/agentmemorygym/assets/slides/coding-agent-memory-post-training-slides.pptx)

## Run locally

```bash
cd agentmemorygym-website
python3 -m http.server 4173 --bind 127.0.0.1
```

Open <http://127.0.0.1:4173>.

The site uses the paper's checked figure exports and a local PDF copy. The training repository and unpublished code are intentionally not linked from the page.

## Slides

The 16-slide English talk follows the white academic style of the author's earlier
project presentations. Its figures and results come from the public paper
`arXiv:2609.34422v1`. The [outline](slides/outline.md) records the source for each slide.

Build outside the repository with Python 3.9+, `python-pptx`, `matplotlib`, `numpy`,
`Pillow`, and `reportlab`:

```bash
python3 scripts/build_slides.py --out /tmp/camg-slides/deck.pptx
python3 scripts/render_slides_pdf.py /tmp/camg-slides/deck.pptx /tmp/camg-slides/deck.pdf
```

The PDF renderer uses macOS Arial and Menlo fonts and reports any overflowing text boxes.
The editable diagrams and tables follow the CRG/SPHERE reference; results are
redrawn at presentation scale with prominent metric callouts.
Review all rendered pages before replacing the published PDF and PPTX together
in `assets/slides/`.
