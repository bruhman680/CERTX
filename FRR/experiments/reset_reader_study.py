"""RR1 finite reset-reader comparison. See the prospectively saved protocol."""
import hashlib
import json
import platform
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'evaluation/reset-reader-study'
TOL = 1e-11
PREPARATIONS = ('natural_y0', 'do_y0', 'fixed_e0', 'fixed_e1', 'fresh_uniform')
SIZES = (1, 2, 4, 'full')


def joint_chain(kernel, h):
    p = np.zeros((4, 4))
    for y in (0, 1):
        for e in (0, 1):
            for yn in (0, 1):
                for en in (0, 1):
                    transport = (1 - h) * (en == e) + h * (en == y)
                    p[2*y+e, 2*yn+en] = kernel[e, y, yn] * transport
    return p


def stationary(kernel, h, p):
    if h == 0:
        pi = np.zeros((2, 2))
        for e in (0, 1):
            switch01, switch10 = kernel[e, 0, 1], kernel[e, 1, 0]
            pi[:, e] = .5 * np.array([switch10, switch01]) / (switch01 + switch10)
        return pi.reshape(-1)
    a = p.T - np.eye(4)
    a[-1] = 1
    b = np.zeros(4)
    b[-1] = 1
    return np.linalg.solve(a, b)


def advance(level, kernel, h):
    nxt = {}
    for word, weights in level.items():
        old_y = word[-1]
        for yn in (0, 1):
            mass = weights * kernel[:, old_y, yn]
            transported = (1 - h) * mass
            transported[old_y] += h * mass.sum()
            nxt[word + (yn,)] = transported
    return nxt


def pools(level, size):
    result = {}
    for word, weights in level.items():
        key = word if size == 'full' else word[-size:]
        if key not in result:
            result[key] = np.zeros(2)
        result[key] += weights
    return result


def kl(p, q):
    p, q = np.asarray(p), np.asarray(q)
    mask = p > 0
    return float(np.sum(p[mask] * np.log(p[mask] / q[mask])))


def inspect_level(actual, assumed, kernel, pi):
    actual_pools = {s: pools(actual, s) for s in SIZES}
    assumed_pools = {s: pools(assumed, s) for s in SIZES}
    names = [f'{family}_{s}' for family in ('matched', 'assumed') for s in SIZES] + ['stationary_1']
    risks = dict.fromkeys(names, 0.)
    regrets = dict.fromkeys(names, 0.)
    for word, weights in actual.items():
        mass = float(weights.sum())
        emissions = kernel[:, word[-1], :]
        true_prediction = (weights / mass) @ emissions
        predictions = {}
        for family, collection in [('matched', actual_pools), ('assumed', assumed_pools)]:
            for size in SIZES:
                key = word if size == 'full' else word[-size:]
                belief = collection[size][key]
                predictions[f'{family}_{size}'] = (belief / belief.sum()) @ emissions
        belief = pi.reshape(2, 2)[word[-1]]
        predictions['stationary_1'] = (belief / belief.sum()) @ emissions
        for name, prediction in predictions.items():
            risks[name] += sum(weights[e] * kl(emissions[e], prediction) for e in (0, 1))
            regrets[name] += mass * kl(true_prediction, prediction)
    identity_error = max(abs((risks[n] - risks['matched_full']) - regrets[n]) for n in names)
    return risks, regrets, identity_error


