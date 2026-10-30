"""Optional byte-bound audit of one declared model-run cohort; no inference."""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re

from evidence_threshold import load_json

RULESET = 'stored-run-audit-0.1'
LIMIT = 8 * 1024 * 1024
LABELS = {'YES', 'NO', 'WITHHOLD'}


class Blocked(ValueError):
    def __init__(self, stage, reason):
        self.stage, self.reason = stage, reason


def require(ok, stage, reason):
    if not ok:
        raise Blocked(stage, reason)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_bound(spec, root):
    require(isinstance(spec, dict) and set(spec) == {'path', 'sha256'},
            'invalid_contract', 'artifact_spec')
    require(isinstance(spec['path'], str) and bool(spec['path']) and
            isinstance(spec['sha256'], str) and
            re.fullmatch('[0-9a-f]{64}', spec['sha256']), 'invalid_contract', 'artifact_spec')
    rel = Path(spec['path'])
    path = (root / rel).resolve()
    require(not rel.is_absolute() and path.is_relative_to(root), 'invalid_contract', 'path_escape')
    try:
        with path.open('rb') as stream:
            data = stream.read(LIMIT + 1)
    except OSError as exc:
        raise Blocked('source_unavailable', 'artifact_read') from exc
    require(len(data) <= LIMIT, 'invalid_source', 'artifact_size')
    actual = sha(data)
    require(actual == spec['sha256'], 'source_hash_mismatch', 'artifact_hash')
    return data


def evaluate(contract, root):
    out = {'ruleset': RULESET, 'status': 'withheld', 'stage': 'invalid_contract',
           'tool_sha256': sha(Path(__file__).read_bytes()),
           'json_loader_sha256': sha(Path(__file__).with_name('evidence_threshold.py').read_bytes()),
           'limitations': [
               'Caller selects cohort, identity and keys; these are not authenticated or proven true.',
               'Exact stripped uppercase labels only; unrecognized output stays in the denominator.',
               'Token arrays/counts and stop metadata are structurally checked, not replayed or decoded.',
               'No cache-file verification, model inference, causal efficacy or generalization claim.']}
    try:
        require(isinstance(contract, dict) and set(contract) == {
            'claim_id', 'identity', 'expected_run_ids', 'raw', 'keys', 'parser'},
            'invalid_contract', 'contract_fields')
        require(isinstance(contract['claim_id'], str) and 0 < len(contract['claim_id']) <= 128,
                'invalid_contract', 'claim_id')
        require(contract['parser'] == 'strip_upper_exact_label_v1', 'invalid_contract', 'parser')
        identity = contract['identity']
        require(isinstance(identity, dict) and set(identity) == {'family', 'facet', 'cycle', 'arm'}
                and all(isinstance(v, str) and 0 < len(v) <= 128 for v in identity.values()),
                'invalid_contract', 'identity')
        ids = contract['expected_run_ids']
        require(isinstance(ids, list) and 0 < len(ids) <= 1000 and
                all(isinstance(v, str) and 0 < len(v) <= 128 for v in ids) and
                len(set(ids)) == len(ids), 'invalid_contract', 'expected_ids')
        root = Path(root).resolve(strict=True)
        require(root.is_dir(), 'invalid_contract', 'root')
        raw_data = read_bound(contract['raw'], root)
        key_data = read_bound(contract['keys'], root)
        out.update(claim_id=contract['claim_id'], identity=identity,
                   contract_sha256=sha(json.dumps(contract, sort_keys=True,
                       separators=(',', ':'), allow_nan=False).encode()),
                   sources={'raw': sha(raw_data), 'keys': sha(key_data)})
        try:
            lines = raw_data.decode('utf-8').splitlines()
            require(bool(lines) and all(line.strip() for line in lines), 'invalid_source', 'blank_record')
            rows = [load_json(line) for line in lines]
            keys = load_json(key_data)
        except (ValueError, UnicodeError) as exc:
            if isinstance(exc, Blocked):
                raise
            raise Blocked('invalid_source', 'strict_json') from exc
        require(isinstance(keys, list) and all(isinstance(k, dict) and
                isinstance(k.get('id'), str) and isinstance(k.get('expected'), str) and
                k['expected'] in LABELS for k in keys), 'invalid_source', 'key_schema')
        require(len(keys) == len(ids) and {k['id'] for k in keys} == set(ids),
                'cohort_mismatch', 'key_ids')
        require(all(isinstance(r, dict) and isinstance(r.get('run_id'), str) for r in rows),
                'invalid_source', 'row_schema')
        require(len(rows) == len(ids) and {r['run_id'] for r in rows} == set(ids),
                'cohort_mismatch', 'run_ids')
        key_map = {k['id']: k['expected'] for k in keys}
        details, labels, stops = [], Counter(), Counter()
        inputs = outputs = matches = baseline = 0
        for row in rows:
            require(all(row.get(k) == v for k, v in identity.items()),
                    'identity_mismatch', 'row_identity')
            require(isinstance(row.get('text'), str), 'invalid_source', 'text')
            require(row.get('stop') in ('eos', 'token_limit'), 'invalid_source', 'stop')
            for count, tokens in [('input_tokens', 'input_token_ids'),
                                  ('output_tokens', 'generated_token_ids')]:
                require(type(row.get(count)) is int and row[count] > 0 and
                        isinstance(row.get(tokens), list) and len(row[tokens]) == row[count] and
                        all(type(t) is int and t >= 0 for t in row[tokens]),
                        'invalid_source', 'token_metadata')
            label = row['text'].strip().upper()
            label = label if label in LABELS else 'UNRESOLVED'
            expected = key_map[row['run_id']]
            hit = label == expected
            matches += int(hit)
            baseline += int(expected == 'YES')
            labels[label] += 1
            stops[row['stop']] += 1
            inputs += row['input_tokens']
            outputs += row['output_tokens']
            details.append({'run_id': row['run_id'], 'label': label,
                            'expected': expected, 'label_match': hit})
        ratio = Fraction(matches, len(ids))
        out.update(status='computed', stage='cohort_summary',
                   summary={'calls': len(ids), 'label_matches': matches,
                            'match_fraction': {'numerator': ratio.numerator, 'denominator': ratio.denominator},
                            'constant_yes_matches': baseline, 'labels': dict(labels),
                            'stops': dict(stops), 'input_tokens': inputs, 'output_tokens': outputs},
                   rows=sorted(details, key=lambda x: ids.index(x['run_id'])))
    except Blocked as exc:
        out.update(stage=exc.stage, reason=exc.reason)
    except (OSError, RuntimeError, TypeError, ValueError):
        out.update(stage='invalid_contract', reason='unreadable_root_or_contract')
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('contract', type=Path)
    parser.add_argument('--root', type=Path, required=True)
    args = parser.parse_args()
    data = args.contract.read_bytes()
    try:
        out = evaluate(load_json(data), args.root)
    except (ValueError, UnicodeError):
        out = {'status': 'withheld', 'stage': 'invalid_contract', 'reason': 'strict_json'}
    out['contract_input_sha256'] = sha(data)
    print(json.dumps(out, indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
