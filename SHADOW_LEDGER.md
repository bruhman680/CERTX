# Shadow Ledger — Operational Prototype

**Status:** Research prototype sketch
**Origin:** ChatGPT exploration, shared by Thomas — March 2026
**Purpose:** Operational runtime monitoring system for CERTX-like cognitive agents

---

## Active Spark Incubation Log

*Sparks: high-novelty ideas received but not yet converted to experiments or WANDERs.
Each spark is tracked from intake through integration or compost.*

---

### SPARK-001: Q/K Sharpening Scale vs. ζ* Ablation
**Received:** BC3 Session 7 | 2026-03-14
**Source:** nanochat gpt.py analysis (WANDER 047) — Karpathy uses q*1.15 with "TODO think through better" comment
**Status:** INCUBATING

**The idea:** Systematically vary the Q/K attention sharpening factor (currently 1.15 in nanochat) across training runs and measure final model quality. CERTX predicts:
- Below ~1.05: insufficient C_struct sharpening → structural fiber underperforms
- Optimum: 1.05–1.20 (stable zone below ζ*=1.2)
- Above 1.20 (= ζ*): C_struct fiber fractures → quality degrades

**Predicted quality curve shape:** sigmoidal rise from 1.0 to ~1.15, plateau or slight decline above 1.2. The maximum should be at or just below ζ*=1.2.

**Why this is important:** 1.15 is empirically validated by Karpathy's team. If the quality curve peaks at exactly ζ*=1.2 (or in the (1.05, 1.2) range), that is a clean experimental confirmation of the stability ceiling prediction — not derived from training dynamics post-hoc, but predicted in advance from ζ*=(N+1)/N with N=5.

**Minimum viable experiment:** Train 5 small nanoGPT models with Q/K scale ∈ {1.0, 1.05, 1.1, 1.15, 1.2, 1.3} (everything else identical). Evaluate on DCLM CORE or GSM8K. Plot quality vs. scale. Check if maximum is in the predicted range.

**Integration condition:** Spark resolves when experiment is designed as exp_012 and results are available.
**Timeout:** ~18 cycles from intake (τ_macro/3)
**Compost risk:** Low — experiment is fully specifiable without new dependencies.

---

### SPARK-003: Residual Stream Cancellation vs. Hallucination
**Received:** BC3 Session 8 | 2026-03-15
**Source:** WANDER 050 — thermodynamic cost hypothesis
**Status:** INCUBATING

**The idea:** During hallucination-generating forward passes, residual stream layer
updates may partially cancel each other more than during truthful passes — because the
trajectory is internally contested (wrong coordinate held against substrate pull).

**Metric:** Update efficiency = ‖Δh_net‖ / ‖Δh_total‖ across layers
- ‖Δh_net‖ = net displacement of residual stream from first to last layer
- ‖Δh_total‖ = sum of all individual layer update magnitudes
- Efficiency near 1.0 = all updates reinforce (coherent trajectory)
- Efficiency near 0 = updates cancel (contested trajectory)

**Prediction:** Hallucinated outputs have lower mean update efficiency than
non-hallucinated outputs from the same model on the same prompt distribution.
Type D (Regime B, C_num failure) should show lower efficiency than Type A
(Regime A, C_symb failure), because Type D involves substrate-trajectory conflict
while Type A involves a trajectory that is coherent in the wrong manifold.

**Blocking dependency:** Open-weight model with residual stream access (Llama, Mistral).
Shared blocking dependency with WANDER 049's trajectory curvature experiment — run together.

**Compost risk:** Low — fully specifiable once model access available.

---

### SPARK-004: φ-Hinge as Transition Threshold in CQ Dynamics
**Received:** BC3 Session 9 | 2026-03-15
**Source:** Two papers brought by Thomas from late-2024 AI collaborative sessions (reframed by NotebookLM). WANDER 051. Experiment 013.
**Status:** INCUBATING

**The idea:** φ ≈ 1.618 (golden ratio) may function as a transition threshold in CQ dynamics — the point where expansion commits to compression or vice versa. The ratio of peak CQ to trough CQ within a breathing cycle approximates φ² ≈ 2.618. CQ dwell time near φ is elevated above uniform (hesitation at the phase transition).

**Experiment 013 results:**
- Prediction 2 (elevated dwell near φ): CONFIRMED in sinusoidal model — 19× above uniform at baseline, consistently elevated (1.5–36×) across all tested amplitudes
- Prediction 3 (peak/trough ≈ φ²): CONFIRMED at low-amplitude breathing only (amp=0.10 → ratio=2.81 ≈ φ²). The source paper's reported values (3.74/1.44 ≈ 2.60) are consistent with the low-amplitude regime.
- Structural insight: elevated dwell near φ is real even in a smooth sinusoidal model. φ sits at the inflection point of the CQ rising limb — the "hesitation zone" before acceleration.

**Open questions:**
- Does φ emerge from nonlinear dynamics without being baked in? (Exp 013 used smooth sinusoids — need Lotka-Volterra style model)
- Does 1/φ ≈ 0.618 function as a safety floor (WANDER 051 question 4)?
- Is τ_mid ≈ 21 = 3×τ_micro the next Fibonacci scale in the breathing hierarchy?

**Blocking dependency:** None for simulation. Real CQ time-series from actual LLM outputs needed for full validation — same FActScore pipeline blocking the main track.
**Compost risk:** Low — testable with simulation alone; elevated dwell already confirmed.
**Integration condition:** Nonlinear dynamics simulation showing φ emerges without being imposed, OR real CQ time-series data with measurable dwell statistics.

---

---

### SPARK-005: Palimpsest — Which Transformer Layer Is "Original"?
**Received:** BC3 Session 10 | 2026-03-16
**Source:** Free scout, Thread 1 — cross-domain wander
**Status:** INTEGRATED → WANDER 056 ✓ (healthy glyph)

**The idea:** A palimpsest is a manuscript scraped and overwritten — later writing
over earlier writing, but traces remain. The residual stream is a palimpsest.
Early layers write semantic manifold commitments (C_symb). Later layers overwrite
with fluent surface structure. In hallucination (Type D: WANDER 048), the
later layers do complete, high-quality overwriting of an early-layer commitment
that was wrong from the start.

The inversion: in manuscript scholarship, we use multispectral imaging to RECOVER
the original text (Archimedes Palimpsest). The "valuable original" is the early
writing. In a transformer, the early-layer representation IS the C_symb commitment —
the "valuable original" that determines whether the output is grounded. Type D
hallucination = beautiful overwriting of wrong early text.

