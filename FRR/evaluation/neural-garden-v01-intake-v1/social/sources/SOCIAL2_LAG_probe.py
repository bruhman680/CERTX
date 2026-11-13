"""Predeclared causal controls for spatially shared versus delayed local observations."""
import argparse
import copy
import json
from pathlib import Path

import numpy as np

from SOC_ENERGY_AWARE_policy import EnergyAwareGarden

ARMS = ("own_only", "own_previous", "neighbor_previous", "neighbor_current",
        "global_previous", "neighbor_older", "own_older", "neighbor_time_scramble")


def run(seed, regrowth, train_ticks, eval_ticks):
    base = EnergyAwareGarden(seed=seed, size=12, learning=True, regrowth=.06)
    for _ in range(train_ticks):
        base.step()
    global_idx = np.random.default_rng(seed + 990011).permutation(base.count)
    results = {}
    for arm in ARMS:
        g = copy.deepcopy(base)
        g.learning = False
        theta_original = g.theta.copy()
        rng_lag = np.random.default_rng(seed + 990012)
        hist = [g.resource.copy() for _ in range(5)]
        snapshots = {}
        for t in range(1, eval_ticks+1):
            r, e = g.resource.copy(), g.energy.copy()
            nb = g._neighbors(r)
            if arm == "own_only":
                observation = r
            elif arm == "own_previous":
                observation = .5*r+.5*hist[-1]
            elif arm == "neighbor_previous":
                observation = .5*r+.5*g._neighbors(hist[-1])
            elif arm == "neighbor_current":
                observation = .5*r+.5*nb
            elif arm == "global_previous":
                observation = .5*r+.5*hist[-1][global_idx]
            elif arm == "neighbor_older":
                observation = .5*r+.5*g._neighbors(hist[0])
            elif arm == "own_older":
                observation = .5*r+.5*hist[0]
            elif arm == "neighbor_time_scramble":
                lag_idx = rng_lag.integers(0, 5)
                observation = .5*r+.5*g._neighbors(hist[lag_idx])
            else:
                raise ValueError(arm)
            inputs = np.stack((3*(observation-.5),3*(e-.5),np.ones(g.count)),axis=1)
            action = (np.sum(g.theta*inputs,axis=1)>=0.).astype(float)
            g.resource = np.clip(r+.08*(nb-r)+regrowth*(1-r)-.18*r*action,0.,1.)
            g.energy = np.clip(e+.25*r*action-.03-.055*action+.008*(1-action),0.,1.)
            hist.pop(0)
            hist.append(r)
            if t in (500,eval_ticks):
                snapshots[str(t)] = {"mean_energy":float(g.energy.mean()),
                                      "floor":float(np.mean(g.energy<=.01)),
                                      "bottom_decile":float(np.quantile(g.energy,.1)),
                                      "mean_resource":float(g.resource.mean())}
        assert np.array_equal(g.theta, theta_original)
        results[arm] = snapshots
    return {"seed":seed,"regrowth":regrowth,"arms":results}


def aggregate(rows,eval_ticks):
    out={}
    for regrowth in (.06,.055):
        selected=[row for row in rows if row["regrowth"]==regrowth]
        out[str(regrowth)]={}
        for arm in ARMS:
            out[str(regrowth)][arm]={}
            for h in (500,eval_ticks):
                key=str(h)
                obj={metric:float(np.mean([row["arms"][arm][key][metric] for row in selected]))
                     for metric in ("mean_energy","floor","bottom_decile","mean_resource")}
                if arm!="own_only":
                    obj["wins_vs_own_only"]=sum(row["arms"][arm][key]["mean_energy"]>row["arms"]["own_only"][key]["mean_energy"] for row in selected)
                if arm!="own_previous":
                    obj["wins_vs_own_previous"]=sum(row["arms"][arm][key]["mean_energy"]>row["arms"]["own_previous"][key]["mean_energy"] for row in selected)
                if arm!="global_previous":
                    obj["wins_vs_global_previous"]=sum(row["arms"][arm][key]["mean_energy"]>row["arms"]["global_previous"][key]["mean_energy"] for row in selected)
                out[str(regrowth)][arm][key]=obj
    return out


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--seed-start",type=int,default=11000)
    ap.add_argument("--seeds",type=int,default=12)
    ap.add_argument("--train",type=int,default=1500)
    ap.add_argument("--eval",type=int,default=2000)
    ap.add_argument("--output",default="SOCIAL2_LAG_results.json")
    args=ap.parse_args()
    if args.eval<500:raise ValueError("need >=500 evaluation ticks")
    rows=[run(seed,regrowth,args.train,args.eval)
          for seed in range(args.seed_start,args.seed_start+args.seeds)
          for regrowth in (.06,.055)]
    payload={"design":vars(args),"arms":ARMS,"summary":aggregate(rows,args.eval),"rows":rows}
    Path(args.output).write_text(json.dumps(payload,indent=2)+"\n")
    print(json.dumps(payload["summary"],indent=2))


if __name__=="__main__":main()
