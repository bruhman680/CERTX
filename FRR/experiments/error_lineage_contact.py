"""Exact development witnesses; no LLM participants or universal error law."""
import hashlib
import json
import math
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'evaluation/error-lineage-v1'
PATHS = ['experiments/error_lineage_contact.py',
         'evaluation/error-lineage-v1/PROTOCOL.md',
         'evaluation/practice-growth-v1/RESIDUALS.json',
         'experiments/pid_contact.py']


def hashes():
    return {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in PATHS}


def joint(route, intervention='none'):
    probs = {}
    for u, weight in [(0, F(9, 10)), (1, F(1, 10))]:
        a = u
        if intervention == 'early':
            a = 0
        b = u if route == 'common' else a
        if intervention == 'late':
            a = 0
        if intervention == 'gate_damage':
            b = None  # Missing output, not a corrected answer.
        key = f'{a},{b}'
        probs[key] = probs.get(key, F(0)) + weight
    assert sum(probs.values()) == 1
    return probs


def main():
    import sys
    if sys.argv[1:] == ['prepare']:
        path = OUT / 'MANIFEST.json'
        if path.exists():
            raise SystemExit('Refusing to overwrite preparation')
        path.write_text(json.dumps({'scope': 'Before first execution; analytical predictions already known',
                                    'hashes': hashes()}, indent=2) + '\n')
        print('Prepared code, protocol and input hashes')
        return
    manifest = json.loads((OUT / 'MANIFEST.json').read_text())
    if hashes() != manifest['hashes']:
        raise SystemExit('Frozen inputs changed')
    dest = OUT / 'RESULTS.json'
    if dest.exists():
        raise SystemExit('Refusing to overwrite results')
    n, p = 32, F(1, 10)
    tail = sum(F(math.comb(n, k)) * p**k * (1-p)**(n-k) for k in range(16, n+1))
    dependence = {'n': n, 'marginal_error_probability': p,
                  'expected_errors_both': n*p,
                  'independent_P_at_least_16_errors': tail,
                  'common_P_at_least_16_errors': p}
    interventions = {mode: {route: joint(route, mode) for route in ['common', 'copy']}
                     for mode in ['none', 'early', 'late', 'sham', 'gate_damage']}
    # Cov(A,B)=E[p(D)^2]-E[p(D)]^2 for conditionally independent readers.
    difficulty = {'marginal': p, 'covariance': F(1, 2)*F(1, 5)**2-p**2}
    repair = {}
    for mode in ['none', 'suppress', 'source_only', 'source_and_recompute']:
        source_wrong = mode not in ['source_only', 'source_and_recompute']
        cached_wrong = [True, True]
        if mode == 'source_and_recompute':
            cached_wrong = [source_wrong, source_wrong]
        completed = [mode != 'suppress'] * 2
        repair[mode] = {'source_wrong': source_wrong,
                        'cached_wrong': sum(cached_wrong),
                        'completed': sum(completed),
                        'wrong_completed': sum(a and b for a, b in zip(cached_wrong, completed)),
                        'correct_completed': sum((not a) and b for a, b in zip(cached_wrong, completed))}
    branching = []
    for rate in [.5, 1., 1.2]:
        offspring_p = rate / 2
        extinction = 0.
        for _ in range(20):
            extinction = (1-offspring_p + offspring_p*extinction)**2
        branching.append({'R': rate, 'generation': 20, 'expected_generation_size': rate**20,
                          'extinction_by_generation': extinction,
                          'eventual_extinction': 1. if rate <= 1 else ((1-offspring_p)/offspring_p)**2})
    raw = json.loads((ROOT / PATHS[2]).read_text())
    residuals = [x for stream in raw['streams'] for x in stream['residuals']]
    audit = {'n': len(residuals), 'mean': math.fsum(residuals)/len(residuals),
             'MAE': math.fsum(abs(x) for x in residuals)/len(residuals),
             'abs_above_0.08': sum(abs(x) > .08 for x in residuals),
             'scope': 'One PI stream per seed; no independent-controller sample multiplication'}
    checks = {
        'equal_mean_different_tail': tail < p and n*p == F(16, 5),
        'observational_equivalence': interventions['none']['common'] == interventions['none']['copy'],
        'selective_early_discriminates': interventions['early']['common'] != interventions['early']['copy'],
        'late_does_not_discriminate': interventions['late']['common'] == interventions['late']['copy'],
        'sham_preserves': interventions['sham'] == interventions['none'],
        'off_target_gate_masks': interventions['gate_damage']['common'] == interventions['gate_damage']['copy'],
        'difficulty_positive_covariance_without_copy': difficulty['covariance'] > 0,
        'source_repair_leaves_stale_descendants': repair['source_only']['wrong_completed'] == 2,
        'suppression_not_task_completion': repair['suppress']['wrong_completed'] == 0 and repair['suppress']['completed'] == 0,
        'repair_and_reopen_completes': repair['source_and_recompute']['correct_completed'] == 2,
        'critical_mean_not_survival': branching[1]['expected_generation_size'] == 1 and branching[1]['eventual_extinction'] == 1,
        'saved_data_replay': audit['n'] == 12000 and audit['abs_above_0.08'] == 1855,
    }
    result = {'scope': 'EL-C1 exact development demonstration and retrospective saved-data replay',
              'dependence': dependence, 'interventions': interventions, 'difficulty': difficulty,
              'repair': repair, 'branching': branching, 'saved_data': audit, 'checks': checks,
              'input_hashes_match': hashes() == manifest['hashes']}
    def encode(x):
        if isinstance(x, F):
            return {'exact': str(x), 'float': float(x)}
        raise TypeError(type(x).__name__)
    dest.write_text(json.dumps(result, indent=2, default=encode) + '\n')
    print(json.dumps({'checks': checks, 'tail_independent': float(tail), 'tail_common': float(p),
                      'branching': branching, 'saved_data': audit}, indent=2))
    if not all(checks.values()):
        raise SystemExit('A declared witness failed; preserve output and investigate')


if __name__ == '__main__':
    main()