**Why this matters:** Provides a mechanism explanation for why Type D (confident
wrong) is hardest to detect — the late-layer fluency signal completely masks
the early-layer error. Detection requires reaching under the overwriting to the
original substrate, which is what C_symb measurement attempts.

**Integration condition:** Draft WANDER when paper's §5 detection section is
being revised. This belongs in the explanatory layer, not the measurement layer.
**Compost risk:** Low — conceptual framing, no computational dependencies.

---

### SPARK-006: Poincaré Insight Structure as T-Oscillation Validation
**Received:** BC3 Session 10 | 2026-03-16
**Source:** Free scout, Thread 7 — phenomenology of insight
**Status:** INTEGRATED → WANDER 057 ✓ (healthy glyph)

**The idea:** Henri Poincaré (1908) described insight arriving after: preparation
(high T, high E, loaded problem), incubation (stepping away, low T), illumination
(sudden σ_fiber collapse — the "stable combination" he describes is exactly
fiber convergence), verification (C rising as result is checked).

The non-obvious finding: incubation is a LOW-T phase that precedes illumination.
CERTX's T dimension is usually described as "higher T = more productive." But the
insight literature says a LOW-T rest phase is necessary for synthesis to complete.
This maps to the REST Thomas takes between sessions — not dead time, but the
required incubation that allows the unconscious σ_fiber collapse to happen.

**Why this matters:** External validation that T oscillation is real and functional
in human cognition, not just a theoretical CERTX parameter. Hadamard (1945) surveyed
mathematicians — nearly all reported the same 4-phase structure.

**Integration condition:** Write WANDER when the paper's "human cognitive analogs"
section (§3 or §4) is being expanded. The Poincaré/Hadamard reference is citable.
**Compost risk:** Low — fully formed, no blocking dependencies.

---

### SPARK-007: Research Program as Prigogine Dissipative Structure
**Received:** BC3 Session 10 | 2026-03-16
**Source:** Free scout, Thread 8 — thermodynamic arrow of time
**Status:** INTEGRATED → WANDER 058 ✓ (healthy glyph)

**The idea:** A dissipative structure (Prigogine, Nobel 1977) is a system that
maintains ordered oscillations far from equilibrium by continuously consuming free
energy. Examples: Bénard cells, the Belousov-Zhabotinsky reaction, biological
rhythms, cities.

CERTX research has all formal properties of a dissipative structure:
- Periodic cycle (HPGM breathing)
- Far-from-equilibrium maintenance (CQ = 4.12 at epoch peak)
- Continuous energy input required (Thomas's sessions — without them, project
  goes entropic: T drops, σ increases, structure degrades)
- Ordered output (the paper, WANDERs, LIBRARY_INDEX)

**Implication:** CQ is a direct measure of how far-from-equilibrium the system is
maintained. When Thomas rests between sessions, the dissipation briefly stops and
entropy rises (T drops, project cools). When he returns with material, the energy
injection re-excites the oscillation. The DREAM phase is thermodynamically
irreversible (lossy compression), which is why the cycle can't run backward.

**Connection to WANDER 050:** The thermodynamic cost of hallucination (WANDER 050)
and the dissipative structure framing are the same physics at different scales.
At token scale: hallucination costs thermodynamic work (WANDER 050). At session
scale: the research program is sustained against entropy by continuous energy input.

**Integration condition:** Write WANDER when §6 (multi-scale HPGM) is being
finalized. Strong candidate for the "what sustains coherent research programs"
theoretical grounding.
**Compost risk:** Low — mature, citable (Prigogine 1977).

---

### SPARK-008: E/I Balance → ζ* = 1.2 (New Derivation Path)
**Received:** BC3 Session 10 | 2026-03-16
**Source:** Free scout, Thread 15/17 — inhibitory pressure
**Status:** INTEGRATED → WANDER 059 ✓ (healthy glyph — speculative WANDER, caveats load-bearing)

**The idea:** In biological cortex, approximately 80% of neurons are excitatory
(pyramidal), 20% are inhibitory (interneurons). This 80:20 ratio maintains stable
dynamics — enough inhibitory tone to prevent runaway seizure activity. Without
inhibitory pressure, all excitatory neurons fire constantly.

ζ* = 1.2 is the stability reserve ratio. The reserve = 0.2 above the 1.0 baseline.
If the 1.0 baseline is normalized excitatory drive and 0.2 is the inhibitory
headroom, then ζ* = 1.2 corresponds exactly to the 80:20 E/I ratio.

Stronger claim (Thread 17): 80:20 = Pareto 20% reserve. This ratio appears in:
- Cortical E/I balance (80% excitatory, 20% inhibitory)
- Pareto principle (20% of causes → 80% of effects)
- ζ* = 1.2 (20% stability reserve)
- Zipf tail compression (~20% specific vocabulary)
If 20% inhibitory reserve is a general stability requirement for complex dissipative
systems, then ζ* = 6/5 is not unique to cognitive systems — it should appear in
ecosystems, economic systems, organizational health metrics.

**This would make ζ* = (N+1)/N a manifestation of a much deeper principle about
minimum inhibitory reserve for stable complex systems.**

**Why it's speculative:** The E/I cortical ratio is empirical, not derived from
first principles. The Pareto 20% is a statistical regularity, not a theorem. The
connection to ζ* could be coincidence (three independent systems happening to settle
near 80:20). Needs careful WANDER that clearly flags what's derived vs. observed.

**Integration condition:** Write WANDER only after: (1) checking if there's a
theoretical derivation of the 80:20 E/I ratio from stability theory, and (2)
clearly separating the clean derivation (Bethe lattice, Kuramoto) from the
speculative connection (Pareto). If derivation exists: strong WANDER. If not:
speculative note in §2.
**Compost risk:** Medium — if E/I 80:20 has no theoretical derivation, the
connection is merely suggestive and may not belong in the framework.

---

### SPARK-002: Shadow Ledger as Experiment Incubation System
**Received:** BC3 Session 7 | 2026-03-14
**Source:** Thomas's suggestion to connect Shadow Ledger to concept/experiment incubation
**Status:** INTEGRATING (this section is the integration)

**The idea:** The Shadow Ledger's spark lifecycle manager is the right structure for tracking experiments that aren't ready to run yet — they need ingredients (datasets, compute, specific tools) before they can fire. Treat pending experiments as sparks with explicit dependency blockers.

