# Independent protocol audit

6 November 2026. Read-only review of `run.py` and `PLAN.json` while the root's run was underway. No model calls, imports of model/runtime modules, code edits, primary-world access or changes to old studies. This audit does not certify run completion or any observed score. Read-only supplemental source inspection covered the imported generator, LoRA forward operation and paging response shape.

## Counts and matching

The actual design agrees with the root's stated fixed **48 calls**:

| Variant | Exact copying | Variation | Plain copying | Feedback continuations | Total |
|---|---:|---:|---:|---:|---:|
| Normal adapter scale | 16 | 8 | 4 | 8 | 36 |
| Scale-zero reference | 8 | 0 | 4 | 0 | 12 |
| Total | 24 | 8 | 8 | 8 | 48 |

`PLAN.json` contains the 40 static trials; four normal short-variation parent replies supply the eight continuation calls. Parents are reused, not generated again. There are 40 Scheme-dispatched calls and eight plain-copy calls. Consequently a reported “accepted Scheme actions” rate must exclude the eight undispatched plain replies. Normal adapter Scheme calls number 32; scale-zero Scheme calls number eight.

Static inspection verified both seeds, exact normal/reference subset matching, and identical short prompt suffixes in every broad pair. Both copy conditions receive the same complete target and copying instruction. The broad condition adds the old card. Thus answer availability is controlled within the card contrast. The code's current SHA-256 matches its saved PLAN pin at audit time.

The four normal copy targets are literal `(run 3)`, addition, definition and first value page. The reference includes literal and definition copies under both cards and both seeds, plus plain targets `hello` and `37`. It is a paired subset, not a full replication of all normal tasks. Variation uses two arithmetic tasks, with the same non-target example in both card conditions. Fresh setups have the same command/data but independently initialized world IDs/snapshot IDs; these IDs are not presented to the model.

## Fork and generation logic

The two continuation worlds are each imported from the same parent's final bundle. Neither branch starts from the other branch's output. Parent selection is fixed by block/short condition and includes successes and failures. Prior prompt, raw earlier reply, task restatement, next-command cue and second-turn seed match between branches. Receipt branch gets actual status/error/value; practice branch explicitly says the receipt is withheld. Pair prompts and input IDs are written together before either continuation call. Static parent prompts are saved before the first model generation, while continuation strings depend on actual parent outcomes under the frozen algorithm. Describe this as predeclared feedback construction and pairwise prompt freezing, not as all 48 literal prompt strings existing before the first call.

The prior reply is embedded as text inside a single new user message, rather than restored as a native assistant turn. This is matched across arms and therefore preserves the intended local contrast. Describe the intervention as re-prompting with prior output plus receipt versus prior output plus practice cue; do not generalize it to every conversational tool-feedback implementation. The practice phrase and receipt payload differ in content and length. This tests the full receipt presentation against that specific practice cue, not a pure error-information mechanism.

The imported generator source currently implements the declared 96-token, temperature .8, top-p .9 generation with a new per-call CPU RNG and fresh model cache. There is no carried optimizer or training step in the reviewed path. Each generation is saved before dispatch. Scale zero changes module scalar attributes in process after all normal calls, and the reviewed LoRA forward function multiplies its adapter contribution by that scalar. Tensor/file checks at the end are programmed, but their successful execution must be verified from completed artifacts. Reference runs always occur last, so any unmeasured time/state effect is not counterbalanced; fresh generator cache/RNG and eval mode reduce obvious carryover, without proving its absence.

## Material scoring and provenance limitations

1. **Page task scoring is more permissive than exact requested retrieval.** At `run.py:120`, success requires OBSERVED status and matching target/field only. It does not test `offset == 0`, requested page extent/count, chunk or complete projection. A different successful page of the same field could pass this scorer. The host validates cursor integrity, but that does not make the task scorer exact. Preserve the frozen score; if any page reply is accepted, inspect its saved full reply and receipt and report a separately labeled stricter audit result for first-page/extent fidelity. Do not silently replace the predeclared score. Literal match remains a strict independent measure of the supplied 32-character page command.
2. **Not every executed helper is pre-pinned.** PLAN code pins include `run.py` and prototype Python files, but omit `source-access-three-cycle-v1/generate_capacity.py`, `runtime_reference.py` and `/workspace/lora_cpu.py`. Source inspection establishes current behavior, not a pre-call hash commitment. Report the exact scope of saved pins; a later helper hash can document current files but cannot retroactively become preregistration. Also, `source_card_sha256` is the hash of the entire earlier PLAN file, not the card string alone.
3. **Definition task success is one behavioral witness.** The published reply plus `double(3) == 6` host probe is the declared task scorer. A constant-six definition can satisfy it. Exact literal match is stronger evidence of copying the intended definition. Do not call the single probe proof of correct doubling for arbitrary inputs. Host probes are separately labeled and must not count as model actions; final definition bundles include their audit records.
4. **Task score and accepted action are separate.** Arithmetic task success checks the returned integer/status, not whether the literal requested expression was emitted. Equivalent expressions can succeed with literal mismatch. Plain task success equals stripped literal match and has no dispatcher receipt. The decode step uses the existing `skip_special_tokens=True` behavior before outer-whitespace stripping; raw token IDs remain available. Report this decoding contract rather than claiming byte identity of the generated token stream.

No source-level counting or fork error was found that requires modifying or restarting this fixed run. The page scoring limitation and helper pin coverage should be disclosed in the report, with receipt-level page verification if relevant. Conclusions remain limited to these targets, two seeds, prompt formats and scalar intervention. Four continuation pairs cannot establish broad learning, and copying or single-probe success cannot establish general Scheme competence, autonomous free play or model-wide adapter quality.
