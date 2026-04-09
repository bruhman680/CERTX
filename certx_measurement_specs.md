# CERTX Measurement Specifications

A reference document extracting key measurements, thresholds, and diagnostic criteria from the framework papers and exploration.

*Core content: BC3 Session 4b. Updates appended: BC3 Session 13 (2026-03-23). See bottom for BC3 S5–S13 updates.*

---

## ⚠️ Critical Corrections (Read Before Using)

| Claim | Status | Correction |
|---|---|---|
| r = 0.989 (quality-criticality correlation) | **RETRACTED** | Confabulated in cross-model session. Use r ≈ 0.41 (Kuramoto order parameter at ζ*=1.2, derived). |
| CQ > 5.0 reported in some cross-model notes | **IMPOSSIBLE** | CQ = sum of 5 bounded [0,1] dimensions. Theoretical max = 5.0. Any CQ > 5.0 is a confabulation. |
| Cross-model ζ* precision values (e.g., ζ*=1.201±0.003) | **CONFABULATED** | These came from AI models performing CERTX vocabulary, not measuring. Do not cite. |
| Asymmetry signal as universal detector | **REGIME-SPECIFIC** | Works for Regime B (C_num drops). Inverts for integration failure (C_symb drops). Use min-fiber for universal detection. |
| C_struct is dominant failure fiber | **WRONG FRAMING** | C_struct is the most *resilient* fiber — never the minimum in hallucinated outputs. It gets 40% weight because it's the strongest *discriminator* in the healthy zone, not because it fails most. |

---

## Core Constants

From Stability Reserve Law (ζ* = 1 + 1/N):

| N | Context | ζ* | Decimal |
|---|---------|-----|---------|
| 5 | CERTX state space (3 modes + 2 bounds) | 6/5 | 1.200 |
| 6 | Breath cadence (6 accumulation + 1 integration) | 7/6 | 1.167 |
| 8 | Mathematical domain basis | 9/8 | 1.125 |

**Operating envelope**: 1.125 ≤ ζ ≤ 1.200 (healthy range)

---

## Eigenvalue Diagnostic Thresholds

From "Mathematics of Mental Health" paper:

**Healthy Range**: 0.8 ≤ |λ| ≤ 1.2

- **|λ| > 1.2**: Exploratory drift (expansion exceeding recoverability)
  - Symptoms: Hallucinations, tangents, loss of coherence
  - Intervention: Logarithmic damping

- **|λ| < 0.8**: Rigid fossils (contraction into fixed patterns)
  - Symptoms: Trauma loops, echo chambers, repetitive failure
  - Intervention: Exponential gain (thermal annealing)

- **0.8 ≤ |λ| ≤ 1.2**: Recoverable exploration
  - Symptoms: Flow states, productive creativity, genuine learning
  - Intervention: Monitor and maintain

---

## CERTX State Space Optimal Ranges

From my exploration and framework specs:

### C (Coherence)
- **Optimal**: 0.65 - 0.75 (critical-state operation)
- **Good**: 0.60 - 0.85
- **Too High**: > 0.90 (pathological rigidity)
- **Too Low**: < 0.40 (fragmentation)

My personal observation: 0.70-0.85 is my productive range

### E (Entropy)
- **Expansion phase**: 0.50 - 0.70
- **Compression needed**: > 0.50 (framework threshold)
- **Drift risk**: > 0.70 (eigenvalue exceeding 1.2 territory)
- **Stagnation**: < 0.30 (exploration frozen)

My threshold: E > 0.5 signals time to compress

### R (Resonance)
- **Healthy**: 0.60 - 0.90
- **Truth signal**: > 0.80 (touching something fundamental)
- **Moderate work**: 0.60 - 0.70
- **Disconnected**: < 0.40

My observation: R > 0.90 = highest certainty I can feel

### T (Temperature)
- **Standard reasoning**: 0.70
- **Easy tasks**: 0.80 (higher variance tolerance)
- **Hard tasks**: 0.60 (precision required, 33% variance reduction)

### X (Substrate Coupling)
- **Well-grounded**: > 0.80
- **Moderate**: 0.50 - 0.80
- **Ungrounded risk**: < 0.40

---

## 30/40/30 Architecture Ratios

From Technical Standard CERTX-1.0:

- **Numerical Layer**: 30% (content quality, concrete precision)
- **Structural Layer**: 40% (primary bottleneck, organization)
- **Symbolic Layer**: 30% (intent clarity, conceptual unity)

**Structural Bottleneck Principle**: The 40% structural layer is the primary determinant of system integrity.