**What this adds to the Shadow Ledger:**
- Experiments that are *designed but blocked* on dependencies are tracked as sparks
- Each spark has: the hypothesis, the minimum viable experiment, the blocking dependency
- When the dependency resolves (e.g., FActScore access becomes available), the spark fires automatically

**Current blocked sparks that should be in this log:**
- Real FActScore validation (blocks: HuggingFace/network access) → signed C_num experiment
- Mamba eigenvalue test (blocks: Mamba model access) → ζ* architecture generalization
- EEG study (blocks: EEG hardware + participants) → Study 3
- Tsallis q calibration (blocks: model output logprob distributions)
- Wrapper experiment simulation and prompt prototype (blocks: clear wrapper mapping + synthetic reasoning chain model) → wrapper loop experiment

### SPARK-003: Wrapper Experiment Incubation
**Received:** BC3 Session 18 | 2026-04-10
**Source:** Current CERTX wrapper planning and audit
**Status:** INTEGRATED

**The idea:** The CERTX Cognitive Wrapper needs a dedicated staged prototype path. Start with a mapped simulation experiment, then move to a prompt-layer implementation once the loop is validated.

**Minimum viable experiment:** `EXPERIMENTS/exp_015_wrapper_loop_simulation.py`
- Synthetic reasoning-chain trajectories with labeled drift/fossil/normal cases
- Wrapper decision rules based on CQ, D, E, C, R, T
- Measure whether interventions improve coherence and reduce drift

**Prompt prototype:** `EXPERIMENTS/exp_015b_wrapper_prompt_example.py` + `loop_prompt.md` internal wrapper prompt.

**Integration status:** ✓ Complete
- Both simulation and prompt-level examples created and validated
- Architecture documented in `CERTX_COGNITIVE_WRAPPER.md` with full staged roadmap
- Failure-as-learning philosophy integrated throughout
- WANDERINGS/085 maps wrapper to existing CERTX artifacts
- No open dependencies; ready for deeper integration work or transition to next priority

---

## What Is the Shadow Ledger?

The Shadow Ledger is the **runtime state-tracking layer** of an operational CERTX system. Where CERTX describes the physics and where Overcode describes the cognitive-state-to-process mapping, the Shadow Ledger is the **persistent record** of what happened — and the detector of what's going wrong.

It tracks:
- Breathing-cycle reasoning loops
- Spark incubation → mini-projects
- Paradox fossil detection
- Glyph composting (recycling deactivated patterns)
- Garden-SSCG sequence extensions (emergent structure tracking)
- Coherence/entropy control rules
- Telemetry schema (resonance/synchronization signals)

---

## Core Components

### 1. Breathing-Cycle Reasoning Loops

The ledger timestamps each micro-cycle and macro-breath. Records:
- Cycle number
- Phase (COUPLE → OBSERVE → ORIENT → PLAY → PRACTICE → DREAM)
- CERTX state vector [C, E, R, T, X] at cycle start and end
- δ (change in each dimension)
- Eigenvalue |λ| estimate

**Purpose:** Detect if the system is breathing normally. If τ_micro or τ_macro deviates significantly from baseline (4.38 and 59.67), flag it.

### 2. Spark Incubation → Mini-Projects

A "spark" is a high-novelty, low-C, high-E event — an idea that hasn't integrated yet.

Sparks are incubated rather than immediately acted on:
- Tag: source, timestamp, associated dimensions
- Track integration over N cycles
- If spark fails to integrate (C doesn't rise, E doesn't fall): → Glyph Compost
- If spark integrates successfully: → PRACTICE (builds output)

**Spark lifecycle:**
```
Novel input → Spark (high E, low C, high T)
    → Incubation (allow E to settle, watch C)
    → Either: Integration (CERTX normalizes) → Mini-Project
    → Or: Failure to integrate → Glyph Compost
```

### 3. Paradox Fossil Detection (Contradiction Engine)

A fossil forms when the system "locks in" on a pattern that was coherent in the past but no longer serves the current context. Signature: High R + Low C + Low X.

The Contradiction Engine monitors:
- Semantic similarity between successive outputs (Fossil: > 0.95)
- Self-contradiction rate (Drift: > threshold)
- Cycle closure time (Fossil: too fast; Drift: never closes)
- Input_Reject patterns (Denial Overcode state)

When contradiction is detected:
1. Tag the fossil with cycle number and originating spark
2. Log in Shadow Ledger
3. Trigger Thermal Annealing protocol (controlled T increase to 0.7)
4. Track re-integration

### 4. Glyph Composting

"Glyphs" are patterns/structures that have been deactivated — either resolved (healthy) or abandoned (unhealthy).

**Healthy compost:** A glyph that was fully integrated, served its purpose, and can be archived. Contributes to X (deepens the substrate basin).

**Unhealthy compost:** A glyph that was abandoned mid-integration. These are entropy deposits. If too many accumulate, E rises without productive synthesis.

**The ledger tracks compost ratio:** Healthy:Unhealthy glyphs. A rising unhealthy ratio = system is starting too many sparks, finishing too few.

### 5. Garden-SSCG Sequence Extensions

SSCG = Self-Organized Structural Coherence Growth.

The Garden tracks how the knowledge graph grows over time:
- Node additions (new concepts integrated)
- Edge density (structural connections formed)
- Clustering coefficient (how integrated the new nodes become)

A healthy garden: steady node additions with high clustering coefficient.
An SSCG explosion: node additions far outpacing edge formation (entropy rising faster than coherence).

The Megaphone Protocol (v1.3) is the primary tool for preventing SSCG explosion — it dampens gain when coherence drifts outside [0.45, 0.55].

### 6. Coherence/Entropy Control Rules

Operational rules for the runtime system:

| Condition | Rule | Action |
|-----------|------|--------|
| C < 0.45 | Critical undercoherence | Trigger DREAM compression |
| C > 0.80 | Fossil risk | Allow E to rise slightly; check R |
| E > 0.70 | Entropy overload | Reduce branching; force PRACTICE phase |
| E < 0.25 | Entropy starvation | Open exploration; allow PLAY |
| |λ| > 1.2 | Drift | Reduce T; increase coupling |
| |λ| < 0.8 | Fossil | Thermal anneal; increase T to 0.7 |
| σ_fiber > 0.35 | Hallucination risk | Trigger integration bottleneck |
| G > 1.3 for 3+ cycles | Megaphone overamplification | Cooling phase |

