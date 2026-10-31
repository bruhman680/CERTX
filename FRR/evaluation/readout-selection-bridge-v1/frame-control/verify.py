"""Audit the separately frozen post-result frame contact without model forwards."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))
from runtime_reference import sha

def main():
    from transformers import AutoTokenizer
    from runtime_readout import prompt
    data = json.loads((ROOT / 'DATA.json').read_text())
    plan = json.loads((ROOT / 'PLAN.json').read_text())
    freeze = json.loads((ROOT / 'FREEZE.json').read_text())
    assert all(sha(ROOT / n) == h for n, h in freeze['sha256'].items())
    assert all(sha(Path(n)) == h for n, h in freeze['dependencies'].items())
    cases = {c['id']: c for c in data}
    assert len(cases) == 12 and len({c['source'] for c in data}) == 12
    for c in data:
        m = re.fullmatch(r'Target plot: (Oak|Beech)\n\nRecord ([12]):\nPlot: (Oak|Beech)\nStatus: (positive|zero|missing)', c['source'])
        assert m and m[1] == m[3] and m[4] == c['state']
    rows = [json.loads(s) for s in (ROOT / 'run/RAW.jsonl').read_text().splitlines()]
    assert len(rows) == 48 and {(r['arm'], r['id']) for r in rows} == {(a, c) for a in plan['mappings'] for c in cases}
    tok = AutoTokenizer.from_pretrained('/workspace/cache_backend_models/smollm2-135m', local_files_only=True, trust_remote_code=False)
    for r in rows:
        c, mapping = cases[r['id']], plan['mappings'][r['arm']]
        assert r['messages'] == [{'role': 'user', 'content': prompt(c, mapping, plan)}]
        assert r['input_token_ids'] == tok.apply_chat_template(r['messages'], tokenize=True, add_generation_prompt=True)
        assert r['text'] == tok.decode(r['generated_token_ids'], skip_special_tokens=True)
        assert r['state'] == c['state']
        assert r['free_state'] == {v: k for k, v in mapping.items()}.get(r['text'].strip())
        assert r['free_correct'] == (r['free_state'] == c['state'])
        assert not r['sum_tied'] and not r['mean_tied']
        scores = r['choice_scores']
        for state, label in mapping.items():
            s = scores[state]
            assert s['ids_including_eos'] == tok.encode(label, add_special_tokens=False) + [tok.eos_token_id]
            assert s['label'] == label and s['sum'] == sum(s['token_logprobs'])
            assert s['mean'] == s['sum']/len(s['token_logprobs'])
        assert r['sum_correct'] == (max(scores, key=lambda s: scores[s]['sum']) == c['state'])
        assert r['mean_correct'] == (max(scores, key=lambda s: scores[s]['mean']) == c['state'])
    summary = json.loads((ROOT / 'run/SUMMARY.json').read_text())
    for arm, s in summary.items():
        rs = [r for r in rows if r['arm'] == arm]
        assert s['n'] == len(rs) == 12
        assert s['free_correct'] == sum(r['free_correct'] for r in rs)
        assert s['sum_correct'] == sum(r['sum_correct'] for r in rs)
        assert s['unresolved'] == sum(r['free_state'] is None for r in rs)
        for state, item in s['by_state'].items():
            assert item['n'] == sum(r['state'] == state for r in rs) == 4
            assert item['free_correct'] == sum(r['state'] == state and r['free_correct'] for r in rs)
    resources = [json.loads(s) for s in (ROOT / 'run/RESOURCE.jsonl').read_text().splitlines()]
    receipt = {'status': 'pass', 'rows_audited': 48, 'unique_sources': 12,
        'frozen_dependencies_unchanged': True, 'prompt_decode_source_metric_checks': True,
        'max_sampled_working_bytes': max(p['working_estimate'] for p in resources),
        'max_sampled_rss_bytes': max(p['process_rss'] for p in resources),
        'generation_input_tokens': sum(len(r['input_token_ids']) for r in rows),
        'generation_output_tokens_including_eos': sum(len(r['generated_token_ids']) for r in rows),
        'generation_and_choice_score_seconds': sum(r['seconds'] for r in rows),
        'raw_sha256': sha(ROOT / 'run/RAW.jsonl')}
    with (ROOT / 'CHECKS.json').open('x') as f:
        json.dump(receipt, f, indent=2, sort_keys=True); f.write('\n')
    print(json.dumps(receipt, indent=2))

if __name__ == '__main__':
    main()
