"""Check package structure and cross-references; no model or API calls."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def check(value, schema, path):
    if 'const' in schema:
        assert value == schema['const'], path
    if 'enum' in schema:
        assert value in schema['enum'], path
    typ = schema.get('type')
    allowed = typ if isinstance(typ, list) else [typ]
    matches = {'object': isinstance(value, dict), 'array': isinstance(value, list),
               'string': isinstance(value, str), 'null': value is None}
    if typ:
        assert any(matches.get(t, False) for t in allowed), path
    if isinstance(value, dict) and typ == 'object':
        assert set(schema.get('required', [])) <= set(value), path
        assert set(value) <= set(schema['properties']), path
        for key, item in value.items():
            check(item, schema['properties'][key], f'{path}.{key}')
    if isinstance(value, list) and typ == 'array':
        for i, item in enumerate(value):
            check(item, schema['items'], f'{path}[{i}]')


def references(record):
    claims = {x['id'] for x in record['claims']}
    artifacts = {x['id'] for x in record['artifacts']}
    all_ids = [x['id'] for group in ['claims', 'artifacts', 'revisions', 'branches']
               for x in record[group]]
    assert len(all_ids) == len(set(all_ids)), 'Duplicate IDs'
    for c in record['claims']:
        assert set(c['support']) <= artifacts
        assert c['supersedes'] is None or c['supersedes'] in claims
        assert c['supersedes'] != c['id']
    for a in record['artifacts']:
        assert set(a['supports']) <= claims
    for r in record['revisions']:
        assert set(r['changed']) <= claims | artifacts
        assert set(r['downstream']) <= artifacts


def main():
    schema = json.loads((ROOT / 'state/schema.json').read_text())
    for name in ['state/empty.json', 'examples/marker-record.json']:
        record = json.loads((ROOT / name).read_text())
        check(record, schema, name)
        references(record)
    ids = set()
    counts = {}
    for split in ['development', 'heldout']:
        cases = [json.loads(line) for line in
                 (ROOT / f'evaluation/{split}.jsonl').read_text().splitlines()]
        counts[split] = len(cases)
        for case in cases:
            assert set(case) == {'id', 'focus', 'turns', 'expected', 'failure'}
            assert case['id'] not in ids
            ids.add(case['id'])
            assert case['turns'] and all(isinstance(t, str) and t for t in case['turns'])
            assert all(case[k] for k in ['focus', 'expected', 'failure'])
    for name in ['README.md', 'LINEAGE.md', 'prompts/runtime.md',
                 'prompts/compact.md', 'evaluation/PROTOCOL.md',
                 'examples/worked-response.md']:
        assert (ROOT / name).read_text().strip(), name
    print(f'Package checks passed: two inquiry records; {counts}; required documents present.')
    print('These checks establish structural consistency, not FRR effectiveness.')


if __name__ == '__main__':
    main()
