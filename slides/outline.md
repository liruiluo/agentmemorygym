# CAMG public paper talk

Audience: ML and agent researchers. Language: English, matching the existing public project talks.
Duration: about 15 minutes, 15 slides. Source: arXiv:2609.34422v1 (28 September 2026),
as linked from the public project page. Ongoing experiments are outside this deck.

Main claim: RL on top of familiar coding-agent file operations can learn reusable
memory behavior for long-horizon tasks.

| # | Role | Action title / takeaway | Main exhibit | Source |
|---|---|---|---|---|
| 1 | Title | Coding Agent Memory Post-training | Full title, authors, JD.com, resource links | Paper p.1 |
| 2 | Motivation | Long tasks need state that outlives context | Teaser | Figure 1 |
| 3 | Question | Can RL unlock the memory prior in file operations? | Familiar actions → task-reward learning | Introduction |
| 4 | Environment | CAMG spans four native task worlds | Four task examples | Section 4; Figure 6 |
| 5 | System | One policy learns across all four environments | Full framework | Figure 2; Section 5 |
| 6 | Mechanism | Files carry reasoning across context boundaries | Act → write → read workflow | Section 5.1 |
| 7 | Learning | Downstream task reward trains the whole memory chain | Write → retrieve → use → reward | Section 5; Appendix B |
| 8 | Result | CAMG-RL achieves 54.4% average success | Six-method average-success chart | Table 2 |
| 9 | Result | The largest gains are in Coding and AutoResearch | CAMG-RL vs CompactionRL by environment | Table 2 |
| 10 | Analysis | File operations build on a measurable pre-training prior | Interface prior / acquired chains / policy shift | Figure 3 |
| 11 | Transfer | Learned memory transfers beyond the training Gym | SWE-bench Verified + MLE-bench Lite | Table 3 |
| 12 | Ablation | Memory-action credit and general files both matter | Four-component ablation | Figure 4 |
| 13 | Intervention | Changing saved memory content reduces later success | Blank / mismatched memory; paired success deltas | Appendix D.3; Figure 8 |
| 14 | Case | A coding episode makes the memory chain visible | Reproduce → patch → save → read/verify | Figure 5 (training trajectory) |
| 15 | Conclusion | Takeaways | Gym, learning method, matched transfer | Paper conclusion |

Design: SPHERE academic style (white, Arial, black short title, restrained blue/red).
Use JD.com as the affiliation mark; do not transfer PKU/BIGAI affiliation from the style reference.
Figures are the already-public project assets. Charts use the exact paper table values.
No appendix or References tail. Small paper section/table references stay on the relevant pages.

Validation: render every slide, inspect a contact sheet and dense pages, check text
overflow and authorship, verify every result against the public paper, then verify
desktop/mobile website links and the deployed PDF bytes.
