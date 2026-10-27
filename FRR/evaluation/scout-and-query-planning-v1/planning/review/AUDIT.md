# Independent exact artifact audit

PASS on the first audit execution; exit 0, empty stderr, 1.308170494 seconds elapsed. `audit_runtime.json`, `audit.stdout`, `audit.stderr`, and `AUDIT.json` preserve this execution. No main source or result was modified and no main rerun occurred. `AUDIT_COUNTS.json` records a supplementary TSV-to-audited-JSON consistency check and artifact totals.

The audit never imports `experiment.py`. It reconstructs observations and prior weights from saved latent worlds, independently optimizes every saved belief using exact Fraction arithmetic, inspects every saved action and transition, and replays every selected ordinary and quality-oracle policy separately in every positive-weight world. The reviewer previously read main source during prospective source review, so this is an independent implementation with non-blinded source review, not a blinded replication or validation of source-paper claims.

Checks passed for 512 saved world rows across four priors; 416 positive-weight world/prior pairs; 3,993 ordinary-plus-oracle belief states; 8,301 action values; 9,432 observation transitions; 2,080 ordinary and 2,080 oracle world/budget policy replays; 192 fixed-subset entries with 1,560 outcomes. All 20 TSV root rows match the independently audited JSON.

All posteriors, feasible-T sets, certificates, branch masses, action availability, stop choices, remaining budgets, path costs and duplicate-observation world aggregation agree exactly. Every unresolved belief has target probability 1/2. Ordinary root support contains all positive-weight worlds and evolves only through actual queried observations; oracle roots alone receive free quality conditioning.

The exact root values match every prospective prediction in `MATH.md`. Each pair below is (resolution probability, expected query count).

| Prior | B=2 adaptive | B=3 and B=4 adaptive | B=2/B=3 best fixed | B=4 best fixed | B>=2 oracle |
| --- | --- | --- | --- | --- | --- |
| FAIR | (1/2,3/2) | (3/4,9/4) | (1/2,2) | (3/4,4) | (3/4,3/2) |
| PRIMARY_FAVORED | (3/4,7/4) | (13/16,33/16) | (3/4,2) | (13/16,4) | (13/16,13/8) |
| REFERENCE_FAVORED | (3/4,7/4) | (13/16,33/16) | (3/4,2) | (13/16,4) | (13/16,13/8) |
| BOTH_BAD | (0,0) | (0,0) | (0,0) | (0,0) | (0,0) |

All policies at B=0 or B=1 stop immediately with (0,0). BOTH_BAD stops immediately at every budget. For nontrivial budgets FAIR and PRIMARY_FAVORED begin with C; REFERENCE_FAVORED begins with M. At B=3 the chosen policy completes the first good route or, when its first scout is bad, scouts the second route and completes it only when good. The fourth budget unit is unused because it cannot improve resolution.

At B=3, adaptive success exceeds best fixed-subset success by 1/4 for FAIR and 1/16 for either asymmetric prior. At B=2 the privileged oracle exceeds ordinary adaptive success by those same amounts. At B=4 all modes have equal resolution. Fixed-subset costs include mandatory full-subset querying, so cost gaps combine contingent stopping and route selection. These are exact properties of the declared authored model and known priors, not empirical reliability estimates or evidence of reader, corpus-harness, training or FRR efficacy.
