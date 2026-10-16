#!/usr/bin/env python3
"""New Prony toy, NOT reproduction of missing Claude erase_gate.py.

Predictions before running:
  * c0*c2-c1**2 = F*P*(a-b)**2 in exact laws.
  * Four noiseless points recover nonzero separated components, unordered.
  * Collision identifies only their sum, not individual amplitudes.
  * Finite-noise fitting may fail or return nonphysical components. Report all.
Carrier labels below are stipulated by sorted decay rates, not discovered.
Noise construction: two independent binomials, each N trials per k, with
p_plus=(1+c_k)/2 and p_minus=(1-c_k)/2. Their difference estimates c_k.
No intervention selectivity or environmental-memory mechanism is simulated.
"""
import json
from pathlib import Path
import numpy as np

F, P, A = 0.128, 0.06, 0.95
GAPS = (0.8, 0.5, 0.2, 0.05, 0.01, 0.0)
N, REPS, SEED = 200_000, 50, 20261016


def fit(c):
    c = np.asarray(c, dtype=float)
    determinant = float(c[0] * c[2] - c[1] ** 2)
    if abs(determinant) < 1e-14:
        return {"status": "degenerate", "determinant": determinant}
    try:
        total_rate, product_rate = np.linalg.solve(
            [[c[1], -c[0]], [c[2], -c[1]]], c[2:4])
        roots = np.roots([1.0, -total_rate, product_rate])
    except np.linalg.LinAlgError:
        return {"status": "singular", "determinant": determinant}
    if np.any(np.abs(roots.imag) > 1e-9):
        return {"status": "complex_rates", "determinant": determinant}
    rates = np.sort(roots.real)[::-1]
    try:
        amplitudes = np.linalg.solve([[1.0, 1.0], rates], c[:2])
    except np.linalg.LinAlgError:
        return {"status": "singular", "determinant": determinant}
    if not np.all(np.isfinite(np.r_[rates, amplitudes])):
        status = "nonfinite"
    elif np.any((rates < 0) | (rates > 1)):
        status = "rates_outside_unit_interval"
    elif np.any(amplitudes < 0) or amplitudes.sum() > 1:
        status = "nonphysical_amplitudes"
    else:
        status = "valid"
    return {"status": status, "determinant": determinant,
            "rates_descending": rates.tolist(), "amplitudes": amplitudes.tolist()}


def main():
    rng = np.random.default_rng(SEED)
    records = []
    exact = []
    for gap in GAPS:
        b = A - gap
        c = F * A ** np.arange(4) + P * b ** np.arange(4)
        result = fit(c)
        expected = F * P * gap ** 2
        np.testing.assert_allclose(c[0]*c[2]-c[1]**2, expected, atol=1e-16)
        if gap:
            assert result["status"] == "valid", result
            np.testing.assert_allclose(result["rates_descending"], [A, b], atol=1e-9)
            np.testing.assert_allclose(result["amplitudes"], [F, P], atol=1e-9)
        else:
            assert result["status"] == "degenerate"
            np.testing.assert_allclose(c, (F+P)*A**np.arange(4), atol=1e-16)
        exact.append({"gap": gap, "true_law": c.tolist(),
                      "expected_determinant": expected, "fit": result})
        for rep in range(REPS):
            plus = rng.binomial(N, (1+c)/2) / N
            minus = rng.binomial(N, (1-c)/2) / N
            measured = plus-minus
            result = fit(measured)
            if result["status"] == "valid":
                result["abs_slow_amplitude_error"] = abs(result["amplitudes"][0]-F)
            records.append({"gap": gap, "replicate": rep,
                            "measured_contrasts": measured.tolist(), "fit": result})
    summaries = []
    for gap in GAPS:
        fits = [r["fit"] for r in records if r["gap"] == gap]
        counts = {s: sum(f["status"] == s for f in fits)
                  for s in sorted({f["status"] for f in fits})}
        valid = [f for f in fits if f["status"] == "valid"]
        summaries.append({"gap": gap, "status_counts": counts,
                          "valid_n": len(valid), "total_n": REPS,
                          "median_abs_slow_amplitude_error_conditional_valid":
                          float(np.median([f["abs_slow_amplitude_error"] for f in valid]))
                          if valid else None})
    output = {"kind": "new constructed inverse-problem audit; not relay replication",
              "parameters": {"F": F, "P": P, "a": A, "gaps": GAPS,
                             "trials_per_arm_per_k": N, "replicates": REPS, "seed": SEED},
              "label_assumption": "slow component called F by stipulation; rate order is not carrier evidence",
              "noise_model": "independent Binomial(N,(1+c)/2)/N - Binomial(N,(1-c)/2)/N",
              "exact_checks": exact, "summaries": summaries, "sampled_fits": records}
    path = Path(__file__).resolve().parents[1] / "evaluation/results/relay-prony-audit.json"
    path.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(summaries, indent=2))


if __name__ == "__main__":
    main()
