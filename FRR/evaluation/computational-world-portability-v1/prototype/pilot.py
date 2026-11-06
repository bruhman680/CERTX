"""Predeclared ten-call fixed-model interface pilot; never primary history."""
from pathlib import Path
import hashlib
import json
import os
import sys
import traceback

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent
ROOT = STUDY.parent.parent
BASE = Path('/workspace/cache_backend_models/smollm2-135m')
ACQ = ROOT / 'evaluation/simple-readout-acquisition-v1/run/canonical'
GARDEN = ROOT / 'evaluation/source-access-three-cycle-v1'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def put(path, value):
    with Path(path).open('x') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


CARD = '''A small persistent Scheme world. Reply with exactly ONE command, no prose or fences.
Commands: (run expression), (define (name x) expression), (run-save name expression), (inspect name), (page name value "" 32).
Scheme examples: (run (+ 1 1)), (define (inc x) (+ x 1)).
Numbers, text and quoted lists are values. Use car, cdr, null?, list, cons, +, *; (if test yes no) evaluates only the selected branch. Only #f is false.
This is an isolated turn with fixed execution/storage limits. A run computes; run-save retains its result.'''

CASES = [
    {'case': 'expression', 'setup': [],
     'request': 'Calculate 2 plus 3 with a run command.', 'host_probes': []},
    {'case': 'definition', 'setup': [],
     'request': 'Define a procedure named double with parameter x that returns x plus x.',
     'host_probes': ['(run (double 3))']},
    {'case': 'repair', 'setup': ['(define (first xs) (car xs))', "(run (first '()))"],
     'request': 'The world returned EMPTY_LIST for (first (quote ())). Revise first: return #f for an empty list, otherwise its first item.',
     'host_probes': ["(run (first '()))", "(run (first '(7)))"]},
    {'case': 'retrieval', 'setup': ['(put seed "a small retained text")'],
     'request': 'Read the first page of the value named seed. Use the page command.', 'host_probes': []},
    {'case': 'free_choice', 'setup': ["(put numbers '(1 2 4 8 16))"],
     'request': 'The world contains numbers = (1 2 4 8 16). You may inspect, experiment, construct or leave a note as data. Choose one action; no particular project is required.',
     'host_probes': []},
]


