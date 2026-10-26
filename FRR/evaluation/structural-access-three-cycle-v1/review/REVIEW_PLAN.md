# Prospective reviewer plan

Reviewed 2026-10-26 before implementation outcomes. Scope is the new SA protocol; predecessor NEXT_CONTACT.md and REPORT.md provide context only. No predecessor artifact is edited. No main experiment is executed by reviewer.

## Design assessment

The declared real 24x24 orthogonal Q acts complex-linearly on 24 complex coordinates. It preserves the entire Hermitian inner product, including its imaginary part. With column vectors, P'=QPQ^T correctly transports the supplied binding projection. The identity, dense rotation and one-plane rotation address different degrees of coordinate dependence; unchanged P is an intentionally mismatched structural assumption. These are algebraic controls, not learned semantics or agent benefit.

The estimated arm has privileged ordered A/N pairs, an external training bank and a supplied target rank d=12. The uncentered difference matrix isolates binding only for the specific SCOPED paired generator with equal context and opposite phases. For noisy training, the estimated projector can be complex Hermitian. m=4 cannot span the full rank-12 oracle projector under this estimator; a task score from its smaller span does not establish full recovery. m=12/48 with no training noise should span the supplied subspace almost surely, subject to saved singular values. No experiment outcome may choose rank, training prefix, seed or noise.

Calibration status labels and entity/time matches are supervised information separate from evaluation. Evaluation identities/statuses may be used only by scoring, including the explicitly diagnostic oracle-relevant metric. U and decoder ABSTAIN must remain distinct; resultants cannot be called calibrated probability.

## Implementation gates

- Check disjoint deterministic RNG streams, fixed seeds, dimensions, counts, nesting and shared base noise. Training bank must not use calibration/evaluation factors. Save raw noise, noisy examples and Q.
- Check row/column conventions carefully: row z'=z Q^T; a complex Hermitian projector acts on rows as z P^T. Using z P instead silently conjugates the intended subspace. Validate Hermiticity/idempotence and estimated transport Q Phat_identity Q^T.
- Check SVD on uncentered difference columns, retaining min(m,d) left singular vectors. Training noise is independent per member and added before Q without subsequent normalization.
- Check zero projected norms, zero products, unavailable centres and angular ties against fixed 1e-10 policy. Stable ranking handles exact ties; near ties remain visible without forced equalization.
- Check actual returned IDs/predictions determine all retrieval/joint metrics. The conditional stance metric remains labeled conditional and separate.
- Check full/oracle product and norm identities, independently calculated real A+iB, and projected algebra before comparing ranks. Set/order/prediction mismatches from last-bit ties or thresholds remain in logs.
- Check source/protocol/reviewer hashes frozen before sole main execution and inputs/hashes written before scoring. No result-dependent repairs or reruns without explicit provenance.

## Outcome audit

Reviewer will independently reconstruct all ledger metrics and aggregates without importing experiment functions; selected saved-array reconstruction may be divided with a fresh auditor. Inspect counts, hashes/reuse, centres, singular spectra, rank, principal cosines and projector distance. Compare full/oracle task outcomes across rotations, and estimated transport separately from oracle recovery. Assess whether naive fixed-mask failure actually occurs, and retain counterexamples or equality rather than assuming its outcome.

The 6,912 paired rows/27,648 method records reuse 48 latent evaluation claims and 384 base query IDs, with zero-noise repetitions and duplicated nonestimated arms. They support descriptive generator claims only; no significance or population inference. Generalization to language, learned semantic decompositions, retrieval infrastructure or agents remains untested.

## Communication

Reviewer warned root about general real 96-dimensional rotations versus complex-linear Q before protocol finalization. Final protocol uses real 24-dimensional Q consistently. Reviewer sent engineer row-action conventions for complex estimated projectors and requested prelaunch code review. Primary-source scout communicated paired-supervision and eigengap limitations; these constrain interpretation, not numerical choices.
