"""Counterfactual deterministic deployment of identical teacher-free weights."""
from pathlib import Path
import json
import numpy as np
from SOC_ENERGY_AWARE_policy import EnergyAwareGarden,ExplicitRuleGarden


def deterministic_step(g,regrowth):
    r=g.resource.copy();e=g.energy.copy()
    x=np.stack([3*(r-.5),3*(e-.5),np.ones(g.count)],axis=1)
    if not g.energy_feature:x[:,1]=0.
    action=(np.sum(g.theta*x,axis=1)>0).astype(float)
    nr=np.clip(r+.08*(g._neighbors(r)-r)+regrowth*(1-r)-.18*r*action,0,1)
    raw=.25*r*action-.03-.055*action+.008*(1-action)
    ne=np.clip(e+raw,0,1)
    g.resource=nr;g.energy=ne;g.tick+=1


def run():
    out=[]
    for regime,base in [('stable',17000),('mild',18000)]:
        for seed in range(base,base+12):
            models={}
            for label,feature in [('energy',True),('resource',False)]:
                train=EnergyAwareGarden(seed=seed,size=16,learning=True,
                                        energy_feature=feature,reward_mode='raw')
                for _ in range(1200):train.step()
                deploy=EnergyAwareGarden(seed=seed+30000,size=16,learning=False,
                                         energy_feature=feature,reward_mode='raw')
                deploy.theta=train.theta.copy()
                models[label]=deploy
            models['fixed50']=ExplicitRuleGarden(seed=seed+30000,size=16)
            for tick in range(1,3001):
                rate=.055 if regime=='mild' and 1001<=tick<=2000 else .06
                deterministic_step(models['energy'],rate)
                deterministic_step(models['resource'],rate)
                models['fixed50'].regrowth=rate
                models['fixed50'].step()
            out.append({'regime':regime,'seed':seed,
                        **{k:{'energy':float(g.energy.mean()),
                              'floor':float(np.mean(g.energy<=.01))}
                           for k,g in models.items()}})
    means={regime:{name:{k:float(np.mean([r[name][k] for r in out if r['regime']==regime]))
                            for k in ('energy','floor')}
                   for name in ('energy','resource','fixed50')}
           for regime in ('stable','mild')}
    return {'design':{'train_ticks':1200,'test_ticks':3000,'size':16,
                      'regimes':'stable .06; mild .055 at test ticks 1001-2000',
                      'policy':'deterministic sign of learned logistic logit, weights frozen'},
            'means':means,'rows':out}


if __name__=='__main__':
    d=run()
    Path(__file__).with_name('SOC_ENERGY_AWARE_deployment_results.json').write_text(json.dumps(d,indent=2)+'\n')
    print(json.dumps(d['means'],indent=2))
