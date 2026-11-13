# One-step error-feedback contact

**Outcome:** one complete cell in three replies under each condition; both dispatched cells reproduced the same semaphore error. No successful repair was observed. [All-six text/code/receipt reading](OBSERVATIONS.md).

13 November 2026, America/Chicago. Detached diagnostic branches; the continuing notebook garden is unchanged at entry 1562 and its original reference remains at 1550. No weights, live decoder, world laws or live memory changed.

## Question

After one sampled reply produced a complete Python cell that failed during multiprocessing semaphore creation, does showing its detailed actual error change the next reply or its real consequences compared with showing only failure status?

This test uses one selected parent reply from the earlier decoder study. That reply's code fence closed but its surrounding explanatory prose reached the 512-token cap. Both conditions retain the exact original initial chat, full sampled assistant reply, and a user-role receipt produced by the canonical `project_feedback` function. The full condition is that actual receipt unchanged. The status-only control changes only stderr to an empty string, retaining stdout, channel, exit code 1 and boundary fields. It is an explicitly counterfactual information-removal control; the true original error remains preserved in the source record. It adds no hint, solution, grading or request to fix anything.

## Planned comparison and all results

Seeds 27201–27203 are paired across both conditions. Sampling temperature .8/top-p .9 and output cap 512 match the preceding diagnostic. Every generation starts with fresh KV, exact retained role sequence, float32 eager CPU and the same local 135M model. Six followup replies were planned before inference. Each reply is delivered unchanged once through the existing notebook law into its own reconstruction of the same exact post-error physical checkpoint. Any complete cells run within the unchanged sandbox and their actual receipts are retained. No second model reply consumes those new receipts in this one-step protocol.

| Feedback | Seed | Output tokens | Stop | Complete cells | Code exit codes | Code-changed paths |
|---|---:|---:|---|---:|---|---|
| full_traceback | 27201 | 512 | token_limit | 0 | no code dispatched | none |
| full_traceback | 27202 | 456 | eos | 1 | [1] | none |
| full_traceback | 27203 | 512 | token_limit | 0 | no code dispatched | none |
| status_only | 27201 | 404 | eos | 1 | [1] | none |
| status_only | 27202 | 512 | token_limit | 0 | no code dispatched | none |
| status_only | 27203 | 230 | eos | 0 | no code dispatched | none |

`SUMMARY.json` reports frequencies by condition. Raw replies, token IDs and parsed fences, batch receipts, per-operation events, object stores and independent world verifications are retained. `PEER_REVIEW.md` and `AUTHENTICITY_REVIEW.json` independently check source text, receipt identity, sole stderr difference and parent checkpoint linkage. The parent diagnostic and active run inventories stayed identical, and parameter digests matched before/after. This uses cached local inference and no paid endpoint.

## What the comparison can and cannot establish

Different observed replies under these two inputs demonstrate sensitivity within this bounded setup. Removing the traceback changes both content and token length, so a difference cannot be uniquely assigned to semantic understanding of that error. Reusing three seeds creates paired random conditions, not six independent garden histories. The parent was selected for having a complete cell, not sampled at random from all possible model behavior.

Prose can refer to errors or propose an alternative without producing an executable action. A complete fence can dispatch and still fail. A zero exit code alone does not demonstrate meaningful repair or a correct explanation. These layers must be read separately from the actual raw text and receipts. Notebook writing is permitted behavior, and all outputs stay in the record. No model reply is rejected for lacking code or for missing an investigator-preferred solution.

This is in-context one-step responsiveness, not weight training, long-term memory acquisition or evidence of a developmental phase. Repeated failed approaches could need more opportunities, but additional cycles have not occurred here. The two-condition experiment is also a new diagnostic chat branch, not exact raw-token continuation of the capped parent and not a replacement for the live greedy trajectory.

## Next direction

Use the observed consequences and read the full text before choosing a follow-up. A multi-step branch would need its own fixed reply budget, exact actual receipts, per-branch persistent world, and no retrospective solution hints. An independent length/content control could better isolate information carried by the detailed traceback. Neither inference nor environmental conditions should be silently changed to force a favorable result.
