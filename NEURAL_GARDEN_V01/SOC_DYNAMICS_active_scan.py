"""Sequential physics research society: 40 evidence-updated threshold experiments.

Each research loop selects a NEW threshold based on prior outcomes, states its
uncertainty-driven hypothesis, runs several matched seeded worlds, and records
whether the observed score beat the previous incumbent. Four explicitly labeled
world-law regimes each get ten sequential loops. Independent held-out seeds
check the top candidates only after the adaptive search completes.

The simulation is a vectorized replay of the original resource/energy laws.
No neural or biological evolution is claimed. Author: experimental scout.
"""
from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import numpy as np

from threshold_policy import ThresholdGarden


ROOT = Path(__file__).resolve().parent
REGIMES = {
    "original": {"regrowth": 0.06, "consumption": 0.18, "diffusion": 0.08},
    "no_diffusion": {"regrowth": 0.06, "consumption": 0.18, "diffusion": 0.0},
    "less_regrowth": {"regrowth": 0.055, "consumption": 0.18, "diffusion": 0.08},
    "more_consumption": {"regrowth": 0.06, "consumption": 0.185, "diffusion": 0.08},
}
TICKS = 3500
TAIL = 500
SEEDS = (4040, 4041, 4042)
HOLDOUT = (4500, 4501, 4502, 4503, 4504)


def simulate(seed, threshold, law, ticks=TICKS):
    g = ThresholdGarden(seed=seed, size=16, threshold=threshold)
    raw = []
    resource_action = []
    harvest = []
    for t in range(ticks):
        before = g.resource
        action = (before > threshold).astype(np.float64)
        if t >= ticks - TAIL:
            raw.append(float((.25 * before * action - .063 * action - .022).mean()))
            resource_action.append(float((before * action).mean()))
            harvest.append(float(action.mean()))
        diffusion = law["diffusion"] * (g._neighbors(before) - before)
        next_r = np.clip(before + diffusion + law["regrowth"] * (1-before)
                         - law["consumption"] * before * action, 0, 1)
        next_e = np.clip(g.energy + .25 * before * action - .063 * action - .022, 0, 1)
        g.resource = next_r
        g.energy = next_e
        g.tick += 1
    return {
        "energy": float(g.energy.mean()),
        "resource": float(g.resource.mean()),
        "floor": float((g.energy <= .01).mean()),
        "ceiling": float((g.energy >= .99).mean()),
        "tail_raw_drift": float(np.mean(raw)),
        "tail_harvest": float(np.mean(harvest)),
        "tail_resource_action": float(np.mean(resource_action)),
    }


def invariant():
    law = REGIMES["original"]
    seed, threshold = 91919, .50
    g = ThresholdGarden(seed=seed, threshold=threshold)
    q = ThresholdGarden(seed=seed, threshold=threshold)
    for _ in range(100):
        g.step()
        before = q.resource
        a = (before > threshold).astype(float)
        q.energy = np.clip(q.energy + .25 * before * a - .063 * a - .022, 0, 1)
        q.resource = np.clip(before + law["diffusion"] * (q._neighbors(before)-before)
                             + law["regrowth"]*(1-before)-law["consumption"]*before*a, 0, 1)
        q.tick += 1
    # Algebraically equivalent raw-energy expression changes floating operation
    # grouping; tolerate roundoff, but no measurable law discrepancy.
    if not (np.allclose(g.resource,q.resource,rtol=0,atol=1e-12)
            and np.allclose(g.energy,q.energy,rtol=0,atol=1e-12)):
        raise AssertionError("Vectorized physics deviates from threshold baseline")


