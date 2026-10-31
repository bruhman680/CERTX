"""Fresh two-record readout bridge; no optimizer updates or model selection."""
from pathlib import Path
import gc
import json
import os
import re

os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['HF_HUB_DISABLE_PROGRESS_BARS'] = '1'
import torch
from lora_cpu import inject_lora, load_adapter
from runtime_reference import Guard, dump_new, sha, parameter_digest
from runtime_readout import evaluate

ROOT = Path(__file__).resolve().parent
ACQUISITION = ROOT.parent / 'simple-readout-acquisition-v1'

def parse(source):
    match = re.fullmatch(r'Target plot: (Oak|Beech)\n\nRecord 1:\nPlot: (Oak|Beech)\nStatus: (positive|zero|missing)\n\nRecord 2:\nPlot: (Oak|Beech)\nStatus: (positive|zero|missing)', source)
    if match is None:
        raise ValueError('Source outside this small grammar')
    target, n1, s1, n2, s2 = match.groups()
    if n1 == n2 or target not in (n1, n2):
        raise ValueError('Duplicate/absent target')
    records = [(n1, s1), (n2, s2)]
    chosen = next((name, state) for name, state in records if name == target)
    crop = f'Plot: {chosen[0]}\nStatus: {chosen[1]}'
    return {'target': target, 'records': records, 'state': chosen[1], 'crop': crop}

def prepare():
    # Freeze only after every acquisition arm has reached its final checkpoint.
    prior = json.loads((ACQUISITION / 'run/RUN_MANIFEST.json').read_text())
    assert prior['status'] == 'complete'
    plan = json.loads((ACQUISITION / 'PLAN.json').read_text())
    plan['prompt_template'] = ('Map the status to its answer. {mapping}. Return only the answer.\n\n{source}')
    data = []
    states = ('positive', 'zero', 'missing')
    for order in range(2):
        for a in states:
            for b in states:
                recs = [('Oak', a), ('Beech', b)]
                if order:
                    recs.reverse()
                body = '\n\n'.join(f'Record {i+1}:\nPlot: {n}\nStatus: {s}' for i, (n, s) in enumerate(recs))
                for target in ('Oak', 'Beech'):
                    source = f'Target plot: {target}\n\n{body}'
                    parsed = parse(source)
                    data.append({'id': f'bridge_{order}_{a}_{b}_{target}', 'split': 'primary',
                                 'source': source, 'state': parsed['state'],
                                 'pair_id': f'pair_{order}_{a}_{b}', 'discordant': a != b})
    assert len(data) == 36
    dump_new(ROOT / 'DATA.json', data)
    dump_new(ROOT / 'PLAN.json', plan)
    checkpoints = {}
    for arm in plan['mappings']:
        directory = ACQUISITION / 'run' / arm
        paths = [directory / 'MANIFEST.json', directory / 'final/manifest.json', directory / 'final/adapter.safetensors']
        checkpoints[arm] = {str(p): sha(p) for p in paths}
    paths = ['bridge.py', 'test_bridge.py', 'PROTOCOL.md', 'DATA.json', 'PLAN.json',
             'runtime_readout.py', 'lora_cpu.py', 'runtime_reference.py']
    dump_new(ROOT / 'FREEZE.json', {'sha256': {name: sha(ROOT / name) for name in paths},
              'acquisition_checkpoints': checkpoints,
              'timing': 'after acquisition outcomes, before any new two-record model forward',
              'arm_selection': 'all four fixed arms, no winner selection'})

