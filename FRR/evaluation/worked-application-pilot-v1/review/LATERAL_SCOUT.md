# Bounded lateral scout: copying, format, and application

Read date: 2026-10-29. Scope: three primary/official sources; no models, inference APIs, installations, or datasets run/downloaded. This is a source-informed discrimination proposal, not an empirical finding about the pinned model.

## Contact with the current result

The parent supplied the following pilot context: pinned `HuggingFaceTB/SmolLM2-135M-Instruct`; previous single-rule guidance echoed verbatim in 10/12 cases; ordinary 5/12 versus rule 2/12 under primary manual scoring. I did not independently inspect those prompts, outputs, scoring, runtime, or model revision. The intended local pilot directory was absent at first read. Treat these counts as supplied context, not independently verified evidence. They motivate testing copying versus application but establish neither a neural mechanism nor a general inability to use demonstrations.

## Three sources and their decision value

1. **Official model card, HuggingFaceTB, SmolLM2-135M-Instruct.** Read model summary, usage, instruction evaluation, and limitations. The card reports IFEval average prompt/instruction 29.9 and warns about factual accuracy and logical consistency. Its usage examples apply a chat template; one example explicitly slices generated tokens after the input. This makes prompt serialization and prompt/output separation worth checking before calling an apparent echo generated copying. The card does not evaluate this pilot, worked-rule application, instruction/data boundaries, or missing-evidence decisions. Benchmark numbers do not estimate this task's accuracy. [Official card](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct)

2. **Min et al., EMNLP 2022, “Rethinking the Role of Demonstrations.”** Read abstract and PDF introduction/model table. Their classification/multiple-choice experiments show that demonstrations can help through label space, input distribution, and sequence format even when labels are randomized. Thus an improved answer prefix or valid output format is insufficient evidence of applying the demonstrated mapping. A mapping-corruption control that preserves format is directly motivated. Their listed core models start at 774M, and the work is not a test of this 135M instruct checkpoint or open-ended evidence reasoning. It does not establish the cause of the reported echoes. [Primary paper](https://aclanthology.org/2022.emnlp-main.759/)

3. **Yoo et al., EMNLP 2022, “Ground-Truth Labels Matter.”** Read abstract and targeted HTML sections on task difficulty, templates, size, prior-free labels, and limitations. They find mapping effects vary with configuration and warn that low sensitivity can accompany weak task performance. Their prior-free-label control separates label semantics from input-label correspondence. This cautions against interpreting equally poor correct/corrupt-demo arms as proof of format-only use. Their model-size analysis spans 1.5B–175B; it does not directly predict SmolLM2-135M-Instruct. Their own limitations acknowledge prompt sensitivity and entangled demonstration factors. [Primary paper, v2](https://arxiv.org/html/2205.12685v2)

## Missing evidence and boundaries

None of these three sources directly demonstrates that this checkpoint distinguishes an explicit negative fact from an absent fact, or maintains an instruction/data boundary on the pilot. Absence of relevant source evidence is not evidence that the model cannot do so. Likewise, no direct evidence here identifies attention, induction heads, decoding, training contamination, or capacity as the echo's cause.

Keep “explicit negative evidence” and “no supporting evidence provided” as different gold conditions. Do not count a correct abstention prefix as correct evidence handling if the content invents a fact. The boundary probe below tests sensitivity to a declared role for a block; it is not a prompt-injection security evaluation.

## One smallest discriminating test proposed, not executed

Use three existing, independently scorable held-out cases: one supported positive, one explicitly negative, and one missing-evidence case. Prefer cases already solved by the ordinary baseline; if that coverage is unavailable, mark task competence unresolved and retain the relevant ordinary baseline output. Do not use test queries as demonstrations.

For each case make one 2×2 matched probe (12 continuations total):

| Factor | Level A | Level B |
| --- | --- | --- |
| Demonstration mapping | Correct worked input→answer pairs | Same inputs, same answer inventory and formatting, answer assignments permuted |
| Declared role | Block declared worked examples to apply | Same block declared quoted document data, not guidance; task instruction outside block unchanged |

Use a balanced demonstration set covering all three decisions so permutation preserves answer counts. Keep query, answer prefix, chat serialization, decoding settings, and output allowance fixed. Keep answer tokens and prose lengths as close as feasible; record residual length differences. Log raw generated continuations separately from the serialized input, verify that the evaluator did not include prompt text, and score task decision, evidence grounding, format validity, and literal echo separately. Count missing-evidence and explicit-negative accuracy separately.

Reading of outcomes: correct mappings improving decisions over permuted mappings in the apply arm supports use of demonstrated correspondence on these cases. Equal format gains with no decision gain remain compatible with format priming, copying, or insufficient competence. A role-dependent change supports sensitivity to the declared boundary; no change alone cannot distinguish boundary failure from task/prompt failure. A successful ordinary baseline makes poor demonstration arms more informative, while a failed baseline leaves a competence confound. Twelve continuations provide a discriminator, not a reliable effect-size estimate or a mechanism claim.

This bounded probe does not require a new corpus. External data collection can proceed if independently useful; these sources supply no basis for requiring it to wait and no basis for prescribing a large ingestion sweep.
