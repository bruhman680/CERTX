"""Matched same-law stewardship reward-shaping comparison, no retuning.

Uses frozen source Garden v0.1, normal learned Garden v0.1, and
StewardshipGarden with augmented resource-delta reward. All live in the same
unchanged resource/energy environmental transition laws.
"""

import argparse
import json
from pathlib import Path

import numpy as np

from garden import Garden
from stewardship_garden import StewardshipGarden
from evaluate import heldout_common_world_probe


def collect(world, probe_seed):
    m = world.metrics()
    return {
        "tick": world.tick,
        "mean_energy": float(world.energy.mean()),
        "fraction_energy_gt_0p1": float(np.mean(world.energy > .1)),
        "fraction_energy_at_zero": float(np.mean(world.energy <= 1e-9)),
        "mean_resource": float(world.resource.mean()),
        "harvest_rate": float(m.get("harvest_rate", 0.)),
        "prediction_mse_on_policy": float(m["prediction_mse"]) if m.get("prediction_mse") is not None else None,
        "reference_action_probe_mse": float(world.prediction_probe(seed=probe_seed,n=128)),
        "common_reference_world_probe_mse": heldout_common_world_probe(world, probe_seed, length=80),
    }


def evaluate(seed,size=12,max_steps=600):
    arms={
        "v01_learning": Garden(seed=seed,size=size,learning=True),
        "v02_stewardship": StewardshipGarden(seed=seed,size=size,learning=True),
        "v01_frozen": Garden(seed=seed,size=size,learning=False),
    }
    out={"seed":seed,"checkpoints":[]}
    for t in range(max_steps+1):
        if t in [0,200,600]:
            out["checkpoints"].append({"step":t,"arms":{
                name:collect(world, probe_seed=100000+seed) for name,world in arms.items()
            }})
        if t<max_steps:
            for world in arms.values():world.step()
    return out


if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--seeds",nargs="+",type=int,default=[151,163,179,191,211])
    p.add_argument("--size",type=int,default=12)
    p.add_argument("--output",type=Path,default=Path("stewardship_results.json"))
    a=p.parse_args()
    r={"design":"Same-law v0.1 vs reward-shaped stewardship v0.2 vs frozen; no parameter tuning on evaluation seeds",
       "seeds":a.seeds,"size":a.size,"max_steps":600,"results":[evaluate(s,a.size) for s in a.seeds]}
    a.output.write_text(json.dumps(r,indent=2)+"\n",encoding="utf-8")
    print(f"Saved {a.output}")
