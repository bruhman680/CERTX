# Causal history, temporal corrections, and provenance — bounded scout

Requested session date: 2026-11-01 America/Chicago. Accessed 2026-11-02 UTC. This is a research note, not an experiment result or a proposal to replace FRR. No FRR/core files, models, runtime dependencies, or source ledgers were changed.

Local scope read: `/workspace/frr/evaluation/revision-authority-settle-v1/REPORT.md`. Its implemented resolver contract is the reference for comparisons below. I did not inspect its code or run its cases; statements about the toy therefore refer to its report. In particular, rule correctness is engineered contract coverage, and the model has not learned these rules.

## Strongest finding

Preserving a parent DAG and old snapshots does not yet distinguish **what the system could answer at an earlier receipt cutoff** from **what it can now answer about that earlier effective period**. A late correction can legitimately change the second answer while leaving the first fixed. A second gap appears when answers depend on several sources: a list of contributing witnesses does not record whether they were alternatives or jointly necessary. Those distinctions are useful before adding more elaborate memory mechanisms.

The first claim is a comparison to the reported toy and an inference from the temporal semantics below. The second has an explicit counterexample in Green et al. §4. Neither establishes a neural memory mechanism or a novel algorithm.

## Four sources and exact accessed scope

### 1. Nuno Preguiça, *Conflict-free Replicated Data Types: An Overview* (2018)

