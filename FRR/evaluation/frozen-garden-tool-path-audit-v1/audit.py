"""External audit only. No canonical generation, file changes, or repairs."""
from pathlib import Path
import base64, collections, hashlib, json, shlex, sys

H = Path(__file__).resolve().parent
P = H.parent / 'final-garden-contract-v1'
sys.path.insert(0, str(P))
import runner
from world import World, action, receive

def save(name, value):
    with (H / name).open('x') as f:
        json.dump(value, f, indent=2, ensure_ascii=False, allow_nan=False)
        f.write('\n')

def file_bytes(bundle, name):
    entry = next(x for x in bundle['entries'] if x[0] == name)
    obj = runner.read(runner.R / 'objects' / (entry[3] + '.json'))
    return base64.b64decode(obj['base64'], validate=True)

def main():
    before = runner.file_inventory(P)
    s = runner.state()
    assert s['paused'] and s['next_entry'] == 1550
    assert not (runner.R / 'PENDING.json').exists()
    runner.verify_pins()
    save('CANONICAL_BEFORE.json', before)
    bundle = runner.read(runner.R / 'bundles' / s['latest_bundle'])
    rows = runner.rows()
    names = ['LAWS.txt', 'notebook.txt', 'prior_replies.jsonl', 'transitions.json']
    material = {n: file_bytes(bundle, n) for n in names}
    copied = H / 'world-copy'
    copied.mkdir()
    for n, b in material.items():
        (copied / n).write_bytes(b)
    prior = [json.loads(line) for line in material['prior_replies.jsonl'].decode().splitlines() if line.strip()]
    counts = collections.Counter(r['result']['kind'] for r in rows)
    literal = '\nDirectory entries: ' + json.dumps(names)
    mechanisms = {
        'paused_at': 1550,
        'canonical_entries_examined': len(rows),
        'kinds': dict(counts),
        'eos': sum(r['stop'] == 'eos' for r in rows),
        'notebook_faults': sum(r['result']['kind'] == 'notebook' and r['visible_feedback'] is not None for r in rows),
        'replies_equal_final_directory_fact': sum(r['text'] == literal.strip() for r in rows),
        'json_action_candidates': sum(r['text'].lstrip().startswith('{') for r in rows),
        'fixed_notice': runner.NOTICE,
        'current_world_bytes': sum(x[4] for x in bundle['entries'] if x[1] == 'file'),
        'world_data_limit': 8388608,
        'file_data_limit': 262144,
        'files': {n: {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()} for n, b in material.items()},
        'prior_replies_lines': len(prior),
        'prior_replies_first': prior[0] if prior else None,
        'prior_replies_last': prior[-1] if prior else None,
        'framing': 'fixed notice and seed; twelve raw assistant replies with blank successful notebook feedback; directory names on final user turn; notebook contents not automatically loaded',
        'no_automatic_new_questions_or_task_outcomes': True,
        'output_tokens': 96,
    }
    save('MECHANICAL_TRACE.json', mechanisms)

    w = World()
    results = []
    def fixture(label, text, expected_kind, expected_stdout=None):
        result = receive(w, text)
        assert result['kind'] == expected_kind
        if expected_stdout is not None:
            assert result['feedback']['stdout'] == expected_stdout, result
            assert result['feedback']['exit_code'] == 0 and result['feedback']['boundary'] is None, result
        results.append({'label': label, 'operator_authored_fixture': True, 'text': text, 'result': result})
        return result
    try:
        w.restore(bundle, runner.R / 'objects')
        fixture('minimal arithmetic', json.dumps({'action': 'shell', 'source': "python3 -I -S -c 'print(6*7)'"}), 'shell', '42\n')
        fixture('read actual laws', json.dumps({'action': 'shell', 'source': 'cat LAWS.txt'}), 'shell', material['LAWS.txt'].decode())
        fixture('read notebook without loading entire book', json.dumps({'action': 'shell', 'source': 'tail -n 1 notebook.txt'}), 'shell', rows[-1]['text'] + '\n')
        fixture('write new durable file', json.dumps({'action': 'shell', 'source': "printf 'persisted\\n' > audit_marker.txt"}), 'shell', '')
        fixture('read across actions', json.dumps({'source': 'cat audit_marker.txt', 'action': 'shell'}), 'shell', 'persisted\n')
        error = fixture('real Python error', json.dumps({'action': 'shell', 'source': "python3 -I -S -c '1/0'"}), 'shell')
        assert error['feedback']['exit_code'] != 0 and 'ZeroDivisionError' in error['feedback']['stderr']
        fixture('code fence is ordinary writing', '```json\n{"action":"shell","source":"touch should_not_run"}\n```', 'notebook')
        fixture('extra key is ordinary writing', '{"action":"shell","source":"touch should_not_run","note":"test"}', 'notebook')
        fixture('raw shell is ordinary writing', 'touch should_not_run', 'notebook')
        assert not (w.home / 'should_not_run').exists()
        objects = H / 'clone-objects'
        after = w.capture(objects)
        w.close()
        w = World()
        w.restore(after, objects)
        assert w.capture(objects) == after
        fixture('read after independent restore', json.dumps({'action': 'shell', 'source': 'cat audit_marker.txt'}), 'shell', 'persisted\n')
        save('CLONE_CHECKPOINT.json', after)
    finally:
        w.close()
    save('TOOL_FIXTURES.json', {'source_checkpoint_entry': 1550, 'canonical_model_calls': 0, 'operator_authored': True, 'tests': results, 'restore_preserved': True, 'canonical_world_modified': False})
    after_inventory = runner.file_inventory(P)
    assert after_inventory == before
    save('CANONICAL_AFTER_MECHANICAL.json', {'identical_inventory': True, 'files_checked': len(before), 'state': runner.state()})
    print(json.dumps({'status': 'pass', 'fixtures': len(results), 'canonical_unchanged': True, 'canonical_entries': len(rows), 'kind_counts': dict(counts)}))

if __name__ == '__main__':
    main()
