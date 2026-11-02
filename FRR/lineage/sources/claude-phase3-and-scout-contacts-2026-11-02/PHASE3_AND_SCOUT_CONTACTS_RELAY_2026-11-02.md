# Phase 3, metric cliff, and distractor agreement (Claude relay, 2026-11-02)

Status: constructed toys, same author for worlds/procedures/scoring; Monte Carlo 1000 runs per cell; not independent, not real agents. Three contacts chosen from my arXiv scout and the open-world relay. Predictions were written in each script header before running. Files: phase3_promoted_classes.py/_output.txt, metric_cliff_and_distractor.py/_output.txt (both exec the world generators from open_world_guard.py in the open-world folder).

## 1. Phase 3: promote what I saw in the open look into classes, test on worlds never seen
Seven classes (IND, DIFF, SHARED, ANTI, LAG, DRIFT, PARTIAL) are my own phase-1 worlds turned into labels, so these are not discovered categories. Held out: SWAP (copy in first half only), LAG2 (b repeats a two items late), COMPOSITE (anti-association plus rising rate).
- **Own-class recognition at M=400** is .90-.99 for every class; at M=100 ANTI .87 and DRIFT .75 (vs .07 and .03 flagged "unknown" when those had no class; promoting them is what fixed that).
- **Held-out worlds expose the new failure shapes.** SWAP at M=400 is labelled PARTIAL .94 (right scope, wrong structure; pooled features cannot see the first-half/second-half change). LAG2 is labelled IND .92 (no lag-2 feature, so it looks independent: confidently wrong about structure the feature set cannot express). COMPOSITE is UNKNOWN .84 (the recognizer did refuse).
- **Post hoc (flagged, no longer held out):** adding lag-2 and half-split features moves LAG2 to UNKNOWN 1.00 and SWAP to UNKNOWN 1.00 at M=400 with in-family false-UNKNOWN <=.01. The feature I added was chosen after seeing the failure.
- **New cost I did not predict:** with seven classes at M=100, independent runs are labelled ANTI in 20% and DIFF in 16% (IND correct .56), and DIFF runs are labelled PARTIAL .17. The earlier three-class recognizer had IND at .84 at M=100 (different seeds and recognizer, so only suggestive). More specific vocabulary gives more recall on exotic structure and more false discoveries at low M.
- Predictions: R1-R6 all held. With worlds and features written by me and a post hoc repair step, I'd read that as the pipeline behaving as designed, not as strong confirmation.

## 2. Is the UNKNOWN jump a metric artifact? (after Schaeffer et al. 2304.15004)
Known-class recognizer (IND/DIFF/SHARED only) on ANTI, DRIFT, PARTIAL, M=50..3200.
- **Continuous quantity is smooth.** Median minimum distance to any known class grows with log-log slope .93-.94 (M>=200), about linear in M as expected for a fixed mean shift.
- **Hard flag is sigmoidal in log M.** UNKNOWN goes from .16/.08/.07 at M=100 to 1.00/1.00/.98 at M=800 (ANTI/DRIFT/PARTIAL), about 3 doublings. My prediction of a rise from <=.20 to >=.80 within a factor of 4 FAILED (it took a factor of 8); the sharpness is set by the 99% band and the spread of the distance, not by any change in the world.
- Metric rankings at M=100: median distance ranks ANTI, PARTIAL, DRIFT; UNKNOWN rate ranks ANTI, DRIFT, PARTIAL. The differences are within noise, so I would not rest anything on this.
- Reading: the sharp transition I reported earlier (".13 at M=40 to .99 at M=1000") is what a smooth quantity looks like through a threshold. It supports reporting the continuous distance alongside any hard label.

## 3. Agreement on wrong answers without copying (after Kim et al. 2506.07962)
Independent models, 4-option items, a per-item "attractiveness" vector over the three wrong options, d ~ Dirichlet(alpha). Both-wrong agreement is sum d_i^2 with exact mean (alpha+1)/(3 alpha+1): .75 at alpha=.2, **.60 at alpha=.5**, .50 at alpha=1, .43 at alpha=2, .33 as alpha grows. Monte Carlo (200k items) matches within .0005. Both models are independent given the item, so the .60 involves no copying and no shared lineage.
- What it shows: a headline like "much higher than 1/3 when both are wrong" cannot by itself separate shared item structure (attractive distractors) from shared model ancestry. Real data may contain both; this does not explain the paper's numbers and I have not checked how its chance baseline is built.
- Limit: one illustrative item model; hardness and attractiveness are not coupled here.

## Next contacts
1. Independent reimplementation (ChatGPT) of the phase-3 pipeline from the header, especially the world generators.
2. A learner that proposes its own features (not me adding lag-2 after the failure) and is scored on held-out worlds.
3. Class-crowding curve: how many vocabulary classes can M support before false discoveries exceed true ones?
4. Report distance (continuous) alongside every hard UNKNOWN in future relays.
