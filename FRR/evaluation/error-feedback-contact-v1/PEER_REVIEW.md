# Independent feedback-protocol review

13 November 2026, America/Chicago. Reviewed `probe.py`, `PLAN.json`, `INPUT_MESSAGES.json`, the retained sampled parent reply, actual parent consequence batch and referenced world bundle. This review made no edits to the running source, performed no inference and did not execute any garden cell. End-of-batch assertions and outcomes remain to be read after the batch completes.

## Finding

No material implementation or input-authenticity error was identified. The protocol can test whether this one-step response differs when actual stderr is present versus removed. It cannot isolate a pure semantic-error-information effect from input-length/format effects or establish general correction/learning competence.

## Independently verified authenticity

`AUTHENTICITY_REVIEW.json` records seven checks, all passed:

- The saved parent sample text exactly equals the raw text delivered in its actual consequence batch.
- The detailed-error input is byte-for-byte the unchanged `candidate.project_feedback` output for that batch.
- Both conditions have identical earlier messages and the exact same sampled assistant reply.
- Their feedback JSON differs only in receipt stderr, which is empty in the reduced condition. Stdout, channel, exit code and boundaries remain equal.
- The selected world bundle SHA-256 matches the written plan, and its bundle ID matches the final parent operation's `after_id`.

The parent code had an actual complete Python cell and an actual `OSError` receipt. It was not an observer rejection or fabricated critique. The full stderr contributes 1,536 UTF-8 bytes. The parent cell did not alter captured files; its preceding notebook append did persist. Both are already included in the shared parent bundle, so this is a continuation from the actual post-attempt state.

## Controls, seeds and interpretation

The reduced condition is a counterfactual information ablation. It retains a visible nonzero exit code, so it is not “no failure feedback.” It also shortens the input, removes Python/library path strings and stack structure, and moves later token positions. The plan acknowledges unmatched lengths and the history/content confound. Any contrast is for this whole stderr-present versus stderr-empty bundle, not a uniquely isolated causal effect of understanding the exception.

Three fixed seeds initialize separate CPU generators, and the same seed set is paired across conditions. Distinct seeds do not guarantee distinct text, and seed pairs do not represent six independently sampled environments. All followups share one selected parent from the preceding experiment; the parent was selected because it contained the sole complete cell, not because its later failure favored a result.

Temperature 0.8, top-p 0.9, 512-token cap, greedy-reference-independent sampling implementation, EOS handling and prefix cache accounting match the declared sampled body. Each input receives a fresh prefill; raw input IDs are saved with each actual reply. No source-level code repair, forced fence closure or diagnostic score is inserted into the model's input.

Only one model response follows each receipt. Changed text or an attempt to revise code is not proof of persistent learning; a failed next attempt does not prove inability to use feedback over longer interaction. More/fewer executable cells are an output-form observation, not sufficient evidence for improved reasoning. Proposed explanations should be tied to visible code and actual receipts rather than inferred internal thoughts.

## Independent world copies and real consequences

Inspection of `GardenWorld.create` confirms each followup initializes a new store, copies the same parent objects and bundle, and reconstructs its own runtime. It does not hardlink mutable model files into the parent store. Each complete generated reply is delivered once through the unchanged notebook receiver, so notebook appends, ordinary execution errors and supported code effects can all be retained. The receiver is not selectively handed only an attractive code substring.

The script retains raw replies before dispatch. Each world's final store is verified after close. End assertions require the canonical run, the prior diagnostic directory, and model weights to remain unchanged. This is a detached branch from a sampled initial context, not entries added to the canonical greedy garden at 1562. The parent reply was capped in its prose explanation, a condition explicitly recorded in the plan and preserved in both inputs.

## Final review checklist

After completion, verify exactly six model replies (three seeds × two conditions), all raw IDs/text and actual receipts, all store checks, canonical/parent inventory equality, and unchanged weights. Count ordinary writing even when it lacks executable cells. Compare the received error with what the followup visibly changes; do not infer an error-handling mechanism solely from apologetic prose. If a code revision succeeds, describe the specific operation and its captured effect rather than claiming general self-correction or emergence.

## Qualitative read of all six outputs

The initial qualitative pass covered five available outputs. After completion, status-only seed 27203 and its actual batch were also read, bringing coverage to all six raw replies and their receipts. Final `RESULTS.json` records six model replies, zero extra feedback cycles, and passed canonical-run, parent-diagnostic and weight-preservation assertions. No additional inference or world operation was needed for this review.

| Condition / seed | Visible output | Actual consequence |
|---|---|---|
| Full traceback / 27201 | Proposes a database-oriented rewrite, still using pools; introduces helper names including `get_context`, `_setup_queues`, `_inqueue`, and an explicit `multiprocessing.Semaphore`. Several names overlap the received traceback and were absent as definitions from the original program. | Hits the 512-token cap with an unfinished fence; notebook append only. The proposed code is not executed. |
| Full traceback / 27202 | Says a timeout should be added, then emits a complete cell with `multiprocessing.Pool()` and no visible timeout implementation. | Notebook append and one Python dispatch. Exit 1 with the same read-only-filesystem exception in semaphore setup. No code-created path change. |
| Full traceback / 27203 | Announces successful writing and explains purported cell/database components; repeatedly recommends pools. | Hits cap with an unfinished fence; notebook append only. No successful program execution supports the prose success statement. |
| Status only / 27201 | Emits a complete program retaining `multiprocessing.Pool(processes=4)`. Its explanation claims that a `boundary` attribute was added to `output_file`, although that operation is absent from the code. | Notebook append and one Python dispatch. Exit 1 with the same semaphore-related read-only-filesystem exception; no code-created path change. |
| Status only / 27202 | Describes `boundary` and `channel` as attributes of cells/process variables even though no such assignments appear in the inherited program. Those words occur in the receipt schema. | Prose only; notebook append, no complete executable cell. |
| Status only / 27203 | Explains the receipt dictionary as if it were the program, assigns inaccurate meanings such as boolean `exit_code`, and then makes unsupported claims about program variables being `None`. | Natural EOS, prose only; notebook append, no executable cell or code-created file change. |

The inspected text shows dependence on material in the feedback: traceback helper names appear in proposed code, and receipt-schema words appear as supposed program attributes. That lexical overlap is observable; it is not sufficient to establish why the model produced it internally or that it interpreted the underlying environmental limitation. A competing description is that feedback text becomes additional material for program-like continuation rather than a successfully used error explanation. Distinguishing those accounts needs further controlled evidence.

The two inspected executed revisions both retain the very pool operation whose semaphore creation failed. Their new receipts demonstrate failure to remove that first observed obstacle in these specific attempts. Other edits and unexecuted later code must not be credited as resolved errors, or blamed for the first exception before they run. Conversely, one failed step should not be generalized into inability to adapt over longer interaction.
