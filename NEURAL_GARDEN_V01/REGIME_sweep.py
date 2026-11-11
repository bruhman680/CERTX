"""Autonomous-policy versus strong controls under labeled season/cost shift."""
from __future__ import annotations
import hashlib,json,platform
from pathlib import Path
import numpy as np
from ADAPTIVE_threshold import AdaptiveThresholdGarden
from REGIME_garden import RegimeGarden

CHECKPOINTS={500,999,1200,1600,1999,2200,2600,3000}
ARMS=('online','frozen_stochastic','frozen_deterministic',
      'untrained_stochastic','fixed50','fixed51')

def run():
    rows=[]
    for training_seed in range(2500,2524):
        trained=AdaptiveThresholdGarden(seed=training_seed,size=16,learning=True)
        initial=trained.thresholds.copy()
        for _ in range(1200):trained.step()
        test_seed=training_seed+10000
        worlds={
            'online':RegimeGarden(seed=test_seed,size=16,learning=True,deterministic=False),
            'frozen_stochastic':RegimeGarden(seed=test_seed,size=16,learning=False,deterministic=False),
            'frozen_deterministic':RegimeGarden(seed=test_seed,size=16,learning=False,deterministic=True),
            'untrained_stochastic':RegimeGarden(seed=test_seed,size=16,learning=False,deterministic=False),
            'fixed50':RegimeGarden(seed=test_seed,size=16,learning=False,deterministic=True),
            'fixed51':RegimeGarden(seed=test_seed,size=16,learning=False,deterministic=True),
        }
        for key in ('online','frozen_stochastic','frozen_deterministic'):
            worlds[key].thresholds=trained.thresholds.copy()
        worlds['untrained_stochastic'].thresholds=initial
        worlds['fixed50'].thresholds[:]=.50
        worlds['fixed51'].thresholds[:]=.51
        # Preconditions: exact matched world state; online/frozen stochastic
        # even share identical action RNG states until their thresholds diverge.
        assert all(np.array_equal(w.resource,worlds['online'].resource)
                   and np.array_equal(w.energy,worlds['online'].energy) for w in worlds.values())
        window={key:[] for key in ARMS}
        for tick in range(1,3001):
            for name,world in worlds.items():
                before=world.resource.copy()
                if tick==1001:before*=.70 # shock occurs inside step before decisions
                world.step()
                raw=float(world.last_raw_delta.mean())
                cov=float(np.mean((before-before.mean())*(world.last_action-world.last_action.mean())))
                window[name].append((raw,cov,world.energy.mean(),world.resource.mean()))
                if tick in CHECKPOINTS:
                    recent=np.array(window[name][-min(100,len(window[name])):])
                    rows.append({"train_seed":training_seed,"test_seed":test_seed,
                        "arm":name,"tick":tick,
                        "regime":world.metrics()['regime'],
                        "mean_energy":float(world.energy.mean()),
                        "mean_resource":float(world.resource.mean()),
                        "energy_floor_fraction":float(np.mean(world.energy<=.01)),
                        "energy_ceiling_fraction":float(np.mean(world.energy>=.99)),
                        "energetic_fraction":float(np.mean(world.energy>.10)),
                        "action_resource_cov":cov,
                        "raw_drift":raw,
                        "tail100_raw_drift":float(recent[:,0].mean()),
                        "tail100_mean_energy":float(recent[:,2].mean()),
                        "mean_threshold":float(world.thresholds.mean()),
                        "mean_threshold_abs_change":float(np.mean(abs(world.thresholds-trained.thresholds)))
                         if name=='online' else None})
    summaries={}
    for tick in sorted(CHECKPOINTS):
        summaries[str(tick)]={}
        for arm in ARMS:
            arr=[x for x in rows if x['tick']==tick and x['arm']==arm]
            summaries[str(tick)][arm]={metric:float(np.mean([x[metric] for x in arr]))
                                        for metric in ('mean_energy','mean_resource','energy_floor_fraction',
                                                       'energetic_fraction','tail100_raw_drift','action_resource_cov')}
    p=Path(__file__).resolve().parent
    src={name:hashlib.sha256((p/name).read_bytes()).hexdigest() for name in
         ('garden.py','ADAPTIVE_threshold.py','REGIME_garden.py','REGIME_sweep.py')}
    result={"design":"exploratory adaptive policy test on novel changed world laws",
            "size":16,"seeds":list(range(2500,2524)),"test_seeds":list(range(12500,12524)),
            "arms":list(ARMS),"training_ticks":1200,"testing_ticks":3000,
            "regimes":[{"from":0,"to":999,"regrowth":.06,"harvest_cost":.055},
                       {"from":1000,"to":1999,"regrowth":.025,"harvest_cost":.07,"resource_shock_factor":.7},
                       {"from":2000,"to":2999,"regrowth":.06,"harvest_cost":.055}],
            "python":platform.python_version(),"numpy":np.__version__,
            "source_sha256":src,"summaries":summaries,"rows":rows}
    (p/'REGIME_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({tick:{name:round(stat['mean_energy'],4) for name,stat in arms.items()}
                      for tick,arms in summaries.items()},indent=2))

if __name__=='__main__':run()
