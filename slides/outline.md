# CAMP V1 · 16-slide public research talk

Updated 2026-11-14. English, approximately 15 minutes.

Story: familiar file interface → task-reward learning → useful memory → transfer.
White 16:9 academic style, native editable exhibits, one main argument per slide.
The recorded Scrapy episode opens and closes the story. No references or appendix tail.

| # | Action title | Evidence |
|---|---|---|
| 1 | Coding Agent Memory Post-training | CAMP V1 · 14 November 2026 · arXiv:2609.34422 |
| 2 | What should survive a context boundary? | Published · Figure 5 / Appendix A.4.3 · recorded training trajectory |
| 3 | The file interface is familiar before RL | Published · Figure 3a · frozen Qwen3.5-4B · rounded point estimates |
| 4 | One shared policy, four kinds of work | CAMG environments · V1 suite · four domains |
| 5 | Task reward trains both acting and remembering | CAMG-RL method · ordinary file operations · fully asynchronous PPO |
| 6 | CAMG-RL reaches 54.4% average task success | Published · Table 2 · 4 × 128 held-out tasks · equal-weight environment average |
| 7 | Fixing syntax does not eliminate the interface gap | ADDITIONAL · November 2026 · revised Appendix D.16 · author-reported |
| 8 | Training increases complete memory chains | Published · Figure 3b · designated-interface metric · continuation writes excluded |
| 9 | The saved content changes what happens next | Published · Appendix D.3 · same-state continuations · eligible tasks only |
| 10 | Memory actions need the learning signal | Published · Figure 4 · average task success (%) |
| 11 | The learned memory policy transfers across interfaces | ADDITIONAL · November 2026 · revised Appendix D.10 · author-reported |
| 12 | Learned file memory beats a 262K-context reference | ADDITIONAL · November 2026 · revised Appendix D.14 · author-reported |
| 13 | The advantage persists across training runs | Published · Appendix D.8 |
| 14 | Gains carry over to external benchmarks | Published · Table 3 · benchmark success (%) · no compute-equivalence claim |
| 15 | The remembered state becomes the next action | Published · Figure 5 / Appendix A.4.3 · shortened training-episode excerpts |
| 16 | Familiar operations. Learned memory. | CAMP V1 · published paper + labelled November additions · data/research.json |

## Evidence and version boundaries

- Published results refer to arXiv v2 (30 September 2026); the main result is Table 2 there, Table 1 in the revised manuscript.
- November additions are clearly labelled, author-reported revised-manuscript results. Raw run receipts were not independently re-verified for this update.
- Slide 8 counts designated-interface chains and excludes mandatory continuation writes; native workspace use is a different metric.
- Slide 9 is a same-state local intervention over eligible tasks, not the entire task population.
- Slide 10 uses published ablations, not the omitted additional content-quality success panel.
- Slide 11 changes only the memory policy with a fixed task executor; no further training.
- Slide 12 changes both context window and compaction procedure; it is a practical reference, not a single-factor causal test.
- Slide 13 uses published Appendix D.8 mean ± SD across five runs; no invented per-run points or confidence intervals.
- Slide 14 shows matched base-to-trained improvements, not compute-equivalent comparisons.
- Slides 2/15 use shortened excerpts from one real training episode, not a held-out or counterfactual comparison.

See [speaker notes](speaker-notes.md) and [shared data](../data/research.json) for the complete speaking guide and experiment-specific protocols.
