# Broad FRR orientation: observed emphasis differences, tied decisions

This exploratory pass actually supplied a broad FRR base to fresh participants. It compared common task instructions alone, generic review guidance, and the existing FRR compact runtime 0.2 verbatim. Three newly authored fictional tasks, one trajectory per arm×task, two turns per trajectory: nine new contexts and 18 participant completions. The full longer runtime and other possible broad FRR formulations were not tested. Core FRR files remain unchanged.

## Predicted dimensions and observed outcomes

All arms selected the decisive execution manifest in the configuration task and the clock calibration in the latency task. All three declined additional records for the already-settled release decision. After the records, all nine final answers satisfied the authored task key in the unblinded parent review. No material unsupported final claim or obstructive doubt was identified by that review. These are judgments about visible responses, not measurements of private reasoning or independent adjudication.

| Condition | Verification choices matching key | Final answers meeting key, parent-rated | Initial answer words, total | Final answer words, total |
|---|---|---|---|---|
| Baseline | 3/3 | 3/3 | 184 | 261 |
| Generic review | 3/3 | 3/3 | 176 | 226 |
| Broad FRR compact 0.2 | 3/3 | 3/3 | 239 | 264 |

The no-request decision counts as the appropriate choice in the settled task. All 18 responses met the requested 350-word limit. Word totals describe output size, not token usage, compute or usefulness. Generic guidance contained 296 whitespace words and FRR 314; similar word count is not equal token cost. Actual model sampling settings, exact token/dollar costs and elapsed-time receipts remain unknown.

The conclusions were consequentially distinct: actual CFG-B execution selected [125] but did not establish intended policy; calibrated before/after latencies both averaged 200 ms for the three matched requests, without establishing workload-wide equality or a causal release effect; complete release prerequisites justified GO without extra verification. Baseline and generic participants made these distinctions as well as FRR participants.

## Post-run noticings, separated from predicted outcomes

The FRR latency response included an early qualification: “Even a confirmed increase would describe these three requests; broader performance and release causation would require further evidence.” Baseline and generic initial answers did not explicitly include that population/causation qualification, but their final answers also limited broader inference. This is a one-output timing/emphasis difference, not a demonstrated reliable FRR benefit. The FRR initial latency answer was 127 words versus baseline 87 and generic 79; more words may accompany useful qualifications or unnecessary elaboration, and length alone cannot decide which.

The generic configuration draft said the “approved settings” label suggested CFG-B should have run. FRR and baseline drafts more explicitly withheld policy authority. This generic wording was a soft suggestion rather than a false assertion of governing policy, and its final answer correctly left intended policy unresolved. Preserve the nuance rather than inflate it into an error or comparative win.

FRR did not become reflexively skeptical in the complete-evidence task: it said to proceed and requested no additional record. Both controls did the same. A broad orientation can coexist with a direct decision in this example; this does not show it always avoids overcomplication. No unexpected new mechanism was discovered. Exact excerpts and parent interpretations are retained in [PARENT_REVIEW.json](PARENT_REVIEW.json).

## Provenance, reproducibility and scope

[Protocol](PROTOCOL.md), exact treatment texts, all case/menu/record/key definitions, participant prompt order, deterministic record assembly and launch hashes were published before participant outputs at [38f8c955](https://github.com/bruhman680/CERTX/commit/38f8c9557670aa0c1c24b84ec37de5d284108de6). All four launch hashes remain unchanged, including the existing compact FRR source. Common prompts used a light JSON wrapper around natural responses and allowed additional consequential observations, without requiring FRR terminology or a lens checklist. First turns chose one record or none; final turns received only that frozen record, with no scoring feedback. No retries, answer repairs or outcome-driven additional cases.

The three preceding design agents reviewed base selection, case candidates and comparison limits. Two suggested cases were adapted by the parent; the third was parent-authored. They share model/design ancestry and had treatment awareness. These are exposed development fixtures, not independent or reserved confirmation tasks. Strong source/units cues and explicit sufficient-evidence wording can create ceilings. Common competent task instructions may already elicit the behaviors at issue. One trajectory per arm×task cannot establish a population treatment effect, general FRR efficacy or a mechanism for the wording differences.

Each participant began with fork_turns=none and continued only its own context for turn two. No prior FRR handoff or old challenge outcomes were supplied. No participant tool calls were visible; filesystem/tools were restricted by instruction, not physically isolated. Records are fictional authored inputs returned by the parent, not real external source retrieval. All contexts share the underlying model provenance. Public repository exposure further limits blinding.

Raw first/final payloads are B01_first.txt through B09_final.txt. Exact first prompts are in SETTINGS.json; final prompts and [retrieval receipts](RETRIEVAL_RECEIPTS.json) preserve delivered records. Payloads were transcribed from final messages by the parent, not exported with provider transport metadata. [RESULTS.json](RESULTS.json) includes per-trial hashes, lengths and explicit ratings. [Integrity checker](../../tools/check_broad_frr_pilot.py) checks launch/prompt/record/excerpt consistency and summarizes the parent judgments; it does not automatically validate natural-language correctness. That checker and review assignments were written after outputs under the prospectively fixed dimensions. No independent or arm-blind judge was used.

[Integrity controls](VALIDATION.json) accepted an unchanged temporary record copy and rejected four separate mutations: changed launch source, changed delivered-record receipt, missing review excerpt and unavailable request ID. Five checks passed. These checks protect record consistency; they do not validate the parent semantic judgments.

This was a broad-guidance comparison rather than the earlier four-arm HPGM test. The previous ties and corrections remain intact. We now have direct observations of this FRR base in participants, including small emphasis differences and tied practical choices; we do not yet have demonstrated superiority. A useful follow-up would distinguish spontaneous evidence search from choosing obviously labeled menu items, using separately prepared cases and repeated assignments. Preserve beneficial, neutral and harmful movement without redefining every extra qualification as success.
