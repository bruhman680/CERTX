"""Exact finite-state checks for the eight-state noisy parity register.

State S_t = (x_t, x_(t-1), x_(t-2)); transition
x_(t+1) = x_t XOR x_(t-1) XOR x_(t-2) XOR eta_t,
eta_t ~ Bernoulli(epsilon). Observation is the current bit x_t.
"""
import json
import itertools
import math
from fractions import Fraction


STATES = list(itertools.product((0, 1), repeat=3))
INDEX = {s: i for i, s in enumerate(STATES)}


def transition(eps=Fraction(1, 10)):
    n = len(STATES)
    P = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i, (a, b, c) in enumerate(STATES):
        parity = a ^ b ^ c
        for noise, prob in ((0, 1 - eps), (1, eps)):
            j = INDEX[(parity ^ noise, a, b)]
            P[i][j] += prob
    return P


def matmul(A, B):
    n = len(A)
    return [[sum((A[i][k] * B[k][j] for k in range(n)), Fraction(0))
             for j in range(n)] for i in range(n)]


def defect(M):
    groups = {0: [i for i, s in enumerate(STATES) if s[0] == 0],
              1: [i for i, s in enumerate(STATES) if s[0] == 1]}
    max_defect = Fraction(0)
    witnesses = []
    for a in (0, 1):
        for i, j in itertools.combinations(groups[a], 2):
            pi = sum((M[i][k] for k in groups[1]), Fraction(0))
            pj = sum((M[j][k] for k in groups[1]), Fraction(0))
            d = abs(pi - pj)  # TV distance of binary projected distributions
            if d > max_defect:
                max_defect, witnesses = d, [(STATES[i], STATES[j])]
            elif d == max_defect and d:
                witnesses.append((STATES[i], STATES[j]))
    return max_defect, witnesses


def binary_entropy(p):
    return -p * math.log2(p) - (1-p) * math.log2(1-p) if 0 < p < 1 else 0.


def run(max_horizon=12):
    eps = Fraction(1, 10)
    P = transition(eps)
    assert all(sum(row) == 1 for row in P)
    assert all(sum(P[i][j] for i in range(8)) == 1 for j in range(8)), "Not doubly stochastic"
    # A uniform stationary distribution follows from double stochasticity.
    M = [[Fraction(int(i == j)) for j in range(8)] for i in range(8)]
    horizons = []
    for t in range(1, max_horizon + 1):
        M = matmul(M, P)
        d, w = defect(M)
        horizons.append({"t": t, "max_projected_tv": float(d), "exact": str(d),
                         "witness": [list(w[0][0]), list(w[0][1])] if w else None})
    # With stationary uniform independent initial triple, b/c are independent
    # fair bits conditioned on current a. The next bit is fair until both are
    # supplied; then it matches parity with probability 0.9.
    Hnoise = binary_entropy(float(eps))
    result = {
        "epsilon": float(eps),
        "states": 8,
        "doubly_stochastic": True,
        "stationary_distribution": [1/8] * 8,
        "current_only_bayes_accuracy": .5,
        "current_plus_one_prior_bayes_accuracy": .5,
        "current_plus_two_priors_bayes_accuracy": .9,
        "conditional_entropy_next_given_current_bits": 1.0,
        "conditional_entropy_next_given_last_three_bits": Hnoise,
        "additional_predictive_mutual_information_bits": 1 - Hnoise,
        "horizon_defects": horizons,
    }
    assert horizons[0]["exact"] == "4/5"
    return result


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