def score(rows):
    results = {}
    for arm in sorted({r['arm'] for r in rows}):
        results[arm] = {}
        for condition in ('full', 'cropped'):
            rs = [r for r in rows if r['arm'] == arm and r['phase'] == condition]
            bypair = {}
            for r in rs:
                bypair.setdefault(r['pair_id'], []).append(r)
            assert len(rs) == 36 and all(len(g) == 2 for g in bypair.values())
            discordant = [g for g in bypair.values() if g[0]['discordant']]
            results[arm][condition] = {'n': 36,
                'free_correct': sum(r['free_correct'] for r in rs),
                'constrained_sum_correct': sum(r['sum_correct'] for r in rs),
                'constrained_mean_correct': sum(r['mean_correct'] for r in rs),
                'unresolved': sum(r['free_state'] is None for r in rs),
                'by_state': {s: {'n': sum(r['state'] == s for r in rs),
                    'free_correct': sum(r['state'] == s and r['free_correct'] for r in rs)}
                    for s in ('positive', 'zero', 'missing')},
                'discordant_n': 24, 'discordant_free_correct': sum(r['free_correct'] for g in discordant for r in g),
                'fully_correct_discordant_pairs': sum(all(r['free_correct'] for r in g) for g in discordant),
                'changed_answer_discordant_pairs': sum(g[0]['free_state'] != g[1]['free_state'] for g in discordant),
                'discordant_pairs': 12}
    return results

def run():
    from transformers import AutoModelForCausalLM, AutoTokenizer
    freeze = json.loads((ROOT / 'FREEZE.json').read_text())
    assert all(sha(ROOT / n) == h for n, h in freeze['sha256'].items())
    assert all(sha(Path(n)) == h for paths in freeze['acquisition_checkpoints'].values() for n, h in paths.items())
    plan, cases = json.loads((ROOT / 'PLAN.json').read_text()), json.loads((ROOT / 'DATA.json').read_text())
    out = ROOT / 'run'; out.mkdir()
    torch.set_num_threads(2)
    base = Path('/workspace/cache_backend_models/smollm2-135m')
    assert sha(base / 'model.safetensors') == plan['base_weights_sha256']
    tok = AutoTokenizer.from_pretrained(base, local_files_only=True, trust_remote_code=False)
    # Full prompts explicitly ask which record is relevant, in addition to mapping.
    fullplan = {**plan, 'prompt_template': 'Read only the record for the target plot.\n' + plan['prompt_template']}
    guard = Guard(plan['working_limit_bytes'], out / 'RESOURCE.jsonl')
    rows = []
    for arm, mapping in plan['mappings'].items():
        torch.manual_seed(plan['seed']); guard.read('before_load', arm=arm)
        model = AutoModelForCausalLM.from_pretrained(base, local_files_only=True, trust_remote_code=False,
                use_safetensors=True, torch_dtype=torch.float32, attn_implementation='eager')
        inject_lora(model, rank=4, alpha=8, dropout=0.)
        manifest = json.loads((ACQUISITION / 'run' / arm / 'MANIFEST.json').read_text())
        load_adapter(model, ACQUISITION / 'run' / arm / 'final', base_pin=manifest['base_pin'])
        assert parameter_digest(model, True) == manifest['final_digest']
        assert parameter_digest(model, False) == manifest['base_digest_after']
        for condition in ('full', 'cropped'):
            inputs = []
            for case in cases:
                chosen = parse(case['source'])
                assert chosen['state'] == case['state']
                inputs.append({**case, 'source': case['source'] if condition == 'full' else chosen['crop']})
            before = len(rows)
            got = evaluate(model, tok, inputs, mapping, fullplan if condition == 'full' else plan,
                           arm, condition, guard)
            # evaluate writes frozen raw evidence; side metadata joined by ID below.
            rows.extend({**r, 'pair_id': case['pair_id'], 'discordant': case['discordant']}
                        for r, case in zip(got, cases))
            assert len(rows)-before == 36
        del model; gc.collect()
        print(json.dumps({'arm': arm, 'finished': True}), flush=True)
    assert len(rows) == 288
    dump_new(out / 'SUMMARY.json', score(rows))
    assert sha(base / 'model.safetensors') == plan['base_weights_sha256']
    assert all(sha(Path(n)) == h for paths in freeze['acquisition_checkpoints'].values() for n, h in paths.items())
    dump_new(out / 'RUN_MANIFEST.json', {'status': 'complete', 'generation_calls': 288,
        'candidate_scoring_batch_calls': 288, 'candidate_sequences': 864,
        'optimizer_updates': 0, 'checkpoints_unchanged': True, 'raw_sha256': sha(out / 'RAW.jsonl'),
        'freeze_sha256': sha(ROOT / 'FREEZE.json')})

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(); p.add_argument('stage', choices=['prepare', 'run']); args = p.parse_args()
    prepare() if args.stage == 'prepare' else run()
