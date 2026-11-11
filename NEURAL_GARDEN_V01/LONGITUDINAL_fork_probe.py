"""Matched forks of ONE persistent checkpoint; canonical run is read-only.

The scientific replication unit here is a counterfactual fork of the exact same
world at tick 100, NOT an independent-seed population. This script probes the
continuation mechanics and long-term response to logged interventions.
"""

from __future__ import annotations

import copy
import hashlib
import json
import platform
from pathlib import Path
import tempfile

import numpy as np

from garden import Garden
from threshold_policy import ThresholdGarden

ROOT = Path(__file__).resolve().parent
WORLD = ROOT / "runs" / "living_world" / "state.pkl"
OUTPUT = ROOT / "LONGITUDINAL_fork_results.json"
MILESTONES = (100, 200, 500, 600, 1000, 1500, 2000, 3000)


def observe(garden, action=None, raw_drift=None):
    resource = garden.resource
    act = garden.last_action
    return {
        "tick": int(garden.tick),
        "mean_energy": float(garden.energy.mean()),
        "mean_resource": float(resource.mean()),
        "energy_floor_fraction": float((garden.energy <= .01).mean()),
        "energy_ceiling_fraction": float((garden.energy >= .99).mean()),
        "harvest_rate": float(act.mean()),
        "resource_action_covariance": float(np.mean((resource - resource.mean()) * (act - act.mean()))),
        "raw_energy_drift": None if raw_drift is None else float(raw_drift),
    }


def main():
    canonical = Garden.load(WORLD)
    if canonical.tick != 100:
        raise ValueError(f"Expected archived tick-100 canonical checkpoint, found tick {canonical.tick}")
    anchor = canonical.fingerprint()
    variants = {
        "unchanged_learning": [],
        "learning_off_at_100": [{"tick": 100, "learning": False}],
        "learning_off_at_500": [{"tick": 500, "learning": False}],
        "learning_off_at_1000": [{"tick": 1000, "learning": False}],
        "threshold_graft_at_100": [{"tick": 100, "policy_graft": "threshold_0.55"}],
        "resource_shock_twice": [{"tick": 500, "resource_scale": .4}, {"tick": 1000, "resource_scale": .4}],
        "resource_rescue_once": [{"tick": 500, "resource_scale": 1.5}],
    }
    results = {}
    for label, changes in variants.items():
        garden = copy.deepcopy(canonical)
        if garden.fingerprint() != anchor:
            raise AssertionError("Fork is not an exact initial copy")
        log = []
        if changes and changes[0]["tick"] == garden.tick:
            event = changes[0]
            if "learning" in event:
                garden.learning = bool(event["learning"])
                kind = "learning_toggled"
            elif event.get("policy_graft") == "threshold_0.55":
                # Explicit experimental surgery: change the *controller*
                # implementation while retaining the exact pre-graft world.
                # Do not mistake this for an adapted neural policy.
                garden.__class__ = ThresholdGarden
                garden.learning = False
                garden.threshold = .55
                kind = "controller_grafted"
            else:
                raise AssertionError("unexpected tick-100 intervention")
            log.append({"kind": kind, "tick": garden.tick,
                        "before_fingerprint": anchor, "after_fingerprint": garden.fingerprint()})
        milestones = {100: observe(garden)}
        raw_tail = []
        for tick in range(101, 3001):
            pre_resource = garden.resource.copy()
            garden.step()
            action = garden.last_action
            raw_delta = .25*pre_resource*action - .03 - .055*action + .008*(1.-action)
            raw_tail.append(float(raw_delta.mean()))
            if garden.tick in MILESTONES:
                milestones[garden.tick] = observe(garden, raw_drift=float(raw_delta.mean()))
            for event in changes:
                if event.get("learning") is not None and event["tick"] == garden.tick:
                    before = garden.fingerprint()
                    garden.learning = bool(event["learning"])
                    log.append({"kind": "learning_toggled", "tick": garden.tick,
                                "before_fingerprint": before, "after_fingerprint": garden.fingerprint()})
                if event.get("resource_scale") is not None and event["tick"] == garden.tick:
                    before = garden.fingerprint()
                    garden.resource = np.clip(garden.resource * event["resource_scale"], 0, 1)
                    log.append({"kind": "resource_scaled", "tick": garden.tick,
                                "factor": event["resource_scale"],
                                "before_fingerprint": before,
                                "after_fingerprint": garden.fingerprint()})
                    milestones[garden.tick]["post_intervention_resource"] = float(garden.resource.mean())
        results[label] = {
            "anchor_fingerprint": anchor,
            "final_fingerprint": garden.fingerprint(),
            "final_tick": garden.tick,
            "interventions": log,
            "milestones": milestones,
            "mean_raw_energy_drift_last_500": float(np.mean(raw_tail[-500:])),
        }
    # Independent continuation invariant: split continuation must match a
    # direct continuation, including all learned weights and both RNG streams.
    direct = copy.deepcopy(canonical)
    for _ in range(40):
        direct.step()
    split = copy.deepcopy(canonical)
    for _ in range(17):
        split.step()
    with tempfile.TemporaryDirectory() as temporary:
        path = Path(temporary) / "state.pkl"
        split.save(path)
        split = Garden.load(path)
        for _ in range(23):
            split.step()
    continuity_pass = direct.fingerprint() == split.fingerprint()
    assert continuity_pass
    assert Garden.load(WORLD).fingerprint() == anchor, "Canonical checkpoint changed!"
    payload = {
        "kind": "one_anchor_longitudinal_counterfactuals",
        "anchor_tick": canonical.tick,
        "anchor_fingerprint": anchor,
        "source_sha256": hashlib.sha256((ROOT / "garden.py").read_bytes()).hexdigest(),
        "python_version": platform.python_version(), "numpy_version": np.__version__,
        "milestones": list(MILESTONES),
        "direct_vs_split_resume_fingerprint_equal": continuity_pass,
        "anchor_unchanged": True,
        "results": results,
        "limitations": ["All variants share one initial world and are dependent counterfactuals, not independent experimental replications.",
                        "Resource injections and shocks are deliberate intervention, not emergence or adaptive evolution.",
                        "Mean energy is clipped to [0,1]; low energy and small measured change can hide persistent negative raw energy budget."],
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: {"tick3000_energy":v["milestones"][3000]["mean_energy"],
                          "tick3000_floor":v["milestones"][3000]["energy_floor_fraction"],
                          "tick3000_resource":v["milestones"][3000]["mean_resource"]}
                      for k,v in results.items()}, indent=2))


if __name__ == "__main__":
    main()
