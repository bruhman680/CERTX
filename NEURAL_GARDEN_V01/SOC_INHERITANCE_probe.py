"""Three causal questions about acquired-threshold inheritance in demographic cells."""

import hashlib
import json
import platform
from pathlib import Path

import numpy as np

from SOC_INHERITANCE_garden import InheritanceGarden

SEEDS = list(range(2600, 2620))
STEPS = 3000
ARMS = {
    "acquired": (True, True, 0., .97),
    "germline_only": (True, False, 0., .97),
    "acquired_mut": (True, True, .025, .97),
    "germline_mut": (True, False, .025, .97),
    "acquired_trace0": (True, True, 0., 0.),
    "no_learning": (False, False, 0., .97),
}


def one(arm, seed):
    learning, acquired, mutation, trace = ARMS[arm]
    world = InheritanceGarden(seed=seed, size=10, learning=learning,
                              inherit_acquired=acquired, mutation_std=mutation,
                              trace_decay=trace)
    before = world.fingerprint()
    milestones = {}
    for tick in range(1, STEPS + 1):
        alpha = .055 if 1001 <= tick <= 2000 else .06
        world.step(regrowth_rate=alpha)
        if tick in (600, 1000, 1200, 2000, 2400, 3000):
            m = world.metrics()
            milestones[tick] = {
                "population": m["population"],
                "mean_energy": m["mean_energy_all"],
                "resource": m["mean_resource"],
                "mean_threshold_living": m["mean_threshold_living"],
                "mean_germline_living": m["mean_germline_living"],
                "births_cumulative": m["births_cumulative"],
                "max_generation": m["max_generation"],
            }
    # Genealogy checks are crucial, but not fitness evidence.
    assert world.next_id == len(world.lineage)
    assert (world.genome_id[world.alive] >= 0).all()
    assert len(set(world.genome_id[world.alive].tolist())) == int(world.alive.sum())
    return {
        "seed": seed, "arm": arm, "run_id": f"inherit-{arm}-{seed}",
        "initial_full_fingerprint": before,
        "final_full_fingerprint": world.fingerprint(),
        "milestones": milestones,
        "living": int(world.alive.sum()),
        "mean_energy_all": float(world.energy.mean()),
        "resource": float(world.resource.mean()),
        "mean_theta_living": float(world.thresholds[world.alive].mean()) if world.alive.any() else 0.,
        "mean_germline_living": float(world.germline[world.alive].mean()) if world.alive.any() else 0.,
        "births": int(world.births),
        "deaths": int(world.deaths),
        "lineage_entries": len(world.lineage),
        "max_generation": int(world.metrics()["max_generation"]),
    }


def main():
    outputs = []
    for arm in ARMS:
        for seed in SEEDS:
            outputs.append(one(arm, seed))
        print("finished", arm, flush=True)
    summaries = {}
    for arm in ARMS:
        rows = [r for r in outputs if r["arm"] == arm]
        summaries[arm] = {
            key: float(np.mean([r[key] for r in rows]))
            for key in ("living", "mean_energy_all", "resource", "mean_theta_living",
                        "mean_germline_living", "births", "deaths", "max_generation")
        }
        summaries[arm]["mean_energy_t1200"] = float(np.mean([
            r["milestones"][1200]["mean_energy"] for r in rows]))
        summaries[arm]["mean_energy_t2400"] = float(np.mean([
            r["milestones"][2400]["mean_energy"] for r in rows]))

    pairs = {}
    for a, b in (("acquired", "germline_only"),
                 ("acquired_mut", "germline_mut"),
                 ("acquired_mut", "acquired"),
                 ("acquired", "acquired_trace0"),
                 ("acquired", "no_learning")):
        x = [r for r in outputs if r["arm"] == a]
        y = [r for r in outputs if r["arm"] == b]
        assert [r["seed"] for r in x] == [r["seed"] for r in y]
        d = np.array([xx["living"] - yy["living"] for xx, yy in zip(x, y)])
        de = np.array([xx["mean_energy_all"]-yy["mean_energy_all"]
                       for xx, yy in zip(x, y)])
        pairs[f"{a} minus {b}"] = {
            "mean_population_diff": float(d.mean()),
            "sd_population_diff": float(d.std(ddof=1)),
            "wins": int((d > 0).sum()),
            "mean_energy_diff": float(de.mean()),
            "sd_energy_diff": float(de.std(ddof=1)),
        }
    folder = Path(__file__).parent
    archive = {
        "status": "executed",
        "questions": [
            "Does inheriting acquired parental threshold updates outperform inheriting germline thresholds?",
            "Does birth mutation help when parental threshold learning is or is not inherited?",
            "Does eligibility trace memory improve long-run demographic ecology over trace-free updates?",
        ],
        "note": "One synthetic demographic world; acquisition uses REINFORCE, not teacher; three explicitly separate hypotheses, not 120 research loops",
        "arms": {k: dict(zip(("learning", "inherit_acquired", "mutation_std", "trace_decay"), v)) for k, v in ARMS.items()},
        "world": "original EvolutionGarden demographic physics, with only regrowth alpha .06/.055/.06 seasonal phase changed identically for all arms",
        "seeds": SEEDS,
        "size": 10,
        "steps": STEPS,
        "python": platform.python_version(), "numpy": np.__version__,
        "source_sha256": {n: hashlib.sha256((folder/n).read_bytes()).hexdigest()
                          for n in ("garden.py", "EVOLUTION_garden.py", "SOC_INHERITANCE_garden.py", "SOC_INHERITANCE_probe.py")},
        "summary": summaries,
        "paired": pairs,
        "rows": outputs,
    }
    out = folder / "SOC_INHERITANCE_results.json"
    out.write_text(json.dumps(archive, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"summary": summaries, "paired": pairs}, indent=2))


if __name__ == "__main__":
    main()
