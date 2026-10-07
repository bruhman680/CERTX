# Continuity 03 — Projection, memory, and lumpability repair

**Inspected:** NOW/TASKS; recovered FRR v0.5 compact seed, Faithful Compression Pass, prediction/memory/intervention branching and search roles; FRR_FIBER_MEASUREMENT_PASS.md; handoff/history keyword contact. The measurement pass is explicitly a proposed design containing reported toy results: I did not execute its sandbox or independently verify those results. No language sufficiency result is established here.

## Surviving relationship and a needed qualification

A many-to-one description can erase a distinction that matters to a specified continuation. FRR correctly allows several repairs: refine state, retain history, change dynamics class, restrict target or horizon. The fiber pass improves the contract by separating present grouping A from future observation O. Its fixed-target defect d(A,O,t) decreases under refinement of A; changing O simultaneously changes the question. A tuple of channel adequacy scores also differs from a joint tuple of observations, so zero marginal defects need not guarantee joint closure.

Repair FRR's sentence “if they agree locally but diverge over longer histories, coarse-graining may have created non-Markovian memory” with an explicit quantifier. For a finite time-homogeneous Markov chain and hard partition, equality of projected one-step transition rows for **every pair in every fiber** is strong lumpability and guarantees a Markov projected process at all horizons and for every initial law. Consequently, later divergence cannot coexist with that exact universal condition. Local agreement might instead mean one preparation, stationary averaging, a selected set of pairs, or a different target observable. Those weaker statements permit later history dependence. Distinguish these before claiming projection-created memory.

## Concrete repair: residual to guarantee

Let X be finite microstates, S macrostates, q:X→S, Q the corresponding deterministic stochastic matrix, P:X→Δ(X), and K:S→Δ(S). For each fiber choose a representative x_s and set K(s,·)=(PQ)(x_s,·). Define ε=max_x TV((PQ)(x,·), K(q(x),·)). The row-pair one-step defect bounds this ε. These are explicitly predictive maps; no action lifting is supplied.

The square P then Q versus Q then K has ε row defect. Conditional on any projected history, the true next macro law is a mixture of the relevant PQ rows and remains within ε of K. Coupling/telescoping therefore bounds length-T visible-path total variation by min(1,Tε), when both processes share the same initial projected law. This is a finite-horizon guarantee, not uniform all-time faithfulness. If K additionally has Dobrushin coefficient ρ<1, macro **marginal** error is bounded by ε(1−ρ^T)/(1−ρ); that improvement does not automatically bound full-path error. For fixed external target O, a small d(A,O,1) alone supplies neither a closed macro transition K nor a long-horizon guarantee.

Recommended implementation: store the tuple (P,q,O,initial-law class,action family,T,ε,error metric), row witnesses and the chosen K with each toy claim. Report exact versus approximate versus preparation-specific closure separately. Add a demonstrator where ε is small but Tε becomes consequential; retain full path and one-time marginal results side by side. Recommendation only, no implementation or fresh numerical run in this report. A square is sufficient; a third operation adds no present evidential benefit.

## Memory placement and serious rival

History-enriched prediction can improve because history identifies a latent present state or an altered environment; improvement alone does not locate a memory mechanism. A serious rival is a hidden-state Markov model with a fixed transition law, competing against a finite-order macro model and an environment-augmented state. Compare held-out continuation likelihood/error, complexity, and reset behavior rather than calling each gain “memory.” Reset the focal state and field independently when feasible. For control, repeat closure across a declared family P^a and admissible intervention liftings; passive closure grants no such result.

For CERTX, cross truth with specificity and hold out subjects as the fiber pass proposes. Then compare F-only prediction against F plus claim path, verified references, and simple entity-count baselines. A path advantage may repair the observable while leaving internal LLM memory unidentified. Equal aggregate fiber values do not establish equal interventions or equally healthy channels. Preserve the exploratory three-fiber idea as a task-relative candidate rather than forcing a fourth channel or a universal pooled scale.

## Source weave and limits

Inherited mathematical lineage, **not newly inspected primary literature**: finite-chain lumpability is associated with Kemeny–Snell; projection-based effective equations with Mori–Zwanzig; approximate aggregation with perturbation and coupling bounds. These are different objects: a partitioned stochastic chain, an operator-projected dynamics with memory/orthogonal terms, and an approximation guarantee. Their shared silhouette does not prove shared mechanism. The coupling bounds above are supplied as explicit mathematical reasoning, not attributed to an unverified paper.

One bounded primary-source attempt used DOI https://doi.org/10.1063/1.1703791 (Zwanzig, 1961, projection/memory lineage); access returned HTTP 403 and no primary text was inspected. An earlier malformed exploratory URL also failed and supplied no evidence. Gaps: exact primary-source statement/hypotheses, weak-lumpability genealogy, practical memory-kernel estimation and error control, and intervention-specific aggregation. Do not describe the inherited names as fresh source confirmation or independent empirical evidence.

NOW's optimizer amendment is acknowledged but outside this report's claim: fixed β1=.9, β2=.999 has the finite envelope recorded in experiments-01, approximately 52.857, rather than a unit bound or an unrestricted “unbounded” claim.
