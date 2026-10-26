# Context perturbation and repair: conditional recovery with an ordering limit

CR-C1/2/3 review completed26October2026 America/Chicago after user resume. **Original strict ordered replay remains FAIL. Fixed-ID readouts and retrieved membership are validated in the fixed sample.** The paused1,170flags are explained, not erased. [Current status](RESUME_STATUS.json); [pause status](STOP_STATUS.json) remains historical.

## What the surrounding-structure idea yielded

The user proposed that surrounding information/structures and perturbations might expose mistaken assumptions and create room for repair, inspired by an earlier GPU-hammer analogy. This is a controlled linear experiment, not hardware disturbance or evidence that the same physical mechanism governs reasoning.

A selective context change repairs the contaminated subspace here. A large response alone does not identify a repair. Known response coefficients also permit recovery from partial context changes or signal changes that simple averaging mishandles. Those coefficient ROLE labels and selective factor access are supplied information, not discovered semantics or calibrated probabilities of mismatch.

[Metamorphic-testing](https://arxiv.org/pdf/2002.12543) and [invariant causal prediction](https://arxiv.org/pdf/1501.01332) primary-method readings clarify justified relations and conditional intervention assumptions. [Scout](scout/REPORT.md) records selected full-method read scopes/access limitations. Neither work implements this experiment or proves its transfer to language. The scout motivated adding a coefficient-aware comparator BEFORE outcomes; initial protocol/source/replay plans remain preserved.

## Algorithm, actual task and privileges

Observed contrast D=n+s mixes nuisance and binding signal. A trusted generator provides D'=alpha*n+beta*s. Averaging gives ((1+alpha)n+(1+beta)s)/2. Coefficient-aware reconstruction is

    s=(D'-alpha*D)/(beta-alpha), when abs(beta-alpha)>1e-10.

When singular, the operator is explicitly unidentified; its downstream zero projector is an unavailable placeholder, not recovered zero signal. Twelve supported singular directions are the supplied rank ceiling; rank-zero inputs do not receive arbitrary SVD completion. [Protocol](PROTOCOL.md) and [math](MATH_NOTE.md) preserve exact rules.

| Probe | alpha,beta | Averaging yields | Coefficient-aware result |
|---|---|---|---|
| COPY | 1,1 | Original contaminated graph | Unidentified |
| CONTEXT_FLIP | -1,1 | Binding | Identified binding |
| PARTIAL_CONTEXT | -.5,1 | Smaller contaminated graph | Identified binding |
| SIGNAL_FLIP | 1,-1 | Context | Identified binding by differencing |
| GLOBAL_FLIP | -1,-1 | Zero average | Unidentified |

Context/signal-flip probes have identical spans (one is the negative of the other), but their averages target different factors. Global flip has ambient relative change2 while preserving the original span. Movement or invariance alone cannot assign semantic roles.

Sources reuse SA/PC tasks and selected aligned training differences: three seeds, twelve context/twelve binding coordinates,48candidate records/seed, separate calibration entities, ratios r=.5/2 and query noise0/1.5, nested12/48example prefixes. Status code, A-reference orientation, calibration labels, rank ceiling and trusted interventions remain privileges. Two paired observations per example have arm-dependent information despite matched counts. No independent test dataset, learned language, deployed-memory or group-benefit claim.

FULL, ORACLE, average REPAIRED and coefficient-aware SOLVED project actual noisy queries and all candidates, rank by normalized complex-product modulus and decode actual top3 using separately fitted circular centres. Joint completion requires all3correct entity/time records AND statuses. Usource uncertainty differs from decoderABSTAIN; missing centres globally abstain under the inherited1e-10policy. Circular concentration is not truth probability.

## Execution and actual outcomes

Two execution attempts, one completed experiment. Attempt01 stopped BEFORE probes/fits/scoring because local raw-byte hashes were compared with source dtype+shape+bytes digests. File hashes passed; source data did not change. Failed source/run/freeze and [repair diff](REPAIR_01.md) preserved. Reviewed correction only changed digest encoding/labels and pre-NumPy single-thread setup. Attempt02 completed exit0 in4.92seconds. No scientific grid, source data, thresholds or scoring changed. Resumption performed saved-data audits only; no main rerun.

Outputs:30,720method records/7,680paired rows/960method conditions;60structures/480calibrations. They reuse48claims/384query IDs/288unique arrays. Exact dedup maps7,680logical arrays to1,207byte-distinct arrays; no rounding or row selection. Repetitions and controls are not independent evidence. [Summary](RUN_SUMMARY.json) retains all160repaired/solved descriptive cells.

Representative noise-free-query (eta0) joint completion at r2, pooled96rows/cell (clean repetitions duplicate claims), equal at both training prefixes:

| Probe | delta.5 average | delta1.5 average | SOLVED, both deltas |
|---|---:|---:|---:|
| COPY | 0 | 0 | Unidentified |
| CONTEXT_FLIP | 1 | 1 | 1 |
| PARTIAL_CONTEXT | 1 | 0 | 1 |
| SIGNAL_FLIP | 0 | 0 | 1 |
| GLOBAL_FLIP | 0 | 0 | Unidentified |

Identified SOLVED conditions match oracle task outcomes, including noisy-query joint completion.875 at r.5 and.28125 at r2. Exact conditional structure recovery does not remove query noise. Partial-context averaging at delta1.5,r2clean has conditional relevant-record stance accuracy1 but evidence/joint completion0: retrieval still omits evidence.

There are3,072unidentified SOLVED records. Their all-zero placeholder scores canonically return the first claim, giving evidence recall.0625. That is not recovered evidence or a conclusion that the original stored vectors lost information.

## The paused replay errors are resolved as a scoped limitation

[Exhaustive ledger audit](review/LEDGER_CHECKS.json) passes all30,720records/960aggregates/7,680pair links,15,360prior-control and14,592repeated-control comparisons. Initial exact aggregate comparison was repaired audit-only: compensated sum versus sequential addition differed by at most7.11e-15; original code/logs retained. Discrete/integer checks remained exact.

Original independent refit replay:32,304checks,60structures/480calibrations,1,920selected records/92,160candidate readouts,1,170strict errors. On resumption these errors reproduce identically, and original code/result/selection/log hashes remain unchanged.

Every flag is classified:223condition-level top-array comparisons,341returned-index comparisons,341returned-ID comparisons,265returned-label sequences. They cascade from341of1,920rows with different top3 ORDER after independent SVD refitting. Every selected set matches. All92,160fixed-ID labels, reasons and validity flags match exactly; max product/score discrepancy1.185e-14. Independent reviewer reconstruction corroborates every changed row and full classification.

Score gaps between reordered records are at most2.054e-15 in saved arithmetic and1.555e-14 after refitting. These are observed gaps, not relaxed tolerances. Original2e-12numeric tolerance and1e-10decision threshold remain. Stored rankings equal exact stable sorting of STORED scores in all1,920selected rows. A saved-projector downstream supplement reproduces order, but is conditional on those projectors and does not establish independent-refit exactness.

**Strict ordered replay remains FAIL.** Separately, fixed-ID readouts/membership are validated in the fixed sample. The reported joint top3 metric is order-insensitive; a future top1 or other order-sensitive decision could be affected and needs its own check. No blanket original PASS, threshold/sample change, main rerun or rule that closeness excuses changed membership. [Final receipt](review/REPLAY_FINAL_RESULT.json), [replay report](review/REPLAY_REPORT.md), [independent summary](review/RESUME_INDEPENDENT_SUMMARY.json) and [resumed review](review/RESUMED_REVIEW.md) distinguish the claims. Complete error/row classifications and executable checks are preserved in the completion archive.

Replay inspected schema/data, not experiment implementation; reviewer inspected implementation prospectively but imported neither experiment nor replay. They share specification/data, not independent empirical observations. A reviewer JSON-serialization failure was preserved and corrected output-only. Audit integrity does not establish real-language selectivity or semantic truth.

## What we can use, and what remains open

Surroundings can supply controlled contrasts and constraints WHEN their response laws are warranted. Preserve original data and withhold unsupported repair when identification is missing. A stronger perturbation, more contexts or a larger swarm does not automatically establish that law.

The strongest next contact is measuring/bounding intervention selectivity and off-target effects, including uncertain or mistaken coefficient roles. Count trusted anchors/witness information and costs; evaluate actual task decisions rather than contrast fit alone. [Next contact](NEXT_CONTACT.md) is proposed only. The solver lives in this experiment, not a deployed general verifier or proven reasoning habit.

Core/runtime/schema/QUEUE.json unchanged; MEM-04partial. Broader historical/status/criterion memory queries, retained-clause fidelity and group reasoning remain open. No automatic fourth cycle/background work. [Restore](RESTORE.md) distinguishes original paused evidence from resumed audit artifacts; original pause history remains preserved.
