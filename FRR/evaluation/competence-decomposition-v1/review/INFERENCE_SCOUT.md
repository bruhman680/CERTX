# Bounded inference scout: delegate computation, preserve the uncertain boundary

29 October 2026, America/Chicago. User requested a parallel scout for inference concepts useful to FRR. Read the current handoff, DM-C1 report, optional verification/evidence-gated-feedback modules, and three primary papers below. Selected-section extraction; no systematic review, code reproduction, model execution, training, model download or paid service. Historical files are unchanged.

## Three primary contacts

### 1. PAL: language compilation and trusted computation are different jobs

[Gao et al., PAL: Program-aided Language Models, ICML 2023 published PDF](https://proceedings.mlr.press/v202/gao23f/gao23f.pdf). Inspected abstract, introduction, section 3 and section 4 setup. PAL generates a program from natural-language input and delegates execution to an interpreter. Its prompts use meaningful variable names to maintain entity roles; experiments use a code-capable Codex backend and task-specific examples. The published results do not establish that our 135M checkpoint can compile reliable programs or extract correct inputs.

**Local extraction:** separate extraction/source binding from arithmetic execution. For the present threshold task, a narrow typed record and fixed comparator are sufficient; unrestricted generated Python is unnecessary. Score whether the model copied the actual measurement and criterion before crediting the comparator's answer. A correct program over wrongly extracted numbers remains a wrong task result. Interpreter correctness does not authenticate source facts. This is an architectural inference from the paper, not a PAL replication or observed FRR benefit.

### 2. Grammar alignment: syntax and probability preservation are separate contracts

[Park et al., Grammar-Aligned Decoding, arXiv:2405.21047v1](https://arxiv.org/html/2405.21047v1). Inspected abstract, section 2 equations/grammar-constrained counterexample, and section 4 discussion/limitations. Ordinary next-token masking checks whether a prefix has some grammatical completion; conditioning on the whole grammar also weights how probable such future completion is. Thus a syntactic guarantee does not itself preserve the globally conditioned distribution. Their ASAp proposal addresses distributional alignment, but convergence can be slow and downstream correctness need not improve.

**Local extraction:** record three separate endpoints: parse/schema validity, source/semantic consistency, and warranted task outcome. A JSON parser or finite label constraint is useful infrastructure; it is not a truth verifier or confidence calibrator. Do not silently describe restricted uppercase label weights from DM-C1 as complete-answer probabilities or an implemented constrained decoder. A future constrained/free comparison needs matched prompts, format and generation budgets. Implementing ASAp is not currently justified for a tiny deterministic threshold diagnostic.

### 3. Uncertainty elicitation is not an automatic small-model capability

[Kadavath et al., Language Models (Mostly) Know What They Know, arXiv:2207.05221v4](https://arxiv.org/html/2207.05221v4). Inspected sections 1.2, 4.1–4.2, 5/5.2 and 6.1. Their model series starts at 800M; smaller models were excluded for poor task performance. Inference-time P(True) asks whether a proposed answer is true, but zero-shot calibration is poor and prompting matters. P(IK) is a different experiment: it finetunes the entire model with a value head. Generalization/calibration can degrade on new tasks.

**Local extraction:** do not import a trained knowledge classifier or larger-model calibration result into our inference-only 135M setup. Explicitly allowing UNKNOWN does not demonstrate reliable abstention; DM-C1 already witnesses that. Before using a confidence threshold, evaluate acceptance error and coverage on separately held examples with explicit labels. For now, source-checked absence can justify a domain UNKNOWN, while a failed parser/extractor should remain an infrastructure-level unresolved result. These have different causes and should not be merged.

## Integration recommendation, ranked by present warrant

1. **Ready as a narrow build:** a fixed comparator consuming a typed, source-bound pair of numbers and a declared comparison relation. Validate type, unit/target compatibility, required fields and an explicit missing-measurement state. Return a receipt that exposes the inputs actually used. Keep extraction accuracy and final decision accuracy separate. Never substitute the threshold itself for an absent measurement.
2. **Ready as guidance:** distinguish observation/extraction, formal computation, output serialization, and task acceptance. A failed upstream stage should not be made to look correct by a well-formed downstream label. The existing optional verification and evidence-gated-feedback modules already support this separation; a short linked worked example is preferable to another universal controller.
3. **Experiment only:** compare direct answering against model extraction plus trusted computation on the same authored sources, with exact prompts/token costs and all failures preserved. Add oracle supplied-input computation as an instrument check, explicitly counting its extra information. Do not call oracle success an agent improvement. For constrained outputs, separately test whether merely fixing serialization changes semantic errors.
4. **Defer:** model self-confidence gating, self-consistency majorities, iterative self-repair or grammar-aligned sampling as defaults. Without task competence, calibration or an independent acceptance check, they can repeat or tidy the same error. This scout did not test those methods and does not claim they are generally ineffective.

## A useful lateral distinction

There are at least three reasons a pipeline can withhold an answer: the source explicitly lacks a required observation; access/extraction failed despite a potentially available observation; or a validly represented observation does not determine the requested decision. The outward word “unknown” can hide these different repair routes. Preserve their causes so the next action can be missing-data collection, retrieval/parser repair, or a genuinely different inference. This is a proposed bookkeeping distinction; behavioral benefit has not been measured.

Hashes/source IDs can bind a receipt to bytes but cannot establish that a source is true or applicable. The instrument's declared relation and units remain assumptions to check against the task. Nothing here validates universal FRR constants, trains the little model, or changes queue-family completion.

## Access and scope record

Public web search located sources; findings above were checked against primary PDF/HTML. PAL: selected pages 1–4, not all 36 pages or repository. Grammar-Aligned Decoding: selected sections 1–2 and 4 limitations; no theorem proof audit or implementation run. Knowledge paper: selected protocol/model/generalization/limitations sections; no calibration reproduction. No claims depend on social-media summaries. A recent constrained-decoding paper surfaced in search but was not opened or used as evidence. Only this new note is written by this scout.
