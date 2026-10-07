"""Local counterexamples and snippet diagnostics, not a full engine test.

Uses constructed data and manually isolated formulas from canon batch 2.
Does not execute attachment code or validate reported neural experiments.
"""
import json
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def entropy(values):
    counts = Counter(values)
    return -sum((n / len(values)) * math.log2(n / len(values))
                for n in counts.values())


def mutual_information(x, y):
    return entropy(x) + entropy(y) - entropy(list(zip(x, y)))


def main():
    results = []

    # Residual f(h)=-h cancels h. Fair binary input avoids continuous MI issues.
    x = [0, 1]
    y = [h + (-h) for h in x]
    before = mutual_information(x, x)
    after = mutual_information(x, y)
    assert before == 1 and after == 0
    results.append(dict(id='residual_information', before_bits=before,
                        after_bits=after, status='unconditional claim contradicted'))

    # Five-dimensional update A=1.1*I passes the proposed eigenvalue band.
    gain = 1.1
    value = gain ** 100
    assert 0.8 <= gain <= 1.2 and value > 10000
    results.append(dict(id='eigenvalue_band', eigenvalue=gain,
                        initial_coordinate=1, coordinate_after_100_steps=value,
                        status='band does not guarantee discrete-time stability'))

    # A constant graph signal has minimum Dirichlet energy but no separation.
    constant = [0, 0, 0]
    separated = [0, 1, 2]
    energy = lambda f: sum((f[i] - f[j]) ** 2 for i, j in [(0, 1), (1, 2)])
    assert energy(constant) == 0 and energy(separated) == 2
    results.append(dict(id='dirichlet_collapse', constant_energy=0,
                        separated_energy=2, status='smoothness alone cannot certify meaning'))

    # Unmasked finite-logit softmax has positive entries, though some are small.
    weights = [math.exp(z) for z in [0, -10, -20]]
    probabilities = [w / sum(weights) for w in weights]
    assert all(p > 0 for p in probabilities)
    results.append(dict(id='softmax_support', probabilities=probabilities,
                        exact_nonzero_fraction=1,
                        status='near-zero and exact-zero sparsity differ'))

    # Literal formula from the claimed sparsity/conductance table.
    rows = [(512, 0, 512, 512), (256, .5, 256, 181),
            (128, .75, 128, 90), (64, .875, 64, 45),
            (32, .9375, 32, 23)]
    comparison = [dict(k=k, formula=math.sqrt(1-s)*n, printed=printed)
                  for k, s, n, printed in rows]
    assert math.isclose(comparison[-1]['formula'], 8)
    assert comparison[-1]['printed'] == 23
    results.append(dict(id='conductance_arithmetic', rows=comparison,
                        status='printed formula column inconsistent with listed inputs'))

    # The supplied SSCG-inspired predictor multiplies current level by a rate.
    predict = lambda c, t: min(c * ({0: 1.1, 1: 2.5, 2: 10, 3: 1000}.get(int(c), 1.1) ** t), 3)
    assert predict(0, 5) == 0 and predict(1, 5) == 3 and predict(2, 5) == 3
    results.append(dict(id='sscg_predictor', zero_after_5=predict(0, 5),
                        one_after_5=predict(1, 5), two_after_5=predict(2, 5),
                        status='heuristic saturates; no validated growth forecast'))

    # Truth of the tuple is not truth of its first field.
    assert bool((False, None)) is True
    results.append(dict(id='loop_tuple', detection=False,
                        caller_condition=bool((False, None)),
                        status='shown caller would enter loop handler even with no detection'))

    # Python iterates over appended children too; bounded reproduction shows it.
    population = [0]
    visits = 0
    for candidate in population:
        visits += 1
        if len(population) < 20:
            population.append(candidate + 1)
    assert visits == 20
    results.append(dict(id='live_list_growth', initial_population=1,
                        diagnostic_cap=20, visits=visits,
                        status='persistent spawn predicate can extend the same iteration without bound'))

    # A one-member population has keep=0; [-0:] keeps every element.
    population = ['candidate']
    keep = int(len(population) * .7)
    survivors = population[-keep:]
    assert keep == 0 and survivors == population
    results.append(dict(id='prune_zero_slice', keep=keep, survivors=survivors,
                        status='shown slicing fails to remove the sole candidate'))

    # Source max-rate expression only responds to the upper boundary.
    rate = lambda lam: .5 * (1.2 - lam)
    assert rate(.8) > rate(1.1) and rate(1.3) < 0
    results.append(dict(id='integration_rate', at_lower_bound=rate(.8),
                        at_1_1=rate(1.1), outside_upper_bound=rate(1.3),
                        status='expression is not a two-sided boundary margin and can be negative'))

    out = ROOT / 'evaluation/results/canon-contact.json'
    out.write_text(json.dumps(dict(kind='constructed local diagnostics',
                                  model_comparison=False, results=results), indent=2) + '\n')
    print(f'{len(results)} local diagnostics completed; results: {out}')
    print('Counterexamples and snippet defects do not refute all neighboring designs.')


if __name__ == '__main__':
    main()
