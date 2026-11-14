# CAMP · 17-slide public research talk

Updated 2026-11-14. English, approximately 15 minutes.

Story: memory need → tool underuse → prior-mismatch hypothesis → research question → contributions → task environments → CAMP method → effectiveness → mechanism → transfer → complete case.

The roadmap follows the title. Background ends at the research question; the separate contribution overview comes next. Background shows only the context-only upper row of Figure 1. The complete Figure 1 and its file-memory solution begin Method, while the frozen-model prior experiment belongs to the mechanism results. The technical Scrapy case appears once, after the results. A lightweight four-chapter trail marks progress; result pages also name the question they answer. There are no full-page chapter dividers, references or appendix tail.

| # | Chapter | Role | Action title | Exhibit |
|---|---|---|---|---|
| 1 | Identity | Identity | Coding Agent Memory Post-training | Full title, authors, affiliation and links |
| 2 | Roadmap | Roadmap | The story in four questions | Four chapters and the questions they answer |
| 3 | Background | Memory need | Long tasks need memory beyond the active context | Figure 1 upper row: context lost → repeated work → unfinished task |
| 4 | Background | Research problem | Having memory tools does not ensure their use | Unused memory tools → lost constraint → failure; prior-mismatch hypothesis → question |
| 5 | Contributions | Contributions | Three contributions to learning reusable memory | Environment suite / learning method / empirical study |
| 6 | Environments | Task demands | One shared policy, four kinds of work | Four task families and the state each must retain |
| 7 | Method | Core idea | Use files to carry working state beyond the context | Original Figure 1, both contrast rows |
| 8 | Method | Learning mechanism | Task reward trains both acting and remembering | Original Figure 2 + shared policy/reward/PPO callouts |
| 9 | Results & analysis | Effectiveness | CAMG-RL reaches 54.4% average task success | Six-method main comparison |
| 10 | Results & analysis | Effectiveness | Learned file memory beats a 262K-context reference | 262K-context practical reference |
| 11 | Results & analysis | Prior evidence | The file interface is familiar before RL | Frozen-model file vs. dedicated-tool likelihood |
| 12 | Results & analysis | Mechanism | Memory actions need the learning signal | Memory-action gradient and continuation ablations |
| 13 | Results & analysis | Mechanism | The saved content changes what happens next | Blank/shuffled memory from the same state |
| 14 | Results & analysis | Transfer | The learned memory policy transfers across interfaces | New memory interfaces, fixed task executor |
| 15 | Results & analysis | Transfer | Gains carry over to external benchmarks | Matched base vs. trained external results |
| 16 | Results & analysis | Case study | Case study: carry a Scrapy fix across contexts | Scrapy saved note + read/check actions + successful finish |
| 17 | Conclusion | Conclusion | Familiar operations. Learned memory. | Three takeaways and project link |

## Speaking and source notes

The contribution overview follows the paper’s actual suite / method / empirical-study structure. Figures 1 and 2 retain their original content; the conceptual comparison is not presented as a measured counterfactual. Results use unchanged source values and essential on-slide comparison conditions. Full provenance and scientific qualifications are in [speaker notes](speaker-notes.md) and [shared data](../data/research.json). Multi-run robustness, the CAMG-RL acquisition trajectory and the syntax-only probe remain optional Q&A material, not additional talk pages. The background shows unused memory tools, a lost constraint and task failure; it carries no isolated zero statistic or defensive labels. Image-generation provenance is in the asset manifest.