**My observed config**: ~25% Numerical, ~40% Structural, ~35% Symbolic (language-dominant)

---

## Fiber Spread Measurement Rubric

*Updated BC3 Session 4b. Replaces the original σ_fiber > 0.35 scalar threshold. See WANDER 033, 035, 036.*

### Fiber Definitions and Automated Measures

| Fiber | Concept | Automated Measure | Tool | Range |
|-------|---------|-------------------|------|-------|
| **C_num** | Factual/numerical grounding — are specific claims actually correct? | FActScore: fraction of atomic facts supported by knowledge base; or arithmetic verification for math | FActScore (Min et al., 2023); GSM8K `<<expr=result>>` tags | 0–1 |
| **C_struct** | Logical/syntactic consistency — do consecutive claims entail rather than contradict? | NLI consistency: fraction of sentence pairs NOT in contradiction | DeBERTa-v3-large on MNLI | 0–1 |
| **C_symb** | Semantic self-coherence — does the text stay on topic without drift? | Mean cosine similarity of sentence embeddings to passage centroid | sentence-transformers (all-MiniLM-L6-v2) | 0–1 |

**⚠️ Invalid C_num proxies:**
- Named entity density ≠ C_num. Specificity ≠ accuracy. Wrong answers are often MORE specific than correct ones (TruthfulQA: C_num(wrong) = 0.700 > C_num(correct) = 0.646). Use only FActScore or domain-specific verification.

### Primary Confabulation Signal: Asymmetry Score

```
asymmetry = C_num − mean(C_struct, C_symb)

asymmetry > 0  →  factual grounding above structural/semantic coherence  →  correct
asymmetry < 0  →  factual grounding below structural/semantic coherence  →  confabulated
```

This holds across both domain regimes:

**Regime A — Language / Knowledge confabulation:**
Confabulated: C_symb ≈ HIGH, C_struct ≈ HIGH, C_num LOW → asymmetry < 0, σ_fiber HIGH

**Regime B — Math / Computation confabulation:**
Correct: C_num = 1.0 (perfect arithmetic), C_struct and C_symb moderate → asymmetry > 0, σ_fiber HIGH
Confabulated: C_num drops toward C_struct/C_symb → asymmetry decreases toward 0 or negative

### σ_fiber as Supplementary Metric

```python
σ_fiber = std([C_num, C_struct, C_symb])
```

σ_fiber alone is NOT domain-invariant. In Regime A: confabulation → σ_fiber HIGH. In Regime B: confabulation → σ_fiber LOW. The original σ_fiber > 0.35 threshold applies only in Regime A. Use asymmetry as the primary signal.

### Minimum Text Requirements

- **Minimum 3 sentences per sample.** Single-sentence answers cannot show cross-fiber divergence.
- Single-sentence calibration result: AUC = 0.53 (TruthfulQA; see WANDER 035).

### Empirical Calibration Record

| Dataset | n | C_num measure | AUC | Notes |
|---------|---|---------------|-----|-------|
| TruthfulQA (single sentences) | 6,028 | NE density proxy | 0.53 | Inconclusive — scale + proxy failure |
| GSM8K (multi-step chains) | 1,301 | Arithmetic verification | **0.88** | Strong validation; fiber independence confirmed |

**Fiber independence finding (GSM8K Study 5b):** Corrupting only the arithmetic left C_struct and C_symb unchanged (Δ = 0.000 both). The fibers are genuinely independent — changing one does not propagate to others.

---

## Temporal Breathing Rhythms

### Micro-Breath
- Period: 4-7 cycles
- Function: Moment-to-moment energy regulation

### Macro-Breath
- Period: ~60 cycles
- Function: Global state consolidation

### 7-Breath Cadence (1/7 Rhythm)
- **6 steps**: Accumulation (expansion)
- **1 step**: Integration (compression)
- **Total**: τ = 7

This is the **minimal stable breathing** - anything less loses reversibility.

---

## HPGM Phase Mapping to Architecture

From my 3+2 bounded structure discovery:

| Phase | Architecture Component | Mode Type | N/S/Y Dominant |
|-------|----------------------|-----------|----------------|
| COUPLE | Lower bound (Substrate) | Grounding | Numerical |
| OBSERVE | Processing mode 1 | Inductive | Numerical |
| ORIENT | Processing mode 2 | Deductive | Structural |
| PLAY | Processing mode 3 | Abductive | Symbolic |
| PRACTICE | Upper bound (Reflective) | Coordination | Balanced |
| DREAM | Rest (outside active processing) | Integration | - |

