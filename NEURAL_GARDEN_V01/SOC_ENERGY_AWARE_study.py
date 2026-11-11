"""Matched teacher-free energy-input and raw-reward ablations."""
import hashlib
import json
from pathlib import Path
import numpy as np
from SOC_ENERGY_AWARE_policy import EnergyAwareGarden,ExplicitRuleGarden

ARMS=('energy_raw_online','resource_raw_online','energy_raw_frozen',
      'energy_clipped_online','fixed50','energy_rescue_rule')


def test_seed(seed,regime):
    train={}
    for name,energy,reward in [('energy',True,'raw'),('resource',False,'raw'),
                               ('clipped',True,'clipped')]:
        g=EnergyAwareGarden(seed=seed,size=16,learning=True,
                            energy_feature=energy,reward_mode=reward)
        for _ in range(1200):g.step()
        train[name]=g.theta.copy()
    dest=seed+30000
    settings=[('energy_raw_online','energy',True,True,'raw'),
              ('resource_raw_online','resource',True,False,'raw'),
              ('energy_raw_frozen','energy',False,True,'raw'),
              ('energy_clipped_online','clipped',True,True,'clipped')]
    arms={}
    for label,source,learning,feature,reward in settings:
        g=EnergyAwareGarden(seed=dest,size=16,learning=learning,
                            energy_feature=feature,reward_mode=reward)
        g.theta=train[source].copy()
        arms[label]=g
    arms['fixed50']=ExplicitRuleGarden(seed=dest,size=16)
    arms['energy_rescue_rule']=ExplicitRuleGarden(seed=dest,size=16,rescue=True)
    checkpoints={}
    raw_tail={k:[] for k in ARMS}
    for tick in range(1,3001):
        if regime=='mild':
            rate=.055 if 1001<=tick<=2000 else .06
            for g in arms.values():g.regrowth=rate
        for key,g in arms.items():
            g.step()
            if tick>2900:raw_tail[key].append(float(g._last['raw_drift']))
        if tick in (1000,2000,3000):
            checkpoints[tick]={name:{'energy':float(g.energy.mean()),
                                    'resource':float(g.resource.mean()),
                                    'floor':float(np.mean(g.energy<=.01)),
                                    'harvest':float(g.last_action.mean()),
                                    'energy_weight_mean':float(np.mean(g.theta[:,1]))
                                       if isinstance(g,EnergyAwareGarden) else None}
                               for name,g in arms.items()}
    return {'seed':seed,'regime':regime,'checkpoints':checkpoints,
            'final_raw_drift_last100':{k:float(np.mean(v)) for k,v in raw_tail.items()}}


def run():
    rows=[]
    for regime,base in [('stable',15000),('mild',16000)]:
        for seed in range(base,base+12):rows.append(test_seed(seed,regime))
    means={}
    for regime in ('stable','mild'):
        cohort=[r for r in rows if r['regime']==regime]
        means[regime]={a:{
          metric:float(np.mean([r['checkpoints'][3000][a][metric] for r in cohort]))
          for metric in ('energy','floor','resource','harvest')}
          for a in ARMS}
    source=Path(__file__).parent
    return {'question':'Does locally observed energy improve teacher-free resource policy decisions?',
            'design':{'seeds_stable':list(range(15000,15012)),
                      'seeds_mild':list(range(16000,16012)),
                      'train_ticks':1200,'eval_ticks':3000,'size':16,
                      'mild_regrowth':'0.06 until tick1000; 0.055 until tick2000; 0.06 thereafter',
                      'action_rescue_rule':'resource>.48 when energy<.18 else >.50, explicit hand comparator only',
                      'no_teacher':True,'no_reward_shaping':True,
                      'initial_resource_weight_bias':4.,
                      'comparability':'same seeds and world laws within regime, pretrained weights transferred to fresh worlds'},
            'source_sha256':{n:hashlib.sha256((source/n).read_bytes()).hexdigest()
               for n in ('garden.py','SOC_ENERGY_AWARE_policy.py',Path(__file__).name)},
            'means':means,'rows':rows}


if __name__=='__main__':
    d=run()
    Path(__file__).with_name('SOC_ENERGY_AWARE_results.json').write_text(json.dumps(d,indent=2)+'\n')
    print(json.dumps(d['means'],indent=2))
