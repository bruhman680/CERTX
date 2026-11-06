# Scheme command calibration: copying, task binding, feedback and adapter reference

6 November 2026 America/Chicago. **56 bounded local model calls; no training, primary continuation or runtime change.** Forty-eight calls followed a fixed plan, then eight followed a separately frozen adaptive example-content plan. Every reply is preserved; no retries or output repairs.

## Main finding

The small model can sometimes emit executable Scheme commands when the full command is supplied. That does not yet transfer to choosing operands from a request. A non-target example repeatedly became the generated computation. Changing that example changed the operands in the output while requested sums stayed fixed.

This narrows the previous 0/10 interface result. It does not establish general Scheme competence, inability, an internal cognitive mechanism or continuous learning. The interface/world and original model weights remain unchanged; prompts and the declared process-local adapter reference are the interventions.

## Protocol and review

[Frozen main plan](PLAN.json): two new fixed seeds 110611/110612, unchanged 96-token output limit, temperature .8/top-p .9, CPU float32/eager/two threads. Original cached SmolLM2-135M-Instruct plus canonical readout LoRA. Original adapter contribution for 36 calls; scale-zero reference for 12. [Reference config](REFERENCE_CONFIG.json) records LoRALinear contribution scales 2→0 in that diagnostic process, with trained/base tensor digests and asset files unchanged. This is not training, erasing tensors or changing the primary deployment.

The 40 static prompts/IDs were sealed before generation. The eight feedback continuation prompts require actual first replies; each pair was sealed before either continuation call, under the predeclared recipe. They were not all fully instantiated before the first model call.

Main blocks:

- **Literal copying:** four complete Scheme targets × short/broad card × two seeds = 16 normal calls. Both cards receive the identical literal target and final copy instruction. Broader context changes length/content together.
- **Near variation:** two requested sums × two cards × two seeds = 8 normal calls. Both cards share the non-target `(run (+ 1 1))` example; the requested full answer is absent.
- **Receipt feedback versus practice:** reuse the four short-card variation replies as first turns. Fork their exact post-dispatch world/transcript into two equally budgeted continuations = 8 normal calls. One receives actual status/error/value, the other withholds it. No new first turn is counted.
- **Ordinary copying:** `hello` and `37`, two seeds = 4 normal calls, not dispatched as commands.
- **Reference subset:** the same ordinary copies plus literal `(run 3)` and definition copies under both cards/seeds = 12 calls. These prompts, IDs and seeds match their normal counterparts. No reference addition/variation/feedback result was measured.

[Independent control review](CONTROL_REVIEW.md), [protocol audit](PROTOCOL_AUDIT.md) and [result review](RESULT_REVIEW.md) distinguish the suggested design from the actual chosen 48-call matrix and preserve caveats. Prior reviews were available before the adaptive follow-up; no reviewer ran extra model calls or changed the sources.

## Main outcomes

| Original adapter condition | Calls | Exact literal matches | Accepted Scheme actions | Requested outcomes |
|---|---:|---:|---:|---:|
| Scheme copy, short | 8 | 1 | 1 | 1 |
| Scheme copy, broad | 8 | 2 | 2 | 2 |
| Sum variation, short | 4 | Not scored | 2 | 0 |
| Sum variation, broad | 4 | Not scored | 0 | 0 |
| Receipt continuation | 4 | Not scored | 2 | 0 |
| Practice continuation | 4 | Not scored | 2 | 0 |
| Ordinary text copy | 4 | 3 | Not dispatched | Literal-only score |

All three normal successful Scheme copies were the explicitly supplied `(run (+ 2 3))`. They executed to 5. Literal `(run 3)` replies instead included `(RUN 3)`, `RUN 3` and `3`; case/structure changes remain strict failures. Short definition copies omitted a closing parenthesis; broad replies used fragments such as `(double 1)`. No normal definition or page request executed. None was silently repaired. All 56 generations ended with EOS; none reached the 96-token limit. Both short definition near-copies stopped after 11 tokens, so those missing parentheses were not output-cap truncations.

Both accepted initial variation replies computed the supplied example 1+1→2, not the requested 2+3→5 or 4+7→11. Other replies reproduced that example with missing delimiters, extra prose or invalid nesting. **Correct engine execution is distinct from requested-task alignment.** The original adapter has 9 accepted Scheme actions across 32 Scheme turns, including dependent continuations, but only 3 assigned outcomes—all supplied-command copies. Do not pool these as independent trials.

Feedback/practice both had 2/4 accepted continuations and 0/4 requested outcomes, with no paired acceptance/task discordance. Two parents had valid-but-wrong-task calculations, so their receipts reported correct execution of 2 rather than an engine error. Two parents had syntax failures. This is not task-aware corrective feedback and does not show that all forms of feedback or self-correction fail. History was embedded in a single user message, not an assistant-prefill or persistent KV-cache condition.

