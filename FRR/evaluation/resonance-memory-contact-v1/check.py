"""Independent mathematical checks of the public 2025 paper formula, not product code."""
import cmath
import hashlib
import json
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent


def energy(z):
    return math.fsum(abs(x) ** 2 for x in z)


def paper_score(a, b):
    ea, eb = energy(a), energy(b)
    if not ea or not eb:
        return 0.0
    return .5 * energy([x + y for x, y in zip(a, b)]) / (ea + eb) * (
        2 * math.sqrt(ea * eb) / (ea + eb))


def real_score(a, b):
    # Preserve every coordinate: complex d dimensions -> real 2d dimensions.
    u = [x.real for x in a] + [x.imag for x in a]
    v = [x.real for x in b] + [x.imag for x in b]
    ea = math.fsum(x * x for x in u)
    eb = math.fsum(x * x for x in v)
    if not ea or not eb:
        return 0.0
    c = math.fsum(x * y for x, y in zip(u, v)) / math.sqrt(ea * eb)
    r = 2 * math.sqrt(ea * eb) / (ea + eb)
    return r / 2 + r * r * c / 2


def normalized(z):
    return [x / math.sqrt(energy(z)) for x in z]


def run():
    rng = random.Random(20261025)
    maxima = dict(real_equivalence=0., symmetry=0., common_phase=0., equal_norm=0.)
    low, high, n = 1., 0., 0
    for d in [1, 4, 16, 64]:
        for _ in range(100):
            a = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(d)]
            raw_b = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(d)]
            phase = cmath.exp(1j * rng.uniform(-math.pi, math.pi))
            for scale in [.25, 1., 4.]:
                b = [x * scale for x in raw_b]
                s = paper_score(a, b)
                maxima['real_equivalence'] = max(maxima['real_equivalence'], abs(s-real_score(a,b)))
                maxima['symmetry'] = max(maxima['symmetry'], abs(s-paper_score(b,a)))
                maxima['common_phase'] = max(maxima['common_phase'], abs(s-paper_score([x*phase for x in a], [x*phase for x in b])))
                an, bn = normalized(a), normalized(b)
                c = math.fsum((x.conjugate()*y).real for x,y in zip(an,bn))
                maxima['equal_norm'] = max(maxima['equal_norm'], abs(paper_score(an,bn)-(1+c)/2))
                low, high, n = min(low,s), max(high,s), n+1
    unit = [1+0j, 0j]
    opposite = [-1+0j, 0j]
    amplified = [2+0j, 0j]
    # These labels are stipulated; no text encoder is being evaluated.
    witnesses = {
        'same_amplitude_opposite_phase': {'amplitude_only_cosine':1., 'realified_cosine':-1., 'paper_score':paper_score(unit,opposite)},
        'same_direction_double_amplitude': {'cosine':1., 'paper_score':paper_score(unit,amplified)},
        'missing_as_zero': {'unknown_encoded':[0,0], 'measured_zero_encoded':[0,0], 'indistinguishable_without_status':True},
        'opposite_records_summed': {'sum':[str(x+y) for x,y in zip(unit,opposite)], 'score_against_query':paper_score(unit,[0j,0j]), 'separate_scores':[paper_score(unit,unit),paper_score(unit,opposite)]},
        'zero_convention':paper_score([0j],[0j])
    }
    checks = {
        'information_matched_equivalence': maxima['real_equivalence'] < 1e-12,
        'symmetry':maxima['symmetry'] < 1e-12,
        'common_phase_invariance':maxima['common_phase'] < 1e-12,
        'equal_norm_reduction':maxima['equal_norm'] < 1e-12,
        'range':low >= -1e-12 and high <= 1+1e-12,
        'opposite_phase':witnesses['same_amplitude_opposite_phase']['paper_score'] == 0,
        'amplitude_scaling':abs(witnesses['same_direction_double_amplitude']['paper_score']-.72)<1e-12,
        'cancellation':witnesses['opposite_records_summed']['score_against_query']==0,
    }
    result = {'scope':'published formula, synthetic inputs, ordinary float64; not product or language reproduction',
              'pairs':n,'seed':20261025,'max_absolute_errors':maxima,'observed_range':[low,high],
              'witnesses':witnesses,'checks':checks,
              'plan_sha256':hashlib.sha256((HERE/'PLAN.md').read_bytes()).hexdigest()}
    (HERE/'RESULTS.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2,allow_nan=False))
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == '__main__':
    run()
