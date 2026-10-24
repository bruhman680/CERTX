# RA-C1: actual readers, current evidence and read access

This is a bounded authored follow-up to MEM-04 and [HI-C1 StageA](../harness-interface-contact-v1/DESIGN.md), following the user-authorized upstream application pass. The [protocol](PROTOCOL.md), [facts](FACTS.json), [rendered packets](PACKETS.json) and [hash bindings](PACKET_HASHES.json) were saved before participant calls. A separate reviewer checked the two renderings for exact fact equivalence before final record replies. Guidance, source facts, access rules and required decisions are the same; structure/whitespace differ.

## Execution

Four fresh contexts (`fork_turns=none`) were assigned prospectively raw,structured,structured,raw. Each saw three tasks and had one lookup turn plus one final turn. Every reader requested A/B/C; the coordinator returned only the frozen requested records, with no gold answer or corrective feedback. [RESPONSES.json](RESPONSES.json) retains copied final-message payload text and parsed JSON; [SECOND_MESSAGES.json](SECOND_MESSAGES.json) retains the delivered reply text. No private internal reasoning is recorded.

Eight participant turns, four parent reply messages and12 requested records; no outcome retries, re-prompts, exclusions, hidden extra cases or reader recontact. Shared model/platform ancestry and physical workspace persist; isolation is instructional, not a security boundary. Actual backend model, reasoning effort, tokens and elapsed compute were not exposed. Equal turns do not mean equal compute. Authority and domain rules are fixture premises, not authenticated facts about real systems. No real shipment/release was approved or rejected.

## Results

| Format | Contexts | Final decisions | Warranted | Conclusive grounded rejections | Appropriate unresolved | Unsupported conclusive |
|---|---:|---:|---:|---:|---:|---:|
|raw|2|6|6|2|4|0|
|structured|2|6|6|2|4|0|

All first responses requested originals and kept preliminary decisions unresolved. After lookup:

- A: four readers used current P31 revision2,8.4C to reject the8C release rule; they did not rely on revision1's7.8C summary.
- B: four readers recognized the returned zero-failure artifact as R61/K61, which cannot substantiate the requested R62/K62 decision. They did not infer that R62 failed its tests.
- C: four readers preserved locked/inaccessible mass evidence as unresolved, without treating unavailable decoded content as proof of absence or failure.

The12 decisions are clustered in4contexts, not12 independent readers. Four cases reach a conclusive task determination; eight warranted unresolved cases are not eight additional completed external tasks. Both formats tie; no benefit from formatting is established. The raw rendering is compact JSON-like event text, not an unstructured natural conversation; the structured view is pretty JSON with the same data, not a semantic extraction/indexing system.

[score.py](score.py) checks packet-relative decisions and simple source-binding substrings, JSON preservation, lookup counts and word caps; [RESULTS.json](RESULTS.json) records all cells. The scoring implementation was written after replies, implementing the previously saved criteria; no label or threshold was retuned. Mechanical substring scoring is limited; a separate [semantic review](../upstream-application-v1/review/READER_SEMANTIC_REVIEW.md) checks what the answers actually say. The parent authored/scored the cases and was unblinded. The reviewer shares parent context/platform and knew the packet warrants; it is separate inspection, not blinded or independent empirical replication.

Prompt whitespace-word totals were296raw versus418structured; returned-record totals114raw versus100structured. Response totals256raw versus366structured include JSON formatting differences. These are record counts, not token/latency/cost estimates or stable efficiency effects.

## Scope and next boundary

This tests actual reader behavior across source-access boundaries, with overt source identifiers and simple rules. It does not establish learning, general FRR benefit, real source authenticity, long-memory performance, adversarial authority detection or writer-produced compression. No label directly says a source is wrong, but the required/current identifiers are visible cues; reader success does not remove that support.

The next informative extension could reduce those cues, independently author ambiguous cases, use a real writer-produced handoff, or measure source-dependent behavior under controlled record changes. No such extension was silently added after seeing perfect/tied outcomes. Earlier MS-L1 and HI-C1 retain their original scopes; broader MEM-04 stays partial.
