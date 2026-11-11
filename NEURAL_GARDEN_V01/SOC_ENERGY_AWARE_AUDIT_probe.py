"""One causal feature ablation: freeze SAME learned weights, mask energy input.

No imitation teacher. This isolates use of the energy channel at deployment
from changes in other learned coefficients during training.
"""

import hashlib
import json
from pathlib import Path

import numpy as np

from SOC_ENERGY_AWARE_policy import EnergyAwareGarden,ExplicitRuleGarden
from SOC_ENERGY_AWARE_deployment import deterministic_step


ROOT=Path(__file__).resolve().parent
SEEDS={"stable":range(19000,19012),"mild":range(20000,20012)}


def one(seed,regime):
    train=EnergyAwareGarden(seed=seed,size=16,learning=True,energy_feature=True,reward_mode='raw')
    for _ in range(1200):train.step()
    test_seed=seed+30000
    models={}
    for name,feature in [('full_energy',True),('masked_energy',False)]:
        g=EnergyAwareGarden(seed=test_seed,size=16,learning=False,energy_feature=feature,
                            reward_mode='raw')
        g.theta=train.theta.copy()  # same learned resource/bias/energy weights
        models[name]=g
    fixed=ExplicitRuleGarden(seed=test_seed,size=16,rescue=False)
    # Must have identical starting physical world and controller weights.
    assert np.array_equal(models['full_energy'].theta,models['masked_energy'].theta)
    assert np.array_equal(models['full_energy'].resource,models['masked_energy'].resource)
    assert np.array_equal(models['full_energy'].energy,models['masked_energy'].energy)
    pre_weight=np.abs(train.theta[:,1]); milestones={}
    for tick in range(1,3001):
        rate=.055 if regime=='mild' and 1001<=tick<=2000 else .06
        deterministic_step(models['full_energy'],rate)
        deterministic_step(models['masked_energy'],rate)
        fixed.regrowth=rate;fixed.step()
        if tick in (1000,2000,3000):
            milestones[str(tick)]={k:{'energy':float(g.energy.mean()),
                                       'floor':float(np.mean(g.energy<=.01)),
                                       'ceiling':float(np.mean(g.energy>=.99))}
                                   for k,g in [*models.items(),('fixed50',fixed)]}
    return {'seed':seed,'regime':regime,
            'trained_energy_weight_abs_mean':float(pre_weight.mean()),
            'trained_energy_weight_positive_fraction':float(np.mean(train.theta[:,1]>0)),
            'milestones':milestones}


def run():
    rows=[one(seed,regime) for regime,seeds in SEEDS.items() for seed in seeds]
    summary={};paired={}
    for regime in SEEDS:
        group=[r for r in rows if r['regime']==regime]
        summary[regime]={arm:{metric:float(np.mean([r['milestones']['3000'][arm][metric]
                                                       for r in group]))
                              for metric in ('energy','floor','ceiling')}
                         for arm in ('full_energy','masked_energy','fixed50')}
        full=np.array([r['milestones']['3000']['full_energy']['energy'] for r in group])
        masked=np.array([r['milestones']['3000']['masked_energy']['energy'] for r in group])
        fixed=np.array([r['milestones']['3000']['fixed50']['energy'] for r in group])
        paired[regime]={
            'energy_input_on_minus_masked':{'mean':float(np.mean(full-masked)),
               'wins':int(np.sum(full>masked)),'losses':int(np.sum(full<masked)),
               'sd':float(np.std(full-masked,ddof=1))},
            'full_minus_fixed50':{'mean':float(np.mean(full-fixed)),
               'wins':int(np.sum(full>fixed)),'losses':int(np.sum(full<fixed))},
        }
    return {'question':'Does energy feature itself matter after holding learned resource and bias weights fixed?',
            'status':'executed independent feature ablation',
            'design':{'seeds':{k:list(v) for k,v in SEEDS.items()},'train_ticks':1200,
                      'test_ticks':3000,'size':16,'same_learned_theta_in_both_ablations':True,
                      'difference':'mask energy observation only at frozen deterministic deployment',
                      'regime_shift':'mild regrowth .06→.055 at t1001–2000, restored thereafter'},
            'source_sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
                for f in ('garden.py','SOC_ENERGY_AWARE_policy.py',
                          'SOC_ENERGY_AWARE_deployment.py',Path(__file__).name)},
            'summary':summary,'paired':paired,'rows':rows,
            'limits':'Same simulator, posthoc model family, policy frozen during test; does not show within-shift learning or indefinite viability.'}


if __name__=='__main__':
    result=run()
    (ROOT/'SOC_ENERGY_AWARE_AUDIT_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'summary':result['summary'],'paired':result['paired']},indent=2))
