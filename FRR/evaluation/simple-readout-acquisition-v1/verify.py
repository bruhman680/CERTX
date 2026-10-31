"""Post-run artifact audit, separately retained from frozen experimental code."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    import torch
    from transformers import AutoTokenizer
    from safetensors.torch import load_file
    from run import prompt, summarize_rows
    plan = json.loads((ROOT / 'PLAN.json').read_text())
    cases = {c['id']: c for c in json.loads((ROOT / 'DATA.json').read_text())}
    rows = [json.loads(line) for line in (ROOT / 'run/RAW.jsonl').read_text().splitlines()]
    freeze = json.loads((ROOT / 'FREEZE.json').read_text())
    assert all(sha(ROOT / n) == h for n, h in freeze['sha256'].items())
    tok = AutoTokenizer.from_pretrained('/workspace/cache_backend_models/smollm2-135m', local_files_only=True, trust_remote_code=False)
    assert len(rows) == 192
    expected = {(a, p, cid) for a in plan['mappings'] for p in ('base', 'trained') for cid in cases}
    assert {(r['arm'], r['phase'], r['id']) for r in rows} == expected
    assert len(expected) == len(rows)
    for row in rows:
        case = cases[row['id']]; mapping = plan['mappings'][row['arm']]
        # Parse the actual source, rather than trusting the authored state key.
        state = re.fullmatch(r'Plot: [A-Za-z]+\nStatus: (positive|zero|missing)', case['source']).group(1)
        assert state == case['state'] == row['state']
        assert row['split'] == case['split']
        assert row['messages'] == [{'role': 'user', 'content': prompt(case, mapping, plan)}]
        assert row['input_token_ids'] == tok.apply_chat_template(row['messages'], tokenize=True, add_generation_prompt=True)
        assert row['text'] == tok.decode(row['generated_token_ids'], skip_special_tokens=True)
        rev = {v: k for k, v in mapping.items()}
        assert row['free_state'] == rev.get(row['text'].strip())
        assert row['free_correct'] == (row['free_state'] == state)
        scores = row['choice_scores']
        assert set(scores) == set(mapping)
        for s, score in scores.items():
            assert score['label'] == mapping[s]
            assert score['ids_including_eos'] == tok.encode(mapping[s], add_special_tokens=False) + [tok.eos_token_id]
            assert len(score['token_logprobs']) == len(score['ids_including_eos'])
            assert score['sum'] == sum(score['token_logprobs'])
            assert score['mean'] == score['sum']/len(score['token_logprobs'])
            assert all(v <= 0 for v in score['token_logprobs'])
        # JSON serialization sorts keys; scores tied at exact float precision would
        # need replay with the original mapping order. In this contact check no ties.
        assert row['sum_tied'] is False and row['mean_tied'] is False
        assert row['sum_state'] == max(scores, key=lambda s: scores[s]['sum'])
        assert row['mean_state'] == max(scores, key=lambda s: scores[s]['mean'])
        assert row['sum_correct'] == (row['sum_state'] == state)
        assert row['mean_correct'] == (row['mean_state'] == state)
        assert row['first_token_correct'] == (row['generated_token_ids'][0] == scores[state]['ids_including_eos'][0])
    assert summarize_rows(rows) == json.loads((ROOT / 'run/SUMMARY.json').read_text())
    initials = []
    for arm in plan['mappings']:
        directory = ROOT / 'run' / arm
        manifest = json.loads((directory / 'MANIFEST.json').read_text())
        assert manifest['completed_updates'] == 48
        assert manifest['base_digest_before'] == manifest['base_digest_after']
        assert all(sha(directory / n) == h for n, h in manifest['binary_sha256'].items())
        logs = [json.loads(s) for s in (directory / 'TRAINING.jsonl').read_text().splitlines()]
        assert len(logs) == 48
        assert Counter(m['state'] for log in logs for m in log['micro']) == Counter(dict.fromkeys(('positive', 'zero', 'missing'), 48))
        assert [[m['id'] for m in log['micro']] for log in logs] == plan['order']
        initial = load_file(str(directory / 'initial/adapter.safetensors'))
        final = load_file(str(directory / 'final/adapter.safetensors'))
        assert initial.keys() == final.keys()
        assert all(torch.isfinite(t).all() for t in final.values())
        assert all(torch.count_nonzero(v) == 0 for n, v in initial.items() if n.endswith('lora_B'))
        assert any(not torch.equal(initial[n], final[n]) for n in initial)
        initials.append(initial)
    assert all(all(torch.equal(init[n], initials[0][n]) for n in init) for init in initials)
    old = json.loads(Path('/workspace/simple-readout-before.json').read_text())
    assert all(sha(Path('/workspace/frr') / n) == h for n, h in old.items())
    resources = [json.loads(s) for s in (ROOT / 'run/RESOURCE.jsonl').read_text().splitlines()]
    receipt = {'status': 'pass', 'rows_audited': len(rows), 'earlier_local_files_unchanged_before_sync': len(old),
        'frozen_inputs_match': True, 'source_states_reparsed': True, 'prompts_tokenization_decodes_checked': True,
        'initial_adapter_tensors_equal': True, 'all_four_frozen_bases_unchanged': True,
        'all_binary_hashes_and_adapter_finiteness_checked': True, 'scoring_recomputed': True,
        'optimizer_pickle_not_loaded': True, 'no_independent_empirical_replication': True,
        'resource_phase_samples': len(resources),
        'max_sampled_working_bytes': max(r['working_estimate'] for r in resources),
        'max_sampled_rss_bytes': max(r['process_rss'] for r in resources),
        'generation_input_tokens': sum(len(r['input_token_ids']) for r in rows),
        'generation_output_tokens_including_eos': sum(len(r['generated_token_ids']) for r in rows),
        'generation_and_choice_score_seconds': sum(r['seconds'] for r in rows),
        'raw_sha256': sha(ROOT / 'run/RAW.jsonl')}
    with (ROOT / 'CHECKS.json').open('x') as f:
        json.dump(receipt, f, indent=2, sort_keys=True); f.write('\n')
    print(json.dumps(receipt, indent=2))

if __name__ == '__main__':
    main()
