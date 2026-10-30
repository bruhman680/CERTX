"""Prepare declarations and freeze before demo; refuses to overwrite a freeze."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent

def reference(path, role=None):
    out = {'path': path, 'sha256': hashlib.sha256((ROOT / path).read_bytes()).hexdigest()}
    if role is not None: out['role'] = role
    return out


def prepare():
    if (HERE / 'FREEZE.json').exists():
        raise SystemExit('Freeze already exists; preserve it and document amendments.')
    cv = 'evaluation/complete-verification-path-v1/'
    nt = 'evaluation/narrow-training-pilot-v1/'
    audit = 'evaluation/stored-run-audit-v1/'
    stations = [{
        'station_id': 'conditional-variance-demo',
        'question': 'Garden03 / Batch03: under the supplied equal-cluster mixture, is variance at most 0.01?',
        'recipe': 'Existing deterministic source grammar -> exact conditional calculation, source-calculation-path-0.1. No model generation in this station.',
        'state': 'Computed conditional answer; source authenticity/truth and independence assumptions external. Authored and exposed demo, not hidden benchmark.',
        'receipt': reference(cv + 'checked_run/DEMO_RECEIPT.json'),
        'ancestry': [reference(cv + 'demo/source.txt', 'declared_source'), reference(cv + 'demo/contract.json', 'declared_contract')]
    }, {
        'station_id': 'full-task-model-audit',
        'question': 'Ten CVP3 full conditional-task direct-model runs: how many exact labels match supplied keys?',
        'recipe': 'Existing stored-run-audit-0.1 over fixed ten-call cohort; raw output capped at 64 new tokens, stripped uppercase exact labels, no correctness filtering.',
        'state': 'Untrusted direct-model diagnostic, exposed cohort. 4/10; always YES. Synthetic supplied keys are not authenticated source truth. Different task and generation cap from narrow training.',
        'receipt': reference(audit + 'RECEIPT.json'),
        'ancestry': [reference(audit + 'contract.json', 'declared_contract'), reference(cv + 'model_diagnostic/RAW_OUTPUTS.jsonl', 'declared_raw'), reference(cv + 'model_diagnostic/KEYS.json', 'declared_keys')]
    }]
    for arm in ('original_test', 'adapted_test'):
        state = ('Original unchanged checkpoint; zero additional updates in this arm; 4/48, 36 unresolved outputs.' if arm == 'original_test' else 'Separate partial checkpoint: one completed full-weight AdamW update/two examples (zero and positive), no missing-class update; memory-headroom stop before step two. 16/48; all NO, equal constant-label baseline; no semantic discrimination demonstrated or model promotion.')
        state += ' Shared 48-case structural test and supplied keys with the other arm; now exposed regression data. Coordinator experiment/scoring, no independent replication. Missing source state is WITHHOLD; unsupported generation is UNRESOLVED.'
        ancestry = [reference(nt + arm + '/' + name, role) for name, role in (
            ('contract.json', 'declared_contract'), ('RAW_SUBSET.jsonl', 'declared_raw'), ('KEY_SUBSET.json', 'declared_arm_keys'), ('DERIVATION.json', 'declared_subset_recipe'))]
        ancestry += [reference(nt + name, role) for name, role in (
            ('EVAL_CASES.json', 'declared_shared_evaluation_inputs'), ('KEYS.json', 'declared_shared_parent_keys'), ('TRAINING_MANIFEST.json', 'declared_training_state'), ('REPORT.md', 'declared_scope_and_limits'))]
        stations.append({'station_id': 'narrow-' + arm.replace('_', '-'),
            'question': 'On 48 fixed structural-holdout cases, does the explicitly recorded sampled-soil count have positive / zero / missing state? Exact label matches for ' + arm + '.',
            'recipe': 'Existing stored-run-audit-0.1; fresh argmax context, eight new-token cap; split/arm exact raw subset, key IDs gain arm suffix; unsupported outputs stay in denominator.',
            'state': state, 'receipt': reference(nt + arm + '/RECEIPT.json'), 'ancestry': ancestry})
    manifest = {'registry_id': 'existing-verification-stations-v1', 'stations': stations}
    (HERE / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    paths = {'tools/station_registry.py', 'tools/evidence_threshold.py', *('evaluation/station-registry-v1/' + name for name in ('PROTOCOL.md', 'test_registry.py', 'prepare_demo.py', 'manifest.json'))}
    for station in stations:
        paths.add(station['receipt']['path'])
        paths.update(ref['path'] for ref in station['ancestry'])
    freeze = {'phase': 'before_real_registry_demo', 'method': 'SHA256 exact bytes',
              'review': 'Station-registry subagent construction/tests; coordinator review not yet performed. Neither is independent replication.',
              'files': {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in sorted(paths)}}
    (HERE / 'FREEZE.json').write_text(json.dumps(freeze, indent=2) + '\n')


if __name__ == '__main__': prepare()
