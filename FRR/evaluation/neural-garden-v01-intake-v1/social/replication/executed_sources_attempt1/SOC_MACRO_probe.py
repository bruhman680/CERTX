"""Thirteen adaptive evidence loops on eight-state Neural Garden coarse-graining.

This experiment compares predictions of the SAME next eight-state microcategory
so fewer macro labels cannot win merely by making the prediction target easier.
No claim is made that these eight categories are C_num, C_struct, or C_symb.
"""

from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import numpy as np

from garden import Garden


HERE = Path(__file__).resolve().parent
SEEDS_TRAIN = list(range(4100, 4108))
SEEDS_TEST = list(range(5100, 5108))
SIZE = 10
STEPS = 420
R_CUT = .48
E_CUT = .12


def categorical(g: Garden) -> np.ndarray:
    """Binary resource, energy, and last-harvest action: eight categories."""
    return (((g.resource >= R_CUT).astype(np.int8) << 2)
            | ((g.energy >= E_CUT).astype(np.int8) << 1)
            | (g.last_action >= .5).astype(np.int8))


def trajectories(seeds: list[int]) -> np.ndarray:
    rows = []
    for seed in seeds:
        garden = Garden(seed=seed, size=SIZE, learning=True)
        sequence = [categorical(garden)]
        for _ in range(STEPS):
            garden.step()
            sequence.append(categorical(garden))
        rows.append(np.stack(sequence))
    return np.stack(rows)


def transition_data(seq: np.ndarray, mapping: np.ndarray, history: int):
    """Predict next microstate; represent past macro labels by mixed radix."""
    m = int(mapping.max() + 1)
    tmin = history
    tmax = seq.shape[1] - 1
    current = seq[:, tmin:tmax, :]
    target = seq[:, tmin + 1:tmax + 1, :].reshape(-1)
    feature = np.zeros_like(current, dtype=np.int32)
    for lag in range(history, -1, -1):
        feature *= m
        feature += mapping[seq[:, tmin - lag:tmax - lag, :]]
    return feature.reshape(-1), target, m ** (history + 1)


def predictive_nll(train, test, mapping, history=0):
    x, y, classes = transition_data(train, mapping, history)
    xt, yt, _ = transition_data(test, mapping, history)
    counts = np.full((classes, 8), .5, dtype=float)
    np.add.at(counts, (x, y), 1.)
    p = counts / counts.sum(axis=1, keepdims=True)
    nll = float(-np.log(p[xt, yt]).mean())
    # Holdout marginal entropy baseline, calculated with the same fixed scale.
    marginal = np.bincount(yt, minlength=8) / yt.size
    ent = float(-np.sum(marginal[marginal > 0] * np.log(marginal[marginal > 0])))
    return {"test_micro_nll": nll, "target_entropy_nats": ent,
            "micro_information_nats": ent - nll, "train_obs": int(x.size),
            "test_obs": int(xt.size), "parameter_rows": int(classes)}


def defect(train, mapping):
    """Weighted within-fibre outgoing TV divergence, on coarse next labels.

    Distinct current microstates in one coarse fibre have distinct transition
    distributions to NEXT MACRO label unless a Markov lumpability condition
    holds. The weighted TV is descriptive only and depends on data occupancy.
    """
    m = int(mapping.max() + 1)
    src = train[:, :-1, :].reshape(-1)
    dst = mapping[train[:, 1:, :].reshape(-1)]
    counts = np.zeros((8, m), dtype=float)
    np.add.at(counts, (src, dst), 1)
    support = counts.sum(axis=1)
    probs = counts / np.maximum(support[:, None], 1.)
    numer = 0.
    denom = 0.
    maximum = 0.
    active_pairs = 0
    for label in range(m):
        members = np.where((mapping == label) & (support > 0))[0]
        for i, a in enumerate(members):
            for b in members[i + 1:]:
                tv = float(.5 * np.abs(probs[a] - probs[b]).sum())
                w = float(min(support[a], support[b]))
                numer += w * tv
                denom += w
                maximum = max(maximum, tv)
                active_pairs += 1
    return {"weighted_tv_defect": float(numer / denom if denom else 0.),
            "max_tv_defect": maximum, "active_member_pairs": active_pairs,
            "supported_microstates": int((support > 0).sum())}


def normalize(labels):
    vals = sorted(set(int(v) for v in labels))
    rename = {v: i for i, v in enumerate(vals)}
    return np.array([rename[int(v)] for v in labels], dtype=np.int8)


def merge(labels, a, b):
    out = labels.copy()
    out[out == b] = a
    return normalize(out)


