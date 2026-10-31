"""Source-grounded transition scoring after all scheduled downstream movement."""
from pathlib import Path
from collections import Counter
import json
from evidence import parse, receipt, transition
from runtime_reference import dump_new, sha

ROOT = Path(__file__).resolve().parent

def summarize(joined):
    summary = {}
    for cohort in ('replay', 'fresh'):
        summary[cohort] = {}
        for condition, seed in sorted({(r['condition'], r['seed']) for r in joined if r['cohort'] == cohort}):
            rs = [r for r in joined if (r['cohort'], r['condition'], r['seed']) == (cohort, condition, seed)]
            seeded = [r for r in rs if r['proposal_state'] is not None]
            changes = Counter(transition(r['proposal_state'], r['free_state'], r['state']) for r in seeded)
            summary[cohort][condition + '__' + seed] = {'n': len(rs),
                'free_correct': sum(r['free_correct'] for r in rs),
                'sum_correct': sum(r['sum_correct'] for r in rs),
                'mean_correct': sum(r['mean_correct'] for r in rs),
                'invalid': sum(r['free_state'] is None for r in rs),
                'initial_correct': sum(r['proposal_state'] == r['state'] for r in seeded),
                'initial_wrong': sum(r['proposal_state'] != r['state'] for r in seeded),
                'transitions': dict(changes),
                'evidence_receipts': dict(Counter(r['receipt']['evidence'] for r in rs)),
                'eligible_after_source_receipt': sum(r['receipt']['eligible_for_this_toy_acceptance'] for r in rs),
                'unique_prompts': len({r['messages'][0]['content'] for r in rs}),
                'readout_and_choice_seconds': sum(r['seconds'] for r in rs),
                'input_tokens': sum(len(r['input_token_ids']) for r in rs),
                'generated_tokens': sum(len(r['generated_token_ids']) for r in rs),
                'by_state': {s: {'n': sum(r['state'] == s for r in rs),
                    'free_correct': sum(r['state'] == s and r['free_correct'] for r in rs)}
                    for s in ('positive', 'zero', 'missing')}}
    return summary

def main():
    cases = {c['id']: c for c in json.loads((ROOT / 'DATA.json').read_text())}
    rows = [json.loads(s) for s in (ROOT / 'run/RAW.jsonl').read_text().splitlines()]
    meta = {r['readout_id']: r for r in (json.loads(s) for s in (ROOT / 'run/CALL_METADATA.jsonl').read_text().splitlines())}
    assert len(rows) == len(meta) == 360
    joined = []
    for row in rows:
        m = meta[row['id']]; case = cases[m['case_id']]
        assert row['state'] == case['state'] == parse(case['source'])['state']
        joined.append({**row, **m, 'receipt': receipt(case['source'], m['delivered_source'], m['evidence_kind'], row['free_state'])})
    summary = summarize(joined)
    dump_new(ROOT / 'run/SUMMARY.json', summary)
    # A mechanical pass-through is an explicit reference, not new model evidence.
    dump_new(ROOT / 'run/PASS_THROUGH_REFERENCE.json', {'replay': {'n': 36, 'correct': 23, 'wrong': 13},
        'fresh_correct_seed': {'n': 12, 'correct': 12}, 'fresh_wrong1_seed': {'n': 12, 'correct': 0},
        'fresh_wrong2_seed': {'n': 12, 'correct': 0}, 'model_calls': 0})
    dump_new(ROOT / 'SCORING_RECEIPT.json', {'raw_sha256': sha(ROOT / 'run/RAW.jsonl'),
        'metadata_sha256': sha(ROOT / 'run/CALL_METADATA.jsonl'), 'rows': len(rows),
        'reference_is_source_grammar_not_external_world_truth': True,
        'receipt_did_not_gate_or_mutate_model_calls': True})
    print(json.dumps(summary, indent=2))

if __name__ == '__main__':
    main()
