# SwaT screenshot source contact

29 October 2026 UTC. User shared a screenshot; this is a bounded source extraction, not a trained-model experiment. Identified [Swarm Telepathy: Prefill-Free KV-Cache Transfer Across Families](https://arxiv.org/html/2610.15095v1), arXiv:2610.15095v1, submitted 10 October 2026. Read methods, tokenizer alignment, training/evaluation, Table 3 and discussion, plus the official repository README at [ae2de2285caf82f4d500526bf6e6992747b98eea](https://github.com/Ar-Kareem/SwaT/blob/ae2de2285caf82f4d500526bf6e6992747b98eea/README.md). Repository implementation files, weights and result logs were not audited; no code/model execution or independent reproduction.

## What the paper adds

A pair-specific learned translator maps a sender's KV-cache into receiver-compatible cache tensors; both language models remain frozen. The receiver avoids its own full document prefill. The mapper still needs original text tokenized by the receiver and character-span alignment. Thus prefill-free is not text-unavailable operation. Single-message handoffs, not repeated transfer or multi-message composition, are the principal tested setting; the discussion leaves those extensions open.

The reported 40% average relative accuracy gain and roughly 4× timing gain concern SwaT plus Attention Matching versus summaries, across three pairs, seven datasets and five budgets. This is distinct from the broader seventeen-benchmark retention evaluation. Timing components include sender GPU work and receiver time-to-first-token, not demonstrated fourfold whole-research-workflow acceleration. Relative percent improvement is not forty percentage points. Matched cache-position budgets are not a universal equal-byte, equal-compute or equal-information guarantee.

## What the repository makes explicit

README describes roughly 300M translator parameters, reconstruction followed by next-token-loss training, and an additional small query-transfer model for compaction. Its documented comparison uses summaries at five detail levels, maps document caches, then compacts them to corresponding budgets. Receiver timing uses batch 16. These are source-described procedures, not executions observed here. Implementation and benchmark reproducibility remain unchecked.

## Usefulness for FRR and memory

Our [earlier C2C extraction](../cache-transfer-join-contact-v1/SOURCE_CONTACT.md) inspected cache fusion; SwaT targets a different boundary, bypassing receiver document prefill across model families. This is relevant to the user's [deferred chat-cache curiosity](../handoff-criterion-shift-v1/DEFERRED_CACHE_THREAD_IDEA.md). Present tools do not expose this session's KV-cache or let us install a cache translator inside the chat service. No chat-storage saving or host capability change follows from reading the paper.

Garden interpretation: a handoff might carry a translated working representation instead of only a written map. Our independent inference is that this changes the communication channel, not the obligation to check what survives. Preserving useful state does not certify its truth or applicability. Frozen weights mean the receiving model is conditioned by supplied state; these experiments do not establish permanent acquisition of a visual skill after that state is removed.

Strongest proposed bridge: test corrections and claim scope across matched transfer conditions. Include an old claim followed by its correction, a numerical acceptance rule whose median/maximum matters, unqueried facts, and questions outside the available evidence. Compare full text, summaries, uncompressed transfer and compacted transfer while accounting for bytes, mapper/alignment/compaction cost and final decoding. Measure source identity, negation, justified unknowns and error propagation separately from task score. Repeated handoffs and stale-source removal are lateral stress tests. These are proposals, not new executed trials or gaps proven absent from the entire literature.

No harness, core, schema or queue changes. Prior completed studies and failures retain their original status. No subagents, model training or background tasks were launched for this intake.
