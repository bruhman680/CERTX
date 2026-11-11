"""Second, separate 100-run threshold-policy sweep on original world laws.

Frozen before outcomes: five candidate thresholds (.35,.45,.55,.65,.75),
twenty common random seeds (200..219), 600 steps, 16x16 cells.
This tests conditional harvesting heuristics, not neural learning.
"""

import hashlib
import json
from pathlib import Path

import numpy as np

from garden import Garden


HERE = Path(__file__).resolve().parent
THRESHOLDS = [0.35, 0.45, 0.55, 0.65, 0.75]
SEEDS = list(range(200, 220))
SIZE = 16
STEPS = 600
CHECKPOINTS = (100, 200, 400, 600)
SCHEMA_VERSION = "threshold_100_v1_frozen_preoutcome"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_one(threshold, seed):
    world = Garden(seed=seed, size=SIZE, learning=False)
    checkpoints = []
    tail = []
    harvest_history = []
    for tick in range(1, STEPS + 1):
        before_r, before_e = world.resource.copy(), world.energy.copy()
        actions = (before_r > threshold).astype(np.float64)
        diffusion = .08 * (world._neighbors(before_r) - before_r)
        regrowth = .06 * (1. - before_r)
        consumption = .18 * before_r * actions
        world.resource = np.clip(before_r + diffusion + regrowth - consumption, 0., 1.)
        delta = .25 * before_r * actions - .03 - .055 * actions + .008 * (1. - actions)
        world.energy = np.clip(before_e + delta, 0., 1.)
        observation = {
            "tick": tick,
            "mean_energy": float(world.energy.mean()),
            "mean_resource": float(world.resource.mean()),
            "floor_fraction": float((world.energy <= .01).mean()),
            "ceiling_fraction": float((world.energy >= .99).mean()),
            "harvest_fraction": float(actions.mean()),
            "raw_unclipped_delta_energy": float(delta.mean()),
            "actual_clipped_delta_energy": float((world.energy-before_e).mean()),
            "harvested_resource_mean": float((before_r * actions).sum() / max(actions.sum(), 1)),
        }
        harvest_history.append(observation["harvest_fraction"])
        if tick in CHECKPOINTS:
            checkpoints.append(observation)
        if tick > 500:
            tail.append(observation)
    config = {"schema": SCHEMA_VERSION, "threshold": threshold, "seed": seed,
              "size": SIZE, "steps": STEPS, "law": "original_v01",
              "learning": False}
    config_hash = hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest()
    tail_means = {key: float(np.mean([x[key] for x in tail]))
                  for key in ("mean_energy", "mean_resource", "floor_fraction", "ceiling_fraction",
                              "harvest_fraction", "raw_unclipped_delta_energy")}
    return {"run_id":f"threshold_{threshold:.2f}_seed_{seed}","config":config,
            "config_sha256":config_hash,"checkpoints":checkpoints,
            "tail_501_600_means":tail_means,
            "harvest_timeline_100_step_means":[float(np.mean(harvest_history[k:k+100]))
                                              for k in range(0, STEPS, 100)],
            "final_state_sha256":hashlib.sha256(world.resource.tobytes()+world.energy.tobytes()).hexdigest()}


def summary(rows,key,checkpoint=True):
    values = np.array([(row["checkpoints"][-1] if checkpoint else row["tail_501_600_means"])[key]
                       for row in rows])
    return {"mean":float(values.mean()),"std_across_seeds":float(values.std(ddof=1)),
            "sem":float(values.std(ddof=1)/np.sqrt(len(values))),
            "approx_95pct_interval_mean":[float(values.mean()-2.093*values.std(ddof=1)/np.sqrt(len(values))),
                                          float(values.mean()+2.093*values.std(ddof=1)/np.sqrt(len(values)))],
            "min":float(values.min()),"max":float(values.max())}


def main():
    rows=[run_one(threshold,seed) for threshold in THRESHOLDS for seed in SEEDS]
    assert len(rows)==100 and len(set(x["run_id"] for x in rows))==100
    keys=("mean_energy","mean_resource","floor_fraction","ceiling_fraction",
          "harvest_fraction","raw_unclipped_delta_energy")
    groups={str(threshold):{"n":len(group),"at_600":{key:summary(group,key) for key in keys},
                             "tail_501_600":{key:summary(group,key,False) for key in keys}}
            for threshold in THRESHOLDS
            for group in [[row for row in rows if row["config"]["threshold"]==threshold]]}
    by_config={(r["config"]["threshold"],r["config"]["seed"]):r for r in rows}
    paired={}
    for threshold in THRESHOLDS:
        if threshold==.55: continue
        diffs=np.array([by_config[(threshold,s)]["checkpoints"][-1]["mean_energy"]-
                        by_config[(.55,s)]["checkpoints"][-1]["mean_energy"] for s in SEEDS])
        paired[str(threshold)+"_minus_0.55"]={"mean_energy_difference":float(diffs.mean()),
            "std_across_paired_seeds":float(diffs.std(ddof=1)),
            "approx_95pct_interval_difference":[float(diffs.mean()-2.093*diffs.std(ddof=1)/np.sqrt(20)),
                                                float(diffs.mean()+2.093*diffs.std(ddof=1)/np.sqrt(20))]}
    output={"design":"fixed second sweep; independent of the original 100 neural-world runs",
            "status":"complete","schema":SCHEMA_VERSION,"run_count":len(rows),
            "candidate_thresholds":THRESHOLDS,"seeds":SEEDS,"size":SIZE,"steps":STEPS,
            "policy":"harvest iff pre-step local resource > threshold",
            "laws":"garden.py v01 original; no neural learning; no metabolism change",
            "source_sha256":{"garden.py":digest(HERE/"garden.py"),
                             "threshold_100_sweep.py":digest(Path(__file__))},
            "caveats":["Candidate values were proposed after earlier .55 exploratory results; tuning is not preregistered independent confirmation.",
                       "Random seeds are shared across arms; CI treats seed as unit and is descriptive, not ecological external validity.",
                       "Raw unclipped delta differs from actual delta at energy boundaries.",
                       "This demonstrates heuristic controls, not neural learning or Darwinian evolution."],
            "summary":groups,"paired_vs_0.55":paired,"runs":rows}
    path=HERE/"threshold_100_results.json"
    path.write_text(json.dumps(output,indent=2))
    print(json.dumps({"run_count":len(rows),"summary":{k:{"energy":v["at_600"]["mean_energy"]["mean"],
        "floor":v["at_600"]["floor_fraction"]["mean"],
        "raw_delta":v["at_600"]["raw_unclipped_delta_energy"]["mean"]} for k,v in groups.items()},
        "paired":paired},indent=2))


if __name__=="__main__":
    main()
