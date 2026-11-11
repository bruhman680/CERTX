"""Bounded, independent checks for Neural Garden v0.1.

No inference of general intelligence or biological learning is intended.
Runs paired initial seeds under learning/frozen policies, independent prediction
probes when exposed by Garden, and deterministic checkpoint replay.
"""

import argparse
import json
import math
import tempfile
from pathlib import Path
import numpy as np

from garden import Garden


def scalar(x):
    if isinstance(x, bool):
        return x
    if isinstance(x, (int, float)):
        return float(x)
    try:
        return float(x.item())
    except (TypeError, ValueError, AttributeError):
        return None


def safe_metrics(world):
    out = {}
    for key, value in world.metrics().items():
        val = scalar(value)
        if val is not None and math.isfinite(val):
            out[key] = val
    return out


def fingerprint(world):
    fn = getattr(world, "fingerprint", None)
    return fn() if callable(fn) else None


def heldout_common_world_probe(model_world, seed, length=80):
    """Score frozen cell predictors on one independent, identical world trace.

    This is a fixed observational transfer test. It retains no weights/hidden
    state from the training world except trained parameters; probe hidden state
    begins at zero and evolves on the reference stream. It is NOT a guarantee
    of generalization to arbitrary dynamics or controlled counterfactuals.
    """
    reference = Garden(seed=900000 + seed, size=model_world.size, learning=False)
    h = np.zeros_like(model_world.hidden)
    errors = []
    for _ in range(length):
        resource = reference.resource.copy()
        energy = reference.energy.copy()
        obs = np.stack([
            resource, energy, reference._neighbors(resource),
            reference._neighbors(energy), reference.prev_action,
            np.clip(reference.prev_reward * 5., -1., 1.),
            np.ones(reference.count),
        ], axis=1)
        h = np.tanh(np.einsum('ni,nih->nh', obs, model_world.win)
                    + np.einsum('ni,nih->nh', h, model_world.wrec)
                    + model_world.bhidden)
        predicted = model_world._sigmoid(np.einsum('nh,nh->n', h, model_world.wpred)
                                         + model_world.bpred)
        reference.step()
        errors.append(float(np.mean((predicted-reference.resource)**2)))
    return float(np.mean(errors))


def run_one(seed, size, steps, learning, probe_count):
    world = Garden(seed=seed, size=size, learning=learning)
    initial = safe_metrics(world)
    history = []
    before_probe = None
    if callable(getattr(world, "prediction_probe", None)):
        before_probe = scalar(world.prediction_probe(seed=100000 + seed, n=probe_count))
    for i in range(steps):
        world.step()
        if (i + 1) % max(1, steps // 10) == 0:
            history.append({"step": i + 1, "metrics": safe_metrics(world)})
    after = safe_metrics(world)
    after_probe = None
    if callable(getattr(world, "prediction_probe", None)):
        after_probe = scalar(world.prediction_probe(seed=100000 + seed, n=probe_count))
    common_probe_mse = heldout_common_world_probe(world, seed)
    return {"seed": seed, "learning": learning, "initial": initial, "final": after,
            "history": history, "initial_probe": before_probe,
            "final_probe": after_probe, "common_world_probe_mse": common_probe_mse,
            "fingerprint": fingerprint(world)}


def resume_test(seed, size, warmup=17, continuation=13):
    direct = Garden(seed=seed, size=size, learning=True)
    to_save = Garden(seed=seed, size=size, learning=True)
    for _ in range(warmup):
        direct.step()
        to_save.step()
    fp_before_direct, fp_before_split = fingerprint(direct), fingerprint(to_save)
    pre_agrees = fp_before_direct == fp_before_split if fp_before_direct is not None else (safe_metrics(direct) == safe_metrics(to_save))
    with tempfile.TemporaryDirectory(prefix="garden-eval-") as tmp:
        save_path = Path(tmp) / "state.chk"
        to_save.save(save_path)
        resumed = Garden.load(save_path)
        fp_reload = fingerprint(resumed)
        reload_agrees = fp_reload == fp_before_direct if fp_before_direct is not None else (safe_metrics(resumed) == safe_metrics(direct))
        trace_agrees = True
        for _ in range(continuation):
            direct.step()
            resumed.step()
            f1, f2 = fingerprint(direct), fingerprint(resumed)
            if f1 is not None:
                trace_agrees &= f1 == f2
            else:
                trace_agrees &= safe_metrics(direct) == safe_metrics(resumed)
    return {"seed": seed, "warmup": warmup, "continuation": continuation,
            "initial_identical": pre_agrees, "reload_identical": reload_agrees,
            "continued_identical": bool(trace_agrees),
            "comparison_depth": "full-state fingerprint" if fp_before_direct is not None else "metrics only"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--size", type=int, default=12)
    ap.add_argument("--steps", type=int, default=200)
    ap.add_argument("--seeds", type=int, nargs="+", default=[7, 17, 29, 43, 61])
    ap.add_argument("--probe-count", type=int, default=256)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    records = []
    for seed in args.seeds:
        records.append({"seed": seed,
                        "learned": run_one(seed, args.size, args.steps, True, args.probe_count),
                        "frozen": run_one(seed, args.size, args.steps, False, args.probe_count)})
    checks = [resume_test(seed, args.size) for seed in args.seeds[:3]]
    report = {"protocol": "Neural Garden v0.1 bounded paired seeds and checkpoint replay",
              "size": args.size, "steps": args.steps, "records": records,
              "resume_tests": checks,
              "limitations": ["Paired initial seeds do not imply paired identical world trajectories after cell actions diverge.",
                              "Prediction probe is informative only if it measures held-out targets under fixed inputs.",
                              "The common-world probe uses a fresh reference trajectory and zero-initialized recurrent memory for both trained and frozen predictors; its distribution may differ from training.",
                              "Seeds, not within-world cell-time points, are replication units.",
                              "No general-cognition or long-term survival claim follows from this toy."]}
    rendered = json.dumps(report, indent=2, allow_nan=False)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
