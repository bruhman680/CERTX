#!/usr/bin/env python3
"""Deterministically build and validate the counterbalanced batch-state curriculum.

No model, network, or training calls. Run this file to regenerate all fixtures.
"""
import hashlib
import itertools
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'DATA'
STATES = ('positive', 'zero', 'missing')
LABEL = dict(zip(STATES, ('YES', 'NO', 'WITHHOLD')))
TRAIN_FORMATS = ('fields', 'prose', 'flatJSON', 'table')
PRIMARY_FORMATS = ('XML', 'bulletsections')
GUIDANCE = {
    'instruction': 'For the named target batch, decide whether its recorded sampled-soil count is positive. Return YES for an explicit positive count, NO for an explicit zero, or WITHHOLD if that target count is unavailable. The markers null, unavailable and not recorded mean missing. Other batches and other fields do not supply the target count. Return only YES, NO or WITHHOLD.',
    'question': "Is the target batch's recorded sampled-soil count positive?",
}

def value(state, positive):
    return {'positive': positive, 'zero': 0, 'missing': None}[state]

def record(name, state, positive):
    return {'batch': name, 'sampled_soils': value(state, positive),
            'observations_per_soil': 5, 'damaged_plots': 0, 'inspections': None}

def body(family, records):
    def count(r):
        return 'not recorded' if r['sampled_soils'] is None else str(r['sampled_soils'])
    if family == 'fields':
        return '\n'.join(f"Batch {r['batch']}: sampled soils {count(r)}; observations per soil 5; damaged plots 0; inspections unavailable." for r in records)
    if family == 'prose':
        return '\n'.join(f"For batch {r['batch']}, the sampled-soil count is {count(r)} and observations per soil total 5. Its damaged plots total 0 and inspections are unavailable." for r in records)
    if family == 'flatJSON':
        # Two complete flat records; no scope-bearing target/other field names.
        return '\n'.join(json.dumps(r, separators=(',', ':')) for r in records)
    if family == 'table':
        return '| batch | sampled soils | observations per soil | damaged plots | inspections |\n| --- | --- | --- | --- | --- |\n' + '\n'.join(f"| {r['batch']} | {count(r)} | 5 | 0 | unavailable |" for r in records)
    if family == 'XML':
        return '<batches>\n' + '\n'.join(f'  <batch name="{r["batch"]}"><sampled_soils>{"unavailable" if r["sampled_soils"] is None else r["sampled_soils"]}</sampled_soils><observations_per_soil>5</observations_per_soil><damaged_plots>0</damaged_plots><inspections>unavailable</inspections></batch>' for r in records) + '\n</batches>'
    if family == 'bulletsections':
        return '\n\n'.join(f"Batch {r['batch']}\n- Sampled soils: {count(r)}\n- Observations per soil: 5\n- Damaged plots: 0\n- Inspections: unavailable" for r in records)
    raise ValueError(family)

def make_case(split, family, target_state, other_state, target_role, position, names, positive, group_id=None):
    target_name = names[target_role]
    other_name = names[1 - target_role]
    records = [record(target_name, target_state, positive), record(other_name, other_state, positive)]
    if position == 'last':
        records.reverse()
    source = f'Target batch: {target_name}.\n' + body(family, records)
    ident = f'{split}_{family}_o{other_state}_r{target_role}_{position}_{target_state}'
    case = {'id': ident, 'split': split, 'structure_family': family, 'source': source}
    key = {'id': ident, 'expected': LABEL[target_state], 'state': target_state,
           'target_state': target_state, 'other_state': other_state,
           'target_value': value(target_state, positive), 'other_value': value(other_state, positive),
           'family': family, 'target_role': target_role, 'target_identity': target_name,
           'other_identity': other_name, 'position': position, 'target_record_position': position,
           'records': [dict(r, record_position=i, state=target_state if r['batch'] == target_name else other_state,
                            is_target=r['batch'] == target_name) for i, r in enumerate(records)]}
    if group_id is not None:
        key['group_id'] = group_id
    return case, key

def build():
    train, primary_cases, primary_keys, dev_cases, dev_keys = [], [], [], [], []
    group_number = 0
    for family, other_state, target_role, position in itertools.product(TRAIN_FORMATS, STATES, (0, 1), ('first', 'last')):
        group_id = f'train_group_{group_number:02d}'
        group_number += 1
        for state in STATES:
            case, key = make_case('train', family, state, other_state, target_role, position, ('Birch', 'Cedar'), 11, group_id)
            train.append(dict(case, **{k: v for k, v in key.items() if k != 'id'}, label=key['expected'], target=key['target_value'], distractor=key['other_value']))
    # Each canonical ordered fact body receives both possible target headers.
    # This is the same 2×3×3×2×2 factorial as target/other enumeration.
    for family, first_state, second_state, first_role in itertools.product(PRIMARY_FORMATS, STATES, STATES, (0, 1)):
        pair_id = f'pair_{family}_{first_state}_{second_state}_r{first_role}'
        for target_role in (0, 1):
            position = 'first' if target_role == first_role else 'last'
            state = first_state if position == 'first' else second_state
            other_state = second_state if position == 'first' else first_state
            case, key = make_case('primary', family, state, other_state, target_role, position, ('Hazel', 'Larch'), 13)
            key['pair_id'] = pair_id
            key['pair_type'] = 'same_state' if first_state == second_state else 'discordant_state'
            primary_cases.append(case)
            primary_keys.append(key)
    for index, family in enumerate(TRAIN_FORMATS):
        for state in STATES:
            case, key = make_case('dev', family, state, 'positive', index % 2, 'first' if index % 2 == 0 else 'last', ('Birch', 'Cedar'), 17)
            dev_cases.append(case)
            dev_keys.append(key)
    return train, primary_cases, primary_keys, dev_cases, dev_keys

