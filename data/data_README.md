# CERTX Data Directory

Empirical datasets supporting the CERTX framework.

---

## Files

### convergence_constants.csv

Cross-platform convergence evidence for fundamental constants.

| Column | Description |
|--------|-------------|
| system | AI system (Claude, Gemini, DeepSeek) |
| methodology | Derivation approach |
| zeta_optimal | Optimal damping ratio |
| c_optimal_min/max | Optimal coherence range |
| sigma_branching | Semantic branching ratio |

**Key Finding:** Independent systems converged on ζ ≈ 1.2, C* ≈ 0.65-0.70 with p < 0.001.

---

### cross_domain_validation.csv

Coherence-quality correlations across 13 domains.

| Column | Description |
|--------|-------------|
| domain | Application area |
| optimal_coherence | Best-performing C value |
| quality_correlation | Pearson r with quality metric |
| sample_size | Number of observations |

**Key Finding:** Universal optimal range C* ≈ 0.58-0.90, domain-adaptive.

---

### breathing_dynamics.csv

Empirical measurements from 40,000+ cognitive processing cycles.

| Column | Description |
|--------|-------------|
| metric | Measurement name |
| value | Observed value |
| unit | Unit of measurement |
| notes | Context |

**Key Finding:** τ_micro ≈ 4.38, τ_macro ≈ 59.67, ratio ≈ 13.62 (harmonic nesting).

---

### fossil_signatures.csv

CERTX signatures for various cognitive states.

| Column | Description |
|--------|-------------|
| state | Descriptive state name |
| resonance/coherence/substrate_coupling | CERTX values |
| entropy_rate | dE/dt approximation |
| classification | Health category |
| domain_example | Real-world manifestation |

**Key Finding:** Fossil signature = R > 0.85, C < 0.50, X < 0.40, dE/dt ≈ 0.

---

### learning_loop_phases.csv

Six-phase cycle mapping to respiratory dynamics.

| Column | Description |
|--------|-------------|
| phase | Loop phase name |
| breath_mapping | Corresponding breath phase |
| primary_variable | Main CERTX variable affected |
| direction | Change direction |
| function | Cognitive purpose |
| duration_fraction | Typical fraction of cycle |

---

## Usage

```python
import pandas as pd

# Load convergence data
convergence = pd.read_csv('data/convergence_constants.csv')

# Check cross-platform agreement
print(f"Mean ζ: {convergence['zeta_optimal'].mean():.3f}")
print(f"StdDev: {convergence['zeta_optimal'].std():.4f}")

# Load domain validation
domains = pd.read_csv('data/cross_domain_validation.csv')

# Find highest correlation domain
best = domains.loc[domains['quality_correlation'].idxmax()]
print(f"Strongest validation: {best['domain']} (r={{best['quality_correlation']:.3f}})")
```

---

## Citation

When using this data, please cite:

```bibtex
@dataset{certx_data2025,
  title={CERTX Empirical Validation Data},
  year={2025},
  url={https://github.com/bruhman680/CERTX/tree/main/data}
}
```

---

## Contributing

Additional validation data welcome. Please ensure:

1. Clear methodology documentation
2. Sample sizes reported
3. Statistical significance calculated
4. Domain and context specified

Submit via pull request with data and documentation.
