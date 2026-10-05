# exp_016: Field transplant in True Garden

**Status:** Executable synthetic demonstration, run 2026-10-05. The recipient was selected to cross a programmed threshold; this is an existence result, not a prevalence estimate or validation of a universal law.

## Question

Can a candidate with the same genome and local state make a different status transition solely because the soil field carries a trace from a different history? Can we separate that trace from the death archive that drives the garden's `K` controller?

## Construction

`true_garden_fluid_settled.py` is the supplied True Garden model retained for this experiment. `exp_016_field_wake_transplant.py` creates independent donors with RNG seeds 17 and 23 and runs each for 120 steps. It then deep-copies a common seven-candidate recipient (seed 7) and transplants donor soil fields and archives independently. The recipient's NK fitness table, candidates, RNG state, and control settings start identical across conditions. Mutation is disabled and the recipient starts in exhale. The target is `seed-4`, genome `011001`. Recipient seed 7 was deliberately selected because its baseline fitness is near the code's `spark`→`proto` criterion.

Run from repository root:

```bash
python EXPERIMENTS/exp_016_field_wake_transplant.py
```

Requires NumPy. The model's optional Matplotlib plot is not part of this probe.

## Observed result

| Transplant | Target fitness at t=0 | Target status at t=3 | Archive count | Integer K at t=3 |
| --- | ---: | --- | ---: | ---: |
| Virgin field, empty archive | 0.633253 | spark | 0 | 3 |
| Donor A field, empty archive | 0.633253 | spark | 0 | 3 |
| Donor B field, empty archive | 0.718547 | **proto** | 0 | 3 |
| Virgin field, donor B archive | 0.633253 | spark | 23 | 3 |
| Donor B field and archive | 0.718547 | **proto** | 23 | 3 |

Donor B's field contains a `0.085294` entry for `011001`; donor A's does not. The B trace decays during replay, but fitness remains `0.717782` at step 3 and changes the programmed status decision. With an empty archive, `soil_richness` is zero even when a transplanted field is present, so the first three field-only conditions have matched K trajectories and the same NK table. The archive alone changes continuous K without creating the target-specific fitness increment.

A separate 100-entry archive with a virgin field saturates richness at 1 and repeatedly redraws the fitness landscape through `inject_entropy`; by step 12 integer K falls from 3 to 2. This is a distinct archive-mediated mechanism. It is not the donor B genotype-specific wake.

## Scope and next contact

This code-level intervention demonstrates that the field can carry a decision-relevant trace relative to a reset candidate. The garden still has one central engine; it does not demonstrate decentralized storage across independent nodes. The experiment does not estimate the frequency of naturally consequential wakes, establish a physical entropy-production rate, or validate the proposed graph-wide `gamma_c` formula. A next pass can predeclare a distribution of recipient states, transplant independently generated fields without selecting a threshold-near seed, and report the fraction of outcomes that change with confidence intervals. Keep the archive and NK table fixed for that estimate.
