"""Untouched-seed confirmation of the coarse-state memory prediction probe."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import SOC_MACRO_probe as study


def main():
    train = study.trajectories(study.SEEDS_TRAIN)
    holdout = study.trajectories(list(range(6100, 6108)))
    records = json.loads((study.HERE / 'SOC_MACRO_results.json').read_text())['loops']
    three = np.array(records[5]['partition'], dtype=np.int8)
    eight = np.arange(8, dtype=np.int8)
    # For the memory comparison align the target time indices: history=3
    # cannot score the first three ticks, so omit them also for history=0.
    out = {"new_holdout_seeds": list(range(6100, 6108)),
           "frozen_three_macro_partition": three.tolist(),
           "full_eight_current": study.predictive_nll(train, holdout, eight, 0),
           "three_current": study.predictive_nll(train, holdout, three, 0),
           "three_current_aligned": study.predictive_nll(train[:, 3:, :], holdout[:, 3:, :], three, 0),
           "three_three_lags": study.predictive_nll(train, holdout, three, 3)}
    (study.HERE / 'SOC_MACRO_confirm_results.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
