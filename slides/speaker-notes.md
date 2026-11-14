# CAMP V1 · 16-slide research talk

Updated 2026-11-14. Approximately 15 minutes. White academic house style; all exhibits are native editable objects. Results are loaded from `data/research.json`. November additions are author-reported revised-manuscript results, separately labelled from published September results.

## 01. Coding Agent Memory Post-training

**Source:** CAMP V1 · 14 November 2026 · arXiv:2609.34422

The thesis is that ordinary file operations offer a familiar starting point, and task reward teaches a shared policy to use those files as useful memory. This is CAMP V1: four environments and reinforcement learning. Blue-labelled November additions are author-reported revised-manuscript results, not already part of the September arXiv release.

## 02. What should survive a context boundary?

**Source:** Published · Figure 5 / Appendix A.4.3 · recorded training trajectory

Start with the real Scrapy episode. The agent has already edited scheduler.py. At round 18 it writes a continuation record. At round 19, after context replacement, it reads that record. The excerpts are shortened. Do not imply a measured failure of the same task without memory; that counterfactual was not run.

## 03. The file interface is familiar before RL

**Source:** Published · Figure 3a · frozen Qwen3.5-4B · rounded point estimates

Lower negative log-likelihood means these valid action tokens are more likely under the frozen model. The strongest contrast here is retrieval. This is evidence of interface familiarity, not proof of which pre-training corpus caused it. No uncertainty bars have been reconstructed.

## 04. One shared policy, four kinds of work

**Source:** CAMG environments · V1 suite · four domains

CAMG is the environment suite, CAMG-RL is the learning method, and fully asynchronous PPO is its system implementation. Native task semantics and grading remain with the environments. The final policy is shared, not four separately deployed environment policies. Do not substitute CAMP-II’s General/Visual domains.

## 05. Task reward trains both acting and remembering

**Source:** CAMG-RL method · ordinary file operations · fully asynchronous PPO

The policy samples task and file actions as part of one trajectory; a shell action can contain both. Native task rewards supply credit through PPO. The environment owns context-replacement timing and the mechanical reset. Before reset the policy writes the bounded continuation file, and after reset it gets only the path and reads it normally. There is no separate memory-writing reward and the reset has no policy token or optimizer row. Responses may include free-form reasoning; do not reintroduce the obsolete no-thinking claim.

## 06. CAMG-RL reaches 54.4% average task success

**Source:** Published · Table 2 · 4 × 128 held-out tasks · equal-weight environment average

All six original comparisons are visible. The same Qwen3.5-4B backbone reaches 54.4, compared with CompactionRL 48.0; paired 95% CI for the 6.4-point gap is 3.3 to 9.5. Shop is saturated and slightly favors CompactionRL; the largest improvements are Coding and AutoResearch. DeepResearch’s gap is not statistically significant. Displayed averages are from unrounded paper scores.

## 07. Fixing syntax does not eliminate the interface gap

**Source:** ADDITIONAL · November 2026 · Revised Appendix D.16 · author-reported

Frozen Qwen3.5-4B, no RL, the same 512 tasks. Both interfaces use generation-time grammar and argument-schema masks, without post-hoc repair. This is not a comparison of trained policies under an identical compaction mechanism. Constrained decoding gives AgeMem a larger boost, 6.6 points versus Bash 2.9. After both get masking, Bash remains at 20.3 versus AgeMem 16.0, a 4.3-point residual. Do not infer significance or an all-confounds-removed causal conclusion. These results are November additions, not already in the September arXiv release.

## 08. Training increases complete memory chains

**Source:** Published · Figure 3b · designated-interface metric · continuation writes excluded

Excludes mandatory continuation writes. This metric covers designated memory interfaces; it does not cover all native workspace use. CAMG-RL rises from 7.97% to 20.9% over its first and last training quarters. AgeMem’s designated six-tool chain rate is zero. This does not mean no memory use: the additional Coding-only analysis reports AgeMem workspace chains in 80.5% of episodes and CAMG-RL workspace chains in 20.3%. Do not mix those with these pooled training-quarter values.

