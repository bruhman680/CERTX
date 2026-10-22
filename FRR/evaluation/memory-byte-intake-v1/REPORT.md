# MB-C1: MemoryTax and byte-distillation screenshot intake

Selected primary reading; no experiments reproduced, models trained or pending tests replaced. User shared two screenshots after SR-C1. The current calibrated/noisy-reset extension and practical agent bridge remain open.

## Primary-source contacts

[MemoryTax, 2610.29823v1](https://arxiv.org/html/2610.29823v1): read main sections, result tables and protocol appendix. One LoCoMo conversation, one rollout per cell, default memory configurations and an LLM judge limit generalization. Agents received photo captions withheld from memory methods; on non-photo questions the strongest Pi/full-context comparison differs by one answer. Writer/reader swaps expose dependence on extracted records. Appendix B retries failed/empty trials and counts only accepted trials; reported cost therefore does not establish all-attempt deployment expense. No independent record-level omission audit was performed here.

[Breaking the Token Ceiling, 2609.12303v1](https://arxiv.org/html/2609.12303v1): read abstract, conversion methods, setup and discussion. An end-of-token symbol preserves termination probability omitted by the approximate byte conversion. This concerns the conversion target, not a guarantee the trained student exactly reproduces its teacher. Reported asymptotic gains are fitted extrapolations. Layer parameters are matched, total parameters differ; byte inference remains expensive and inference-cost-matched comparisons are outside scope. Lower bits-per-byte need not imply better downstream task performance.

An initial visual transcription used2610.29323, which resolved to an unrelated astronomy paper. Title checking caught the mismatch;2610.29823 was confirmed as MemoryTax. The unrelated source is excluded. Secondary search results were used only to locate the title; conclusions above use primary texts.

## Consequences for our designs — our inferences

- Match the information available to each condition, including metadata/captions, before attributing a performance difference to memory architecture. Measure actual access separately.
- Cross writer and reader where useful. Distinguish omitted information from failed retrieval, failed use, incorrect source data and evaluator error. An aggregate writer/reader gap alone cannot locate every failure.
- Preserve raw records plus navigable derivatives as a candidate architecture. Do not infer that either raw access or compressed memory always wins; include storage, preparation, retrieval, reuse count and update workload.
- Count all attempts, retries, failed tool calls and preparation costs; separately disclose accepted-run costs. This sharpens HI-C1's full-cost requirement.
- Treat representation boundaries as part of the information contract. Termination, scope, uncertainty and provenance can be lost while a transformed representation still looks well formed. This is a proposed cross-domain analogy, not a proved correspondence between byte conversion and agent memory.
- Evaluate downstream decisions as well as representation fidelity. A faithful target does not guarantee successful learning, access or action.

For the pending actual-agent bridge, retain the same-evidence access comparison, source lookup, missing/mismatched records and explicit uncertainty outcomes. A later compression condition should use actual writer-produced records, with raw-record fallback as a distinct arm. This intake adds no test family, scientific status promotion or core revision. It does not establish a universal memory ceiling, make model-training claims about untrained transformers, or alter SR-C1's scoped findings.
