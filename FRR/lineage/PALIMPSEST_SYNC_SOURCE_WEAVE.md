# Palimpsest and GitHub sync: established relatives and actual burdens

This pass reads the original [palimpsest seed](sources/2-palimpsest_seed.md) alongside primary engineering documentation and LLM memory research. It asks what preserving and synchronizing layers can actually do. No GitHub mutations, model evaluations or FRR core changes were performed.

## Surviving relationship

**Preserve the trail, but derive the current view.** Retaining an older interpretation makes revision inspectable and recovery possible. It should not make the older interpretation equally authoritative forever. A sync operation moves records; it does not determine whether their claims are true or whether a future reader will use the right version.

The seed's strongest contribution is its warning that repeated tracing can look like independent convergence. Its strongest practical requirement is to record what a supposedly fresh pass could see. Agent identity, a later date or a separate file alone cannot establish evidential independence.

The lines “Revision is not correction” and “the only failure mode that matters here” work as poetic instructions to retain legibility. They should not be adopted literally as an operating contract. Corrections can invalidate claims while leaving their historical expressions intact; incomplete capture, stale projections, lost references, access failures and false provenance are also consequential failure modes.

## Source weave and access depth

| Source | Inspection depth | What it contributes | What it does not establish |
|---|---|---|---|
| [Fowler, Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html) | Complete primary HTML downloaded; state capture, rebuild, snapshots, replay and external-gateway sections inspected | Recorded state-changing events can support reconstruction, temporal queries and repair | A directory of dated notes is not automatically event sourced; unlogged state changes defeat completeness |
| [Fowler, Bitemporal History](https://martinfowler.com/articles/bitemporal-history.html) | Complete primary HTML downloaded; actual/record history distinction inspected | Distinguishes when something applied from when the system learned or recorded it | A later entry is not necessarily a later real-world state, and a timestamp does not validate content |
| [W3C PROV-DM](https://www.w3.org/TR/prov-dm/) | Full normative document downloaded; entities, activities, agents, revision, derivation and provenance-of-provenance inspected | Vocabulary for who produced what, through which activity, using which records; revision as a derivation relation | PROV represents provenance assertions; it does not itself authenticate them or prove truth/causal influence |
| [Pro Git: Git Objects](https://github.com/progit/progit2/blob/main/book/10-git-internals/sections/objects.asc) | Primary project documentation inspected; blob/tree/commit and content-addressing sections | Content identities, snapshots and parent links make versions inspectable | Ordinary commit author text is not verified identity; a content hash is not a truth test |
| [Pro Git: Signing Your Work](https://github.com/progit/progit2/blob/main/book/07-git-tools/sections/signing.asc) | Primary project documentation inspected | Signatures can connect specified content with a key under a trust policy | A signature does not make the assertion true or the signer unbiased; key trust must be established |
| [Git garbage collection](https://github.com/git/git/blob/master/Documentation/git-gc.adoc) | Official source documentation inspected; unreachable-object and retention discussion | Documents why reachable references and retention policy matter | Git is not an unconditional eternal append-only archive; unreachable objects can be removed |
| [LongMemEval v1](https://arxiv.org/html/2410.10813v1) | Full primary HTML downloaded; knowledge-update definition and indexing/retrieval/reading distinctions inspected | Tests updated personal information, temporal interpretation and abstention; retrieval and correct reading are separate stages | Does not directly evaluate our GitHub handoffs, FRR or a physical shared substrate |
| [Lost in the Middle v1](https://arxiv.org/html/2307.03172v1) | Full primary HTML downloaded; controlled evidence-location experiments inspected | Shows retained context can remain poorly used depending on location and task | Does not prove all current models fail similarly, nor that our summary placement policy solves the problem |

These are different contributions rather than eight independent confirmations. Engineering patterns explain feasible record systems. Memory benchmarks provide conditional observations about particular model/system configurations. Neither validates FRR efficacy by association.

## Four different claims often compressed into “memory”

1. **Auditability:** an investigator can retrieve the earlier artifact and inspect its relationship to the revision. This needs retention, references, permissions, readable formats and adequate context.
2. **Authenticity/integrity:** the retrieved artifact has the expected bytes and, where required, is attributable to a trusted key or actor. Content hashes and signatures address different parts of this burden.
3. **Semantic truth:** its assertion accurately describes the relevant world or artifact. This requires evidence or a test outside merely preserving the assertion.
4. **Reasoning benefit:** providing the record helps an agent reach a better calibrated or more correct result than a matched alternative. This needs an actual comparison; preservation alone cannot establish it.

GitHub helps with the first two when properly used. It does not automatically establish the latter two. A false completion claim committed faithfully is an authentic record of a false claim.

## History, current view and synchronization

Event sourcing gives a useful distinction between a retained event trail and a computed application state. For our work, a practical analogue is a preserved lineage plus a compact **current-status view**. The view identifies active claims, superseded claims, unresolved alternatives and where the supporting artifacts live. It should record the source versions from which it was built.

This analogue is not a claim that our Markdown collection already has replay-complete semantics. Exact rebuilding would additionally require defined events, complete input capture, deterministic or recorded transformation choices, versioned reducer code and controls for external effects.

Bitemporal thinking adds a useful distinction:

- `applies_at`: the time or version of the situation being described;
- `recorded_at`: when this record or correction entered our archive.

A correction learned today can concern a run from last week. Sorting only by save date can confuse “latest knowledge about an old run” with “newest run.” A third `verified_at` or source receipt can help track when the assertion was checked, without pretending that checking guarantees truth.

Synchronization should similarly be described through observed states: locally prepared, locally checked, external write attempted, external write confirmed, and remote content inspected. A commit receipt should identify repository, branch, commit SHA and the verified paths. An interrupted write is unknown until readback establishes what happened. This is a recordkeeping repair to our own earlier interruption risk; it is not a cognitive theory.

## The documentation wake and stale handoffs

An older conclusion can survive a careful correction by remaining in summaries, filenames, schemas, prompts or copied datasets. That is a specific **propagation path** to inspect, not merely more history to collect.

LongMemEval provides an established test setting for whether assistants recognize updates and temporal distinctions. It also separates indexing, retrieval and reading: retrieving the relevant record does not ensure that the answer applies its update correctly. Lost in the Middle supplies a different result: evidence can be present in a context while its position affects use. Together they justify testing access and application rather than equating retention with usable memory.

Neither paper directly shows that our current handoff is stale or harmful. That needs a controlled continuation test. A useful one presents matched fresh agents with: the same current view alone; the current view plus labeled superseded history; or the current view plus an unlabeled stale summary. Ask both a present-state question and a historical “what was believed then?” question. Score version selection, provenance fidelity, calibrated uncertainty and factual outcome separately. Rotate evidence order and keep task information and budget comparable.

This can meaningfully fail in either direction: full history may preserve useful reasoning that a compact view erases, or stale material may displace a correct update. Finding the second effect would not justify deleting all history. It would motivate better retrieval and status labeling.

## Minimal useful additions, if we implement them

- Keep original artifacts and dated corrections; do not silently replace the historical seed.
- Add explicit `supersedes`/`corrects` relations where a current claim changes, including why and which evidence changed its status.
- Generate a concise current view with pinned dependencies rather than requiring each future agent to infer authority from file order.
- Record information access for independent reviews: allowed sources, excluded prior interpretations, shared generators and shared labels.
- Verify sync through remote readback before asserting publication; separate delivery evidence from scientific validation.
- Periodically test recoverability and stale-claim selection with a fresh reader. No reasoning-performance gain is claimed until compared against matched baselines.

Fowler's replay warning also matters: reconstructing a history must not resend external messages, payments or publications. A record replay and an action replay are different operations. Our continuation harness should preserve that distinction even when the domain logic is unchanged.

The current stabilization point is therefore modest but useful: **the palimpsest can improve legibility and accountability when corrections remain authoritative and their lineage remains recoverable.** Whether that also improves agent reasoning is a separate open evaluation.
