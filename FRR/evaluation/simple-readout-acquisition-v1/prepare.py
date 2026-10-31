"""Author/freeze a small explicit-status readout contact before model forwards."""
from pathlib import Path
import hashlib
import json
import random

ROOT = Path(__file__).resolve().parent

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def put(name, obj):
    with (ROOT / name).open('x') as f:
        json.dump(obj, f, indent=2, sort_keys=True); f.write('\n')

def main():
    states = ['positive', 'zero', 'missing']
    data = []
    for split, plots in [('seen', ['Alder', 'Birch', 'Cedar', 'Elm']),
                         ('primary', ['Hazel', 'Larch', 'Maple', 'Willow'])]:
        for i, plot in enumerate(plots):
            for state in states:
                data.append({'id': f'{split}_{i}_{state}', 'split': split,
                             'source': f'Plot: {plot}\nStatus: {state}', 'state': state})
    mappings = {'canonical': dict(zip(states, ['YES', 'NO', 'WITHHOLD']))}
    for i in range(3):
        labels = ['A', 'B', 'C']
        mappings[f'alias_{i}'] = dict(zip(states, labels[i:] + labels[:i]))
    rng = random.Random(73103)
    groups = []
    for epoch in range(12):
        indices = list(range(4)); rng.shuffle(indices)
        for index in indices:
            group = [f'seen_{index}_{state}' for state in states]
            rotation = len(groups) % 3
            groups.append(group[rotation:] + group[:rotation])
    put('DATA.json', data)
    put('PLAN.json', {'seed': 73103, 'mappings': mappings, 'order': groups,
        'updates': 48, 'lr': .001, 'weight_decay': .01, 'rank': 4, 'alpha': 8,
        'objective': 'mean complete answer plus EOS', 'max_tokens': 8,
        'training_wall_seconds_per_arm': 300, 'working_limit_bytes': 5153960755,
        'train_token_guard': 128, 'base_revision': '12fd25f77366fa6b3b4b768ec3050bf629380bac',
        'base_weights_sha256': '5af571cbf074e6d21a03528d2330792e532ca608f24ac70a143f6b369968ab8c',
        'interpretation': 'interface-package and acquisition contact, not pure token-length effect or harder-task transfer',
        'retries': 0, 'checkpoint_selection': 'final fixed48 updates only',
        'candidate_score_policy': 'argmax sum logprob of complete label including EOS; length-normalized diagnostic separate',
        'prompt_template': 'Map the status to its answer. {mapping}. Return only the answer.\n\n{source}',
        'decision': 'report exact free-generation and constrained per-state counts; no promotion or universal threshold'})
    assert len({c['source'] for c in data}) == 24
    assert len(groups) == 48
    assert all({x.rsplit('_', 1)[1] for x in g} == set(states) for g in groups)
    names = ['DATA.json', 'PLAN.json', 'PROTOCOL.md', 'prepare.py', 'run.py',
             'test_readout.py', 'lora_cpu.py', 'runtime_reference.py']
    put('FREEZE.json', {'sha256': {name: sha(ROOT / name) for name in names},
                         'timing': 'before tokenizer/model load and all new forwards'})
    print('Frozen 24 cases, 4 mappings, 48 updates per mapping')

if __name__ == '__main__':
    main()
