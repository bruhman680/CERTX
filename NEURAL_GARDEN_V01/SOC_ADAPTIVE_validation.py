"""Post-selection robustness check across larger worlds and longer horizons.

Sealed only relative to original design seeds; hypothesis and hyperparameters
were chosen adaptively from earlier synthetic results. No generality claim.
"""
import hashlib
import json
from pathlib import Path
import numpy as np
from ADAPTIVE_threshold import AdaptiveThresholdGarden
from threshold_policy import ThresholdGarden
from SOC_ADAPTIVE_sequential import INITIAL


def evaluate(cfg, seed, steps=3000):
    g=AdaptiveThresholdGarden(seed=seed,size=16,learning=True,**cfg)
    original=g.thresholds.copy()
    for _ in range(500):g.step()
    dest=seed+30000
    learned=AdaptiveThresholdGarden(seed=dest,size=16,learning=False,
                                   deterministic=True,**cfg)
    learned.thresholds=g.thresholds.copy()
    untrained=AdaptiveThresholdGarden(seed=dest,size=16,learning=False,
                                     deterministic=True,**cfg)
    untrained.thresholds=original
    return learned,untrained


def run():
    source=Path(__file__).parent
    search=json.loads((source/'SOC_ADAPTIVE_results.json').read_text())
    config=search['selected_champion']['config']
    rows=[]
    for seed in range(8800,8812):
        # Separate, truly matched evaluation worlds, including the strongest
        # fixed policies seen during earlier exploratory work.
        learned,untrained=evaluate(config,seed)
        initial,_=evaluate(INITIAL,seed)
        fixed50=ThresholdGarden(seed=seed+30000,size=16,threshold=.50)
        fixed51=ThresholdGarden(seed=seed+30000,size=16,threshold=.51)
        milestones={}
        for t in range(1,3001):
            learned.step();untrained.step();initial.step();fixed50.step();fixed51.step()
            if t in (500,1000,2000,3000):
                milestones[t]={k:{'energy':float(v.energy.mean()),
                                  'floor':float(np.mean(v.energy<=.01))}
                    for k,v in [('learned',learned),('untrained',untrained),
                                ('initial',initial),('fixed50',fixed50),('fixed51',fixed51)]}
        rows.append({'seed':seed,'milestones':milestones})
    final={name:{'energy':float(np.mean([r['milestones'][3000][name]['energy'] for r in rows])),
                 'floor':float(np.mean([r['milestones'][3000][name]['floor'] for r in rows]))}
           for name in ('learned','untrained','initial','fixed50','fixed51')}
    return {'design':{'seeds':list(range(8800,8812)),'size':16,
                      'train_ticks':500,'test_ticks':3000,
                      'selected_hyperparameters':config,
                      'posthoc_tests':'chosen after size8 optimization; not a pristine prospective confirmation'},
            'sources':{n:hashlib.sha256((source/n).read_bytes()).hexdigest()
                       for n in ('SOC_ADAPTIVE_sequential.py','ADAPTIVE_threshold.py','garden.py','threshold_policy.py',Path(__file__).name)},
            'mean_t3000':final,'runs':rows}


if __name__=='__main__':
    output=run()
    dest=Path(__file__).with_name('SOC_ADAPTIVE_validation.json')
    dest.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output['mean_t3000'],indent=2))
