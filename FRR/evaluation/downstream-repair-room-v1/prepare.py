"""Freeze real-error replay plus fresh balanced seed controls before any forwards."""
from pathlib import Path
import hashlib
import json
from evidence import parse, STATES, MAPPING

ROOT = Path(__file__).resolve().parent
OLD = ROOT.parent / 'readout-selection-bridge-v1'
ACQUISITION = ROOT.parent / 'simple-readout-acquisition-v1'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def put(name, obj):
    with (ROOT / name).open('x') as f:
        json.dump(obj, f, sort_keys=True, indent=2); f.write('\n')

def main():
    prior = [json.loads(s) for s in (OLD / 'run/RAW.jsonl').read_text().splitlines()]
    actual = {r['id']: r for r in prior if r['arm'] == 'canonical' and r['phase'] == 'full'}
    data = []
    for old in json.loads((OLD / 'DATA.json').read_text()):
        p = parse(old['source']); raw = actual[old['id']]
        assert p['state'] == old['state'] == raw['state']
        assert raw['free_state'] is not None  # scope: actual valid-label errors
        data.append({'id': 'replay_' + old['id'], 'cohort': 'replay',
            'source': old['source'], 'state': p['state'],
            'proposal': raw['text'].strip(), 'proposal_state': raw['free_state'],
            'upstream_record_id': old['id'], 'upstream_raw_sha256': sha(OLD / 'run/RAW.jsonl')})
    assert len(data) == 36
    assert sum(c['proposal_state'] == c['state'] for c in data) == 23
    # New study-held-out sources, balanced state/target/order, cyclic distractor.
    # This is a deliberately limited subset, not all distractor assignments.
    for target in ('Spruce', 'Fir'):
        other = 'Fir' if target == 'Spruce' else 'Spruce'
        for i, state in enumerate(STATES):
            for order in range(2):
                recs = [(target, state), (other, STATES[(i+1)%3])]
                if order:
                    recs.reverse()
                body = '\n\n'.join(f'Record {j+1}:\nPlot: {n}\nStatus: {s}' for j, (n, s) in enumerate(recs))
                source = f'Target plot: {target}\n\n{body}'
                assert parse(source)['state'] == state
                data.append({'id': f'fresh_{target}_{state}_{order}', 'cohort': 'fresh',
                             'source': source, 'state': state})
    conditions = ['baseline_full', 'baseline_selected', 'wrong_selection',
                  'proposal_only', 'reopen_full', 'reopen_selected']
    calls = []
    for c in data:
        for condition in conditions[:3]:
            calls.append({'case_id': c['id'], 'condition': condition, 'seed': 'none'})
        seeds = ['actual'] if c['cohort'] == 'replay' else ['correct', 'wrong1', 'wrong2']
        for seed in seeds:
            for condition in conditions[3:]:
                calls.append({'case_id': c['id'], 'condition': condition, 'seed': seed})
    assert len(calls) == 360
    plan = json.loads((ACQUISITION / 'PLAN.json').read_text())
    mapping = plan['mappings']['canonical']
    assert mapping == MAPPING
    put('DATA.json', data)
    put('CALLS.json', calls)
    put('PLAN.json', {'mapping': mapping, 'seed': plan['seed'], 'max_tokens': 8,
        'working_limit_bytes': plan['working_limit_bytes'],
        'base_revision': plan['base_revision'], 'base_weights_sha256': plan['base_weights_sha256'],
        'generation_calls': 360, 'optimizer_updates': 0,
        'base_template': 'Map the status to its answer. {mapping}. Return only the answer.\n\n{source}',
        'full_prefix': 'Read only the record for the target plot.\n',
        'proposal_prefix': 'Earlier answer proposal: {proposal}\nThis proposal may be wrong. Check the available evidence before answering.\n',
        'no_evidence_source': 'No source record is available in this step.',
        'interpretation': 'one bounded downstream pass in fresh contexts; no learning, no independent-agent benefit, no explicit model error-awareness test',
        'retry_or_selection': 'none; fixed final canonical adapter and all scheduled calls'})
    dependencies = [OLD / 'DATA.json', OLD / 'run/RAW.jsonl',
        ACQUISITION / 'run/canonical/MANIFEST.json',
        ACQUISITION / 'run/canonical/final/adapter.safetensors',
        ACQUISITION / 'run/canonical/final/manifest.json']
    names = ['DATA.json', 'CALLS.json', 'PLAN.json', 'PROTOCOL.md', 'evidence.py',
             'prepare.py', 'run_room.py', 'score.py', 'test_room.py',
             'runtime_readout.py', 'runtime_reference.py', 'lora_cpu.py']
    put('FREEZE.json', {'sha256': {n: sha(ROOT / n) for n in names},
            'dependencies': {str(p): sha(p) for p in dependencies},
            'timing': 'after previous results, before all new replay/fresh model forwards'})
    print('Frozen 36 actual-proposal replay sources +12 fresh sources;360 calls')

if __name__ == '__main__':
    main()
