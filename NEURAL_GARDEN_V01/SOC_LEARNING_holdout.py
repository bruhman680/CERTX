"""Untouched-seed counterfactuals for evolutionary search.

Distinguish manual policy bias selection from inherited mutation and from
non-neural threshold control. The search did not use these 40 seed worlds.
"""

import hashlib
import json
from pathlib import Path

import numpy as np

from EVOLUTION_garden import EvolutionGarden
from SOC_LEARNING_search import HOLDOUT, SIZE, STEPS, evaluate


def threshold_run(seed):
    garden = EvolutionGarden(seed=seed, size=SIZE, policy="threshold", mutation_std=0.)
    for _ in range(STEPS):
        garden.step()
    return {
        "seed": seed,
        "population": garden.metrics()["population"],
        "energy": float(garden.energy.mean()),
        "max_generation": int(garden.metrics()["max_generation"]),
    }


def main():
    previous = json.loads(Path(__file__).with_name("SOC_LEARNING_results.json").read_text())
    chosen = previous["chosen"]
    cache = {}
    no_mut = evaluate((chosen["action_bias"], chosen["recurrent_gain"], 0.), HOLDOUT, cache)
    same_bias_mut = evaluate((chosen["action_bias"], chosen["recurrent_gain"], .025), HOLDOUT, cache)
    threshold = [threshold_run(seed) for seed in HOLDOUT]
    references = {
        "hand_tuned_clonal_neural": no_mut,
        "hand_tuned_mutating_neural": same_bias_mut,
        "handcoded_threshold55": {
            "mean_population": float(np.mean([r["population"] for r in threshold])),
            "mean_energy": float(np.mean([r["energy"] for r in threshold])),
            "trials": threshold,
        },
    }
    paired = {}
    for name in ("hand_tuned_mutating_neural", "handcoded_threshold55"):
        d = np.array([no_mut["trials"][i]["population"] - references[name]["trials"][i]["population"] for i in range(len(HOLDOUT))])
        paired[name] = {
            "mean_clonal_minus_reference": float(d.mean()),
            "sd": float(d.std(ddof=1)),
            "wins": int((d > 0).sum()),
            "losses": int((d < 0).sum()),
            "ties": int((d == 0).sum()),
        }
    archive = {
        "interpretation": "preselected bias evaluated once on untouched 40 seeds; candidate originally selected via six-seed development search",
        "hypothesis": "At fixed manually tuned bias and recurrent gain, does mutation improve descendants? And how does it compare to a non-genetic resource rule?",
        "seeds": HOLDOUT,
        "steps": STEPS,
        "size": SIZE,
        "changed_world": "EvolutionGarden demographic rules are identical across arms, but threshold control bypasses neural phenotype",
        "source_sha256": {x: hashlib.sha256(Path(__file__).with_name(x).read_bytes()).hexdigest() for x in ("SOC_LEARNING_holdout.py", "SOC_LEARNING_search.py", "EVOLUTION_garden.py")},
        "reference": references,
        "paired": paired,
        "next": "Never attribute hand-tuned initial phenotype advantages to heritable selection without mutation and lineage fitness gains",
    }
    out = Path(__file__).with_name("SOC_LEARNING_holdout_results.json")
    out.write_text(json.dumps(archive, indent=2, sort_keys=True) + "\n")
    print({k: (round(v["mean_population"], 3), round(v["mean_energy"], 4)) for k, v in references.items()})
    print(paired)


if __name__ == "__main__":
    main()
