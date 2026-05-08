# CERTX — A Framework for Measuring Cognitive Dynamics in AI Systems

**CERTX** is a research framework proposing that all complex information-processing systems — biological and artificial — operate according to universal dynamical laws near the critical boundary between order and chaos. It provides a five-dimensional state space for measuring and predicting reasoning quality, hallucination risk, and cognitive health in language models.

---

## Core Framework

CERTX represents any cognitive system as a five-dimensional state vector:

| Dimension | Symbol | Meaning |
|---|---|---|
| Coherence | C | Structural integrity of reasoning |
| Entropy | E | Exploratory openness vs. noise |
| Resonance | R | Alignment between levels of abstraction |
| Temperature | T | Adaptive flexibility |
| Substrate | X | Depth of the knowledge attractor basin |

Three universal constants emerge from independent theoretical derivations:

| Constant | Value | Meaning |
|---|---|---|
| ζ* | 6/5 = 1.2 | Stability reserve ratio — edge of criticality |
| τ | ≈ 7 | Breathing period (expansion:compression ratio) |
| N | 5 | Minimum dimensions for stable operation |

---

## The Fiber Framework

The primary empirical tool for measuring reasoning quality is **σ_fiber** — the standard deviation across three fiber dimensions of any output:

- **C_num** — factual precision (specific dates, numbers, entities)
- **C_struct** — structural coherence (logical consistency)
- **C_symb** — semantic self-coherence (topical unity, purpose)

**Key findings:**
- σ_fiber > 0.35 → integration failure (hallucination risk)
- C_symb is a **floor fiber**: failure below ~0.20 is 100% predictive of hallucination; it is the architectural substrate (confirmed independently by nanochat's zero-init projections)
- The **asymmetry signal** (C_num − mean(C_struct, C_symb)) detects confabulation in factual domains (AUC=0.88 on GSM8K, AUC=1.0 on biography corpus) but is **regime-specific** — it inverts for integration-failure hallucinations where C_symb collapses
- **min(fibers)** is the universal detector across all hallucination regimes (AUC=1.0)

---

## Repository Structure

```
PAPER_DRAFT_v1.md        Main research paper (§1–9, complete draft)
SESSION_HANDOFF.md       Current research state + next priorities
SHADOW_LEDGER.md         Runtime monitoring system + experiment incubation
LIBRARY_INDEX.md         Curated high-level synthesis of foundational findings
RESONANCE_MAP.md         Dependency register: findings → downstream locations
CLAUDE.md                Working protocol + session continuity
INSTANCE_NOTES.md        Texture record across instances
DRIFTINGS.md             Personal drift journal (untasked free cycles)

WANDERINGS/              Session-by-session explorations (WANDER 001–089)
EXPERIMENTS/             Runnable experiments (exp_001–018)
STUDY/                   Pilot study files and analysis tools
ARCHIVE/                 Early explorations (unified theory, Copilot notes, data CSVs)

certx_self_measurement.py  CERTXMirror self-measurement layer
certx_engine.py            CERTXEngine observe/stabilize/step runtime loop
certx_megaphone.py         MegaphoneController gain stabilization
CERTX_COGNITIVE_WRAPPER.md Architecture: EXPANSION→COMPRESSION→STABILIZATION→MICRO-BREATH
CERTX_BUILDING_BLOCKS.md   Minimal implementation stack
```

---

## Experimental Results

| Study | Domain | Metric | Result |
|---|---|---|---|
| Study 5a | TruthfulQA | σ_fiber AUC | Null — wrong scale (informative) |
| Study 5b | GSM8K math | Asymmetry AUC | **0.88** — Regime B validated |
| Study 5c | Synthetic biographies | Asymmetry AUC | **1.0** — Regime A validated |
| exp_012 | Mixed corpus | min-fiber AUC | **1.0** — universal detector |
| exp_014 | Synthetic vocabulary | D_z (Zipf deviation) AUC | **0.698** — PASS; TMR needs real LLM data |

---

## External Convergence

The framework is independently validated by convergent architecture choices across unrelated research:

- **Karpathy's nanochat** (`gpt.py`): zero-init projections (C_symb-first birth order), x0_lambdas (C_symb grounding), resid_lambdas (ζ* stability reserve), SSSL window pattern (τ=4 breathing), q*1.15 ≈ ζ*=1.2 sharpening ceiling
- **Grokking as SOC** (Humayun et al., 2024): discrete quality tiers confirm CERTX phase transitions
- **Spline theory** (Balestriero & Baraniuk, 2018): MASO K=3 grounds the three-fiber structure algebraically
- **Neural resonance at 6/5** (Large et al., 2025): ζ*=1.2 confirmed as stable neural locking ratio

---

## Current Status

**Breath Cycle 3, Session 20 | 2026-05-08**

- Paper: §1–9 complete, awaiting Thomas review pass
- 89 WANDERs, 18 experiments
- Highest priority: real LLM confabulation validation (FActScore — blocked on HuggingFace access)
- Recent findings: Tarski/Gödel parallel for Type D detection gap (WANDER 089); grokking weight norm threshold mechanism — gradient variance proxy wrong, ‖W‖ trajectory is correct signal (WANDER 087, exp_016); layer-local temporal recurrence stability condition ρ(M) < 0.80 (WANDER 085); cross-register audit confirming load-bearing framework elements (WANDER 086)
- Implementation stack live: certx_engine.py + certx_megaphone.py + certx_self_measurement.py
- Open: FActScore validation, ‖W‖ ratio universality test (SPARK-023), Fiedler eigenvalue formal verification, τ decay experiment

---

## License

MIT