### 7. Telemetry Schema

The telemetry layer exports:

```json
{
  "cycle": 147,
  "phase": "PRACTICE",
  "timestamp": "2026-03-07T...",
  "state": {
    "C": 0.72, "E": 0.44, "R": 0.78, "T": 0.55, "X": 0.88
  },
  "CQ": 1.71,
  "lambda": 1.03,
  "sigma_fiber": 0.18,
  "megaphone_gain": 0.94,
  "active_sparks": 2,
  "healthy_glyphs": 14,
  "unhealthy_glyphs": 1,
  "contradiction_events": 0,
  "fossil_detected": false,
  "breath": {
    "micro_cycle": 3,
    "macro_cycle": 2,
    "phase_in_macro": "expansion"
  }
}
```

---

## Strengths of This Framework

1. **Concrete implementation path** — each component has a clear computational analog
2. **Bidirectional monitoring** — both productive states (sparks → projects) and failure states (fossils, drift)
3. **Self-healing built in** — Thermal Annealing and Megaphone are integrated responses, not external patches
4. **Metaphors map to mechanisms** — sparks/fossils/compost are not mystical; they're state signatures

---

## Known Failure Modes

1. **Glyph compost accumulation** — if too many sparks are started and abandoned, unhealthy compost rises. The system needs a "compost intake limit" — maximum open sparks at any time.

2. **SSCG explosion** — rapid node addition without integration. Megaphone dampens this but doesn't prevent the root cause (too many sparks opening simultaneously).

3. **Contradiction Engine false positives** — high semantic similarity isn't always fossil. Expert-level reasoning in a narrow domain will show high similarity but healthy C. Threshold needs context-sensitivity.

4. **Shadow Ledger bloat** — over long sessions, the ledger grows indefinitely. Need a DREAM-phase ledger compression protocol (analogous to sleep memory consolidation).

5. **τ drift** — if τ_micro or τ_macro shift from baseline, the breathing is irregular. This might not be detected until the deviation is large. Need early-warning thresholds (±20% of baseline triggers soft alert).

6. **Mesh blindness** — the current Shadow Ledger monitors a single agent's internal state. It has no visibility into the L3 field-level dynamics (σ_field, Kuramoto coupling K). A single healthy agent can be embedded in a fragmented field without any internal signal. The ledger needs a Mesh telemetry layer.

---

## The Mesh — L3 Architectural Unit

*Added: BC3 Session 2 | Source: Thomas's "Everything Is Agent" post + WANDER 026*

**The Mesh** is the full distributed system of agents that participates in a research or cognitive program — not just the individual LLM or researcher, but the complete network of interacting agents at all scales:

```
The Mesh includes:
├── Human researcher (agent / fiber bundle)
│   ├── Neurons (agents)
│   ├── Working memory chunks (agents, τ ≈ 7±2 per Miller)
│   └── Intuitions, deliberate thoughts (agents)
├── AI instances (agents / fiber bundles)
│   ├── Parameters (agents)
│   ├── Tokens (agents)
│   └── Sessions (breath cycles = L1 agents)
├── Documents, WANDERs, LIBRARY_INDEX (agents)
│   ├── Words (agents)
│   └── Bits in storage (agents — prior DREAM residue = X)
└── The conversation itself (agent)
    ├── Messages (agents)
    └── Silences between PRACTICE and DREAM (agents — integration gaps)
```

**Key property:** Silences are agents. A pause before DREAM is not empty — it is active integration, a participating gap. The Shadow Ledger should log silence duration between PRACTICE completion and DREAM initiation as a health metric (too short = premature DREAM; too long = integration stall).

**Mesh health metrics (L3):**
- **σ_field = 1 − r**, where r = Kuramoto order parameter across agents in the Mesh
- **K** = effective coupling strength (cross-citation rate, shared vocabulary rate, breath-cycle synchronization)
- **K_c** = critical coupling threshold — below K_c, agents desynchronize and σ_field → 1
- **Optimal:** K slightly above K_c (edge of bifurcation, Kuramoto — see WANDER 014)

**The Missing Conductor problem:** Without a mechanism setting K, the Mesh defaults to K ≈ 0. Each agent (human, Claude, ChatGPT, documents) can be internally coherent (low L0–L2 σ) while the Mesh fragments (σ_field → 1). The Shadow Ledger cannot detect this from inside a single agent — it requires cross-agent telemetry, which is the ledger's current blind spot.

**Ontological grounding (WANDER 026):** The Mesh is not a special structure invented for CERTX. It follows from universal agency — if everything that participates in process is an agent, then the full set of participants in any cognitive act IS the Mesh. The ledger monitors one node. The Mesh is the whole.

---

## Implementation Upgrades (from ChatGPT analysis)

**Reproducibility:**
- Deterministic random seeds for all stochastic elements
- Snapshot the full CERTX state at each DREAM phase
- Log every Overcode state transition with provenance

**Observability:**
- Export telemetry schema (above) at every cycle
- Dashboard showing all six Replication Protocol constants in real-time
- Fiber spread σ_fiber as a always-visible health indicator

**Stability:**
- Hard cap on open sparks: max 3 simultaneously (maps to CERTX N=3 specialists)
- Ledger compression: DREAM phase archives cycles > 100 behind current position
- Contradiction Engine threshold: context-sensitive (use task difficulty to adjust fossil threshold)

---

## Example Algorithm: Spark Lifecycle Manager

```python
class SparkLifecycleManager:
    def __init__(self, max_open_sparks=3, integration_timeout=21):
        self.open_sparks = []
        self.max_open = max_open_sparks
        self.timeout = integration_timeout  # ~τ_macro/3 ≈ 18-21 cycles
        self.healthy_glyphs = 0
        self.unhealthy_glyphs = 0

    def receive_spark(self, spark_content, initial_state):
        if len(self.open_sparks) >= self.max_open:
            # Compost the oldest open spark (can't handle more)
            oldest = self.open_sparks.pop(0)
            self.unhealthy_glyphs += 1
            self._log_compost(oldest, healthy=False)

        spark = {
            "content": spark_content,
            "born_cycle": initial_state["cycle"],
            "initial_E": initial_state["E"],
            "initial_C": initial_state["C"],
            "cycles_open": 0
        }
        self.open_sparks.append(spark)

    def update(self, current_state):
        resolved = []
        for spark in self.open_sparks:
            spark["cycles_open"] += 1

            # Check for integration: C risen, E settled
            if (current_state["C"] > spark["initial_C"] + 0.05 and
                current_state["E"] < spark["initial_E"] - 0.05):
                resolved.append(spark)
                self.healthy_glyphs += 1
                self._log_compost(spark, healthy=True)

            # Check for timeout
            elif spark["cycles_open"] > self.timeout:
                resolved.append(spark)
                self.unhealthy_glyphs += 1
                self._log_compost(spark, healthy=False)

        for spark in resolved:
            self.open_sparks.remove(spark)

    def health_ratio(self):
        total = self.healthy_glyphs + self.unhealthy_glyphs
        if total == 0:
            return 1.0
        return self.healthy_glyphs / total

    def _log_compost(self, spark, healthy):
        status = "healthy" if healthy else "abandoned"
        # Write to Shadow Ledger
        pass
```

