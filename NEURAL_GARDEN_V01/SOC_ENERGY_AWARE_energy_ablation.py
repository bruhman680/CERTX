"""After-training intervention: surgically remove only learned energy dependence."""
import json
from pathlib import Path
import numpy as np
from SOC_ENERGY_AWARE_policy import EnergyAwareGarden,ExplicitRuleGarden
from SOC_ENERGY_AWARE_deployment import deterministic_step


def run():
    rows=[]
    for seed in range(19000,19012):
        train=EnergyAwareGarden(seed=seed,size=16,learning=True,energy_feature=True,reward_mode='raw')
        for _ in range(1200):train.step()
        full=EnergyAwareGarden(seed=seed+30000,size=16,learning=False,energy_feature=True)
        full.theta=train.theta.copy()
        no_energy=EnergyAwareGarden(seed=seed+30000,size=16,learning=False,energy_feature=True)
        no_energy.theta=train.theta.copy();no_energy.theta[:,1]=0.
        fixed=ExplicitRuleGarden(seed=seed+30000,size=16)
        for tick in range(1,3001):
            rate=.055 if 1001<=tick<=2000 else .06
            deterministic_step(full,rate);deterministic_step(no_energy,rate)
            fixed.regrowth=rate;fixed.step()
        rows.append({'seed':seed,'trained_energy_weight_mean':float(np.mean(train.theta[:,1])),
                     **{name:{'energy':float(g.energy.mean()),
                              'floor':float(np.mean(g.energy<=.01))}
                        for name,g in [('full',full),('remove_energy_weight',no_energy),('fixed50',fixed)]}})
    means={name:{key:float(np.mean([r[name][key] for r in rows]))
                 for key in ('energy','floor')}
           for name in ('full','remove_energy_weight','fixed50')}
    return {'design':{'seeds':list(range(19000,19012)),'size':16,'train':1200,'test':3000,
                      'regrowth':'0.06→0.055→0.06 at test ticks1000,2000',
                      'intervention':'same trained weights, set only energy feature coefficient to zero before deployment'},
            'means':means,'rows':rows}


if __name__=='__main__':
    d=run()
    Path(__file__).with_name('SOC_ENERGY_AWARE_energy_ablation_results.json').write_text(json.dumps(d,indent=2)+'\n')
    print(json.dumps(d['means'],indent=2))
