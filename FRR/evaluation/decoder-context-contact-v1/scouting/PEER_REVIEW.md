# Independent implementation review

13 November 2026, America/Chicago. Read `probe.py`, its written `PLAN.json`, `summarize.py`, and available execution-log rows while the batch was running. No changes were made to the running source and no inference was performed for this review. Final results and all assertions must still be checked after completion.

## Finding

No material protocol implementation error was identified in the inspected decoder comparison. The source implements the declared limited comparison; it does not establish a new live-garden decoder, sustained competence, or a causal account of prior inactivity.

## Exact contexts and preservation

Each context is loaded from the prior detached cap study, and the script asserts that its retained token IDs equal `apply_chat_template` on its recorded messages with `add_generation_prompt=True`. Both decoder arms therefore use the same retained prefix within each context. Input-plus-output capacity is asserted. The two contexts differ in history and length, so a between-context effect cannot be attributed to length alone. `summarize.py` states that qualification.

The model is evaluation-only and gradients are disabled. Parameter digests are checked before and after; live run-file inventories are compared after the batch. Fresh sampling uses raw retained input IDs without a new coaching message. The only output writes are inside this detached study. Final preservation claims remain conditional on the actual end assertions succeeding.

## Nucleus selection

The logits are divided by the declared temperature 0.8, sorted descending, and converted to probabilities. A token is removed when its preceding cumulative mass exceeds 0.9. This retains the threshold-crossing token, keeps the highest-probability token, renormalizes the retained mass, and samples via the explicitly supplied CPU generator. This is the intended shifted-cutoff nucleus scheme. At exact equality of preceding cumulative mass with the threshold it also retains the next token; that conventional boundary convention is unlikely to affect the observed protocol but is more precise than claiming a unique mathematically minimal set for every floating-point tie.

There is no hidden top-k limit, EOS ban, minimum-length processor, repetition penalty, forced fence closure, or output-text repair in the sampled branch. These absences matter because this is a decoder comparison rather than a formatting intervention. EOS is counted in output tokens and terminates normally; decoded text excludes special tokens as it does in the retained references.

## Seeds and reference reuse

Each seed initializes a separate CPU generator for its sampling run. The four seed values are fixed in the plan before sampling. Reusing that set across two contexts does not create eight independent environmental replications; the proposed report calls them paired conditions. Different seeds do not guarantee different visible replies: a sharply concentrated or singleton nucleus can make several runs identical. No independence or diversity conclusion should be inferred merely from distinct seed integers.

The greedy rows reuse the previous cap study rather than consuming new inference. For the initial context the reference is the 512-token prefix of a longer greedy generation; for the later context it is the natural EOS-terminated output if shorter. These are valid fixed baselines at the same upper cap, but are not fresh repetitions, uncertainty estimates, or independent evidence. Both the plan and proposed report make that distinction.

## Meaning of measurements

The unchanged notebook parser decides exact complete-fence eligibility. Python `ast.parse` checks syntax of complete Python cells without executing them. Shell cells are counted by the parser but have no separate shell syntax check. Even a Python AST is insufficient to establish successful compilation in every context, available imports, safe runtime behavior, correct answers, or useful environmental effects. The proposed report explicitly separates static syntax and parser eligibility from execution and emergence.

Observed 256-token milestones and final 512/EOS assessments are prefixes from the same reply, not repeated trials. The source retains every final outcome and does not automatically select a successful sample for the live garden. An eventual closed-cell count difference can support sensitivity to this sampling condition on these inputs, but not a universal performance ordering.

## Operational limit outside the scientific comparison

The script refuses an already completed `RESULTS.json`, but it is not a crash-safe resumable experiment runner: if interrupted before completion, rerunning the same script could overwrite raw paths or the plan. No such rerun was observed in this review. Preserve partial files and choose a new study directory if interruption occurs; do not claim the detached script itself provides the canonical garden's transaction/recovery guarantees.

## Recommended final checks

Verify eight retained sampled rows, all four seeds in both contexts, end-of-batch inventory and parameter assertions, and zero generated-code executions. Publish the fixed plan, all outputs, and the referenced greedy-source hashes. Keep the naturally ended unfinished outputs in the reported denominator. Treat any later consequence execution as a separately declared test on copies.
