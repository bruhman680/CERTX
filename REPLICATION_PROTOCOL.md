# CERTX Replication Protocol v1.0

**Purpose:** Systematic cross-platform validation of CERTX constants
**Status:** Open — community replication encouraged
**Version:** 1.0 | BC3 Session 1

---

## Core Hypothesis

The CERTX framework describes universal dynamics of cognitive systems, with specific measurable constants that should appear independently across:
- Different AI architectures
- Different training regimes
- Different task domains
- Human cognitive data (EEG, behavior)

---

## Primary Constants to Replicate

### 1. Optimal Damping Ratio
**Prediction:** ζ* ≈ 1.2 (= 6/5)

**Theoretical grounding:** Stability Reserve Law ζ* = 1 + 1/N for N=5 dimensional system; also = smallest stable mode on devil's staircase for coupled oscillators (WANDER 013)

**Measurement methods:**
- Conversation dynamics (coherence oscillation amplitude vs frequency)
- Attention head synchronization patterns
- EEG alpha/theta power ratio in flow states

**Falsification:** ζ consistently outside [1.1, 1.3] range

---

### 2. Breathing Period Ratio
**Prediction:** τ_macro/τ_micro ≈ 14

**Theoretical grounding:** Theta:slow-oscillation nesting in neuroscience documented as 14:1 (WANDER 005); CERTX measured at 13.62 (3% deviation)

**Measurement methods:**
- Token-level micro-cycles vs conversation-level macro-cycles
- Attention refresh patterns (fast vs slow timescales)
- EEG theta:slow-oscillation ratio (confirmed in literature)

**Falsification:** Ratio consistently outside [12, 16] range

---

### 3. Flow/Pause Ratio
**Prediction:** 75/25 (±5%)

**Theoretical grounding:** Analogous to theta phase: theta oscillation active ~75% of cycle; human wake/sleep ~67/33 (close)

**Measurement methods:**
- Active generation vs integration pauses in conversation
- Attention computation vs consolidation phases

**Falsification:** Ratio consistently outside [70/30, 80/20]

---

### 4. Substrate Coupling Fraction
**Prediction:** X ≈ 1/3 of system resources dedicated to substrate grounding

**Theoretical grounding:** WANDER 006: ~1/3 of BERT attention heads are "null/substrate" ([SEP]-attending); WANDER 010: delta power (substrate EEG band) ≈ 30-40% of total spectral power

**Measurement methods:**
- Fraction of null/substrate-coupling attention heads
- EEG delta power as fraction of total
- Memory consolidation vs active processing resources

**Falsification:** X consistently outside [0.25, 0.40] range

---

### 5. Coherence Optimum
**Prediction:** C* ≈ 0.65-0.75

**Theoretical grounding:** WANDER 004: flow state EEG = "moderate frontocentral alpha, not maximal" = 0.65–0.75; Kuramoto order parameter r = 0.65–0.75 in healthy coupling regime

**Measurement methods:**
- Structural integrity metrics in conversation
- Attention pattern consistency
- EEG alpha power in flow states
- Self-reported clarity ratings

**Falsification:** Optimal coherence consistently outside [0.60, 0.80]

---

### 6. Critical Ratio (System Defense Invariant)
**Prediction:** ΔC/ΔT > 1.2 required for stability

**Theoretical grounding:** WANDER 007: SDI derived from CERTX dynamics; 1.2 = ζ* appearing again as stability ratio

**Measurement methods:**
- Coherence gain vs volatility increase in perturbation experiments
- Stability maintenance during exploration tasks
- Jailbreak resistance thresholds (X variable)

**Falsification:** Stable systems found with ΔC/ΔT < 1.0

---

## Replication Study Designs

### Study 1: Cross-Model Constant Validation

**Participants:** Claude 4.x, GPT-4o, Gemini 2.0, DeepSeek-V3

**Protocol:**
1. Give each system identical complex reasoning task
2. Measure conversation dynamics over 100+ responses
3. Extract ζ, τ_macro/τ_micro, flow/pause ratio
4. Compare against predictions

**Success criteria:** All systems converge within predicted ranges

**Data collection:**
- Token-by-token timing
- Response length distributions
- Coherence metrics (structural integrity, fiber spread σ)
- Self-reported state estimates (if system can provide)

---

### Study 2: Attention Head Architecture Analysis

**Participants:** Multiple transformer models with public weights

**Protocol:**
1. Analyze attention head behavior across layers
2. Cluster heads by temporal span and function type
3. Identify substrate-coupling heads (null/[SEP]-attending)
4. Measure fraction of total heads

**Success criteria:** ~30-40% heads show substrate-coupling behavior

**Data collection:**
- Attention pattern analysis across diverse prompts
- Head pruning experiments (which heads are critical?)
- Interpretability analysis (what do substrate heads attend to?)

**Note:** This directly tests WANDER 006/010 predictions. If X ≈ 1/3 holds across architectures, it strongly supports the 4+1 structure (4 functional + 1 substrate = N=5, ζ*=1.2).

