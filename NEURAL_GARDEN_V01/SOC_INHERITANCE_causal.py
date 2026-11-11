"""Paired first-birth mechanism test: acquired vs germline transfer.

Exactly matches prebirth histories. The first differing state should be the
newborn's inherited learned threshold, not environmental physics or resources.
"""

import hashlib
import json
from pathlib import Path

import numpy as np

from SOC_INHERITANCE_garden import InheritanceGarden


def first_birth(seed):
    acquired = InheritanceGarden(seed=seed, size=10, learning=True,
                                 inherit_acquired=True, mutation_std=0.)
    germline = InheritanceGarden(seed=seed, size=10, learning=True,
                                 inherit_acquired=False, mutation_std=0.)
    for step in range(1, 301):
        before_births = acquired.births
        acquired.step()
        germline.step()
        assert acquired.births == germline.births
        assert np.array_equal(acquired.resource, germline.resource)
        assert np.array_equal(acquired.energy, germline.energy)
        if acquired.births > before_births:
            # The newly allocated uid is the last one at the first birth tick;
            # matched RNG streams produce the same child slot in both worlds.
            uid = acquired.next_id - 1
            idx = int(np.flatnonzero(acquired.genome_id == uid)[0])
            assert uid == germline.next_id - 1
            assert germline.genome_id[idx] == uid
            parent_uid = acquired.lineage[uid]["parent"]
            parent = int(np.flatnonzero(acquired.genome_id == parent_uid)[0])
            assert acquired.germline[parent] == germline.germline[parent]
            return {
                "seed": seed,
                "first_birth_tick": step,
                "parent_acquired_threshold": float(acquired.thresholds[parent]),
                "parent_germline_threshold": float(acquired.germline[parent]),
                "child_acquired_inheritance": float(acquired.thresholds[idx]),
                "child_germline_only": float(germline.thresholds[idx]),
                "child_delta_equals_parent_acquisition": bool(np.isclose(
                    acquired.thresholds[idx] - germline.thresholds[idx],
                    acquired.thresholds[parent] - acquired.germline[parent])),
                "same_birth_location": True,
                "same_resource_and_energy_at_first_birth": True,
            }
    raise RuntimeError("No first birth in 300 ticks")


def main():
    seeds = list(range(2700, 2720))
    observations = [first_birth(seed) for seed in seeds]
    assert all(x["child_delta_equals_parent_acquisition"] for x in observations)
    folder = Path(__file__).parent
    out = {
        "hypothesis": "Only child inherited threshold differs at first birth; the parent learned/germline difference is faithfully transmitted without mutation",
        "status": "pass",
        "seeds": seeds,
        "observations": observations,
        "mean_absolute_acquired_delta_at_birth": float(np.mean([abs(x["child_acquired_inheritance"]-x["child_germline_only"]) for x in observations])),
        "not_evidence_of": "beneficial selection, biological Lamarckism, or improved ecological survival",
        "source_sha256": {x: hashlib.sha256((folder/x).read_bytes()).hexdigest()
                          for x in ("SOC_INHERITANCE_garden.py", "SOC_INHERITANCE_causal.py")},
    }
    (folder/"SOC_INHERITANCE_causal_results.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("PASS",len(observations),"paired first births, mean absolute transfer difference",out["mean_absolute_acquired_delta_at_birth"])


if __name__ == "__main__":
    main()