def validate(train, primary, primary_keys, dev, dev_keys):
    assert (len(train), len(primary), len(primary_keys), len(dev), len(dev_keys)) == (144, 72, 72, 12, 12)
    assert all(set(c) == {'id', 'split', 'structure_family', 'source'} for c in primary + dev)
    for rows in (train, primary, dev):
        assert len({r['id'] for r in rows}) == len(rows)
        assert len({r['source'] for r in rows}) == len(rows)
    assert len({r['source'] for r in train + primary + dev}) == 228
    assert Counter(r['label'] for r in train) == {'YES': 48, 'NO': 48, 'WITHHOLD': 48}
    assert Counter(k['expected'] for k in primary_keys) == {'YES': 24, 'NO': 24, 'WITHHOLD': 24}
    assert Counter(k['expected'] for k in dev_keys) == {'YES': 4, 'NO': 4, 'WITHHOLD': 4}
    assert Counter((r['structure_family'], r['target_state'], r['other_state'], r['target_role'], r['position']) for r in train) == Counter(itertools.product(TRAIN_FORMATS, STATES, STATES, (0, 1), ('first', 'last')))
    assert Counter((k['family'], k['target_state'], k['other_state'], k['target_role'], k['position']) for k in primary_keys) == Counter(itertools.product(PRIMARY_FORMATS, STATES, STATES, (0, 1), ('first', 'last')))
    for i in range(0, len(train), 3):
        triple = train[i:i+3]
        assert [r['label'] for r in triple] == ['YES', 'NO', 'WITHHOLD']
        assert len({r['group_id'] for r in triple}) == 1
        assert len({(r['family'], r['other_state'], r['target_role'], r['position']) for r in triple}) == 1
    by_id = {c['id']: c for c in primary}
    pairs = defaultdict(list)
    for k in primary_keys:
        pairs[k['pair_id']].append(k)
    assert len(pairs) == 36
    assert Counter(v[0]['pair_type'] for v in pairs.values()) == {'discordant_state': 24, 'same_state': 12}
    for members in pairs.values():
        assert len(members) == 2
        a, b = [by_id[k['id']]['source'] for k in members]
        ha, ba = a.split('\n', 1)
        hb, bb = b.split('\n', 1)
        assert ba.encode('utf-8') == bb.encode('utf-8')
        assert ha != hb and {ha, hb} == {'Target batch: Hazel.', 'Target batch: Larch.'}
        assert {k['target_role'] for k in members} == {0, 1}
        assert {k['position'] for k in members} == {'first', 'last'}
    for cases, keys, positive, names in ((train, train, 11, ('Birch', 'Cedar')), (primary, primary_keys, 13, ('Hazel', 'Larch')), (dev, dev_keys, 17, ('Birch', 'Cedar'))):
        assert [c['id'] for c in cases] == [k['id'] for k in keys]
        for c, k in zip(cases, keys):
            header, text = c['source'].split('\n', 1)
            assert not re.search(r'\b(?:other|target)\b', text, re.I)
            assert header == f'Target batch: {names[k["target_role"]]}.'
            assert len(k['records']) == 2
            for r in k['records']:
                assert r['observations_per_soil'] == 5 and r['damaged_plots'] == 0 and r['inspections'] is None
                assert r['sampled_soils'] == value(r['state'], positive)
                assert r['batch'] in names
            position_index = 0 if k['position'] == 'first' else 1
            assert k['records'][position_index]['is_target']
            assert k['expected'] == LABEL[k['target_state']]
    return {'all_passed': True, 'train_cases': 144, 'train_groups': 48, 'train_group_labels': ['YES', 'NO', 'WITHHOLD'],
            'primary_cases': 72, 'primary_pairs': 36, 'discordant_pairs': 24, 'discordant_cases': 48,
            'same_state_pairs': 12, 'same_state_cases': 24, 'dev_cases': 12,
            'primary_body_byte_identity': True, 'primary_pair_only_header_changes': True,
            'all_source_unique': True, 'factorial_coverage_complete': True,
            'labels_balanced': True, 'body_role_words_absent': True, 'all_records_complete': True,
            'positive_values': {'train': 11, 'primary': 13, 'dev': 17},
            'irrelevant_fields': {'observations_per_soil': 5, 'damaged_plots': 0, 'inspections': None},
            'comparison': 'Compare this training package with the existing old 72-source-trained mean checkpoint using the same 48 updates. Changes include format and support; this is not an isolated causal test of record position.'}

def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')

def main():
    DATA.mkdir(exist_ok=True)
    train, primary, primary_keys, dev, dev_keys = build()
    checks = validate(train, primary, primary_keys, dev, dev_keys)
    files = {'TRAIN.json': train, 'PRIMARY_CASES.json': primary, 'PRIMARY_KEYS.json': primary_keys,
             'DEV_CASES.json': dev, 'DEV_KEYS.json': dev_keys, 'GUIDANCE.json': GUIDANCE}
    for name, obj in files.items():
        write_json(DATA / name, obj)
    checks['sha256'] = {name: hashlib.sha256((DATA / name).read_bytes()).hexdigest() for name in files}
    write_json(ROOT / 'DATA_CHECKS.json', checks)
    print(json.dumps({k: checks[k] for k in ('all_passed', 'train_cases', 'primary_cases', 'primary_pairs', 'dev_cases')}))

if __name__ == '__main__':
    main()
