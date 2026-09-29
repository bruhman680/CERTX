#!/usr/bin/env python3
"""Eight-state sandbox for three distinct projections of one Markov process.

The binary coordinates are mathematical handles, not empirical CERTX fibers.
Rows are source states; distributions are row vectors.
"""

from itertools import product

import numpy as np


STATES = list(product((0, 1), repeat=3))
DRIVER = (1, 2, 0)  # each coordinate can depend on a different hidden bit


def transition(coupling, inertia=0.2):
    """Build a stochastic 8x8 matrix with independently tunable defects."""
    P = np.zeros((8, 8))
    for i, source in enumerate(STATES):
        prob_one = [
            0.5 + inertia * (source[k] - 0.5)
            + coupling[k] * (source[DRIVER[k]] - 0.5)
            for k in range(3)
        ]
        if not all(0 <= p <= 1 for p in prob_one):
            raise ValueError("Transition probabilities must lie in [0, 1]")
        for j, target in enumerate(STATES):
            P[i, j] = np.prod([
                prob_one[k] if target[k] else 1 - prob_one[k]
                for k in range(3)
            ])
    assert np.allclose(P.sum(axis=1), 1)
    return P


def projection(coordinates):
    """Hard projection onto one or more binary coordinates."""
    labels = [tuple(s[k] for k in coordinates) for s in STATES]
    distinct = sorted(set(labels))
    return np.array([[float(label == value) for value in distinct]
                     for label in labels])


def defect(P, Q, horizon=1):
    """Maximum TV between projected futures of states merged by Q.

    Zero at horizon 1 is strong lumpability for a hard partition. At longer
    horizons this measures a narrower marginal-future question, not the full
    visible path law or response to interventions.
    """
    visible = np.linalg.matrix_power(P, horizon) @ Q
    labels = np.argmax(Q, axis=1)
    return max(
        0.5 * np.abs(visible[i] - visible[j]).sum()
        for i in range(8) for j in range(i + 1, 8)
        if labels[i] == labels[j]
    )


def evaluate(name, coupling):
    P = transition(coupling)
    defects = np.array([defect(P, projection((k,))) for k in range(3)])
    scores = 1 - defects  # illustrative normalization for this toy only
    return {
        "case": name,
        "coupling": list(coupling),
        "defect_t1": defects.tolist(),
        "defect_t2": [defect(P, projection((k,)), 2) for k in range(3)],
        "score_t1": scores.tolist(),
        "minimum": float(scores.min()),
        "mean": float(scores.mean()),
        "spread_population": float(scores.std()),
    }


def main():
    import json

    cases = {
        "all_exact": (0, 0, 0),
        "only_projection_0_fails": (0.4, 0, 0),
        "only_projection_1_fails": (0, 0.4, 0),
        "only_projection_2_fails": (0, 0, 0.4),
        "one_approximate": (0.05, 0, 0),
        "all_fail_equally": (0.4, 0.4, 0.4),
    }
    results = [evaluate(name, c) for name, c in cases.items()]
    for result in results:
        assert np.allclose(result["defect_t1"], result["coupling"])
    assert defect(transition((0.4, 0, 0)), projection((0, 1))) < 1e-12
    assert results[0]["spread_population"] == 0
    assert results[-1]["spread_population"] < 1e-12
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
