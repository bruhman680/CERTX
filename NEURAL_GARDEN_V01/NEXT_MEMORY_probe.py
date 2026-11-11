"""Two independent memory/lineage questions in the synthetic Neural Garden.

1. Does a fixed three-symbol macro-history aid next-eight-state prediction after
   explicitly reducing regrowth in an otherwise fixed-threshold resource world?
2. Is acquired threshold inheritance behaviorally consequential at a matched
   first birth, or only mechanically transmitted?

No original source is modified; findings are not C_num/C_struct/C_symb measures.
"""

from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import numpy as np

from threshold_policy import ThresholdGarden
from SOC_INHERITANCE_causal import first_birth
import SOC_MACRO_probe as macro

HERE = Path(__file__).resolve().parent
MAPPING = np.array([0, 0, 1, 1, 0, 0, 2, 2], dtype=np.int8)
TRAIN = list(range(22300, 22308))
TEST = list(range(23300, 23308))


class RegrowthThreshold(ThresholdGarden):
    """Identical original physics except explicitly lower regrowth on given ticks."""

    def __init__(self, *args, low_regrowth=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.low_regrowth = low_regrowth

    def step(self):
        before_r = self.resource.copy()
        before_e = self.energy.copy()
        action = (before_r > self.threshold).astype(float)
        diffusion = .08 * (self._neighbors(before_r) - before_r)
        alpha = .055 if self.low_regrowth and (160 <= self.tick < 320) else .06
        next_r = np.clip(before_r + diffusion + alpha * (1. - before_r)
                         - .18 * before_r * action, 0., 1.)
        delta_e = .25 * before_r * action - .03 - .055 * action + .008 * (1. - action)
        next_e = np.clip(before_e + delta_e, 0., 1.)
        self.resource = next_r
        self.energy = next_e
        self.prev_action = action
        self.last_action = action.copy()
        self.prev_reward = next_e - before_e
        self.tick += 1
        self._last = {'tick': self.tick, 'mean_energy': float(next_e.mean()),
                      'mean_resource': float(next_r.mean()),
                      'harvest_rate': float(action.mean()),
                      'raw_drift': float(delta_e.mean())}
        return self.metrics()


def trajectories(seeds, low_regrowth):
    traces=[]
    ends=[]
    for seed in seeds:
        garden=RegrowthThreshold(seed=seed, size=10, threshold=.50,
                                 low_regrowth=low_regrowth)
        frames=[macro.categorical(garden)]
        for _ in range(420):
            garden.step()
            frames.append(macro.categorical(garden))
        traces.append(np.stack(frames))
        ends.append({'seed':seed, 'energy':float(garden.energy.mean()),
                     'floor':float(np.mean(garden.energy <= .01))})
    return np.stack(traces), ends


def macro_memory_probe():
    out={}
    for regime in ('baseline','seasonal_regrowth_reduced'):
        low=regime!='baseline'
        train,te=trajectories(TRAIN,low)
        test,ends=trajectories(TEST,low)
        current=macro.predictive_nll(train[:,3:],test[:,3:],MAPPING,0)
        lagged=macro.predictive_nll(train,test,MAPPING,3)
        full=macro.predictive_nll(train[:,3:],test[:,3:],np.arange(8,dtype=np.int8),0)
        out[regime]={'current3':current,'history3':lagged,'full8':full,
                     'memory_gain_nats':current['test_micro_nll']-lagged['test_micro_nll'],
                     'final_worlds':ends,'test_occupancy':np.bincount(test.reshape(-1),minlength=8).tolist(),
                     'intervention':'regrowth .06→.055 only at ticks161–320' if low else 'unchanged original world'}
    return out


def inherited_action_probe():
    seeds=list(range(24300,24320))
    births=[first_birth(seed) for seed in seeds]
    # The only difference at the matched first birth is the newborn threshold.
    # Test the *expected* action probabilities at standardized resource values,
    # avoiding noisy one-off sampled decisions.
    samples=np.linspace(.25,.75,501)
    records=[]
    for birth in births:
        a=birth['child_acquired_inheritance'];g=birth['child_germline_only']
        pa=1/(1+np.exp(-14*(samples-a)))
        pg=1/(1+np.exp(-14*(samples-g)))
        records.append({'seed':birth['seed'],'first_birth_tick':birth['first_birth_tick'],
                        'threshold_shift':a-g,
                        'max_abs_propensity_change':float(np.max(np.abs(pa-pg))),
                        'mean_abs_propensity_change':float(np.mean(np.abs(pa-pg))),
                        'matched_physical_state':birth['same_resource_and_energy_at_first_birth']})
    return {'sampled_resource_domain':[.25,.75],'slope':14.,
            'first_births':records,
            'mean_max_abs_propensity_change':float(np.mean([r['max_abs_propensity_change'] for r in records])),
            'mean_abs_threshold_shift':float(np.mean([abs(r['threshold_shift']) for r in records])),
            'qualifier':'Mechanistic child action-propensity comparison only; no demonstrated fitness gain.'}


def main():
    a=macro_memory_probe()
    b=inherited_action_probe()
    inputs=['garden.py','threshold_policy.py','SOC_MACRO_probe.py',
            'SOC_INHERITANCE_garden.py','SOC_INHERITANCE_causal.py',Path(__file__).name]
    result={'status':'executed two independent conceptual probes','train_seeds':TRAIN,
            'test_seeds':TEST,'size':10,'horizon':420,
            'eight_categories':'resource>=.48, energy>=.12, last action',
            'frozen_mapping':MAPPING.tolist(),
            'macro_memory_regimes':a,'acquired_action':b,
            'python':platform.python_version(),'numpy':np.__version__,
            'source_sha256':{x:hashlib.sha256((HERE/x).read_bytes()).hexdigest() for x in inputs},
            'limits':['Not continuous world-state recovery or an intelligence measure.',
                      'Macro-memory reference labels were selected on earlier experiments; no optimization on these test worlds.',
                      'Seasonal regrowth changes external physics by design.',
                      'Same simulator generator, synthetic seeds not real-world replication.']}
    (HERE/'NEXT_MEMORY_results.json').write_text(json.dumps(result,indent=2)+'\n')
    for regime,item in a.items():
        print(regime,'NLL current',item['current3']['test_micro_nll'],
              'history',item['history3']['test_micro_nll'],
              'gain',item['memory_gain_nats'],
              'energy',np.mean([x['energy'] for x in item['final_worlds']]))
    print('inheritance mean max propensity shift',b['mean_max_abs_propensity_change'])


if __name__=='__main__':
    main()
