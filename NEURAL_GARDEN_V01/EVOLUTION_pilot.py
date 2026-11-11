"""Small, honest, reproducible exploratory pilot for EvolutionGarden.

Purely synthetic, designed to check behavior and invariants, not establish
evolutionary adaptation. The scripts in this branch are not a scientific proof.
"""

import hashlib
import json
import platform
from pathlib import Path

import numpy as np

from EVOLUTION_garden import EvolutionGarden


HERE = Path(__file__).resolve().parent


def check_resume():
    reference = EvolutionGarden(seed=1007, size=8, policy="neural")
    resumed = EvolutionGarden(seed=1007, size=8, policy="neural")
    for _ in range(48):
        reference.step()
        resumed.step()
    assert reference.fingerprint() == resumed.fingerprint(), "seed replay differed"
    tmp = HERE / "EVOLUTION_test_resume.pkl"
    try:
        resumed.save(tmp)
        resumed = EvolutionGarden.load(tmp)  # trusted local checkpoint only
        for _ in range(72):
            reference.step()
            resumed.step()
        assert reference.fingerprint() == resumed.fingerprint(), "checkpoint continuation differed"
    finally:
        tmp.unlink(missing_ok=True)
    assert len(set(reference.lineage)) == len(reference.lineage)
    for uid, record in reference.lineage.items():
        assert uid >= 0
        assert record["parent"] == -1 or record["parent"] < uid
        assert len(reference.ancestry(uid)) == record["generation"] + 1
    assert reference.births + sum(1 for rec in reference.lineage.values() if rec["parent"] == -1) == len(reference.lineage)
    return True


def pilot():
    checks = check_resume()
    variants = [("neural_mutating", "neural", .025),
                ("neural_clonal", "neural", 0.),
                ("threshold_mutating_genomes", "threshold", .025)]
    seeds = list(range(801, 821))
    rows = []
    for variant, policy, mutation in variants:
        for seed in seeds:
            g = EvolutionGarden(seed=seed, size=10, policy=policy, mutation_std=mutation)
            trajectories = [{"tick": 0, **g.metrics()}]
            for tick in range(1, 601):
                metrics = g.step()
                if tick in (100, 300, 600):
                    trajectories.append(dict(metrics))
            assert len(g.lineage) == sum(1 for rec in g.lineage.values() if rec["parent"] == -1) + g.births
            assert all(rec["parent"] == -1 or rec["parent"] < uid for uid,rec in g.lineage.items())
            rows.append({"variant": variant, "seed": seed, "trajectory": trajectories,
                         "fingerprint": g.fingerprint(), "lineage_count": len(g.lineage)})
    summary = {}
    for name, _, _ in variants:
        subset = [r["trajectory"][-1] for r in rows if r["variant"] == name]
        summary[name] = {key: {"mean": float(np.mean([r[key] for r in subset])),
                               "sd_seeds": float(np.std([r[key] for r in subset], ddof=1))}
                         for key in ("population", "mean_energy_all", "mean_resource",
                                     "births_cumulative", "deaths_cumulative", "max_generation")}
    result = {"label": "exploratory synthetic pilot, not confirmatory evidence",
              "seed_ids": seeds, "grid": 10, "steps": 600,
              "check_seed_replay_checkpoint_and_ancestry": checks,
              "python": platform.python_version(), "numpy": np.__version__,
              "source_sha256": hashlib.sha256((HERE/"EVOLUTION_garden.py").read_bytes()).hexdigest(),
              "summary": summary, "rows": rows}
    path = HERE/"EVOLUTION_pilot_results.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(json.dumps(summary, indent=2))
    print("wrote", path)
    return result


if __name__ == "__main__":
    pilot()
