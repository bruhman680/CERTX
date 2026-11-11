# Threshold-policy robustness across altered resource laws

**Type:** One substantive, explicitly *posthoc* research loop: mathematical orientation → matched-seed counterfactual worlds → numerical audit → revised confidence. Results are a designed toy simulator outcome, not evidence that intelligence emerged.

**Artifacts:** `REGIME_DYNAMICS_probe.py` and `REGIME_DYNAMICS_results.json`. Exact per-run endpoints, tail moments, seed provenance, configuration, Python/NumPy versions and SHA-256 source fingerprints are in the JSON. This uses new files and leaves the persistent Living Garden and existing v0.1 physics intact.

## Question

The original resource-threshold rule near `.50` appears almost energy-neutral over 20,000 ticks. Is that an ecologically robust strategy, or merely a narrow consequence of the chosen resource regeneration, consumption and diffusion coefficients?

Under the parameterized resource law,

`R' = clip(R + kappa*(neighbor_mean(R) - R) + alpha*(1-R) - beta*R*A, 0,1)`,

the raw energy budget remains the **original** one:

`delta_E_raw = .25*R*A - .063*A - .022`.

At near-stationary resource levels and with no resource clipping, the globally summed spatial diffusion term vanishes, so

`E[R*A] ≈ (alpha/beta)*(1-E[R])`, giving

`E[delta_E_raw] ≈ .25*(alpha/beta)*(1-E[R]) - .063*E[A] - .022`.

This identifies `alpha/beta` and the policy's resource–action timing as distinct control levers. It also warns that apparent improvements from changing the world must not be credited to neural learning.

## Controlled design

160 finite runs: **8 explicit world regimes ×5 frozen thresholds ×4 matched seeds** `1040..1043`, size16 (256 cells), **5,000 ticks** each, tail averages over the final 1,500 ticks. Thresholds `.48, .50, .51, .525, .55` were selected *after* previous probes; this is screening, not preregistered confirmation. Every regime changes at most **one** coefficient compared with baseline `alpha=.06, beta=.18, kappa=.08`.

Regimes: baseline; diffusion `0,.04,.12`; regrowth `.045,.075`; consumption `.15,.21`. Every condition starts with the identical seeded per-cell initial resource/energy state for the same seed, using the same deterministic threshold rule. Only the declared world-law coefficient changes. These variants are **not** neuron-learning interventions.

## Results: environment can overwhelm threshold optimization

Mean stored energy at tick 5,000 (4 matched seeds each):

| World regime | Threshold .48 | .50 | .51 | .525 | .55 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Original laws | .258 | **.671** | **.677** | .562 | .037 |
| No diffusion (`kappa=0`) | .072 | .513 | .513 | .422 | .037 |
| Half diffusion (`kappa=.04`) | .121 | .600 | .600 | .481 | .035 |
| Increased diffusion (`kappa=.12`) | .303 | .688 | **.702** | .608 | .039 |
| Slower regrowth (`alpha=.045`) | .013 | .017 | .016 | .019 | .019 |
| Faster regrowth (`alpha=.075`) | .989 | .980 | .979 | .981 | .981 |
| Less extraction (`beta=.15`) | .982 | .984 | .981 | .980 | .977 |
| More extraction (`beta=.21`) | .019 | .024 | .023 | .025 | .022 |

The `.50`–`.51` corridor is relatively favorable **among these tested thresholds** under unchanged baseline laws and the diffusion-only variants. Increasing diffusion from 0 to .12 raises the final mean energy at threshold .50 from .513 to .688, consistent with the earlier harvest-phase finding, but this is a changed physical coupling law. The tested winner in that one regime is .51 by a small margin, not a demonstrated universal optimum.

Crucially, decreasing regrowth by 25% (`alpha=.06→.045`) or increasing consumption by about 17% (`beta=.18→.21`) causes **every threshold here to fail badly** by tick 5,000, with substantial energy-floor occupancy. Conversely, faster regrowth or lower consumption pushes every threshold near the **energy ceiling**, which hides policy differences through clipping. Thus apparent stability near threshold `.50` is **fragile to plausible coefficient changes within this invented model**.

## Raw drift diagnostics

Under baseline laws at threshold `.50`, final-tail average raw drift is **+0.00001574/tick**; higher diffusion `.12` at threshold `.51` gives **+0.00003283/tick**. These are tiny margins compared with the severe perturbations:

- `alpha=.045`, threshold `.50`: **−0.00539/tick**;
- `alpha=.075`, threshold `.50`: **+0.00536/tick**;
- `beta=.15`, threshold `.50`: **+0.00400/tick**;
- `beta=.21`, threshold `.50`: **−0.00286/tick**.

All regimes preserve exact global resource mass balance within floating-point precision (maximum audited per-run mean residual ≈`2×10⁻¹⁷`). Raw energy identity errors are below `2×10⁻¹⁵`. At high-energy endpoints the `[0,1]` ceiling clips away excess raw gains; near collapse the floor masks ongoing deficits. We therefore report both raw drift and floor/ceiling fractions separately in the JSON.

## Confidence and corrected interpretation

1. **High confidence within the implemented simulator:** the exact global budget identity, unchanged energy law, numerical regime separation, and source-provenance records are internally consistent.
2. **Moderate within-model confidence:** the `.50`–`.51` threshold corridor is favorable in the **original and tested diffusion-only** worlds for this horizon; close threshold differences may be seed- and time-sensitive.
3. **Low confidence for generalization:** a small change in resource regeneration or extraction reverses outcomes. Four seeds and 5,000 ticks are exploratory. The regime grid and candidate thresholds were selected after earlier observations. These tests do not establish a robust optimum or long-run viability.
4. **No evidence of learned adaptation:** all policies are deterministic, hand-written threshold rules. Altered world laws create or destroy viability by construction, irrespective of neural capabilities.

**Next strong pressure:** Use an unchanged long-lived world and introduce *logged, temporary* ecological perturbations in reversible forks. Evaluate whether a neural controller can adjust its policy after the regime changes, compared with a fixed threshold, while preserving the untouched original living history as the causal reference. That would test adaptive regulation rather than merely tuning a static numerical threshold.
