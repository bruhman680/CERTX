"""Post-bridge format control: single target record, same full-frame instruction."""
from pathlib import Path
import gc
import json
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))
import torch
import runtime_readout
from runtime_reference import sha, dump_new, Guard, parameter_digest
from lora_cpu import inject_lora, load_adapter
from bridge import parse

ACQUISITION = ROOT.parent.parent / 'simple-readout-acquisition-v1'

def prepare():
    assert json.loads((ROOT.parent / 'run/RUN_MANIFEST.json').read_text())['status'] == 'complete'
    plan = json.loads((ROOT.parent / 'PLAN.json').read_text())
    plan['prompt_template'] = 'Read only the record for the target plot.\n' + plan['prompt_template']
    bridge_cases = json.loads((ROOT.parent / 'DATA.json').read_text())
    cases = {}
    for c in bridge_cases:
        p = parse(c['source'])
        index = next(i for i, (n, s) in enumerate(p['records']) if n == p['target']) + 1
        source = f'Target plot: {p["target"]}\n\nRecord {index}:\n{p["crop"]}'
        # Deduplicate by actual prompt source, not by author metadata/number of parent occurrences.
        cases[source] = {'id': f'frame_{p["target"]}_{p["state"]}_{index}', 'source': source,
                         'state': p['state'], 'split': 'primary'}
    assert len(cases) == 12
    dump_new(ROOT / 'DATA.json', list(cases.values()))
    dump_new(ROOT / 'PLAN.json', plan)
    names = ['frame_control.py', 'PROTOCOL.md', 'PLAN.json', 'DATA.json']
    pins = {}
    for arm in plan['mappings']:
        for name in ('MANIFEST.json', 'final/adapter.safetensors', 'final/manifest.json'):
            p = ACQUISITION / 'run' / arm / name; pins[str(p)] = sha(p)
    for name in ('runtime_readout.py', 'runtime_reference.py', 'lora_cpu.py', 'bridge.py'):
        p = ROOT.parent / name; pins[str(p)] = sha(p)
    dump_new(ROOT / 'FREEZE.json', {'sha256': {n: sha(ROOT / n) for n in names}, 'dependencies': pins,
        'timing': 'control designed after first bridge alias result; frozen after complete bridge, before control model forwards',
        'no_retraining_or_winner_selection': True})

def run():
    from transformers import AutoTokenizer, AutoModelForCausalLM
    freeze = json.loads((ROOT / 'FREEZE.json').read_text())
    assert all(sha(ROOT / n) == h for n, h in freeze['sha256'].items())
    assert all(sha(Path(n)) == h for n, h in freeze['dependencies'].items())
    plan, cases = json.loads((ROOT / 'PLAN.json').read_text()), json.loads((ROOT / 'DATA.json').read_text())
    out = ROOT / 'run'; out.mkdir()
    # The frozen readout instrument writes to ROOT/run. Explicitly redirect only
    # its output destination, not its prompt/scoring/generation implementations.
    runtime_readout.ROOT = ROOT
    torch.set_num_threads(2)
    base = Path('/workspace/cache_backend_models/smollm2-135m')
    assert sha(base / 'model.safetensors') == plan['base_weights_sha256']
    tok = AutoTokenizer.from_pretrained(base, local_files_only=True, trust_remote_code=False)
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
        rows.extend(runtime_readout.evaluate(model, tok, cases, mapping, plan, arm, 'single_record_full_frame', guard))
        del model; gc.collect()
        print(json.dumps({'arm': arm, 'finished': True}), flush=True)
    summary = {}
    for arm in plan['mappings']:
        rs = [r for r in rows if r['arm'] == arm]
        assert len(rs) == 12
        summary[arm] = {'n': 12, 'free_correct': sum(r['free_correct'] for r in rs),
            'sum_correct': sum(r['sum_correct'] for r in rs), 'mean_correct': sum(r['mean_correct'] for r in rs),
            'unresolved': sum(r['free_state'] is None for r in rs),
            'by_state': {s: {'n': 4, 'free_correct': sum(r['state'] == s and r['free_correct'] for r in rs)} for s in mapping}}
    assert all(sha(Path(n)) == h for n, h in freeze['dependencies'].items())
    dump_new(out / 'SUMMARY.json', summary)
    dump_new(out / 'RUN_MANIFEST.json', {'status': 'complete', 'generation_calls': 48, 'candidate_scoring_batch_calls': 48,
        'candidate_sequences': 144, 'optimizer_updates': 0, 'frozen_dependencies_unchanged': True,
        'raw_sha256': sha(out / 'RAW.jsonl')})

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(); p.add_argument('stage', choices=['prepare', 'run']); a = p.parse_args()
    prepare() if a.stage == 'prepare' else run()
