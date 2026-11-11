"""Adaptive sequence of controlled evolution-controller probes.

Every search iteration proposes a distinct, history-dependent hypothesis,
executes matched-seed simulator runs, records the observed contradiction or
support, and decides whether to retain the candidate. These are algorithmic
research *search loops*, not generations or independent discoveries.

Base environmental laws and the existing EvolutionGarden code are unchanged.
"""

from __future__ import annotations

import hashlib
import json
import math
import platform
from pathlib import Path

import numpy as np

from EVOLUTION_garden import EvolutionGarden

OUT = Path(__file__).with_name("SOC_LEARNING_results.json")
DEVELOPMENT = list(range(1110, 1116))
HOLDOUT = list(range(2010, 2050))
STEPS = 1500
SIZE = 10


def one(seed, bias, recurrence, mutation):
    garden = EvolutionGarden(
        seed=seed, size=SIZE, policy="neural",
        mutation_std=mutation, initial_occupancy=.65, max_age=240,
    )
    # Deliberate controller interventions; all ecological rules unchanged.
    garden.bact += bias
    garden.wrec *= recurrence
    trajectory = {}
    for t in range(1, STEPS + 1):
        garden.step()
        if t in (200, 600, 1000, 1500):
            m = garden.metrics()
            trajectory[t] = {
                "population": m["population"],
                "mean_energy_all": m["mean_energy_all"],
                "mean_resource": m["mean_resource"],
                "max_generation": m["max_generation"],
            }
    m = garden.metrics()
    alive = garden.alive
    # A rank-agnostic policy phenotype probe: neural propensity at controlled
    # resource values, setting all other inputs/cell hidden states to neutral.
    h = garden.HIDDEN
    low = np.tile([.3, .5, .3, .5, 0, 0, 1], (garden.count, 1))
    high = low.copy()
    high[:, 0] = high[:, 2] = .7
    z_low = np.tanh(np.einsum("ni,nih->nh", low, garden.win) + garden.bhidden)
    z_high = np.tanh(np.einsum("ni,nih->nh", high, garden.win) + garden.bhidden)
    p_low = garden._sigmoid(np.einsum("nh,nh->n", z_low, garden.wact) + garden.bact)
    p_high = garden._sigmoid(np.einsum("nh,nh->n", z_high, garden.wact) + garden.bact)
    return {
        "seed": seed,
        "population": int(alive.sum()),
        "energy": float(garden.energy.mean()),
        "births": int(garden.births),
        "deaths": int(garden.deaths),
        "max_generation": int(m["max_generation"]),
        "mean_policy_p_low": float(p_low.mean()),
        "mean_policy_p_high": float(p_high.mean()),
        "policy_resource_sensitivity": float((p_high - p_low).mean()),
        "trajectory": trajectory,
    }


def evaluate(parameters, seeds, cache):
    key = json.dumps([parameters, seeds], sort_keys=True)
    if key not in cache:
        b, r, m = parameters
        trials = [one(seed, b, r, m) for seed in seeds]
        cache[key] = {
            "parameters": {"action_bias": b, "recurrent_gain": r, "mutation_std": m},
            "seeds": list(seeds),
            "mean_population": float(np.mean([x["population"] for x in trials])),
            "mean_energy": float(np.mean([x["energy"] for x in trials])),
            "mean_sensitivity": float(np.mean([x["policy_resource_sensitivity"] for x in trials])),
            "mean_generation": float(np.mean([x["max_generation"] for x in trials])),
            "trials": trials,
        }
        # Score is a DESIGNER value, not evolution or general intelligence.
        cache[key]["score"] = cache[key]["mean_population"] / 100 + cache[key]["mean_energy"]
    return cache[key]


