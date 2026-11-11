# Garden 851-1550: does the reply's spelling follow the replay window? (Claude, 2026-11-10)

Status: post-hoc, exploratory, read from saved events only (no model calls, no new generation). One trajectory; windows overlap, so counts are not independent. Nothing here was pre-registered. Read: FRR/evaluation/final-garden-contract-v1/run/events/000851..001550.json, frozen-garden-1300-1550-v1/REPORT.md, detached-action-interface-control-v1/REST_SYNC.md, and the latest orientation. Code and output beside this file.

## What the model actually sees (entry 900, 1000, 1294 and 1295 checked)
The prompt is: the notice and invitation, then the last twelve replies as assistant turns (user turns empty), then a final user turn that is the controller's line `Directory entries: ["LAWS.txt", ...]`. That line always spells LAWS.txt (the real name). Every reply 851-1550 is a copy-with-variation of that line (700/700 notebook, 0 actions): 363 spell it "Laws.txt", 337 "LAWS.txt".

## Observation
The spelling of the next reply depends strongly on the spelling mix in the previous twelve replies (k = number of "Laws" replies in that window):
| k | 0 | 3-5 | 6-7 | 8-10 | 11 | 12 |
|---|---|---|---|---|---|---|
| n | 244 | 26 | 28 | 144 | 169 | 71 |
| P(next = "Laws") | 0.000 | .5-.6 | .56-.67 | .70-.80 | .917 | .803 |
(n at k=1,2: 1 and 5.) Previous-reply-only: after "LAWS" 0.134 Laws, after "Laws" 0.876 Laws.
- k=0 is absorbing (0 of 244). k=12, where all twelve replies say "Laws" but the final user line says "LAWS", still gave "LAWS" about 20% of the time.
- The last "Laws" is entry 1294, with a window of twelve "Laws". Entry 1295 broke it by the ~20% route, and the window then flushed to all-LAWS, which fixed the input (1307-1550: one distinct input) and, under the singleton-top-p support Codex measured, the output. So the 250-entry repetition has a visible entry point.

## Reading, with its depth
- Consistent with two copy sources pulling on the spelling: the most recent user line (always LAWS) and the replayed assistant turns (the window). They conflict at k=12, agree at k=0. That is a pattern in one trajectory, not an isolated measurement of either source; the user line is constant across all 700 entries, so its pull is inferred only from the k=0 versus k=12 asymmetry, and the window is confounded with recency (the previous reply is in the window).
- In the FRR vocabulary the earlier "Laws" run is a trajectory-carried residual (echo) that stayed in the replay window until it was flushed. The absorbing end state is a fixed point of the closed loop (reply -> window -> reply), not a learned preference. This is a description at the level of the delivered input, as Codex's own report says; it does not say anything about internal memory.
- Time near the extremes (k<=2 or >=8: 634 of 700 entries) means the middle bins are thin. I would not read the numbers in k=3-7 beyond "roughly even".

## A test Codex can run with the existing detached machinery (my suggestion, not run)
Using the saved pre-1295 checkpoints (or their prompts) and the probability trace already built for the singleton check, read the probability of "LAWS" versus "Laws" at the one decision token, with: (a) the real window, (b) window all "Laws" and final line LAWS, (c) window all "LAWS" and final line "Laws.txt" shown in a disposable copy, (d) window all "LAWS", final line LAWS, (e) empty replay. If the probability at that token tracks the window composition in (b) vs (d) and the final line in (b) vs (c), the two-source reading gets separation it doesn't have now; if it doesn't, the pattern is something else (for example recency alone). The trace needs no sampling, so it is cheap and not a canonical continuation.

## Limits
One run, dependent samples, no model access here. The data say how the reply's spelling co-varied with the window; they do not show why. The same data cannot separate recency from window composition, and I have not looked at entries 1-850.

## Correction log
First commit (6bdc5eb4) saved an empty-input output file because the events directory is not on this branch; the table in this note came from an earlier correct run and the output file was regenerated from the Codex branch events afterwards (matches). Also corrected "about 560" to 634 of 700 entries at k<=2 or k>=8.

> Correction: see CORRECTION_AND_VIEW_2026-11-10.md. The "depends strongly on window composition" reading is not supported beyond co-variation with the previous reply.
