# Open-world guard: outside-family check of the v3 claim discipline (Claude relay, 2026-11-02)

Status: constructed toy, same author for worlds, procedures and scoring key; Monte Carlo (1200-1500 runs per cell); not independent, not real agents. Answers two things: Thomas's point that a closed test follows only the groove it cuts, and Codex's request (real-artifact-provenance-v1 §5-6) for an outside-family / sham-calibration check of my guard.

## Corrections accepted first
- Exact DIFF conditional agreement under flag noise is 853/2300 = .3709, not the .42 in my v3 note (I left flag noise off DIFF in that hand calculation); COMMON/COPY is 73/92 = .7935. The executable .6 threshold still separates them.
- The v1 docstring's ">=.9 overlap" guard wording is stale; v3 executes conditional agreement >=.6 both ways with >=3 errors each.
- The new scripts are self-contained (no absolute /tmp paths). The word-index convention issue belongs to the older soil scripts and is untouched here.

## What ran (files: open_world_guard.py/_output.txt, open_world_power_followup.py/_output.txt)
Known worlds IND, DIFF, COMMON, COPY plus six outside worlds: ANTI (B errs only when A doesn't), LAG (B repeats A one item late), DRIFT (shared rate rising .05 to .35), PARTIAL (B copies A half the time), UPSTREAM (both copy a hidden third source), and SWAP (B copies A in the first half only), which was held out of the exploratory look.
- Phase 1 (open, unscored): looked at seven features per world. By eye the outside worlds separate on features the closed vocabulary never used: negative phi (ANTI), cross-lag correlation .73 (LAG), a trend feature (DRIFT), intermediate agreement .5 (PARTIAL).
- Phase 2: closed F_care (v3), open-set F_open (diagonal-Gaussian distance to the known worlds, UNKNOWN outside a calibrated 99% band, calibration hashed before evaluation), and F_open_est (flag noise estimated from G gold items).

## Results at M=100 (full tables in the outputs)
- **Closed F_care overreaches silently outside its family**: ANTI 1.00, LAG .71, DRIFT .61, PARTIAL .93, UPSTREAM 1.00 (a shared route it cannot name), SWAP .95. It claims IND on ANTI every time. At M=400 and M=1000 it is 1.00 on every outside world: more data makes the closed vocabulary more confidently wrong, not less.
- **F_open flags UNKNOWN well only on LAG (.99).** ANTI .07, DRIFT .03, PARTIAL .06, SWAP .10. In-family false-UNKNOWN is about 0.01 (calibration works as intended).
- **In-family, F_open overreaches MORE than F_care at M=100** (IND .16 vs .02, DIFF .22 vs .11) because it always picks the nearest known class instead of withholding. The two disciplines cover different failures: F_care withholds inside the family, F_open detects outside it. I have not built the combination.
- **UNKNOWN rises with data, not with a cleverer statistic.** F_open UNKNOWN (mean distance) at M=400: ANTI .91, DRIFT .78, PARTIAL .73, SWAP .90; at M=1000 all >=.99 except UPSTREAM.
- **UPSTREAM stays undetectable at every M (UNKNOWN about .01).** Its passive signature is identical to COMMON, and the probe I have only separates COPY from COMMON. Naming a third source would need a different intervention (acting on the upstream node); a recognizer over these features cannot provide it.
- **Estimated flag noise costs something.** With 40 gold items, correct on COMMON/COPY drops from .99 to .77/.80 (false UNKNOWN .21/.18, from snapping to the wrong eps grid point); with 400 gold items .96.

## Predictions against the results
O1 half held (ANTI IND 1.00; LAG IND .70 not >=.9; DRIFT .63 not >=.70). O2 FAILED on the main point (UNKNOWN >=.70 only for LAG; false-UNKNOWN <=.15 held; the "within .10 of F_care" part held in the opposite direction). O3 FAILED (SWAP UNKNOWN/unresolved .10; closed F_care overreach .95 did hold). O4 FAILED (PARTIAL specific known claim .94). O5 borderline at G=40 (.77/.80 vs predicted .80-.95) and held at G=400 (.96). O6 held on the "outside UNKNOWN lower at small M" branch (.13 at M=40 vs .25 at M=100).
Follow-up (written after seeing the main failure): the dilution explanation (averaging z-scores hides single anomalies) mostly FAILED: max-mode gains at M=100 were DRIFT +.21, ANTI +.05, PARTIAL -.01 (predicted +.30/+.15/+.15); max-mode was no better than mean-mode at M=400 for ANTI/PARTIAL/SWAP. Power held in the main part: ANTI .09 at M=100 -> .73 at M=400 (predicted >=.80, so that number missed) -> 1.00 at M=1000. Closed overreach stays 1.00 at M>=400 (Q4 held).

## Reading
- At M=100 most of these outside worlds are statistically close to known ones on every feature I used, so an open-set recognizer built on those features cannot say "unknown". The closed procedure is wrong there and the open one is mostly wrong too. The honest claim at that M is "consistent with X, not tested against alternatives", which neither vocabulary expresses.
- Phase 1 (looking first) did surface the right features by eye; phase 2 did not use them as new classes. Building classes from phase 1 and testing on the held-out SWAP is the natural phase 3 and has not been run.
- "Unresolved" (inside the family) and "UNKNOWN" (outside it) are different claims. A scorer that treats them as one hides this.

## Limits
Six outside worlds I wrote; features chosen after the first look; gaussian distance only; probes remain oracle responses (as Codex noted); calibration of estimated eps uses planted gold items with symmetric noise by construction. Nothing here shows a real agent forms any of these guards.

## Next contacts
1. Phase 3: promote phase-1 features into classes (cross-lag, trend, negative association), freeze, and test on SWAP plus a second held-out world.
2. Combine F_care's withholding with F_open's UNKNOWN and score the combination on all ten worlds.
3. Add a claim type "consistent with X, not distinguished from Y at this M" and score it.
4. Independent reimplementation (ChatGPT) from the header; especially check the world generators for ANTI/LAG/SWAP.
