"""Twenty-thousand-tick futures from the canonical Living Garden tick-100 checkpoint.

One historical world, four dependent counterfactual branches. This is a
longitudinal stability probe, NOT an independent-seed statistical study.
"""

from __future__ import annotations

import copy
import hashlib
import json
import platform
from pathlib import Path

import numpy as np

from garden import Garden
from threshold_policy import ThresholdGarden

ROOT = Path(__file__).resolve().parent
CANONICAL = ROOT / "runs" / "living_world" / "state.pkl"
OUTPUT = ROOT / "LONGITUDINAL_20K_results.json"
END = 20_000
MARKS = {100, 200, 500, 1000, 2000, 3000, 5000, 7500, 10000, 12500, 15000, 17500, 20000}
CONFIGS = {
    "original_neural_learning": {"controller": "neural", "shocks": []},
    "threshold_049": {"controller": "threshold", "threshold": .49, "shocks": []},
    "threshold_050": {"controller": "threshold", "threshold": .50, "shocks": []},
    "threshold_051": {"controller": "threshold", "threshold": .51, "shocks": []},
    "threshold_052": {"controller": "threshold", "threshold": .52, "shocks": []},
    "threshold_053": {"controller": "threshold", "threshold": .53, "shocks": []},
    "threshold_054": {"controller": "threshold", "threshold": .54, "shocks": []},
    "threshold_055": {"controller": "threshold", "threshold": .55, "shocks": []},
    "threshold_050_shocked": {"controller": "threshold", "threshold": .50, "shocks": [5000, 10000]},
}


def metrics(g):
    a = g.last_action
    r = g.resource
    return {
        "mean_energy": float(g.energy.mean()),
        "mean_resource": float(r.mean()),
        "floor_fraction": float((g.energy <= .01).mean()),
        "ceiling_fraction": float((g.energy >= .99).mean()),
        "harvest_rate": float(a.mean()),
        "resource_action_covariance": float(np.mean((r-r.mean())*(a-a.mean()))),
    }


def main():
    anchor = Garden.load(CANONICAL)
    if anchor.tick != 100:
        raise ValueError(f"Expected tick100 checkpoint, found {anchor.tick}")
    fingerprint = anchor.fingerprint()
    runs = {}
    for name, cfg in CONFIGS.items():
        g = copy.deepcopy(anchor)
        assert g.fingerprint() == fingerprint
        events = []
        if cfg["controller"] == "threshold":
            before = g.fingerprint()
            g.__class__ = ThresholdGarden
            g.learning = False
            g.threshold = cfg["threshold"]
            events.append({"tick": 100, "kind": "handwritten_policy_graft",
                           "threshold": g.threshold, "prior_fingerprint": before,
                           "post_fingerprint": g.fingerprint()})
        checkpoints = {100: metrics(g)}
        tail_drift = []
        last1000_energy = []
        for tick in range(101, END+1):
            prior_r = g.resource.copy()
            g.step()
            action = g.last_action
            raw_delta = .25*prior_r*action - .03 - .055*action + .008*(1.-action)
            tail_drift.append(float(raw_delta.mean()))
            if len(tail_drift) > 1000:
                tail_drift.pop(0)
            last1000_energy.append(float(g.energy.mean()))
            if len(last1000_energy) > 1000:
                last1000_energy.pop(0)
            if tick in MARKS:
                checkpoints[tick] = metrics(g)
                checkpoints[tick]["raw_drift_mean_last_1000_or_less"] = float(np.mean(tail_drift))
            if tick in cfg["shocks"]:
                before = g.fingerprint()
                g.resource = np.clip(g.resource*.4,0,1)
                events.append({"tick":tick,"kind":"exogenous_resource_shock",
                               "resource_multiplier":.4,
                               "prior_fingerprint":before,
                               "post_fingerprint":g.fingerprint()})
                checkpoints[tick]["post_shock_mean_resource"] = float(g.resource.mean())
        runs[name] = {"config":cfg, "events":events,
                      "checkpoints":checkpoints,
                      "final_state_fingerprint":g.fingerprint(),
                      "final_1000_mean_energy":float(np.mean(last1000_energy)),
                      "final_1000_mean_raw_drift":float(np.mean(tail_drift))}
    assert Garden.load(CANONICAL).fingerprint() == fingerprint
    result = {
        "status":"executed", "experiment":"four_futures_one_historical_world",
        "canonical_source_tick":100,
        "canonical_source_fingerprint":fingerprint,
        "canonical_source_unmodified":True,
        "size":anchor.size,
        "end_tick":END,
        "source_sha256":{
            f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
            for f in ("garden.py","threshold_policy.py","LONGITUDINAL_20K_probe.py")},
        "python":platform.python_version(), "numpy":np.__version__,
        "runs":runs,
        "interpretation_warning":"One selected world, four matched counterfactuals; not independent replicated evidence; threshold controllers are handwritten; energy floor is clipped and low energy is not extinction.",
    }
    OUTPUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({k:{"mean_energy":v["checkpoints"][END]["mean_energy"],
                          "floor":v["checkpoints"][END]["floor_fraction"],
                          "last1000_raw_drift":v["final_1000_mean_raw_drift"]}
                      for k,v in runs.items()},indent=2))


if __name__=="__main__":
    main()
