"""Verify stored pilot records and rebuilt worlds; no generation or weights load."""
from pathlib import Path
import hashlib
import json
import sys
import tempfile

from world_store import World
from world_bundle import import_world


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    study = Path(__file__).resolve().parents[1]
    pilot = study / 'pilot'
    plan = json.loads((pilot / 'PLAN.json').read_text())
    summary = json.loads((pilot / 'SUMMARY.json').read_text())
    profile = json.loads((study / 'constants.json').read_text())
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained('/workspace/cache_backend_models/smollm2-135m',
                                              local_files_only=True, trust_remote_code=False)
    assert all(sha(path) == expected for path, expected in plan['model_file_pins'].items())
    assert all(sha(path) == expected for path, expected in plan['code_pins'].items())
    assert sha(study / 'constants.json') == plan['profile_sha256']
    rows = []
    with tempfile.TemporaryDirectory(prefix='cw-pilot-rebuild-') as directory:
        for trial in plan['trials']:
            identity = trial['id']
            generation = json.loads((pilot / 'generations' / (identity + '.json')).read_text())
            result = json.loads((pilot / 'receipts' / (identity + '.json')).read_text())
            start = json.loads((pilot / 'starts' / (identity + '.json')).read_text())
            ids = tokenizer.apply_chat_template([{'role': 'user', 'content': trial['prompt']}],
                                                tokenize=True, add_generation_prompt=True)
            assert ids == trial['input_token_ids'] == generation['input_token_ids']
            assert generation['text'] == tokenizer.decode(generation['generated_token_ids'], skip_special_tokens=True)
            assert generation['rng_seed'] == trial['seed'] == start['seed']
            assert start['plan_sha256'] == sha(pilot / 'PLAN.json')
            assert generation['temperature'] == plan['temperature']
            assert generation['top_p'] == plan['top_p']
            assert 1 <= len(generation['generated_token_ids']) <= 96
            if generation['stop'] == 'eos':
                assert generation['generated_token_ids'][-1] == tokenizer.eos_token_id
            else:
                assert generation['stop'] == 'token_limit' and len(generation['generated_token_ids']) == 96
            db = Path(directory) / (identity + '.sqlite')
            import_world(pilot / 'final_bundles' / (identity + '.json'), db, profile)
            world = World(db, profile)
            try:
                retry = world.submit('model-action', trial['expected_snapshot'], generation['text'].strip())
                assert retry == result['receipt']
                assert not result['accepted_action']
                assert result['receipt']['world_snapshot'] == trial['expected_snapshot']
                world.verify_integrity()
            finally:
                world.close()
            rows.append({'id': identity, 'input_tokens': len(ids),
                         'generated_tokens': len(generation['generated_token_ids']),
                         'record_verified': True, 'bundle_rebuilt_and_retry_identical': True,
                         'guest_snapshot_unchanged_by_model_reply': True})
    assert len(rows) == summary['calls'] == 10
    assert summary['accepted_actions'] == 0 and summary['requested_outcomes_correct'] == 0
    result = {'schema': 'cw-pilot-record-verification-1', 'records': len(rows),
              'new_model_generations': 0, 'model_weights_loaded': False,
              'all_verified': True, 'model_asset_files_unchanged': True,
              'generation_time_tensor_digest_checks': summary['weights_and_adapter_unchanged'],
              'plan_sha256': sha(pilot / 'PLAN.json'), 'rows': rows,
              'start_records_match_plan_hash': True,
              'scope': 'Record and immutable-world reconstruction checks, not stochastic generation reruns or general model capability.'}
    (pilot / 'RECORD_CHECKS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'records_verified': len(rows), 'reconstructed_worlds': len(rows),
                      'new_generations': 0}))


if __name__ == '__main__':
    main()
