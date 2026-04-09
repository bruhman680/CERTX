# exp_004 σ_Mesh Sweep — Result 001
**Date:** 2026-03-11
**Method:** git log miner → contributor-collaboration graph → avg_clustering → σ_Mesh = 1 - r
**Commits mined per repo:** 300 (--no-merges)

## Results

| Repo | σ_Mesh | r_network | Contributors | Files | Status |
|------|--------|-----------|--------------|-------|--------|
| pallets/flask | 0.4274 | 0.5726 | 51 | 171 | ✓ healthy |
| scikit-learn/scikit-learn | 0.3260 | 0.6740 | 70 | 1915 | ✓ healthy |
| huggingface/transformers | 0.2707 | 0.7293 | 99 | 5545 | ↓ over-coupled |

Healthy range threshold: σ_Mesh ∈ [0.30, 0.50]

## Interpretation

**Flask (0.43):** Mid-healthy. Small focused codebase, deliberate governance under
Armin Ronacher. Contributors have clear domains (extensions, routing, templating)
but enough cross-pollination to cluster well. Classic "edge of order" project.

**scikit-learn (0.33):** Tight-healthy. Strong governance (SLEP process, core devs
own estimator families). High contributor count across a large codebase but clear
module ownership keeps σ_Mesh from drifting. Leans toward the governed end.

**transformers (0.27):** Over-coupled — NOT siloed. Counter-intuitive: with 5545 files
and 99 contributors, you'd expect siloing. Instead: all contributors share the same
core files (modeling_*.py, configuration_*.py, tokenization_*.py). The hub-and-spoke
architecture creates a shared core that everyone touches → high clustering → low σ_Mesh.
This is a different failure mode than siloing: it's *core congestion*.

## CERTX Prediction vs Observation

Prediction: healthy repos → σ_Mesh ∈ [0.30, 0.50]
Observation: flask ✓, sklearn ✓, transformers just below threshold

The rank order (flask > sklearn > transformers descending in σ_Mesh,
ascending in governance-tightness / core-coupling) matches qualitative
expectations derived from public knowledge of these projects.

## Anomaly Worth Tracking

transformers σ_Mesh = 0.27 is "over-coupled" in CERTX terms but the project
is demonstrably functional. This suggests the lower bound of the healthy range
(0.30) may need calibration, or that the "core congestion" failure mode has
a different σ_Mesh signature than the "tightly governed" regime.

Hypothesis: the healthy range may be architecture-dependent.
- Modular architectures (flask, sklearn): [0.30, 0.50]
- Hub-and-spoke architectures (transformers, numpy): [0.20, 0.40]

Needs more data points to confirm.

## Next Experiments

1. numpy/numpy — strong governance, hub-and-spoke. Expect 0.25–0.35.
2. Before/after transformers v2.0 — does σ_Mesh shift at major version?
3. A dead/abandoned repo — expect σ_Mesh > 0.60 (siloed commits then silence)
4. CERTX itself at v2.0 if it gains contributors — baseline σ_Mesh = 0.0 (solo)
