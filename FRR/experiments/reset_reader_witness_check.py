"""Post-run verification of RR1's three reversals, using rational path weights.

This check was added after seeing RR1. It verifies the selected witnesses;
it is not a preregistered independent confirmation or a new kernel search.
"""
from decimal import Decimal, localcontext
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'evaluation/reset-reader-study'


def decimal(x):
    return Decimal(x.numerator) / Decimal(x.denominator)


def verify_time(kernel, t):
    # At h=0, e never changes. Compute path likelihoods directly, rather than
    # importing or calling the study's filter or matrix propagation.
    stationary_y0 = [kernel[e][1][0] / (kernel[e][0][1] + kernel[e][1][0]) for e in (0, 1)]
    prior = [x / sum(stationary_y0) for x in stationary_y0]
    words = [(0,) + suffix for suffix in product((0, 1), repeat=t)]
    actual, assumed = {}, {}
    pool = {y: [F(0), F(0)] for y in (0, 1)}
    for word in words:
        likelihood = []
        for e in (0, 1):
            value = F(1)
            for a, b in zip(word, word[1:]):
                value *= kernel[e][a][b]
            likelihood.append(value)
        actual[word] = likelihood[0]  # fixed e=0 preparation
        assumed[word] = [prior[e] * likelihood[e] for e in (0, 1)]
        for e in (0, 1):
            pool[word[-1]][e] += assumed[word][e]
    if sum(actual.values()) != 1:
        raise AssertionError('Exact path weights do not sum to one')
    risks = {name: Decimal(0) for name in ('full', 'one')}
    with localcontext() as context:
        context.prec = 60
        for word in words:
            y = word[-1]
            target = kernel[0][y]
            for name, weights in [('full', assumed[word]), ('one', pool[y])]:
                prediction = [sum(weights[e]*kernel[e][y][yn] for e in (0, 1)) / sum(weights) for yn in (0, 1)]
                loss = sum(decimal(target[yn]) * (decimal(target[yn])/decimal(prediction[yn])).ln() for yn in (0, 1))
                risks[name] += decimal(actual[word]) * loss
        gap = risks['full'] - risks['one']
        result = dict(t=t, full_risk_nats=str(risks['full']), one_risk_nats=str(risks['one']), gap_nats=str(gap))
    return result


def main():
    models = json.loads((OUT/'MODELS.json').read_text())
    kernel = [[[F(str(x)) for x in row] for row in env] for env in models['transfer_b']['kernel']]
    main_rows = json.loads((OUT/'RESULTS.json').read_text())['rows']
    rows = []
    for t in (4, 5, 6):
        result = verify_time(kernel, t)
        original = next(r for r in main_rows if r['model']=='transfer_b' and r['h']==0 and r['preparation']=='fixed_e0' and r['t']==t)
        error = abs(float(result['gap_nats'])-original['assumed_full_minus_assumed_1'])
        if Decimal(result['gap_nats']) <= 0 or error > 1e-14:
            raise AssertionError('Rational-path witness check failed')
        result['difference_from_float_run'] = error
        rows.append(result)
    output = dict(scope='Post-run selected-witness verification. Exact rational path weights and 60-digit Decimal logarithms; shared model definitions, no independent real-system evidence.',model='transfer_b',h=0,preparation='fixed_e0',rows=rows)
    (OUT/'WITNESS_CHECK.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))


if __name__ == '__main__':
    main()
