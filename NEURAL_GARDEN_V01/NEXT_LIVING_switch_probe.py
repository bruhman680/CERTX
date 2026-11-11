"""Exact-fork longitudinal counterfactuals; never advance canonical Garden."""

from __future__ import annotations

import copy
import hashlib
import json
from collections import deque
from pathlib import Path

import numpy as np

from garden import Garden
from SOC_LONGITUDINAL_explore import PolicyFork


ROOT = Path(__file__).resolve().parent
ANCHOR = ROOT / "runs/living_world/state.pkl"
OUTPUT = ROOT / "NEXT_LIVING_switch_results.json"
MILESTONES = (100, 200, 500, 1000, 3000, 5000, 7000, 10000)
POLICIES = {
    "fixed050": {"kind": "fixed", "theta": .50},
    "rescue": {"kind": "energy_rescue", "theta": .51,
               "low_energy": .12, "discount": .025},
    "reverse": {"kind": "energy_rescue", "theta": .51,
                "low_energy": .12, "discount": -.025},
}


def switch(g, mode, reset_hidden=False):
    """Switch controller without changing physical state or inherited weights."""
    prior = g.fingerprint()
    if mode == "learned":
        g.__class__ = Garden
        g.learning = True
        if reset_hidden:
            g.hidden[:] = 0.
    else:
        g = PolicyFork(g, POLICIES[mode])
        g.learning = False
    return g, {"mode": mode, "fingerprint_before": prior,
               "fingerprint_after": g.fingerprint(),
               "reset_hidden": reset_hidden}


def summarize(g, raw_tail):
    return {
        "energy": float(g.energy.mean()),
        "resource": float(g.resource.mean()),
        "floor": float(np.mean(g.energy <= .01)),
        "high_energy": float(np.mean(g.energy >= .5)),
        "ceiling": float(np.mean(g.energy >= .99)),
        "raw_drift_tail": float(np.mean(raw_tail)) if raw_tail else None,
    }


def simulate(anchor, schedule, shocks=None, horizon=10000, reset_modes=()):
    g = copy.deepcopy(anchor)
    base = g.fingerprint()
    events = []
    checkpoints = {str(g.tick): summarize(g, ())}
    tails = deque(maxlen=1000)
    shocks = shocks or {}
    for tick in range(g.tick + 1, horizon + 1):
        if tick in schedule:
            g, event = switch(g, schedule[tick], reset_hidden=tick in reset_modes)
            event["tick"] = tick
            event["kind"] = "explicit_policy_switch"
            events.append(event)
        before_r = g.resource.copy()
        g.step()
        action = g.last_action
        delta = .25*before_r*action-.03-.055*action+.008*(1.-action)
        tails.append(float(delta.mean()))
        if g.tick in MILESTONES:
            checkpoints[str(g.tick)] = summarize(g, tails)
        if g.tick in shocks:
            factor = shocks[g.tick]
            g.resource = np.clip(g.resource * factor, 0, 1)
            events.append({"kind": "exogenous_shock", "tick": g.tick,
                           "resource_multiplier": factor})
    return {"schedule": schedule, "shock_ticks": shocks,
            "events": events, "start_fingerprint": base,
            "checkpoints": checkpoints, "final": summarize(g, tails),
            "final_fingerprint": g.fingerprint()}


def run():
    anchor = Garden.load(ANCHOR)
    assert anchor.tick == 100
    fp = anchor.fingerprint()
    configs = {
        "original_neural": ({}, {}),
        "fixed050_from_100": ({101: "fixed050"}, {}),
        "rescue_from_100": ({101: "rescue"}, {}),
        "reverse_from_100": ({101: "reverse"}, {}),
        "learn500_then_rescue": ({501: "rescue"}, {}),
        "learn1000_then_rescue": ({1001: "rescue"}, {}),
        "rescue5000_then_relearn": ({101: "rescue", 5001: "learned"}, {}),
        "rescue5000_then_relearn_reset": ({101: "rescue", 5001: "learned"}, {}),
        "fixed050_two_shocks": ({101: "fixed050"}, {5000:.7, 7000:.7}),
        "rescue_two_shocks": ({101: "rescue"}, {5000:.7, 7000:.7}),
        "fixed_then_rescue_at_first_shock": ({101:"fixed050",5001:"rescue"}, {5000:.7, 7000:.7}),
    }
    results = {}
    for name, (schedule, shocks) in configs.items():
        resets = (5001,) if name.endswith("_reset") else ()
        results[name] = simulate(anchor, schedule, shocks, reset_modes=resets)
    assert Garden.load(ANCHOR).fingerprint() == fp
    hashes = {name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
              for name in ("garden.py", "SOC_LONGITUDINAL_explore.py",
                           "NEXT_LIVING_switch_probe.py")}
    return {"status": "executed", "canonical_tick":100,
            "canonical_fingerprint_before_after":fp,
            "canonical_unchanged":True, "size":16,
            "horizon":10000, "source_sha256": hashes,
            "runs": results,
            "caution": "One historical seed and dependent exact-state counterfactuals. Handwritten policy switches, not neural discoveries. Resetting hidden state alone does not reset weights; period outcomes can be confounded by depletion before switch."}


if __name__ == "__main__":
    payload = run()
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True)+"\n")
    print(json.dumps({k:{"energy":v["final"]["energy"],"floor":v["final"]["floor"]}
                      for k,v in payload["runs"].items()}, indent=2))
