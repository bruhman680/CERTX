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


def target_defect(P, grouping, observable, horizon=1):
    """Maximum TV between target futures of states merged by grouping.

    Keeping the observable fixed makes refinement comparisons meaningful.
    If the observable is refined too, more distinctions become measurable and
    the defect may increase even while the grouping gets finer.
    """
    visible = np.linalg.matrix_power(P, horizon) @ observable
    labels = np.argmax(grouping, axis=1)
    pairs = [
        (i, j) for i in range(8) for j in range(i + 1, 8)
        if labels[i] == labels[j]
    ]
    return max((0.5 * np.abs(visible[i] - visible[j]).sum()
                for i, j in pairs), default=0.0)


def defect(P, Q, horizon=1):
    """Maximum TV between projected futures of states merged by Q.

    Zero at horizon 1 is strong lumpability for a hard partition. At longer
    horizons this measures a narrower marginal-future question, not the full
    visible path law or response to interventions.
    """
    return target_defect(P, Q, Q, horizon)


def joint_only_chain():
    """Each binary coordinate is exact, but the (0,1) joint is not.

    Given source bit c, the next two bits have parity c. Each individual
    target bit is fair, and the third target bit is also fair.
    """
    P = np.zeros((8, 8))
    for i, (_, _, c) in enumerate(STATES):
        for j, (a_next, b_next, _) in enumerate(STATES):
            if (a_next ^ b_next) == c:
                P[i, j] = 0.25
    assert np.allclose(P.sum(axis=1), 1)
    return P


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
    P_joint = joint_only_chain()
    local = [defect(P_joint, projection((k,))) for k in range(3)]
    joint = defect(P_joint, projection((0, 1)))
    assert np.allclose(local, 0) and np.isclose(joint, 1)
    P_one = transition((0.4, 0, 0))
    fixed_target_refinement = {
        "coarse": target_defect(P_one, projection((0,)), projection((0,))),
        "refined": target_defect(P_one, projection((0, 1)), projection((0,))),
    }
    assert np.isclose(fixed_target_refinement["coarse"], 0.4)
    assert np.isclose(fixed_target_refinement["refined"], 0)
    print(json.dumps({
        "independent_projection_cases": results,
        "joint_only_case": {
            "individual_defects": local,
            "joint_01_defect": joint,
            "joint_01_defect_t2": defect(P_joint, projection((0, 1)), 2),
        },
        "fixed_target_refinement": fixed_target_refinement,
    }, indent=2))


if __name__ == "__main__":
    main()
