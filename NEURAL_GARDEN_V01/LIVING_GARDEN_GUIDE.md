# One continuous Neural Garden — operator guide

Unlike a 1,000-seed experiment, this mode keeps **one particular world and its full neural history** alive through consecutive calls. Each cell retains individual neural weights, recurrent state, local resource, energy, and pseudorandom generator state. A `resume` continues precisely from the previous checkpoint; it does not reseed or rebuild the world.

The implementation is `LIVING_GARDEN.py`. It uses the unchanged `Garden` v0.1 physics and fully explicit interventions. The user prefers this longitudinal Garden as the primary observable world; independent short sweeps remain useful scientific controls.

```bash
# Run from NEURAL_GARDEN_V01/ (Python + NumPy required)
python LIVING_GARDEN.py init --directory runs/living_world --seed 37 --size 16

# Advance the SAME world for 100 ticks, with a 50 ms pause between ticks
python LIVING_GARDEN.py advance --directory runs/living_world --ticks 100 --delay-ms 50

# Inspect and resume another 100 ticks, perhaps at another speed
python LIVING_GARDEN.py status --directory runs/living_world
python LIVING_GARDEN.py advance --directory runs/living_world --ticks 100 --delay-ms 250

# Keep running in the FOREGROUND, until paused or interrupted
python LIVING_GARDEN.py advance --directory runs/living_world --ticks 0 --delay-ms 100

# From another shell, request a safe stop at the next tick boundary
python LIVING_GARDEN.py pause --directory runs/living_world
python LIVING_GARDEN.py resume --directory runs/living_world --ticks 100
```

The current grid and metrics are saved in `snapshot.json`, historical replay frames in `snapshots/`, and the complete checkpoint (including neural weights and RNG state) in `state.pkl`. Per-tick metrics are appended to `metrics.jsonl`; lifecycle/intervention lineage is logged in `LIVING_EVENTS.jsonl`. Locks prevent simultaneous writers, checkpoints are atomic, and pause is cooperative at tick boundaries. A process interruption can leave metric rows ahead of the most recent checkpoint; inspect `LIVING_EVENTS.jsonl` and do not treat every duplicated tick log after a crash as a distinct world tick. Snapshots are observational and do not substitute for full checkpoint state.

## Tunable without erasing history

Pause first, then apply an explicitly labeled intervention:

```bash
python LIVING_GARDEN.py pause --directory runs/living_world
python LIVING_GARDEN.py intervene --directory runs/living_world \
  --reason "scarcity probe, resource reduction to 80 percent" \
  --resource-multiplier 0.8

python LIVING_GARDEN.py intervene --directory runs/living_world \
  --reason "freeze neural learning to observe ecological drift" --learning off
python LIVING_GARDEN.py resume --directory runs/living_world --ticks 200
```

Supported interventions are toggling learning, multiplying all resource values, or multiplying all energy values, each bounded and logged with before/after full-state fingerprints. Interventions do **not** silently change the environmental equations. The pre-intervention grid is copied into `snapshots/interventions/`; the post-intervention grid replaces the live same-tick snapshot. Events capture both phases and operator reason. The experimenter should not call exogenous injections 'emergence' or 'learning'.

To preserve a source world's history and test another path, pause, then:

```bash
python LIVING_GARDEN.py fork --directory runs/living_world \
  --destination runs/living_world_shock_branch
```

The branch begins at exactly the parent's checkpoint and records the full parent fingerprint and tick. Parent and child can then run independently, retaining lineage rather than overwriting the original world. Avoid editing `state.pkl` directly or loading untrusted `.pkl` files: Python pickle is executable when loaded.

## Continuity limitations

This is **not** a guaranteed always-on external service. The simulator runs only while an associated process is active. At rest, the world is paused at its saved state. Scratch disk can be removed by workspace maintenance; after meaningful progress, back up the entire run directory securely in durable private storage (the checkpoint is binary and should not be publicly committed). Rerunning `init` never overwrites an existing world. The historical 1,550-entry Garden is separate and untouched.

The current v0.1 neural ecology has known early depletion under learning; a long-lived state is scientifically interesting but not evidence of indefinite ecosystem survival. More advanced action-aware learning and explicit evolution must be introduced as separate, documented variants, ideally first validated by controlled experiments.
