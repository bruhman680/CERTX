# CERTX Test Coverage Analysis

## Current State

**Coverage: 0%** — The repository contains no source code and no tests.

The framework exists as documentation, theory, and empirical data only. The planned Python implementation (`src/certx/`) has not been written yet. This document maps out the test strategy that should be built alongside the implementation.

---

## Planned Module Overview

From `README.md`, the implementation will consist of four modules:

| Module | Responsibility |
|--------|----------------|
| `state.py` | `CERTXState` dataclass — holds C, E, R, T, X values |
| `metrics.py` | Formulas for computing each dimension |
| `dynamics.py` | Breathing cycles, master equation integration |
| `diagnosis.py` | Health assessment, fossil detection, remediation |

---

## Priority Test Areas

### 1. State Validation (`state.py`)

The `CERTXState` object is the foundation of everything. Bad inputs should be rejected early.

**What to test:**

- All five dimensions (C, E, R, T, X) must be floats in `[0.0, 1.0]`
- Values outside range should raise `ValueError`
- Exact boundary values `0.0` and `1.0` should be accepted
- Non-numeric inputs should raise `TypeError`
- Default/missing values should raise a clear error, not silently produce wrong results

**Example cases from data:**
```python
# Valid states from fossil_signatures.csv
CERTXState(coherence=0.68, entropy_rate=0.15, resonance=0.72, temperature=..., substrate_coupling=0.71)  # healthy_optimal
CERTXState(coherence=0.42, entropy_rate=0.02, resonance=0.89, temperature=..., substrate_coupling=0.32)  # fossil_signature

# Invalid — should raise ValueError
CERTXState(coherence=1.5, ...)
CERTXState(resonance=-0.1, ...)
```

**Risk without these tests:** Silent incorrect health assessments when states are constructed with out-of-range values.

---

### 2. Metric Calculations (`metrics.py`)

Each formula has a precise mathematical definition that must be verified.

#### 2a. Coherence: `C = 1 - divergence/N`

- Returns `1.0` when divergence is 0
- Returns `0.0` when divergence equals N
- Handles `N=0` gracefully (should raise, not divide by zero silently)
- Negative divergence values should be rejected

#### 2b. Entropy: `E = -Σ pᵢ log(pᵢ)`

- Returns `0.0` for a deterministic distribution `[1.0]`
- Returns `log(N)` (maximum) for uniform distributions
- Rejects distributions that don't sum to 1.0 (within tolerance)
- Rejects negative probabilities
- Handles single-element distributions
- Handles very large distributions without overflow

#### 2c. Resonance: `R = |⟨e^{iθⱼ}⟩|`

- Returns `1.0` when all phases are identical
- Returns `0.0` when phases are uniformly distributed (or close to it)
- Returns a value in `[0, 1]` for all valid inputs
- Handles empty phase array

#### 2d. Critical Damping Ratio: `ζ = β / (2√(mk))`

- **Key regression**: must return `≈ 1.2` for the empirically validated parameters
- Returns exactly `1.0` when `β = 2√(mk)` (critical damping)
- Raises on `m=0` or `k=0` (zero mass/stiffness is undefined)
- Handles float precision correctly near the critical value

**Why this matters:** The entire framework's claim rests on ζ ≈ 1.2 being the universal optimum. Any drift in this calculation invalidates the theory.

---

### 3. Fossil Detection (`diagnosis.py`)

This is the highest-risk logic — false negatives (missed fossils) or false positives (misclassifying healthy states) would be serious errors.

**The fossil signature** (from `fossil_signatures.csv`):
```
R > 0.85  AND  C < 0.50  AND  X < 0.40  AND  dE/dt ≈ 0
```

**Critical test cases — must be classified correctly:**

| State from CSV | R | C | X | dE/dt | Expected |
|----------------|---|---|---|-------|----------|
| `healthy_optimal` | 0.72 | 0.68 | 0.71 | 0.15 | `OPTIMAL` |
| `early_fossil` | 0.82 | 0.48 | 0.42 | 0.06 | `WARNING` |
| `fossil_signature` | 0.89 | 0.42 | 0.32 | 0.02 | `FOSSIL` |
| `severe_fossil` | 0.94 | 0.35 | 0.28 | 0.01 | `FOSSIL` |
| `recovering` | 0.76 | 0.55 | 0.58 | 0.12 | `HEALING` |

**Boundary conditions that need explicit tests:**

- R = 0.85 exactly → should NOT trigger fossil (threshold is `>`, not `>=`)
- R = 0.851 with C = 0.499 and X = 0.399 → must trigger fossil
- All four conditions must be true simultaneously; three of four should not trigger fossil
- `dE/dt ≈ 0` threshold must be defined and tested (what counts as "approximately zero"?)

**Additional classification tests:**
- `healthy_exploring` (R=0.58, C=0.52, X=0.68) → `EXPANSION`
- `mild_rigidity` (R=0.81, C=0.88, X=0.72) → `SUBOPTIMAL`
- `ungrounded` (R=0.68, C=0.62, X=0.35) → `UNGROUNDED`

---

