# CAMP · 17-slide research story

Updated 2026-11-14. Approximately 15 minutes (14.5 minutes of speaking plus transitions). White academic house style. Small chapter navigation and experimental questions sit above each chapter page’s larger title; a concise comparison/intervention line introduces each experimental plot. Text, charts and case diagrams are editable. The Figure 1 context crop, Figure 2 environment crop and the two full paper figures are pictures in PPTX and original vectors in PDF. The memory-underuse visual is a GPT-image-2 raster asset. Results come from `data/research.json`. Source-version boundaries below are speaker preparation, not slide labels.

## 01. Coding Agent Memory Post-training

**Chapter:** Identity · **Role:** Identity · **Target:** 35 seconds

**Source:** CAMP V1 · 14 November 2026 · arXiv:2609.34422

The thesis is that ordinary file operations offer a familiar starting point, and task reward teaches a shared policy to use those files as useful memory. This is CAMP V1: four environments and reinforcement learning. Result provenance is retained in the notes and shared data; the spoken story is motivation, contributions, environments, learning and outcomes.

## 02. The story in four questions

**Chapter:** Roadmap · **Role:** Roadmap · **Target:** 20 seconds

**Source:** Talk roadmap

Keep this to about twenty seconds. Background explains memory need, tool underuse and the prior-mismatch hypothesis, then ends at the research question. It does not explain the proposed solution. Environments explain what makes the task suite demand memory. Method explains how ordinary file operations learn from task reward. Results answer three questions: Q1, does CAMP improve long-horizon task performance; Q2, why does it work; Q3, does the learned memory behavior generalize. Close Q2 with the complete Scrapy case, then show transfer.

## 03. Long tasks need memory beyond the active context

**Chapter:** Background · **Role:** Memory need · **Target:** 45 seconds

**Source:** Figure 1 · upper context-only row

Long-horizon tasks accumulate constraints, evidence and decisions that later actions still depend on. Follow the top row of Figure 1: the agent makes progress, earlier working state leaves the active context, work is repeated and the task remains unfinished. The upper row is cropped directly from the original figure. The complete figure, including the file-memory solution, appears in Method.

## 04. Having memory tools does not ensure their use

**Chapter:** Background · **Role:** Research problem · **Target:** 80 seconds

**Source:** AgeMem (ACL 2026) · CAMP Figure 3b and interface-prior analysis