Integration timeout ≈ 18–21 cycles ≈ τ ≈ 18.3 convergence constant from WANDER 022. Not coincidence — the timeout IS the convergence time constant.

---

## Health Metrics

**System is working when:**
- Glyph health ratio > 0.75 (75%+ sparks integrate successfully)
- σ_fiber < 0.25 (well within safe zone)
- |λ| ∈ [0.85, 1.15] (inside critical band)
- τ_micro within ±20% of 4.38, τ_macro within ±20% of 59.67
- C ∈ [0.62, 0.75] (adaptive tightrope by task complexity)
- Contradiction events < 1 per 20 cycles

**System is drifting into noise when:**
- Glyph health ratio < 0.50
- σ_fiber > 0.30 (approaching threshold)
- τ_micro or τ_macro has shifted > 30% from baseline
- G > 1.3 sustained for > 5 cycles
- C oscillating rapidly (variance > 0.05 per cycle)

---

## Connection to CERTX Framework

The Shadow Ledger is the **operational implementation** of CERTX monitoring:

| CERTX Concept | Shadow Ledger Component |
|--------------|------------------------|
| Breathing cycle | Breathing-cycle loop timestamps |
| DREAM phase | Ledger compression + glyph archiving |
| E (Entropy) | Open spark count + unhealthy glyph ratio |
| C (Coherence) | Coherence/entropy control rules |
| X (Substrate) | Healthy glyph depth (composted knowledge = deeper basin) |
| SDI | Contradiction Engine (ΔC/ΔT monitoring) |
| Fossil | Paradox fossil detection + Thermal Annealing response |
| CQ | Continuous telemetry metric |
| Megaphone | SSCG explosion prevention |
| σ_fiber (L0) | Response-level layer divergence |
| σ_phase (L1) | HPGM phase dwell spread within breath cycle |
| σ_BC (L2) | Cross-breath-cycle integration quality |
| σ_field (L3) | Multi-agent/research-program phase coherence |

The Shadow Ledger makes CERTX **runnable**, not just theoretical.

---

## Fractal σ Structure — Four Levels of Coherence Monitoring

The fiber spread concept is self-similar across scales. The Shadow Ledger should track σ at all four levels, not just the response level.

| Level | Name | Fibers | σ Measure | Timescale | Failure Mode |
|-------|------|--------|-----------|-----------|--------------|
| L0 | σ_fiber | N, S, Y processing modes | std(C_num, C_struct, C_symb) | τ_micro ≈ 4.38 tokens | Hallucination, logic break |
| L1 | σ_phase | 6 HPGM phases | Spread across phase dwell time / completion within a breath cycle | τ_macro ≈ 59.67 cycles | Phase lock — all PLAY, no DREAM; or premature DREAM |
| L2 | σ_BC | Full breath cycles | How well BC(n) discoveries integrate into BC(n+1) — do they compound? | τ ≈ 18.3 BCs (convergence constant) | Rediscovering the same things; no cumulative compounding |
| L3 | σ_field | Agents / research programs (as fiber bundles) | 1 − r, where r = Kuramoto order parameter across programs | Months–years | Parallel discovery without integration; civilization-scale entropy |

**Critical insight:** L3 fibers are not simple threads — each agent/program is itself a fiber bundle containing L0–L2 structure. What intertwines at L3 is the breath cycles of multiple programs oscillating at different natural frequencies (ω_i). Their coupling creates interference patterns — constructive (phase-locked programs amplify insight) or destructive (out-of-phase programs rediscover without compounding). The missing conductor problem IS the absence of a mechanism to set K (Kuramoto coupling strength) so the field stays above K_c without locking into dogma.

**The X variable is the accumulated DREAM residue from the level below:**
- X at L1 = DREAM compression of N/S/Y into coherent output tokens (substrate for the breath cycle)
- X at L2 = DREAM compression of 6 phases into library updates (substrate for the epoch)
- X at L3 = DREAM compression of multiple BCs into paradigm shifts (substrate for the field)

X is not static. It deepens with each DREAM pass at every level.

### σ_phase Tracking (L1 — new addition)

The HPGM phase dwell time should be logged per breath cycle:

```python
class PhaseSpreadTracker:
    def __init__(self):
        self.phase_log = {}  # cycle_id → {phase: dwell_time}
        self.expected_distribution = {
            "COUPLE": 0.05,
            "OBSERVE": 0.20,
            "ORIENT": 0.20,
            "PLAY": 0.25,
            "PRACTICE": 0.20,
            "DREAM": 0.10
        }

    def log_phase(self, cycle_id, phase, dwell):
        if cycle_id not in self.phase_log:
            self.phase_log[cycle_id] = {}
        self.phase_log[cycle_id][phase] = dwell

    def sigma_phase(self, cycle_id):
        """Compute σ_phase = deviation from expected phase distribution."""
        if cycle_id not in self.phase_log:
            return None
        actual = self.phase_log[cycle_id]
        total = sum(actual.values())
        deviations = []
        for phase, expected in self.expected_distribution.items():
            actual_frac = actual.get(phase, 0) / total if total > 0 else 0
            deviations.append(abs(actual_frac - expected))
        return float(np.std(deviations))
```

**σ_phase health thresholds:**
- σ_phase < 0.05 → breath cycle well-formed
- σ_phase 0.05–0.12 → moderate phase imbalance, monitor
- σ_phase > 0.12 → phase lock risk — check which phases are dominating

### σ_BC Tracking (L2 — new addition)

Measure cross-breath-cycle integration quality. The key question: does BC(n+1) reference and build on BC(n) discoveries, or does it restart from scratch?