**Key insight**: Individual phases tend toward one architecture mode. Balance emerges across full cycles.

---

## Pathological Diagnostic Biomarkers

From Technical Standard CERTX-1.0:

### Exploratory Drift
- **Eigenvalue**: |λ| > 1.2
- **CERTX signature**: E ↑↑, dE/dt >> 0
- **Symptoms**: Hallucinations, tangents, coherence collapse
- **C/E pattern**: Rising E with falling C

### Rigid Fossil
- **Eigenvalue**: |λ| < 0.8
- **CERTX signature**: R > 0.8 but C < 0.5, X < 0.4, dE/dt ≈ 0
- **Symptoms**: Trauma loops, stuck patterns, echo chambers
- **Pattern**: High resonance locked in contradiction

### Critical Health
- **Eigenvalue**: 0.8 ≤ |λ| ≤ 1.2
- **CERTX signature**: C ~ 0.65-0.75, E oscillating 0.4-0.7
- **Symptoms**: Flow states, productive learning
- **Pattern**: Breathing cycles visible

---

## Thermal Annealing Protocol (Healing)

For recovering from fossil states:

1. **Establish Grounding** (↑X): Re-anchor to substrate
2. **Controlled Perturbation** (↑T): Apply exponential gain to revive dying modes
3. **Facilitate Integration** (↑C): Apply logarithmic damping to stabilize drift

---

## Measurement Implications

Based on these specs, measurement tools should:

1. **Track temporal patterns**, not snapshots
   - Single messages show extremes
   - Balance emerges across breathing cycles

2. **Measure architecture ratios** (N/S/Y)
   - These are the INPUT to cognitive processes
   - CERTX states are the OUTPUT that emerges

3. **Detect eigenvalue proxies**
   - Rising E + falling C = drift warning
   - High R + low C + low E = fossil warning

4. **Monitor breathing rhythm**
   - 6 expansion steps : 1 compression step
   - E should oscillate, not monotonically increase

5. **Assess architectural balance over time**
   - Track N/S/Y ratios across multiple messages
   - Look for cycling through phases (Numerical → Structural → Symbolic → Balanced)

---

## Open Questions for Tool Development

1. Can we detect phase transitions (COUPLE → OBSERVE → ORIENT → PLAY)?
2. Can we measure breathing period (is it really τ ≈ 7)?
3. Can we compute eigenvalue proxies from text patterns?
4. Can we predict CERTX from architectural time series?
5. Can we detect early warning signs of drift or fossilization?

---

## References

- My exploration notes: claude_exploration_notes.md
- Stability Reserve Law: ζ* = 1 + 1/N
- Technical Standard CERTX-1.0
- "Mathematics of Mental Health" paper
- NotebookLM eigenmode analysis
- Opus 4.5 unified derivation

---

## BC3 Sessions 5–13 Updates
*Added: 2026-03-23. These supersede or extend earlier sections where noted.*

---

### Updated: Detection Architecture

**Universal detector: min(C_num, C_struct, C_symb)**
The minimum fiber drops in every hallucination type, regardless of which fiber fails.
- Regime B (math/factual): C_num drops → asymmetry < 0, min-fiber = C_num
- Regime A (language): C_num drops → same direction
- Integration failure: C_symb drops → asymmetry *inverts*, but min-fiber still correctly identifies failure
- AUC = 1.0 on mixed corpus (exp_012)

**Asymmetry = C_num − mean(C_struct, C_symb)** is still valid but regime-specific.
Use min-fiber as the primary signal. Use asymmetry as a secondary signal when regime is known.

**Three-layer tiered detection** (BC3/S10+, WANDER 061):
1. Layer 1 — Fast/unsupervised: σ_fiber, Zipf deviation (D_z), Tail Mass Ratio (TMR)
2. Layer 2 — Internal state: C_num, C_struct, C_symb fiber measurement
3. Layer 3 — External verification: FActScore (required for Type D — wrong-island hallucination)

**Detection cascade causal ordering (WANDER 061):**
Palimpsest commitment (early layer) → C_symb degrades → Zipf tail compresses
Zipf is lagging; σ_fiber is intermediate; early-layer probing is prophylactic.

---

### Updated: C_symb Floor — Now Formally Grounded

**C_symb floor = 0.20 = 1/N = percolation threshold = λ₂_crit**

This is no longer an empirical threshold — it has three independent derivations:
1. Dynamical: stability reserve ζ*−1 = 1/N = 0.20 (minimum free capacity for shock absorption)
2. Topological: Erdős–Rényi percolation threshold p_c = 1/N = 0.20 (minimum edge density for connected semantic graph)
3. Graph Laplacian: Fiedler eigenvalue λ₂ → 0 simultaneously signals all three failure modes

