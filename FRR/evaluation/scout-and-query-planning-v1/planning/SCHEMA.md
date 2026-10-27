# Exact finite planning artifact schema

`experiment.py` uses Python's standard library and `fractions.Fraction` throughout all probability, posterior, objective, and cost calculations. No sampling or floating point arithmetic is used. It is a finite authored secret-sharing proxy, not an actual reader, harness, or model-training evaluation. Run only after the root protocol has been frozen:

```sh
python planning/experiment.py --output-dir planning/run
```

The output directory receives `results.json` and `root_outcomes.tsv`. The script is inert when imported. Every rational quantity in JSON and TSV is an exact reduced `numerator/denominator` string, including integer-valued probabilities and expected costs. Counts, budgets, masks, latent bits, and fixed subset query costs are JSON integers. Observation tuples become JSON arrays.

## Finite model

There are 128 enumerated raw latent microstates. IDs 0 through 127 follow lexicographic binary enumeration of `(T,qP,qR,X,Y,u,v)`. `T,X,Y,u,v` are independent fair bits. `qP,qR` are independent quality bits with known probabilities `pP,pR`; these quality bits are independent of the other five bits. Their four prior labels are `FAIR` `(1/2,1/2)`, `PRIMARY_FAVORED` `(3/4,1/4)`, `REFERENCE_FAVORED` `(1/4,3/4)`, and `BOTH_BAD` `(0,0)`.

The records, in canonical action order, are `P=X`, `C=(qP,kP)`, `R=Y`, `M=(qR,kR)`. Here `kP=X xor T` if `qP=1` and `u` otherwise; `kR=Y xor T` if `qR=1` and `v` otherwise. All queries cost one. There is no repeated query. A belief is identified only if every compatible positive-weight microstate has the same `T`. Zero-probability microstates are retained in world and duplicate-observation tables but excluded from beliefs and certificates.

## `results.json`

Top-level fields are `schema_version`, `experiment`, `record_order`, `latent_order`, `scope`, `objective`, and `priors`. Each of the four `priors` entries contains:

- `prior`, `pP`, `pR`: the prior label and exact quality probabilities.
- `worlds`: all 128 rows, with `world_id`, named `latent` bits, exact unconditional `probability`, and named record `observations`.
- `positive_weight_microstates`: size of this prior's positive support.
- `duplicate_observations.per_record`: one table per record. `duplicate_observations.joint_all_four` groups by all four record values in canonical order. Each row gives `observation`, `raw_microstate_count`, `positive_weight_microstate_count`, all `world_ids`, and total unconditional `probability`. Counts refer to raw latent worlds, not distinct observable worlds; zero-mass groups remain explicit.
- `roots`: exactly five rows, for budgets 0 through 4. Every root gives the `root_state`, `chosen_action`, optimal `resolution_probability`, optimal `expected_query_cost`, `terminal_outcomes`, `fixed_subset_baseline`, `resolution_advantage_over_best_fixed_subset`, and `quality_informed_oracle`.
- `belief_states`: the complete DP state dictionary for all five root budgets, including the branches of every admissible action, even actions not selected by the optimum.
- `quality_informed_belief_states`: the analogous DP dictionary for the oracle's quality-conditioned initial beliefs.

## Belief states and policy

State IDs have the form `b{remaining_budget}_m{queried_mask_hex}_w{support_bitset_hex}`. The bitset uses bit `i` for world ID `i`. IDs uniquely describe the belief, queried records, and remaining budget within a prior. A state has `remaining_budget`, `queried_mask`, `queried_records`, `support_world_ids`, unconditional `prior_mass`, a full exact `posterior` list (`world_id`, `probability`), `feasible_T` (the sorted compatible target bits), and `certified_T` (0, 1, or null). Mask bits 0,1,2,3 denote P,C,R,M.

The value and policy fields are `resolution_probability`, `expected_additional_cost`, `chosen_action`, and `actions`. An action row contains its `action` (`STOP` or a record name), exact value and cost, and `branches`. A query branch gives the observed value, its exact conditional probability, and the `child_state` ID. `STOP` has no branches. Every child has one fewer unit of remaining budget and its queried record added to the mask.

The Bellman objective lexicographically maximizes probability of a certified decision and then minimizes expected additional query cost. All available actions are evaluated. Strict improvements replace the incumbent; query ties retain canonical order P,C,R,M. `STOP` starts as the incumbent, has cost zero, and resolution equal to whether the present belief is certified. Thus useless queries are not made, and resolved beliefs stop. This is an exact finite dynamic program, not a learned policy.

Root `terminal_outcomes` exhaustively replays the selected policy. Each leaf contains the sequence of `path` query/observation objects, its `terminal_state`, unconditional probability relative to that root, realized `query_cost`, `feasible_T`, and `certified_T`. Leaves sum to one; their probability-weighted resolution and cost equal the DP root values. These equalities are asserted during execution.

## Comparators

`fixed_subset_baseline.all_subsets` enumerates every fixed subset of size at most the budget, including the empty set. Rows provide canonical `records`, exact `resolution_probability`, and integer `query_cost`. Its `outcomes` enumerate each joint observation with exact conditional probability, compatible world IDs, feasible target bits, and certificate. `best` maximizes resolution then minimizes subset size; any remaining tie retains combinations enumeration order. Every chosen record is charged on every world, with no free adaptive early stopping. The reported adaptive-minus-fixed difference compares resolution only. Their costs follow different stopping conventions and are not presented as a fair cost improvement.

The `quality_informed_oracle` receives qP and qR free before querying, but does not receive T. It runs the same DP within each positive-mass quality branch and then averages values. `quality_branches` gives qP, qR, unconditional branch probability, oracle root `state`, conditional resolution, and conditional expected cost. The aggregate includes `extra_information`, `resolution_probability`, and `expected_query_cost`. It is an explicitly extra-information comparator. For these priors its exact resolution is zero at budgets 0 and 1 and `1-(1-pP)(1-pR)` at budgets 2 through 4; execution asserts this independently specified formula against the oracle DP.

## `root_outcomes.tsv`

The 20 data rows contain `prior`, `pP`, `pR`, `budget`, `resolution`, `expected_cost`, `best_fixed_resolution`, `best_fixed_cost`, `oracle_resolution`, `oracle_cost`, and `first_action`. Full policies, terminal branches, every fixed subset, and microstate/duplicate-observation counts are in `results.json`.
