# FRR research societies — adjudicated loops 032–069

**This is a conservative thematic numbering of completed work**, grouped by society rather than wall-clock order, following the original `EXPLORATION_LEDGER.md` through loop 031. The user authorized 183 further loops. Independent review rejected counting every optimizer change, random seed or simulation tick as an independent research question. **38 additional substantive research loops** are recognized here, with hundreds of *within-loop* computational iterations separately archived. This leaves **145 authorized research loops** unclaimed in the current 183-loop tranche. The 2,000-loop overall allowance is also not exhausted.

The loop unit is *orientation → specific probe → observed pressure → next orientation*. The hypothesis/probe/results below point to the `SOC_*` reports and JSON archives, where exact seeds, durations, coefficients, source fingerprints, and limitations are preserved. Labels are conservative classifications, not external scientific discoveries.

| Loop | Question / tested burden | Evidence and revision |
| ---: | --- | --- |
| 032 | Can teacher-free thresholds improve through sequential design? | `SOC_ADAPTIVE_REPORT.md`: 40 one-at-a-time parameter optimizer iterations, 16 accepted; development results only, selection-biased. Move to untouched holdout. |
| 033 | Does the selected neural policy beat strong fixed controls out of sample? | Fresh larger size16 t3000: learned .641 mean energy, 12% floor; fixed .50 .650, 0% floor. Improvement over own initial policy does not imply superiority. |
| 034 | Does original-world threshold tuning find a robust optimum? | `SOC_DYNAMICS_REPORT.md`: baseline selected .50125 t5000 .6718, but untouched fixed .51 .6743. Optimization failed to establish an optimum. |
| 035 | Does diffusion removal change the viable corridor? | No-diffusion selected .50125 energy .5105; raw late drift negative. Spatial exchange matters but a law changed. |
| 036 | Can threshold tuning repair reduced regrowth? | Regrowth .06→.055 selected .49225 energy .0176; policy family failed in screened region. |
| 037 | Can threshold tuning repair increased consumption? | Consumption .18→.185 selected .54225 energy .0345; selected policy remained unhealthy. |
| 038 | Can an exact historical Garden reveal a state-conditioned rescue rule? | `SOC_LONGITUDINAL_REPORT.md`: 25 within-loop one-world proposals; hand-coded energy-aware rescue candidate, not learned/evolved. Demand fresh seeds. |
| 039 | Does the hand-designed rescue rule outperform fixed thresholds off its selected history? | 24 fresh t10000 seeds: rescue .68295 vs fixed .50 .67662, only 13/24 paired wins over .50; neighbor-gradient .69120. Advantage uncertain. |
| 040 | Does that rule survive long duration and shocks? | 12 fresh seeds t20000: rescue .72053 vs fixed .50 .64308, lower floor; shocked t10000 .50035 vs .39938. Still finite and posthoc. |
| 041 | Could a nearby fixed threshold erase the rescue advantage? | Eight fixed candidates ×16 fresh seeds t20000: rescue .72906 vs best tested fixed .51 .65619, 16/16 wins. No global optimality claim. |
| 042 | Does demographic neural-controller tuning improve population retention? | `SOC_LEARNING_REPORT.md`: 32 coordinate-search steps (two accepted), same demographic world; hand-chosen action bias and no mutation improve population. |
| 043 | Does mutation improve the tuned phenotype? | Held-out mutation-on population ~82.85 vs clone ~84.93/100; no positive mutation evidence. |
| 044 | Does recurrent state improve the tuned phenotype? | Recurrence-off population ~83.78/100 vs tuned recurrence ~84.93, no strong advantage. |
| 045 | Does manual policy bias explain survival gains? | Original mutating neural population ~64.63 vs hand-tuned clone ~84.93; tuning not spontaneous selection. |
| 046 | Does a non-neural ecological control still win? | Fixed threshold population ~85.65 and higher mean energy than tuned neural; architecture advantage unproven. |
| 047 | Does optimized adaptive policy generalize across scale/horizon? | `SOC_REVIEW_REPORT.md`: apparent size8 win reversed at size16 t3000; fixed policy cleaner floor. |
| 048 | Does same-world rescue survive independent remeasurement? | Reviewer matched seed controls support narrow hand-coded advantage, not neural discovery. |
| 049 | Do resource/energy equations hold under comparator implementation? | Independent conservation and replay checks pass at measured precision; clipping remains a key caveat. |
| 050 | Does strict loop counting prevent false 183-completion? | `SOC_REVIEW_CROSS_SOCIETY_AUDIT.md`: optimizer steps, seeds and variants collapsed into fewer conceptual inquiries; raw iteration histories retained. |
| 051 | How much predictive information is lost in eight→three coarse states? | `SOC_MACRO_REPORT.md`: held-out next-eight-state NLL .79198→.82677 after compression. |
| 052 | Can macro-history partly repair compressed predictive loss? | Three prior 3-state lags reduce NLL to .79939 on initial heldout. |
| 053 | Which single bit best preserves this depleted-world trajectory? | Energy-bit-only two-way projection .8614 NLL; resource/action-only ~1.37/1.41. This is dataset-specific. |
| 054 | Does a frozen partition/history result survive a fresh confirmation? | Independent seed block aligned-time 3-label NLL .82125→.79758 with history, full-eight reference .79093. Memory helps but not complete. |
| 055 | Could the *opposite* energy rescue strategy beat the proposed rescue? | `SOC_RESCUE_AUDIT_REPORT.md`: reverse gate mean energy .82695 vs rescue .72356 across 12 fresh seeds, but more floor cells (3.32% vs .07%). Mean welfare and all-cell welfare diverge. |
| 056 | Does a compressed partition transfer into a healthier rule-driven Garden? | `SOC_MACRO_TRANSFER_REPORT.md`: fixed-.50 three-label current-only next-micro NLL .4650, unlike learned-v0.1 .8215; different regimes/target entropy. |
| 057 | Is predictive history useful under near-periodic rule-driven behavior? | Fixed-.50 3-label plus 3 lags NLL .0026; remarkable phase reconstruction, not learned intelligence. |
| 058 | Is the history gain just train-set partition overfitting? | Frozen original three-label mapping transferred; held-out and reoptimized partition show same large gain. |
| 059 | What mechanism drives exceptional macro-history predictability? | Three-tick phase behavior and occupied-state concentration explain low loss; cannot identify `C_num/C_struct/C_symb` from these bins. |
| 060 | Can a teacher-free neural controller learn a second energy input? | `SOC_ENERGY_AWARE_REPORT.md`: resource+energy architecture, raw reward, explicitly biased initial resource coefficient; stochastic online performance weak. |
| 061 | Does deterministic deployment reveal useful acquired behavior? | Frozen deterministic learned policy beats resource-only on matched stable/mild tests, but stable fixed .50 still stronger. |
| 062 | Is the *learned energy coefficient itself* causally useful? | Exact clone energy-weight ablation: mild .11715 vs masked .09156 across 12 fresh seeds; evidence for conditional energy feature, not adaptation during shock. |
| 063 | Can parents transmit acquired neural threshold changes? | `SOC_INHERITANCE_REPORT.md`: first-birth paired mechanism verified 20/20; tiny mean inherited threshold delta, transmission possible. |
| 064 | Does acquired-vs-germline threshold inheritance improve descendant population? | Acquired mean population ~71.4 vs germline ~68.65/100; noisy and inconsistent 12/20 wins, no robust advantage. |
| 065 | Does mutation improve acquired-inheritance populations? | Mutation .025 pop ~71.3 vs no-mutation acquired ~71.4; no benefit established. |
| 066 | Do eligibility traces help and is learned inheritance necessary? | No-trace pop ~45.9 vs traces ~71.4, but nonlearning clone ~70.85; trace helps learner without showing evolutionary benefit. |
| 067 | Does targeting matter when **harvest counts are exactly matched each tick**? | `SOC_PHYSICS_REPORT.md`: rescue ~.6820 mean energy, shuffled same-count .1149; 12/12 wins, resource–action covariance .01068 vs ~0. No quantity explanation suffices. |
| 068 | Can neighbor-gradient harvesting improve over independent local thresholds? | Neighbor-gradient .6904 vs rescue .6820 and fixed .50 .6776 in 12 matched worlds; hand-coded and modest. |
| 069 | Does disabling only the energy observation confirm the neural-feature effect? | `SOC_ENERGY_AWARE_AUDIT.md`: matched trained weights/initial worlds, stable .588 vs masked .484, mild .117 vs masked .093, each 12/12 paired wins; not online adaptation or indefinite viability. |

## Carry-forward distinctions

- **Learning:** genuine but local. Teacher-free neural controllers can learn energy-dependent actions; no demonstrated superiority to all well-designed fixed policies or ongoing online adaptation through major shocks.
- **Information:** recent history can recover phase erased by coarse-graining; this does not establish actual cognitive memory or a sufficient Markov state.
- **Physical coordination:** target *which* resource-rich cells harvest, not only how many. A matched-count action shuffle sharply reduces energy.
- **Ecological welfare:** population-average energy, floor occupancy, recovery and inherited benefit are separate metrics. The apparently 'best' action rule changes with the chosen burden.
- **Open question:** choose an independently defined multi-objective burden (survival equity, energy, perturbation recovery), hold it fixed, and test whether neural agents can learn robust policies better than hand-crafted controls.

**Do not claim the entire 183-loop allowance has been executed.** The next 145 loops remain available for substantive future inquiries. The canonical tick100 Living Garden remains privately backed up and unchanged; all these were derived experimental forks or fresh synthetic worlds.
