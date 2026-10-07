"""A minimal reproducible probe of an agent with two reinforced route choices.

This is a choice process, not a simulation of a general graph.  The field on
each route decays by gamma and receives w when that route is chosen.  The agent
uses softmax(beta * field) at each choice and has no other persistent state.
"""

from math import exp, tanh
from random import Random


def p_first(z, beta):
    return 1.0 / (1.0 + exp(-beta * z))


def mean_field_fixed_difference(gamma, w, beta):
    if gamma + w * beta / 2.0 <= 1.0:
        return 0.0
    # The positive nonzero branch solves (1-gamma) z = w tanh(beta z/2).
    lo, hi = 1e-12, w / (1.0 - gamma)
    for _ in range(100):
        mid = (lo + hi) / 2.0
        if (gamma - 1.0) * mid + w * tanh(beta * mid / 2.0) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def stochastic_run(gamma, w, beta, steps=200_000, seed=1005):
    random = Random(seed)
    z = 0.0
    choices = [0, 0]
    sign_switches = 0
    previous_sign = 0
    for _ in range(steps):
        choice = 0 if random.random() < p_first(z, beta) else 1
        choices[choice] += 1
        z = gamma * z + (w if choice == 0 else -w)
        sign = 1 if z > 0 else -1 if z < 0 else 0
        if previous_sign and sign != previous_sign:
            sign_switches += 1
        previous_sign = sign
    return choices, sign_switches, z


if __name__ == "__main__":
    beta, w = 2.0, 0.2
    print(f"beta={beta}, w={w}, mean-field gamma_c={1 - w * beta / 2:.3f}")
    for gamma in (0.7, 0.8, 0.9):
        fixed_z = mean_field_fixed_difference(gamma, w, beta)
        choices, switches, final_z = stochastic_run(gamma, w, beta)
        print(
            f"gamma={gamma:.1f}: mean-field z*={fixed_z:.6f}; "
            f"stochastic choices={choices}; sign switches={switches}; "
            f"final z={final_z:.6f}; route probability floor "
            f">= {p_first(-w / (1 - gamma), beta):.8f}"
        )
