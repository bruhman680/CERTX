"""Stored-record and independent reconstruction checks; no model generation."""
from pathlib import Path
import hashlib
import json
import sys
import tempfile

R = Path(__file__).resolve().parent
P = R.parent / 'computational-world-portability-v1'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    sys.path.insert(0, str(P / 'prototype'))
    from world_store import World
    from world_bundle import import_world
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained('/workspace/cache_backend_models/smollm2-135m', local_files_only=True, trust_remote_code=False)
    profile = json.loads((P / 'constants.json').read_text())
    plan = json.loads((R / 'PLAN.json').read_text())
    adaptive = json.loads((R / 'example_probe/PLAN.json').read_text())
    for source in (plan, adaptive):
        assert all(sha(path) == value for path, value in source['model_file_pins'].items())
        assert all(sha(path) == value for path, value in source['code_pins'].items())
    rows = []
    with tempfile.TemporaryDirectory(prefix='scheme-calibration-verify-') as directory:
        for folder in (R, R / 'example_probe'):
            current_plan = plan if folder == R else adaptive
            for path in sorted((folder / 'receipts').glob('*.json')):
                result = json.loads(path.read_text()); trial = result['trial']; identity = trial['id']
                generation = json.loads((folder / 'generations' / (identity + '.json')).read_text())
                start = json.loads((folder / 'starts' / (identity + '.json')).read_text())
                assert start['plan_sha256'] == sha(folder / 'PLAN.json')
                ids = tok.apply_chat_template([{'role': 'user', 'content': trial['prompt']}], tokenize=True, add_generation_prompt=True)
                assert ids == trial['input_token_ids'] == generation['input_token_ids']
                assert generation['prompt'] == trial['prompt'] and generation['rng_seed'] == trial['seed']
                assert generation['text'] == tok.decode(generation['generated_token_ids'], skip_special_tokens=True)
                assert generation['temperature'] == .8 and generation['top_p'] == .9
                assert 1 <= len(generation['generated_token_ids']) <= 96
                if generation['stop'] == 'eos': assert generation['generated_token_ids'][-1] == tok.eos_token_id
                else: assert generation['stop'] == 'token_limit' and len(generation['generated_token_ids']) == 96
                text = generation['text'].strip()
                if trial.get('block') == 'plain':
                    assert result['receipt'] is None and result['accepted_action'] is None
                    assert result['literal_match'] == (text == trial['target']) == result['task_success']
                    rebuilt = False
                else:
                    db = Path(directory) / ((folder.name + '-' + identity) + '.sqlite')
                    import_world(folder / 'final_bundles' / (identity + '.json'), db, profile)
                    world = World(db, profile)
                    try:
                        assert world.submit('model-' + identity, trial['snapshot'], text) == result['receipt']
                        receipt = result['receipt']
                        accepted = receipt.get('error') is None and receipt['status'] in ('COMPUTED', 'PUBLISHED', 'OBSERVED', 'ALIAS_DROPPED')
                        assert accepted == result['accepted_action']
                        if trial.get('case') == 'definition':
                            probe = result['host_probes'][0]
                            success = receipt['status'] == 'PUBLISHED' and probe['status'] == 'COMPUTED' and type(probe['value']) is int and probe['value'] == 6
                        elif trial.get('case') == 'page':
                            # None was accepted; the permissive original page score has no effect.
                            assert not accepted
                            success = False
                        else:
                            value = trial.get('expected_value', 3 if trial.get('case') == 'literal' else 5)
                            success = receipt['status'] == 'COMPUTED' and type(receipt.get('value')) is int and receipt['value'] == value
                        assert success == result['task_success']
                        if 'target' in trial: assert result['literal_match'] == (text == trial['target'])
                        world.verify_integrity()
                    finally:
                        world.close()
                    rebuilt = True
                rows.append({'id': identity, 'record_verified': True, 'world_rebuilt': rebuilt})
    main_rows = [json.loads(p.read_text()) for p in (R / 'receipts').glob('*.json')]
    by_id = {x['id']: x for x in main_rows}
    reference_pairs = 0
    for row in main_rows:
        t = row['trial']
        if t['variant'] != 'scale_zero': continue
        normal = by_id[t['id'].replace('scale_zero_', 'normal_', 1)]['trial']
        assert t['prompt'] == normal['prompt'] and t['input_token_ids'] == normal['input_token_ids'] and t['seed'] == normal['seed']
        reference_pairs += 1
    feedback_pairs = 0
    for path in (R / 'feedback_plans').glob('*.json'):
        feedback = json.loads(path.read_text()); left, right = feedback['pair']
        assert left['seed'] == right['seed'] and left['snapshot'] == right['snapshot']
        assert sha(R / 'initial_bundles' / (left['id'] + '.json')) == sha(R / 'initial_bundles' / (right['id'] + '.json'))
        assert feedback['parent_generation_sha256'] == sha(R / 'generations' / (feedback['parent'] + '.json'))
        feedback_pairs += 1
    same_length_pairs = 0
    for t in adaptive['trials']:
        if t['condition'] != 'example89': continue
        parent = by_id[t['matched_parent']]['trial']
        assert len(t['input_token_ids']) == len(parent['input_token_ids'])
        changed = [(a, b) for a, b in zip(t['input_token_ids'], parent['input_token_ids']) if a != b]
        assert len(changed) == 2
        same_length_pairs += 1
    assert len(rows) == 56 and sum(x['world_rebuilt'] for x in rows) == 48
    result = {'schema': 'scheme-command-record-checks-1', 'model_generations_in_studies': 56,
              'new_generations_for_verification': 0, 'model_weights_loaded_by_verifier': False,
              'records_verified': len(rows), 'worlds_reconstructed': 48,
              'matched_reference_prompt_seed_pairs': reference_pairs,
              'feedback_pairs_with_byte_identical_initial_bundles': feedback_pairs,
              'example_operand_pairs_same_length_two_token_changes': same_length_pairs,
              'model_asset_and_declared_code_pins_unchanged': True,
              'original_scoring_preserved': True, 'all_record_checks_pass': True, 'rows': rows,
              'limits': 'Record checks, not stochastic generation reruns or independent model trials. Main PLAN did not pin all helper files; see protocol audit.'}
    (R / 'RECORD_CHECKS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ('records_verified', 'worlds_reconstructed', 'all_record_checks_pass')}))


if __name__ == '__main__': main()
