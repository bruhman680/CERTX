#!/usr/bin/env python3
"""Exact finite authored secret-sharing planning proxy; standard library only.

This is not an actual reader, corpus harness, or model-training experiment.
Execution writes results only to the explicitly supplied output directory.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations, product
import json
from pathlib import Path

RECORDS = ("P", "C", "R", "M")
VARIABLES = ("T", "qP", "qR", "X", "Y", "u", "v")
WORLDS = tuple(product((0, 1), repeat=7))
PRIORS = (
    ("FAIR", F(1, 2), F(1, 2)),
    ("PRIMARY_FAVORED", F(3, 4), F(1, 4)),
    ("REFERENCE_FAVORED", F(1, 4), F(3, 4)),
    ("BOTH_BAD", F(0), F(0)),
)


def rational(value):
    value = F(value)
    return f"{value.numerator}/{value.denominator}"


def observations(world):
    t, qp, qr, x, y, u, v = world
    return (x, (qp, x ^ t if qp else u), y, (qr, y ^ t if qr else v))


OBS = tuple(observations(w) for w in WORLDS)


def weights(pp, pr):
    return tuple(F(1, 32) * (pp if w[1] else 1 - pp)
                 * (pr if w[2] else 1 - pr) for w in WORLDS)


def certificate(support):
    targets = sorted({WORLDS[i][0] for i in support})
    assert targets
    return targets[0] if len(targets) == 1 else None


class Solver:
    """Belief is a positive-weight subset; posterior is prior conditioned on it."""

    def __init__(self, probability):
        self.probability = probability
        self.cache = {}
        self.states = {}

    def mass(self, support):
        return sum((self.probability[i] for i in support), F(0))

    @staticmethod
    def state_id(support, mask, budget):
        bits = sum(1 << i for i in support)
        return f"b{budget}_m{mask:01x}_w{bits:032x}"

    def partition(self, support, record):
        groups = defaultdict(list)
        for i in support:
            groups[OBS[i][record]].append(i)
        return [(value, tuple(group)) for value, group in sorted(groups.items())]

    def solve(self, support, mask, budget):
        key = (support, mask, budget)
        if key in self.cache:
            return self.cache[key]
        state_id = self.state_id(*key)
        mass = self.mass(support)
        assert mass > 0 and all(self.probability[i] > 0 for i in support)
        target = certificate(support)
        best = (F(target is not None), F(0), "STOP")
        actions = [{"action": "STOP", "resolution_probability": rational(best[0]),
                    "expected_additional_cost": "0/1", "branches": []}]
        if budget > 0:
            for record, name in enumerate(RECORDS):
                if mask & (1 << record):
                    continue
                resolution, cost, branches = F(0), F(1), []
                for value, child_support in self.partition(support, record):
                    conditional = self.mass(child_support) / mass
                    child = self.solve(child_support, mask | (1 << record), budget - 1)
                    resolution += conditional * child[0]
                    cost += conditional * child[1]
                    branches.append({"observation": value,
                                     "conditional_probability": rational(conditional),
                                     "child_state": self.state_id(child_support, mask | (1 << record), budget - 1)})
                actions.append({"action": name, "resolution_probability": rational(resolution),
                                "expected_additional_cost": rational(cost), "branches": branches})
                # Strict improvement preserves canonical action order P,C,R,M.
                if (resolution, -cost) > (best[0], -best[1]):
                    best = (resolution, cost, name)
        self.cache[key] = best
        self.states[state_id] = {
            "remaining_budget": budget, "queried_mask": mask,
            "queried_records": [name for i, name in enumerate(RECORDS) if mask & (1 << i)],
            "support_world_ids": list(support), "prior_mass": rational(mass),
            "posterior": [{"world_id": i, "probability": rational(self.probability[i] / mass)} for i in support],
            "feasible_T": sorted({WORLDS[i][0] for i in support}),
            "certified_T": target, "chosen_action": best[2],
            "resolution_probability": rational(best[0]), "expected_additional_cost": rational(best[1]),
            "actions": actions,
        }
        return best

    def leaves(self, support, mask, budget, path=(), root_mass=None):
        if root_mass is None:
            root_mass = self.mass(support)
        state_id = self.state_id(support, mask, budget)
        action = self.solve(support, mask, budget)[2]
        if action == "STOP":
            return [{"path": list(path), "terminal_state": state_id,
                     "probability": rational(self.mass(support) / root_mass),
                     "query_cost": len(path), "feasible_T": sorted({WORLDS[i][0] for i in support}),
                     "certified_T": certificate(support)}]
        record = RECORDS.index(action)
        result = []
        for value, child in self.partition(support, record):
            result.extend(self.leaves(child, mask | (1 << record), budget - 1,
                                      path + ({"record": action, "observation": value},), root_mass))
        return result


def fixed_subsets(solver, support, budget):
    candidates = []
    for size in range(budget + 1):
        for subset in combinations(range(4), size):
            groups = defaultdict(list)
            for i in support:
                groups[tuple(OBS[i][r] for r in subset)].append(i)
            resolution = sum((solver.mass(group) for group in groups.values()
                              if certificate(group) is not None), F(0)) / solver.mass(support)
            candidates.append({"records": [RECORDS[r] for r in subset],
                               "resolution_probability": rational(resolution),
                               "query_cost": size,
                               "outcomes": [{"observations": observation,
                                             "probability": rational(solver.mass(group) / solver.mass(support)),
                                             "support_world_ids": group,
                                             "feasible_T": sorted({WORLDS[i][0] for i in group}),
                                             "certified_T": certificate(group)}
                                            for observation, group in sorted(groups.items())]})
    best = max(candidates, key=lambda c: (F(c["resolution_probability"]), -c["query_cost"]))
    return {"cost_convention": "Every selected record is queried; no adaptive early stopping.",
            "best": best, "all_subsets": candidates}


def duplicate_readout(probability, records):
    groups = defaultdict(list)
    for i, obs in enumerate(OBS):
        groups[tuple(obs[r] for r in records)].append(i)
    return [{"observation": value, "raw_microstate_count": len(ids),
             "positive_weight_microstate_count": sum(probability[i] > 0 for i in ids),
             "world_ids": ids, "probability": rational(sum((probability[i] for i in ids), F(0)))}
            for value, ids in sorted(groups.items())]


def prior_experiment(label, pp, pr):
    probability = weights(pp, pr)
    assert sum(probability) == 1
    support = tuple(i for i, p in enumerate(probability) if p > 0)
    solver = Solver(probability)
    oracle_solver = Solver(probability)
    roots = []
    for budget in range(5):
        resolution, cost, action = solver.solve(support, 0, budget)
        baseline = fixed_subsets(solver, support, budget)
        oracle_branches, oracle_resolution, oracle_cost = [], F(0), F(0)
        for qp, qr in product((0, 1), repeat=2):
            child_support = tuple(i for i in support if WORLDS[i][1:3] == (qp, qr))
            if not child_support:
                continue
            mass = solver.mass(child_support)
            ores, ocost, _ = oracle_solver.solve(child_support, 0, budget)
            oracle_resolution += mass * ores
            oracle_cost += mass * ocost
            oracle_branches.append({"qP": qp, "qR": qr, "probability": rational(mass),
                                    "state": oracle_solver.state_id(child_support, 0, budget),
                                    "resolution_probability": rational(ores),
                                    "expected_query_cost": rational(ocost)})
        expected_oracle = 1 - (1 - pp) * (1 - pr) if budget >= 2 else F(0)
        assert oracle_resolution == expected_oracle
        leaves = solver.leaves(support, 0, budget)
        assert sum(F(leaf["probability"]) for leaf in leaves) == 1
        assert sum((F(leaf["probability"]) for leaf in leaves if leaf["certified_T"] is not None), F(0)) == resolution
        assert sum((F(leaf["probability"]) * leaf["query_cost"] for leaf in leaves), F(0)) == cost
        assert resolution >= F(baseline["best"]["resolution_probability"])
        assert oracle_resolution >= resolution
        roots.append({"budget": budget, "root_state": solver.state_id(support, 0, budget),
                      "chosen_action": action, "resolution_probability": rational(resolution),
                      "expected_query_cost": rational(cost), "terminal_outcomes": leaves,
                      "fixed_subset_baseline": baseline,
                      "resolution_advantage_over_best_fixed_subset": rational(resolution - F(baseline["best"]["resolution_probability"])),
                      "quality_informed_oracle": {
                          "extra_information": "qP and qR are revealed before queries, but T is not; quality reveal costs zero.",
                          "resolution_probability": rational(oracle_resolution),
                          "expected_query_cost": rational(oracle_cost), "quality_branches": oracle_branches}})
    return {"prior": label, "pP": rational(pp), "pR": rational(pr),
            "worlds": [{"world_id": i, "latent": dict(zip(VARIABLES, w)),
                        "probability": rational(probability[i]),
                        "observations": dict(zip(RECORDS, OBS[i]))} for i, w in enumerate(WORLDS)],
            "positive_weight_microstates": len(support),
            "duplicate_observations": {"per_record": {name: duplicate_readout(probability, (r,))
                                                       for r, name in enumerate(RECORDS)},
                                       "joint_all_four": duplicate_readout(probability, tuple(range(4)))},
            "roots": roots, "belief_states": solver.states,
            "quality_informed_belief_states": oracle_solver.states}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    results = {"schema_version": "1.0", "experiment": "finite_authored_secret_sharing_planning_proxy",
               "record_order": RECORDS, "latent_order": VARIABLES,
               "scope": "Finite authored proxy; no actual reader, harness, or model training evaluated.",
               "objective": "Maximize certified T resolution, then minimize expected query cost; query ties P,C,R,M.",
               "priors": [prior_experiment(*prior) for prior in PRIORS]}
    result_path = args.output_dir / "results.json"
    result_path.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
    rows = ["prior\tpP\tpR\tbudget\tresolution\texpected_cost\tbest_fixed_resolution\tbest_fixed_cost\toracle_resolution\toracle_cost\tfirst_action"]
    for prior in results["priors"]:
        for root in prior["roots"]:
            fixed, oracle = root["fixed_subset_baseline"]["best"], root["quality_informed_oracle"]
            rows.append("\t".join(map(str, (prior["prior"], prior["pP"], prior["pR"], root["budget"],
                                          root["resolution_probability"], root["expected_query_cost"],
                                          fixed["resolution_probability"], fixed["query_cost"],
                                          oracle["resolution_probability"], oracle["expected_query_cost"], root["chosen_action"]))))
    (args.output_dir / "root_outcomes.tsv").write_text("\n".join(rows) + "\n")
    print(f"Wrote {result_path} and root_outcomes.tsv (20 prior/budget rows).")


if __name__ == "__main__":
    main()
