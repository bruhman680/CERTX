"""Independent evidential pressure probes for the Neural Garden.

Only tests predeclared, distinct methodological hypotheses. Counts a *research
loop* at the cluster level in SOC_REVIEW_REPORT.md, not for each random seed.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from garden import Garden


def hash_file(name):
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


def threshold_trace(seed, *, size=12, threshold=.5, ticks=2500,
                    diffusion=.08, alpha=.06, beta=.18,
                    shock_at=(), shock_factor=.5):
    # Instantiate the original Garden for identical initialization and neighbor
    # topology. No neural policy update is performed in this threshold test.
    obj = Garden(seed=seed, size=size, learning=False)
    res = obj.resource.copy()
    eng = obj.energy.copy()
    rows = []
    raw_tail, actual_tail, covariance_tail = [], [], []
    checkpoints = {0, 100, 400, 600, 1000, 2000, ticks}
    snapshots = {}
    for tick in range(ticks + 1):
        if tick in checkpoints:
            snapshots[str(tick)] = {
                "mean_energy": float(eng.mean()),
                "mean_resource": float(res.mean()),
                "floor_fraction": float((eng <= .01).mean()),
                "ceiling_fraction": float((eng >= .99).mean()),
            }
        if tick == ticks:
            break
        pre_res, pre_eng = res.copy(), eng.copy()
        act = (pre_res > threshold).astype(float)
        delta_r = (diffusion * (obj._neighbors(pre_res) - pre_res)
                   + alpha * (1 - pre_res) - beta * pre_res * act)
        next_res = np.clip(pre_res + delta_r, 0, 1)
        raw = .25 * pre_res * act - .03 - .055 * act + .008 * (1 - act)
        next_eng = np.clip(pre_eng + raw, 0, 1)
        if tick >= ticks - min(250, ticks):
            raw_tail.append(float(raw.mean()))
            actual_tail.append(float((next_eng - pre_eng).mean()))
            covariance_tail.append(float(np.mean(pre_res * act) - pre_res.mean() * act.mean()))
        if tick + 1 in shock_at:
            next_res *= shock_factor
        res, eng = next_res, next_eng
    return {
        "snapshots": snapshots,
        "tail_raw_drift": float(np.mean(raw_tail)),
        "tail_realized_drift": float(np.mean(actual_tail)),
        "tail_resource_action_covariance": float(np.mean(covariance_tail)),
        "tail_clipping_gap": float(np.mean(np.array(actual_tail) - np.array(raw_tail))),
    }


def verify_global_equations():
    checks = []
    for size in [2, 4, 8, 16]:
        for seed in [7, 19, 101]:
            obj = Garden(seed, size, learning=False)
            r = obj.resource.copy()
            a = obj.rng_action.integers(0, 2, obj.count).astype(float)
            d = .08 * (obj._neighbors(r) - r)
            next_r = np.clip(r + d + .06 * (1-r) - .18 * r * a, 0, 1)
            resource_residual = float(abs((next_r-r).mean() - (.06*(1-r.mean()) - .18*(r*a).mean())))
            de = .25*r*a-.03-.055*a+.008*(1-a)
            energy_residual = float(abs(de.mean() - (.25*(r*a).mean()-.063*a.mean()-.022)))
            checks.append((resource_residual, energy_residual))
    return {"max_resource_balance_error": max(x[0] for x in checks),
            "max_raw_energy_balance_error": max(x[1] for x in checks),
            "cases": len(checks)}


def verify_hidden_state():
    # Verify that learning and pause/resume have measurable, deterministic
    # effects, without treating a model-state hash as prediction accuracy.
    seed = 9134
    learned, frozen = Garden(seed=seed, size=8, learning=True), Garden(seed=seed, size=8, learning=False)
    fp_init = learned.fingerprint()
    assert np.array_equal(learned.resource, frozen.resource)
    assert np.array_equal(learned.energy, frozen.energy)
    for _ in range(120):
        learned.step(); frozen.step()
    probe_before = learned.fingerprint()
    heldout = learned.prediction_probe(n=12)
    probe_after = learned.fingerprint()
    checkpoint = HERE / "SOC_REVIEW_temp.pkl"
    try:
        learned.save(checkpoint)
        restored = Garden.load(checkpoint)
        exact_restore = restored.fingerprint() == learned.fingerprint()
        for _ in range(15):
            restored.step(); learned.step()
        exact_continuation = restored.fingerprint() == learned.fingerprint()
    finally:
        if checkpoint.exists():
            checkpoint.unlink()
    return {
        "learning_changes_state": fp_init != probe_before,
        "weights_learned_differ_from_frozen": bool(np.any(learned.wact != frozen.wact)),
        "nonmutating_probe": probe_before == probe_after,
        "offpolicy_probe_mse": heldout,
        "exact_restore": exact_restore,
        "exact_continuation": exact_continuation,
        "learned_energy_after_135": float(learned.energy.mean()),
        "frozen_energy_after_120": float(frozen.energy.mean()),
    }


def assess_boundaries():
    # Apply the *same* original raw energy budget to cells deliberately placed
    # near opposite caps. The discrepancy is an algebraic fact about clipping.
    r = np.array([.01, .95, .01, .95])
    a = np.array([0., 1., 1., 0.])
    raw = .25*r*a-.03-.055*a+.008*(1-a)
    before = np.array([0., 1., .00001, .99999])
    observed = np.clip(before + raw, 0, 1) - before
    return {"raw":raw.tolist(),"realized":observed.tolist(),
            "max_abs_clipping_gap":float(np.max(np.abs(raw-observed))),
            "floor_example_raw":float(raw[0]),"floor_example_realized":float(observed[0]),
            "ceiling_example_raw":float(raw[1]),"ceiling_example_realized":float(observed[1])}


def main():
    result = {"design":"independent source-level falsification ladder, not a broad optimization search",
              "source_sha256":{"garden.py":hash_file("garden.py"),
                               "SOC_REVIEW_probe.py":hash_file("SOC_REVIEW_probe.py")},
              "platform":{"python":sys.version.split()[0],"numpy":np.__version__,
                          "system":platform.platform()},
              "exact_identities":verify_global_equations(),
              "checkpoint_and_learning":verify_hidden_state(),
              "clipping":assess_boundaries()}
    # Parameter questions are all paired by seed. Rows are grouped into six
    # substantive evidence-bearing clusters, NOT treated as 100+ loops.
    seed_pool=[8101,8102,8103,8104]
    configs={
       "horizon_base_500":dict(threshold=.50,ticks=500,size=12),
       "horizon_base_2000":dict(threshold=.50,ticks=2000,size=12),
       "horizon_base_5000":dict(threshold=.50,ticks=5000,size=12),
       "horizon_055_500":dict(threshold=.55,ticks=500,size=12),
       "horizon_055_2000":dict(threshold=.55,ticks=2000,size=12),
       "horizon_055_5000":dict(threshold=.55,ticks=5000,size=12),
       "small_grid_8":dict(threshold=.50,ticks=3000,size=8),
       "large_grid_16":dict(threshold=.50,ticks=3000,size=16),
       "no_diffusion":dict(threshold=.50,ticks=3000,size=12,diffusion=0),
       "more_diffusion":dict(threshold=.50,ticks=3000,size=12,diffusion=.12),
       "lower_regrowth":dict(threshold=.50,ticks=3000,size=12,alpha=.055),
       "higher_consumption":dict(threshold=.50,ticks=3000,size=12,beta=.19),
       "resource_shock":dict(threshold=.50,ticks=3000,size=12,shock_at=(1000,),shock_factor=.65),
    }
    result["paired_configs"]={}
    for key, cfg in configs.items():
        runs=[threshold_trace(seed,**cfg) for seed in seed_pool]
        result["paired_configs"][key]={"config":cfg,"seeds":seed_pool,"runs":runs,
            "mean_final_energy":float(np.mean([r["snapshots"][str(cfg["ticks"])]["mean_energy"] for r in runs])),
            "mean_final_floor":float(np.mean([r["snapshots"][str(cfg["ticks"])]["floor_fraction"] for r in runs])),
            "mean_tail_raw_drift":float(np.mean([r["tail_raw_drift"] for r in runs])),
            "mean_tail_covariance":float(np.mean([r["tail_resource_action_covariance"] for r in runs])),
        }
    out=HERE/"SOC_REVIEW_results.json"
    out.write_text(json.dumps(result,indent=2,sort_keys=True),encoding="utf-8")
    print("wrote",out,"paired configs",len(configs),"seeds per config",len(seed_pool))


if __name__=="__main__":
    main()
