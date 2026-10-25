# Mathematical review for the derived-control Reddit report

This review was prepared after RM-C1. It is a mathematical review, not a blinded empirical replication, product audit, or new natural-language experiment. Historical RM-C1 artifacts were read but not edited.

## Derivation

Let z,w be nonzero vectors in C^d. Define E=||z||², F=||w||² and h=Re(sum conjugate(z_j)w_j). Either conventional conjugation convention gives the same real part. The paper's Eq.2/3 is

S=(1/2)[||z+w||²/(E+F)][2 sqrt(EF)/(E+F)].

Realification U=(Re z, Im z), V=(Re w, Im w) lies in R^(2d). It obeys ||U||²=E, ||V||²=F, U·V=h. Thus c=h/sqrt(EF) is ordinary real cosine and R=2sqrt(EF)/(E+F) lies in (0,1]. Expand ||z+w||²=E+F+2h to obtain

S=R/2+R²c/2=R(1+Rc)/2.

This holds for arbitrary complex inputs, not only real ones, provided both energies are positive and finite in mathematical real arithmetic. The paper's own Appendix A Eq.5 already supplies the expansion nearly directly. Present this as a transparent control/extension of its stated real equal-norm reduction, not a novelty claim.

## Exact ranking conditions

1. If query and each candidate have equal nonzero norm, R=1 and S=(1+c)/2. All rankings and exact ties match cosine on realified coordinates.
2. More generally, for a fixed nonzero query, if all candidates have the same positive norm, R is constant across candidates, even if the query norm differs. S is then a strictly increasing affine function of c, so rankings and ties still match. Scores are equal to (1+c)/2 only in case1.
3. Equal candidate norms are sufficient, not necessary: candidates can have different norms but the same R when their norms are reciprocal relative to query norm, t and1/t. Coincidental ranking agreement is also possible without constant R.
4. If norms vary, this theorem does not guarantee rankings. Explicit reversal: q=(1,0), a=(10,0), b=(0,1). Cosines are1 and0, respectively. Resonance S(q,a)=1210/10201≈.118615822 while S(q,b)=.5. Orthogonal balanced b outranks perfectly parallel unbalanced a.
5. Mathematical ranking identity does not guarantee identical approximate-nearest-neighbor results, floating-point tie handling, latency, indexing, cost or learned encodings. Compare exact rankings first.

## Energy balance nuance: not a pointwise penalty

Calling R an energy-imbalance factor is fine. Saying imbalance always decreases each score is false when c is negative. For fixed c, dS/dR=1/2+Rc. At c=-1, S=R(1-R)/2. It is0 for exactly matched antiparallel patterns (R=1), but rises as energy imbalance is introduced, reaching1/8 at R=1/2, then falling toward0 as R→0. R=1/2 corresponds to amplitude ratios t=2±sqrt(3).

Exact scalar examples for z=1:

| w | c | R | S |
|---|---|---|---|
| 1 | 1 | 1 | 1 |
| 2 | 1 | 4/5 | 18/25=.72 |
| -1 | -1 | 1 | 0 |
| -2 | -1 | 4/5 | 2/25=.08 |
| -3 | -1 | 3/5 | 3/25=.12 |

The original denominator-normalized sum contains leftover energy for unequal antiparallel amplitudes. Phase opposition alone does not force zero; z=-w does. Distinguish equal relative phase pi with unequal amplitudes from exact additive opposites.

## Bounds and degeneracies

Because c∈[-1,1], S lies between R(1-R)/2 and R(1+R)/2, hence [0,1]. S=1 requires R=1 and c=1, giving z=w≠0. For both nonzero patterns, S=0 requires R=1 and c=-1, giving z=-w. If either pattern is zero, the paper formula/convention yields S=0; c is undefined there, so do not evaluate the derived expression as though zero cosine had a canonical meaning. In particular S(0,0)=0 by convention, not1.

Realification preserves mathematical complex-vector information. It is not a bitwise identity between finite-precision polar and Cartesian storage. At zero amplitude, different raw phase values encode the same complex zero; phases differing by2pi also represent the same complex value. Do not claim preservation of arbitrary raw phase-buffer metadata.

## Geometry and semantics

The expression depends only on energies and the real inner product. A simultaneous orthogonal transformation of the realified coordinates preserves it; common complex unitary transformations are included. Thus the score itself does not assign a privileged semantic meaning to a chosen coordinate's phase. Useful semantic meaning must come from encoding/training/procedures and task evaluation.

Real-valued vectors already preserve sign. Sign-phase mapping of an original signed real embedding does not create a new independent semantic signal: the vector is recovered as its complex real part. Comparing richer phase-conditioned data with amplitude-only features deliberately removes information from the baseline. That is a useful ablation but not a scoring-only control.

## Numerical caution

The archived test exercises modest synthetic magnitudes and standard float64, not arbitrary dynamic range. Naive E*F, E+F or squares can overflow/underflow; finite input coordinates alone do not ensure finite intermediate values. The realified form can cancel near R=1,c=-1, whereas the direct sum can accurately represent a small residual in some such cases. Conversely Cartesian/polar conversion has its own rounding. Avoid calling the derived formula universally more numerically stable. Shared rescaling can improve moderate implementations, but any actual stable kernel needs its own edge-case specification and tests.

All1200 pairs are comparisons, not1200 independent empirical trials:400 base pairs were each reused at3 scales, and normalized comparisons reuse their directions. This is correct for checking identities, but avoid statistical significance/confidence-interval language about sample success. No finite sample proves an algebraic identity; the derivation does.

## Questions worth inviting externally

- Does the realification or score algebra fail for a clearly specified case satisfying the assumptions?
- Are candidate energies normalized in the actual pipeline? If so, what additional retrieval behavior remains beyond the encoding?
- Where do the phase labels come from, and can their meaning be validated on held-out scoped negations or revisions?
- Can the proposed product be tested independently against the paper formula, or is its current kernel distinct?
- Is agreement or evidence relevance the intended target? Opposing evidence can be essential even when phase alignment is low.

Review result: the core identity is correct. The main corrections needed in a long public explanation are precise ranking assumptions, the nonmonotonic imbalance effect for negative cosine, zero-input qualification, and restrained interpretation of synthetic comparison counts.

## Publication draft recheck

Read the publication draft at `/workspace/frr/publications/REDDIT_PHASE_MEMORY_DERIVED_CONTROL.md` after its initial assembly. Its derivation, scalar phase formula, exact scalar examples, ranking reversal and threshold transformation are correct. The extracted illustrative Python block executed successfully with exit0 and maximum discrepancy4.440892098500626e-16. This check did not rerun or alter the archived original experiment. Softmax clarification: for R=1, softmax(S/T_S)=softmax(c/(2T_S)), so matching a cosine temperature T_c requires T_S=T_c/2. For constant R, use T_S=R²T_c/2. Do not reverse that scaling. Minor wording precision: the original eight checks contain exact equality/boolean fixtures as well as floating-point tolerances; say all eight passed and the floating-point equivalence checks used1e-12 rather than implying every fixture used that tolerance. No blocking mathematical error found in the inspected draft. The coordinator was separately advised to credit Appendix A Eq5 and qualify raw polar zero-amplitude phase aliases.
