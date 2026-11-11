"""Separate exploratory threshold-policy control; NOT one of the 100 sweep runs.

Threshold 0.55 was suggested after observing earlier results. It is held fixed
on fresh seeds here, but this is not independent preregistered validation.
"""

import json
from pathlib import Path

import numpy as np

from garden import Garden


SEEDS = list(range(600, 620))
THRESHOLD = .55


def threshold_run(seed, steps=600):
    world = Garden(seed=seed, size=16, learning=False)
    measures=[]
    for t in range(1, steps+1):
        old_r,old_e=world.resource.copy(), world.energy.copy()
        action = (old_r>THRESHOLD).astype(float)
        diffusion=.08*(world._neighbors(old_r)-old_r)
        regrowth=.06*(1.-old_r)
        consumption=.18*old_r*action
        world.resource=np.clip(old_r+diffusion+regrowth-consumption,0.,1.)
        delta=.25*old_r*action-.03-.055*action+.008*(1.-action)
        world.energy=np.clip(old_e+delta,0.,1.)
        if t in [200,600]:
            measures.append({"step":t,"mean_energy":float(world.energy.mean()),
                             "floor_fraction":float((world.energy<=.01).mean()),
                             "mean_resource":float(world.resource.mean()),
                             "harvest_rate":float(action.mean()),
                             "raw_unclipped_delta_energy":float(delta.mean())})
    return {"seed":seed,"policy":"harvest iff local resource>.55", "measures":measures}


def main():
    runs=[threshold_run(seed) for seed in SEEDS]
    mean_at=lambda t,key:float(np.mean([next(x for x in r["measures"] if x["step"]==t)[key] for r in runs]))
    obj={"status":"exploratory separate baseline, not part of fixed 100-run sweep",
         "threshold":THRESHOLD,"seeds":SEEDS,"runs":runs,
         "averages":{str(t):{k:mean_at(t,k) for k in ["mean_energy","floor_fraction","mean_resource","harvest_rate","raw_unclipped_delta_energy"]} for t in [200,600]}}
    out=Path(__file__).resolve().parent/"heuristic_counterfactual.json"
    out.write_text(json.dumps(obj,indent=2))
    print(json.dumps({"averages":obj["averages"]},indent=2))


if __name__ == "__main__":
    main()
