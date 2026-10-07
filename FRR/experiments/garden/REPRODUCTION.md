# Garden reproduction — 5 October 2026

The newly supplied engine is copied byte-for-byte into `true_garden_fluid_settled.py`. The two uploaded garden probes are copied without behavioral edits. `reproduce.py` imports these artifacts, reproduces the reported runs, records environment/version provenance, and adds explicit diagnostic interventions. No model API or external physical measurements are used.

Run from this directory:

```bash
python3 reproduce.py
```

Detailed results are in `../../evaluation/results/garden-reproduced-2026-10-05.json`. The original command was also executed directly with plotting set to a noninteractive backend; it generated `garden_settled.png`.

## Reproduced observations

The original seed-99, 2,000-step run gives last-500 means K=0, diversity approximately .588, soil richness=1, and fitness approximately .621; final population is 33. These match the supplied audit at printed precision. The code's population handling is not a strict cap of 30: it removes at most one spark and may add more candidates or have no eligible spark to remove.

The transplant gives reference-genome fitness .633253 in the virgin field and .718547 in donor B's field at time zero. At step three, the donor B field conditions promote the target to proto while virgin, donor A, and archive-B-only conditions retain spark. The transplanted field's fitness effect is a direct programmed input to the promotion criterion. This is a causal demonstration within this model under deliberately selected initial conditions, not a prevalence estimate or physical law.

The step-120 reset probe also matches: clearing only field removes immediate field fitness contribution; clearing only archive zeros richness while leaving the field contribution present. At 100-step replay, clearing both leaves K approximately .3947 while the other three branches reach zero. The step-40 reset conditions coincide because both carriers are empty then. Longer trajectories are controlled initial-state replays, not isolated estimates of each carrier's cumulative effect.

## Mechanisms visible in the supplied code

- Death writes a genotype-specific field increment and a separate archive record. They have distinct readers.
- `soil_richness` ignores the field when the archive is empty, and reaches one from 80 archive entries even if the field is empty. Field decay cannot prevent that archive floor.
- The K controller includes a negative richness term and clips to zero. The observed boundary result does not establish interior self-regulation. Changes in rounded K redraw the landscape; entropy injection also redraws it.
- Cross-pollination creates a new child; it does not modify parent genomes. With mutation disabled, the transplant's reference target stays fixed. This resolves the specific uncertainty raised in the previous comparison.
- Ordinary and injected mutation update genomes without recomputing positions. Consequently partner choice and measured diversity can use stale genotype positions.
- The dormant transition is unreachable: three last values above .6 force a five-value nonnegative mean above .36, incompatible with the simultaneous mean below .3.
- `verifications` is incremented each step. It counts repeated evaluations, not independent evidential tests.
- With six loci, there are at most five other partners. Allowing K=6 or 7 allocates entries for nonexistent partners; not all table entries can be reached. This does not crash these runs, but K no longer has its advertised NK interpretation beyond five.
- The wake log takes its baseline after decay and after possible composting; it is not a net-field-change ledger. Distinguish writing, decay, deletion, and net change in future logging.

“Hidden EPR” remains an unsupported physical interpretation: the code computes fitness increments and decay, not thermodynamic entropy production. Preserve the soil image as a model interpretation while keeping measured behavior separate.

## Scope and next repair

Execution supports the reported behavior of the submitted construction. It does not establish general FRR benefit, universal field-memory laws, or calibrated cognitive metrics. Selected-seed demonstrations and multiple seeds of the same implementation do not become independent mechanistic confirmation.

The original is preserved. A future corrected variant should separate carrier metrics, update positions after mutations, make dormancy reachable under a declared rule, enforce intended resource bounds, constrain NK partners consistently, and state whether landscape contributions persist across K changes. Compare each repair against the original before redesigning everything at once.
