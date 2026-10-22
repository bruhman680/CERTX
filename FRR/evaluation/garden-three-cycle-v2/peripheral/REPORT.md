# Peripheral contact: missing outcomes and decisions under partial identification

Two primary contacts from established econometrics, found with two search queries. Selected methods/assumptions were read, not only abstracts. These contacts inform an authored toy decision design; they do not establish real-agent memory performance, a preferred universal loss, or superiority of FRR. Both sources are Manski's work and share a lineage; they are not independent corroboration.

## Source contacts

[Manski2007, Minimax-regret treatment choice with missing outcome data](https://www.its.caltech.edu/~mshum/reading/manskiminimax.pdf). Read introduction, definitions, missing-data mixture equation, Proposition1 and proof, and finite-sample assumptions through Proposition2. Observable outcome distributions and observability fractions do not determine missing outcomes. Bounded welfare yields feasible mean ranges; dominance and minimax-regret choice are separate. Its population-diversification setting permits randomized treatment assignments, and its conclusions depend on the explicitly chosen welfare and regret criterion. The finite-sample result has additional restrictive sampling/observability assumptions.

[Manski, Identification and Statistical Decision Theory, arXiv2204.11318v2](https://arxiv.org/pdf/2204.11318v2). Read introduction and sections2–5 through binary-action formulation. The PDF header says draft August2023; arXiv metadata records v2 uploaded21March2024. It separates knowledge of an observation law from finite samples and separates learning a state from selecting actions. Randomization can improve some ambiguity criteria without adding state information. This does not mean that more data are useless, that all criteria favor randomization, or that a confidence set can simply replace the full state space in finite-sample risk claims.

## Transfer candidates — our inferences

1. **Unknown is not zero.** For binary survival S and readability G, preserve separate probabilities of readable1, readable0 and missing. If selection depends on S, an observed conditional mean is not necessarily the latent survival rate. An identified interval can be the warranted output rather than a failed estimate.
2. **A decision may be stable while the mechanism remains ambiguous.** Evaluate an action across every compatible state. If the same action wins throughout, exact hidden-state allocation may be unnecessary for that scoped action. If actions disagree, report that distinction instead of forcing a mechanism story.
3. **Costs and objectives belong in the contract.** Minimax loss, minimax regret and subjective expected loss can choose different actions. They express a chosen decision problem, not competing discoveries about which world is true.
4. **A witness can be informative without being worth using.** Count inspection cost and side effects alongside any benefit. The source contact motivates explicit decision accounting; it does not prove a universal value-of-information result for destructive or biased probes.
5. **Keep identification and sampling uncertainty distinct.** Repeating the same observation process can reduce sampling noise while leaving a feasible population interval unchanged. Different observation access or credible assumptions may change the interval; neither is automatically free or valid.

## Small decision model proposed to coordinator

Let latent survival probability v lie in[L,U], keeping an artifact have expected loss1−v, and a safe rebuild have fixed loss c∈[0,1]. The latter assumes rebuilding succeeds and its entire relevant cost is c. With k=1−c, keep dominates when L≥k and rebuild dominates when U≤k. If L<k<U, define A=k−L and B=U−k. Choosing rebuild with probability A/(A+B) balances endpoint regrets and gives worst regret AB/(A+B); a deterministic choice achieves min(A,B). These are direct algebraic consequences of this authored loss, not a reproduction of the papers' empirical settings.

This model is useful because it can retain unresolved state information and still make an explicitly qualified action choice. It must not quietly substitute action confidence for confidence in the causal/memory explanation. A decision that is useful under one cost or feasible-state interval can change when those inputs change. Any fresh Cycle2 implementation should freeze its exact actions, losses, costs, grid and checks before execution.

## Access and scope limits

The2007 PDF is the primary article hosted by a university reading page; no code, proof formalization or dataset was reproduced. An initial arXiv HTML request for2204.11318v1 returned404; the PDF and metadata were then read successfully. Secondary search results located sources only. No third source, install, provider call, experiment, global-navigation edit or GitHub publication was performed by this scout.
