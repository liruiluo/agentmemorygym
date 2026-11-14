# CAMP · 16-slide research story

Updated 2026-11-14. Approximately 15 minutes (14.5 minutes of speaking plus transitions). White academic house style. Text, charts and case diagrams are editable; Figures 1 and 2 are faithful paper-figure pictures in PPTX and vector originals in PDF. Results come from `data/research.json`. Source-version boundaries below are speaker preparation, not slide labels.

## 01. Coding Agent Memory Post-training

**Chapter:** Opening / roadmap · **Role:** Identity · **Target:** 45 seconds

**Source:** CAMP V1 · 14 November 2026 · arXiv:2609.34422

The thesis is that ordinary file operations offer a familiar starting point, and task reward teaches a shared policy to use those files as useful memory. This is CAMP V1: four environments and reinforcement learning. Result provenance is retained in the notes and shared data; the spoken story is motivation, contributions, environments, learning and outcomes.

## 02. The story in four questions

**Chapter:** Opening / roadmap · **Role:** Roadmap · **Target:** 20 seconds

**Source:** Talk roadmap

Keep this to about twenty seconds. Background explains why this work is needed, not just why memory matters. Environments explain what makes the task suite demand memory. Method explains how ordinary file operations learn from task reward. Results answer effectiveness, mechanism and transfer. After the results, show a complete Scrapy case before closing.

## 03. Why learn memory through familiar file operations?

**Chapter:** Background · **Role:** Why CAMP · **Target:** 80 seconds

**Source:** Introduction · motivation and research question

Long tasks lose useful working state at context boundaries. The paper identifies two gaps in prior learned-memory work: it often introduces specialized memory tools and trains in domain-specific, relatively short-horizon settings. This is not a claim that all prior work has those limitations. CAMP asks whether task-reward RL can build on familiar file operations to learn memory across diverse long-horizon tasks. Coding agent describes the form of memory operations, not a restriction to programming tasks.

## 04. The file interface is familiar before RL

**Chapter:** Background · **Role:** Why files · **Target:** 50 seconds

**Source:** Published · Figure 3a · frozen Qwen3.5-4B · rounded point estimates

Lower negative log-likelihood means these valid action tokens are more likely under the frozen model. The strongest contrast here is retrieval. This is evidence of interface familiarity, not proof of which pre-training corpus caused it. No uncertainty bars have been reconstructed.

## 05. Use files to carry working state beyond the context

**Chapter:** Background · **Role:** Core idea · **Target:** 55 seconds

**Source:** Figure 1 · conceptual illustration

Read the original paper figure from top to bottom. The top row illustrates how relying on active context can lead to repeated work. The bottom row shows ordinary file writes and reads preserving working state. This figure is a conceptual explanation, not a measured matched failure/success pair. It retains both rows and every original label. Files are available throughout the episode, not only at reset.

## 06. Three contributions to learning reusable memory

**Chapter:** Background · **Role:** Contributions · **Target:** 25 seconds

**Source:** Introduction · three contributions

This is the actual three-part contribution structure of the paper. CAMG is the environment suite; CAMG-RL is the learning method; the empirical study establishes useful and reusable memory behavior. Fully asynchronous PPO is the implementation, not a claim to a new optimizer. This page is a twenty-to-thirty-second preview; the next pages explain each contribution.

## 07. One shared policy, four kinds of work

**Chapter:** Environments · **Role:** Task demands · **Target:** 55 seconds

**Source:** CAMG environments · V1 suite · four domains

CAMG is the environment suite, CAMG-RL is the learning method, and fully asynchronous PPO is its system implementation. Native task semantics and grading remain with the environments. The final policy is shared, not four separately deployed environment policies. Do not substitute CAMP-II’s General/Visual domains.

## 08. Task reward trains both acting and remembering

**Chapter:** Method · **Role:** Learning mechanism · **Target:** 85 seconds

**Source:** Figure 2 · CAMG-RL · fully asynchronous PPO

Start at the shared CAMG-RL policy, follow ordinary task/file actions into the four environments, then trace task reward through the episode queue and PPO learner back to the weights. Rollout and learning proceed concurrently. A shell action may combine task and file operations. The environment owns context-replacement timing; the policy writes a bounded continuation file before reset, gets its path after reset, and reads it normally. Reset is not a policy action. No separate memory-writing reward is added. Free-form reasoning is permitted.

## 09. CAMG-RL reaches 54.4% average task success

**Chapter:** Results & analysis · **Role:** Effectiveness · **Target:** 60 seconds

**Source:** Published · Table 2 · 4 × 128 held-out tasks · equal-weight environment average

All six original comparisons are visible. The same Qwen3.5-4B backbone reaches 54.4, compared with CompactionRL 48.0; paired 95% CI for the 6.4-point gap is 3.3 to 9.5. Shop is saturated and slightly favors CompactionRL; the largest improvements are Coding and AutoResearch. DeepResearch’s gap is not statistically significant. Displayed averages are from unrounded paper scores.

