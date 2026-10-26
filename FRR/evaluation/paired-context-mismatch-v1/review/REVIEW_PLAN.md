# Prospective review plan

Written 2026-10-26 before any new main execution. This review concerns declared paired context mismatch, using predecessor NEXT_CONTACT.md and MATH_NOTE.md as context. Reviewer does not execute the main experiment or edit predecessor artifacts. Protocol read after its initial publication; implementation-specific preflight follows receipt of code.

## Analytic separation of targets

Write P_B=diag(0,I) for intended binding and d=12. Training examples are A=((c+delta*a),b)/sqrt(2) and N=((c-delta*a),-b)/sqrt(2), without subsequent normalization. Their half-difference is D=(delta*a,b)/sqrt(2). Common c cancels, while the declared unmatched context remains. The estimator is the top 12 left singular vectors of the uncentered 24-by-m difference matrix; supplied rank and pair labels are privileges.

For independent unit isotropic a and b, E[DD^T]=diag(delta^2 I,I)/(2d). Its top-rank-12 population eigenspace is binding for delta=.5, context for delta=1.5. The normalized population-to-binding distance is respectively 0 and 1. More samples may improve recovery of the population target while worsening intended binding recovery; finite prefixes need not improve monotonically.

For aligned a=b, E[DD^T]=[[delta^2 I,delta I],[delta I,I]]/(2d). Its rank-12 range is the graph span of (delta*b,b), with projector [[delta^2 I,delta I],[delta I,I]]/(1+delta^2). Given a full-rank binding prefix, m>=12 recovers that graph exactly up to roundoff. Its normalized distance to binding is delta/sqrt(1+delta^2), approximately .447214 for delta=.5 and .832050 for delta=1.5. This is deterministic structured contamination rather than sample noise.

Clean delta=0 has intended binding as its population target. Population projectors must be rotated by the same supplied dense real orthogonal Q as the representations. Population recovery, intended binding recovery, and task retrieval/status outcomes are separate measurements. Population target is an analytical diagnostic, not information available to the estimated arm. No result proves semantics, historical truth, learned rank selection, or broad agent reasoning.

## Preflight gates

- Exact predecessor evaluation/calibration arrays and dense Q are reused and hashed, without regeneration, alteration, train-bank contamination or evaluation-dependent design choices.
- New training a,b,c come from declared independent RNG streams, disjoint from the predecessor task factors; new master seeds 94101/94111/94121 spawn separate c,b,a streams; all five conditions share their 1024-vector base banks, with nested fitting prefixes m=12,48,192,768 and separate reporting-only validation contrasts 768:1024.
- Verify saved raw draws, normalized a,b,c, pairs and exact half-differences. Per-example renormalization is prohibited because it changes cancellation and population formulas.
- For aligned conditions use a=b exactly, not a correlated approximation. Clean controls retain delta=0. No undisclosed additive noise or centering.
- Fit uncentered differences after Q, retain exactly rank12, save singular values, cutoff gap and numerical rank; avoid deriving estimator from population/oracle geometry.
- Explicitly check row conventions: rotation xQ^T; projector action xP^T. Verify idempotence, Hermiticity, principal angles, and normalized Frobenius distance to both intended binding and analytic population.
- Calibration uses the fixed predecessor labeled calibration records and existing decoder policy. Training does not consume calibration labels, evaluation identities, gold status, or outcome metrics. Gold relevance is only a separate scoring diagnostic.
- Full and oracle controls should reproduce predecessor dense-Q outcomes, subject only to documented last-bit ranking effects. Repeated controls across train conditions or m are bookkeeping, not independent observations.
- Hash code, protocol and reviewer preflight before sole main attempt; write saved inputs before fitting/scoring, preserve attempts, and block outcome-dependent repairs or reruns without explicit provenance.

## Outcome review

Independently reconstruct metric rows and aggregates from saved artifacts without importing experiment functions. Recompute selected pair differences, SVD projectors, calibration centers, query scores, stable top3 retrieval and status outputs from arrays. Check 7680 paired rows, 23040 method rows, 720 aggregates, all IDs, returned-record metrics, U versus ABSTAIN, diagnostic-only oracle-relevant stance, training versus held-out contrast residuals, fixed 1e-10 zero/tie policies, full/oracle invariances, and actual task outcomes against both structural distances. No task conclusion follows solely from projector distance.

This contact reuses 48 underlying evaluation entity-time claims and 384 base query IDs; zero-noise repeats and duplicated controls remain non-independent. Results are descriptive for the declared deterministic generator, fixed seeds and prefixes. Distinguish zero-mean independent contamination (whose sample cross-block tends to zero, but whose block variance persists) from aligned persistent cross-block bias.
