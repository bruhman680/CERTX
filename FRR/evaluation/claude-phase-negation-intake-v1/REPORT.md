# CP-N1: Claude phase-memory and scoped-negation relay intake

2026-10-25. User asked to locate the recent Claude branch, read its relay, and extract useful insights. Located **claude/pam-scoped-negation-2026-10-25**, pinned at **abebe1b5d78e8694cb0559648db63355e11cc062**. Thirteen supplied files are copied byte-for-byte into [the source archive](../../lineage/sources/claude-pam-negation-2026-10-25/README.md), with Git blob/SHA256 checks in [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json). Only those files are imported; no wholesale branch merge or edits to Claude's originals.

## What reproduced

Inspected all four Python scripts before running; their operations are bounded NumPy/standard-library calculations with printed output. Executed each unchanged once with single-thread BLAS limits: the8,000-pair identity check, PAM claim tests, flawed scoped-negation v1, and revised v2. **All four exited0, had empty stderr, and matched their supplied stdout exactly.** [REPRODUCTION.json](REPRODUCTION.json) links run records/diffs. These are same-code execution reproductions, not independent empirical confirmation, model training or product evaluation. The preserved v1 prints the disclosed design failure; exit0 is not a scientific success verdict.

The identity check reproduces `S=R/2+R²c/2` with maximum absolute discrepancy6.66e-16. V2 gives zero S/cosR top3 mismatches in each1,800-comparison setting. These reuse entity bindings/noise trials and oracle status assignments, not independent language tasks. See the original [PAM relay](../../lineage/sources/claude-pam-negation-2026-10-25/pam_claims/PAM_CLAIMS_TEST_RELAY_2026-10-24.md) and [scoped relay](../../lineage/sources/claude-pam-negation-2026-10-25/scoped_negation/SCOPED_NEGATION_RELAY_2026-10-25.md).

## Useful additions to our understanding

1. **Retrieval and stance can use different readouts.** Under the globally rotated E1 codebook at low noise, real-part cosine favors agreement and retrieves about one third of the three relevant statuses. Complex-inner-product modulus retrieves all three, while angle distinguishes their supplied stance labels. This is a useful constructed design, not proof that phase learns language. Metadata labels also perform well under their stipulated conditions.
2. **Magnitude needs task semantics.** The PAM fixtures distinguish matching strength, arbitrary scale and “higher is preferred” confidence. Energy balancing helps or harms depending on the defined target; it is not a general confidence estimator. Controls with explicit norm/confidence features expose that dependency.
3. **Aggregation can erase disputes under a specified summation rule.** The count19zero-sum histories at n=4,18containing opposite emissions, is a constructed counting witness.94.7% is a fraction under uniform enumeration of those histories, not an empirical dispute probability for agents or a demonstrated database fault.
4. **Scoped modulation is less clean than whole-vector rotation.** Shared context mixes with the phase-bearing binding. This motivates calibration/weight-drift checks before treating angle as a stable semantic label.

## Important interpretation corrections

- The scoped relay's broad sentence that a scalar cannot serve agreement and evidence retrieval together is too strong. Its own E0 low-noise row obtains1.000 agreement/status/evidence with cosine. The observed tradeoff concerns particular encoding/readout/task choices, not all scalar retrieval functions.
- T3 in v2 classifies the stance of **oracle-selected relevant records** via `W[idx[(v,0,s)]]`. It does not classify the actual retrieved top3 and jointly score entity/time/relevance/stance. The component results therefore are not a measured end-to-end pipeline success rate. At high noise, excellent conditional T3 can coexist with lost relevant records.
- E0's near-chance angle-only T3 does not mean E0 lacks all stance information: its symmetric real stance tokens support strong T1/T4 at low noise. Angle is one readout, not the entire representation.
- V2's T1/T4 queries are still built with the correct A/N oracle status. Symmetric tokens and noise repair the disclosed v1 comparison flaws; they do not test language parsing or learning a phase convention. Calibration entities are separate, but calibration/evaluation noise levels and the codebook remain matched.
- The short summary says the source paper reports scan times but not negation results. The original paper's section4.2 does report a small operator-retrieval experiment including NEG. Appropriate scope: not a demonstrated general held-out natural-language negation benchmark. Preserve this correction instead of adopting the short summary literally.

## A separate real-coordinate control and boundary witness

[real_channels_check.py](real_channels_check.py) imports none of the supplied scripts. It checks the elementary two-real-channel expression for complex inner products, plus an orthogonal two-component context/binding example. This is a small algebraic development check, **not** the requested full independent v2 rebuild or a learned-encoder experiment.

For `z=x+iy`, `w=a+ib`, define `A=x·a+y·b`, `B=x·b−y·a`. Then `conj(z)·w=A+iB`; normalized modulus is `hypot(A,B)/(||z||||w||)`, angle is `atan2(B,A)` when the product is nonzero. Ordinary realified cosine reads A only. The extra readout is another function of the same paired real coordinates, not additional information accessible only to complex numbers.

In128moderate random pairs, modulus error is at most1.11e-16 and wrapped-angle error4.44e-16. Eight declared checks pass; [results](REAL_CHANNEL_RESULTS.json) retain all errors and examples. Unknown status uses an externally supplied pi/3code here, not Claude's pi/2; that arbitrary choice does not model calibrated uncertainty.

For normalized `q=(a,b)` and scoped opposite `w_N=(a,−b)`, their inner product is `(a²−b²)/(a²+b²)`. Equal context/binding amplitudes give zero modulus and undefined angle; context dominance gives angle0 for both A and N. A record has not disappeared from storage: the **comparison readout** has cancelled or collided. This bounds global-phase intuition under scoped mixtures. It does not prove that full vectors, joint magnitude+angle or other trained readouts cannot distinguish the statuses. [MATH_NOTE.md](MATH_NOTE.md) develops the assumptions.

## What to carry forward

Keep relevance coverage, stance/epistemic status and final warrant separate, as in SF-C1/LH-C1. The vector/codebook parallel is structural, not replication of actual-agent reasoning. The strongest next bounded contact is an end-to-end retrieved-record score under changed context/binding ratios and calibration/evaluation noise mismatch, with the same real-coordinate channels and explicit metadata controls. Do not rush to training before defining that measurement. [NEXT_CONTACT.md](NEXT_CONTACT.md) is proposed, not executed.

Claude flags a possible missing R/2 in the pasted Reddit version. Our39,782-character repository draft is intact and contains the full formula. The actual posted copy was not obtained, so that warning remains unverified; no Reddit edit/message was sent. Abstract-level prior-art pointers in the relay were not independently read here.

Confidence is high in exact source reproduction and the stated algebraic witnesses, limited for oracle-fixture usefulness, and open for learned encoders, general negation, deployed memory and group-reasoning gains. Queue/core/schema status unchanged; original failures and historical public draft preserved.
