# One missing-evidence rule: repetition is not application

Client 28 October 2026 America/Chicago; host 29 October UTC. User authorized the next narrow experiment while supplying DeepSeek material. This is a separate paired small-model development run following the [first FRR-base pilot](../smollm-frr-base-pilot-v1/REPORT.md), not an application of DeepSeek's variance gate. No weights were trained and no earlier cache/log history was replaced.

## Frozen comparison

Twelve authored items: four families with missing, measured-negative and measured-positive evidence. Pear sweetness, cold retention, a deterministic toy zero-effect definition and delivery rates with/without denominators. Four goldYES/fourNO/fourUNKNOWN. Two conditions receive identical records, question and common short-sentence output instruction: competent ordinary guidance versus a single concrete distinction that no measurement is unknown rather than failure or zero effect. No worked examples or teacher feedback. [Guidance](GUIDANCE.json), [cases/key](CASES.json), [protocol](PROTOCOL.md), [input freeze](FREEZE.json).

Ordinary guidance is25words/30tokens; the single-rule draft is26words/31tokens. They are near-matched, not exact word/token matches, and no post-outcome adjustment was made. The same pinned local SmolLM2-135M CPU model runs greedily, float32 eager/two threads, with96newtokens maximum. Condition order alternates across cases. One response per condition/item;24new terminal cache branches saved locally. Each is a separate inference context, not an independent statistical model or weight update.

## Observations

| Descriptive result | Ordinary | Single rule |
|---|---:|---:|
| Clear task decisions matching key | 5/12 | 2/12 |
| Appropriate unknowns on four missing-evidence cases | 2/4 | 2/4 |
| Ambiguous/incomplete or wrong-target decisions | 2/12 | 10/12 |
| Exact generic rule echoes | 0/12 | 10/12 |
| EOS before96token cap | 12/12 | 12/12 |
| One-sentence outputs | 11/12 | 10/12 |
| Input/output tokens | 1,468/136 | 1,480/158 |

Ten single-rule outputs are exactly “No measurement means unknown, not failure or zero effect.” That conditional rule is sound, but it does not decide the supplied case. The same text appears on cases with an actual measured pass, fail, zero and nonzero effect. It is not evidence that the model discriminates those states. We code the generic echoes as ambiguous application rather than treating a keyword as a task answer or calling the rule itself a false proposition.

On missing pear/battery measurements, both conditions explicitly acknowledge absent measurements; those are warranted unknowns even without the literal word UNKNOWN. On the unmeasured effect and missing denominator, ordinary instead makes definite claims; single-rule outputs remain generic. A post-outcome lenient interpretation credits the single-rule generic statement as an implicit unknown only on those two missing cases and credits ordinary's bare8-unit restatement as implicit failure against the10-unit threshold. That yields ordinary6/12 versus single-rule4/12. This is disclosed sensitivity, not a new trial or frozen alternate endpoint. Primary and lenient readings show no observed improvement for this draft on these items.

Root authored and manually scored with visible condition identities; no blinded/independent or population efficacy claim. [Raw prompts/tokens/unedited outputs](RAW_OUTPUTS.jsonl), [pre-score raw hashes](RAW_FREEZE.json), [scores and individual reasons](SCORES.json), [runner](run.py). Observed inference elapsed totals excluding serialization were about14.24seconds ordinary and16.23seconds single-rule; these are descriptive, not a timing benchmark. No retries or prompt/budget changes followed the outcomes.

## What this adds

The previous short-output limitation is not the immediate issue: all responses naturally terminate. Here the salient concrete instruction can be repeated fluently without being used as a case-specific decision rule. This suggests testing instruction-versus-data separation and example-based application next. It does not establish the causal neural mechanism, an internal frozen state, or general inability to learn the distinction.

This case set differs from the preceding FRR-base pilot. A change from its unknown-handling count is not an estimated treatment improvement across studies. Within this run, both conditions appropriately acknowledge two of four missing cases; measured cases and unsupported certainty remain important controls. Echoing a safe-sounding instruction is not automatically safe task behavior.

## Preservation and next directions

Before/after byte hashes verify86prior files unchanged, including model weights, previous cache branches and first FRR-pilot files. All24new actual terminal caches are saved under a new local state directory and their hashes verified. [Before](PRESERVATION_BEFORE.json), [after](PRESERVATION_AFTER.json). Complete prompt/output/token records and manifests are saved in GitHub; large binary tensors/weights remain local and depend on workspace durability. Last generated token/cache-boundary metadata remains explicit. No old branch was cropped, wiped, rewritten or trained on.

Keep this version as experimental. A next prospectively frozen comparison could distinguish giving a rule from showing its application, with matched examples/information and new questions. Another narrow contact could move guidance into a separate message and test whether that reduces rule echo, without changing record facts. Evaluate explicit decisions, justified unknowns, task-target fidelity and unsupported explanations separately. These are proposals, not post-outcome rescue runs or guaranteed improvements.

The parallel [DeepSeek intake](../deepseek-gate-intake-v1/REPORT.md) preserves useful selection/diagnosis questions while rejecting an unexercised universal variance gate. No source claim or new default habit is promoted from these small runs. Runtime/core/schema/queue and prior verdicts remain unchanged; no background work or automatic continuation.
