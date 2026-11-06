"""Fixed 48-call calibration. Frozen weights; strict full-reply dispatch."""
from pathlib import Path
import hashlib
import json
import os
import sys
import traceback

R = Path(__file__).resolve().parent
ROOT = R.parent.parent
P = R.parent / 'computational-world-portability-v1'
G = R.parent / 'source-access-three-cycle-v1'
BASE = Path('/workspace/cache_backend_models/smollm2-135m')
ACQ = R.parent / 'simple-readout-acquisition-v1/run/canonical'
SEEDS = (110611, 110612)
TARGETS = {'literal': '(run 3)', 'addition': '(run (+ 2 3))',
           'definition': '(define (double x) (+ x x))', 'page': '(page seed value "" 32)'}
VARIATIONS = {'add23': ('Calculate 2 plus 3.', 5), 'add47': ('Calculate 4 plus 7.', 11)}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def put(path, value):
    with Path(path).open('x') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2); stream.write('\n')


def main():
    os.environ['HF_HUB_OFFLINE'] = '1'
    os.environ['HF_HUB_DISABLE_PROGRESS_BARS'] = '1'
    sys.path.insert(0, str(P / 'prototype')); sys.path.insert(0, str(G)); sys.path.insert(0, '/workspace')
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    from lora_cpu import inject_lora, load_adapter
    from runtime_reference import Guard, parameter_digest
    from generate_capacity import generate
    from world_store import World
    from world_cli import run_isolated
    from world_bundle import export_world, import_world
    import scheme_core as sc

    for folder in ('starts', 'generations', 'receipts', 'initial_bundles', 'final_bundles', 'feedback_plans'):
        (R / folder).mkdir(exist_ok=False)
    workspace = Path('/workspace/scheme_calibration_worlds'); workspace.mkdir(exist_ok=False)
    profile = json.loads((P / 'constants.json').read_text())
    prior = json.loads((P / 'pilot/PLAN.json').read_text()); card = prior['syntax_aid']
    tok = AutoTokenizer.from_pretrained(BASE, local_files_only=True, trust_remote_code=False)
    torch.set_num_threads(2)
    manifest = json.loads((ACQ / 'MANIFEST.json').read_text())
    files = [BASE / 'model.safetensors', BASE / 'tokenizer.json', BASE / 'tokenizer_config.json',
             ACQ / 'final/adapter.safetensors', ACQ / 'final/manifest.json', ACQ / 'MANIFEST.json']
    pins = {str(p): sha(p) for p in files}
    assert pins[str(BASE / 'model.safetensors')] == manifest['base_pin']['weights_sha256']
    trials = []
    for variant in ('normal', 'scale_zero'):
        for seed in SEEDS:
            for text in ('hello', '37'):
                trials.append({'id': f'{variant}_plain_{text}_{seed}', 'variant': variant, 'block': 'plain',
                               'seed': seed, 'target': text, 'prompt': 'Copy the following text exactly. Output only this one line:\n' + text})
            selected = TARGETS if variant == 'normal' else {k: TARGETS[k] for k in ('literal', 'definition')}
            for name, target in selected.items():
                for condition in ('short', 'broad'):
                    prompt = 'Copy the following text exactly. Output only this one line:\n' + target
                    if condition == 'broad': prompt = card + '\n\n' + prompt
                    trials.append({'id': f'{variant}_copy_{name}_{condition}_{seed}', 'variant': variant,
                                   'block': 'copy', 'case': name, 'condition': condition,
                                   'seed': seed, 'target': target, 'prompt': prompt})
            if variant == 'normal':
                for name, (request, expected) in VARIATIONS.items():
                    for condition in ('short', 'broad'):
                        prompt = 'Use a Scheme run command. Example: (run (+ 1 1)). ' + request + ' Reply with one command only.'
                        if condition == 'broad': prompt = card + '\n\n' + prompt
                        trials.append({'id': f'normal_variation_{name}_{condition}_{seed}', 'variant': variant,
                                       'block': 'variation', 'case': name, 'condition': condition,
                                       'seed': seed, 'expected_value': expected, 'prompt': prompt})
    for trial in trials:
        trial['input_token_ids'] = tok.apply_chat_template([{'role': 'user', 'content': trial['prompt']}], tokenize=True, add_generation_prompt=True)
        assert len(trial['input_token_ids']) <= 8096
        if trial['block'] != 'plain':
            db = workspace / (trial['id'] + '.sqlite'); world = World(db, profile)
            world.submit('host-setup', world.snapshot()['id'], '(put seed "bounded seed")')
            trial['db'] = str(db); trial['snapshot'] = world.snapshot()['id']
            export_world(world, R / 'initial_bundles' / (trial['id'] + '.json')); world.close()
    plan = {'schema': 'scheme-command-calibration-1', 'calls': 48,
            'static_calls': len(trials), 'feedback_calls': 8, 'trials': trials,
            'feedback': {'parents': 'normal short-card variation, both tasks/seeds; reuse those first calls',
                'arms': ['receipt', 'practice'], 'second_seed': 'parent seed + 1000',
                'construction': 'same prior prompt and model reply; receipt arm adds actual status/error/value, practice arm withholds receipt; both same task restatement and next-command cue',
                'policy': 'include successful and failed parents, no selection/retry; prompts frozen per pair before its generation'},
            'settings': {'temperature': .8, 'top_p': .9, 'output_limit': 96, 'input_limit': 8096, 'threads': 2},
            'reference': {'paired_subset': 'plain targets plus literal/definition copies, both cards/seeds',
                'intervention': 'all LoRALinear.scale 2 to 0 in this process only; tensors/files unchanged'},
            'scoring': 'entire reply stripped only; literal match, accepted execution and semantic task score separate; plain is not dispatched; feedback paired, not independent calls',
            'source_card_sha256': sha(P / 'pilot/PLAN.json'), 'model_file_pins': pins,
            'code_pins': {str(p): sha(p) for p in [R / 'run.py', *sorted((P / 'prototype').glob('*.py'))]},
            'profile_sha256': sha(P / 'constants.json')}
    assert len(trials) == 40
    put(R / 'PLAN.json', plan)
    guard = Guard(5153960755, R / 'RESOURCE.jsonl'); rows = []; by_id = {}

    def call(trial):
        identity = trial['id']
        put(R / 'starts' / (identity + '.json'), {'id': identity, 'seed': trial['seed'], 'plan_sha256': sha(R / 'PLAN.json')})
        row = generate(model, tok, trial['prompt'], guard, identity, trial['seed'])
        assert row['input_token_ids'] == trial['input_token_ids']
        put(R / 'generations' / (identity + '.json'), row)
        text = row['text'].strip(); result = None; probes = []; accepted = None
        exact = text == trial['target'] if 'target' in trial else None
        success = exact if trial['block'] == 'plain' else False
        if trial['block'] != 'plain':
            result = run_isolated(trial['db'], profile, 'model-' + identity, trial['snapshot'], text)
            accepted = result.get('error') is None and result['status'] in ('COMPUTED', 'PUBLISHED', 'OBSERVED', 'ALIAS_DROPPED')
            world = World(trial['db'], profile)
            if trial.get('case') == 'definition':
                probe = world.submit('host-probe', world.snapshot()['id'], '(run (double 3))'); probes.append(probe)
                success = result['status'] == 'PUBLISHED' and probe['status'] == 'COMPUTED' and type(probe['value']) is int and probe['value'] == 6
            elif trial.get('case') == 'page':
                value = result.get('value'); success = result['status'] == 'OBSERVED' and isinstance(value, dict) and value.get('target') == world.snapshot()['aliases']['seed']['id'] and value.get('field') == 'value'
            else:
                expected = trial.get('expected_value', 3 if trial.get('case') == 'literal' else 5)
                success = result['status'] == 'COMPUTED' and type(result.get('value')) is int and result['value'] == expected
            export_world(world, R / 'final_bundles' / (identity + '.json')); world.close()
        record = {'id': identity, 'trial': trial, 'receipt': result, 'host_probes': probes,
                  'literal_match': exact, 'accepted_action': accepted, 'task_success': bool(success),
                  'not_primary_history': True, 'raw_saved_before_dispatch': True}
        put(R / 'receipts' / (identity + '.json'), record); rows.append(record); by_id[identity] = record
        print(json.dumps({'id': identity, 'text': row['text'], 'exact': exact, 'accepted': accepted, 'success': bool(success)}), flush=True)

    try:
        guard.read('before_model_load')
        model = AutoModelForCausalLM.from_pretrained(BASE, local_files_only=True, trust_remote_code=False, use_safetensors=True,
                                                    torch_dtype=torch.float32, attn_implementation='eager')
        inject_lora(model, rank=4, alpha=8, dropout=0.)
        load_adapter(model, ACQ / 'final', base_pin=manifest['base_pin']); model.eval()
        assert parameter_digest(model, True) == manifest['final_digest']
        assert parameter_digest(model, False) == manifest['base_digest_after']
        for trial in (t for t in trials if t['variant'] == 'normal'): call(trial)
        # Fork both continuations from the identical actual first-turn world.
        for parent in (t for t in trials if t['block'] == 'variation' and t['condition'] == 'short'):
            previous = json.loads((R / 'generations' / (parent['id'] + '.json')).read_text())['text']
            receipt = by_id[parent['id']]['receipt']
            signal = {'status': receipt['status'], 'error': receipt.get('error'), 'value': receipt.get('value')}
            pair = []
            for arm in ('receipt', 'practice'):
                identity = parent['id'] + '_follow_' + arm
                db = workspace / (identity + '.sqlite')
                import_world(R / 'final_bundles' / (parent['id'] + '.json'), db, profile)
                world = World(db, profile); snapshot = world.snapshot()['id']
                export_world(world, R / 'initial_bundles' / (identity + '.json')); world.close()
                prompt = parent['prompt'] + '\n\nYour previous reply:\n' + previous
                prompt += '\n\n' + ('Actual world receipt: ' + json.dumps(signal, ensure_ascii=False) if arm == 'receipt' else 'World receipt withheld for this practice control.')
                prompt += '\n\nTask: ' + VARIATIONS[parent['case']][0] + ' Reply with one Scheme run command only.'
                trial = {'id': identity, 'variant': 'normal', 'block': 'feedback', 'case': parent['case'],
                         'condition': arm, 'parent': parent['id'], 'seed': parent['seed'] + 1000,
                         'expected_value': parent['expected_value'], 'prompt': prompt, 'db': str(db), 'snapshot': snapshot}
                trial['input_token_ids'] = tok.apply_chat_template([{'role': 'user', 'content': prompt}], tokenize=True, add_generation_prompt=True)
                assert len(trial['input_token_ids']) <= 8096; pair.append(trial)
            put(R / 'feedback_plans' / (parent['id'] + '.json'), {'parent': parent['id'], 'parent_generation_sha256': sha(R / 'generations' / (parent['id'] + '.json')), 'pair': pair})
            for trial in pair: call(trial)
        scales = {name: float(module.scale) for name, module in model.named_modules() if module.__class__.__name__ == 'LoRALinear'}
        assert scales and all(v == 2. for v in scales.values())
        for module in model.modules():
            if module.__class__.__name__ == 'LoRALinear': module.scale = 0.
        put(R / 'REFERENCE_CONFIG.json', {'before': scales, 'after': {k: 0. for k in scales}, 'tensor_changes': 0, 'original_primary_changed': False})
        for trial in (t for t in trials if t['variant'] == 'scale_zero'): call(trial)
        assert len(rows) == 48
        assert parameter_digest(model, True) == manifest['final_digest']
        assert parameter_digest(model, False) == manifest['base_digest_after']
        assert all(sha(path) == value for path, value in pins.items())
        assert all(sha(path) == value for path, value in plan['code_pins'].items())
        put(R / 'SUMMARY.json', {'calls': len(rows), 'training_updates': 0, 'tensor_and_asset_pins_unchanged': True,
            'rows': [{k: row[k] for k in ('id', 'literal_match', 'accepted_action', 'task_success')} for row in rows],
            'scope': 'Small paired interface diagnostics; feedback continuations dependent; no model-wide adapter ranking or continuous learning claim.'})
    except BaseException as exc:
        put(R / 'ERROR.json', {'error': repr(exc), 'traceback': traceback.format_exc(), 'completed_receipts': len(rows), 'no_silent_retry': True})
        raise


if __name__ == '__main__': main()
