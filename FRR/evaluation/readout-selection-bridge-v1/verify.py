"""Post-run source/prompt/metric/serialization audit, not independent replication."""
from pathlib import Path
from collections import Counter
import json

from bridge import parse, score
from runtime_reference import sha

ROOT = Path(__file__).resolve().parent

def main():
    from transformers import AutoTokenizer
    from runtime_readout import prompt
    data = json.loads((ROOT / 'DATA.json').read_text())
    plan = json.loads((ROOT / 'PLAN.json').read_text())
    fullplan = {**plan, 'prompt_template': 'Read only the record for the target plot.\n' + plan['prompt_template']}
    freeze = json.loads((ROOT / 'FREEZE.json').read_text())
    assert all(sha(ROOT / n) == h for n, h in freeze['sha256'].items())
    assert all(sha(Path(n)) == h for paths in freeze['acquisition_checkpoints'].values() for n, h in paths.items())
    tok = AutoTokenizer.from_pretrained('/workspace/cache_backend_models/smollm2-135m', local_files_only=True, trust_remote_code=False)
    byid = {c['id']: c for c in data}
    assert len(data) == 36 and len(byid) == 36
    assert Counter(c['state'] for c in data) == Counter(dict.fromkeys(('positive', 'zero', 'missing'), 12))
    assert len({c['source'] for c in data}) == 36
    assert len({parse(c['source'])['crop'] for c in data}) == 6
    bodypairs = {}
    first = last = 0
    for c in data:
        p = parse(c['source']); assert p['state'] == c['state']
        assert p['state'] == dict(p['records'])[p['target']]
        first += p['records'][0][1] == p['state']; last += p['records'][1][1] == p['state']
        bodypairs.setdefault(c['pair_id'], []).append(c)
    assert first == last == 24
    assert len(bodypairs) == 18 and sum(g[0]['discordant'] for g in bodypairs.values()) == 12
    for group in bodypairs.values():
        assert len(group) == 2
        assert group[0]['source'].split('\n', 1)[1] == group[1]['source'].split('\n', 1)[1]
        assert group[0]['discordant'] == (group[0]['state'] != group[1]['state'])
    rows = [json.loads(s) for s in (ROOT / 'run/RAW.jsonl').read_text().splitlines()]
    assert len(rows) == 288
    assert {(r['arm'], r['phase'], r['id']) for r in rows} == {(a, p, c) for a in plan['mappings'] for p in ('full', 'cropped') for c in byid}
    joined = []
    for r in rows:
        c = byid[r['id']]; m = plan['mappings'][r['arm']]
        source = c['source'] if r['phase'] == 'full' else parse(c['source'])['crop']
        guide = fullplan if r['phase'] == 'full' else plan
        assert r['messages'] == [{'role': 'user', 'content': prompt({'source': source}, m, guide)}]
        assert r['input_token_ids'] == tok.apply_chat_template(r['messages'], tokenize=True, add_generation_prompt=True)
        assert r['text'] == tok.decode(r['generated_token_ids'], skip_special_tokens=True)
        assert r['state'] == c['state'] and r['split'] == c['split']
        assert r['free_state'] == {v: k for k, v in m.items()}.get(r['text'].strip())
        assert r['free_correct'] == (r['free_state'] == c['state'])
        assert not r['sum_tied'] and not r['mean_tied']
        choices = r['choice_scores']
        for state, label in m.items():
            s = choices[state]
            assert s['label'] == label
            assert s['ids_including_eos'] == tok.encode(label, add_special_tokens=False) + [tok.eos_token_id]
            assert s['sum'] == sum(s['token_logprobs'])
            assert s['mean'] == s['sum'] / len(s['token_logprobs'])
        assert r['sum_state'] == max(choices, key=lambda s: choices[s]['sum'])
        assert r['mean_state'] == max(choices, key=lambda s: choices[s]['mean'])
        assert r['sum_correct'] == (r['sum_state'] == c['state'])
        assert r['mean_correct'] == (r['mean_state'] == c['state'])
        joined.append({**r, 'pair_id': c['pair_id'], 'discordant': c['discordant']})
    assert score(joined) == json.loads((ROOT / 'run/SUMMARY.json').read_text())
    resources = [json.loads(s) for s in (ROOT / 'run/RESOURCE.jsonl').read_text().splitlines()]
    receipt = {'status': 'pass', 'rows_audited': 288, 'source_header_pairs': 18, 'discordant_pairs': 12,
        'full_unique_sources': 36, 'unique_crops': 6, 'frozen_inputs_and_acquisition_checkpoints_unchanged': True,
        'baseline_always_first_correct': first, 'baseline_always_last_correct': last,
        'prompt_tokenization_decode_choice_metric_checks': True,
        'max_sampled_working_bytes': max(p['working_estimate'] for p in resources),
        'max_sampled_rss_bytes': max(p['process_rss'] for p in resources),
        'generation_input_tokens': sum(len(r['input_token_ids']) for r in rows),
        'generation_output_tokens_including_eos': sum(len(r['generated_token_ids']) for r in rows),
        'generation_and_choice_score_seconds': sum(r['seconds'] for r in rows),
        'max_input_tokens': max(len(r['input_token_ids']) for r in rows),
        'raw_sha256': sha(ROOT / 'run/RAW.jsonl'), 'no_independent_empirical_replication': True}
    with (ROOT / 'CHECKS.json').open('x') as f:
        json.dump(receipt, f, indent=2, sort_keys=True); f.write('\n')
    print(json.dumps(receipt, indent=2))

if __name__ == '__main__':
    main()
