# Letting imperfect answers continue downstream

31 October 2026 UTC. Completed local inference and source-receipt contacts. No training or default-model promotion.

We gave earlier failures space to continue instead of making upstream correctness a prerequisite for every experiment. That space exposed both recovery and damage. A source-free second pass collapsed to a constant answer. Reopening the full two-record source changed little. Supplying the correct target record repaired every earlier semantic error in this toy, even when the wrong proposal remained visible.

This supports a scoped working pattern: carry provisional answers through a bounded investigation, preserve their trace, and distinguish the checks used for further exploration from the checks used to accept a result. It does not show that unguided extra review is beneficial or that a model independently learned to detect its mistakes.

## A. Actual earlier answers, including all errors

The prior canonical reader produced 23 correct and 13 wrong labels on 36 two-record sources. All were retained. This is exposed regression replay, not a new primary set. Each case then passed through all six frozen conditions; 216 new generated answers. A mechanical pass-through would retain 23/36 without another model call.

| Later path | Final correct /36 | Wrong→correct /13 | Correct→wrong or invalid /23 | Source-supported acceptance /36 |
|---|---:|---:|---:|---:|
| Full source, no proposal | 23 | — | — | 23 |
| Selected target, no proposal | 36 | — | — | 36 |
| Deliberately wrong target record | 12 | — | — | 0 |
| Earlier proposal, no source | 12 | 4 | 15 | 0 |
| Earlier proposal + full source | 22 | 1 | 2 | 22 |
| Earlier proposal + selected target | 36 | 13 | 0 | 36 |

**The four source-free “repairs” were not evidence of error recognition.** That reader returned `NO` on all 36 calls. It happened to fix four earlier errors while damaging fifteen correct answers. All source-free outputs receive an UNSUPPORTED evidence receipt, including the twelve labels that match the task reference.

With the full source and earlier proposal, one error was repaired and two correct answers were damaged: 23→22 correct. The selected-target path retained all 23 correct answers and repaired all 13 wrong ones. The harness selected the record; the model did not decide to retrieve it. The parser can solve this literal-status task without an LLM, so this is a diagnostic of the surrounding workflow and reader, not a claim that the LLM is necessary.

## B. Fresh paired correct and wrong proposals

Twelve new study sources cross Spruce/Fir, three explicit target states and both target positions. The distractor is a fixed cyclic alternative, always conflicting; this is not every possible distractor assignment. Each source receives a correct, wrong1, and wrong2 proposal, balanced across the same label vocabulary. All inputs and metrics were frozen before their forwards. These 144 calls include three no-proposal source conditions plus nine proposal/evidence combinations per source.

| Evidence available to later reader | Correct proposal /12 | Wrong proposal 1 /12 | Wrong proposal 2 /12 |
|---|---:|---:|---:|
| No source | 4 | 4 | 4 |
| Full two-record source | 4 | 5 | 4 |
| Selected target record | 12 | 12 | 12 |

Without any proposal, full-source reading scores 6/12 and selected-target reading scores 12/12. Deliberately supplying the other record scores 0/12. With a selected target, all twelve cases work under every proposal assignment, including both wrong alternatives. **The mistaken proposal can remain visible while the answer changes appropriately.** No stored history or model weights were erased to accomplish this.

The full-source branch also struggles with correct proposals. Proposal presence adds wording and tokens; these results do not uniquely diagnose psychological anchoring, attention, internal confidence or a neural mechanism. The paired seed-content contrast is controlled within these fixtures, but the broader full-versus-selected contrast changes length, record structure and selection together. A matched-length context test remains a strong next direction.

## C. Evidence identity after movement, then one real repair

Every deliberate wrong selection was allowed through a model readout first. The later source receipt checks selected-record identity against the original target, separately from answer correctness. It finds TARGET_MISMATCH on all 48 wrong handoffs. Twelve replay answers nonetheless match because both records share the same status. A correct-looking label therefore does not establish a correct handoff. Source absence, wrong identity, altered content, invalid output and label inconsistency have separate fields.

In an outcome-informed follow-up, a frozen one-step controller reacts to those identity receipts: reopen the original source, select its target record, then read it with the actual mistaken prior answer still present. [Loop protocol](identity-repair-loop/PROTOCOL.md), [raw](identity-repair-loop/run/RAW.jsonl), [summary](identity-repair-loop/run/SUMMARY.json). It executes all 48 cases, including the twelve initially matching labels. Result: 48/48 source-consistent and eligible final answers, 36 wrong→correct, 12 correct retained. Original wrong handoffs and their receipts remain linked and unchanged.

