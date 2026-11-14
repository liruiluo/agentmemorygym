# CAMP · 16-slide public research talk

Updated 2026-11-14. English, approximately 15 minutes.

Story: why memory → why CAMP → contributions → task environments → learning method → effectiveness → mechanism → transfer → the case carried to completion.

The roadmap follows the title and leads directly into background. The technical Scrapy case appears once, after the results. A lightweight four-chapter trail marks progress; result pages also name the question they answer. There are no full-page chapter dividers, references or appendix tail.

| # | Chapter | Role | Action title | Exhibit |
|---|---|---|---|---|
| 1 | Opening / roadmap | Identity | Coding Agent Memory Post-training | Full title, authors, affiliation and links |
| 2 | Opening / roadmap | Roadmap | The story in four questions | Four chapters and the questions they answer |
| 3 | Background | Why CAMP | Why learn memory through familiar file operations? | Interface and training-setting gaps → research question |
| 4 | Background | Why files | The file interface is familiar before RL | Frozen-model file vs. dedicated-tool likelihood |
| 5 | Background | Core idea | Use files to carry working state beyond the context | Original Figure 1, both contrast rows |
| 6 | Background | Contributions | Three contributions to learning reusable memory | Environment suite / learning method / empirical study |
| 7 | Environments | Task demands | One shared policy, four kinds of work | Four task families and the state each must retain |
| 8 | Method | Learning mechanism | Task reward trains both acting and remembering | Original Figure 2 + shared policy/reward/PPO callouts |
| 9 | Results & analysis | Effectiveness | CAMG-RL reaches 54.4% average task success | Six-method main comparison |
| 10 | Results & analysis | Effectiveness | Learned file memory beats a 262K-context reference | 262K-context practical reference |
| 11 | Results & analysis | Mechanism | Memory actions need the learning signal | Memory-action gradient and continuation ablations |
| 12 | Results & analysis | Mechanism | The saved content changes what happens next | Blank/shuffled memory from the same state |
| 13 | Results & analysis | Transfer | The learned memory policy transfers across interfaces | New memory interfaces, fixed task executor |
| 14 | Results & analysis | Transfer | Gains carry over to external benchmarks | Matched base vs. trained external results |
| 15 | Results & analysis | Case study | Case study: carry a Scrapy fix across contexts | Scrapy saved note + read/check actions + successful finish |
| 16 | Opening / roadmap | Conclusion | Familiar operations. Learned memory. | Three takeaways and project link |

## Speaking and source notes

The contribution overview follows the paper’s actual suite / method / empirical-study structure. Figures 1 and 2 retain their original content; the conceptual comparison is not presented as a measured counterfactual. Results use unchanged source values and essential on-slide comparison conditions. Full provenance and scientific qualifications are in [speaker notes](speaker-notes.md) and [shared data](../data/research.json). Multi-run robustness, chain counts and the syntax-only probe are optional Q&A material, not additional talk pages.
