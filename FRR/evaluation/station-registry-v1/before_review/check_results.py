"""Post-demo consistency and source-preservation checks, not independent review."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sha = lambda data: hashlib.sha256(data).hexdigest()
freeze = json.loads((HERE / 'FREEZE.json').read_text())
changed = [p for p, h in freeze['files'].items() if sha((ROOT / p).read_bytes()) != h]
assert not changed, changed
receipt_bytes = (HERE / 'REGISTRY_RECEIPT.json').read_bytes()
out = json.loads(receipt_bytes)
assert out['status'] == 'indexed' and len(out['stations']) == 4
stations = out['stations']
assert all(s['status'] == 'indexed' for s in stations)
assert stations[0]['scoped_summary']['answer'] == 'YES'
assert [(s['scoped_summary']['summary']['label_matches'], s['scoped_summary']['summary']['calls']) for s in stations[1:]] == [(4, 10), (4, 48), (16, 48)]
assert stations[2]['scoped_summary']['unresolved_outputs'] == 36
assert stations[3]['scoped_summary']['summary']['labels'] == {'NO': 48}
assert not {'summary', 'confidence', 'vote', 'answer', 'contradiction'} & out.keys()
assert stations[2]['reported_source_hashes']['keys'] != stations[3]['reported_source_hashes']['keys']
for role in ('declared_shared_evaluation_inputs', 'declared_shared_parent_keys'):
    assert any(sum(u['role'] == role for u in w['uses']) == 2 for w in out['ancestry_warnings']), role
replay = subprocess.run([sys.executable, str(ROOT / 'tools/station_registry.py'), str(HERE / 'manifest.json'), '--root', str(ROOT)], capture_output=True, check=True)
assert replay.stdout == receipt_bytes
checks = {'status': 'passed', 'frozen_files_checked': len(freeze['files']), 'changed_frozen_files': changed,
          'indexed_stations': len(stations), 'shared_hash_warnings': len(out['ancestry_warnings']),
          'scoped_counts': [[4, 10], [4, 48], [16, 48]], 'unresolved_original_test_outputs': 36,
          'shared_input_and_parent_key_warnings': True, 'distinct_arm_key_hashes_retained': True,
          'no_pooled_result_fields': True, 'deterministic_replay_byte_equal': True,
          'receipt_sha256': sha(receipt_bytes), 'freeze_sha256': sha((HERE / 'FREEZE.json').read_bytes()),
          'review': 'Subagent-authored checks of subagent-built registry. Coordinator review separate; no independent replication.'}
(HERE / 'CHECKS.json').write_text(json.dumps(checks, indent=2) + '\n')
print(json.dumps(checks, indent=2))
