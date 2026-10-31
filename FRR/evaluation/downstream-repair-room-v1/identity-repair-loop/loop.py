"""One later-stage identity repair, preserving the actual wrong-selection output."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))
import torch
import runtime_readout
from runtime_reference import sha, dump_new, append_json, Guard, parameter_digest
from run_room import material
from evidence import parse, receipt, transition
from lora_cpu import inject_lora, load_adapter

def prepare():
    parent = ROOT.parent
    assert json.loads((parent / 'CHECKS.json').read_text())['status'] == 'pass'
    cases = {c['id']: c for c in json.loads((parent / 'DATA.json').read_text())}
    rows = {r['id']: r for r in (json.loads(s) for s in (parent / 'run/RAW.jsonl').read_text().splitlines())}
    metadata = [json.loads(s) for s in (parent / 'run/CALL_METADATA.jsonl').read_text().splitlines()]
    inputs = []
    for m in metadata:
        if m['condition'] != 'wrong_selection':
            continue
        c, bad = cases[m['case_id']], rows[m['readout_id']]
        audit = receipt(c['source'], m['delivered_source'], m['evidence_kind'], bad['free_state'])
        # The trigger is record identity, including lucky correct labels.
        assert audit['evidence'] == 'TARGET_MISMATCH'
        inputs.append({'original_case_id': c['id'], 'upstream_readout_id': bad['id'],
            'prior_receipt': audit, 'case': {**c, 'id': c['id'] + '__after_identity_receipt',
                'proposal_state': bad['free_state'], 'proposal': bad['text'].strip()}})
    assert len(inputs) == 48
    dump_new(ROOT / 'INPUTS.json', inputs)
    plan = json.loads((parent / 'PLAN.json').read_text())
    dump_new(ROOT / 'PLAN.json', plan)
    acq = parent.parent / 'simple-readout-acquisition-v1/run/canonical'
    dependencies = [parent / n for n in ('DATA.json', 'PLAN.json', 'CHECKS.json', 'run/RAW.jsonl',
                    'run/CALL_METADATA.jsonl', 'run_room.py', 'evidence.py', 'runtime_readout.py',
                    'runtime_reference.py', 'lora_cpu.py')]
    dependencies += [acq / n for n in ('MANIFEST.json', 'final/adapter.safetensors', 'final/manifest.json')]
    dump_new(ROOT / 'FREEZE.json', {'sha256': {n: sha(ROOT / n) for n in ('loop.py', 'PROTOCOL.md', 'INPUTS.json', 'PLAN.json')},
        'dependencies': {str(p): sha(p) for p in dependencies},
        'timing': 'after complete360-call contact and its audit; before all48loop forwards',
        'selection': 'all deliberate wrong-selection handoffs; identity trigger, not semantic correctness'})

def run():
    from transformers import AutoTokenizer, AutoModelForCausalLM
    freeze = json.loads((ROOT / 'FREEZE.json').read_text())
    assert all(sha(ROOT / n) == h for n, h in freeze['sha256'].items())
    assert all(sha(Path(n)) == h for n, h in freeze['dependencies'].items())
    plan = json.loads((ROOT / 'PLAN.json').read_text())
    inputs = json.loads((ROOT / 'INPUTS.json').read_text())
    out = ROOT / 'run'; out.mkdir()
    runtime_readout.ROOT = ROOT
    guard = Guard(plan['working_limit_bytes'], out / 'RESOURCE.jsonl')
    base = Path('/workspace/cache_backend_models/smollm2-135m')
    assert sha(base / 'model.safetensors') == plan['base_weights_sha256']
    torch.set_num_threads(2); torch.manual_seed(plan['seed'])
    tok = AutoTokenizer.from_pretrained(base, local_files_only=True, trust_remote_code=False)
    guard.read('before_load')
    model = AutoModelForCausalLM.from_pretrained(base, local_files_only=True, trust_remote_code=False,
        use_safetensors=True, torch_dtype=torch.float32, attn_implementation='eager')
    inject_lora(model, rank=4, alpha=8, dropout=0.)
    acq = ROOT.parent.parent / 'simple-readout-acquisition-v1/run/canonical'
    manifest = json.loads((acq / 'MANIFEST.json').read_text())
    load_adapter(model, acq / 'final', base_pin=manifest['base_pin'])
    assert parameter_digest(model, True) == manifest['final_digest']
    rows = []
    for item in inputs:
        case = item['case']
        call = {'case_id': case['id'], 'condition': 'reopen_selected', 'seed': 'actual'}
        ec, guidance, meta = material(case, call, plan)
        # One invocation after the identity receipt. No label-based retry.
        row = runtime_readout.evaluate(model, tok, [ec], plan['mapping'], guidance,
                                      'canonical', 'after_identity_receipt', guard)[0]
        source_receipt = receipt(case['source'], meta['delivered_source'], meta['evidence_kind'], row['free_state'])
        append_json(out / 'RECEIPTS.jsonl', {'id': row['id'], 'original_case_id': item['original_case_id'],
             'upstream_readout_id': item['upstream_readout_id'], 'initial_state': case['proposal_state'],
             'receipt': source_receipt, 'transition': transition(case['proposal_state'], row['free_state'], parse(case['source'])['state'])})
        rows.append(row)
    assert len(rows) == 48
    assert all(sha(Path(n)) == h for n, h in freeze['dependencies'].items())
    assert parameter_digest(model, True) == manifest['final_digest']
    assert parameter_digest(model, False) == manifest['base_digest_after']
    records = [json.loads(s) for s in (out / 'RECEIPTS.jsonl').read_text().splitlines()]
    from collections import Counter
    summary = {'n': 48, 'initial_correct': sum(i['case']['proposal_state'] == parse(i['case']['source'])['state'] for i in inputs),
        'final_correct': sum(r['free_correct'] for r in rows), 'invalid': sum(r['free_state'] is None for r in rows),
        'final_eligible': sum(r['receipt']['eligible_for_this_toy_acceptance'] for r in records),
        'transitions': dict(Counter(r['transition'] for r in records)),
        'prior_target_mismatches': 48, 'optimizer_updates': 0}
    dump_new(out / 'SUMMARY.json', summary)
    # Audit every prompt/token/label/source receipt without another model call.
    for item, row, record in zip(inputs, rows, records):
        case = item['case']
        ec, guidance, m = material(case, {'condition': 'reopen_selected', 'seed': 'actual'}, plan)
        assert row['messages'] == [{'role': 'user', 'content': runtime_readout.prompt(ec, plan['mapping'], guidance)}]
        assert row['input_token_ids'] == tok.apply_chat_template(row['messages'], tokenize=True, add_generation_prompt=True)
        assert row['text'] == tok.decode(row['generated_token_ids'], skip_special_tokens=True)
        assert row['free_state'] == {v: k for k, v in plan['mapping'].items()}.get(row['text'].strip())
        assert row['free_correct'] == (row['free_state'] == parse(case['source'])['state'])
        assert record['receipt'] == receipt(case['source'], m['delivered_source'], m['evidence_kind'], row['free_state'])
        for state, label in plan['mapping'].items():
            s = row['choice_scores'][state]
            assert s['ids_including_eos'] == tok.encode(label, add_special_tokens=False) + [tok.eos_token_id]
            assert s['sum'] == sum(s['token_logprobs'])
            assert s['mean'] == s['sum']/len(s['token_logprobs'])
    resource = [json.loads(s) for s in (out / 'RESOURCE.jsonl').read_text().splitlines()]
    checks = {'status': 'pass', 'rows_audited': 48, 'base_adapter_prior_records_unchanged': True,
        'generation_input_tokens': sum(len(r['input_token_ids']) for r in rows),
        'generation_output_tokens_including_eos': sum(len(r['generated_token_ids']) for r in rows),
        'readout_and_choice_seconds': sum(r['seconds'] for r in rows),
        'max_sampled_working_bytes': max(p['working_estimate'] for p in resource),
        'max_sampled_rss_bytes': max(p['process_rss'] for p in resource),
        'raw_sha256': sha(out / 'RAW.jsonl'), 'no_independent_replication_or_model_initiated_retrieval': True}
    dump_new(ROOT / 'CHECKS.json', checks)
    dump_new(out / 'RUN_MANIFEST.json', {'status': 'complete', 'generation_calls': 48,
        'choice_scoring_batch_calls': 48, 'choice_sequences': 144, 'optimizer_updates': 0,
        'original_wrong_selection_rows_retained': True})
    print(json.dumps(summary, indent=2))

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(); p.add_argument('stage', choices=['prepare', 'run']); a = p.parse_args()
    prepare() if a.stage == 'prepare' else run()