## 10. Learned file memory beats a 262K-context reference

**Chapter:** Results & analysis · **Role:** Effectiveness · **Target:** 45 seconds

**Source:** ADDITIONAL · November 2026 · Revised Appendix D.14 · author-reported

Same base model, PPO, task rewards and 200-update budget. Context windows and compaction procedures differ. The long-context policy retains native task files but has no dedicated file-memory interface. This is a practical system comparison, not an isolated causal test of memory. The reference scores 49.2 average and CAMG-RL scores 54.4 with 30,720 active tokens, a 5.2-point advantage. Do not describe this as strict isolation of memory, because compaction and context settings differ. Do not claim a cost advantage without cost measurements.

## 11. Memory actions need the learning signal

**Chapter:** Results & analysis · **Role:** Mechanism · **Target:** 55 seconds

**Source:** Published · Figure 4 · average task success (%)

The no-gradient condition retains rewards, critic targets and critic learning. The two continuation conditions intervene at different stages. The four rows are distinct interventions. Full training reaches 54.4, no memory-action actor gradients reaches 21.1, restricting to continuation during both training and evaluation gives 41.8, and restricting only at evaluation gives 28.1.

## 12. The saved content changes what happens next

**Chapter:** Results & analysis · **Role:** Mechanism · **Target:** 60 seconds

**Source:** Published · Appendix D.3 · same-state continuations · eligible tasks only

Forked continuations from the same post-reset state, within eligible tasks only. Shuffled donors are within-environment and length-matched. This is a local memory-content intervention, not a whole-distribution effect. Negative bars are percentage-point changes relative to intact files. The eligible counts are 128, 29, 60, and 23. Equal-environment mean losses are 14.1 for blank and 11.5 for shuffled memory. This is stronger local evidence than an uncontrolled correlation between writing and success, but not a population-wide treatment effect.

## 13. The learned memory policy transfers across interfaces

**Chapter:** Results & analysis · **Role:** Transfer · **Target:** 60 seconds

**Source:** ADDITIONAL · November 2026 · Revised Appendix D.10 · author-reported

Task-execution policy stays frozen Qwen3.5-4B; only the memory-writing/reading policy changes. No further training. Sample counts, intervals and significance are not supplied. The gains are 11.4 points with Claude Code file tools and 6.4 with AgeMem memory tools. Only the memory-writing and reading policy changes. This is not a claim about changing the entire task actor, and no uncertainty or sample size should be invented.

## 14. Gains carry over to external benchmarks

**Chapter:** Results & analysis · **Role:** Transfer · **Target:** 50 seconds

**Source:** Published · Table 3 · benchmark success (%) · no compute-equivalence claim

Benchmark success percentages. Larger frozen models are capability references, not compute-equivalent controls. These outcomes do not isolate a memory-only transfer effect. Focus on matched base-to-trained gains at each scale: SWE-bench Verified 7.6 to 15.8 for 4B and 14.8 to 27.6 for 9B; MLE-bench Lite 0.0 to 4.5 and 4.5 to 9.1. Larger frozen MoE models remain capability references in the paper; this slide shows only matched base-to-trained comparisons.

## 15. Case study: carry a Scrapy fix across contexts

**Chapter:** Results & analysis · **Role:** Case study · **Target:** 85 seconds

**Source:** Figure 5 / Appendix A.4.3 · recorded training episode · shortened excerpts

An illustrative training episode, not a held-out comparison or a counterfactual failure without memory. Introduce the case here, after the audience knows the problem and method. Task: fix response logging in Scrapy. At round 12 the agent edits scheduler.py; at round 18 it saves the diagnosis and next steps to CONTINUATION.md. After context replacement it reads the file at round 19, then performs subsequent checks and finishes at round 30 within a 40-round budget. The tests are later actions, not all at round 19. Hidden tests passed; terminal return is 1.00. The excerpts are shortened. No matched no-memory failure is claimed.

## 16. Familiar operations. Learned memory.

**Chapter:** Opening / roadmap · **Role:** Conclusion · **Target:** 40 seconds

**Source:** CAMP V1 · published paper + labelled November additions · data/research.json

Close with three scoped statements. Familiarity is measured before training. Task reward teaches useful memory behaviors, supported by acquisition, ablation and local content intervention. The benefits extend to external benchmarks and, in November additions, new memory interfaces. Do not claim universal causality or compute savings. The project page links the paper, code and slides. Detailed protocol and source-version boundaries stay in these speaker notes and shared data, not the audience-facing story.

## Additional Q&A material (not extra slides)

The shared data also retains the designated-interface acquisition metric (7.97% to 20.9%), the syntax-constrained frozen-model comparison (Bash 20.3% vs. AgeMem 16.0%), and five-run robustness (CAMG-RL 55.3 ± 2.9 vs. CompactionRL 47.1 ± 3.5, mean ± SD). These are omitted from the main talk to preserve the motivation → method → effectiveness → mechanism → transfer story. Refer to each experiment’s own protocol before using these numbers.
