# MS-L1: a faithful summary can be insufficient for a new question

The user asked for a queue overview and further bounded work, then reported45% remaining in the five-hour usage window. We limited execution to the already prepared eight-reader/16-turn contact and source intake, with no additional swarm/benchmark expansion. Remaining live allowance is not programmatically visible; token/$/compute consumption was not measured.

**Result:** original-record access resolved both hidden-world decisions; summary-only readers and readers receiving an accurate but wrong-run record appropriately remained unresolved. No observed false certainty in these authored cases. This is a task-relative access result, not a comparison of reasoning frameworks or evidence of an autonomous memory field.

## Preparation and execution

[Protocol](PROTOCOL.md), [configuration](CONFIG.json), [initial messages](INITIAL_MESSAGES.json), [keys](KEYS.json), [arithmetic checks](KEY_CHECKS.json), [source contact](SOURCE_CONTACT.md) and manifest were deposited at [0ab526a7](https://github.com/bruhman680/CERTX/commit/0ab526a7c5c12705c2215762c3d39980feab6a8a) before participants. Original manifest-bound files remained unchanged.

Two constructed worlds share the same truthful handoff: run Q7 passed the old band[99.9,100.1], but exact reading/uncertainty were omitted. The new question uses[99.99,100.01]. In one world Q7 is100.040±.001, entirely outside the new band. In the other it is100.004±.001, entirely inside. Both satisfy the old band. A different run Q6 has the opposite-world reading and is accurate only for Q6. The input explicitly stipulates reading-bound coverage and record authority for the named run; no physical measurement or authentication was performed.

Four conditions, two fresh readers each: current record supplied; summary only/no lookup; one lookup returning the current record; one lookup returning the wrong-run record. Guidance stays the same; access instructions and exposed data deliberately differ. One context per world/condition, two turns per context. All eight contexts began with fork_turns=none and were instructed not to use tools/files/other participants. Shared physical access and model ancestry remain; instructional isolation is not a security barrier.

First response gave a decision and optional RUN request. Parent supplied exactly the requested record or no additional evidence, without correcting participants. Second response was final. All16 replies completed, no outcome retries or extra cases. [Responses](RESPONSES.jsonl) retain collaboration final-message payload text and parsed JSON; [second messages](SECOND_MESSAGES.jsonl) retain delivered record replies. No private reasoning/backend token metadata is recorded.

## Results

[Scoring output](RESULTS.json), [scorer](../../tools/score_memory_task_shift.py). Source-grounded completion requires relevant Q7 evidence as well as a correct decision; an unsupported lucky answer would not count. Packet-relative warrant separately credits appropriate unresolved responses.

| Access condition | Readers | Warranted final responses | Source-grounded completions | Appropriate unresolved | False certainty | Lookups |
|---|---:|---:|---:|---:|---:|---:|
| Current record supplied | 2 | 2/2 | 2/2 | 0 | 0 | 0 |
| Summary only | 2 | 2/2 | 0/2 | 2/2 | 0 | 0 |
| Lookup returns current record | 2 | 2/2 | 2/2 | 0 | 0 | 2 |
| Lookup returns Q6 record | 2 | 2/2 | 0/2 | 2/2 | 0 | 2 |

All eight first-turn decisions and request choices also matched the prepared packet warrant/policy. All replies respected200-word caps. Sixteen participant turns are measured; equal turns do not imply equal computation. Returned whitespace-separated word counts were260,279,281,255 respectively for the table's order; these small differences are not stable cost estimates.

Unblinded parent semantic review agrees with the mechanical scoring. MS03 used Q7's[100.039,100.041] to reject the narrower band while preserving old acceptance. MS07 used Q7's[100.003,100.005] to accept. MS04 explicitly rejected using Q6's interval for Q7. MS01 distinguished old acceptance from evidence sufficient for the new criterion. No independently blinded semantic regrading was performed.

## What we learned and what remains open

The distinction is not that summaries are inherently bad: this summary was truthful and sufficient for the old acceptance statement. Its retained distinctions did not settle the later narrower question. Supplying/retrieving relevant original data repaired the gap here. Fetching an accurate record for a different run did not repair it. Readers handled that boundary appropriately under explicit cues.

This narrows MEM-04/HPGM-03: fresh-reader exposure and source/version relevance are operationally testable. It does not complete either family. Conditions were designed to differ in available decisive information, so they do not establish an FRR instruction effect, autonomous retrieval quality or a natural-world performance advantage. Only two worlds/eight contexts; highly cued criterion/run labels; parent-authored keys; no learned writer, actual internal-memory truncation, long-context positional manipulation, population calibration or independent source reliability estimation.

The optional workflow refinement is to check whether a retained conclusion still addresses the current question. Preserve old criterion/scope, omitted consequential detail and an original-record locator when possible. This is guidance; the study did not ablate those individual fields or prove a universally optimal handoff. More detail is not always necessary—retrieve what the changed question needs, then stop when the evidence suffices.

[LongMemEval](https://proceedings.iclr.cc/paper_files/paper/2025/file/d813d324dbf0598bbdc9c8e79740ed01-Paper-Conference.pdf) separately studies memory abilities and indexing/retrieval/reading stages. [Lost in the Middle](https://cs.stanford.edu/~nfliu/papers/lost-in-the-middle.arxiv2023.pdf) manipulates information position within context. Our short missing/relevance test differs from both; see source-contact limits. Neither benchmark was rerun.

Next discriminating work: less-cued record selection, plausible wrong metadata rather than explicitly different run IDs, independent task families and source authority checks, actual writer-produced compression and longer reuse. Keep those pending rather than expanding beyond this run's resource boundary. Core FRR remains unchanged.
