# Neural Garden v0.1 — operator guide

**Scope:** Standalone CPU simulation. Runs are bounded and repeatable; no daemon, cloud hosting, autonomous background monitor, or permanent infrastructure is implied. The original frozen CERTX Garden is separate and must not be modified.

## Quick start

From the `NEURAL_GARDEN_V01/` directory, with Python and NumPy installed:

```bash
python run_garden.py init --directory runs/first --seed 7 --size 16
python run_garden.py run --directory runs/first --steps 250 --checkpoint-every 10 --snapshot-every 10 --report-every 50
python run_garden.py status --directory runs/first
python run_garden.py inspect --directory runs/first --tail 5
```

To request a pause while another terminal is running the bounded loop:

```bash
python run_garden.py pause --directory runs/first
```

The running process notices `PAUSE_REQUESTED` at the next step boundary, writes a final checkpoint and snapshot, then stops. Sending Ctrl+C or SIGTERM similarly requests a graceful stop after the current step. A Python interpreter killed without handler execution (SIGKILL, power loss, hardware failure) may leave work after the last successful checkpoint unrecoverable.

To resume from the last durable checkpoint:

```bash
python run_garden.py resume --directory runs/first --steps 250 --checkpoint-every 10 --snapshot-every 10
```

`resume` clears the explicit pause marker. Both `run` and `resume` have finite step budgets (default 100); they do **not** create an unattended always-on service. Repeat deliberately authorized chunks or use an external supervisor only after explicitly choosing its scope and persistence guarantees.

## Independent control

Create a separate run with the same seed, dimensions, and environment but with online neural learning disabled:

```bash
python run_garden.py init --directory runs/no_learning --seed 7 --size 16 --no-learning
python run_garden.py run --directory runs/no_learning --steps 250
```

Compare trajectories and predictions rather than treating raw activity or survival as evidence of learning. Different intervention arms may diverge in their world state; matched seeds alone do not guarantee matched observations after divergence.

## Files

| Path | Purpose |
| --- | --- |
| `state.pkl` | Engine checkpoint including neural weights, cell/environment state, and RNG. Binary pickle: **only load checkpoints you created and trust**. |
| `manifest.json` | Run provenance, intended seed/size/learning, durable step count, and checkpoint time. |
| `metrics.jsonl` | Append-only step and operator events; one JSON record per line. |
| `snapshot.json` | Latest JSON-serializable world snapshot for a viewer. |
| `snapshots/step_XXXXXXXX.json` | Periodic snapshots for manual replay or visualization. |
| `PAUSE_REQUESTED` | Operator's cooperative pause request. |
| `RUNNING.lock` | Exclusive-writer lock during `run`/`resume`; prevents accidental concurrent writers. |

Use `python run_garden.py snapshot --directory runs/first` to export the current checkpoint state without advancing it.

The file `snapshot.json` has `{ "completed_steps": N, "garden": <Garden.snapshot()> }`; the per-tick files use the same shape.

## Reproducibility and recovery boundaries

- Smoke verification (2026-11-11 UTC): seed 11, size 8; a 12-step run plus cooperative pause and a three-step resume produced the **exact same** `snapshot.json` SHA-256 as a separate uninterrupted 15-step run (`918bb4fa41a9119d58f764695d5929d97bfd3c2762a6d88634778f4ab5184c66`). That SHA comparison covers **visible snapshot fields only**, not neural weights, hidden states, or RNG. The separate full-state `Garden.fingerprint()` and load/continuation checks verify those components; more seeds and long-horizon checkpoint tests remain useful.
- Fixed seed and identical sequence of actions and parameters should reproduce the same engine trajectory. The engine checkpoint must include the exact PRNG state; test this against a never-paused run.
- Checkpoints are written to a temporary file then atomically renamed. A manifest is written separately; if a crash occurs between those operations, the CLI can reconcile a **newer** engine tick with the manifest on the next run and records the event. A manifest ahead of the checkpoint is treated as an error requiring manual audit.
- Metrics are written per step while checkpoints are periodic. A hard crash may leave log records ahead of the restored checkpoint. The CLI preserves those records and adds a `checkpoint_recovery` event if it must replay steps, instead of silently deleting history. Downstream analysis must use the latest valid run segment, not count repeated step numbers twice.
- A stale `RUNNING.lock` after a hard crash stops further writes. Inspect the process and files before manually removing that specific lock. Do not automatically override it.
- A pause is **not** a decision by the neural agents; it is a human/operator control external to the world.
- The workspace can be pruned or reset. Save valuable source, reports, and selected checkpoints to durable storage or GitHub. GitHub source commits alone do not preserve an active process or large binary world state.
- The current v0.1 CLI does not support live tuning mid-step. Pause, preserve a checkpoint, declare a new experimental condition, and record exactly which parameter changed before resuming or branching the run.

## Safe study protocol

1. Keep world laws fixed within a baseline run.
2. Use at least one no-learning and one shuffled/synthetic control where relevant.
3. Prefer independent seeds and declared observation windows.
4. Report prediction loss, energy/population dynamics, and stability independently; activity is not learning by itself.
5. When comparing interventions, record differing compute, information and checkpoint histories.
6. Never describe exploratory neural/cellular dynamics as conscious behavior or evidence of intelligence without task-grounded tests.
