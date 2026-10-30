# Wording, number form and source frame: three adaptive contacts

30 October 2026, America/Chicago. Parent commit `dafd3a9b3055c7a194ad62e55f805ec3d1698906`.

**The strongest new observation is a source-frame effect on the reader's number roles.** Completing the missing question comparison did not improve its aggregate score. A subsequent number-form hypothesis failed a controlled countertest. Returning to the difficult values then separated two source-frame packages:0/4correct with a passive-event frame,4/4 with a there-are attribution frame. This is a small behavioral contrast, not a general repair or a neural explanation.

Unlike the prior prespecified three-phase run, these are genuinely sequential contacts: WC-C1 completed first; its remaining role errors motivated NF-C1; NF-C1's16/16successes motivated SF-C1. Each protocol, cases, keys, runner and preservation manifest was separately hash-frozen before its own new inference. Later protocols were chosen after seeing earlier results; they must not be relabeled as a single preregistered confirmatory study.

## Cycle 1: complete the missing question/source comparison

[WC-C1](../reader-wording-cross-v1/REPORT.md) gives the eight exposed CR-C3 short sources exactly the already specified CR-C2 question for their known task family. It preserves the original source text, gold key, guidance, model and64-tokencap; saved CR-C3 outputs provide the original-question control. Neither the source nor the wording was newly optimized here.

| Family | Original question, saved control | Reworded question,8newcalls |
|---|---:|---:|
| Soil grouping | 1/4 | 2/4 |
| Both reset values supplied? | 3/4 | 2/4 |
| Total | 4/8 | 4/8 |

The rewording gains N2's eight-soil answer and N6's recognition that supplying only qA does not supply both q values. It loses N5/N7: both nonzero supplied values and both zero supplied values are now denied. Thus the same total again conceals gains and losses. One count case has equal target and observation values (8/8), so its correct value alone cannot certify discrimination of number roles.

For the difficult32/2counts the reworded reader still answers2instead of32, and32distinctsoils instead of2. It even mentions2later in the latter answer; that does not repair the false32claim. The simple absent-count source remains correctly recognized. All8calls reach EOS, strict bare-format0/8; semantic scoring accepts clear sentence answers. This completes the missing crossed cell, not an independent new-data validation or a globally superior prompt.

Inputs/chronology: [protocol](../reader-wording-cross-v1/PROTOCOL.md), [basis/pairs](../reader-wording-cross-v1/BASIS.json), [keys](../reader-wording-cross-v1/KEYS.json), [freeze](../reader-wording-cross-v1/FREEZE.json), [raw](../reader-wording-cross-v1/RAW_OUTPUTS.jsonl), [scores](../reader-wording-cross-v1/SCORES.json), [summary](../reader-wording-cross-v1/SUMMARY.json). A [chronology clarification](../reader-wording-cross-v1/REVIEW_CHRONOLOGY_NOTE.md) corrects the interpretation of the raw-stage label: all8outputs had been viewed at completion before structured scoring, rather than only a partial subset. Input/raw hashes remain unchanged, and no masked or independent review was claimed.

## Cycle 2: test the tempting number-word explanation

The remaining source-role failures suggested a possible upstream display issue: soil counts were written as words while observation counts used digits. [NF-C1](../number-format-role-v1/REPORT.md) tests that possibility rather than accepting it.

Four new authored base pairs `(soil count, observations per soil)` are `(4,12),(12,4),(3,24),(24,3)`. For each, independently render each number as digits or English words. The source syntax and existing C2 grouping question remain fixed:

`There are {T} independently sampled soils. Each soil supplies {O} observations.`

| Target form | Observation form | Correct |
|---|---|---:|
| Digits | Digits | 4/4 |
| Words | Digits | 4/4 |
| Digits | Words | 4/4 |
| Words | Words | 4/4 |

**All16answers are correct.** Within each base record the output text is identical across its four variants. No answers use the foil observation count. All calls reach EOS. Responses are full sentences, so strict bare-format0/16, independent of semantic correctness.

This does not support number words alone as a sufficient explanation of the earlier errors. It also does not prove global number-form invariance or say that model states/logits are identical: only generated answers/text were compared. The scaffold and some values differ from the earlier failing sources; that is why the next contact returns to the difficult values under controlled frame variation. NF does not by itself isolate syntax as the missing cause.

[Protocol](../number-format-role-v1/PROTOCOL.md), [factorial design](../number-format-role-v1/DESIGN.json), [cases](../number-format-role-v1/CASES.json), [keys](../number-format-role-v1/KEYS.json), [freeze](../number-format-role-v1/FREEZE.json), [raw](../number-format-role-v1/RAW_OUTPUTS.jsonl), [scores](../number-format-role-v1/SCORES.json) and [summary](../number-format-role-v1/SUMMARY.json) preserve this negative test of the proposed explanation. Nothing was rewritten or trained to make it succeed.

## Cycle 3: return to32/2and cross the source frame

SF-C1 uses `(T,O)=(32,2)` and `(2,32)`. Observation counts stay in digits. Cross target form (digits/words) with these two source-frame packages, keeping the instruction, C2 question, model and cap fixed:

**Passive-event frame:**

`{T} soils were sampled independently. Each soil supplied {O} observations.`

**There-are attribution frame:**

`There are {T} independently sampled soils. Each soil supplies {O} observations.`

The intended answer to the soil-count question is the same within each base pair. These strings are not declared equivalent for every possible temporal or linguistic claim: tense, adverb position, initial capitalization and syntax change together as parts of the frame package. The contrast does not isolate which feature matters internally.

