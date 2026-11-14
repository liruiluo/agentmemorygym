# CAMP · 17-slide public research talk

Updated 2026-11-14. English, approximately 15 minutes.

Story: memory need → tool underuse → prior-mismatch hypothesis → research question → contributions → task environments → CAMP method → Q1 effectiveness → Q2 mechanism and complete case → Q3 transfer.

The roadmap follows the title. Background ends at the research question; the separate contribution overview comes next. Background shows only the context-only upper row of Figure 1. The environment page uses Figure 2’s right-hand panel with one memory demand per task family. The complete Figure 1 and its file-memory solution begin Method, while the frozen-model prior experiment belongs to the mechanism results. The technical Scrapy case closes Q2. A lightweight four-chapter trail marks progress before Results; each result page carries its Q1, Q2 or Q3 question above the exhibit while keeping a conclusion-led main title. There are no full-page chapter dividers, references or appendix tail.

| # | Chapter | Question | Role | Action title | Exhibit |
|---|---|---|---|---|---|
| 1 | Identity | — | Identity | Coding Agent Memory Post-training | Full title, authors, affiliation and links |
| 2 | Roadmap | — | Roadmap | The story in four questions | Four chapters and the questions they answer |
| 3 | Background | — | Memory need | Long tasks need memory beyond the active context | Figure 1 upper row: context lost → repeated work → unfinished task |
| 4 | Background | — | Research problem | Having memory tools does not ensure their use | Unused memory tools → lost constraint → failure; prior-mismatch hypothesis → question |
| 5 | Contributions | — | Contributions | Three contributions to learning reusable memory | Environment suite / learning method / empirical study |
| 6 | Environments | — | Task demands | CAMG: four kinds of long-horizon work | Figure 2 environment panel + what each task family must remember |
| 7 | Method | — | Core idea | Use files to carry working state beyond the context | Original Figure 1, both contrast rows |
| 8 | Method | — | Learning mechanism | Task reward trains both acting and remembering | Original Figure 2 + shared policy/reward/PPO callouts |
| 9 | Results & analysis | Q1 | Effectiveness | CAMG-RL reaches 54.4% average task success | Six-method main comparison |
| 10 | Results & analysis | Q1 | Effectiveness | Learned file memory beats a 262K-context reference | 262K-context practical reference |
| 11 | Results & analysis | Q2 | Prior evidence | The file interface is familiar before RL | Frozen-model file vs. dedicated-tool likelihood |
| 12 | Results & analysis | Q2 | Mechanism | Memory actions need the learning signal | Memory-action gradient and continuation ablations |
| 13 | Results & analysis | Q2 | Mechanism | The saved content changes what happens next | Blank/shuffled memory from the same state |
| 14 | Results & analysis | Q2 | Case study | Case study: carry a Scrapy fix across contexts | Scrapy saved note + read/check actions + successful finish |
| 15 | Results & analysis | Q3 | Transfer | The learned memory policy transfers across interfaces | New memory interfaces, fixed task executor |
| 16 | Results & analysis | Q3 | Transfer | Gains carry over to external benchmarks | Matched base vs. trained external results |
| 17 | Conclusion | — | Conclusion | Familiar operations. Learned memory. | Three takeaways and project link |

## Speaking and source notes

The contribution overview follows the paper’s actual suite / method / empirical-study structure. Figures 1 and 2 retain their original content; the conceptual comparison is not presented as a measured counterfactual. Results use unchanged source values and essential on-slide comparison conditions. Full provenance and scientific qualifications are in [speaker notes](speaker-notes.md) and [shared data](../data/research.json). Multi-run robustness, the CAMG-RL acquisition trajectory and the syntax-only probe remain optional Q&A material, not additional talk pages. The background shows unused memory tools, a lost constraint and task failure; it carries no isolated zero statistic or defensive labels. Image-generation provenance is in the asset manifest.
