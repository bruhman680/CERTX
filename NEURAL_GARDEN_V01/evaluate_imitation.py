"""Bounded educational probe: supervised neural imitation versus fixed threshold.

Runs five exploratory seeds, original laws, 16x16 grid, 600 ticks. Results
are not evidence of autonomous ecological learning or independent replication.
"""
import json
import sys
from pathlib import Path
from imitation_garden import ImitationGarden
from threshold_policy import ThresholdGarden
from garden import Garden


def run(seed, cls, **kw):
    sim = cls(seed=seed, size=16, **kw)
    trajectory = []
    for i in range(600):
        m = sim.step()
        if i in (99, 199, 399, 599):
            trajectory.append({"tick": i+1, "energy": m["mean_energy"],
                               "resource": m["mean_resource"],
                               "harvest": m["harvest_rate"],
                               "imitation_accuracy": m.get("teacher_imitation_accuracy")})
    return {"seed": seed, "final": trajectory[-1], "trajectory": trajectory}


def main():
    seeds = [740, 741, 742, 743, 744]
    arms = {"supervised_imitation": (ImitationGarden, {}),
            "fixed_threshold": (ThresholdGarden, {"threshold": .55}),
            "original_neural": (Garden, {"learning": True})}
    results = {}
    for name, (cls, kw) in arms.items():
        results[name] = [run(s, cls, **kw) for s in seeds]
        print(name, 'mean_final_energy',
              sum(row['final']['energy'] for row in results[name]) / len(seeds),
              flush=True)
    output = {"design": "exploratory_supervised_capacity_probe",
              "teacher_threshold": .55, "original_world_laws": True,
              "seeds": seeds, "steps": 600, "size": 16, "results": results}
    p = Path(__file__).with_name('imitation_pilot_results.json')
    p.write_text(json.dumps(output, indent=2) + '\n')
    print(p)


if __name__ == '__main__':
    main()