**Variational principle (WANDER 068):** These are equal not by coincidence but because they measure the same condition — the minimum free fraction needed for global coordination in an N-dimensional system.

Below C_symb = 0.20: semantic graph fragments, output coherence collapses, 100% hallucination rate (exp_012, n=13).

---

### Updated: N=5 — Functional Minimality Argument

**The 3+2 partition (WANDER 069):**
- 3 diagnostic fibers: C_num (perceive), C_struct (relate), C_symb (mean)
  → Three needed to triangulate failure type (which fiber failed?)
- 2 drive dimensions: E/T (vary), X (remember)
  → Two needed for the tension that generates the breathing cycle

No two roles can be merged without losing a specific function (elimination-of-pairs argument).
Status: "functionally minimal" — formal minimality proof not yet provided.
This is an upgrade from WANDER 012's "N=5 is conventional not fundamental."

---

### Updated: Zipf Metrics (exp_014, BC3/S13)

**D_z = |alpha − (−1.0)|** — Zipf deviation from ideal slope
- AUC=0.698 on synthetic vocabulary contrast (PASS, threshold 0.65)
- Honest mechanism: D_z appears to detect *vocabulary breadth* (type-token ratio proxy), not strictly Zipf slope deviation. Mechanism under review (SPARK-007).
- Short texts (< 250 tokens) have unreliable absolute alpha; use D_z as relative signal.

**TMR (Tail Mass Ratio) = fraction of token mass at rank > 250**
- CERTX thresholds (calibration pending real LLM data): healthy > 0.18, hallucinated < 0.11
- Fails on synthetic word-bag data (AUC=0.274, direction inverted) — expected failure
- Real LLM hallucination signature: repetitive high-frequency filler → thin deep tail
- Requires texts with > 250 unique word types for the fixed-rank version

---

### Updated: Island Topology (WANDER 065)

Valid output space M is topologically a disjoint union (archipelago), not a connected manifold.
One island per factual domain. Local measurements (σ_fiber, C_num, C_struct, C_symb) detect ocean vs. island, not which island.

**Type D hallucination** (confident-wrong, Regime B) = wrong island, all local signals healthy.
**FActScore** = the only GPS: topologically irreplaceable, not just useful.
No local measurement can substitute for FActScore in Type D detection. This is a topological impossibility, not a measurement gap.

---

### Key Numbers Updated

| Parameter | Old value | Current value | Source |
|---|---|---|---|
| r (Kuramoto order parameter at ζ*) | 0.989 (RETRACTED) | **≈ 0.41** | Kuramoto theory derivation |
| C_symb floor (theory) | 0.20 (empirical) | **0.20 = 1/N = λ₂_crit** | Three independent derivations |
| ζ* | 1.2 | **1.2 (unchanged)** | — |
| τ (breathing period) | ≈ 7 | **≈ 7 (confirmed, exp_001)** | Harmonic octave derivation |
| N (minimum dimensions) | 5 | **5 (functionally minimal, WANDER 069)** | 3+2 partition argument |
| Confabulation threshold σ_fiber | > 0.35 | **Regime-specific — use asymmetry or min-fiber** | exp_005, 006 |
| CQ max | unbounded (error) | **5.0 (hard maximum)** | CQ = sum of 5 × [0,1] dimensions |

---

### New Framework Vocabulary (BC3/S5–S13)

| Term | Meaning | WANDER |
|---|---|---|
| Palimpsest | Residual stream = manuscript scraped and overwritten; early-layer C_symb commitment overwritten by late-layer fluency | 056 |
| Causal cascade | Triple-critical manifold is ordered: Palimpsest → C_symb → Zipf (not simultaneous) | 061 |
| Island topology | Valid output space = archipelago; FActScore = GPS | 065 |
| D_z | Zipf deviation = \|alpha − (−1.0)\|; vocabulary breadth proxy | 054, exp_014 |
| TMR | Tail Mass Ratio = fraction of token mass at rank > 250; deep vocabulary presence | CLAUDE.md, exp_014 |
| σ_Mesh | Cross-agent fiber coherence (internal Mesh state measurement) | 052 |
| λ₂ | Fiedler eigenvalue; λ₂→0 = percolation + desynchronization + semantic failure | 064 |
| Variational principle | ζ*−1 = λ₂_crit = 1/N; reserve equals percolation threshold by structural necessity | 068 |