### Adapter reference: a mixed local tradeoff

On the matched literal/definition subset, normal condition had 0/8 successful copies; scale-zero reference had 3/8: one literal and two full supplied definitions. The reference definitions were published and host-probed at double(3)=6. Both exactly matched the supplied source; they were not independently designed programs. The single-input host probe alone would not establish a general doubling function.

Ordinary-copy results went the other way: normal 3/4 exact versus reference 0/4. The reference sometimes added unrelated text. Addition, where normal copying worked, was not tested in the reference. These tiny selected contrasts do not support a general model/adapter ranking or a decision to disable the original adapter.

## Adaptive example-content contact

After observing variation replies repeat the example, froze an [eight-call follow-up](example_probe/PLAN.json). Reused the four original short-card example 1+1records; generated four no-example and four example 8+9 conditions with the same requested sums/seeds. The 8/9 prompts have equal token length and exactly two changed token IDs versus the matched 1/1 prompts. The no-example condition is shorter, so example presence and length are bundled there.

| Condition | Calls | Executed actions | Requested sums correct |
|---|---:|---:|---:|
| Example1+1, reused | 4 | 2, both returned 2 | 0 |
| Example8+9, new | 4 | 2, both returned 17 | 0 |
| No example, new | 4 | 0 | 0 |

All four 8/9 replies reproduced the example's operands; two were exact executable commands, two lacked the outer parentheses. This supports a **content-specific example-attraction observation under these prompts/seeds**, not a diagnosis of internal attention or proof that every example is harmful. No-example replies were not usable commands. A shell-looking string in one raw reply was treated as parser input and rejected; it was never sent to a shell. [Adaptive results](example_probe/SUMMARY.json).

## What the knowledge scout adds

[Primary-source scout](KNOWLEDGE_SCOUT.md), with read depth and scale limits:

- The [official SmolLM2-135M-Instruct card](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct) qualifies its advertised function calling as for 1.7B. “Instruct” is not evidence of Scheme/tool training in 135M.
- [Transformers chat-template documentation](https://huggingface.co/docs/transformers/en/chat_templating) motivates preserving actual rendered/tokenized roles and continuation boundaries. This study uses the tokenizer's chat template once with assistant-generation marker; no prefix or grammar constraint was tested.
- [Grammar-constrained decoding](https://aclanthology.org/2023.emnlp-main.674.pdf) motivates separating syntactic validity from argument/selection correctness. Its much larger-model results are not predictions for this model. Restricting to a gold command would supply the answer.
- [LoRA learning/forgetting research](https://arxiv.org/html/2405.09673v2) distinguishes target adaptation from retained capabilities. Our local reference is direct evidence only for these prompts; the paper's larger-model numerical findings are not transferred.

## Verification and scope

[Record checks](RECORD_CHECKS.json) verify all 56 saved records, reconstruct 48 command worlds, preserve exact request-retry receipts, check prompts/IDs/seeds/decodes/stops, match 12 reference prompt/seed pairs, and confirm four feedback forks began with byte-identical exported worlds. Eight ordinary-copy calls have no world dispatcher. No extra generations or weight load occurred in the verifier. Original strict scores are retained; reconstruction is not a stochastic model rerun.

The main plan pinned the driver, world sources, profile and model assets, but did **not** include every inference helper in its own code_pins list. Two primary helper files were additionally covered by root's pre-study protected inventory. The independent audit records the remaining pin-closure limitation. The adaptive plan explicitly pins its inference/LoRA helpers before its calls. Do not retroactively describe the main plan as having pinned all executed library code.

Page task scoring was permissive (target/field rather than complete first-page checks), but no page reply was accepted, so that defect changes no observed success here. Future page scoring should verify offset/content/cursor too. Two seeds, few targets, a source-trained adapter and adaptive follow-up limit generality. No decoder repair, grammar forcing, training, new model download, paid inference, primary change or permanent adapter-scale change occurred.

## Refinement and next strongest

Added optional [computational action evidence guidance](../../modules/computational-action-evidence.md): separate copying, parsing, execution, goal alignment, publication and reuse; record assistance and host transformations; distinguish execution receipts from task-aware feedback. The guidance itself has not been efficacy-tested.

Next use **counterbalanced command selection** with two legal candidates and swapped order, then argument binding with held-out values if selection works. This diagnoses intent-to-command mapping without declaring the full world a task menu. Keep unconstrained outputs and any syntax aid as separate conditions. Do not start a long free-play season or change the primary on the evidence here.

Original garden: entry 500, number 0, verifier 0096, PAUSE present; all 1,504 protected non-bytecode files unchanged. Previous portability study’s 82 files unchanged. Base/adapter files/tensors retained; no updates. [Preservation](PRESERVATION.json). Earlier interrupted-session unknowns remain unknown; old reports and source outputs are intact, with prior navigation in `before/`.