## 09. The saved content changes what happens next

**Source:** Published · Appendix D.3 · same-state continuations · eligible tasks only

Forked continuations from the same post-reset state, within eligible tasks only. Shuffled donors are within-environment and length-matched. This is a local memory-content intervention, not a whole-distribution effect. Negative bars are percentage-point changes relative to intact files. The eligible counts are 128, 29, 60, and 23. Equal-environment mean losses are 14.1 for blank and 11.5 for shuffled memory. This is stronger local evidence than an uncontrolled correlation between writing and success, but not a population-wide treatment effect.

## 10. Memory actions need the learning signal

**Source:** Published · Figure 4 · average task success (%)

The no-gradient condition retains rewards, critic targets and critic learning. The two continuation conditions intervene at different stages. The four rows are distinct interventions. Full training reaches 54.4, no memory-action actor gradients reaches 21.1, restricting to continuation during both training and evaluation gives 41.8, and restricting only at evaluation gives 28.1.

## 11. The learned memory policy transfers across interfaces

**Source:** ADDITIONAL · November 2026 · Revised Appendix D.10 · author-reported

Task-execution policy stays frozen Qwen3.5-4B; only the memory-writing/reading policy changes. No further training. Sample counts, intervals and significance are not supplied. The gains are 11.4 points with Claude Code file tools and 6.4 with AgeMem memory tools. Only the memory-writing and reading policy changes. This is not a claim about changing the entire task actor, and no uncertainty or sample size should be invented.

## 12. Learned file memory beats a 262K-context reference

**Source:** ADDITIONAL · November 2026 · Revised Appendix D.14 · author-reported

Same base model, PPO, task rewards and 200-update budget. Context windows and compaction procedures differ. The long-context policy retains native task files but has no dedicated file-memory interface. This is a practical system comparison, not an isolated causal test of memory. The reference scores 49.2 average and CAMG-RL scores 54.4 with 30,720 active tokens, a 5.2-point advantage. Do not describe this as strict isolation of memory, because compaction and context settings differ. Do not claim a cost advantage without cost measurements.

## 13. The advantage persists across training runs

**Source:** Published · Appendix D.8

Five training runs per method. Error bars show SD, not confidence intervals. Individual run scores were not supplied. CAMG-RL averages 55.3 with SD 2.9, CompactionRL 47.1 with SD 3.5. The original 54.4 and 48.0 values are individual main-table runs, not the means. A separate model-family replication on the website trains Gemma 3 4B from 15.0 to 47.7; this is not zero-shot transfer of Qwen weights.

## 14. Gains carry over to external benchmarks

**Source:** Published · Table 3 · benchmark success (%) · no compute-equivalence claim

Benchmark success percentages. Larger frozen models are capability references, not compute-equivalent controls. These outcomes do not isolate a memory-only transfer effect. Focus on matched base-to-trained gains at each scale: SWE-bench Verified 7.6 to 15.8 for 4B and 14.8 to 27.6 for 9B; MLE-bench Lite 0.0 to 4.5 and 4.5 to 9.1. Larger frozen MoE models remain capability references, visible in the website’s full table.

## 15. The remembered state becomes the next action

**Source:** Published · Figure 5 / Appendix A.4.3 · shortened training-episode excerpts

An illustrative training episode, not a held-out comparison or a counterfactual failure without memory. Timeline: edit scheduler.py at round 12, write CONTINUATION.md at round 18, reset, read at round 19, later run test_spider.py and pytest tests/test_crawl.py -v, terminal round 30 within a 40-round budget with return 1.00 and hidden tests passed. Test commands are subsequent actions, not all asserted to occur at round 19.

## 16. Familiar operations. Learned memory.

**Source:** CAMP V1 · published paper + labelled November additions · data/research.json

Close with three scoped statements. Familiarity is measured before training. Task reward teaches useful memory behaviors, supported by acquisition, ablation and local content intervention. The benefits extend to external benchmarks and, in November additions, new memory interfaces. Do not claim universal causality or compute savings. Full experiment tables, protocol boundaries, source/version labels and editable slides are on the project page.