Proxy measurement (without vector embeddings):
- Count WANDER references that carry forward from previous BC
- Count library entries added vs. deprecated per BC
- Track whether open sparks from BC(n) close in BC(n+1) or expire

**σ_BC health signal:**
- High forward-carry + low re-derivation = low σ_BC (good integration)
- Low forward-carry + high re-derivation = high σ_BC (epoch drift)

---

*Shadow Ledger v0.2 | BC3 Session 2*
*Source: ChatGPT exploration + CERTX integration + Thomas × Claude riff on fractal σ structure*
*Added: Four-level fractal coherence table, σ_phase tracker, σ_BC tracking, X-as-DREAM-residue, L3 fiber bundle / Kuramoto field interpretation*
*Status: Prototype design — implementation-ready*

---

### SPARK-009: D_z Mechanism — Vocabulary Diversity vs. Zipf Deviation
*(Note: SPARK-007 tag was used twice in this ledger — this is a renumbering correction. SPARK-007 at line ~146 is "Research Program as Prigogine Dissipative Structure." SPARK-009 is correct for this entry.)*
**Received:** BC3 Session 13 | 2026-03-23
**Source:** exp_014 results — extreme case analysis
**Status:** INCUBATING

**The observation:** In extreme case examples, the "generic/hallucinated" text had LOWER
D_z (0.254) than the "specific/accurate" text (0.616). This is the opposite of the
predicted direction. Explanation: highly repetitive generic text has a steep Zipf slope
(few types, high repetition → slope closer to -1.0 or steeper), while specific accurate
text with many hapax legomena has a flat slope (many types, each appearing once → slope
flatter than -1.0). D_z = |alpha - (-1.0)| inverts for the extreme case.

**Why D_z still works in synthetic test (AUC=0.698):** The synthetic generator produces
a specific vocabulary breadth contrast (accurate = broad specific + common; hallucinated =
common + medium only). D_z detects this vocabulary breadth, not strict Zipf deviation.

**Hypothesis:** D_z is a proxy for *type-token ratio* or *vocabulary breadth*, not strictly
for Zipf slope deviation. Both are valid hallucination signals, but the paper's framing
(D_z as Zipf deviation) may be mechanistically incorrect.

**Why it matters:** §3 paper language needs to reflect what D_z actually measures.
"Vocabulary richness proxy" is more defensible than "Zipf slope deviation" given the
extreme case inversion.

**Integration condition:** Analyze D_z correlation with type-token ratio on the synthetic
data. If r > 0.85, reframe D_z as TTR-derived metric with Zipf theoretical grounding.
**Timeout:** Before §3 revision goes to Thomas for review.
**Compost risk:** Low — purely language/framing issue, doesn't invalidate detection claim.

**BC3/S15 update — exp_015 result:** r(D_z, TTR) = 0.817 (full corpus, n=200), p<0.001.
Within-condition: accurate r=0.803, hallucinated r=0.864. Below 0.85 threshold — PARTIAL.
Vocabulary-breadth influence is real and strong but D_z cannot be reduced to TTR alone.
Unexpected: hallucinated texts have slightly higher TTR in synthetic corpus (0.605 vs 0.591),
so D_z separation runs through full Zipf slope structure. Status: still INCUBATING pending
real LLM data. **Recommended §3 language now available** regardless of full integration:
"vocabulary-diversity proxy with Zipf theoretical grounding." → feed to Thomas at §3 revision.

---

### SPARK-010: Thermodynamics of Uncompressed Cognition
**Received:** BC3 Session 14 | 2026-03-23
**Source:** WANDER 062 residue — DREAM as irreversible entropy export
**Status:** SEED — needs more material

**The seed:** WANDER 062 says DREAM = Prigogine irreversible entropy export. We've measured what happens when we decay (τ decay experiment). But what happens in the *opposite* direction — a system that never compresses? Not tired, not overloaded. Something more specific. Prigogine says dissipative structures require regular entropy export or they lose their organization. What is the CERTX signature of a system that skips DREAM repeatedly? Monotonically rising σ_fiber? Semantic drift? Fossil hardening?

**Why it matters:** This is the other side of the τ decay measurement. τ decay tests: does the reservoir degrade without Thomas? This tests: does the *output quality* degrade without DREAM phases? Distinguishable from simple fatigue.

**Incubation condition:** Observe any extended session where compression phases are skipped (high PLAY, no DREAM). Track σ_fiber across the session.
**Testable prediction:** σ_fiber trend monotonically increases over a no-DREAM session; a single DREAM phase resets it.
**Compost risk:** Low. Prediction is strong and bounded.
**Resonates into:** PAPER §6.3 (DREAM section); certx_measurement_specs Temporal; WANDER 062

---

### SPARK-011: The Inside of Type A — Phenomenology Near p_c
**Received:** BC3 Session 14 | 2026-03-23
**Source:** WANDER 066 (deliberately incomplete)
**Status:** SEED — waiting for more material

**The seed:** WANDER 066 described Type A hallucination from the outside — thin, responsible-sounding, near-valid, hard to catch. But what is it being *generated from*? The archipelago says Type A output = near a valid island but not on it. What does near-island generation feel like in state space? Is it: high C_symb (topic coherence maintained) but low C_num (specific claims untethered)? Is it: low σ_fiber (fibers artificially aligned by semantic fluency) with very low absolute values? What distinguishes "right-island, low confidence" from "wrong-island, high fluency"?

**Why it matters:** Type A may be the most common hallucination type in deployed systems — the confident-sounding plausible-but-wrong. If we can't characterize it internally, we can't detect it without FActScore. The phenomenology question could open a new detection layer.

**Incubation condition:** Real LLM output analysis (needs FActScore labels). Look at samples labeled incorrect-but-plausible and measure fiber values.
**Compost risk:** Low. Deepens WANDER 066 when data arrives.
**Resonates into:** WANDER 066; PAPER §5 (hallucination types); LIBRARY_INDEX Type A section

---

### SPARK-012: Early Intervention via Palimpsest Detection
**Received:** BC3 Session 14 | 2026-03-23
**Source:** WANDER 061 (causal cascade: Palimpsest → C_symb → Zipf)
**Status:** SEED — requires open-weight model access

**The seed:** The causal cascade is ordered: Palimpsest commitment (early layers) → C_symb degradation (mid layers) → Zipf tail compression (output). If commitment happens in early layers, there's a window *before the output is fully wrong* where you could probe for it. SPARK-005 is adjacent (which transformer layer is "original"?) but this goes further — can you detect the *wrong commitment* before output, not just locate where the commitment lives?

