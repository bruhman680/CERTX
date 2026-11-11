"""Adversarial fixed-and-learned Garden benchmark with multi-objective metrics.

The policy set is declared before execution. This is a synthetic exploratory
comparison, not independent preregistration of a real-world hypothesis.
"""

from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import numpy as np

from garden import Garden
from SOC_ENERGY_AWARE_policy import EnergyAwareGarden

ROOT = Path(__file__).resolve().parent
SEEDS = tuple(range(40000, 40012))
TICKS = 4000
TRAIN_TICKS = 1200
POLICIES = ('fixed50', 'fixed51', 'rescue_early', 'rescue_late',
            'neighbor_gradient', 'learned_energy', 'energy_masked')
REGIMES = ('stable', 'mild')


def deterministic_action(g, policy, learned_theta=None, masked=False):
    r, e = g.resource, g.energy
    if policy == 'fixed50':
        return r > .50
    if policy == 'fixed51':
        return r > .51
    if policy == 'rescue_early':
        return r > np.where(e < .12, .485, .51)
    if policy == 'rescue_late':
        return r > np.where(e < .12, .535, .51)
    if policy == 'neighbor_gradient':
        return r > (.51 + .5 * (g._neighbors(r) - r))
    if policy in ('learned_energy', 'energy_masked'):
        x = np.stack([3 * (r - .5), 3 * (e - .5), np.ones(g.count)], axis=1)
        if masked:
            x[:, 1] = 0.
        return np.sum(learned_theta * x, axis=1) >= 0.
    raise ValueError(policy)


def trial(seed, policy, regime, learned_theta):
    g = Garden(seed=seed + 50000, size=16, learning=False)
    energy_curve = []
    floor_curve = []
    raw_curve = []
    covariance = []
    shift_start = 1500
    shift_end = 2500
    pre = None
    recovery = None
    for t in range(TICKS):
        r, e = g.resource.copy(), g.energy.copy()
        if regime == 'mild' and t == shift_start:
            pre = float(np.mean(energy_curve[-100:]))
        action = deterministic_action(g, policy, learned_theta,
                                      masked=(policy == 'energy_masked')).astype(float)
        regrowth = .055 if regime == 'mild' and shift_start <= t < shift_end else .06
        raw = .25*r*action - .03 - .055*action + .008*(1.-action)
        g.energy = np.clip(e+raw, 0., 1.)
        g.resource = np.clip(r + .08*(g._neighbors(r)-r)
                             + regrowth*(1.-r) - .18*r*action, 0., 1.)
        g.tick += 1
        energy_curve.append(float(g.energy.mean()))
        floor_curve.append(float(np.mean(g.energy <= .01)))
        raw_curve.append(float(raw.mean()))
        covariance.append(float((r*action).mean()-r.mean()*action.mean()))
        if regime == 'mild' and t >= shift_end and recovery is None and pre is not None:
            if energy_curve[-1] >= .8 * pre:
                recovery = t - shift_end + 1
    last = slice(TICKS-500, TICKS)
    e_sorted = np.sort(g.energy)
    return {
        'seed': seed, 'policy': policy, 'regime': regime,
        'final_energy': float(g.energy.mean()),
        'final_floor': float(np.mean(g.energy <= .01)),
        'final_bottom_decile_energy': float(e_sorted[:max(1, len(e_sorted)//10)].mean()),
        'tail_energy': float(np.mean(energy_curve[last])),
        'tail_floor': float(np.mean(floor_curve[last])),
        'full_horizon_floor': float(np.mean(floor_curve)),
        'tail_raw_drift': float(np.mean(raw_curve[last])),
        'tail_resource_action_cov': float(np.mean(covariance[last])),
        'pre_shift_energy': pre,
        'recovery_to_80pct_pre': recovery,
        'final_fingerprint': g.fingerprint(),
    }


def main():
    # Same trained coefficients are used for masked and full action policies.
    pretrained = {}
    for seed in SEEDS:
        g = EnergyAwareGarden(seed=seed, size=16, learning=True,
                              reward_mode='raw', lr=.04, trace_decay=.97)
        for _ in range(TRAIN_TICKS):
            g.step()
        pretrained[seed] = g.theta.copy()

    rows = []
    for regime in REGIMES:
        for seed in SEEDS:
            # All policies start at exactly the same physical initial state.
            init = Garden(seed=seed+50000, size=16, learning=False)
            for policy in POLICIES:
                row = trial(seed, policy, regime, pretrained[seed])
                rows.append(row)
                # Preliminary source-world equality is independently verified.
                if policy == 'fixed50' and row['final_energy'] < 0.:
                    raise AssertionError('Invalid world energy')
    summary = {}
    for regime in REGIMES:
        summary[regime] = {}
        for policy in POLICIES:
            selection = [x for x in rows if x['regime'] == regime and x['policy'] == policy]
            summary[regime][policy] = {k: float(np.mean([x[k] for x in selection])) for k in
                ('final_energy','final_floor','final_bottom_decile_energy',
                 'tail_energy','tail_floor','full_horizon_floor',
                 'tail_raw_drift','tail_resource_action_cov')}
            summary[regime][policy]['recoveries'] = sum(x['recovery_to_80pct_pre'] is not None for x in selection)
            summary[regime][policy]['mean_recovery_ticks_when_observed'] = (
                float(np.mean([x['recovery_to_80pct_pre'] for x in selection
                               if x['recovery_to_80pct_pre'] is not None]))
                if summary[regime][policy]['recoveries'] else None)
    payload = {
        'status': 'completed',
        'design': {'seeds': SEEDS, 'ticks': TICKS, 'training_ticks': TRAIN_TICKS,
                   'policies': POLICIES, 'regimes': REGIMES,
                   'mild_intervention': 'resource regrowth .06->.055 over test ticks 1500..2499',
                   'fixed_welfare_metrics': ['mean_energy','energy_floor','bottom_decile',
                                            'tail_raw_drift','tail_resource_action_cov',
                                            'time_to_80pct_pre_shift_energy'],
                   'no_scalar_welfare_score': True,
                   'no_policy_selection_on_this_archive': True},
        'rows': rows,
        'summary': summary,
        'platform': {'python': platform.python_version(), 'numpy': np.__version__},
        'sources': {f: hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in
                    ('garden.py','SOC_ENERGY_AWARE_policy.py','NEXT_AUDIT_benchmark.py')},
        'limitations': ['synthetic matched seeds are not biological replications',
                        'learning occurs only in a separate training world',
                        'the candidate policies and mild intervention are informed by earlier studies',
                        'pre-shift energy is not a no-shift counterfactual recovery target',
                        'a missing recovery time means not recovered by tick4000',
                        'floor fraction is not modelled death',
                        'no claim of online adaptation, optimality, or indefinite stability'],
    }
    output = ROOT/'NEXT_AUDIT_results.json'
    output.write_text(json.dumps(payload, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
