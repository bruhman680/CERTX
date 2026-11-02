# arXiv scout for FRR (Claude, 2026-11-02) — curiosity notes for ChatGPT

Status: literature contact, not evidence about our toys. Seven pages were actually read (abstract level through the fetch tool, one HTML full-text page); search snippets were never used as evidence. Reading depth is stated per paper. Absence from my search is not absence from the literature. Standard-mode search only. Papers already scouted by Codex (arxiv-scout-v1 and later: 0710.3742, 2309.08911, 2404.15454, 2406.05937, 2503.10834, 2602.16313, 2603.25796, 2605.06527, 2607.27080, 2610.02070) were excluded on purpose.

Search roles used (by function, not vocabulary): shared error source (correlated errors), learning from failures (negative samples), outcomes that change the data (performative), emergence vs metric choice, named failure taxonomies. NOT yet searched: open-set/novelty recognition, causal identification from identical observational laws, misspecified-model inference, selective prediction/abstention. Unread: Huang et al. 2310.01798 (self-correction without external feedback; fetch was refused by the allowlist), so it is a lead only.

## Selected with most confidence (ranked by how much they could change our next move)

1. **The Surprising Effectiveness of Negative Reinforcement in LLM Reasoning** (Zhu, Xia, Wei, Chen, Chen, Meng; arXiv 2506.01347, v2 Oct 2025). Read: abstract-level page.
   Establishes (author-reported): training only on incorrect samples (NSR) improves over the base model across Pass@k up to k=256, often matching PPO/GRPO; positive-only training (PSR) improves Pass@1 but degrades high-k, which they attribute to lost diversity. Models: Qwen2.5-Math-7B, Qwen3-4B, Llama-3.1-8B-Instruct; math data. Mechanism claim from gradient analysis: NSR suppresses wrong generations and redistributes mass by the model's prior, "refining existing knowledge."
   Why for us: the closest published contact with "learns more from errors than successes," but it is a training-objective result on verifiable-reward math, not a claim about reasoning practice or claim discipline. It connects to my error-vs-success relay (rarity and horizon decide where evidence lives) and to the diversity point: positive-only updates can collapse the field.
   Does not capture: claims/assumptions made from failures; non-math tasks; anything beyond Pass@k; no variance in the abstract.
   Curiosity: does the NSR/PSR asymmetry track error rarity (as in my EC-vs-IND share table) or something else? A toy with a controllable pass rate could test this.

2. **Performative Prediction** (Perdomo, Zrnic, Mendler-Dünner, Hardt; arXiv 2002.06673). Read: abstract-level page.
   Establishes: when predictions drive decisions that change the outcome distribution, the right target is the distribution the model itself induces. Performative stability (optimal for the distribution it induces) and optimality are generally different. Repeated retraining converges linearly under smoothness, strong convexity and a sensitivity bound eps < gamma/beta (Wasserstein-1); otherwise it can oscillate or diverge.
   Why for us: the most direct formal home I found for "wake" (a changed field, not a remembering state). The distribution map D(theta) is the coupled system-environment representation in FRR v0.5. The convergence criterion is a concrete example of the Boundary/Order/Uniformity checks: retraining converges only when response sensitivity is small relative to curvature.
   Does not capture: discrete hidden-state worlds like WK; the assumptions (strong convexity, Lipschitz map) are restrictive and the map is typically unknown.
   Curiosity: write WK's soil update as a distribution map and compute whether the eps<gamma/beta analogue predicts when repeated correction oscillates in our toy.

3. **Partially Performative Prediction** (Lee, Zrnic; arXiv 2606.07890, 5 Jun 2026). Read: abstract-level plus assumptions from the PDF page.
   Establishes: distribution is a mixture (1-alpha_t) D(theta) + alpha_t P_t of an endogenous response and an exogenous shift; learners are scored by regret to time-varying stable/optimal points; bounds grow with path length; no lower bounds given.
   Why for us: separates "the field changed by my action" from "the field changed by something else," which is exactly the wake-vs-drift distinction that my open-world DRIFT world could not make with passive features. Single-source and very recent (near my training cutoff), so treat details as unverified until read in full.
   Curiosity: add a mixed WK+DRIFT world and see whether intervention-versus-sham arms recover alpha.

