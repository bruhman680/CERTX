"""Predeclared 100-run Neural Garden factorial sweep (5 arms × 20 seeds).

No model or law parameters are tuned by this script. Each independent run uses
the same 16×16 initial seed within its arm. The three model families remain
separate experiments; cross-world comparisons are descriptive, not causal
attributions to a learning rule alone.
"""

from __future__ import annotations

import hashlib
import json
import statistics
from pathlib import Path

import numpy as np

from garden import Garden
from stewardship_garden import StewardshipGarden
from viable_garden import ViableGarden


ROOT = Path(__file__).resolve().parent
SEEDS = list(range(100, 120))
STEPS = 200
SIZE = 16
CHECKPOINT_STEPS = [0, 50, 100, 150, 200]
ARMS = [
    ("v01_learning", Garden, True),
    ("v01_frozen", Garden, False),
    ("v02_stewardship_learning", StewardshipGarden, True),
    ("v03_viable_learning", ViableGarden, True),
    ("v03_viable_frozen", ViableGarden, False),
]


def source_hashes():
    names = ["garden.py", "stewardship_garden.py", "viable_garden.py", "hundred_cycle_sweep.py"]
    return {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names}


def measurements(garden):
    m = dict(garden.metrics())
    m["fraction_energy_le_001"] = float((garden.energy <= .01).mean())
    m["energy_std"] = float(np.std(garden.energy))
    m["resource_std"] = float(np.std(garden.resource))
    m["active_energy_fraction_gt_010"] = float((garden.energy > .10).mean())
    return m


def one_run(arm_name, cls, learning, seed):
    run_config = {"arm":arm_name,"seed":seed,"size":SIZE,"steps":STEPS,
                  "learning":learning,"model":cls.__name__}
    config_hash = hashlib.sha256(json.dumps(run_config,sort_keys=True).encode()).hexdigest()
    garden = cls(seed=seed, size=SIZE, learning=learning)
    trajectory = [{"step": 0, **measurements(garden)}]
    for step in range(1, STEPS+1):
        garden.step()
        if step in CHECKPOINT_STEPS:
            trajectory.append({"step": step, **measurements(garden)})
    return {"run_id":f"{arm_name}__seed_{seed}", "config_sha256":config_hash,
            "arm": arm_name, "seed": seed, "size": SIZE, "steps": STEPS,
            "learning": learning, "model": cls.__name__, "trajectory": trajectory,
            "final": trajectory[-1], "fingerprint": garden.fingerprint()}


def summarize(runs):
    summary = {}
    for name, _, _ in ARMS:
        subset = [x for x in runs if x["arm"] == name]
        fields = ["mean_energy", "mean_resource", "harvest_rate", "prediction_mse",
                  "fraction_energy_le_001", "active_energy_fraction_gt_010"]
        summary[name] = {k: {"mean": statistics.fmean(x["final"][k] for x in subset),
                            "sd_across_seeds": statistics.stdev(x["final"][k] for x in subset),
                            "min": min(x["final"][k] for x in subset),
                            "max": max(x["final"][k] for x in subset)} for k in fields}
        summary[name]["n_independent_runs"] = len(subset)
    # Matched-seed differences make the comparison explicit, with no claims of
    # statistical independence across the five arms sharing the same seed.
    contrasts = {}
    for left,right in [("v01_learning","v01_frozen"),
                       ("v02_stewardship_learning","v01_learning"),
                       ("v03_viable_learning","v03_viable_frozen"),
                       ("v03_viable_learning","v01_learning")]:
        l={r["seed"]:r for r in runs if r["arm"]==left}
        rr={r["seed"]:r for r in runs if r["arm"]==right}
        contrasts[f"{left}_minus_{right}"]={key: {
            "mean":statistics.fmean(l[s]["final"][key]-rr[s]["final"][key] for s in SEEDS),
            "sd_across_seeds":statistics.stdev(l[s]["final"][key]-rr[s]["final"][key] for s in SEEDS)
        } for key in ["mean_energy","prediction_mse","harvest_rate"]}
    return summary,contrasts


def main():
    runs=[]
    for name,cls,learning in ARMS:
        for seed in SEEDS:
            runs.append(one_run(name,cls,learning,seed))
        print(f"Finished {name}: {len(SEEDS)} seeds", flush=True)
    summary,contrasts=summarize(runs)
    result={"experiment":"neural-garden-100-run-v1", "status":"completed",
            "total_runs":len(runs),"arms": [a[0] for a in ARMS],
            "seeds":SEEDS,"steps_per_run":STEPS,"size":SIZE,
            "source_sha256":source_hashes(),"summary":summary,
            "paired_contrasts":contrasts,"runs":runs,
            "limitations":"Synthetic, same finite world families; 20 seeds per arm; no external-grounded intelligence or emergent evolution inference; exploratory conditions calibrated before sweep but not preregistered externally."}
    out=ROOT/"hundred_cycle_results.json"
    out.write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps({"total_runs":result["total_runs"],"summary":summary,"paired_contrasts":contrasts},indent=2))


if __name__ == "__main__":
    main()