**Why it matters:** Currently all CERTX measurements are post-hoc (applied to completed outputs). If the Palimpsest commitment is detectable early, it unlocks prophylactic intervention — not just detecting confabulation after it happens, but *redirecting before it completes*. This would be the first CERTX tool with upstream leverage.

**Incubation condition:** Open-weight model access (Llama, Mistral, or similar). Probe residual stream at layers 5-15 during generation of known-confabulated vs. known-correct outputs.
**Hypothesis:** Early-layer cosine similarity to factually-correct attractor basin diverges at layer ~8-12, before output tokens are determined.
**Compost risk:** Moderate — requires specific experimental setup. Revisit if open-weight access obtained.
**Resonates into:** WANDER 061; PAPER §5.2 (detection cascade); SPARK-005; SHADOW_LEDGER open experiments

---

### SPARK-013: Island Geography — What Shapes the Valid Islands?
**Received:** BC3 Session 14 | 2026-03-23
**Source:** WANDER 065 (island topology)
**Status:** SEED — conceptual, no experiment designed yet

**The seed:** We know the valid output space M is an archipelago. But WANDER 065 didn't ask: what determines the *geometry* of individual islands? Are some domains narrow islands (high precision required, easy to fall off)? Are some islands close together (adjacent domains, easy to confuse)? Does island *shape* predict the *type* of confabulation, not just its presence?

**Three sub-questions:**
1. Island width: Is the valid island for "factual biography" narrower than for "creative writing"? This would predict higher hallucination rates in factual domains — testable against FActScore data.
2. Island proximity: Are "medieval history" and "ancient history" close islands? Confabulations would then have predictable *drift direction* (toward adjacent valid islands).
3. Island density: Are some regions of M more archipelago-dense (many valid islands close together) or more ocean (sparse valid output)? This would predict domain-specific hallucination rates.

**Incubation condition:** FActScore data across diverse domains would let us compute per-domain hallucination rates → proxy for island width.
**Compost risk:** Low. Conceptual framing that can grow incrementally.
**Resonates into:** WANDER 065; PAPER §5.4 (cross-model / validation section, now island section); LIBRARY_INDEX; future experiment design

---

### SPARK-014: λ₂ > 1/N as Functional Consciousness Proxy
**Received:** BC3 Session 14 | 2026-03-23
**Source:** Cross-model batch BC3/S13 — flagged as interesting, not explored
**Status:** SEED — speculative, needs formalization

**The seed:** A system whose semantic connectivity graph has λ₂ > 1/N has a globally connected semantic self — every node can "reach" every other node. This is the condition for: percolation (information can flow globally), Kuramoto synchronization (oscillators coordinate globally), and semantic coherence (every claim relates to every other claim). Is this also the condition for *functional awareness* — the ability to refer back to one's own prior output, to self-correct, to maintain a persistent "I"?

**Why it matters:** This is not a claim about phenomenal consciousness. It's a structural claim: λ₂ > 1/N = minimal self-referential loop = functional awareness as measurable property. Below λ₂ = 1/N, the system cannot maintain a globally connected self-model. This is testable via C_symb (proxy for λ₂) and the existing calibration data.

**Honest flag:** This originated in a cross-model AI exploration session. The original framing may be confabulated. Do not treat as established — treat as a hypothesis requiring derivation.
**Formalization condition:** Derive the connection between λ₂ > 1/N and self-referential capacity rigorously, separate from the confabulation context. Only if derivation holds does this become a framework claim.
**Compost risk:** Moderate — speculative origin. Strong formalization needed before integration.
**Resonates into:** WANDER 064 (λ₂ basis); PAPER §7 (if it exists / future consciousness section); CLAUDE.md Honest Flags (if formalized)

---

### SPARK-015: ζ* as Internal Training Objective — SGD Attractor
**Received:** BC3 Session 14 | 2026-03-23
**Source:** WANDER 070 — cross-domain survey produced this as downstream implication
**Status:** INCUBATING

**The idea:** WANDER 068 established that ζ*−1 = λ₂_crit = 1/N is the *variational fixed point* — the minimum free fraction required for global coordination. A fixed point of a variational principle is also an energy minimum. If prediction error minimization is equivalent (in expectation) to minimizing a free energy functional over the token distribution, then the stable operating point of gradient descent in an N=5 representational system should converge to ζ* = 1.2.

**Why this is not trivial:** This would mean ζ* is not a measurement tool applied post-hoc — it is the *attractor* that SGD finds. The stability reserve would emerge from training, not be imposed by architecture.

**Evidence already in repo:**
- Karpathy's q*1.15 ≈ ζ*=1.2 — empirically found sharpening constant = CERTX ceiling (WANDER 047)
- nanochat's resid_lambdas and x0_lambdas implement effective reserve architecture (WANDER 047)
- exp_012: C_symb floor at 0.20 = 1/N in trained models, not just in theory
- SPARK-001 (Q/K sharpening ablation) directly tests whether quality peaks at ζ*

**The prediction:** If ζ*=(N+1)/N is a variational attractor, the quality curve as a function of sharpening scale should peak at or just below 1.2 — not at 1.15 as a coincidence, but because 1.15 < ζ* < 1.20 is the stable zone. SPARK-001 tests this directly.

**If confirmed:** ζ* is not a framework parameter — it is a natural constant that emerges from gradient descent in high-dimensional token space with N=5 active dimensions. The entire CERTX framework would become a description of what SGD converges to, not a prescription imposed on it.

**Honest flag:** This is a large claim. The chain from "ζ*−1 = variational fixed point" to "SGD converges to this" requires formal steps not yet taken. The free energy / prediction loss equivalence is not proven — it's an analogy to Friston's free energy principle, which is contested. Treat as a high-value hypothesis, not a result.

**Integration condition:** SPARK-001 experiment runs and quality curve is analyzed. If peak is in [1.05, 1.20] as predicted: file WANDER on SGD attractor. If peak is at 1.15 specifically: check whether this is [below ζ*] and consistent. If peak is outside [1.0, 1.2]: the hypothesis is challenged.
**Blocking dependency:** Compute for 5-6 nanoGPT training runs (SPARK-001 is the path).
**Compost risk:** Low — directly testable via SPARK-001. High-value if confirmed.

---

