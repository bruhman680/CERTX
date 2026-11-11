"""Beyond 2000-tick: paired 5000-step held-out longitudinal test, no tuning."""
import hashlib,json,platform
from pathlib import Path
import numpy as np
from ADAPTIVE_threshold import AdaptiveThresholdGarden
from threshold_policy import ThresholdGarden

def run():
    checkpoints={500,1000,2000,3500,5000};rows=[]
    for seed in range(1200,1210):
        train=AdaptiveThresholdGarden(seed=seed,size=16,learning=True)
        initial=train.thresholds.copy()
        for _ in range(1200):train.step()
        base=seed+5000
        arms={"learned":AdaptiveThresholdGarden(seed=base,size=16,learning=False,deterministic=True),
              "untrained":AdaptiveThresholdGarden(seed=base,size=16,learning=False,deterministic=True),
              "fixed":ThresholdGarden(seed=base,size=16,threshold=.55),
              "fixed50":ThresholdGarden(seed=base,size=16,threshold=.50)}
        arms['learned'].thresholds=train.thresholds.copy()
        arms['untrained'].thresholds=initial
        for tick in range(1,5001):
            before={name:world.resource.copy() for name,world in arms.items()} if tick in checkpoints else None
            for world in arms.values():world.step()
            if tick in checkpoints:
                for name,world in arms.items():
                    r=before[name]; a=world.last_action
                    rows.append({"training_seed":seed,"test_seed":base,"arm":name,"tick":tick,
                                 "energy":float(world.energy.mean()),"resource":float(world.resource.mean()),
                                 "floor_fraction":float(np.mean(world.energy<=.01)),
                                 "energetic_fraction":float(np.mean(world.energy>.10)),
                                 "ceiling_fraction":float(np.mean(world.energy>=.99)),
                                 "energy_q10":float(np.quantile(world.energy,.10)),
                                 "energy_q50":float(np.quantile(world.energy,.50)),
                                 "energy_q90":float(np.quantile(world.energy,.90)),
                                 "harvest_rate":float(a.mean()),
                                 "raw_drift":float((.25*r*a-.03-.055*a+.008*(1-a)).mean()),
                                 "resource_action_cov":float(np.mean((r-r.mean())*(a-a.mean())))})
    summary={}
    for tick in sorted(checkpoints):
        summary[str(tick)]={arm:float(np.mean([x['energy'] for x in rows if x['tick']==tick and x['arm']==arm]))
                            for arm in ('learned','untrained','fixed','fixed50')}
    p=Path(__file__).resolve().parent
    sha={f:hashlib.sha256((p/f).read_bytes()).hexdigest()
         for f in ('ADAPTIVE_threshold.py','ADAPTIVE_longterm_probe.py','garden.py','threshold_policy.py')}
    result={"description":"exploratory posthoc 10-seed, 5000-tick held-out longitudinal comparison",
            "training":1200,"test":5000,"size":16,"seeds":list(range(1200,1210)),
            "source_sha256":sha,"python":platform.python_version(),"numpy":np.__version__,
            "summary":summary,"rows":rows}
    (p/'ADAPTIVE_longterm_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':run()