Walk through the budget example: the agent sees a $50 limit, proceeds without calling the available memory tools, loses the constraint as context moves on, and places an $80 order. The image was generated with GPT-image-2; generation provenance is in slides/illustration-assets.json. AgeMem exposes ADD, UPDATE, DELETE, RETRIEVE, SUMMARY and FILTER (Yu et al., ACL 2026, https://aclanthology.org/2026.acl-long.981/). In the CAMP AgeMem-tool arm, 53 of 261,941 policy responses attempt the dedicated tools and complete designated store–retrieve–use chains are zero in the first and last quarters. These observations concern the compared dedicated interface; native workspace use is separate. Our hypothesis is that post-training memory actions are poorly aligned with the pre-trained behavioral prior. End at the research question; the mechanism and supporting experiment follow later.

## 05. Three contributions to learning reusable memory

**Chapter:** Contributions · **Role:** Contributions · **Target:** 25 seconds

**Source:** Introduction · three contributions

This is the actual three-part contribution structure of the paper. CAMG is the environment suite; CAMG-RL is the learning method; the empirical study establishes useful and reusable memory behavior. Fully asynchronous PPO is the implementation, not a claim to a new optimizer. This page is a twenty-to-thirty-second preview; the next pages explain each contribution.

## 06. CAMG: four kinds of long-horizon work

**Chapter:** Environments · **Role:** Task demands · **Target:** 50 seconds

**Source:** CAMG environments · Figure 2 right-hand panel

Introduce the four task families with the environment panel from Figure 2. Shop requires remembering user preferences and purchase history across linked sessions. Coding requires carrying forward diagnosis, code changes and test progress. DeepResearch requires retaining sources and intermediate findings. AutoResearch requires tracking hypotheses, experimental trials and their results. The common demand is that later decisions depend on information gathered earlier. The suite supports learning and evaluating memory use across these different tasks. Keep the policy, rollout and PPO explanation for the full Figure 2 in Method.

## 07. Use files to carry working state beyond the context

**Chapter:** Method · **Role:** Core idea · **Target:** 60 seconds

**Source:** Figure 1 · conceptual illustration

Read the original paper figure from top to bottom. This is now the first method page, after the environment suite. The top row illustrates how relying on active context can lead to repeated work. The bottom row shows ordinary file writes and reads preserving working state. This figure is a conceptual explanation, not a measured matched failure/success pair. It retains both rows and every original label. Files are available throughout the episode, not only at reset.

## 08. Task reward trains both acting and remembering

**Chapter:** Method · **Role:** Learning mechanism · **Target:** 75 seconds

**Source:** Figure 2 · CAMG-RL · fully asynchronous PPO

Start at the shared CAMG-RL policy, follow ordinary task/file actions into the four environments, then trace task reward through the episode queue and PPO learner back to the weights. Rollout and learning proceed concurrently. A shell action may combine task and file operations. The environment owns context-replacement timing; the policy writes a bounded continuation file before reset, gets its path after reset, and reads it normally. Reset is not a policy action. No separate memory-writing reward is added. Free-form reasoning is permitted.

## 09. CAMG-RL reaches 54.4% average task success

**Chapter:** Results & analysis · **Role:** Effectiveness · **Target:** 60 seconds

**Source:** Published · Table 2 · 4 × 128 held-out tasks · equal-weight environment average

**Experimental question:** Q1 · Does CAMP improve long-horizon task performance?

Comparison / intervention: Compare six approaches with Qwen3.5-4B on the same held-out tasks.

All six original comparisons are visible. The same Qwen3.5-4B backbone reaches 54.4, compared with CompactionRL 48.0; paired 95% CI for the 6.4-point gap is 3.3 to 9.5. Shop is saturated and slightly favors CompactionRL; the largest improvements are Coding and AutoResearch. DeepResearch’s gap is not statistically significant. Displayed averages are from unrounded paper scores.

## 10. Learned file memory beats a 262K-context reference

**Chapter:** Results & analysis · **Role:** Effectiveness · **Target:** 40 seconds

**Source:** ADDITIONAL · November 2026 · Revised Appendix D.14 · author-reported

**Experimental question:** Q1 · Does CAMP improve long-horizon task performance?

Comparison / intervention: Same base, PPO, task rewards and 200 updates; context and compaction differ.

Same base model, PPO, task rewards and 200-update budget. Context windows and compaction procedures differ. The long-context policy retains native task files but has no dedicated file-memory interface. This is a practical system comparison, not an isolated causal test of memory. The reference scores 49.2 average and CAMG-RL scores 54.4 with 30,720 active tokens, a 5.2-point advantage. Do not describe this as strict isolation of memory, because compaction and context settings differ. Do not claim a cost advantage without cost measurements.

## 11. The file interface is familiar before RL

**Chapter:** Results & analysis · **Role:** Prior evidence · **Target:** 50 seconds

**Source:** Published · Figure 3a · frozen Qwen3.5-4B · rounded point estimates

**Experimental question:** Q2 · Why does CAMP work?

Comparison / intervention: Score file and dedicated-tool memory actions with frozen Qwen3.5-4B.

Lower negative log-likelihood means these valid action tokens are more likely under the frozen model. The strongest contrast here is retrieval. This is evidence of interface familiarity, not proof of which pre-training corpus caused it. No uncertainty bars have been reconstructed.

## 12. Memory actions need the learning signal

**Chapter:** Results & analysis · **Role:** Mechanism · **Target:** 50 seconds

**Source:** Published · Figure 4 · average task success (%)

**Experimental question:** Q2 · Why does CAMP work?

Comparison / intervention: Remove memory-action actor gradients (keep rewards/critic), or use only CONTINUATION.md.

The no-gradient condition retains rewards, critic targets and critic learning. The two continuation conditions intervene at different stages. The four rows are distinct interventions. Full training reaches 54.4, no memory-action actor gradients reaches 21.1, restricting to continuation during both training and evaluation gives 41.8, and restricting only at evaluation gives 28.1.

## 13. The saved content changes what happens next

**Chapter:** Results & analysis · **Role:** Mechanism · **Target:** 55 seconds

**Source:** Published · Appendix D.3 · same-state continuations · eligible tasks only

**Experimental question:** Q2 · Why does CAMP work?

Comparison / intervention: Resume from the same post-reset state with intact, blank or shuffled memory.

Forked continuations from the same post-reset state, within eligible tasks only. Shuffled donors are within-environment and length-matched. This is a local memory-content intervention, not a whole-distribution effect. Negative bars are percentage-point changes relative to intact files. The eligible counts are 128, 29, 60, and 23. Equal-environment mean losses are 14.1 for blank and 11.5 for shuffled memory. This is stronger local evidence than an uncontrolled correlation between writing and success, but not a population-wide treatment effect.

## 14. Case study: carry a Scrapy fix across contexts

**Chapter:** Results & analysis · **Role:** Case study · **Target:** 80 seconds

**Source:** Figure 5 / Appendix A.4.3 · recorded training episode · shortened excerpts

**Experimental question:** Q2 · Why does CAMP work?

An illustrative training episode, not a held-out comparison or a counterfactual failure without memory. Use this case to close Q2: show the memory behavior behind the preceding mechanism results, then turn to Q3 and generalization. Task: fix response logging in Scrapy. At round 12 the agent edits scheduler.py; at round 18 it saves the diagnosis and next steps to CONTINUATION.md. After context replacement it reads the file at round 19, then performs subsequent checks and finishes at round 30 within a 40-round budget. The tests are later actions, not all at round 19. Hidden tests passed; terminal return is 1.00. The excerpts are shortened. No matched no-memory failure is claimed.

## 15. The learned memory policy transfers across interfaces

**Chapter:** Results & analysis · **Role:** Transfer · **Target:** 55 seconds

**Source:** ADDITIONAL · November 2026 · Revised Appendix D.10 · author-reported

**Experimental question:** Q3 · Does the learned memory behavior generalize?

Comparison / intervention: Keep the task executor fixed; replace only the memory policy, with no further training.

Task-execution policy stays frozen Qwen3.5-4B; only the memory-writing/reading policy changes. No further training. Sample counts, intervals and significance are not supplied. The gains are 11.4 points with Claude Code file tools and 6.4 with AgeMem memory tools. Only the memory-writing and reading policy changes. This is not a claim about changing the entire task actor, and no uncertainty or sample size should be invented.

## 16. Gains carry over to external benchmarks

**Chapter:** Results & analysis · **Role:** Transfer · **Target:** 50 seconds

**Source:** Published · Table 3 · benchmark success (%) · no compute-equivalence claim

**Experimental question:** Q3 · Does the learned memory behavior generalize?

Comparison / intervention: Compare frozen base and trained policies at the same 4B and 9B model scales.

Benchmark success percentages. Larger frozen models are capability references, not compute-equivalent controls. These outcomes do not isolate a memory-only transfer effect. Focus on matched base-to-trained gains at each scale: SWE-bench Verified 7.6 to 15.8 for 4B and 14.8 to 27.6 for 9B; MLE-bench Lite 0.0 to 4.5 and 4.5 to 9.1. Larger frozen MoE models remain capability references in the paper; this slide shows only matched base-to-trained comparisons.

## 17. Takeaways

**Chapter:** Conclusion · **Role:** Conclusion · **Target:** 40 seconds

**Source:** CAMP V1 · published paper + labelled November additions · data/research.json

Close with three scoped statements. Familiarity is measured before training. Task reward teaches useful memory behaviors, supported by acquisition, ablation and local content intervention. The benefits extend to external benchmarks and, in November additions, new memory interfaces. Do not claim universal causality or compute savings. The project page links the paper, code and slides. Detailed protocol and source-version boundaries stay in these speaker notes and shared data, not the audience-facing story.

## Additional Q&A material (not extra slides)

The Background uses the Figure 1 context-only row and a visual failure story to motivate the problem. The AgeMem arm’s zero designated memory-chain observation remains supporting material for questions, not an on-slide statistic. The shared data also retains the CAMG-RL acquisition trajectory (7.97% to 20.9%), the syntax-constrained frozen-model comparison (Bash 20.3% vs. AgeMem 16.0%), and five-run robustness (CAMG-RL 55.3 ± 2.9 vs. CompactionRL 47.1 ± 3.5, mean ± SD). These are omitted from the main talk to preserve the motivation → method → effectiveness → mechanism → transfer story. Refer to each experiment’s own protocol before using these numbers.