def candidate(previous, stage):
    """Select new threshold from optimism + distance-to-tested exploration."""
    if stage < 3:
        return (.475, .5, .525)[stage], "calibration_anchor"
    xs = np.array([v["threshold"] for v in previous])
    ys = np.array([v["objective"] for v in previous])
    order = np.argsort(xs)
    grid = np.linspace(.43, .56, 521)
    estimate = np.interp(grid, xs[order], ys[order])
    uncertainty = np.min(np.abs(grid[:,None]-xs[None,:]),axis=1)
    # The optimism coefficient decreases as the regime becomes better mapped.
    bonus = (0.15 / (1 + stage / 3)) * uncertainty / .04
    acq = estimate + bonus
    acq[uncertainty < .00015] = -np.inf
    return float(grid[int(np.argmax(acq))]), "highest_predicted_score_plus_exploration"


def run():
    invariant()
    loops = []
    regime_summary = {}
    for regime, law in REGIMES.items():
        local = []
        for stage in range(10):
            trial, rationale = candidate(local, stage)
            previous_best = max((x["objective"] for x in local), default=None)
            rows = [simulate(s, trial, law) for s in SEEDS]
            m = {key: float(np.mean([r[key] for r in rows])) for key in rows[0]}
            # Objective is ecological mean energy while penalizing floor losses.
            objective = float(m["energy"] - .25*m["floor"])
            accepted = previous_best is None or objective > previous_best
            entry = {
                "loop": len(loops)+1,
                "regime": regime,
                "orientation": "Improve retained mean energy without hiding depleted cells",
                "hypothesis": "New candidate threshold will improve incumbent" if stage > 0 else "Locate first viable region",
                "selection_reason": rationale,
                "threshold": trial,
                "prior_best_score": previous_best,
                "metrics": m,
                "seed_rows": rows,
                "objective": objective,
                "improved_incumbent": bool(accepted),
                "inference": ("New best candidate under the declared score" if accepted
                              else "Candidate rejected by observed score; uncertainty narrowed"),
                "next_orientation": "Select an untested threshold balancing predicted score and uncertainty",
            }
            local.append(entry)
            loops.append(entry)
        best = max(local,key=lambda v:v["objective"])
        # Holdout has not participated in candidate selection.
        comparators = sorted(set([round(best["threshold"],5),.50,.51,.525,.55]))
        holdout = {}
        for th in comparators:
            rows = [simulate(s, th, law, ticks=5000) for s in HOLDOUT]
            holdout[str(th)] = {
                "mean_energy": float(np.mean([x["energy"] for x in rows])),
                "mean_floor": float(np.mean([x["floor"] for x in rows])),
                "mean_raw_drift":float(np.mean([x["tail_raw_drift"] for x in rows])),
                "seed_rows":rows,
            }
        regime_summary[regime] = {
            "law":law, "best_screened_threshold":best["threshold"],
            "best_screened_objective":best["objective"],
            "successful_incumbent_updates":sum(int(x["improved_incumbent"]) for x in local),
            "holdout":holdout,
        }
    result = {
        "description":"40 sequential hypothesis-and-probe research loops; four regimes ×10 adaptive threshold decisions; no neural learning",
        "status":"completed",
        "loop_count":len(loops),
        "run_count":40*len(SEEDS) + sum(len(v["holdout"])*len(HOLDOUT) for v in regime_summary.values()),
        "seeds_screen":SEEDS,"seeds_holdout":HOLDOUT,
        "size":16,"ticks_screen":TICKS,"ticks_holdout":5000,
        "regimes":regime_summary,"loops":loops,
        "python_version":platform.python_version(),"numpy_version":np.__version__,
        "source_sha256":{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in
                         ("garden.py","threshold_policy.py","SOC_DYNAMICS_active_scan.py")},
    }
    destination=ROOT/"SOC_DYNAMICS_results.json"
    destination.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"loops":len(loops),"runs":result["run_count"],
                      "best":{r:(v["best_screened_threshold"],v["holdout"][str(v["best_screened_threshold"])]["mean_energy"])
                              for r,v in regime_summary.items()}},indent=2))


if __name__ == "__main__":
    run()
