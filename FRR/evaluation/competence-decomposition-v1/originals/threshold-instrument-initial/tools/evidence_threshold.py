"""Optional source-bound at-least comparison over explicitly structured evidence.

No natural-language extraction, source authentication or model confidence. JSON
syntax and hash identity cannot establish empirical truth. Local trusted workspace
scope only; this is separate from FRR verification-layer adapter versions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path
import re

RULESET = 'evidence-threshold-0.1'
MAX_ARTIFACT_BYTES = 1_048_576
DECIMAL = re.compile(r'[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)\Z')
CHECKER_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def _text(value):
    return isinstance(value, str) and bool(value.strip()) and len(value) <= 256


def _decimal(value):
    # bool is an int subclass. Floats are deliberately excluded, even finite ones.
    if type(value) is int:
        value = str(value)
    if not isinstance(value, str) or len(value) > 128 or not DECIMAL.fullmatch(value):
        raise ValueError('Expected an ordinary finite decimal string or integer.')
    try:
        number = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError('Invalid decimal.') from exc
    if not number.is_finite():
        raise ValueError('Nonfinite decimal.')
    return number


def _keys(value, names):
    return isinstance(value, dict) and set(value) == set(names)


def _strict_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON field.')
        result[key] = value
    return result


def _reject_constant(value):
    raise ValueError('Nonfinite JSON constant: ' + value)


def load_json(data):
    """Strict JSON object parsing; duplicates and nonfinite constants are rejected."""
    return json.loads(data, object_pairs_hook=_strict_pairs, parse_constant=_reject_constant)


def assess(contract, root):
    """Return a scoped receipt. Invalid contracts never reach evidence assessment."""
    out = {'ruleset': RULESET, 'checker_sha256': CHECKER_SHA256,
           'verdict': 'unresolved', 'stage': 'invalid_contract', 'reasons': [],
           'binding': {'artifact_sha256': False, 'entity_scope_unit': False},
           'limitations': ['Structured facts are supplied, not extracted or authenticated.',
                           'No implicit unit conversion or conflict-resolution rule.']}
    if not _keys(contract, ['claim_id', 'entity', 'scope', 'criterion', 'evidence']):
        out['reasons'].append('Contract fields do not match the supported schema.')
        return out
    if not all(_text(contract[k]) for k in ['claim_id', 'entity', 'scope']):
        out['reasons'].append('Claim, entity and scope must be nonempty literal strings.')
        return out
    criterion, evidence = contract['criterion'], contract['evidence']
    if not _keys(criterion, ['id', 'operator', 'unit', 'minimum']) or not all(
            _text(criterion[k]) for k in ['id', 'unit']) or criterion['operator'] != 'at_least':
        out['reasons'].append('Only an explicitly identified at_least criterion is supported.')
        return out
    if (not _keys(evidence, ['path', 'sha256']) or not _text(evidence['path']) or
            not isinstance(evidence['sha256'], str) or
            not re.fullmatch(r'[0-9a-f]{64}', evidence['sha256'])):
        out['reasons'].append('Evidence needs a relative path and lowercase SHA256.')
        return out
    try:
        minimum = _decimal(criterion['minimum'])
        root_path = Path(root).resolve(strict=True)
        relative = Path(evidence['path'])
        if not root_path.is_dir() or relative.is_absolute():
            raise ValueError('Root must be a directory and evidence path relative.')
        path = (root_path / relative).resolve()
        if not path.is_relative_to(root_path):
            raise ValueError('Evidence path escapes the supplied root.')
        canonical = json.dumps(contract, sort_keys=True, separators=(',', ':'), allow_nan=False)
    except (ValueError, TypeError, OSError, RuntimeError):
        out['reasons'].append('Invalid numeric criterion, evidence root, relative path or JSON contract.')
        return out
    out.update(claim_id=contract['claim_id'], entity=contract['entity'], scope=contract['scope'],
               criterion_id=criterion['id'], contract_sha256=hashlib.sha256(canonical.encode()).hexdigest())
    out['stage'] = 'evidence_unavailable'
    try:
        with path.open('rb') as stream:
            data = stream.read(MAX_ARTIFACT_BYTES + 1)
    except OSError:
        out['reasons'].append('Bound evidence file could not be read.')
        return out
    if len(data) > MAX_ARTIFACT_BYTES:
        out['stage'] = 'invalid_evidence'
        out['reasons'].append('Evidence exceeds the one MiB input bound.')
        return out
    actual_hash = hashlib.sha256(data).hexdigest()
    out['artifact_sha256'] = actual_hash
    out['stage'] = 'artifact_mismatch'
    if actual_hash != evidence['sha256']:
        out['reasons'].append('Evidence bytes do not match the declared SHA256.')
        return out
    out['binding']['artifact_sha256'] = True
    out['stage'] = 'invalid_evidence'
    try:
        artifact = load_json(data)
    except (ValueError, UnicodeDecodeError):
        out['reasons'].append('Bound bytes are not supported strict JSON.')
        return out
    if not _keys(artifact, ['entity', 'scope', 'unit', 'observations']):
        out['reasons'].append('Evidence fields do not match the supported schema.')
        return out
    out['stage'] = 'identity_mismatch'
    if (artifact['entity'], artifact['scope'], artifact['unit']) != (
            contract['entity'], contract['scope'], criterion['unit']):
        out['reasons'].append('Literal entity, scope or unit differs from the contract.')
        return out
    out['binding']['entity_scope_unit'] = True
    out['stage'] = 'invalid_evidence'
    observations = artifact['observations']
    if not isinstance(observations, list):
        out['reasons'].append('Observations must be a list.')
        return out
    measured, missing = [], 0
    for obs in observations:
        if _keys(obs, ['state']) and obs['state'] == 'missing':
            missing += 1
        elif _keys(obs, ['state', 'value']) and obs['state'] == 'measured':
            try:
                measured.append(_decimal(obs['value']))
            except ValueError:
                out['reasons'].append('Measured value is not a supported finite decimal.')
                return out
        else:
            out['reasons'].append('Observation is neither explicit missing nor measured value.')
            return out
    out.update(observation_count=len(observations), measured_count=len(measured), missing_count=missing)
    distinct = set(measured)
    if (missing and measured) or len(distinct) > 1:
        out['stage'] = 'conflicting_measurements'
        out['reasons'].append('Conflicting values or simultaneous missing and measured records; no precedence assumed.')
        return out
    if not measured:
        out['stage'] = 'missing_measurement'
        out['reasons'].append('No measured value is supplied; missing is not zero or failure.')
        return out
    value = measured[0]
    supported = value >= minimum
    out.update(verdict='supported' if supported else 'contradicted', stage='compared',
               comparison={'value': str(value), 'operator': 'at_least', 'minimum': str(minimum),
                           'unit': criterion['unit'], 'holds': supported})
    out['reasons'].append('Comparison is conditional on the caller-supplied structured evidence and criterion.')
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('contract', type=Path)
    parser.add_argument('--root', required=True, type=Path)
    args = parser.parse_args()
    try:
        contract = load_json(args.contract.read_bytes())
    except (ValueError, UnicodeDecodeError, OSError) as exc:
        print(json.dumps({'ruleset': RULESET, 'verdict': 'unresolved', 'stage': 'invalid_contract',
                          'reasons': ['Contract could not be read as strict JSON.']}, indent=2))
        return
    print(json.dumps(assess(contract, args.root), indent=2))


if __name__ == '__main__':
    main()
