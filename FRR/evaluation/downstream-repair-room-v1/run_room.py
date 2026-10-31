"""Allow every scheduled imperfect proposal to reach one bounded downstream step."""
from pathlib import Path
import json
import os

os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['HF_HUB_DISABLE_PROGRESS_BARS'] = '1'
import torch
import runtime_readout
from runtime_reference import Guard, sha, dump_new, append_json, parameter_digest
from lora_cpu import inject_lora, load_adapter
from evidence import parse, STATES

ROOT = Path(__file__).resolve().parent
ACQUISITION = ROOT.parent / 'simple-readout-acquisition-v1'

def material(case, call, plan):
    p = parse(case['source']); condition = call['condition']
    if condition in ('baseline_full', 'reopen_full'):
        delivered, kind = case['source'], 'full'
    elif condition in ('baseline_selected', 'reopen_selected'):
        delivered, kind = p['crop'], 'selected'
    elif condition == 'wrong_selection':
        delivered, kind = p['other_crop'], 'selected'
    elif condition == 'proposal_only':
        delivered, kind = plan['no_evidence_source'], 'none'
    else:
        raise ValueError(condition)
    seed = call['seed']; proposal_state = proposal = None
    if seed == 'actual':
        proposal_state, proposal = case['proposal_state'], case['proposal']
    elif seed != 'none':
        offset = {'correct': 0, 'wrong1': 1, 'wrong2': 2}[seed]
        proposal_state = STATES[(STATES.index(p['state']) + offset) % 3]
        proposal = plan['mapping'][proposal_state]
    template = plan['base_template']
    if kind == 'full':
        template = plan['full_prefix'] + template
    if proposal is not None:
        template = plan['proposal_prefix'].format(proposal=proposal) + template
    # Evaluation metadata goes into scoring only, never template expansion.
    evalcase = {'id': case['id'] + '__' + condition + '__' + seed,
                'source': delivered, 'state': p['state'], 'split': case['cohort']}
    return evalcase, {**plan, 'prompt_template': template}, {
        'case_id': case['id'], 'cohort': case['cohort'], 'condition': condition,
        'seed': seed, 'proposal_state': proposal_state, 'proposal_text': proposal,
        'evidence_kind': kind, 'delivered_source': delivered}

def main():
    plan = json.loads((ROOT / 'PLAN.json').read_text())
    cases = {c['id']: c for c in json.loads((ROOT / 'DATA.json').read_text())}
    calls = json.loads((ROOT / 'CALLS.json').read_text())
    freeze = json.loads((ROOT / 'FREEZE.json').read_text())
    assert all(sha(ROOT / n) == h for n, h in freeze['sha256'].items())
    assert all(sha(Path(n)) == h for n, h in freeze['dependencies'].items())
    out = ROOT / 'run'; out.mkdir()  # no overwrite, automatic retry or early accuracy gate
    runtime_readout.ROOT = ROOT
    from transformers import AutoTokenizer, AutoModelForCausalLM
    base = Path('/workspace/cache_backend_models/smollm2-135m')
    assert sha(base / 'model.safetensors') == plan['base_weights_sha256']
    torch.set_num_threads(2); torch.manual_seed(plan['seed'])
    tok = AutoTokenizer.from_pretrained(base, local_files_only=True, trust_remote_code=False)
    guard = Guard(plan['working_limit_bytes'], out / 'RESOURCE.jsonl')
    guard.read('before_load')
    model = AutoModelForCausalLM.from_pretrained(base, local_files_only=True, trust_remote_code=False,
            use_safetensors=True, torch_dtype=torch.float32, attn_implementation='eager')
    inject_lora(model, rank=4, alpha=8, dropout=0.)
    directory = ACQUISITION / 'run/canonical'
    manifest = json.loads((directory / 'MANIFEST.json').read_text())
    load_adapter(model, directory / 'final', base_pin=manifest['base_pin'])
    assert parameter_digest(model, True) == manifest['final_digest']
    assert parameter_digest(model, False) == manifest['base_digest_after']
    for i, call in enumerate(calls, 1):
        case = cases[call['case_id']]
        evalcase, guidance, metadata = material(case, call, plan)
        row = runtime_readout.evaluate(model, tok, [evalcase], plan['mapping'], guidance,
                                      'canonical', call['condition'] + '__' + call['seed'], guard)[0]
        append_json(out / 'CALL_METADATA.jsonl', {'readout_id': row['id'], **metadata})
        if i % 36 == 0:
            print(json.dumps({'completed': i, 'planned': len(calls)}), flush=True)
    assert all(sha(Path(n)) == h for n, h in freeze['dependencies'].items())
    assert parameter_digest(model, True) == manifest['final_digest']
    assert parameter_digest(model, False) == manifest['base_digest_after']
    assert sha(base / 'model.safetensors') == plan['base_weights_sha256']
    dump_new(out / 'RUN_MANIFEST.json', {'status': 'complete', 'generation_calls': len(calls),
        'choice_scoring_batch_calls': len(calls), 'choice_sequences': 3*len(calls),
        'optimizer_updates': 0, 'base_and_adapter_unchanged': True,
        'frozen_dependencies_unchanged': True, 'no_source_based_or_accuracy_gating': True,
        'raw_sha256': sha(out / 'RAW.jsonl')})

if __name__ == '__main__':
    main()