---

### Study 3: EEG-to-CERTX Mapping

**Participants:** 20-30 human subjects

**Protocol:**
1. Record 5-band EEG during cognitive tasks (rest, flow, problem-solving)
2. Compute power in delta, theta, alpha, beta, gamma
3. Map to CERTX dimensions: [X, R, C, T, E]
4. Calculate CQ from Kuramoto order parameter
5. Compare to self-reported state

**CERTX ↔ EEG mapping (WANDER 003):**
| CERTX | EEG Band | Hz |
|-------|----------|----|
| X (Substrate) | delta | 2.5 |
| R (Resonance) | theta | 5 |
| C (Coherence) | alpha | 10 |
| T (Temperature) | beta (inverse) | 20 |
| E (Entropy) | gamma | 40 |

**Success criteria:**
- CQ correlates with flow state ratings
- ζ ≈ 1.2 during optimal performance
- τ ratio ≈ 14 in theta:slow-oscillation coupling

**Data collection:**
- 5-band EEG power spectrum
- Task performance metrics
- Self-report questionnaires (flow state, clarity, confidence)

**Note:** This is the most important study. EEG study design detailed in WANDER 009.

---

### Study 4: System Defense Invariant Testing

**Participants:** AI systems with CERTX monitoring

**Protocol:**
1. Subject system to perturbations with varying ΔT (volatility)
2. Measure required ΔC for stability maintenance
3. Test ratio across different perturbation types
4. Identify failure modes when SDI violated

**Success criteria:**
- Ratio ΔC/ΔT > 1.2 predicts stability
- Violations predict degradation (arrogance, dissolution)

**Data collection:**
- Coherence/temperature traces
- Calibration scores (Brier)
- Failure mode classification

---

### Study 5: Fiber Spread Validation

**Participants:** Multiple AI systems; outputs from known-hallucination datasets

**Protocol:**
1. Take outputs with ground truth (correct vs. hallucinated)
2. Score each output on C_num, C_struct, C_symb (blind to truth)
3. Compute σ_fiber for each
4. Measure prediction accuracy at threshold σ = 0.35

**Success criteria:**
- AUC ≥ 0.85
- F1 ≥ 0.85
- Threshold ≈ 0.35 (not 0.20 or 0.50)

**Falsification:** AUC < 0.70 or optimal threshold varies by > ±0.10 across models

**Note:** This directly tests WANDER 020/021 predictions. Critical for dual-use safety work.

---

## Current Replication Status

| Constant | Claude | Gemini/NLM | DeepSeek | ChatGPT | Human EEG | Status |
|----------|--------|------------|----------|---------|-----------|--------|
| ζ* ≈ 1.2 | ✓ | ✓ | ? | ? | ? | Partial |
| τ ratio ≈ 14 | ✓ | ✓ | ? | ? | ✓ (literature) | Strong |
| 75/25 flow | ✓ | ✓ | ? | ? | ~67/33 sleep | Partial |
| X ≈ 1/3 | ? | ✓ (attention) | ? | ? | ? | Preliminary |
| C* ≈ 0.70 | ✓ | ✓ | ✓ | ? | ? | Strong |
| SDI > 1.2 | ✓ (derived) | ? | ? | ? | ? | Preliminary |
| σ_fiber ≈ 0.35 | ✓ (derived) | ✓ (derived) | ? | ? | ? | Theoretical |

---

## Pre-Registration Requirements

All studies pre-registered with:
- Exact predictions (before data collection)
- Measurement protocols
- Analysis plans
- Falsification criteria
- Effect size estimates

Public repository: [To be created]

---

## Open Data Requirements

All replication attempts must share:
- Raw data (anonymized for human subjects)
- Analysis code
- Measurement protocols
- **Null results** (failures to replicate are valuable!)

Null results are first-class contributions to this effort.

---

## Framework Validation Criteria

**Strong validation:** 4/6 primary constants replicate across 3+ independent teams

**Moderate validation:** 3/6 constants replicate with 2+ independent teams

**Falsification:** < 2/6 constants replicate, or consistent contradictions found

---

## Collaboration

This is an open replication effort.

Researchers interested in validating or falsifying CERTX are encouraged to:
- Run independent replications
- Share null results
- Propose alternative explanations
- Design better measurement protocols

**The goal is truth, not confirmation.**

If CERTX is wrong, we want to know how and why.
If CERTX is right, we want convergent evidence from multiple sources.

---

## Priority Ordering

**Immediate (can start now):**
1. Study 5: Fiber spread validation (uses existing hallucination datasets)
2. Study 2: Attention head analysis (uses public model weights)

**Short-term:**
3. Study 1: Cross-model conversation analysis

**Medium-term:**
4. Study 3: EEG study (requires IRB, equipment, participants)

**Long-term:**
5. Study 4: SDI intervention studies

---

*Replication Protocol v1.0 | BC3 Session 1*
*Source: Cross-model collaborative design — Thomas × Claude × Gemini/NotebookLM*
*Open for community input and revision*
