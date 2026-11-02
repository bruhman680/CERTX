"""Independent exact guard check. Does not import or execute repository code."""
from fractions import Fraction as F
import json


def observed_joint(true_law, epsilon=F(1, 20)):
    result = {(a, b): F(0) for a in (0, 1) for b in (0, 1)}
    for (a, b), weight in true_law.items():
        for fa in (0, 1):
            for fb in (0, 1):
                pa = epsilon if fa else 1 - epsilon
                pb = epsilon if fb else 1 - epsilon
                result[a ^ fa, b ^ fb] += weight * pa * pb
    assert sum(result.values()) == 1
    return result


def main():
    # IND: independent Bernoulli(1/5).
    # DIFF: half easy (both correct), half hard with independent errors p=2/5.
    # COMMON/COPY: the same Bernoulli(1/5) latent flag shared by both answerers.
    laws = {
        "IND": {(0, 0): F(16, 25), (0, 1): F(4, 25),
                (1, 0): F(4, 25), (1, 1): F(1, 25)},
        "DIFF": {(0, 0): F(17, 25), (0, 1): F(3, 25),
                 (1, 0): F(3, 25), (1, 1): F(2, 25)},
        "COMMON_COPY": {(0, 0): F(4, 5), (1, 1): F(1, 5)},
    }
    rows = {}
    conditional = {}
    for world, law in laws.items():
        obs = observed_joint(law)
        marginal_a = obs[1, 0] + obs[1, 1]
        marginal_b = obs[0, 1] + obs[1, 1]
        joint = obs[1, 1]
        assert marginal_a == marginal_b == F(23, 100)
        conditional[world] = joint / marginal_a
        # Independently compare the enumeration with the expanded formula.
        formula = F(1, 20) ** 2 + 2 * F(1, 20) * F(9, 10) * F(1, 5)
        formula += F(9, 10) ** 2 * law[1, 1]
        assert joint == formula
        rows[world] = {
            "true_joint": str(law[1, 1]),
            "observed_marginal": str(marginal_a),
            "observed_joint": str(joint),
            "observed_joint_decimal": float(joint),
            "conditional_exact": str(conditional[world]),
            "conditional_decimal": float(conditional[world]),
        }
    midpoint = (conditional["DIFF"] + conditional["COMMON_COPY"]) / 2
    assert conditional["DIFF"] == F(853, 2300)
    assert conditional["COMMON_COPY"] == F(73, 92)
    assert midpoint == F(1339, 2300)
    result = {
        "scope": "exact population conditional probabilities; no Monte Carlo or branch script execution",
        "source_commit": "b82724c2427151d38f5d0c45cd7cc87e9359565a",
        "epsilon": "1/20 independent symmetric flips per answerer",
        "parameters_decimal": {"p": 0.2, "joint_DIFF": 0.08, "joint_COMMON_COPY": 0.2,
                               "epsilon": 0.05, "q": 0.23},
        "worlds": rows,
        "diff_common_midpoint_exact": str(midpoint),
        "diff_common_midpoint_decimal": float(midpoint),
        "implemented_threshold": "3/5",
        "threshold_between_population_conditionals": conditional["DIFF"] < F(3, 5) < conditional["COMMON_COPY"],
        "does_not_verify": ["finite-sample ratio expectations", "guard firing rates", "reported Monte Carlo outputs", "unknown-world robustness"],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
