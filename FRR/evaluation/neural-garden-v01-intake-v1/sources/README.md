# Neural Garden v0.1 — independent neural cells in a local world

**Status:** Runnable research prototype. This is a fixed-population neural ecology, **not yet an evolving organism population or self-improving ecosystem**. It is separate from the original frozen 1,550-entry Garden.

## What is implemented

- A toroidal square grid (default 16×16, 256 cells).
- Each cell owns *distinct* small recurrent neural weights, a hidden state, an energy store, and local observations. Parameters are not shared among cells.
- Fixed world rules for resource diffusion, regrowth, consumption, and energy costs.
- Simultaneous steps: observe → predict and choose harvest action → update world → local neural updates from observed consequences.
- Explicit `learning=True/False` controls, independent seeded randomness, metrics and snapshots.
- Recoverable checkpoints including neural weights, hidden activity, environment and RNG state; bounded CLI run/pause/resume/status/inspect.
- An offline, read-only HTML replay viewer for recorded snapshots.

Not implemented: births, deaths, movement, mutation/inheritance, true open-ended evolutionary selection, autonomous goal discovery, or guaranteed always-on background compute. Those are prospective separate extensions.

## Run locally

Requires Python 3.12+ and NumPy (no GPU or PyTorch needed for the engine).

From the repository root:

```bash
python NEURAL_GARDEN_V01/run_garden.py init --directory neural_garden_run --size 16 --seed 7
python NEURAL_GARDEN_V01/run_garden.py run --directory neural_garden_run --steps 200 --checkpoint-every 20 --snapshot-every 10
python NEURAL_GARDEN_V01/run_garden.py status --directory neural_garden_run
python NEURAL_GARDEN_V01/run_garden.py pause --directory neural_garden_run
python NEURAL_GARDEN_V01/run_garden.py resume --directory neural_garden_run --steps 200
python NEURAL_GARDEN_V01/viewer.py neural_garden_run --output neural_garden_replay.html
```

`run` and `resume` advance only the requested finite number of steps. `pause` is a cooperative request if a run is active; `resume` explicitly clears it. No daemon starts automatically. See [OPERATIONS.md](OPERATIONS.md) for locking, checkpoint and crash semantics.

**Security:** `state.pkl` is a Python pickle. Load only checkpoints created by your own trusted run; untrusted pickles can execute code.

## First experimental findings

Across five seeds × 200 steps, neural learning improved *on-policy* prediction MSE (~0.00388 versus ~0.01611 frozen), yet average cell energy was **lower** (~0.0178 versus ~0.0549). An independent reference-world prediction probe improved, while a separate standardized off-policy probe worsened—showing that “learning improved” is target-distribution dependent. At a fresh 600-step check, learned energy fell further. A short-sighted harvest policy can optimize an immediate feedback signal while failing long-term stewardship.

See [EVALUATION.md](EVALUATION.md) and [AUDIT.md](AUDIT.md) for actual controls and limitations. This is a scientific *negative* for sustainable improvement, not proof that the platform failed to function.

## Suggested v0.2 experiments (not implemented here)

1. Action-conditioned prediction and separate held-out forecasts.
2. Resource stewardship with long-horizon energy costs, compared with original v0.1 and a nonlearning controller.
3. Local signaling and environmental memory with selective erasure/transplant controls.
4. Reproduction, inheritance and mutation as a **separate** evolution mechanism.
5. Selection among different neural controllers; measured diversity and lineage preservation.

Preserve v0.1 results before making changes, and use untouched seeds for confirmatory tests. Relevant literature and prior art are in [RESEARCH.md](RESEARCH.md).
