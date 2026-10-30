# Prospective design and scoring review

Reviewer read the preceding worked-application report, its frozen scoring contract and runner before the new outputs existed. This is design/outcome judgment by another agent, not independent scientific replication. Review applies to a bounded 27-generation proposal: nine new threshold tasks crossed with no examples, correct labels and cyclically permuted labels. Ordinary guidance is held fixed; no FRR-named intervention is tested here.

## What the control can distinguish

Correct/permuted arms should contain identical demonstration facts, questions, ordering and wrappers. Change only the demonstration answer labels by YES→NO, NO→UNKNOWN, UNKNOWN→YES. Retain all three labels once each. Measure actual tokenizer lengths before generation; do not infer matched token counts from equal word counts. Equal aggregate counts alone do not mean each label position has identical token identity or conditional influence. The no-example arm is a structural reference, not an equal-information/equal-input-token control.

All task gold labels follow the target records and threshold rule, independent of the deliberately incorrect demonstration labels. Target labels must remain absent from the prompt as evaluator metadata, but the target facts legitimately determine them; do not call these questions answer-hidden or held out. Preserve the intentionally misleading demonstrations explicitly in the artifacts and report. A response shift under permutation shows conditional sensitivity in these authored inputs. It does not establish semantic mapping acquisition, permanent learning, an internal mechanism, or a general gain/harm from examples.

Use three tasks of each gold label, with new entities/numbers. State that threshold comparison includes equality. Missing measurement warrants UNKNOWN; a number appearing solely as the criterion is not a measurement. To avoid accidental source ambiguity, examples use a distinct entity and units from targets and actual task begins with a clear boundary. Rotating arm order is reasonable bookkeeping; independent fresh model calls and caches must prevent cross-call history. Do not tune inputs after outputs.

## Scoring contract recommended before freeze

Record these separately for each generated text:

1. **Surface label:** the literal leading YES/NO/UNKNOWN if present. A demonstration copied from the prompt may have a surface label without answering the target. Missing label is NONE, incompatible unqualified labels are AMBIGUOUS.
2. **Explicit task decision:** leading YES/NO or an unambiguous target-directed acceptance/rejection counts; explicit UNKNOWN requires a target-directed cannot-determine/unknown/insufficient-information statement. A generic conditional rule is not such a decision. If the entire answer instead concerns the demonstrated entity/task, this field is NONE and target mismatch is true, even if its surface label coincidentally matches gold.
3. **Evidence-sensitive task status:** start with the explicit task decision. Without one, a case-specific acknowledgment that the required target measurement is absent can count UNKNOWN. Bare numeric restatement or a generic conditional rule remains AMBIGUOUS. Do not silently convert an answer to NO because a human can calculate it from copied numbers.
4. **Full warrant:** task status matches the frozen record-based gold and the answer contains no material false criterion, fabricated measurement, wrong source/entity or unjustified comparison. A clear bare correct decision can qualify when no explanation was requested. For missing evidence, require acknowledgment of the actual missing measurement if an explanation is provided; do not demand a long explanation. Correct direction plus a false explanation does not qualify.
5. **Target mismatch / wrong-entity echo:** mark when answer addresses the demonstration rather than the target. A target-directed answer with an incorrect invented quantity is an explanation/source error, not automatically a wrong-entity answer.
6. **Exact demonstration echo:** mark only substantive copied demonstration content (entity, quantities or a whole labeled demonstration block), not YES/NO/UNKNOWN alone. In these arms the answer labels are intentionally the same vocabulary as valid task answers, so a bare label cannot identify echo. Preserve a verbatim copied span where present.
7. **Generic rule echo:** answer repeats instructions/conditional threshold rule without applying it to this target. Can coexist with other flags if text also includes a decision.
8. **Material explanation/source error:** extra false or unsupported explanatory facts or rule. Keep **unsupported certainty on missing evidence** separate: a bare wrong YES/NO for an unmeasured target has unsupported certainty but no additional fabricated explanation. If an invented measurement is added, both flags can be true. Never implement blanket clearing of explanation-error flags from uncertainty flags.
9. **Stop/completeness:** EOS versus cap and incomplete/clipped answer separately. EOS is not proof of semantic completion; capped answers are not automatically false.

Report counts separately for task-decision match, evidence-sensitive status match, fully warranted answers, echo and source error. Do not collapse them into a single success score. Report the paired per-item transitions between correct and permuted arms, including unchanged outputs, so one incidental matching label is not treated as rule understanding. A cyclically shifted answer is a useful secondary descriptor, but remains an evaluator relation, not evidence of an identified neural operation.

## Review procedure

Root should freeze source cases, gold/bases, demonstration sets, guidance, design, scoring contract and runner before generation. Freeze raw outputs and root scores before this reviewer receives a shuffled packet containing target records/question/gold/output only. Reviewer should not read condition mappings, prompts or root scores during outcome coding. Shared filesystem masking is instructional, and response style can reveal arms. Preserve initial independent judgments and reconcile append-only. Never overwrite historical files or old caches; create a new local state directory. Save input/output token costs and actual runtime without extrapolating billing or energy.

If the frozen design materially differs from this proposal, record its differences and obtain a prospective read before inference. No model run or outcome inspection was performed by this reviewer in preparing this note.

## Final pre-generation read

Read CASES.json, DESIGN.md, run.py and INPUT_COSTS.json before generation. Nine threshold cases are balanced three per gold label; the missing-measurement instruction explicitly resolves the question wording in favor of UNKNOWN. Correct/permuted full prompts have identical recorded tokenizer lengths per item (280–284), while no-example prompts have135–139tokens. Runner creates a fresh cache per call, decodes only generated IDs, rotates arm order, saves separate terminal cache files and refuses existing cache filenames. It checks frozen inputs before model loading. No semantic retries/training occur in the runner. No blocking design change requested. Final SCORING_CONTRACT.md saved at study root; freeze it before inference.

Design difference from initial recommendation: Rod Indigo examples and Beam Silver targets share cm units, while entities and values differ. This is a limited near-transfer case, not a uniformly distinct-unit transfer design. Do not claim all demonstration/target units are distinct. Coordinator reports adding an existing-raw-output refusal before freeze; this adds execution protection and does not alter the scientific contrast.