[Author paper, arXiv HTML](https://arxiv.org/html/1806.10254), version banner v1, 27 June 2018. Read introduction and §2.1 through register and set semantics; did not audit implementations or security sections.

**Source claims:** Causality records which effects were present when an update was made. A multi-value register returns writes with no causally later write; concurrent writes survive together. LWW instead chooses under a declared total order. Concurrent add/remove can use add-wins or remove-wins semantics. These are application choices, not a universal correct answer. Replica convergence is defined for replicas receiving the same updates.

**Inference for FRR:** The toy's sibling conflict retention is compatible in spirit with a multi-value register, but it is not thereby a CRDT. A deterministic batch resolver and reversal checks do not establish asynchronous replication guarantees. In particular, the reported missing-parent error might become resolvable after later arrival. An error at one received prefix should not imply permanent corruption without a completeness assumption. A declared parent link also need not encode all real observation causality.

**Do not import:** automatic LWW, add-wins, or remove-wins as epistemic truth rules. Convergence can preserve a conflict; agreement does not authenticate a speaker or establish truth.

### 2. XTDB, *Time in XTDB* (official documentation)

[Official page](https://docs.xtdb.com/about/time-in-xtdb.html). Read system-time and valid-time definitions, worked address example, and “In practice” query distinctions. Documentation is live; no release-pinned server was installed or tested.

**Source claims:** System time records database history, while valid time represents the period an application considers a fact effective. Late information or corrections can revise that effective history. Queries can recover both current corrected history and the database view before a correction. The worked example stores a future effective change separately from when it was learned.

**Inference for FRR:** A revision number and parent ancestry cannot alone answer both temporal questions. A correction event needs an asserted effective interval; a receipt cutoff needs a separately recorded ingestion history. An “as of” question must identify the intended dimension. This may matter to a remembered claim, but is not necessary for every repository-content question.

**Do not import:** XTDB's whole schema or database engine. Valid-time annotations are asserted applicability, not verified real-world truth. A temporal index does not resolve competing source authority or concurrent branches.

### 3. Todd J. Green, Grigoris Karvounarakis, Val Tannen, *Provenance Semirings* (PODS 2007)

[Author-hosted paper](https://www.cs.ucdavis.edu/~green/papers/pods07.pdf). Read §§3–4, especially Definition 3.2, Figure 5, and Proposition 4.2; checked the conclusion's boundary on negation. Did not reproduce recursive Datalog algorithms.

**Source claims:** Positive relational algebra combines annotations by addition for alternatives and multiplication for joint use. Flat contributing-tuple sets can hide different derivations with the same contributors; §4 gives such an example. Symbolic polynomials retain that structure and can be evaluated under chosen source valuations. The paper does not supply unrestricted negation via ordinary positive semiring operations.

**Inference for FRR:** Status-origin sets suffice for the reported direct single-field materialization but would be too weak for general derived answers. For Boolean support, `a OR b` remains supported after withdrawing `a`, while `a AND b` does not, although both have contributor set `{a,b}`. A copied source should retain its dependency rather than becoming independent corroboration. Withdrawal of support, assertion of a negative fact, and deletion of an entity require distinct contracts.

**Do not import:** polynomial coefficients as confidence or votes. Multiplicity of derivations does not establish independence. The algebra does not authenticate labels, and generic conflict resolution or epistemic retraction is not provided by positive relational provenance alone.

### 4. Differential Dataflow, *Making Changes* (official project documentation)

[Project book](https://timelydataflow.github.io/differential-dataflow/chapter_3/chapter_3_3.html). Read the complete short input-session page. No execution, version-pinned API check, or audit of the wider runtime.

**Source claims:** `insert` and `remove` respectively increment and decrement an item's count. `update` permits signed differences. `update_at` permits updates at a specified time in the input session's present or future; the text explicitly limits it to that range. Effects may wait until input passes their times.

**Inference for FRR:** Retraction can be represented as an explicit change to a maintained result, rather than erasing the historical input. But a negative count update is an accounting operation, not automatically a claim that the real-world proposition is false. A system needs to identify which support is withdrawn, protect replay identity, and decide when output is sufficiently complete for its question.

**Do not import:** arbitrary past logical-time insertion as a promise of this API. Application effective time and input progress time need separate treatment. A streaming engine would be disproportionate to the current single-field study.

## What the reported toy leaves open

These are comparison inferences, not failures discovered by execution:

- **Prefix versus complete history:** unavailable parents can be transient; a complete invalid graph and an incomplete delivery need different operational handling.
- **Two temporal dimensions:** corrected effective history and earlier received knowledge need separate query parameters and receipts.
- **Retraction scope:** deleting a subject, removing one field, withdrawing one source claim, and revoking source authority have different downstream effects. The report tests the first two, not the others.
- **Derived support:** a flat set does not distinguish alternative derivations, joint prerequisites, or copied witnesses. Equal-valued branch heads are already correctly not counted as independent confirmations in the report.
- **Multiple source branches:** causally later within one lineage does not imply authority over another source. Source precedence, if desired, needs a declared policy separate from ancestry, clocks, and value equality.

## One bounded next test: late correction with a frozen earlier view

This is a specification suggestion only; it has not been implemented or run. It is deliberately separate from the main agent's real-artifact Git inspection.

Use one subject, one declared authoritative source, one field, two immutable claims, and an explicit temporal policy. Let effective times be ordinal `V1 < V2` and receipt cutoffs `K1 < K2 < K3`; these are test coordinates, not inferred clock measurements.

- `e1`: received at `K1`, status `ready`, effective `[V1, infinity)`.
- `e2`: received at `K3`, correction of `e1`, status `blocked`, effective `[V2, infinity)`.
- Policy: at a knowledge cutoff, use only claims received by that cutoff; an authorized explicit correction supersedes its parent only over its declared effective interval. Old claims and old receipts remain available. This interval policy is an extension, not a claim that the existing toy already implements it.

Declare the oracle before implementation:

| Receipt cutoff | Effective point V1 | Effective point V2 |
| --- | --- | --- |
| K1 | ready, witness e1 | ready, witness e1 |
| K2 | ready, witness e1 | ready, witness e1 |
| K3 | ready, witness e1 | blocked, witness e2 |

Six exact query results, plus immutable raw events, are sufficient. After ingesting `e2`, replaying the `K2,V2` question must still return `ready`; querying `K3,V2` must return `blocked`. Preserve receipt coordinates, eligible event IDs, applied correction edge, answer, and witness. A latest-only comparator will fail at least the frozen historical question; a receipt-only history without effective intervals cannot express the `K3,V1` versus `K3,V2` distinction.

No model call is needed to test this contract. If it passes, it demonstrates declared temporal materialization on one fixture, not learned temporal reasoning, general source truth, arbitrary retraction, or independent empirical validation. AND/OR provenance withdrawal would be a separate later test, not an extra dimension silently added to this one.

## Access limits and uncertainty

Research used browser retrieval of the primary paper/docs above. The original 2011 CRDT author-hosted PDF timed out, and HAL returned an access-denial page; I did not infer their contents from that failure or bypass it. A university mirror of RR-7687 v2 was accessible and inspected for causal-history definitions, but the claims selected above use the directly accessible author overview so that the recommendation rests on four sources. No novelty or “latest best method” claim is made.

The local baseline was a report, not a code audit. No claims here establish signatures, authentication, real-world effective dates, trust independence, model learning, or production scalability. Network policy was inspected under the cloud-environment runtime skill: unrestricted HTTP policy was reported enforced; no credentials were used or printed.
