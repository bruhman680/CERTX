"""Adaptive, predeclared eight-call example-attraction follow-up; no retries."""
from pathlib import Path
import json
import os
import sys

R = Path(__file__).resolve().parent
ROOT = R.parent.parent
P = R.parent / 'computational-world-portability-v1'
G = R.parent / 'source-access-three-cycle-v1'
BASE = Path('/workspace/cache_backend_models/smollm2-135m')
ACQ = R.parent / 'simple-readout-acquisition-v1/run/canonical'


def main():
    os.environ['HF_HUB_OFFLINE'] = '1'; os.environ['HF_HUB_DISABLE_PROGRESS_BARS'] = '1'
    sys.path.insert(0, str(P / 'prototype')); sys.path.insert(0, str(G)); sys.path.insert(0, '/workspace')
    from run import put, sha, VARIATIONS, SEEDS
    from world_store import World
    from world_cli import run_isolated
    from world_bundle import export_world
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    from lora_cpu import inject_lora, load_adapter
    from runtime_reference import Guard, parameter_digest
    from generate_capacity import generate

    out = R / 'example_probe'; out.mkdir(exist_ok=False)
    for folder in ('starts', 'generations', 'receipts', 'initial_bundles', 'final_bundles'):
        (out / folder).mkdir()
    workspace = Path('/workspace/scheme_example_probe_worlds'); workspace.mkdir(exist_ok=False)
    profile = json.loads((P / 'constants.json').read_text())
    manifest = json.loads((ACQ / 'MANIFEST.json').read_text())
    tok = AutoTokenizer.from_pretrained(BASE, local_files_only=True, trust_remote_code=False)
    torch.set_num_threads(2)
    trials = []
    for seed in SEEDS:
        for name, (request, expected) in VARIATIONS.items():
            parent = json.loads((R / 'receipts' / f'normal_variation_{name}_short_{seed}.json').read_text())['trial']
            for condition in ('no_example', 'example89'):
                identity = f'{name}_{condition}_{seed}'
                clause = '' if condition == 'no_example' else 'Example: (run (+ 8 9)). '
                prompt = 'Use a Scheme run command. ' + clause + request + ' Reply with one command only.'
                ids = tok.apply_chat_template([{'role': 'user', 'content': prompt}], tokenize=True, add_generation_prompt=True)
                if condition == 'example89': assert len(ids) == len(parent['input_token_ids'])
                db = workspace / (identity + '.sqlite'); world = World(db, profile)
                world.submit('host-setup', world.snapshot()['id'], '(put seed "bounded seed")')
                snapshot = world.snapshot()['id']
                export_world(world, out / 'initial_bundles' / (identity + '.json')); world.close()
                trials.append({'id': identity, 'seed': seed, 'case': name, 'condition': condition,
                               'prompt': prompt, 'input_token_ids': ids, 'expected_value': expected,
                               'db': str(db), 'snapshot': snapshot, 'matched_parent': parent['id']})
    pins = {str(p): sha(p) for p in (BASE / 'model.safetensors', ACQ / 'final/adapter.safetensors', ACQ / 'final/manifest.json', ACQ / 'MANIFEST.json')}
    code = [R / 'example_probe.py', R / 'run.py', G / 'generate_capacity.py', G / 'runtime_reference.py',
            Path('/workspace/lora_cpu.py'), *sorted((P / 'prototype').glob('*.py'))]
    plan = {'schema': 'example-attraction-followup-1', 'adaptive': True,
            'observed_trigger': 'Main variation replies repeatedly reproduced the shared non-target (+ 1 1) example; all requested sums failed.',
            'calls': 8, 'trials': trials, 'reused_example11_calls': 4,
            'question': 'Does changing example operands change the generated command while task stays fixed?',
            'prediction': 'Exploratory; no new confirmatory population hypothesis or held-out claim.',
            'settings': {'temperature': .8, 'top_p': .9, 'output_limit': 96, 'threads': 2},
            'analysis': 'Exact reply, accepted execution and requested-result score; report source-expression example matches without treating prose as action. example89 has matched token length to reused example11; no_example is shorter.',
            'model_file_pins': pins, 'code_pins': {str(p): sha(p) for p in code}}
    put(out / 'PLAN.json', plan)
    guard = Guard(5153960755, out / 'RESOURCE.jsonl'); guard.read('before_model_load')
    assert pins[str(BASE / 'model.safetensors')] == manifest['base_pin']['weights_sha256']
    model = AutoModelForCausalLM.from_pretrained(BASE, local_files_only=True, trust_remote_code=False,
                                                use_safetensors=True, torch_dtype=torch.float32, attn_implementation='eager')
    inject_lora(model, rank=4, alpha=8, dropout=0.)
    load_adapter(model, ACQ / 'final', base_pin=manifest['base_pin']); model.eval()
    assert parameter_digest(model, True) == manifest['final_digest'] and parameter_digest(model, False) == manifest['base_digest_after']
    rows = []
    for trial in trials:
        identity = trial['id']; put(out / 'starts' / (identity + '.json'), {'id': identity, 'plan_sha256': sha(out / 'PLAN.json')})
        generation = generate(model, tok, trial['prompt'], guard, identity, trial['seed'])
        assert generation['input_token_ids'] == trial['input_token_ids']
        put(out / 'generations' / (identity + '.json'), generation)
        receipt = run_isolated(trial['db'], profile, 'model-' + identity, trial['snapshot'], generation['text'].strip())
        accepted = receipt.get('error') is None and receipt['status'] in ('COMPUTED', 'PUBLISHED', 'OBSERVED', 'ALIAS_DROPPED')
        correct = receipt['status'] == 'COMPUTED' and type(receipt.get('value')) is int and receipt['value'] == trial['expected_value']
        record = {'id': identity, 'trial': trial, 'receipt': receipt, 'accepted_action': accepted,
                  'task_success': correct, 'example89_exact': generation['text'].strip() == '(run (+ 8 9))',
                  'example11_exact': generation['text'].strip() == '(run (+ 1 1))'}
        put(out / 'receipts' / (identity + '.json'), record); rows.append(record)
        world = World(trial['db'], profile); export_world(world, out / 'final_bundles' / (identity + '.json')); world.close()
        print(json.dumps({'id': identity, 'text': generation['text'], 'accepted': accepted, 'correct': correct}), flush=True)
    assert parameter_digest(model, True) == manifest['final_digest'] and parameter_digest(model, False) == manifest['base_digest_after']
    assert all(sha(p) == h for p, h in pins.items()) and all(sha(p) == h for p, h in plan['code_pins'].items())
    put(out / 'SUMMARY.json', {'calls': len(rows), 'correct': sum(x['task_success'] for x in rows),
                             'accepted': sum(x['accepted_action'] for x in rows), 'tensor_and_files_unchanged': True,
                             'rows': rows, 'scope': 'Adaptive content-specific example manipulation; not proof of internal mechanism.'})


if __name__ == '__main__': main()