def best_merge(train, labels):
    """Choose pair by TRAIN micro prediction loss only, no test peeking."""
    present = list(range(int(labels.max() + 1)))
    choices = []
    for i, a in enumerate(present):
        for b in present[i + 1:]:
            candidate = merge(labels, a, b)
            x, y, rows = transition_data(train, candidate, 0)
            counts = np.full((rows, 8), .5, dtype=float)
            np.add.at(counts, (x, y), 1.)
            p = counts / counts.sum(axis=1, keepdims=True)
            loss = float(-np.log(p[x, y]).mean())
            choices.append((loss, a, b, candidate))
    return min(choices, key=lambda p: (p[0], p[1], p[2]))


def add_loop(log, train, test, orient, labels, history, pressure, extra=None):
    metrics = predictive_nll(train, test, labels, history)
    result = {"loop": len(log) + 1, "orientation": orient,
              "partition": [int(x) for x in labels],
              "macro_count": int(labels.max() + 1),
              "memory_lags": history, "metrics": metrics,
              "defect": defect(train, labels),
              "next_pressure": pressure}
    if extra:
        result["selection_basis"] = extra
    log.append(result)


def main():
    train = trajectories(SEEDS_TRAIN)
    test = trajectories(SEEDS_TEST)
    log = []
    labels = np.arange(8, dtype=np.int8)
    add_loop(log, train, test, "Establish full eight-category one-step reference", labels, 0,
             "Measure how much information a first merge erases; target remains eight micro categories.")
    k3 = None
    for k in [7, 6, 5, 4, 3, 2]:
        loss, a, b, labels = best_merge(train, labels)
        add_loop(log, train, test,
                 f"Merge one current-category fibre: {k+1} to {k} labels, based on training loss",
                 labels, 0,
                 "Assess heldout micro prediction and within-fibre macro transition defect before next merge.",
                 {"merged_training_labels": [a, b], "train_nll": loss})
        if k == 3:
            k3 = labels.copy()
    assert k3 is not None
    for history in [1, 2, 3]:
        add_loop(log, train, test,
                 f"Test whether {history} previous coarse state(s) repair lost predictive history",
                 k3, history,
                 "Check heldout target micro-NLL relative to history zero, controlling parameter growth.")
    # Three distinct projections from identical microstates; each gets the
    # same eight-state micro prediction burden. Not the theoretical C axes.
    for name, projection in [
        ("resource", np.array([v >> 2 for v in range(8)], dtype=np.int8)),
        ("energy", np.array([(v >> 1) & 1 for v in range(8)], dtype=np.int8)),
        ("action", np.array([v & 1 for v in range(8)], dtype=np.int8)),
    ]:
        add_loop(log, train, test,
                 f"Compare alternative observable projection: {name} alone",
                 projection, 0,
                 "Compare against learned two-way merge; do not relabel as C_num/C_struct/C_symb.")
    assert len(log) == 13
    output = {
        "study": "Neural Garden local eight-state coarse-graining, 13 adaptive research loops",
        "limitations": [
            "The greedy merge path is selected on training data; test observations are held out by seed.",
            "The 13 steps are distinct changes in representation or memory burden, not new natural discoveries.",
            "Binary categories deliberately erase continuous resources and energy and all neighbor and neural hidden-state information.",
            "Temporal observations from the same cell and run are dependent; seeds, not cells, are independent runs.",
            "Target remains the original eight-state micro category, preventing trivial target coarsening.",
            "Within-fibre TV defect measures coarse next-label inconsistency; test NLL measures next microstate predictive retention.",
        ],
        "world": {"size": SIZE, "ticks": STEPS, "r_cut": R_CUT, "e_cut": E_CUT,
                  "train_seeds": SEEDS_TRAIN, "test_seeds": SEEDS_TEST,
                  "learning": True, "python": platform.python_version(),
                  "numpy": np.__version__,
                  "garden_source_sha256": hashlib.sha256((HERE / 'garden.py').read_bytes()).hexdigest(),
                  "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
        "loops": log,
    }
    target = HERE / 'SOC_MACRO_results.json'
    target.write_text(json.dumps(output, indent=2) + '\n')
    print('completed', len(log), 'loops; output', target)
    for row in log:
        m = row['metrics']
        print(f"{row['loop']:2d} k={row['macro_count']} hist={row['memory_lags']} nll={m['test_micro_nll']:.5f} "
              f"info={m['micro_information_nats']:.5f} defect={row['defect']['weighted_tv_defect']:.5f} "
              f"{row['orientation'][:43]}")


if __name__ == '__main__':
    main()

