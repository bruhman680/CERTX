# Exact output schema

`python experiment.py --output run` writes `run/ROWS.json` (array of exactly 144 row objects) and `run/SUMMARY.json` (object). It refuses to overwrite either existing result file. Execution logs, runtime, environment and pre-run provenance are captured by the invoking experiment controller.

Every mathematical rational is a canonical `Fraction` string: integers are `"0"`, `"1"`, etc.; other values are `"numerator/denominator"`. Counts are JSON integers; decisions are booleans. Only keys ending in `_display` contain floating-point square roots. Unavailable numerical results are JSON null. Interval objects always have rational `lower` and `upper`, including endpoints. No floating-point value participates in a decision.

## Main row

- `row_id`: `PROBE:BIAS:CONTRACT:rho=RATIONAL`; `probe`, `bias_case`, `contract`, `rho` specify the grid position.
- `world`: `world_id` (`PROBE:BIAS`), `alpha`, `beta`, `bias_a`, `bias_b`, `true_gap`, `true_nonsingular`, `orthogonal_n_s` (true), `signal_norm` (1), `nuisance_norm` (rho).
- `observations`: `y_a`, `y_b`, `r_a`, `r_b`. References are null for BLIND/WIDE and rational for the reference contracts.
- `method`: `assumption` prose; `declared_radius`; integer `primary_scalar_measurements`, `extra_scalar_measurements`, `total_scalar_measurements`; `reference_role_authority_supplied`; `declared_bias_intervals` with `a`/`b` interval objects; `actual_bias_contract_valid` (both actual biases inside the declared bias intervals).
- `coefficient_intervals`: `a` and `b` interval objects. `compatible_gap_interval` is the true-compatible beta-minus-alpha interval.
- `coverage`: booleans `a`, `b`, `both`, `true_gap` (true gap in compatible interval).
- `gate`: `intervals_nonempty`, `gap_strictly_excludes_zero`, `status` (`PASS` or `WITHHOLD`), `reason` (`gap_excludes_zero`, `empty_intervals`, or `gap_contains_zero`). Empty intervals are represented as an independent flag, not point unavailability.
- `point`: rational `alpha_hat`, `beta_hat`, `h`, `delta_a`, `delta_b`; boolean `available` (h != 0), `offered` (gate pass and available); `unavailable_reason` (null or `zero_point_gap`); rational-or-null `nuisance_coefficient`, `signal_gain`, `relative_error_squared`; float-or-null `relative_error_sqrt_display`. The diagnostic point is retained whenever available even if withheld.
- `envelope`: `conditional_on` names coefficient coverage, orthogonality and known norm ratio; rational `error_radius_a`, `error_radius_b`; `available`; rational-or-null `relative_error_squared_upper_bound`; float-or-null `relative_error_sqrt_upper_bound_display`; boolean-or-null `actual_error_within_envelope` (null iff h=0); `condition_satisfied` equals coefficient coverage. The envelope uses the fixed point h.
- `raw_budget`: rational `relative_error_limit` (1/10) and `squared_limit` (1/100); boolean-or-null `actual_point_meets_budget` (null iff h=0); `raw_certified` iff gate passes and available envelope squared <= 1/100; `false_raw_certificate` iff raw certified and actual point error squared > 1/100. Actual truth is used only to evaluate the certificate, not to issue it.

## Summary

Metadata: `study`, `authored_exact_toy`, `independent_repetitions` (0), `probability_claims` (false), `grid` (probes, biases, contracts, rational rho_values, 12 distinct worlds and 144 rows), `raw_budget`, `scope`.

Count objects appear at `totals`; by contract at `by_contract`; by probe at `by_probe`; by bias at `by_bias`; by rational rho string at `by_rho`; and nested contract then bias at `by_contract_and_bias`.

Every count object has the following integer fields:

- `rows`, `coefficient_coverage`, `actual_bias_contract_valid`, `gate_pass`, `gate_withhold`, `empty_intervals`, `true_nonsingular`, `true_nonsingular_withheld`, `true_singular_gate_pass`.
- `point_available`, `point_unavailable`, `point_offered`, `exact_point_recovery` (available diagnostic point with actual error squared exactly zero).
- `conditional_envelope_checks` (covered and point available), `conditional_envelope_violations` (covered, available and actual error exceeds envelope), `uncovered_envelope_violations` (uncovered, available and actual error exceeds envelope).
- `actual_point_meets_raw_budget` (available diagnostic point meeting budget), `raw_certified`, `false_raw_certificates`.

`ambiguous_worlds` is separate from every main-grid count, with `included_in_main_grid_counts` false. `worlds` has two objects (`OBSERVED_COPY` and `ALTERNATIVE`) containing `label`, exact `alpha`, `beta`, `bias_a`, `bias_b`, `true_gap`, `true_nonsingular`, `y_a`, `y_b` and `contract_diagnostics_at_rho_one` (four full rows as defined above, one per contract, bias_case `AMBIGUITY`). These are the exact (1,1), (3/25,-3/25) bias world and the (28/25,22/25), (0,0) bias alternative. Other fields are `primary_observations_identical` (true), `valid_reference_observations_differ` (true), and explanatory `interpretation`. These eight diagnostic rows are two worlds × four contracts at rho=1, outside the 144-row main grid. Their probe equals their label, world_id is `LABEL:AMBIGUITY`, and row_id is `LABEL:AMBIGUITY:CONTRACT:rho=1`. Observational equivalence concerns the two scalar primary readings only: under the same fixed orthogonal n and s, the worlds have different Dprime vectors; full-vector equivalence is not claimed.