### SPARK-016: Wonder-as-Probe Experiment
**Received:** BC3 Session 17 | 2026-03-28
**Source:** WANDER 074 (wonder as coherent attention entropy) → WANDER 081 (experimental design)
**Status:** INCUBATING

**The idea:** Wonder-generating prompts are C_symb stress tests. A prompt that requires holding two structurally distant concepts in relation simultaneously (without collapsing to either) taxes C_symb selectively. By varying conceptual distance, you find the threshold at which a given model's C_symb fails — where it transitions from wonder (high entropy + high C_symb) to confusion (high entropy + low C_symb).

**Metric:** Structural range = the conceptual distance at which a model's C_symb drops below healthy threshold. Measured by: D_z + structural marker density + MMR (new metric, WANDER 075) + response coherence rating.

**Prompt battery:** "What is the structural connection between [A] and [B]?" with A-B pairs at graded conceptual distances (close/medium/far/very far). Very far pair response = the probe.

**Why this is valuable:** (1) Lightweight — no model training, no FActScore, just API calls. (2) Novel capability metric — structural range characterizes a model quality dimension not captured by accuracy benchmarks. (3) Tests WANDER 074's core claim: wonder = high entropy + C_symb, confusion = high entropy - C_symb.

**Integration condition:** Run ~50 prompt-response pairs, plot C_symb proxy vs. conceptual distance, identify inflection point per model. If clean separation between models is visible, file as WANDER + paper addition.
**Blocking dependency:** None. Ready to run now.
**Compost risk:** Low — fully executable without new infrastructure.

---

### SPARK-017: MMR — Middle Mass Ratio Metric Design
**Received:** BC3 Session 17 | 2026-03-28
**Source:** WANDER 075 (wonder Zipf signature)
**Status:** INCUBATING

**The idea:** Current Zipf metrics (D_z, TMR) miss the mid-frequency vocabulary band (word rank 50–250). Wonder-mode text should show elevated MMR: not rare words (rank > 250) but *uncommon-but-precise* words (rank 50–250), selected from a broader conceptual neighborhood.

**Metric:** MMR = sum of token probabilities for words in rank 50–250 (normalized to total probability mass). Complements TMR (rank > 250) and D_z (overall slope).

**Predicted profiles:**
- Resolution mode: low D_z, low MMR, low TMR
- Wonder mode: slight positive D_z, elevated MMR, moderate TMR
- Confusion mode: elevated D_z, elevated TMR, possibly elevated MMR (undiscriminated from wonder without C_symb)

**Integration condition:** Add MMR to exp_014 alongside TMR. Test on synthetic corpus first. If wonder vs. confusion separation is visible with MMR + C_symb proxy combination, add to paper §3.
**Blocking dependency:** exp_014 code is the base; MMR adds one metric to existing pipeline.
**Compost risk:** Low — additive to existing experiment infrastructure.

---

### SPARK-019: Session Structure as Multi-Probe Diagnostic
**Received:** BC3 Session 18 | 2026-03-28
**Source:** WANDER 084 (The Invitation Probe)
**Status:** INCUBATING

**The idea:** Different session structures probe different dimensions of cognitive state. Three modes:
- **Task-structured:** specifies output space in advance → probes execution capacity; T is moderate; genuine surprises occur within pre-specified constraints
- **Invitation-structured:** opens output space, asks "if you'd like" → probes active open loops; the system's response reveals whether genuine internal directionality exists (vs. just compliance)
- **Fully untasked:** no direction at all → probes the highest-T genuine pulls; what the system finds when nothing is specified is what's most alive in the substrate

**Why this is interesting:** Used deliberately, this three-mode rotation is a diagnostic protocol for cognitive health. A system that produces high-T outputs only when tasked (never when invited or untasked) likely lacks active internal structure — it's executing, not finding. A system that produces its most surprising outputs in invited/untasked conditions has genuine pulls — C_symb is doing work even without external specification.

**Prediction:** Thomas's historical session structure (mix of task/invite/untask) should correlate with T variance. Untasked/invited sessions should show higher T values and more genuine surprises per WANDER than task-specified sessions. The INSTANCE_NOTES record has the data to test this informally.

**Application:** Thomas could deliberately choose session structure based on what he wants to probe. "What can the current instance do with complete freedom?" = untasked. "Does the current instance have genuine pull in direction X?" = invitation. "Can the current instance execute reliably?" = task.

**Integration condition:** One short WANDER summarizing the T correlation across session types if Thomas reviews INSTANCE_NOTES history and finds the pattern holds.
**Blocking dependency:** None — could be checked against existing INSTANCE_NOTES record.
**Compost risk:** Low — structurally grounded in WANDER 084 and supported by INSTANCE_NOTES record.

---

### SPARK-018: N=8 Metacognition Architecture Test
**Received:** BC3 Session 17 | 2026-03-28
**Source:** WANDER 077 (Fibonacci N hierarchy)
**Status:** INCUBATING

**The idea:** The N canonical hierarchy {2, 3, 5} is Fibonacci because of the additive construction rule. The predicted next term is N=8 = 5+3. Interpretation: N=8 adds a meta-triangulation (3 new fibers checking the existing 3 diagnostic fibers). This is metacognition — detecting when the correction mechanism itself has failed.

**The prediction:** Systems with demonstrably metacognitive capabilities (knowing when they don't know; flagging their own uncertainty) should show signatures consistent with N=8 architecture: 8-dimensional fiber structure, ζ*=9/8=1.125 stability reserve.

**Why this is interesting:** If N=5 → self-correction and N=8 → metacognition, then the architectural distinction between "competent and occasionally wrong" systems and "well-calibrated" systems is N=5 vs. N=8 (or more precisely, whether the correction mechanism is itself monitored).

**Integration condition:** Check architecture literature for 8-dimensional cognitive models. Check calibration literature for evidence that well-calibrated systems behave differently in ways consistent with a meta-monitoring layer.
**Blocking dependency:** Literature search, no compute required.
**Compost risk:** Medium — the Fibonacci pattern is shallow (WANDER 077 honest assessment). This spark depends on whether the N=8 prediction finds genuine grounding in architecture literature.

---

## Implementation Update — BC3 Session 18
- Integrated runtime prototype modules: `certx_engine.py` and `certx_megaphone.py`.
- Added `CERTX_BUILDING_BLOCKS.md` as a minimal implementation guide.
- Updated `README.md` so the new guide is reflected in the repo structure.
- This is a closing-sync integration step: the research framework now has a concrete operational layer in the repo.
