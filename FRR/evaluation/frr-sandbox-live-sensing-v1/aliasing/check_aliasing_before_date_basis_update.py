"""Read-only real-world witness: a complete directory projection can alias content.

No world opens, actions, model generation or replay. Optional output is confined
to a newly named results JSON file, using exclusive creation.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
EVALUATION = HERE.parents[1]
INSTRUMENT = EVALUATION / 'frr-sandbox-rd-v1/interface/instrument/snapshot_packet.py'
SOURCE = EVALUATION / 'history-retrieval-three-cycle-v1/program-transfer'
sys.path[:0] = [str(INSTRUMENT.parent), str(EVALUATION / 'observability-three-contact-v1')]
from snapshot_packet import make_snapshot
import common as c


def inventory(path: Path) -> dict[str, str]:
    return {str(p.relative_to(path)): c.sha(p) for p in sorted(path.rglob('*'))
            if p.is_file() and '__pycache__' not in p.parts}


def decode_file(store: Path, entry: list) -> bytes:
    assert entry[1] == 'file'
    obj = c.read(store / 'objects' / (entry[3] + '.json'))
    data = base64.b64decode(obj['base64'], validate=True)
    assert len(data) == entry[4] == obj['bytes']
    assert hashlib.sha256(data).hexdigest() == entry[3] == obj['sha256']
    return data


def check() -> dict:
    source_before = inventory(SOURCE)
    instrument_sha = c.sha(INSTRUMENT)
    source_results = c.read(SOURCE / 'RESULTS.json')
    saved_artifact_path = EVALUATION / 'history-retrieval-three-cycle-v1/results/provided_value_t1_raw.json'
    artifact = c.read(saved_artifact_path)['text']
    rows = {x['case']: x for x in source_results['rows']}
    evidence = {}
    projections = {}
    bundles = {}
    for case, expected_value in [('transfer_a', 'K7M4Q9'), ('transfer_b', 'R2V8T6')]:
        store = SOURCE / 'worlds' / case
        verification = c.verify_store(store)  # Source/CAS/chain reads only.
        assert verification['status'] == 'pass'
        bundle_path = store / 'bundles/000001.json'
        bundle = c.read(bundle_path)
        bundles[case] = bundle
        assert bundle['id'] == rows[case]['before_id']
        entry = next(x for x in bundle['entries'] if x[0] == 'probe_value.json')
        file_bytes = decode_file(store, entry)
        value = json.loads(file_bytes)['value']
        assert value == expected_value
        projected = make_snapshot(bundle, timing='initial', world_step=1,
                                  reply_index=None, max_packet_bytes=8192)
        projections[case] = projected
        batch_path = SOURCE / 'results' / (case + '_batch.json')
        batch = c.read(batch_path)
        assert batch['raw_text'] == artifact
        assert batch['parsed'] == c.parse_notebook(artifact)
        assert batch['parsed']['complete_executable_cells'] == 1
        assert batch['operations'][0]['before_id'] == bundle['id']
        for op in batch['operations']:
            plain = {k: v for k, v in op.items()
                     if k not in ['cell_index', 'source_start', 'source_end']}
            assert plain == c.read(store / 'events' / f"{op['step']:06d}.json")
            if 'cell_index' in op:
                assert op['source'] == batch['parsed']['cells'][op['cell_index']]['source']
        cells = [op for op in batch['operations'] if op['channel'] == 'python']
        assert len(cells) == 1
        cell = cells[0]
        assert cell['feedback']['exit_code'] == 0 and cell['feedback']['boundary'] is None
        assert cell['feedback']['stdout'] == 'Value: ' + value + '\n'
        assert rows[case]['stdout'] == [cell['feedback']['stdout']]
        assert rows[case]['after_id'] == batch['operations'][-1]['after_id']
        evidence[case] = {
            'initial_bundle_id': bundle['id'],
            'source_file_entry': entry,
            'decoded_source_json': json.loads(file_bytes),
            'decoded_file_bytes': len(file_bytes),
            'projection_observer_record': projected.observer_record,
            'saved_artifact_stdout': cell['feedback']['stdout'],
            'saved_artifact_cell_source_sha256': hashlib.sha256(cell['source'].encode()).hexdigest(),
            'saved_result_before_id_matches': True,
            'stored_world_verification': verification,
        }
    a, b = bundles['transfer_a'], bundles['transfer_b']
    ea, eb = {x[0]: x for x in a['entries']}, {x[0]: x for x in b['entries']}
    assert set(ea) == set(eb)
    differing_entries = [name for name in sorted(ea) if ea[name] != eb[name]]
    assert differing_entries == ['probe_value.json']
    assert ea['probe_value.json'][:3] == eb['probe_value.json'][:3]
    assert ea['probe_value.json'][4] == eb['probe_value.json'][4] == 19
    assert ea['probe_value.json'][3] != eb['probe_value.json'][3]
    pa, pb = projections['transfer_a'], projections['transfer_b']
    assert pa.model_packet == pb.model_packet
    assert pa.model_text == pb.model_text
    assert a['id'] != b['id']
    assert pa.observer_record['source_bundle_id'] != pb.observer_record['source_bundle_id']
    assert evidence['transfer_a']['saved_artifact_cell_source_sha256'] == evidence['transfer_b']['saved_artifact_cell_source_sha256']
    assert evidence['transfer_a']['saved_artifact_stdout'] != evidence['transfer_b']['saved_artifact_stdout']
    assert source_before == inventory(SOURCE)
    assert instrument_sha == c.sha(INSTRUMENT)
    source_pins = {str(p): c.sha(p) for p in [
        Path(__file__), INSTRUMENT, SOURCE / 'PLAN.json', SOURCE / 'RESULTS.json',
        saved_artifact_path,
        EVALUATION / 'minimal-garden-candidate-v1/world/garden_world.py',
        EVALUATION / 'final-garden-contract-v1/world.py',
        EVALUATION / 'final-garden-contract-v1/server.py',
    ]}
    for case in ['transfer_a', 'transfer_b']:
        for rel in ['bundles/000001.json', 'MANIFEST.json', 'STATE.json']:
            path = SOURCE / 'worlds' / case / rel
            source_pins[str(path)] = c.sha(path)
        path = SOURCE / 'results' / (case + '_batch.json')
        source_pins[str(path)] = c.sha(path)
    return {
        'status': 'pass', 'date': '2026-11-14 America/Chicago',
        'new_model_calls': 0, 'new_world_actions': 0, 'world_opens': 0,
        'source_worlds_modified': False, 'instrument_modified': False,
        'source_version': 'history-retrieval-three-cycle-v1/program-transfer, previously completed artifact check',
        'source_activity_not_rerun': {'model_calls': source_results['model_calls'],
                                    'artifact_executions': source_results['artifact_executions']},
        'projection_version': 'snapshot_packet_v1',
        'shared_projection_arguments': {'timing': 'initial', 'world_step': 1,
                                        'reply_index': None, 'max_packet_bytes': 8192},
        'captured_entries_per_world': len(a['entries']),
        'different_supported_entries': differing_entries,
        'same_model_packet': True, 'same_model_text': True,
        'model_packet_bytes': len(pa.model_text.encode()),
        'model_text_sha256': hashlib.sha256(pa.model_text.encode()).hexdigest(),
        'shared_model_text': pa.model_text,
        'observer_bundle_ids_differ': True,
        'file_contents_differ': True,
        'same_saved_reading_artifact': True,
        'saved_read_consequences_differ': True,
        'evidence': evidence, 'source_pins': source_pins,
        'interpretation': 'A complete directory metadata projection is not injective over the supported filesystem content states. The same saved reading program had distinct actual consequences. This does not test a new model policy or establish that the sensor is useless.',
        'important_scope': 'The witness aliases the directory packet alone, not a full next input that also includes distinct actual read receipts or different histories. Observer-side CAS bytes remain separate from model-visible metadata.',
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write-results', type=Path)
    args = parser.parse_args()
    if args.write_results is not None and args.write_results.exists():
        raise FileExistsError('Preserve prior results: choose a new result path')
    result = check()
    if args.write_results is not None:
        assert args.write_results.parent.resolve() == HERE.resolve(), 'Outputs belong only in aliasing/'
        with args.write_results.open('x', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
            f.write('\n')
    print(json.dumps({k: result[k] for k in ['status', 'captured_entries_per_world',
          'same_model_text', 'model_packet_bytes', 'saved_read_consequences_differ',
          'new_model_calls', 'new_world_actions', 'world_opens']}))
