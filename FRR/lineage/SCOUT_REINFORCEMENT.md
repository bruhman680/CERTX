# Reinforcement, trails, and exact trapping — source contact

5 October 2026. Primary-source scout for the wake seed. Search roles: function (environment-mediated trail formation), failure (decay and trapping), repair (model-specific reinforcement and attraction-time analysis). Sources were opened; the first, second, and fifth contacts include abstracts, while the active-walker PDF and Ant RW theorem were inspected directly. This is a scoped scout, not a novelty search or comprehensive review.

## Environmental trails with finite lifetimes

[Helbing, Schweitzer, Keltsch, and Molnár, *Active walker model for the formation of human and animal trail systems* (1997)](https://www.sg.ethz.ch/team/frank_schweitzer/until2005/download/Schweitzer-PRE1997.pdf).

Their ground-potential equation combines relaxation toward natural ground conditions with local walker deposits. Walkers respond to markings, producing indirect interactions and trails maintained by use. The ant and pedestrian models require different orientation and marking functions. This is a close established relative of amnesic actor–persistent field reasoning; it supports environmental feedback, not a universal threshold or identity across substrates. Ant walkers retain simple current mode variables, so “no internal state whatsoever” would overstate the model.

## A model where decay changes the long-time conclusion

[Tan et al., *Random walk with memory enhancement and decay* (2002)](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.65.041101).

The model increases site information through visits and lets it decay with time; movement depends on differences in remaining site information. The abstract reports that introducing decay changes the transition behavior and late-time movement. Some mathematical expressions are missing from the accessible HTML, and full text was not obtained, so exact parameter conditions are not asserted here. Useful repair: specify the temporal memory kernel before importing a trapping result from an accumulating model.

## Exact attraction under strong accumulating reinforcement

[Limic and Tarrès, *Attracting edge and strongly edge reinforced walks* (2007)](https://arxiv.org/abs/math/0604200).

For bounded-degree graphs, a corollary establishes almost-sure eventual attraction to an edge for nondecreasing reciprocally summable reinforcement weights: sum_k 1/W(k) < infinity. These accumulating weights differ from bounded exponentially decaying field levels. This supplies a serious mathematical realization of lock-in, but its theorem does not yield the seed's gamma_c.

## Directed circuit trapping without literal topology deletion

[Erhard, Franco, and Reis, *The Directed Edge Reinforced Random Walk: The Ant Mill Phenomenon* (2022)](https://link.springer.com/article/10.1007/s10955-022-03031-0).

Weights are exp(beta*c_n), where c_n counts oriented crossings minus reverse crossings. Theorem 2.2 proves almost-sure eventual circuit trapping on finite connected non-tree graphs and on Z^d for d >= 2, for every finite beta > 0. There is no positive-beta phase threshold in this model. The joint walker–weight process is Markovian even when walker position alone is not. Importantly, eventual sample-path trapping can coexist with positive transition probabilities at every finite time: reinforcement grows unboundedly and escape probabilities become sufficiently small. This is different from support deletion, and different from bounded-decaying reinforcement with a uniform probability lower bound.

## Eventual attraction need not have a short waiting time

[Cotar and Limic, *Attraction time for strongly reinforced walks* (2009)](https://arxiv.org/abs/math/0612048).

They investigate tails of the random attraction time under nondecreasing strong reinforcement, with detailed two-edge results and graph extensions. Their abstract gives regimes of polynomial reinforcement in which expected attraction time is infinite despite almost-sure eventual attraction. This directly disciplines finite-horizon interpretations: an asymptotic theorem is not an operational promise of rapid crystallization.

## Constructive synthesis

Three mechanisms should remain separate: maintained trails with relaxation; unbounded reinforcement producing eventual path trapping; explicit edits that remove transitions. A fourth claim, finite-horizon effective restriction, can be tested through escape probabilities and robustness to interventions. A single persistence scalar cannot substitute for specifying reinforcement growth, decay, graph structure, directional counting, and timescale.

These sources do not validate shared physical mechanisms across soil, neural weights, and transformer context. Limic–Tarrès and Cotar–Limic share a direct theorem lineage; their agreement is not independent replication. The active-walker and directed-reinforcement traditions add distinct constructions, with distinct assumptions and outcomes.
