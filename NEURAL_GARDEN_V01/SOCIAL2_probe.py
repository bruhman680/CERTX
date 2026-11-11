"""Controlled policy copying among toroidal neighboring neural cells.

All learned theta originate in identical per-seed teacher-free training;
subsequent deployment is deterministic and policy-gradient updates are off.
"""
import argparse
import copy
import json
from pathlib import Path

import numpy as np

from SOC_ENERGY_AWARE_policy import EnergyAwareGarden


ARMS = ("none", "top_neighbor", "bottom_neighbor", "random_neighbor", "global_shuffle", "neighbor_mean")


def transplant(g, arm, seed):
    donor = g.theta.copy()
    if arm == "none":
        return {"mean_l2_change": 0., "donor_energy_advantage": 0.}
    rng = np.random.default_rng(seed + 800000)
    n = g.size
    ii = np.arange(n * n).reshape(n, n)
    neighbors = np.stack((np.roll(ii, 1, 0), np.roll(ii, -1, 0),
                          np.roll(ii, 1, 1), np.roll(ii, -1, 1)), axis=-1).reshape(-1, 4)
    if arm == "top_neighbor":
        chosen = neighbors[np.arange(g.count), np.argmax(g.energy[neighbors], axis=1)]
    elif arm == "bottom_neighbor":
        chosen = neighbors[np.arange(g.count), np.argmin(g.energy[neighbors], axis=1)]
    elif arm == "random_neighbor":
        chosen = neighbors[np.arange(g.count), rng.integers(0, 4, g.count)]
    elif arm == "global_shuffle":
        chosen = rng.permutation(g.count)
    elif arm == "neighbor_mean":
        g.theta = donor[neighbors].mean(axis=1)
        return {"mean_l2_change": float(np.linalg.norm(g.theta - donor, axis=1).mean()),
                "donor_energy_advantage": float((g.energy[neighbors].mean(axis=1) - g.energy).mean())}
    else:
        raise ValueError(arm)
    g.theta = donor[chosen].copy()
    return {"mean_l2_change": float(np.linalg.norm(g.theta - donor, axis=1).mean()),
            "donor_energy_advantage": float((g.energy[chosen] - g.energy).mean())}


def run(seed, regrowth, train_ticks, eval_ticks, period=0):
    base = EnergyAwareGarden(seed=seed, size=12, learning=True, regrowth=.06)
    for _ in range(train_ticks):
        base.step()
    arms = {}
    for arm in ARMS:
        g = copy.deepcopy(base)
        g.learning = False
        g.regrowth = regrowth
        info = transplant(g, arm, seed)
        # Deterministic action, frozen weights: reuses original environment law.
        for t in range(eval_ticks):
            if period and t and t % period == 0:
                transplant(g, arm, seed + t)
            r, e = g.resource.copy(), g.energy.copy()
            features = np.stack((3*(r-.5), 3*(e-.5), np.ones(g.count)), axis=1)
            action = (np.sum(g.theta * features, axis=1) >= 0).astype(float)
            g.resource = np.clip(r + .08*(g._neighbors(r)-r) + regrowth*(1-r) - .18*r*action, 0., 1.)
            g.energy = np.clip(e + .25*r*action - .03 - .055*action + .008*(1-action), 0., 1.)
        arms[arm] = {**info, "mean_energy": float(g.energy.mean()),
                     "floor": float(np.mean(g.energy <= .01)),
                     "bottom_decile": float(np.quantile(g.energy, .1)),
                     "mean_resource": float(g.resource.mean()),
                     "theta_dispersion": float(np.mean(np.std(g.theta, axis=0))),
                     "transfer_events": 0 if arm == "none" else 1 + (eval_ticks - 1)//period if period else int(arm != "none")}
    return {"seed": seed, "regrowth": regrowth, "arms": arms}


def aggregate(rows):
    out = {}
    for regrowth in (.06, .055):
        selected = [r for r in rows if r["regrowth"] == regrowth]
        out[str(regrowth)] = {}
        for arm in ARMS:
            obj = {metric: float(np.mean([r["arms"][arm][metric] for r in selected]))
                   for metric in ("mean_energy", "floor", "bottom_decile", "mean_resource", "mean_l2_change", "donor_energy_advantage")}
            if arm != "none":
                obj["paired_wins_vs_none"] = sum(r["arms"][arm]["mean_energy"] > r["arms"]["none"]["mean_energy"] for r in selected)
            if arm not in ("none", "random_neighbor"):
                obj["paired_wins_vs_random_neighbor"] = sum(r["arms"][arm]["mean_energy"] > r["arms"]["random_neighbor"]["mean_energy"] for r in selected)
            out[str(regrowth)][arm] = obj
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=12)
    ap.add_argument("--seed-start", type=int, default=10400)
    ap.add_argument("--train", type=int, default=1500)
    ap.add_argument("--eval", type=int, default=3000)
    ap.add_argument("--period", type=int, default=0, help="Repeat social copying every N ticks; 0 means one initial copy")
    ap.add_argument("--output", default="SOCIAL2_results.json")
    args = ap.parse_args()
    rows = [run(seed, regrowth, args.train, args.eval, args.period)
            for seed in range(args.seed_start, args.seed_start + args.seeds)
            for regrowth in (.06, .055)]
    result = {"design": {"seeds": args.seeds, "seed_start": args.seed_start,
                         "train_ticks": args.train, "eval_ticks": args.eval, "period": args.period,
                         "arms": ARMS, "regrowths": [.06, .055]},
              "summary": aggregate(rows), "rows": rows}
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result["summary"], indent=2))


if __name__ == "__main__":
    main()
