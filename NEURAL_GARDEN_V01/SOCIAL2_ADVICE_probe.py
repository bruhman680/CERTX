"""Non-destructive spatial observation sharing for fixed neural policies."""
import argparse
import copy
import json
from pathlib import Path

import numpy as np

from SOC_ENERGY_AWARE_policy import EnergyAwareGarden

ARMS = ("own", "local_mean", "random_neighbor", "global_shuffle", "stale_local")


def run(seed, regrowth, train_ticks, eval_ticks):
    original = EnergyAwareGarden(seed=seed, size=12, learning=True, regrowth=.06)
    for _ in range(train_ticks):
        original.step()
    result = {}
    idx = np.arange(original.count).reshape(original.size, original.size)
    neighbor_idxs = np.stack((np.roll(idx, 1, 0), np.roll(idx, -1, 0),
                              np.roll(idx, 1, 1), np.roll(idx, -1, 1)), axis=-1).reshape(-1, 4)
    donor_random = np.random.default_rng(seed + 900000).integers(0, 4, original.count)
    donor_random = neighbor_idxs[np.arange(original.count), donor_random]
    shuffled = np.random.default_rng(seed + 900001).permutation(original.count)
    for arm in ARMS:
        g = copy.deepcopy(original)
        g.learning = False
        g.regrowth = regrowth
        before_theta = g.theta.copy()
        stale = g._neighbors(g.resource)
        checks = {}
        for t in range(1, eval_ticks + 1):
            r = g.resource.copy()
            e = g.energy.copy()
            current_neighbors = g._neighbors(r)
            if arm == "own":
                observed = r
            elif arm == "local_mean":
                observed = .5*r + .5*current_neighbors
            elif arm == "random_neighbor":
                observed = .5*r + .5*r[donor_random]
            elif arm == "global_shuffle":
                observed = .5*r + .5*r[shuffled]
            elif arm == "stale_local":
                observed = .5*r + .5*stale
            else:
                raise ValueError(arm)
            features = np.stack((3*(observed-.5), 3*(e-.5), np.ones(g.count)), axis=1)
            action = (np.sum(g.theta*features, axis=1) >= 0.).astype(float)
            g.resource = np.clip(r + .08*(current_neighbors-r) + regrowth*(1-r) -.18*r*action, 0., 1.)
            g.energy = np.clip(e+.25*r*action-.03-.055*action+.008*(1-action), 0., 1.)
            stale = current_neighbors
            if t in (500, eval_ticks):
                checks[str(t)] = {"mean_energy": float(g.energy.mean()),
                                  "floor": float(np.mean(g.energy <= .01)),
                                  "bottom_decile": float(np.quantile(g.energy,.1)),
                                  "mean_resource": float(g.resource.mean())}
        assert np.array_equal(g.theta, before_theta), "social observations must not modify neural weights"
        result[arm] = checks
    return {"seed": seed, "regrowth": regrowth, "arms": result}


def aggregate(rows, eval_ticks):
    out = {}
    for regime in (.06,.055):
        sr = [x for x in rows if x["regrowth"] == regime]
        out[str(regime)] = {}
        for arm in ARMS:
            out[str(regime)][arm] = {}
            for horizon in (500, eval_ticks):
                key = str(horizon)
                obj = {metric:float(np.mean([x["arms"][arm][key][metric] for x in sr]))
                       for metric in ("mean_energy", "floor", "bottom_decile", "mean_resource")}
                if arm != "own":
                    obj["wins_vs_own"] = sum(x["arms"][arm][key]["mean_energy"] > x["arms"]["own"][key]["mean_energy"] for x in sr)
                if arm not in ("own", "global_shuffle"):
                    obj["wins_vs_shuffle"] = sum(x["arms"][arm][key]["mean_energy"] > x["arms"]["global_shuffle"][key]["mean_energy"] for x in sr)
                out[str(regime)][arm][key] = obj
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed-start",type=int,default=10800)
    ap.add_argument("--seeds",type=int,default=12)
    ap.add_argument("--train",type=int,default=1500)
    ap.add_argument("--eval",type=int,default=2000)
    ap.add_argument("--output",default="SOCIAL2_ADVICE_results.json")
    args = ap.parse_args()
    if args.eval < 500:
        raise ValueError("Evaluation requires at least 500 ticks")
    rows = [run(seed,regime,args.train,args.eval)
            for seed in range(args.seed_start,args.seed_start+args.seeds)
            for regime in (.06,.055)]
    payload = {"design":vars(args),"arms":ARMS,"summary":aggregate(rows,args.eval),"rows":rows}
    Path(args.output).write_text(json.dumps(payload,indent=2)+"\n")
    print(json.dumps(payload["summary"],indent=2))


if __name__ == "__main__":
    main()