def main():
    source_names = ("garden.py", "EVOLUTION_garden.py", "SOC_LEARNING_search.py")
    source = {
        name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
        for name in source_names
    }
    # Predeclare 32 sequential coordinate hypotheses. The sign of each next
    # move is chosen by observed acceptance/rejection (direction reversal).
    steps = {
        "action_bias": [.45, .30, .20, .15, .10, .06],
        "recurrent_gain": [.75, .5, .35, .25, .15, .10],
        "mutation_std": [.025, .015, .01, .007, .004, .002],
    }
    parameter_names = ["action_bias", "recurrent_gain", "mutation_std"]
    allowed = {"action_bias": (-2., 2.), "recurrent_gain": (0., 4.), "mutation_std": (0., .2)}
    best = {"action_bias": 0., "recurrent_gain": 1., "mutation_std": .025}
    direction = {key: (-1. if key == "action_bias" else 1.) for key in parameter_names}
    cache = {}
    history = []
    original = tuple(best[k] for k in parameter_names)
    champion = evaluate(original, DEVELOPMENT, cache)
    for i in range(32):
        name = parameter_names[i % 3]
        stage = min((i // 3) // 2, len(steps[name]) - 1)
        amount = steps[name][stage]
        proposal = best.copy()
        proposal[name] = float(np.clip(
            proposal[name] + direction[name] * amount, *allowed[name]
        ))
        # Handle accidental unchanged candidate at a constraint boundary.
        if proposal[name] == best[name]:
            direction[name] *= -1
            proposal[name] = float(np.clip(
                best[name] + direction[name] * amount, *allowed[name]
            ))
        candidate = evaluate(tuple(proposal[k] for k in parameter_names),
                             DEVELOPMENT, cache)
        delta = candidate["score"] - champion["score"]
        accepted = bool(delta > .004)
        prior = best.copy()
        if accepted:
            best = proposal
            champion = candidate
        else:
            direction[name] *= -1
        hypothesis = (
            f"Changing {name} from {prior[name]:.4g} to "
            f"{proposal[name]:.4g} will improve the same-seed "
            f"development ecology score while preserving world physics."
        )
        history.append({
            "search_loop": i + 1,
            "orientation": hypothesis,
            "challenger": proposal,
            "incumbent_before": prior,
            "development_seeds": DEVELOPMENT,
            "result": {
                "challenger_score": candidate["score"],
                "incumbent_score": candidate["score"] - delta,
                "score_difference": delta,
                "mean_population": candidate["mean_population"],
                "mean_energy": candidate["mean_energy"],
                "mean_resource_sensitivity": candidate["mean_sensitivity"],
            },
            "decision": "accept" if accepted else "reject and reverse search direction",
            "next": f"Probe {parameter_names[(i + 1) % 3]} next, with surviving incumbent.",
            "evidence_level": "in-simulator exploratory search, not independent confirmation",
        })
    # Four validation movements, each designed to attack a different claim.
    final_tuple = tuple(best[k] for k in parameter_names)
    final = evaluate(final_tuple, HOLDOUT, cache)
    original_hold = evaluate(original, HOLDOUT, cache)
    no_mut = evaluate((best["action_bias"], best["recurrent_gain"], 0.), HOLDOUT, cache)
    no_rec = evaluate((best["action_bias"], 0., best["mutation_std"]), HOLDOUT, cache)
    holdout = {
        "searched_controller": final,
        "unchanged_neural_controller": original_hold,
        "clonal_same_controller": no_mut,
        "no_recurrence_same_controller": no_rec,
    }
    checks = []
    for key in ("unchanged_neural_controller", "clonal_same_controller",
                "no_recurrence_same_controller"):
        a = final["trials"]
        b = holdout[key]["trials"]
        differences = [a[j]["population"] - b[j]["population"] for j in range(len(HOLDOUT))]
        checks.append({
            "search_loop": 33 + len(checks),
            "orientation": "Does searched controller beat " + key + " on untouched seeds?",
            "probe": "40 paired heldout seeds, 1500 ticks each; original world laws",
            "result": {
                "paired_mean_population_difference": float(np.mean(differences)),
                "paired_sd_population_difference": float(np.std(differences, ddof=1)),
                "wins": int(sum(d > 0 for d in differences)),
                "reference_mean_population": holdout[key]["mean_population"],
            },
            "next": "Keep population improvement separate from selection, inherited cognition or viability.",
        })
    checks.append({
        "search_loop": 36,
        "orientation": "Does any measured policy resource sensitivity support a memory mechanism?",
        "probe": "synthetic standardized probe p(resource=.7) − p(resource=.3), final/controls",
        "result": {
            name: value["mean_sensitivity"] for name, value in holdout.items()
        },
        "next": "A static two-resource difference is not evidence recurrent memory aids decision making.",
    })
    archive = {
        "status": "completed",
        "method": "history-dependent coordinate search followed by untouched validation",
        "disclaimer": "36 computational research-search movements, not 36 independent scientific discoveries",
        "base_world": "original EvolutionGarden demographic world, not fixed-occupancy Garden",
        "seeds_development": DEVELOPMENT,
        "seeds_holdout": HOLDOUT,
        "size": SIZE,
        "steps": STEPS,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "source_sha256": source,
        "initial": list(original),
        "chosen": best,
        "history": history,
        "validation_movements": checks,
        "holdout": holdout,
        "unique_cached_experiments": len(cache),
    }
    OUT.write_text(json.dumps(archive, indent=2, sort_keys=True) + "\n")
    print("Recorded", len(history) + len(checks), "search movements,",
          len(cache), "distinct configurations/seed families")
    print("Chosen", best, "holdout population", final["mean_population"],
          "original", original_hold["mean_population"],
          "clone", no_mut["mean_population"], "no recurrence", no_rec["mean_population"])


if __name__ == "__main__":
    main()