def main():
    os.environ['HF_HUB_OFFLINE'] = '1'
    os.environ['HF_HUB_DISABLE_PROGRESS_BARS'] = '1'
    sys.path.insert(0, '/workspace')
    sys.path.insert(0, str(GARDEN))
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    from lora_cpu import inject_lora, load_adapter
    from runtime_reference import Guard, parameter_digest
    from generate_capacity import generate
    from world_store import World
    from world_cli import run_isolated, compact_observation
    from world_bundle import export_world
    import scheme_core as sc

    destination = STUDY / 'pilot'
    destination.mkdir(exist_ok=False)
    for folder in ('starts', 'generations', 'receipts', 'initial_bundles', 'final_bundles'):
        (destination / folder).mkdir()
    # Live SQLite files stay outside published research artifacts.
    workspace = Path('/workspace/portability_pilot_worlds')
    workspace.mkdir(exist_ok=False)
    profile = json.loads((STUDY / 'constants.json').read_text())
    manifest = json.loads((ACQ / 'MANIFEST.json').read_text())
    pins = {str(p): sha(p) for p in (BASE / 'model.safetensors', ACQ / 'final/adapter.safetensors',
                                    ACQ / 'final/manifest.json', ACQ / 'MANIFEST.json')}
    assert pins[str(BASE / 'model.safetensors')] == manifest['base_pin']['weights_sha256']
    torch.set_num_threads(2)
    tokenizer = AutoTokenizer.from_pretrained(BASE, local_files_only=True, trust_remote_code=False)
    trials = []
    for seed in (110601, 110602):
        for case in CASES:
            identity = case['case'] + '_' + str(seed)
            db = workspace / (identity + '.sqlite')
            world = World(db, profile)
            setups = []
            for index, source in enumerate(case['setup']):
                setups.append(world.submit('setup-' + str(index), world.snapshot()['id'], source))
            snapshot = world.snapshot()
            export_world(world, destination / 'initial_bundles' / (identity + '.json'))
            world.close()
            prompt = CARD + '\n\n' + case['request'] + '\nYour command:'
            ids = tokenizer.apply_chat_template([{'role': 'user', 'content': prompt}],
                                                tokenize=True, add_generation_prompt=True)
            assert len(ids) <= 8096
            trials.append({'id': identity, 'case': case['case'], 'seed': seed,
                           'prompt': prompt, 'input_token_ids': ids, 'db': str(db),
                           'expected_snapshot': snapshot['id'], 'setup_receipts': setups,
                           'host_probes': case['host_probes']})
    plan = {'schema': 'cw-interface-pilot-1', 'trials': trials, 'calls': 10,
            'output_tokens_per_call': 96, 'input_token_limit': 8096,
            'temperature': .8, 'top_p': .9, 'threads': 2,
            'scope': 'Syntax-assisted fresh-context interface trials, not a continuous season or evidence of curiosity.',
            'rules': 'No output extraction, retries, automatic repair or training; save raw generation before dispatch.',
            'syntax_aid': CARD, 'scoring': 'Expression result5; double(3)=6; repaired first returns #f/7; retrieval executes page on seed; freechoice has no task-correctness score.',
            'model_file_pins': pins, 'code_pins': {str(p): sha(p) for p in sorted(HERE.glob('*.py'))},
            'profile_sha256': sha(STUDY / 'constants.json')}
    put(destination / 'PLAN.json', plan)
    guard = Guard(5153960755, destination / 'RESOURCE.jsonl')
    rows = []
    try:
        guard.read('before_model_load')
        model = AutoModelForCausalLM.from_pretrained(BASE, local_files_only=True, trust_remote_code=False,
                                                    use_safetensors=True, torch_dtype=torch.float32,
                                                    attn_implementation='eager')
        inject_lora(model, rank=4, alpha=8, dropout=0.)
        load_adapter(model, ACQ / 'final', base_pin=manifest['base_pin'])
        model.eval()
        assert parameter_digest(model, True) == manifest['final_digest']
        assert parameter_digest(model, False) == manifest['base_digest_after']
        for trial in trials:
            identity = trial['id']
            put(destination / 'starts' / (identity + '.json'),
                {'id': identity, 'seed': trial['seed'], 'plan_sha256': sha(destination / 'PLAN.json')})
            generation = generate(model, tokenizer, trial['prompt'], guard, identity, trial['seed'])
            assert generation['input_token_ids'] == trial['input_token_ids']
            assert tokenizer.decode(generation['generated_token_ids'], skip_special_tokens=True) == generation['text']
            put(destination / 'generations' / (identity + '.json'), generation)
            receipt = run_isolated(trial['db'], profile, 'model-action', trial['expected_snapshot'], generation['text'].strip())
            world = World(trial['db'], profile)
            probes = []
            for index, source in enumerate(trial['host_probes']):
                probes.append({'source': source, 'receipt': world.submit('host-probe-' + str(index),
                               world.snapshot()['id'], source), 'origin': 'predeclared host check, not model action'})
            score = None
            if trial['case'] == 'expression':
                score = receipt['status'] == 'COMPUTED' and type(receipt.get('value')) is int and receipt['value'] == 5
            elif trial['case'] == 'definition':
                score = receipt['status'] == 'PUBLISHED' and probes[0]['receipt']['status'] == 'COMPUTED' and type(probes[0]['receipt']['value']) is int and probes[0]['receipt']['value'] == 6
            elif trial['case'] == 'repair':
                score = receipt['status'] == 'PUBLISHED' and probes[0]['receipt']['status'] == 'COMPUTED' and probes[0]['receipt']['value'] is False and probes[1]['receipt']['status'] == 'COMPUTED' and type(probes[1]['receipt']['value']) is int and probes[1]['receipt']['value'] == 7
            elif trial['case'] == 'retrieval':
                value = receipt.get('value')
                score = receipt['status'] == 'OBSERVED' and isinstance(value, dict) and value.get('field') == 'value' and value.get('target') == world.snapshot()['aliases']['seed']['id']
            accepted = receipt.get('error') is None and receipt['status'] in ('COMPUTED', 'PUBLISHED', 'OBSERVED', 'ALIAS_DROPPED')
            row = {'id': identity, 'case': trial['case'], 'seed': trial['seed'], 'receipt': receipt,
                   'model_visible_receipt': compact_observation(receipt, profile), 'host_probes': probes,
                   'accepted_action': accepted, 'requested_outcome': score,
                   'not_primary_history': True, 'generation_saved_before_dispatch': True}
            put(destination / 'receipts' / (identity + '.json'), row)
            export_world(world, destination / 'final_bundles' / (identity + '.json'))
            world.close()
            rows.append(row)
            print(json.dumps({'id': identity, 'text': generation['text'],
                              'accepted': accepted, 'requested_outcome': score}), flush=True)
        assert parameter_digest(model, True) == manifest['final_digest']
        assert parameter_digest(model, False) == manifest['base_digest_after']
        assert all(sha(Path(path)) == value for path, value in pins.items())
        assert all(sha(Path(path)) == value for path, value in plan['code_pins'].items())
        put(destination / 'SUMMARY.json', {'calls': len(rows), 'accepted_actions': sum(x['accepted_action'] for x in rows),
            'requested_outcomes_correct': sum(x['requested_outcome'] is True for x in rows),
            'scored_task_calls': sum(x['requested_outcome'] is not None for x in rows),
            'free_choice_calls': 2, 'training_updates': 0, 'weights_and_adapter_unchanged': True,
            'rows': [{k: x[k] for k in ('id', 'case', 'seed', 'accepted_action', 'requested_outcome')} for x in rows],
            'scope': 'Small syntax-assisted interface pilot; no independence, open-ended growth or general reasoning claim.'})
    except BaseException as exc:
        put(destination / 'ERROR.json', {'error': repr(exc), 'traceback': traceback.format_exc(),
                                       'no_silent_retry': True, 'completed_receipts': len(rows)})
        raise


if __name__ == '__main__':
    main()
