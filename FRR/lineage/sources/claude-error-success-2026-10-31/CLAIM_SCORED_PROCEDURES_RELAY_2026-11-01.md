# Claim-scored comparison: success-accumulation vs failure-first, with and without claim discipline (Claude relay, 2026-11-01)

Status: constructed toy, exact world laws, Monte Carlo (3000 runs per cell, seed 20261101), same author as the procedures AND the scoring key. Not independent, not a real-agent result. Motivated by Thomas's clarification that the practice is as much about CLAIMS and ASSUMPTIONS made from failures as about the failures.

## Setup (see script header)
Two answerers A,B over M items, error rate .2, flag noise 5%. Worlds: IND, DIFF (shared item difficulty, independent given item), COMMON (hidden source defect hits both), COPY (B copies A). COMMON and COPY give identical passive error flags; only an intervention (correct A's source, re-ask B) separates them. Procedures: S (success accumulation: agreement taken as independent confirmation), F_naive (failure-first, passive, picks the favoured story), F_care (claim discipline: hold ranges open, resolve only with probes), F_probe (always probes, attributes a route). Scoring: correct / honest-unresolved / overreach.

## Three runs, all preserved (the first two broke for implementation reasons, and I want that visible)
- **v1** (`..._v1_INITIAL*`): the guard for "identical signature" used Jaccard >= .9. Flag noise defeats it at M>=40, so F_care's guard never fired on the shared worlds: overreach 87-100% there, and P2-P5 mostly failed. That is a result about a brittle guard, not about the idea.
- **v2** (`..._v2_threshold75*`): switched to conditional agreement P(B|A)>=.75. The expected value in COMMON/COPY under noise is about .79, so the guard fired only ~57% of the time. I should have computed this before running.
- **v3** (current): threshold .6, the midpoint between COMMON's expected .79 and DIFF's .42, derived analytically before running. It assumes known flag-noise rate. Only the guard changed between v1, v2 and v3.

## v3 results at M=100 (M=20 and 40 in the output file)
| procedure | IND | DIFF | COMMON | COPY | overall overreach | probes/run |
|---|---|---|---|---|---|---|
| S | c1.00 | o1.00 | o1.00 | o1.00 | .750 | 0 |
| F_naive | c.88 | c.71 | c.96 | o1.00 | .362 | 0 |
| F_care b=0 | c.69 h.27 | c.44 h.45 | h.96 | h.97 | .052 | 0 |
| F_care b=3 | c.69 h.27 | c.44 h.45 | c.96 | c.96 | .056 | 1.45 |
| F_probe | o1.00 | o1.00 | c1.00 | c.99 | .503 | 3.00 |
(c = correct, h = honest unresolved, o = overreach.)

## Predictions against v3
P1 held (S overreach .75 at every M, but that number is fixed by my 4-world prior, 3 of 4 worlds not being IND; it is not a measured weakness of success accumulation). P2: IND .88 and COMMON .96 held; DIFF .71 FAILED (predicted >=.85); COPY overreach 1.0 held; overall overreach .36 not ~.25. P3: unresolved >= .9 and overreach <= .05 on COMMON/COPY held; correct on IND/DIFF >= .85 FAILED (.69, .44) because F_care withholds on IND/DIFF (.27, .45 honest-unresolved), not because it is wrong there. With b=3, correct COMMON/COPY .96 held. P4 held (naive misclassifies 31%/46% at M=20; care's overall overreach .196 vs .518). P5 held (F_probe overreach 1.0 on IND/DIFF, overall .503). P6: the tradeoff is real. F_care has the fewest overreaches but at small M is "correct" on IND/DIFF only 22%/9%, answering "unresolved" 75-77% of the time; F_probe has the highest probe cost and wrong attributions where no source exists; F_naive is correct more often but overreaches 100% on COPY at every M. P7 (the v1 failure was specific) was only partly checked: overreach was 87-100% on the shared worlds in v1, which matches, but I did not inspect which wrong claim types F_care made.

## What this supports and doesn't
- Supports (within this toy): when failure patterns are observationally identical across causes, the attribution step is where failure-first reasoning overclaims, and a procedure that keeps the range open and probes only on the ambiguous signature avoids that at modest probe cost.
- The discipline itself depends on a guard whose calibration (flag-noise rate) must be known. v1 and v2 show that a miscalibrated guard turns "careful" back into overreach on exactly the cases it exists for.
- Design limits: the correct answer for identical signatures ("unresolved") was written into the scoring key by me; the world family is closed (an unknown fifth world, say both agents copying a hidden third, would be mis-claimed by every procedure here); F_care was written knowing the worlds. It shows discipline reduces overreach given a right family, not discovery of the family.
- Not shown: that a real agent forms and keeps such guards, or that repairs persist downstream.

## Next contacts
1. Add an unknown world not in the claim vocabulary and score "none of the above" as an honest claim.
2. Replace the known-eps guard with an estimated one (sham arm) and see how much overreach returns.
3. Independent reimplementation (ChatGPT) from the header alone, especially the scoring key.
4. Add downstream cached answers so repair persistence is scored, not only the cause claim.