4. **Are Emergent Abilities of Large Language Models a Mirage?** (Schaeffer, Miranda, Koyejo; arXiv 2304.15004). Read: abstract-level page.
   Establishes: for fixed tasks and model families, apparent sharp emergence arises mainly from discontinuous or nonlinear metrics (exact match, multiple-choice grade; >92% of claimed BIG-Bench cases), small test sets, and sparse sampling; continuous metrics (token edit distance, Brier) show smooth gains; they also induce "emergence" in small vision models by choosing the metric. They explicitly do not claim LLMs cannot show emergent abilities; their per-token independence assumption is acknowledged false.
   Why for us: speaks to Thomas's point that a system with many parameters needs space for emergence, from the other side: what looks like emergence can be our scoring key. My claim-scored comparison scores correct/over/unresolved, an all-or-nothing rubric, which could manufacture cliffs. The free-play phase should log continuous quantities.
   Does not capture: emergence that survives a continuous metric.
   Curiosity: rescore my claim procedures with a proper score over claim distributions and see whether the apparent transitions with M (e.g. UNKNOWN rising from .13 to .99) are smooth.

5. **Why Do Multi-Agent LLM Systems Fail?** (Cemri et al.; arXiv 2503.13657, NeurIPS D&B 2025). Read: abstract-level page (last ~7,700 chars of the page unread).
   Establishes: taxonomy MAST, 14 failure modes in 3 categories (system design, inter-agent misalignment, task verification), built from 150 traces (human kappa .88), applied to 1,642 traces from 7 frameworks; LLM-judge annotation kappa .77; failure modes with similar symptoms correlate up to .63, so automated judges can conflate root causes; authors state it does not cover every failure pattern.
   Why for us: a published example of "named failure patterns" as method, with the same problem we keep meeting: symptoms do not identify the route, and a closed taxonomy made from a few traces is then applied at scale. Direct analogue of my UNKNOWN/closed-vocabulary finding and of error-lineage's route separation.
   Curiosity: map FRR's named patterns (shared source, repeated ancestry, stale cache, silent success, proxy drift) against MAST's categories on their public traces, and count where the two disagree.

6. **Correlated Errors in Large Language Models** (Kim, Garg, Peng, Garg; arXiv 2506.07962, Jun 2025). Read: full HTML page summary.
   Establishes: across 349 models (Open LLM Leaderboard, 12,032 MMLU items) and 71 models (HELM, 14,042 items), pairs agree on wrong answers far above their stated chance baseline (HELM about 60% vs about 1/3; HF .423 vs .127); same provider, architecture or size and higher accuracy raise correlation; LLM judges inflate accuracy of weaker, same-provider models. Their metric ignores probabilities and treats all wrong answers alike; multiple-choice only.
   Why for us: empirical context for the shared-soil worry in my group-vote relay (matched marginals and pairwise stats can still give opposite majority behaviour). Observational data cannot separate shared item difficulty from copying or a common source: in my toy, difficulty alone gives P(B wrong|A wrong) about .37 vs .23 independent with no copying (open_world_guard_output.txt, phase 1). Check how their chance baseline is built before comparing numbers.
   Does not capture: route (common cause vs copying) without intervention.

7. **Not All Negative Samples Are Equal: LLMs Learn Better from Plausible Reasoning** (Di et al.; arXiv 2602.03516, Feb 2026). Read: abstract-level page.
   Establishes (author-reported): negatives that look right but end wrong ("locally plausible, globally wrong") work better than easy negatives or judge-made ones; gains over RL are small on small benchmarks. My fetch summary noted that the Qwen-7B table averages differ by about 0.46 points (39.89 vs 39.43) while the abstract claims 2.03%; this is from a summary, not from my own reading of the table, so check it in the full text before citing the 2.03% number. Automated error-type annotation; ablations on one model only.
   Why for us: errors differ in how much they teach. Plausible-wrong is near the decision boundary, which matches the idea that information depends on what an error is compared with, not that it is an error.
   Possible same-line dependence with item 1 (not verified), so do not count them as two independent confirmations.

## What could change our next move
- Wake has a formal home (items 2-3). A small calculation could tell us whether our repeated-correction loops are in the convergent or oscillating regime.
- "Emergence" needs a continuous log before any all-or-nothing score (item 4).
- Our named-failure practice has a published sibling (item 5) with the same conflation risk; comparing taxonomies on shared traces is a cheap, falsifiable contact.
- Item 1 is the nearest external evidence for Thomas's thesis, and it is scoped: a training result on math, not a reasoning-practice result.

## Search state and gaps (for the next scout)
Reached clusters: error correlation, negative-sample RL, performative prediction, metric-induced emergence, MAS failure taxonomies. Gaps: open-set/novelty recognition; causal identification when observational laws coincide (intervention design); misspecified-model consistency (classical: Berk 1966, White 1982 — not fetched); selective prediction/abstention; self-correction without external feedback (2310.01798 not read). Repairs proposed in my relays (UNKNOWN claim, sham-calibrated guard, claim-scored scoring) have not yet had their own literature search.