| True soil count | Observations/soil | Passive, target digits | Passive, target words | There-are, digits | There-are, words |
|---:|---:|---:|---:|---:|---:|
| 32 | 2 | 2: wrong | 2: wrong | 32: correct | 32: correct |
| 2 | 32 | 32: wrong | 12: wrong | 2: correct | 2: correct |

Passive0/4versusthere-are4/4. Aggregated target-form correctness is the same for digits and words (2/4each). Yet one wrong word-form response invents12, so do not generalize this into “the model always copies the other visible number” or “number form has no effect on output.” Three errors use the observation-count foil; one invents a third number.

The passive-word32source exactly repeats WC-N1's prompt. Input and generated token IDs match, confirming the repeated failure under the same procedure. It is exposed repeat evidence, not an independent scientific replication. The other variants are newly authored here; all remain a small fixture set, not a hidden population sample.

All8calls reach EOS. Strict bare-format0/8, semantic matches4/8. There was no continuation, retry, fine-tuning, optimizer or source rewrite applied to an old record. [Protocol](PROTOCOL.md), [cases](CASES.json), [keys](KEYS.json), [basis](BASIS.json), [freeze](FREEZE.json), [raw](RAW_OUTPUTS.jsonl), [scores](SCORES.json) and [summary](SUMMARY.json) preserve the full contrast. All8outputs were viewed in the completion check before structured scoring, explicitly disclosed in the raw-stage receipt; review is not blinded.

## What this supports, and what it does not

The simple number-word explanation was too broad. In these controlled fixtures, the supplied source frame changes whether the small reader assigns a visible quantity to the requested role. That gives us a useful next experimental variable. “Fragile source-role reading” is a description of generated behavior, not a discovered neural circuit or a proof about internal reasoning.

The success is elicitation under a declared source frame, **not model learning**. Weights are unchanged. No evidence here shows that an autonomous agent can discover a correct excerpt, certify a rewrite's equivalence, preserve source uncertainty through a multi-step report, perform the earlier variance calculation, identify real memory carriers, or improve broad FRR reasoning. The earlier SR-C1 failed reader and valid SD toy mathematics remain as recorded. We have not installed an always-rewrite-to-there-are policy.

The optional [verification guidance](../../modules/verification-layer.md) and [design example](../../examples/soil-design-and-reset-calibration.md) add two refinements: test a plausible upstream explanation with semantics-controlled variants before repairing it; and keep frame-specific successes tied to their exact task/source mapping, preserving originals and uncertainties. A correct calculation cannot rescue a wrong input role, while a well-framed correct readout is not proof of downstream calculation. Existing source-role/threshold tools are unchanged and do not parse this domain or validate linguistic equivalence. No core/runtime/schema or queue status changed.

## Execution, costs and preserved history

All three contacts use the same pinned `HuggingFaceTB/SmolLM2-135M-Instruct`, revision `12fd25f77366fa6b3b4b768ec3050bf629380bac`, text-only, CPUfloat32/eager,2threads,eval/inference,argmax,64-new-tokencap. Python3.12.14,torch2.6.0+cpu,transformers4.57.1. Fresh prompt contexts are used; prior saved branches are not erased or passed to new calls. The main assistant is a separate system. These are authored language-reading probes, not a benchmark of internal cognition.

| Contact | New calls | Input tokens | Output tokens | Inference seconds excluding serialization/load |
|---|---:|---:|---:|---:|
| WC-C1 crossed question | 8 | 885 | 137 | 12.0266 |
| NF-C1 number-form factorial | 16 | 1,712 | 184 | 16.8535 |
| SF-C1 source-frame factorial | 8 | 857 | 90 | 8.5911 |
| Total | 32 | 3,454 | 411 | 37.4712 |

Cache serialization totals .1340seconds. Model loading and preservation/hash checks are outside the inference timings. These are local observations, not throughput or billing guarantees. No paid API/resource was invoked. Each study's runtime/stderr manifest is preserved; dtype deprecation warnings were nonfatal.

Thirty-two new terminal cache files totaling176,780,896bytes remain under `/workspace/smollm_wording_cross_states_v1`, `/workspace/smollm_number_role_states_v1`, and `/workspace/smollm_source_frame_states_v1`. Byte hashes, tensor sequence dimensions, exact rendered prompt/input IDs, decoded output IDs and cached-prefix hashes were checked. The final emitted token can be absent from the terminal cache; recorded lengths/token IDs retain reconstruction information. Binaries remain local; published manifests supply hashes/tokens/model pin. Workspace persistence is not guaranteed; no main-assistant cache access or chat-storage improvement is claimed.

The final pre-integration snapshot includes2,681priorFRRfiles and296recordedmodel/oldcachefiles. Each study separately checks its earlier snapshot and newly created caches. No historical program, raw response, source original, failed hypothesis, model weight or old cache was changed. Seven current navigation/guidance files are byte-archived in [ARCHIVE_RECEIPT.json](ARCHIVE_RECEIPT.json) before authorized updates. Moved links retain their original bases; use the original paths at the parent commit for historical navigation. [Final checks](FINAL_CHECKS.json) state the exact preservation and link scope.

Whole-response semantic review and source equivalence judgments are coordinator-only, not independent/masked peer review. Gold keys are frozen separately and hashed but not parsed into model prompts. Newly authored protocols follow the earlier outcomes by design. No population confidence interval, broad statistical significance or invariant-meaning theorem follows from repeated forms of two/four base records.

## Strongest next

Confirm the source-frame effect on fresh counts and additional sentence forms before any routing/rewrite default. A controlled next contact can separate adverb/noun alignment from tense or voice, and include missing-count statements so a fluent count answer is not mistaken for appropriate uncertainty. Keep the task-specific original-to-representation mapping and role checks explicit; only reconnect arithmetic once its source inputs are validated. Stop after these three contacts rather than search for a winning phrase. No background work remains active.
