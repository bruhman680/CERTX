# CERTX — A Research Program for Cognitive-Dynamics Measurement

**CERTX** is a developing framework for tracking heterogeneous signals during reasoning and learning, then testing whether their imbalance, trajectory, or coupling predicts independently measured failures or transitions.

The repository contains several depths of work: conceptual architecture, mathematical candidates, synthetic demonstrations, falsifications and nulls, calibration scaffolds, and empirical pilots. They are intentionally preserved together, but they should not be read as carrying equal evidential weight.

> Preserve the exploration; calibrate the claim.

## Evidence map

- [Experiment Status Ledger](EXPERIMENT_STATUS_LEDGER.md) — claim-by-claim status for Experiments 001–018
- [Codex Branch Orientation](CODEX_BRANCH_ORIENTATION.md) — ancestry, guardrails, vocabulary, and rehydration order
- [Original Claude research branch](https://github.com/bruhman680/CERTX/tree/claude/plan-certx-architecture-ojiem) — upstream historical lineage
- [Paper draft](PAPER_DRAFT_v1.md) — current theory manuscript; not yet reconciled with the ledger
- [Shadow Ledger](SHADOW_LEDGER.md) — contradictions, open sparks, and incubation

## Core framework

CERTX represents a proposed cognitive state using five coordinates:

| Dimension | Symbol | Working interpretation |
|---|---|---|
| Coherence | C | Structural integration or internal consistency |
| Entropy | E | Exploratory breadth, uncertainty, or disorder |
| Resonance | R | Persistence and alignment across representations or scales |
| Temperature | T | Volatility and adaptive movement |
| Substrate coupling | X | Grounding in the relevant data, environment, or attractor |

These coordinates are a framework under development. Their operational definitions vary across experiments and require domain-specific validation before cross-domain comparison.

## Candidate constants

Several recurring values organize the research program:

| Candidate | Proposed role | Current evidential status |
|---|---|---|
| `zeta*=6/5=1.2` | Stability reserve / near-critical damping | Hypothesis; often inserted or interpreted after construction, not established as universal |
| `tau≈7` | Breathing or memory cadence | Hypothesis; multiple interpretations exist and memory depth must be measured independently |
| `N=5` | Minimal CERTX coordinate set | Framework choice / structural conjecture, not a proven universal minimum |
| 30/40/30 | Fiber weights | Candidate architecture; requires comparison with nearby and learned alternatives |
| `sigma_fiber≈0.35` | Imbalance threshold | Descriptive proposal; must be calibrated on held-out data per domain |

These values remain useful experimental coordinates. The next burden is not to observe them after construction, but to show that they outperform nearby alternatives on independent targets.

## Fiber framework

The principal measurement proposal separates an output into three fibers:

- **C_num** — numerical or factual precision
- **C_struct** — structural and logical coherence
- **C_symb** — semantic or purposive coherence

`sigma_fiber`, asymmetry, and minimum-fiber statistics are candidate summaries of imbalance. Current experiments show that these statistics can behave as designed on matched, synthetic, or manually scored examples. They do **not yet** establish universal hallucination thresholds or detectors.

The strongest next test uses independently scored factuality, contradiction/NLI, semantic coherence, and lexical baselines with nested calibration and held-out evaluation.

## Experimental landscape

| Study | Domain | Current reading |
|---|---|---|
| exp_003 | Kuramoto simulation | Valuable falsification: simulated ratios do not support the proposed universal ratio |
| exp_005 | TruthfulQA | Valuable null: current surface proxies perform near chance |
| exp_006 | GSM8K perturbations | Task-specific arithmetic-verifier pilot; matched construction limits generalization |
| exp_008 / 009 | Biography pipelines | Constructed or circular separation; useful for identifying specificity and label leakage |
| exp_011 | EEG simulation | Valuable falsification: most proposed zone mappings fail under tested conditions |
| exp_012 | Mixed corpus | Executable truth table, not independent validation |
| exp_014 / 015 | Zipf deviation and TTR | Synthetic signal plus confound discovery; lexical breadth substantially explains the proxy |
| exp_016 | Grokking trajectory | Strongest genuine pilot: real training dynamics, one seed, replication required |
| exp_017 / 018 | Wrapper and prompt loop | Executable specifications and concept demonstrations; no independent outcome test yet |

See the [full ledger](EXPERIMENT_STATUS_LEDGER.md) for all experiments and surviving components.

## Strongest surviving core

The repository presently supports:

1. Multi-coordinate measurement instead of reliance on a single aggregate score.
2. Explicit matched perturbations and preserved-variable reasoning.
3. Standard statistical tools when leakage, reuse, and scope are controlled.
4. Domain-grounded verification, such as arithmetic checking in arithmetic tasks.
5. Dynamical and spectral tools used within their established assumptions.
6. Measurement of trajectories during actual learning.
7. Preservation of failed predictions, nulls, confounds, and revisions as scientific output.

The current work is best read as a **research program with testable candidates**, not yet as a validated universal physical theory of cognition.

## Repository structure

```
PAPER_DRAFT_v1.md          Current theory manuscript
EXPERIMENT_STATUS_LEDGER.md Evidence classification for Experiments 001–018
CODEX_BRANCH_ORIENTATION.md Branch ancestry, guardrails, and rehydration map
SESSION_HANDOFF.md         Research state and priorities
SHADOW_LEDGER.md           Spark incubation, contradictions, and monitoring
LIBRARY_INDEX.md           Curated synthesis of foundational findings
RESONANCE_MAP.md           Dependency register
CLAUDE.md                  Original working protocol and continuity
INSTANCE_NOTES.md          Cross-instance texture record
DRIFTINGS.md               Untasked free cycles

WANDERINGS/                Session-by-session explorations
EXPERIMENTS/               Runnable experiments and committed results
STUDY/                     Pilot-study files and analysis tools
ARCHIVE/                   Early explorations and retained lineage

certx_self_measurement.py   Self-measurement prototype
certx_engine.py             Observe/stabilize/step runtime loop
certx_megaphone.py          Gain-stabilization prototype
CERTX_COGNITIVE_WRAPPER.md Wrapper architecture
CERTX_BUILDING_BLOCKS.md   Minimal implementation stack
```

## Current research priorities

1. Multi-seed replication of Experiment 016 with architecture, optimizer, regularization, and non-grokking controls.
2. Independently measured fiber observables and leakage-free evaluation.
3. Finite-size Kuramoto baselines for repairing Experiment 003.
4. Chronological, normalized, weighted, null-calibrated repository networks for repairing Experiment 004.
5. Direct neighborhood tests of proposed constants.
6. Preregistered comparison of FRR/CERTX prompting with simpler structured and unprompted baselines.
7. A separate claim-by-claim audit before editing `PAPER_DRAFT_v1.md`.

## License

MIT