def run():
    start = time.perf_counter()
    models = json.loads((OUT / 'MODELS.json').read_text())
    rows = []
    maxima = dict(mass_error=0., joint_marginal_error=0., stationarity_error=0.,
                  risk_identity_error=0., matched_order_violation=0., h1_risk_error=0.)
    for model_name, specification in models.items():
        kernel = np.array(specification['kernel'], dtype=float)
        if np.max(abs(kernel.sum(axis=2) - 1)) > TOL or np.min(kernel) <= 0:
            raise ValueError('Invalid model table')
        for h in specification['h']:
            p = joint_chain(kernel, h)
            pi = stationary(kernel, h, p)
            maxima['stationarity_error'] = max(maxima['stationarity_error'], float(abs(pi @ p - pi).max()), float(abs(p.sum(1) - 1).max()))
            natural = pi[:2] / pi[:2].sum()
            priors = dict(natural_y0=natural, do_y0=pi.reshape(2, 2).sum(axis=0),
                          fixed_e0=np.array([1., 0.]), fixed_e1=np.array([0., 1.]),
                          fresh_uniform=np.array([.5, .5]))
            for preparation in PREPARATIONS:
                actual = {(0,): priors[preparation].copy()}
                assumed = {(0,): natural.copy()}
                joint = np.r_[priors[preparation], [0., 0.]]
                for t in range(9):
                    risks, regrets, error = inspect_level(actual, assumed, kernel, pi)
                    maxima['risk_identity_error'] = max(maxima['risk_identity_error'], error)
                    for level in (actual, assumed):
                        maxima['mass_error'] = max(maxima['mass_error'], abs(sum(w.sum() for w in level.values()) - 1))
                    aggregate = np.zeros(4)
                    for word, weights in actual.items():
                        aggregate[2*word[-1]:2*word[-1]+2] += weights
                    maxima['joint_marginal_error'] = max(maxima['joint_marginal_error'], float(abs(aggregate-joint).max()))
                    order = [risks[f'matched_{s}'] for s in SIZES]
                    maxima['matched_order_violation'] = max(maxima['matched_order_violation'], max(order[i+1] - order[i] for i in range(3)))
                    if h == 1 and t >= 1:
                        maxima['h1_risk_error'] = max(maxima['h1_risk_error'], max(abs(risks[n]) for n in ['matched_full', 'matched_2', 'assumed_full', 'assumed_2']))
                    rows.append(dict(model=model_name, h=h, preparation=preparation, t=t,
                                     risks_nats=risks, excess_vs_matched_full_nats=regrets,
                                     assumed_full_minus_assumed_1=risks['assumed_full']-risks['assumed_1'],
                                     assumed_full_minus_stationary_1=risks['assumed_full']-risks['stationary_1']))
                    actual = advance(actual, kernel, h)
                    assumed = advance(assumed, kernel, h)
                    joint = joint @ p
    summaries = {}
    compact = lambda r: {k: r[k] for k in ['model', 'h', 'preparation', 't', 'risks_nats', 'assumed_full_minus_assumed_1']}
    for name in models:
        subset = [r for r in rows if r['model'] == name]
        reversals = [r for r in subset if r['assumed_full_minus_assumed_1'] > TOL]
        shifted = [r for r in subset if r['preparation'] != 'natural_y0']
        largest = max(subset, key=lambda r: r['assumed_full_minus_assumed_1'])
        summaries[name] = dict(cells=len(subset), shifted_cells=len(shifted),
            assumed_full_worse_than_assumed_1=len(reversals),
            first_reversal=compact(reversals[0]) if reversals else None,
            largest_reversal=compact(largest) if reversals else None,
            largest_full_preparation_penalty_nats=max(r['excess_vs_matched_full_nats']['assumed_full'] for r in subset))
    inputs = ['evaluation/reset-reader-study/PROTOCOL.md', 'evaluation/reset-reader-study/MODELS.json', 'experiments/reset_reader_study.py']
    hashes = {f: hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in inputs}
    maxima = {name: float(value) for name, value in maxima.items()}
    summary = dict(scope='Deterministic finite-history toy, all prespecified cells; no model-agent efficacy or physical-memory claim.',
                   row_count=len(rows), cells_per_reader=len(rows), tolerance=TOL,
                   maxima=maxima, algebraic_and_integrity_checks_pass=all(v <= TOL for v in maxima.values()),
                   predictions={'P1_matched_order': maxima['matched_order_violation'] <= TOL,
                                'P2_risk_decomposition': maxima['risk_identity_error'] <= TOL,
                                'P3_source_reversal_exists': summaries['source']['assumed_full_worse_than_assumed_1'] > 0,
                                'P4_h1_preparation_forgetting': maxima['h1_risk_error'] <= TOL},
                   by_model=summaries, input_sha256=hashes,
                   environment=dict(python=sys.version, numpy=np.__version__, platform=platform.platform()),
                   elapsed_seconds=time.perf_counter()-start)
    (OUT/'RESULTS.json').write_text(json.dumps(dict(summary=summary, rows=rows), indent=2)+'\n')
    (OUT/'SUMMARY.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary, indent=2))
    return summary['algebraic_and_integrity_checks_pass']


if __name__ == '__main__':
    sys.exit(0 if run() else 1)
