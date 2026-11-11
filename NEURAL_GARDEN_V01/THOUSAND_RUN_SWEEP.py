"""Matched-seed, same-world 1,000-run Neural Garden comparison.

Four policy arms, 250 seeds per arm, 600 ticks each. Persistent JSONL rows
make this long bounded batch resumable after interruption. No hidden tuning.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import statistics
import sys
from pathlib import Path

import numpy as np

from garden import Garden
from stewardship_garden import StewardshipGarden
from threshold_policy import ThresholdGarden

ROOT = Path(__file__).resolve().parent
ARMS = ["v01_learning", "v01_frozen", "v02_stewardship", "threshold_055"]
SEEDS = range(300, 550)
SIZE = 16
STEPS = 600
CHECKPOINTS = {0, 100, 200, 400, 600}
DATA = ROOT / "THOUSAND_RUN_ROWS.jsonl"
META = ROOT / "THOUSAND_RUN_META.json"
RESULT = ROOT / "THOUSAND_RUN_RESULTS.json"
FILES = ["garden.py", "stewardship_garden.py", "threshold_policy.py", "THOUSAND_RUN_SWEEP.py"]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def metadata():
    return {"experiment": "garden-matched-1000-v1", "arms": ARMS,
            "seeds": [300, 549], "count_per_arm": 250,
            "steps": STEPS, "size": SIZE,
            "checkpoints": sorted(CHECKPOINTS),
            "source_sha256": {name: sha((ROOT / name).read_bytes()) for name in FILES},
            "runtime": {"python": sys.version, "numpy": np.__version__,
                        "platform": platform.platform()},
            "note": "Synthetic toy world; four controllers under identical original environmental laws. Existing models unchanged."
           }


def construct(arm, seed):
    if arm == "v01_learning":
        return Garden(seed=seed, size=SIZE, learning=True)
    if arm == "v01_frozen":
        return Garden(seed=seed, size=SIZE, learning=False)
    if arm == "v02_stewardship":
        return StewardshipGarden(seed=seed, size=SIZE, learning=True)
    if arm == "threshold_055":
        return ThresholdGarden(seed=seed, size=SIZE, threshold=.55)
    raise ValueError(arm)


def snapshot(g):
    x = dict(g.metrics())
    x.update({"fraction_floor": float(np.mean(g.energy <= .01)),
              "fraction_ceiling": float(np.mean(g.energy >= .99)),
              "energy_std": float(np.std(g.energy)),
              "resource_std": float(np.std(g.resource))})
    return x


def one_run(arm, seed):
    g = construct(arm, seed)
    trajectory = [{"tick": 0, **snapshot(g)}]
    drift_sum = covariance_sum = harvest_sum = 0.
    tail_drift_sum = tail_cov_sum = tail_harvest_sum = 0.
    for tick in range(1, STEPS + 1):
        resources = g.resource.copy()
        g.step()
        actions = g.last_action
        raw = .25 * resources * actions - .03 - .055 * actions + .008 * (1. - actions)
        covariance = float(np.mean(resources * actions) - np.mean(resources) * np.mean(actions))
        raw_drift = float(raw.mean())
        harvest = float(actions.mean())
        drift_sum += raw_drift
        covariance_sum += covariance
        harvest_sum += harvest
        if tick > STEPS - 100:
            tail_drift_sum += raw_drift
            tail_cov_sum += covariance
            tail_harvest_sum += harvest
        if tick in CHECKPOINTS:
            trajectory.append({"tick": tick, **snapshot(g),
                               "raw_drift_this_tick": raw_drift,
                               "resource_action_covariance": covariance})
    config = {"arm": arm, "seed": seed, "steps": STEPS, "size": SIZE}
    return {"run_id": f"{arm}__seed_{seed}", "arm": arm, "seed": seed,
            "config_sha256": sha(json.dumps(config, sort_keys=True).encode()),
            "trajectory": trajectory, "final": trajectory[-1],
            "raw_drift_mean": drift_sum / STEPS,
            "resource_action_covariance_mean": covariance_sum / STEPS,
            "harvest_rate_mean": harvest_sum / STEPS,
            "tail_100_raw_drift_mean": tail_drift_sum / 100,
            "tail_100_resource_action_covariance_mean": tail_cov_sum / 100,
            "tail_100_harvest_mean": tail_harvest_sum / 100,
            "state_fingerprint": g.fingerprint()}


def atomic_json(path, obj):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(tmp, path)


def load_rows():
    rows = {}
    if not DATA.exists():
        return rows
    # Only complete lines are written by our writer. A partial trailing line
    # after an unclean termination is discarded before further appends.
    with DATA.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.endswith("\n"):
                break
            row = json.loads(line)
            if row["run_id"] in rows:
                raise ValueError("duplicate run ID in archival JSONL")
            rows[row["run_id"]] = row
    return rows


def aggregate(rows):
    fields = ["mean_energy", "mean_resource", "harvest_rate", "fraction_floor", "fraction_ceiling"]
    fields += ["raw_drift_mean", "resource_action_covariance_mean", "tail_100_raw_drift_mean"]
    output = {}
    for arm in ARMS:
        subset = [r for r in rows if r["arm"] == arm]
        values = {}
        for field in fields:
            numbers = [r["final"][field] if field in r["final"] else r[field] for r in subset]
            values[field] = {"mean": statistics.fmean(numbers),
                             "sd": statistics.stdev(numbers) if len(numbers)>1 else None,
                             "min": min(numbers), "max": max(numbers)}
        output[arm] = {"n": len(subset), "values": values}
    seedmaps = {arm: {r["seed"]:r for r in rows if r["arm"] == arm} for arm in ARMS}
    paired = {}
    for left,right in [("v01_learning","v01_frozen"),
                       ("v02_stewardship","v01_learning"),
                       ("threshold_055","v01_learning"),
                       ("threshold_055","v02_stewardship")]:
        pairs = sorted(set(seedmaps[left]) & set(seedmaps[right]))
        delta = [seedmaps[left][s]["final"]["mean_energy"] - seedmaps[right][s]["final"]["mean_energy"] for s in pairs]
        paired[f"{left}_minus_{right}"] = {"n":len(delta),"mean":statistics.fmean(delta),
             "sd":statistics.stdev(delta) if len(delta)>1 else None}
    return output, paired


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--max-runs",type=int, default=1000,help="maximum total runs in this invocation")
    args=parser.parse_args()
    current=metadata()
    if META.exists():
        old=json.loads(META.read_text(encoding="utf-8"))
        if old != current:
            raise RuntimeError("source or environment changed since this archival batch was initialized")
    else:
        if DATA.exists():
            raise RuntimeError("orphan rows without metadata; stopping for audit")
        atomic_json(META,current)
    rows=load_rows()
    if rows:
        print(f"Resuming {len(rows)} archived complete runs",flush=True)
    completed=0
    with DATA.open("a",encoding="utf-8") as output:
        for arm in ARMS:
            for seed in SEEDS:
                run_id=f"{arm}__seed_{seed}"
                if run_id in rows:
                    continue
                if completed>=args.max_runs:
                    break
                row=one_run(arm,seed)
                output.write(json.dumps(row,separators=(",",":"),allow_nan=False)+"\n")
                output.flush()
                os.fsync(output.fileno())
                rows[run_id]=row
                completed+=1
                if len(rows)%25==0:
                    print(f"archived {len(rows)}/1000 runs",flush=True)
            if completed>=args.max_runs:
                break
    if len(rows)==1000:
        ordered=[rows[f"{arm}__seed_{seed}"] for arm in ARMS for seed in SEEDS]
        summary,paired=aggregate(ordered)
        result={**current,"status":"completed","total_runs":len(ordered),
                "summary":summary,"paired_contrasts":paired,"runs_sha256":sha(DATA.read_bytes()),
                "limitations":"Matched seeds and same world laws, but stochastic controllers diverge. Threshold selected after earlier exploration. No reproduction or mutation. Within-simulator evidence only."}
        atomic_json(RESULT,result)
        print(json.dumps({"status":"completed","total_runs":1000,"summary":summary,"paired":paired}))
    else:
        print(f"Incomplete batch: {len(rows)}/1000 runs archived; rerun to resume",flush=True)


if __name__=="__main__":
    main()
