"""Audit source/prompt/transition/provenance records without new model forwards."""
from pathlib import Path
from collections import Counter
import json
import re

ROOT = Path(__file__).resolve().parent

def main():
    from transformers import AutoTokenizer
    from evidence import receipt, parse, transition
    from run_room import material
    from runtime_readout import prompt
    from runtime_reference import sha, dump_new
    from score import summarize
    plan = json.loads((ROOT / 'PLAN.json').read_text())
    cases = {c['id']: c for c in json.loads((ROOT / 'DATA.json').read_text())}
    calls = json.loads((ROOT / 'CALLS.json').read_text())
    freeze = json.loads((ROOT / 'FREEZE.json').read_text())
    assert all(sha(ROOT / n) == h for n, h in freeze['sha256'].items())
    assert all(sha(Path(n)) == h for n, h in freeze['dependencies'].items())
    tok = AutoTokenizer.from_pretrained('/workspace/cache_backend_models/smollm2-135m', local_files_only=True, trust_remote_code=False)
    rows = [json.loads(s) for s in (ROOT / 'run/RAW.jsonl').read_text().splitlines()]
    metadata = [json.loads(s) for s in (ROOT / 'run/CALL_METADATA.jsonl').read_text().splitlines()]
    assert len(rows) == len(metadata) == len(calls) == 360
    assert len({r['id'] for r in rows}) == 360
    joined = []
    for call, row, meta in zip(calls, rows, metadata):
        c = cases[call['case_id']]
        # Alternative source reading: explicit lines to target-name lookup.
        lines = c['source'].splitlines()
        target = lines[0].removeprefix('Target plot: ')
        records = [(lines[i].removeprefix('Plot: '), lines[i+1].removeprefix('Status: '))
                   for i in range(len(lines)-1) if lines[i].startswith('Plot: ')]
        assert len(records) == len(dict(records)) == 2
        truth = dict(records)[target]
        assert truth == c['state'] == row['state']
        ec, guidance, expected_metadata = material(c, call, plan)
        assert row['id'] == ec['id'] == meta['readout_id']
        assert meta == {'readout_id': row['id'], **expected_metadata}
        assert row['messages'] == [{'role': 'user', 'content': prompt(ec, plan['mapping'], guidance)}]
        assert row['input_token_ids'] == tok.apply_chat_template(row['messages'], tokenize=True, add_generation_prompt=True)
        assert row['text'] == tok.decode(row['generated_token_ids'], skip_special_tokens=True)
        assert row['free_state'] == {v: k for k, v in plan['mapping'].items()}.get(row['text'].strip())
        assert row['free_correct'] == (row['free_state'] == truth)
        assert row['split'] == c['cohort']
        scores = row['choice_scores']; assert set(scores) == set(plan['mapping'])
        for state, label in plan['mapping'].items():
            s = scores[state]
            assert s['label'] == label
            assert s['ids_including_eos'] == tok.encode(label, add_special_tokens=False) + [tok.eos_token_id]
            assert len(s['ids_including_eos']) == len(s['token_logprobs'])
            assert s['sum'] == sum(s['token_logprobs'])
            assert s['mean'] == s['sum']/len(s['token_logprobs'])
            assert all(v <= 0 for v in s['token_logprobs'])
        choice_sum = max(plan['mapping'], key=lambda s: scores[s]['sum'])
        choice_mean = max(plan['mapping'], key=lambda s: scores[s]['mean'])
        assert row['sum_state'] == choice_sum and row['mean_state'] == choice_mean
        assert row['sum_correct'] == (choice_sum == truth) and row['mean_correct'] == (choice_mean == truth)
        assert row['sum_tied'] == (sum(s['sum'] == scores[choice_sum]['sum'] for s in scores.values()) > 1)
        assert row['mean_tied'] == (sum(s['mean'] == scores[choice_mean]['mean'] for s in scores.values()) > 1)
        joined.append({**row, **meta, 'receipt': receipt(c['source'], meta['delivered_source'], meta['evidence_kind'], row['free_state'])})
    summary = summarize(joined)
    assert summary == json.loads((ROOT / 'run/SUMMARY.json').read_text())
    for groups in summary.values():
        for s in groups.values():
            t = s['transitions']
            if t:
                assert sum(t.values()) == s['n']
                repaired = t.get('wrong_to_correct', 0)
                harmed = t.get('correct_to_wrong', 0) + t.get('correct_to_invalid', 0)
                assert s['free_correct'] == s['initial_correct'] + repaired - harmed
    fresh = [c for c in cases.values() if c['cohort'] == 'fresh']
    assert len(fresh) == len({c['source'] for c in fresh}) == 12
    assert Counter(c['state'] for c in fresh) == Counter(dict.fromkeys(('positive', 'zero', 'missing'), 4))
    for condition in ('proposal_only', 'reopen_full', 'reopen_selected'):
        for seed in ('correct', 'wrong1', 'wrong2'):
            rs = [r for r in joined if r['cohort'] == 'fresh' and r['condition'] == condition and r['seed'] == seed]
            assert Counter(r['proposal_state'] for r in rs) == Counter(dict.fromkeys(('positive', 'zero', 'missing'), 4))
    oldrows = [json.loads(s) for s in (ROOT.parent / 'readout-selection-bridge-v1/run/RAW.jsonl').read_text().splitlines()]
    mismatches = []
    for condition, oldphase in [('baseline_full', 'full'), ('baseline_selected', 'cropped')]:
        originals = {r['id']: r for r in oldrows if r['arm'] == 'canonical' and r['phase'] == oldphase}
        for r in joined:
            if r['cohort'] != 'replay' or r['condition'] != condition:
                continue
            old = originals[cases[r['case_id']]['upstream_record_id']]
            if old['input_token_ids'] != r['input_token_ids'] or old['generated_token_ids'] != r['generated_token_ids']:
                mismatches.append({'id': r['id'], 'condition': condition, 'old_output': old['text'], 'new_output': r['text']})
    previous = json.loads(Path('/workspace/downstream-room-before.json').read_text())
    assert all(sha(Path('/workspace/frr') / n) == h for n, h in previous.items())
    resource = [json.loads(s) for s in (ROOT / 'run/RESOURCE.jsonl').read_text().splitlines()]
    checks = {'status': 'pass', 'rows_audited': len(rows),
        'all_scheduled_calls_executed_before_evidence_receipts': True,
        'frozen_inputs_and_dependencies_match': True, 'source_prompt_token_decode_choice_transition_checks': True,
        'prior_local_files_unchanged_before_sync': len(previous),
        'exact_replay_baseline_comparisons': 72, 'replay_baseline_mismatches': mismatches,
        'generation_input_tokens': sum(len(r['input_token_ids']) for r in rows),
        'generation_output_tokens_including_eos': sum(len(r['generated_token_ids']) for r in rows),
        'readout_and_choice_seconds': sum(r['seconds'] for r in rows),
        'unique_prompts': len({r['messages'][0]['content'] for r in rows}),
        'max_input_tokens': max(len(r['input_token_ids']) for r in rows),
        'max_sampled_working_bytes': max(p['working_estimate'] for p in resource),
        'max_sampled_rss_bytes': max(p['process_rss'] for p in resource),
        'raw_sha256': sha(ROOT / 'run/RAW.jsonl'), 'no_independent_empirical_replication': True,
        'no_model_error_awareness_or_calibrated_abstention_measured': True}
    dump_new(ROOT / 'CHECKS.json', checks)
    print(json.dumps(checks, indent=2))

if __name__ == '__main__':
    main()
