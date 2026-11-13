"""Transfer the eight-state coarse-graining probe across ecological policies.

Four evidence-driven passes: state occupancy, frozen mapping transfer,
history repair, and train-only reoptimized compression. Same microstate bins
and same seeds are used across original learned and fixed-.50 worlds.
"""

import hashlib
import json
from pathlib import Path

import numpy as np

from garden import Garden
from threshold_policy import ThresholdGarden
import SOC_MACRO_probe as macro


HERE = Path(__file__).resolve().parent
TRAIN = list(range(7200, 7208))
TEST = list(range(8200, 8208))
K3_FROM_LEARNED = np.array([0, 0, 1, 1, 0, 0, 2, 2], dtype=np.int8)


def observe(seeds, policy):
    result = []
    final = []
    for seed in seeds:
        if policy == 'learned_original':
            model = Garden(seed=seed, size=macro.SIZE, learning=True)
        elif policy == 'fixed_50':
            model = ThresholdGarden(seed=seed, size=macro.SIZE, threshold=.50)
        else:
            raise ValueError(policy)
        rows = [macro.categorical(model)]
        for _ in range(macro.STEPS):
            model.step()
            rows.append(macro.categorical(model))
        result.append(np.stack(rows))
        final.append({'seed': seed, 'energy': float(model.energy.mean()),
                      'resource': float(model.resource.mean()),
                      'floor_frac': float((model.energy <= .01).mean())})
    return np.stack(result), final


def fractions(arr):
    counts = np.bincount(arr.reshape(-1), minlength=8)
    return {'counts': counts.astype(int).tolist(),
            'fractions': (counts / counts.sum()).tolist(),
            'supported': int((counts > 0).sum()),
            'energy_high_frac': float(np.mean(((arr >> 1) & 1) > 0))}


def values(train, test, mapping):
    aligned = {'micro8_current': macro.predictive_nll(train, test, np.arange(8, dtype=np.int8), 0),
               'coarse3_current': macro.predictive_nll(train, test, mapping, 0),
               'coarse3_current_aligned': macro.predictive_nll(train[:, 3:], test[:, 3:], mapping, 0),
               'coarse3_memory3': macro.predictive_nll(train, test, mapping, 3),
               'within_fibre_defect': macro.defect(train, mapping)}
    aligned['memory_gain_nats'] = aligned['coarse3_current_aligned']['test_micro_nll'] - aligned['coarse3_memory3']['test_micro_nll']
    return aligned


def main():
    experiments = {}
    for policy in ['learned_original', 'fixed_50']:
        train, train_final = observe(TRAIN, policy)
        test, test_final = observe(TEST, policy)
        # Candidate k3 merge path chosen afresh on TRAIN data only.
        labels = np.arange(8, dtype=np.int8)
        merges = []
        for k in [7, 6, 5, 4, 3]:
            loss, a, b, labels = macro.best_merge(train, labels)
            merges.append({'k': k, 'merge': [a, b], 'train_loss': loss})
        experiments[policy] = {
            'train_occupancy': fractions(train),
            'test_occupancy': fractions(test),
            'final_train_worlds': train_final, 'final_test_worlds': test_final,
            'frozen_mapping': values(train, test, K3_FROM_LEARNED),
            'reoptimized_mapping': labels.astype(int).tolist(),
            'reoptimized_values': values(train, test, labels),
            'train_only_merge_path': merges,
        }
    report = {
        'study': 'Four conceptual transfer probes from collapsing v0.1 to fixed .50 policy',
        'train_seeds': TRAIN, 'test_seeds': TEST,
        'size': macro.SIZE, 'steps': macro.STEPS,
        'category': 'resource>=.48, energy>=.12, last_action harvest',
        'frozen_three_macro_labels': K3_FROM_LEARNED.tolist(),
        'source_sha256': {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest() for name in
            ['garden.py','threshold_policy.py','SOC_MACRO_probe.py','SOC_MACRO_TRANSFER_probe.py']},
        'experiments': experiments,
        'limitations': [
            'Eight-bit categories omit continuous state, neighbors, and recurrent neural states.',
            'Learned and deterministic fixed-policy worlds have different state-occupancy and target entropy; compare relative losses within each policy.',
            'Fixed .50 action largely covaries with current resource, so some eight categories are rare or impossible; smoothing affects NLL.',
            'Threshold policies are fixed by design, not autonomously discovered.',
            'Eight worlds per split are simulator seeds, not real-world replications.',
        ],
    }
    path = HERE / 'SOC_MACRO_TRANSFER_results.json'
    path.write_text(json.dumps(report, indent=2) + '\n')
    for key, value in experiments.items():
        a = value['frozen_mapping']; b = value['reoptimized_values']
        print(key, 'final energy', np.mean([e['energy'] for e in value['final_test_worlds']]),
              'high-energy occupancy', value['test_occupancy']['energy_high_frac'])
        print(' learned k3', a['coarse3_current_aligned']['test_micro_nll'],
              'memory3', a['coarse3_memory3']['test_micro_nll'],
              'gain', a['memory_gain_nats'])
        print(' new k3 labels', value['reoptimized_mapping'],
              'nll', b['coarse3_current_aligned']['test_micro_nll'],
              'memory gain', b['memory_gain_nats'])


if __name__ == '__main__':
    main()

