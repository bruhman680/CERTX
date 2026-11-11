# Learning / evolution society — sequential hypothesis search and inherited-behavior controls

**Status:** Completed synthetic research-search study, consisting of **32 sequential hypothesis-update search movements**, **4 held-out diagnostic movements**, and **1 additional held-out mutation / fixed-policy counterfactual**. These are **37 documented computational research movements** under one scientific line of inquiry, *not* 37 independent scientific discoveries, generations, or universal laws. Preserve that distinction when integrating with the broader FRR Garden ledger.

## Question and world

Can inherited recurrent neural-cell controllers improve ecological survival through mutation, recurrent memory, and selection, *without changing world physics*?

All probes use the separately defined **EvolutionGarden demographic world**, not the original fixed-occupancy neural Garden. Living cells can die and reproduce, with finite age, local offspring, transferable weight vectors, mutation, and explicit energy cost of reproduction. Each runs a 10×10 grid for 1,500 ticks. Environmental rules and demographic coefficients stay fixed across all arms. Initial cell occupancy, local resources and pseudorandom seed are matched within paired comparisons. The hand-written `.55` threshold controller receives the *same* world laws but bypasses the neural action head; it is a baseline, not genetic adaptation.

## Exploration phase: 32 sequential search movements

Source `SOC_LEARNING_search.py`; full per-movement hypotheses, measured scores, decisions and next orientations in `SOC_LEARNING_results.json`. An exploratory history-dependent coordinate search probes three independent design choices:

1. Initial neural action bias (`bact` offset): a **designer intervention** affecting whether cells harvest aggressively.
2. Recurrent-memory matrix gain (`wrec` multiplier): a controlled proxy for strength of recurrent influence.
3. Inherited mutation standard deviation (σ): whether newborns receive exact copies or modified neural weights.

Every proposal is evaluated against its current incumbent using the same six *development* seeds 1110–1115. The predefined scalar design score is `(mean living population/100) + mean energy across all sites`. A candidate is accepted only if it improves this score by more than .004; a rejection reverses the next direction of search. Every chosen step is in `history` as orientation → probe → evidence → accept/reject → next. This is adaptive **designer search**, not autonomous evolution by the cells. Reusing six development seeds also risks overfitting, which is why all primary comparisons below use separate held-out seeds.

**Only two of the 32 search proposals were accepted.** First, reducing the action bias by .45 significantly improved development survival. Second, turning *mutation off* improved the same developmental score. Recurrent gain stayed at 1.0. The chosen controller was simply **a hand-tuned negative action bias with zero offspring mutation**.

## Independent held-out controls: 40 untouched seeds

Seeds 2010–2049, 1,500 ticks. No held-out seed was used during search. Two sources: `SOC_LEARNING_results.json` and `SOC_LEARNING_holdout_results.json`, both with per-seed results, exact parameters, and source SHA-256.

| Policy | Mean living cells / 100 | Mean energy across all sites | Interpretation |
| --- | ---: | ---: | --- |
| Original neural mutation σ=.025, no manual bias | **64.63** | .2632 | Previously implemented evolutionary baseline |
| Manually tuned negative-bias neural, **clonal σ=0** | **84.93** | .3610 | Best searched variant |
| Same tuned neural bias, mutation σ=.025 | **82.85** | .3431 | Mutation did not help in this comparison |
| Original recurrent controller disabled, same tuned clonal genotype | **83.78** | .3642 | Weak population gain from recurrence, not a strong memory benefit |
| Hand-coded non-neural resource threshold .55 | **85.65** | .4187 | Stronger simple-rule baseline under same demographic laws |

Paired seed-level differences:

- Clonal tuned minus original neural: **+20.3 living cells per 100** on average, SD 12.34, positive in 38/40 seeds. This is the effect of **designer-selected initial bias plus changed mutation**, not evidence of natural adaptive evolution.
- Clonal tuned minus same-bias mutating neural: **+2.075 cells**, SD 6.75, wins 20, losses 13, ties 7. The uncertainty is substantial, and a slight clonal advantage does not prove all mutation is harmful.
- Clonal tuned minus non-neural .55 policy: **−0.725 cells**, SD 7.93, wins 20, losses 17, ties 3. No robust population advantage over the simple resource-aware baseline; the latter retains higher mean energy.
- Removing recurrent memory reduced tuned-clonal mean population by **1.15 cells** (paired SD 6.44); it actually raised mean energy slightly, .3642 versus .3610. Thus no meaningful causal benefit from recurrence is established by these aggregate metrics.

## Genotype, phenotype, and memory are different burdens

The standardized action-response probe asks how much a cell's neural harvest propensity changes between synthetic resource input `.3` and `.7`, with other inputs held neutral. The manually tuned controller has average sensitivity ~`.01061`; the original neural controller only ~`.00257`. However this controlled static one-step difference cannot tell whether useful history was stored in the recurrent hidden state, whether descendants were preferentially selected for it, or whether a memory mechanism supports long-term adaptation.

Making reproduction and inheritance available does **not** guarantee helpful mutation. Even though the population grows, genotype changes might be neutral or harmful; survival might reflect initial resources, local geography, or the deliberately changed action bias. In particular, no gradient-learning occurs inside `EvolutionGarden`. We must not silently attribute gains from our **external coordinate search** to the simulated organism society itself.

## Evidence boundaries and next movement

- Development used a small reused six-seed set and posthoc model selection. The 40-seed holdout checks whether the selected design's measured population advantage repeats within this simulator, not whether the chosen weights generalize to nature or a different world.
- All five arms share the *same demographic extension*, which differs from the original fixed-occupancy Garden. Comparing their raw energy to v0.1 results would be confounded.
- Population and mean energy are coarse outputs; neither captures true genotype fitness, frequency-dependent selection, lineage persistence after shocks, or open-ended cultural/cognitive evolution.
- Recurrent scaling at initialization does not by itself test remembering particular events. A controlled history-swap / memory-reset probe with same genotype and exact matched resource states is needed.
- We have not demonstrated mutation beneficial relative to cloning nor a discovered neural harvesting policy better than a simple fixed rule. Both negative controls should remain prominent.

**Strongest next hypothesis:** Selection for resource-sensitive action timing may require a controller phenotype that can represent the timing relation *and* inherit it faithfully. Before further mutation tuning, independently establish genotype–phenotype–fitness linkage and a matched memory-reset experiment where only recurrent state differs.
