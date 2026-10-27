# Three source contacts and an exact query-planning precursor

Resumed from SJ commit3f25c7967f3915cbdd4a842e6117a7dafd05f892 with three screenshot leads and authorization for parallel scouts. Client session date26October2026 America/Chicago; scouts record their observed27October access dates separately. Completed bounded phases: primary-source extraction/prospective planning review, one exact model execution, independent audit and sync. Six contexts including root: three source scouts, implementation engineer and mathematical/source reviewer-auditor. Scouts shared relevant findings; no participant reader, model API, training, index installation or production backend change occurred.

The screenshots are useful leads. We inspected the underlying sources rather than adopting the social posts' claims. The practical return is a clearer information-and-work accounting, plus a small exact prototype distinguishing adaptive query planning from privileged pre-query knowledge. This is not a unified theory of the papers or evidence that FRR improves model reasoning.

## Source extraction and original transfer questions

Each source note separates a bounded primary summary, our proposed transfer and actual read scope/access limits. No paper was reproduced. The notes and manifests preserve primary URLs/versions, code pins where inspected, unsuccessful discovery and distinctions between paper results and later software.

| Lead and inspected source | Saved extraction | Our next useful question, not a paper result |
|---|---|---|
| [Scalable Patch-Level Self-Supervised Learning,2610.10013v1](https://arxiv.org/html/2610.10013v1) | [PATCH](sources/PATCH.md), [source manifest](sources/PATCH_SOURCES.json) | Which task distinctions must survive an alternate view, and which transformations destroy them? Test selective invariance alongside sensitivity rather than treating all agreement as useful. |
| [LEANN,2506.08276v2](https://arxiv.org/html/2506.08276v2) and pinned author repository | [LEANN](sources/LEANN.md), [source manifest](sources/LEANN_SOURCES.json) | Count retained sources, derived index, model access, recomputation and latency separately. What becomes unavailable or stale when a representation dependency changes? |
| [On-Policy Self-Training,2610.32770v1](https://arxiv.org/html/2610.32770v1) | [SELFTRAIN](sources/SELFTRAIN.md), [source manifest](sources/SELFTRAIN_SOURCES.json) | Separate information supplied to a teacher/evaluator from what the ordinary solver can access. Self-consistency can nominate a check without authenticating a premise. |

The coordinator initially transcribed the patch paper ID incorrectly as2610.01031; the scout resolved the correct2610.10013 from primary metadata. This was our tentative transcription error, not an error attributed to the user's screenshot. [Initial scout note](sources/PATCH_INITIAL.md) is preserved. Limited failure to find an official code repository is recorded as an access/discovery limit, not proof of absence.

These contacts suggest different work at different layers: representation sufficiency, retained-versus-derived memory and privileged-versus-accessible learning information. They do not justify discarding originals, replacing our memory backend, treating synthetic agreement as ground truth or importing image augmentations into semantic reasoning without a task-specific check. Detailed training costs, benchmark limitations and software-versus-paper distinctions remain in the source notes rather than being generalized here.

## Planning question from the preceding reader result

[SJ](../source-join-reader-v1/REPORT.md) contained a correct unresolved answer after a two-record path yielded a broad interval, while a different pair could decide. That did not prove the reader chose irrationally: unseen information was not available before the first query. Before another participant comparison, we therefore modeled a setting where pre-query knowledge, observed reliability and prices are explicit.

This new model is an authored complementary-information proxy using bits, not a simulation of the source papers or a natural-language retrieval benchmark. The distinction is intentional: do not silently let a planner inspect the hidden route quality that the reader had to discover.

## Exact model and comparison classes

Task truth T and six other latent bits define128microstates. T,X,Y,u,v are independent fair bits. qP,qR are independent route-quality bits with known probabilities p,r. Four records cost1each:

    P = X
    C = (qP, X XOR T if qP=1, otherwise u)
    R = Y
    M = (qR, Y XOR T if qR=1, otherwise v).

Every individual record leaves T evenly balanced. A good complete P+C or R+M pair identifies T; bad-route fragments do not. C/M additionally reveal whether their route is usable. Those reliability flags and their semantics are supplied, perfectly reliable model premises, not an empirically validated reference channel.

The ordinary planner knows the generative model and prior but not actual latent bits. It maintains exact positive-weight compatible worlds, queries or stops, and may certify T only if every compatible world agrees. It maximizes identification probability first, then minimizes expected queries, with deterministic tie-breaking. This is a finite dynamic program, not a learned or universal reasoning algorithm.

Comparators:

- Every fixed subset of size<=budget, chosen before observations. Each selected query is charged on every world; no adaptive stopping. Its best resolution/cost is reported. Cost differences therefore include stopping and branch selection, not an isolated test of either.
- A quality-informed oracle given actual qP,qR for free before queries, but not T. It can select a good pair when one exists. This is extra information, not equal-information evidence of a superior policy.

Four known priors: (p,r)=(1/2,1/2),(3/4,1/4),(1/4,3/4),(0,0). Budgets0through4give20root comparisons. Zero-probability worlds are excluded from inference; unused latent bits and repeated observations retain combined probability. These are exact model probabilities, not empirical trials or confidence estimates.

## Results: what adaptive choice changes

Balanced prior p=r=1/2:

| Lookup budget | Adaptive: resolved prior mass; expected queries | Best fixed set: resolved mass; queries | Free-quality oracle: resolved mass; expected queries |
|---|---|---|---|
|0or1|0;0|0;0|0;0|
|2|1/2;3/2|1/2;2|3/4;3/2|
|3|3/4;9/4|1/2;2|3/4;3/2|
|4|3/4;9/4|3/4;4|3/4;3/2|

The third slot lets an ordinary planner inspect one route's quality, complete it when good, or inspect and complete the other when needed. A fixed set with three slots cannot contain both two-record pairs. At four slots the fixed set also has both routes, so its resolution ties. Both-bad worlds remain unresolved even after every record; more querying cannot create missing task information.

In the asymmetric priors, budget2adaptive resolution is3/4 with expected7/4queries. Budgets3/4resolve13/16with expected33/16queries. At budget3the fixed best pair still resolves3/4; its budget4set reaches13/16. The mirrored priors yield identical values and swap the preferred quality-first action. If both qualities are known always bad, the optimal planner stops immediately at every budget.

The oracle's budget2advantage in the balanced model is exactly the free quality information: it resolves3/4rather than1/2without paying to learn which route is good. It does not know T in advance. Do not label this gap an algorithmic improvement at matched information.

All twenty exact rows are readable in [ROOT_OUTCOMES.tsv](planning/ROOT_OUTCOMES.tsv). [Prospective algebra](planning/review/MATH.md) gives closed forms. [Full-output archive and restore](planning/RESTORE.md) preserves all worlds, duplicate-observation masses, fixed-set outcomes, belief states, every action/branch and ordinary/oracle policy leaves—not a lossy summary.

## A useful peripheral noticing

All single-record posteriors keep T at1/2, yet the quality-bearing C/M records can change which later query is worth taking. Information useful for choosing evidence need not answer the task immediately. Conversely, a record containing an answer fragment can be useless without its applicable relation or scope.

This is a finite-model illustration of planning value, not a novelty claim or a rule to always collect metadata first. It relies on trustworthy quality previews, known priors, unit prices and the specified certification objective. Real sources can have false metadata, correlated failures, missing model support, variable costs or a task where action can be warranted without exact identification. Those require different models and domain evidence.

## Execution, review and preservation

Prospective independent math and full source/schema review preceded [freeze](FREEZE.json). Sole main exited0in approximately1.089seconds under Python3.12.14, with exact Fraction arithmetic and no sampling. [Execution record](planning/EXECUTION.json), [stdout](planning/STDOUT.txt), [stderr](planning/STDERR.txt), [implementation](planning/experiment.py), [schema](planning/SCHEMA.md), [source review](planning/review/SOURCE_REVIEW.md).

Independent audit passed on its first execution, approximately1.308seconds. It checked512world rows,3993belief states,8301action values,9432transitions,2080ordinary and2080oracle world-budget policy replays,192fixed subsets/1560outcomes, and all20root rows against separately derived exact formulas. [Audit](planning/review/AUDIT.md), [machine checks](planning/review/AUDIT.json), [counts](planning/review/AUDIT_COUNTS.json), [audit code](planning/review/audit.py). The auditor had inspected main source for prospective review and discloses that exposure; no main imports or blinded-replication claim. No main/audit failure, outcome tuning or rerun occurred.

Paper-scout access limits and a malformed unsuccessful search call remain in source manifests. Main-code alignment edits occurred before final approval/freeze. No full paper/PDF was deposited. Full numerical run files total12,584,271bytes and are preserved byte-for-byte in the91,848bytearchive. [Manifest](planning/ARCHIVE_MANIFEST.json) records archive/member hashes; all extracted members were checked against originals. Numerical compression is lossless and is not a semantic-memory result.

No module/core/runtime/schema/tool/queue-status change is warranted just from this toy or source contact. Earlier actual-reader outcomes, rating disagreements, prospective fixture failures and historical strictCR replayFAIL remain unchanged. Current navigation is synced; no follow-up participant experiment or background job is running.

## Next strongest contact

Before an actual-reader planning comparison, specify what reliability metadata can honestly be known before acquisition, its cost and its own warrant. Use fresh cases with matched access and budgets, a simpler fixed/provenance comparator, and source conditions where quality previews are wrong or absent. Preserve unsupported certainty separately from unresolved but correct decisions; do not compare an oracle-informed planner to an ordinary reader as if their information matched.

For memory infrastructure, an optional backend trial would first need dependency/version manifests, preserved originals and end-to-end storage/latency/support accounting. For generated research questions, use model agreement to nominate a source check, not to close one. For representation experiments, explicitly test which task distinctions a proposed view preserves. [Next contacts](NEXT_CONTACT.md) are proposals only. High confidence in scoped exact arithmetic/audit and recorded source access; real-world planning benefit and FRR efficacy remain open.
