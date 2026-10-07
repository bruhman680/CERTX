# Experiments 04: garden checkpoint wake/archive reset

Executed 2026-10-07 locally, Python 3.12.14, NumPy 2.3.5. Supplied originals remained unchanged. Outputs are in `outputs/experiments-04/`. This is execution of recovered source, not recovery of an earlier execution result. Shared FRR/source ancestry is not independent empirical corroboration.

## Commands and provenance

Read NOW.md, compact runtime seed in FLUID_RELATIONAL_REASONING_v0.5_CANDIDATE.md, RECOVERY_NOTE.md, garden_wake_probe.py and true_garden_fluid_settled.py. Handoff/history were copied to context-inspected.txt for local availability but not used as experimental evidence. Original-copy hashes recorded in provenance.sha256:

- garden_wake_probe.py: `1978da2f5c989b2d15177c4f11c7deb3afd0649f46383f316927713ecb9f6fa7`
- true_garden_fluid_settled.py: `d8156b72cedc6deddf39dc2a4d4e67fcbc8824a1469d9666672ba801bb5b77bd`

Actual successful setup/execution commands (after an initial nonexistent-working-directory tool failure, which executed nothing):

```sh
mkdir -p /workspace/frr-distributed-2026-10-07/outputs/experiments-04
cp /workspace/recovered-originals/2026-10-05/garden_wake_probe.py /workspace/recovered-originals/2026-10-05/true_garden_fluid_settled.py /workspace/frr-distributed-2026-10-07/outputs/experiments-04/
# In that output directory:
python garden_wake_probe.py > original-probe.txt
sha256sum /workspace/recovered-originals/2026-10-05/garden_wake_probe.py /workspace/recovered-originals/2026-10-05/true_garden_fluid_settled.py > provenance.sha256
python inspect_checkpoints.py > checkpoints.json
```

The added inspection script preserves the engine, deep-copies each checkpoint, applies the same four ablations, and records horizons 0/1/3/12/100. It adds recomputed mean fitness and cached-minus-recomputed fitness to the supplied observables. This reversible measurement improvement is implemented only in the isolated output folder.

## Observed results

Seed 99, K=3, mutation .08, checkpoints 40 and 120, continuation 100 steps.

Checkpoint 40 has zero soil archive and zero wake; all four reset branches produce identical observed snapshots. Consequently this checkpoint is a null intervention, not evidence that a present field is behaviorally irrelevant.

Checkpoint 120 has wake .7343, archive 27, richness .5823 and fitness-field delta .0116. Immediate clearing of wake yields richness .3375 and delta zero. Clearing archive yields richness zero while retaining wake .7343 and delta .0116. Clearing both yields zeros. Initial K remains 2.3305 in every branch.

| Intervention | after 100: K | richness | wake | archive | fitness-field delta | mean fit |
|---|---:|---:|---:|---:|---:|---:|
| unaltered | 0 | 1 | 1.7640 | 68 | .0161 | .6153 |
| clear wake | 0 | 1 | 1.1722 | 71 | .0303 | .5046 |
| clear archive | 0 | 1 | 1.6985 | 41 | .0305 | .4880 |
| clear both | .3947 | .8721 | 1.0413 | 42 | .0096 | .5440 |

All final populations are 30. Population equality, K saturation and richness saturation compress differences still visible in wake, archive and fitness.

Snapshot mean_fit is cached candidate fitness. Immediately after wake clearing it remains .5426529 although recomputation with the cleared field gives .5310337. The supplied record's fitness_field_delta correctly recomputes fitness, but snapshot mean_fit does not immediately expose this intervention. This is a measurement distinction, not evidence that wake has no direct fitness effect.

At horizon 1, K values are 2.294139 (unaltered), 2.307805 (clear wake), 2.313039 (clear archive), 2.326705 (clear both). Richnesses are .606988, .362949, .269488, .025449 respectively. Deaths replenish archive even after clearing it; field clearing is not a maintained zero-field condition.

## Scope, rival and surviving relation

The archive and field are separable stored objects but coupled functional inputs. compute_fitness reads genotype-keyed wake. soil_richness combines wake/3 and archive-count/80, saturates at one, and returns zero whenever archive is empty. Richness influences K, compost emergence, dormancy waking and entropy injection; archive supplies compost genomes. Thus archive clearing changes controller input even with unchanged wake. It is not a pure deletion of historical genetic storage.

Deepcopy preserves checkpoint candidates, fitness histories, tables, controller and RNG states. Different branches subsequently consume RNG differently through conditional operations. The serious rival to a pure wake-memory interpretation is richness/controller threshold crossing plus downstream stochastic trajectory divergence, including model-coded fitness supplementation. At horizon 1 unaltered richness exceeds .6, activating entropy injection; reset branches do not. Later differences cannot identify direct genotype wake influence alone.

Surviving domain-specific relation: action deposits genotype-indexed fitness contributions and an archive; resetting either retained component changes later trajectories in this implemented engine. Nothing here establishes a universal field-persistence mechanism, permanent barriers, or cross-domain transfer. This is checkpoint ablation, not common-recipient donor transplantation.

Recommended next reversible refinement (not implemented): factor scoring wake from controller richness in an explicit experimental wrapper, retain separately labelled historical and current-computation snapshots, and predeclare multiple checkpoint seeds. Maintaining field=0 each step would be a different sustained intervention and must be labelled as such. A square comparing reset-then-evolve with evolve-then-reset could measure a defect, but its noncommutation alone would not locate cause; no cube adds useful evidence here.
