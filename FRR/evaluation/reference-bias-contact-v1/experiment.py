#!/usr/bin/env python3
"""Execute the prospectively specified, deterministic RB-C1/2/3 grid once.

Exact arithmetic is used for every decision. See PROTOCOL.md and SCHEMA.md.
The caller is responsible for preserving pre-run hashes and execution logs.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import json
from math import sqrt
from pathlib import Path

PROBES = {
    "CONTEXT": (F(-1), F(1)),
    "WEAK": (F(9, 10), F(1)),
    "SIGNAL": (F(1), F(-1)),
    "COPY": (F(1), F(1)),
}
BIASES = {
    "ZERO": (F(0), F(0)),
    "COMMON": (F(3, 25), F(3, 25)),
    "OPPOSED": (F(3, 25), F(-3, 25)),
}
CONTRACTS = ("BLIND", "WIDE", "REFERENCE", "BAD_REFERENCE")
RHOS = (F(1, 2), F(1), F(2))
RAW_BUDGET = F(1, 10)


def interval(lower, upper):
    return {"lower": lower, "upper": upper}


def contains(bounds, value):
    return bounds["lower"] <= value <= bounds["upper"]


def build_row(probe, bias, alpha, beta, bias_a, bias_b, contract, rho):
    ya, yb = alpha + bias_a, beta + bias_b
    if contract == "BLIND":
        radius, ra, rb, extra = F(1, 50), None, None, 0
        assumption = "Each primary-role bias lies in [-1/50, 1/50]."
    elif contract == "WIDE":
        radius, ra, rb, extra = F(3, 20), None, None, 0
        assumption = "Each primary-role bias lies in [-3/20, 3/20]."
    elif contract == "REFERENCE":
        radius, ra, rb, extra = F(1, 100), bias_a, bias_b, 2
        assumption = "Role-specific transported bias references each have absolute error at most 1/100."
    elif contract == "BAD_REFERENCE":
        radius, ra, rb, extra = F(1, 100), F(0), F(0), 2
        assumption = "Declared zero bias references each have absolute error at most 1/100; invalid for nonzero biases."
    else:
        raise ValueError(contract)
    ca, cb = ra if ra is not None else F(0), rb if rb is not None else F(0)
    bias_ia, bias_ib = interval(ca - radius, ca + radius), interval(cb - radius, cb + radius)
    ia = interval(ya - bias_ia["upper"], ya - bias_ia["lower"])
    ib = interval(yb - bias_ib["upper"], yb - bias_ib["lower"])
    gap = interval(ib["lower"] - ia["upper"], ib["upper"] - ia["lower"])
    nonempty = ia["lower"] <= ia["upper"] and ib["lower"] <= ib["upper"]
    excludes_zero = gap["lower"] > 0 or gap["upper"] < 0
    gate = nonempty and excludes_zero
    ahat, bhat = ya - ca, yb - cb
    g, h = beta - alpha, bhat - ahat
    da, db = ahat - alpha, bhat - beta
    covers_a, covers_b = contains(ia, alpha), contains(ib, beta)
    coverage = covers_a and covers_b
    ea = max(abs(ahat - ia["lower"]), abs(ahat - ia["upper"]))
    eb = max(abs(bhat - ib["lower"]), abs(bhat - ib["upper"]))
    available = h != 0
    error_sq = ((da * rho) ** 2 + db ** 2) / h ** 2 if available else None
    envelope_sq = ((ea * rho) ** 2 + eb ** 2) / h ** 2 if available else None
    envelope_holds = error_sq <= envelope_sq if available else None
    actual_budget = error_sq <= RAW_BUDGET ** 2 if available else None
    raw_certified = gate and available and envelope_sq <= RAW_BUDGET ** 2
    if coverage and available:
        assert envelope_holds, "Conditional envelope failed under coefficient coverage"
    assert not gate or available, "A passing gate must permit the centered point inversion"
    return {
        "row_id": f"{probe}:{bias}:{contract}:rho={rho}",
        "probe": probe, "bias_case": bias, "contract": contract, "rho": rho,
        "world": {"world_id": f"{probe}:{bias}", "alpha": alpha, "beta": beta,
                  "bias_a": bias_a, "bias_b": bias_b, "true_gap": g,
                  "true_nonsingular": g != 0, "orthogonal_n_s": True,
                  "signal_norm": F(1), "nuisance_norm": rho},
        "observations": {"y_a": ya, "y_b": yb, "r_a": ra, "r_b": rb},
        "method": {"assumption": assumption, "declared_radius": radius,
                   "primary_scalar_measurements": 2, "extra_scalar_measurements": extra,
                   "total_scalar_measurements": 2 + extra,
                   "reference_role_authority_supplied": extra == 2,
                   "declared_bias_intervals": {"a": bias_ia, "b": bias_ib},
                   "actual_bias_contract_valid": contains(bias_ia, bias_a) and contains(bias_ib, bias_b)},
        "coefficient_intervals": {"a": ia, "b": ib}, "compatible_gap_interval": gap,
        "coverage": {"a": covers_a, "b": covers_b, "both": coverage,
                     "true_gap": contains(gap, g)},
        "gate": {"intervals_nonempty": nonempty, "gap_strictly_excludes_zero": excludes_zero,
                 "status": "PASS" if gate else "WITHHOLD",
                 "reason": "gap_excludes_zero" if gate else ("empty_intervals" if not nonempty else "gap_contains_zero")},
        "point": {"alpha_hat": ahat, "beta_hat": bhat, "h": h, "delta_a": da, "delta_b": db,
                  "available": available, "offered": gate and available,
                  "unavailable_reason": None if available else "zero_point_gap",
                  "nuisance_coefficient": -da / h if available else None,
                  "signal_gain": (g - da) / h if available else None,
                  "relative_error_squared": error_sq,
                  "relative_error_sqrt_display": sqrt(error_sq) if available else None},
        "envelope": {"conditional_on": ["coefficient_coverage", "orthogonality", "known_norm_ratio"],
                     "error_radius_a": ea, "error_radius_b": eb, "available": available,
                     "relative_error_squared_upper_bound": envelope_sq,
                     "relative_error_sqrt_upper_bound_display": sqrt(envelope_sq) if available else None,
                     "actual_error_within_envelope": envelope_holds,
                     "condition_satisfied": coverage},
        "raw_budget": {"relative_error_limit": RAW_BUDGET, "squared_limit": RAW_BUDGET ** 2,
                       "actual_point_meets_budget": actual_budget, "raw_certified": raw_certified,
                       "false_raw_certificate": raw_certified and actual_budget is False},
    }


def counts(rows):
    return {
        "rows": len(rows),
        "coefficient_coverage": sum(r["coverage"]["both"] for r in rows),
        "actual_bias_contract_valid": sum(r["method"]["actual_bias_contract_valid"] for r in rows),
        "gate_pass": sum(r["gate"]["status"] == "PASS" for r in rows),
        "gate_withhold": sum(r["gate"]["status"] == "WITHHOLD" for r in rows),
        "empty_intervals": sum(not r["gate"]["intervals_nonempty"] for r in rows),
        "true_nonsingular": sum(r["world"]["true_nonsingular"] for r in rows),
        "true_nonsingular_withheld": sum(r["world"]["true_nonsingular"] and r["gate"]["status"] == "WITHHOLD" for r in rows),
        "true_singular_gate_pass": sum(not r["world"]["true_nonsingular"] and r["gate"]["status"] == "PASS" for r in rows),
        "point_available": sum(r["point"]["available"] for r in rows),
        "point_unavailable": sum(not r["point"]["available"] for r in rows),
        "point_offered": sum(r["point"]["offered"] for r in rows),
        "exact_point_recovery": sum(r["point"]["available"] and r["point"]["relative_error_squared"] == 0 for r in rows),
        "conditional_envelope_checks": sum(r["coverage"]["both"] and r["point"]["available"] for r in rows),
        "conditional_envelope_violations": sum(r["coverage"]["both"] and r["point"]["available"] and not r["envelope"]["actual_error_within_envelope"] for r in rows),
        "uncovered_envelope_violations": sum(not r["coverage"]["both"] and r["point"]["available"] and not r["envelope"]["actual_error_within_envelope"] for r in rows),
        "actual_point_meets_raw_budget": sum(r["raw_budget"]["actual_point_meets_budget"] is True for r in rows),
        "raw_certified": sum(r["raw_budget"]["raw_certified"] for r in rows),
        "false_raw_certificates": sum(r["raw_budget"]["false_raw_certificate"] for r in rows),
    }


def ambiguous_worlds():
    # These diagnostic rows are separate from the fixed 144-row main grid.
    worlds = [
        ("OBSERVED_COPY", F(1), F(1), F(3, 25), F(-3, 25)),
        ("ALTERNATIVE", F(28, 25), F(22, 25), F(0), F(0)),
    ]
    detail = []
    for name, a, b, ba, bb in worlds:
        detail.append({"label": name, "alpha": a, "beta": b, "bias_a": ba, "bias_b": bb,
                       "true_gap": b - a, "true_nonsingular": a != b,
                       "y_a": a + ba, "y_b": b + bb,
                       "contract_diagnostics_at_rho_one": [build_row(name, "AMBIGUITY", a, b, ba, bb, c, F(1)) for c in CONTRACTS]})
    assert detail[0]["y_a"] == detail[1]["y_a"] and detail[0]["y_b"] == detail[1]["y_b"]
    assert detail[0]["true_nonsingular"] != detail[1]["true_nonsingular"]
    return {"included_in_main_grid_counts": False, "worlds": detail,
            "primary_observations_identical": True,
            "valid_reference_observations_differ": True,
            "interpretation": "The two scalar primary readings alone do not identify singularity. With the same fixed orthogonal n and s, these worlds have different Dprime vectors; full-vector observational equivalence is not claimed. Valid references distinguish the scalar worlds through supplied role authority, transport and error assumptions."}


def exact_json(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {key: exact_json(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [exact_json(item) for item in value]
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("run"))
    args = parser.parse_args()
    # Refuse to overwrite any earlier execution's result artifacts.
    args.output.mkdir(parents=True, exist_ok=True)
    paths = [args.output / "ROWS.json", args.output / "SUMMARY.json"]
    if any(path.exists() for path in paths):
        raise FileExistsError("Result artifact already exists; preserve the original execution before diagnosing or repairing.")
    rows = [build_row(probe, bias, a, b, ba, bb, contract, rho)
            for probe, (a, b) in PROBES.items()
            for bias, (ba, bb) in BIASES.items()
            for contract in CONTRACTS for rho in RHOS]
    assert len(rows) == 144 and len({r["row_id"] for r in rows}) == 144
    assert Counter(r["contract"] for r in rows) == {c: 36 for c in CONTRACTS}
    assert Counter(r["world"]["world_id"] for r in rows) == {f"{p}:{b}": 12 for p in PROBES for b in BIASES}
    # Enforce identical primary evidence across all methods and norm ratios.
    for world in {r["world"]["world_id"] for r in rows}:
        shared = {(r["observations"]["y_a"], r["observations"]["y_b"])
                  for r in rows if r["world"]["world_id"] == world}
        assert len(shared) == 1
    summary = {
        "study": "RB-C1/2/3 reference-bias-contact-v1", "authored_exact_toy": True,
        "independent_repetitions": 0, "probability_claims": False,
        "grid": {"probes": list(PROBES), "biases": list(BIASES), "contracts": list(CONTRACTS),
                 "rho_values": RHOS, "distinct_coefficient_bias_worlds": 12, "rows": 144},
        "raw_budget": {"relative_error_limit": RAW_BUDGET, "squared_limit": RAW_BUDGET ** 2},
        "totals": counts(rows),
        "by_contract": {c: counts([r for r in rows if r["contract"] == c]) for c in CONTRACTS},
        "by_probe": {p: counts([r for r in rows if r["probe"] == p]) for p in PROBES},
        "by_bias": {b: counts([r for r in rows if r["bias_case"] == b]) for b in BIASES},
        "by_rho": {str(rho): counts([r for r in rows if r["rho"] == rho]) for rho in RHOS},
        "by_contract_and_bias": {c: {b: counts([r for r in rows if r["contract"] == c and r["bias_case"] == b]) for b in BIASES} for c in CONTRACTS},
        "ambiguous_worlds": ambiguous_worlds(),
        "scope": "Counts describe the fixed authored grid, not frequencies from independent trials. Contracts and references are supplied assumptions. No semantic-role, general verification, retrieval, or behavioral improvement claim.",
    }
    # Fixed prospective counts independently derived from the declared grid.
    expected_totals = {
        "rows": 144, "coefficient_coverage": 96, "gate_pass": 105,
        "gate_withhold": 39, "empty_intervals": 0, "true_nonsingular": 108,
        "true_nonsingular_withheld": 9, "true_singular_gate_pass": 6,
        "point_available": 117, "point_unavailable": 27,
        "conditional_envelope_violations": 0,
    }
    for key, expected in expected_totals.items():
        assert summary["totals"][key] == expected, (key, summary["totals"][key], expected)
    for path, data in zip(paths, (rows, summary)):
        with path.open("x", encoding="utf-8") as handle:
            json.dump(exact_json(data), handle, indent=2, sort_keys=True, allow_nan=False)
            handle.write("\n")
    print(json.dumps({"rows": len(rows), "output": str(args.output), "totals": summary["totals"]}, sort_keys=True))


if __name__ == "__main__":
    main()
