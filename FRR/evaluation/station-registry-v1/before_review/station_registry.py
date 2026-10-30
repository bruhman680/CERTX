"""Optional read-only byte-bound receipt index; no evidence adjudication."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
from evidence_threshold import load_json

RULESET = 'station-registry-0.1'
MAX_BYTES = 1_048_576
HASH = re.compile(r'[0-9a-f]{64}\Z')
LIMITATIONS = [
    'Hashes bind bytes, not authenticity, source truth, independence or model competence.',
    'Questions, recipes, state and ancestry links are caller declarations, not authenticated.',
    'Receipt summaries are reported scoped results; underlying tools are not rerun.',
    'No pooled score, vote, confidence, universal truth or cross-task contradiction is computed.',
    'Missing shared hashes do not establish independence; different key hashes can encode shared keys.',
    'Local trusted workspace only; code hashes do not authenticate runtime or bytecode.'
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def text(value):
    return isinstance(value, str) and 0 < len(value.strip()) <= 4096


def exact(obj, fields):
    return isinstance(obj, dict) and set(obj) == set(fields.split())


def digest(value):
    return isinstance(value, str) and HASH.fullmatch(value) is not None


def read_bound(ref, root):
    if not exact(ref, 'path sha256') or not text(ref['path']) or not digest(ref['sha256']):
        raise ValueError('Invalid file reference.')
    relative = Path(ref['path'])
    path = (root / relative).resolve()
    if relative.is_absolute() or not path.is_relative_to(root):
        raise ValueError('Path escapes root.')
    with path.open('rb') as stream:
        data = stream.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError('File exceeds one MiB.')
    if sha(data) != ref['sha256']:
        raise ValueError('Declared SHA256 differs from file bytes.')
    return data


def summarize(receipt):
    """Narrow projections; fail closed on unknown versions or extra top-level fields."""
    if not isinstance(receipt, dict):
        raise ValueError('Receipt must be an object.')
    common = set('ruleset status stage tool_sha256 json_loader_sha256 limitations claim_id'.split())
    if not common <= receipt.keys() or not all(text(receipt[k]) for k in
            ('claim_id', 'stage', 'status')) or not all(digest(receipt[k]) for k in
            ('tool_sha256', 'json_loader_sha256')):
        raise ValueError('Unsupported receipt envelope.')
    if not isinstance(receipt['limitations'], list) or not all(text(x) for x in receipt['limitations']):
        raise ValueError('Invalid receipt limitations.')
    if receipt['ruleset'] == 'source-calculation-path-0.1':
        required = common | set('mode answer reason_codes entity scope contract_canonical_sha256 declared_model criterion source_sha256 bound_fields formula variance count_product interpretation'.split())
        if not required <= receipt.keys() or set(receipt) - required - {'contract_input_sha256'}:
            raise ValueError('Unsupported source receipt fields.')
        if (receipt['status'], receipt['stage'], receipt['mode']) != ('computed', 'conditional_answer', 'deterministic_source') or receipt['answer'] not in ('YES', 'NO'):
            raise ValueError('Only computed conditional source receipts are projected.')
        if not digest(receipt['source_sha256']) or not digest(receipt['contract_canonical_sha256']):
            raise ValueError('Invalid source hashes.')
        if (not exact(receipt['declared_model'], 'name mean between within assumptions') or
                not all(text(receipt['declared_model'][k]) for k in ('name', 'mean', 'between', 'within')) or
                not isinstance(receipt['declared_model']['assumptions'], list) or
                not all(text(x) for x in receipt['declared_model']['assumptions']) or
                not exact(receipt['criterion'], 'operator threshold') or receipt['criterion']['operator'] != 'at_most' or
                not text(receipt['criterion']['threshold']) or
                not exact(receipt['variance'], 'numerator denominator decimal_approximation display_precision_digits') or
                not all(text(receipt['variance'][k]) for k in ('numerator', 'denominator', 'decimal_approximation')) or
                type(receipt['variance']['display_precision_digits']) is not int or
                not all(text(receipt[k]) for k in ('entity', 'scope', 'formula', 'count_product', 'interpretation')) or
                not isinstance(receipt['reason_codes'], list) or not all(text(x) for x in receipt['reason_codes']) or
                not exact(receipt['bound_fields'], 'soil_count per_soil_observations') or
                any(not exact(v, 'state value quote') or v['state'] not in ('known', 'observed') or
                    not text(v['value']) or not text(v['quote']) for v in receipt['bound_fields'].values())):
            raise ValueError('Unsupported conditional source projection shape.')
        if 'contract_input_sha256' in receipt and not digest(receipt['contract_input_sha256']):
            raise ValueError('Invalid contract-input hash.')
        return {'kind': 'reported_conditional_answer', **{k: receipt[k] for k in
                ('claim_id', 'entity', 'scope', 'answer', 'criterion', 'declared_model', 'variance', 'interpretation')}}, {'source': receipt['source_sha256']}
    if receipt['ruleset'] != 'stored-run-audit-0.1':
        raise ValueError('Unsupported receipt ruleset.')
    required = common | set('identity contract_sha256 sources summary rows'.split())
    if not required <= receipt.keys() or set(receipt) - required - {'contract_input_sha256'}:
        raise ValueError('Unsupported audit receipt fields.')
    if (receipt['status'], receipt['stage']) != ('computed', 'cohort_summary'):
        raise ValueError('Only computed audit cohorts are projected.')
    if not exact(receipt['identity'], 'family facet cycle arm') or not all(text(v) for v in receipt['identity'].values()):
        raise ValueError('Invalid audit identity.')
    if not exact(receipt['sources'], 'raw keys') or not all(digest(v) for v in receipt['sources'].values()) or not digest(receipt['contract_sha256']):
        raise ValueError('Invalid audit source hashes.')
    if 'contract_input_sha256' in receipt and not digest(receipt['contract_input_sha256']):
        raise ValueError('Invalid contract-input hash.')
    summary, rows = receipt['summary'], receipt['rows']
    if not exact(summary, 'calls label_matches match_fraction constant_yes_matches labels stops input_tokens output_tokens') or not isinstance(rows, list):
        raise ValueError('Invalid audit summary.')
    if not rows or any(not exact(r, 'run_id label expected label_match') for r in rows):
        raise ValueError('Invalid audit rows.')
    if any(not text(r['run_id']) or r['label'] not in ('YES', 'NO', 'WITHHOLD', 'UNRESOLVED') or r['expected'] not in ('YES', 'NO', 'WITHHOLD') or type(r['label_match']) is not bool or r['label_match'] != (r['label'] == r['expected']) for r in rows):
        raise ValueError('Invalid row identity, label or match.')
    if len({r['run_id'] for r in rows}) != len(rows):
        raise ValueError('Duplicate run ID.')
    for key in ('calls', 'label_matches', 'constant_yes_matches', 'input_tokens', 'output_tokens'):
        if type(summary[key]) is not int or summary[key] < 0:
            raise ValueError('Invalid summary count.')
    labels = dict(Counter(r['label'] for r in rows))
    matches = sum(r['label_match'] for r in rows)
    fraction = summary['match_fraction']
    stops = summary['stops']
    if (summary['calls'] != len(rows) or summary['label_matches'] != matches or
            summary['constant_yes_matches'] != sum(r['expected'] == 'YES' for r in rows) or
            summary['labels'] != labels or not exact(fraction, 'numerator denominator') or
            any(type(fraction[k]) is not int for k in fraction) or fraction['denominator'] <= 0 or
            fraction['numerator'] * len(rows) != matches * fraction['denominator'] or
            not isinstance(stops, dict) or not stops or
            any(not text(k) or type(v) is not int or v < 0 for k, v in stops.items()) or sum(stops.values()) != len(rows)):
        raise ValueError('Audit summary/rows are inconsistent.')
    return {'kind': 'reported_exact_label_cohort', 'claim_id': receipt['claim_id'],
            'identity': receipt['identity'], 'summary': summary,
            'unresolved_outputs': labels.get('UNRESOLVED', 0)}, receipt['sources']


def build(manifest, root, manifest_sha256=None):
    out = {'ruleset': RULESET, 'tool_sha256': sha(Path(__file__).read_bytes()),
           'json_loader_sha256': sha(Path(__file__).with_name('evidence_threshold.py').read_bytes()),
           'manifest_sha256': manifest_sha256, 'status': 'unresolved', 'stations': [],
           'ancestry_warnings': [], 'limitations': LIMITATIONS}
    if not exact(manifest, 'registry_id stations') or not text(manifest['registry_id']) or not isinstance(manifest['stations'], list) or not 1 <= len(manifest['stations']) <= 64:
        out['reason'] = 'Unsupported manifest schema or station count.'
        return out
    entries = manifest['stations']
    fields = 'station_id question recipe state receipt ancestry'
    if any(not exact(e, fields) or not all(text(e[k]) for k in ('station_id', 'question', 'recipe', 'state')) or not isinstance(e['ancestry'], list) or len(e['ancestry']) > 32 for e in entries):
        out['reason'] = 'Unsupported station declarations.'
        return out
    if len({e['station_id'] for e in entries}) != len(entries):
        out['reason'] = 'Duplicate station IDs.'
        return out
    try:
        root = Path(root).resolve(strict=True)
        if not root.is_dir():
            raise ValueError('Root is not a directory.')
    except (ValueError, OSError, RuntimeError):
        out['reason'] = 'Invalid root.'
        return out
    out['registry_id'] = manifest['registry_id']
    shared = defaultdict(list)
    for entry in entries:
        station = {k: entry[k] for k in ('station_id', 'question', 'recipe', 'state')}
        station.update(status='unresolved', receipt_reference=entry['receipt'], ancestry=[])
        out['stations'].append(station)
        try:
            data = read_bound(entry['receipt'], root)
            station['receipt_bytes_bound'] = True
            receipt = load_json(data)
            station['reported_receipt'] = receipt
            projection, source_hashes = summarize(receipt)
            station['scoped_summary'] = projection
            station['reported_source_hashes'] = source_hashes
            for role, value in source_hashes.items():
                shared[value].append({'station_id': entry['station_id'], 'role': 'reported_' + role})
            shared[sha(data)].append({'station_id': entry['station_id'], 'role': 'receipt_bytes'})
            for ancestry in entry['ancestry']:
                if not exact(ancestry, 'role path sha256') or not text(ancestry['role']):
                    raise ValueError('Unsupported ancestry reference.')
                read_bound({k: ancestry[k] for k in ('path', 'sha256')}, root)
                station['ancestry'].append({**ancestry, 'bytes_bound': True, 'link_status': 'caller_declared'})
                shared[ancestry['sha256']].append({'station_id': entry['station_id'], 'role': ancestry['role']})
            station['status'] = 'indexed'
        except (ValueError, TypeError, UnicodeDecodeError, OSError, RuntimeError) as exc:
            station['reason'] = str(exc)
    for value, uses in sorted(shared.items()):
        if len({x['station_id'] for x in uses}) > 1:
            out['ancestry_warnings'].append({'code': 'shared_hash_observed', 'sha256': value, 'uses': uses,
                'meaning': 'Shared byte identity or reported hash; ancestry links are declared. Do not count as independent confirmation.'})
    out['status'] = 'indexed' if all(s['status'] == 'indexed' for s in out['stations']) else 'partial_unresolved'
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest')
    parser.add_argument('--root', required=True)
    args = parser.parse_args()
    try:
        with Path(args.manifest).open('rb') as stream:
            data = stream.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise ValueError('Manifest exceeds one MiB.')
        result = build(load_json(data), args.root, sha(data))
    except (ValueError, UnicodeDecodeError, OSError, RuntimeError) as exc:
        result = {'ruleset': RULESET, 'status': 'unresolved', 'reason': str(exc)}
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0 if result['status'] == 'indexed' else 2


if __name__ == '__main__':
    raise SystemExit(main())