### 4. Cognitive Breathing / Dynamics (`dynamics.py`)

**Breathing cycle detection:**

- Given a time series of `(C, E)` values, detect inhale vs. exhale phases
- Inhale: E increasing, C decreasing
- Exhale: C increasing, E decreasing
- Anti-correlation between C and E should yield `r ≈ -0.62` on empirical data (from README)
- A static time series (no change in E) should be flagged as "not breathing"

**Master equation integration:**

- Output state values must remain in `[0, 1]` for all valid initial conditions
- With ζ = 1.2 (empirical optimal), the system must converge to a stable fixed point
- With ζ < 1.0 (underdamped), system must exhibit oscillation
- With ζ >> 2.0 (overdamped), system must converge slowly but without oscillation

**Breathing timescales** (from `breathing_dynamics.csv`):
- τ_micro ≈ 4.38 — unit test that micro-cycle is near this value
- τ_macro ≈ 59.67 — unit test for macro-cycle
- Ratio τ_macro / τ_micro ≈ 13.62 — regression test for harmonic nesting

---

### 5. Data Integrity Tests

These tests validate that the empirical CSV files that ground the theory haven't been corrupted or accidentally modified.

**`convergence_constants.csv` regressions:**

```python
# All three systems must agree on these values
assert abs(mean_zeta - 1.2) < 0.01        # ζ ≈ 1.2
assert abs(mean_c_min - 0.657) < 0.015    # C*_min ≈ 0.657
assert abs(mean_sigma - 1.003) < 0.025    # σ ≈ 1.0
assert std_zeta < 0.01                    # Tight convergence
```

**`cross_domain_validation.csv` integrity:**

- All 13 domains are present
- `quality_correlation` values are in `[0, 1]` for all rows
- `sample_size` values are positive integers
- No domain has `optimal_coherence` outside `[0.5, 0.95]`

**`fossil_signatures.csv` integrity:**

- All 9 known states are present
- The `fossil_signature` row has R > 0.85, C < 0.50, X < 0.40

---

### 6. Integration Tests

End-to-end tests using the Quick Start example from the README:

```python
from certx import CERTXState, assess_health

state = CERTXState(
    coherence=0.68,
    entropy=0.45,
    resonance=0.72,
    temperature=0.65,
    substrate_coupling=0.70
)
diagnosis = assess_health(state)

assert diagnosis.health_state == HealthState.OPTIMAL
assert diagnosis.fossil_risk == False
assert abs(diagnosis.zeta - 1.2) < 0.1
```

**Pipeline tests:**

- State → metrics → diagnosis roundtrip produces deterministic results
- The same state always produces the same diagnosis
- Fossil remediation suggestion is present when `fossil_risk=True`

---

### 7. Edge Cases and Boundary Tests

These are the tests most likely to be skipped but most likely to expose bugs:

| Case | Why it matters |
|------|----------------|
| All dimensions at `0.5` | Neutral state — should be SUBOPTIMAL or similar |
| All dimensions at `0.0` | Degenerate state — should raise or return defined "null" health |
| All dimensions at `1.0` | Over-constrained — should flag as pathological |
| C=0.65, rest invalid | Partial validity — constructor should reject entirely |
| Entropy of `[0.5, 0.5]` | Should return `log(2) ≈ 0.693` |
| Phase array of one element | Resonance formula edge case |
| Very small `dE/dt` (1e-10) | Should it trigger fossil? Needs explicit threshold |

---

## Recommended Test Framework

**pytest** with the following plugins:

```
pytest
pytest-cov          # Coverage reporting
pytest-parametrize  # Table-driven tests for CSV-based cases
hypothesis          # Property-based testing for metric formulas
numpy               # For numerical comparisons with tolerances
```

**Coverage target:** 90%+ line coverage for `metrics.py` and `diagnosis.py` (these are the formula-heavy, error-prone modules). 80%+ for `state.py` and `dynamics.py`.

---

## Proposed Test File Structure

```
tests/
├── test_state.py          # CERTXState construction and validation
├── test_metrics.py        # C, E, R, T, X formula correctness
├── test_dynamics.py       # Breathing, oscillation, damping
├── test_diagnosis.py      # Health assessment, fossil detection
├── test_data_integrity.py # CSV validation regressions
└── test_integration.py    # End-to-end pipeline tests
```

---

## Summary of Gaps (Priority Order)

1. **Fossil detection boundary conditions** — the R/C/X thresholds are clearly defined but the `dE/dt ≈ 0` threshold is undefined. This must be specified and tested before the classifier is trustworthy.

2. **Metric formula edge cases** — division by zero in coherence (`N=0`), zero-entropy distributions, and empty arrays for resonance will crash without explicit handling.

3. **Damping ratio regression** — the ζ ≈ 1.2 result is the framework's central empirical claim. A regression test pinning this value to the measured constants prevents silent drift.

4. **Data integrity regressions** — the CSV files are the only empirical grounding. Tests that pin their values prevent accidental corruption from going unnoticed.

5. **Integration smoke test** — the Quick Start example in README should be a passing test from day one; if it doesn't run, nothing works.
