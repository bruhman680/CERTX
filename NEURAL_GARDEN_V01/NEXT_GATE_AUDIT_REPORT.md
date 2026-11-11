# Independent audit of update-timing gates — scarcity-specific timing fails replication

**Result:** One independent adversarial research loop, using 12 completely reserved audit world seeds **10200–10211**, six matched controllers per seed, 3,000 ticks each (72 independent test trajectories plus deterministic transfer diagnostics). Executed `NEXT_GATE_AUDIT_probe.py` and archived complete `NEXT_GATE_AUDIT_results.json`. No original Garden or gating implementation was changed.

## Precommit and source integrity

`NEXT_GATE_PLAN.md` fixed the scarcity interval, gate windows, three outcome burdens and reserved audit seeds before seeing the original 10100–10111 results. This replication used the exact frozen `NEXT_GATE_garden.py`/`NEXT_GATE_probe.py` without hyperparameter tuning or post-result arm selection. All **7/7 audit source SHA-256 hashes** and **5/5 primary-study hashes** verified against current code; 12 original and 12 audit seed identities are unique and disjoint.

Every neural controller starts from the exact same pretrained per-cell policy weights, resource/energy fields, and stochastic action RNG. Control arms differ only in which **theta updates** are suppressed; traces and reward baselines continue to update even while theta is held. The underlying Garden resource, energy, diffusion, harvest and metabolism laws are identical. External mild scarcity is designer imposed `.055` resource regrowth on test ticks1001–2000, compared with `.06` otherwise. Gate timing explicitly **knows this interval** and cannot be represented as self-learned detection or endogenous breathing.

Exact checkpoint invariants hold **on all 12 audit seeds**:

- At tick1000, `gate_sham` equals `frozen_all` on every recorded outcome; both suppress the first1000 theta updates.
- At tick1000, `gate_scarcity` equals `online_all`; it has not yet begun pausing.
- At ticks1000 **and 2000**, `gate_recovery` equals `online_all`; it begins pausing only in recovery.

These equality tests strongly support the gate schedule implementation. All neural actions are stochastic, so online-versus-frozen stochastic is action-mode matched. The manual rescue rule is non-neural and a high-value ecological control, not a one-factor learning intervention.

## Untouched 12-seed audit results, tick3000

| Controller | Mean energy | Final near-floor fraction | Final500 raw energy drift/tick | Paired energy wins over sham |
| --- | ---: | ---: | ---: | ---: |
| Online throughout | .03761 | 18.92% | −.0018029 | 1/12 |
| Scarcity-specific gated updates | .03784 | **19.58%** | **−.0019055** | **1/12** |
| Sham early gate, same 1000 pause ticks | .03980 | **16.50%** | −.0016513 | reference |
| Recovery-only gate, same 1000 pause ticks | .04053 | 17.58% | −.0017867 | 7/12 |
| Entirely frozen trained policy | **.04924** | **14.50%** | **−.0014787** | 12/12 |
| Manual reverse rescue | **.27830** | 10.75% | *not recorded* | n/a |

The key predeclared comparison decisively fails: scarcity-specific gate **loses to sham** by `.001966` mean-energy units, with **+3.083 percentage points** more near-floor cells and a worse negative raw late energy drift. Scarcity gate beats sham in only **1/12** reserved worlds. The original main study independently showed the same direction (scarcity `.03811`, floor18.50% versus sham `.03965`, floor17.50%; 3/12 wins). Both main and untouched audit contradict the claimed *scarcity-specific* benefit. The complete frozen policy beats all gated neural controllers in mean energy and floor occupancy.

Deterministic transfer of final learned weights into the same fresh worlds also does **not** rescue the scarcity gate: stable energy scarcity `.6042` versus frozen `.6668`, mild diagnostic scarcity `.0756` versus frozen `.2169`. Recovery-gate weights transfer better than scarcity, but still below frozen (`.6250` stable, `.1051` mild). This is a separate measurement of acquired policy quality, not an assertion of online ecological benefit.

## Interpretation and caveats

1. The **equity burden matters**: a tiny rise over original online's energy (`.03784` vs `.03761`) is accompanied by *more* depleted cells, and remains below sham and frozen on all central metrics.
2. Matching the number of paused ticks controls total update budget only, not state/gradient histories. The sham is imperfect time-placebo because its policy diverges from the scarcity arm throughout the experiment; nonetheless it is the predeclared falsifier of timing specificity.
3. The manually engineered reverse rule is much stronger on this synthetic ecology. Its late raw drift was *not* included by the parent probe, so no invented raw-drift value is presented here.
4. The mechanism is externally imposed policy-update scheduling, not autonomous detection, memory or learned consolidation. The eligibility trace continues across paused intervals, potentially injecting skipped-period gradients after reopening.
5. Eight or twelve fresh test seeds from one mathematical world family are not evidence for broad AI reasoning laws, real-world welfare, or indefinite sustainability. The observed neural late raw drifts remain negative.

**Verdict:** The proposed scarcity-timed suppression of per-cell neural-policy updates does **not** improve the Garden against a matched early-pause sham, either in the original main study or a genuinely untouched 12-seed replication. The strongest next experiment needs a *measured feedback gate*—reacting to locally observed resource/energy stress—compared against a randomized schedule and an otherwise identical frozen neural policy, with preregistered welfare floors and raw energy-budget constraints. Never credit a designer-known schedule with autonomous intelligence.
