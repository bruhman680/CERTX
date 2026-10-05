"""Controlled field transplant in the submitted TrueGardenEngine.

Run: python EXPERIMENTS/exp_016_field_wake_transplant.py
The two donor fields arise from separate 120-step histories.  All recipients
start with identical candidates, NK table, RNG, and control settings.  Field
and archive are assigned independently.  This probes code behavior, not a
physical claim about environmental memory or universal laws.
"""

from collections import defaultdict
from copy import deepcopy

from true_garden_fluid_settled import TrueGardenEngine, compute_fitness


DONOR_STEPS = 120
HORIZONS = (0, 1, 3, 12)


def make_donor(seed):
    donor = TrueGardenEngine(seed_rng=seed)
    donor.seed()
    donor.run(DONOR_STEPS)
    return donor


def make_recipient():
    # Seed 7 places seed-4 near the spark/proto criterion; this was chosen
    # deliberately to expose a status effect, so it is not an unbiased draw.
    recipient = TrueGardenEngine(seed_rng=7, K=3, mut_rate=0.0)
    recipient.seed()
    # No branching in the first 12 steps; mutation rate zero keeps seed
    # genotypes fixed. Cross-pollination at steps 5 and 10 remains possible.
    recipient.phase = "exhale"
    recipient.phase_age = 0
    return recipient


def observe(engine, target_id, target_genome):
    target = engine.candidates[target_id]
    return {
        "target_fitness": round(float(compute_fitness(target_genome, engine.fitness_table, engine.soil_field)), 6),
        "target_status": target.status,
        "target_genome": "".join(map(str, target.genome)),
        "K": round(engine.K, 5),
        "K_int": engine.last_K_int,
        "soil_richness": round(engine.soil_richness(), 5),
        "wake_total": round(float(sum(engine.soil_field.values())), 5),
        "archive_n": len(engine.soil),
        "population": len([c for c in engine.candidates.values() if c.status != "extinct"]),
    }


def experiment():
    donors = {"A": make_donor(17), "B": make_donor(23)}
    base = make_recipient()
    target = next(c for c in base.candidates.values() if c.label == "seed-4")
    assert "".join(map(str, target.genome)) == "011001"
    fields = {
        "virgin": {},
        "A": dict(donors["A"].soil_field),
        "B": dict(donors["B"].soil_field),
    }
    archives = {
        "empty": [],
        "B": list(donors["B"].soil),
        "saturated": (list(donors["B"].soil) * 5)[:100],
    }
    # Vary one carrier at a time, then cross field B with archive B.
    conditions = (
        ("virgin_empty", "virgin", "empty"),
        ("field_A_empty", "A", "empty"),
        ("field_B_empty", "B", "empty"),
        ("virgin_archive_B", "virgin", "B"),
        ("field_B_archive_B", "B", "B"),
        ("virgin_saturated", "virgin", "saturated"),
    )
    outcomes = {}
    for label, field_name, archive_name in conditions:
        recipient = deepcopy(base)
        recipient.soil_field = defaultdict(float, fields[field_name])
        recipient.soil = list(archives[archive_name])
        records = {0: observe(recipient, target.id, target.genome)}
        for t in range(1, max(HORIZONS) + 1):
            recipient.step()
            if t in HORIZONS:
                records[t] = observe(recipient, target.id, target.genome)
        outcomes[label] = records
    return donors, outcomes


if __name__ == "__main__":
    donors, outcomes = experiment()
    for label, donor in donors.items():
        print(f"donor {label}: seed={17 if label == 'A' else 23}, "
              f"wake={sum(donor.soil_field.values()):.5f}, "
              f"target_wake={donor.soil_field.get('011001', 0):.5f}, "
              f"archive_n={len(donor.soil)}")
    for condition, records in outcomes.items():
        print(condition)
        for t, row in records.items():
            print(f"  t={t:2} {row}")