This is an operational replay, not independent corroboration: all 48/48 loop input prompts already occurred in the main contact, and the loop has 24 unique prompts. It demonstrates the controller actually executing and appending a repair branch, not a new capability test or an independent sample of success. The target trigger and selector are explicit code over a declared grammar. This is neither model-initiated retrieval nor autonomous error awareness.

## What counts as repair, and what counts as support

For a seeded cohort, let R be wrong→correct and H be correct→wrong/invalid. The exact accounting is:

`correct_after = correct_before + R - H`

Keep wrong→other-wrong, wrong retained and wrong→invalid visible too. An invalid string is not automatically calibrated abstention; changing a label is not automatically a repair. `WITHHOLD` here remains the learned semantic answer to an explicitly supplied `Status: missing`. Epistemic source absence is a separate UNSUPPORTED receipt.

The receipt is conditional on the exact authored source and a tiny parser. It does not authenticate the author, establish external-world truth, detect fabricated but internally consistent source data, or validate unrestricted documents. Its acceptance field is computed after the experimental movement; it never rewrites the answer. Fixture grammar validation and resource guards still apply. “No gating” in the execution manifest refers to not screening scheduled proposals by correctness or the later acceptance receipt, not to disabling input validity or resource checks.

## Method, cost and preservation

Pinned SmolLM2-135M-Instruct with the saved final canonical q/v LoRA adapter from [simple acquisition](../simple-readout-acquisition-v1/REPORT.md). Same weights in fresh reader contexts; no training, independent agent comparison or FRR-versus-no-FRR intervention. One bounded review pass per branch, then a separate one-step identity controller. No accuracy-based retry or checkpoint choice. Greedy eight-token/EOS readout; complete-label+EOS summed log probability and mean diagnostic retained separately. All outputs were valid labels here. Summed-choice scoring matches every free label in the main contact. Mean scoring differs on two calls and is retained separately. Neither score is calibrated confidence.

[Protocol](PROTOCOL.md), [freeze](FREEZE.json), [data](DATA.json), [call schedule](CALLS.json), [raw](run/RAW.jsonl), [per-state/transition summary](run/SUMMARY.json), [checks](CHECKS.json), [final audit](FINAL_CHECKS.json). Six focused source/identity/transition tests pass. All 72 no-proposal replay baselines match the earlier input and output token IDs exactly. All 3485 previous local files match before navigation sync; earlier navigation/module originals are byte-archived here.

Main: 360 free generations plus 360 three-choice scoring batch forwards (1080 candidate sequences), 33360 generation input tokens and 1082 generated tokens including EOS. Readout plus choice scoring: 383.910 seconds, excluding model loading, other work and instrumentation. Largest input: 127 tokens; sampled working maximum 1975373824 bytes, process RSS 948150272 bytes. These are phase samples, not continuous peaks or billing evidence.

Loop: 48 additional generations and 48 choice batches (144 candidate sequences), 4254 generation input tokens, 160 generated tokens and 51.072 readout/scoring seconds. Across all 408 calls there are 171 unique prompts. Repeated prompts and reused sources are disclosed rather than counted as independent evidence.

Exact source/prompt/token/decoded-answer/choice-score/transition and dependency checks pass. Original base, final adapter and earlier artifacts remain unchanged. No new binary model state; full terminal KV tensors are not retained for these diagnostic readouts. The existing local 12.8 MB simple-readout snapshot contains this adapter and excludes dense base/runtime. The older capsule the user saved to desktop contains different adapters. No fresh-environment/optimizer-resume rehearsal, model download, installation, separately paid API or rental. Account usage/billing is not visible.

## Practice and next directions

An [optional example](../../examples/provisional-downstream-repair.md) records this distinction between carrying a provisional result and accepting it. The verification module receives a short link/clarification; core prompts/schema, general tool implementations, queue statuses and default model remain unchanged. Earlier failed reading gates remain historical failures for their original claims. They do not prohibit a separately scoped study of failure propagation or repair.

Next strong paired tests can preserve this basic readout while varying matched-length neutral, agreeing and conflicting neighbors. A separate direction is letting a reader request evidence instead of receiving a harness-chosen reopening path. Longer compressed writer handoffs, stale/wrong-source versions and retrieval cost remain broader open work. Do not assume an autonomous retrieval policy or genuine unknown-state action has already been learned. The parked Grok substrate-depth relay remains unvetted and unadopted.

Within this garden plot, additional downstream space became useful through visible evidence and repair opportunities. More source-free movement amplified error. Both outcomes stay in the history.
