"""Frozen prospective composition of generated claims, not source authentication.

Only unsigned integer cm/kg spellings are parsed. Simple sentence wrappers are
accepted syntactically; negation, quotation and entity ownership are NOT checked.
No original-record numeric fact or evaluator key enters action selection.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys

P = Path(__file__).resolve().parent
CHECKER_PATH = P.parents[1] / 'tools/evidence_threshold.py'
sys.path.insert(0, str(CHECKER_PATH.parent))
import evidence_threshold as checker

if Path(checker.__file__).resolve() != CHECKER_PATH.resolve():
    raise ImportError('Expected the local pinned threshold checker.')

CHECKER_SHA256 = checker.CHECKER_SHA256
PIPELINE_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
SIGNS = '+-\N{MINUS SIGN}\N{SMALL HYPHEN-MINUS}\N{FULLWIDTH HYPHEN-MINUS}\N{FULLWIDTH PLUS SIGN}\N{EN DASH}\N{EM DASH}'
QUANTITY = re.compile(r'(?<!\S)([0-9]+)\s+(cm|kg)(?=$|[\s.,;])')
MISSING = re.compile(r'\bMISSING\b', flags=re.IGNORECASE)
RECORD_ID = re.compile(r'[A-Za-z0-9_-]{1,80}\Z')
LIMITATIONS = [
    'Surface parsing does not check negation, quotation, entity ownership or source truth.',
    'Caller context supplies entity/unit and run association, not numeric gold repair.',
    'Checker hashes bind supplied bytes; they do not authenticate their meaning.',
    'Unusable extraction is infrastructure withholding, not proof of missing evidence.',
]


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _surface_claims(text, unit):
    """Return measured quantities and explicit MISSING token positions, or reason."""
    if not isinstance(text, str) or unit not in {'cm', 'kg'}:
        return None, 'Unsupported text or literal unit.'
    stripped = text.strip()
    if not stripped or len(stripped) > 4096:
        return None, 'Empty or overlong generated text.'
    if re.search('[' + re.escape(SIGNS) + r']\s*[0-9]', stripped):
        return None, 'Signed numeric spellings are unsupported.'
    quantities = list(QUANTITY.finditer(stripped))
    if re.findall(r'[0-9]+', stripped) != [m.group(1) for m in quantities]:
        return None, 'A numeric expression lacks the supported integer/unit form.'
    if any(m.group(2) != unit for m in quantities):
        return None, 'A quantity has the wrong literal unit.'
    # Reject suffixes such as cm/s, cm^2 or kg2 by the quantity-boundary rule.
    events = [(m.start(), {'state': 'measured', 'value': m.group(1)}) for m in quantities]
    events.extend((m.start(), {'state': 'missing'}) for m in MISSING.finditer(stripped))
    events.sort(key=lambda x: x[0])
    if not events:
        return None, 'No supported quantity or literal MISSING token.'
    return [obs for _, obs in events], None


def parse_measurements(text, unit):
    observations, reason = _surface_claims(text, unit)
    return {'usable': observations is not None, 'observations': observations, 'reason': reason}


def parse_minimum(text, unit):
    observations, reason = _surface_claims(text, unit)
    if observations is None:
        return {'usable': False, 'value': None, 'reason': reason}
    if len(observations) != 1 or observations[0]['state'] != 'measured':
        return {'usable': False, 'value': None,
                'reason': 'Minimum needs exactly one measured quantity and no MISSING token.'}
    return {'usable': True, 'value': observations[0]['value'], 'reason': None}


def compute_pair(measurement_text, minimum_text, entity, unit, record_id, artifactroot):
    """Compute a conditional action using only generated numeric claims.

    Writes one new evidence file with exclusive creation. Repeating a record ID
    in the same directory raises FileExistsError rather than replacing history.
    Parser or checker failures withhold action as UNKNOWN, with explicit stage.
    """
    out = {'record_id': record_id, 'measurement_text': measurement_text,
           'minimum_text': minimum_text, 'action': 'UNKNOWN',
           'stage': 'invalid_pipeline_context', 'receipt': None, 'contract': None,
           'checker_sha256': CHECKER_SHA256, 'pipeline_sha256': PIPELINE_SHA256,
           'limitations': LIMITATIONS[:], 'artifact_path': None}
    if (not isinstance(entity, str) or not entity.strip() or len(entity) > 256 or
            unit not in {'cm', 'kg'} or not isinstance(record_id, str) or
            not RECORD_ID.fullmatch(record_id)):
        out['reason'] = 'Unsupported entity, unit or record identifier.'
        return out
    if _sha(CHECKER_PATH) != CHECKER_SHA256:
        out.update(stage='checker_changed', reason='Checker file differs from loaded source snapshot.')
        return out
    measurement = parse_measurements(measurement_text, unit)
    minimum = parse_minimum(minimum_text, unit)
    out.update(parsed_measurements=measurement, parsed_minimum=minimum)
    if not measurement['usable'] or not minimum['usable']:
        out.update(stage='extraction_unusable',
                   reason='A generated field cannot be represented by the frozen surface parser.')
        return out
    root = Path(artifactroot)
    root.mkdir(parents=True, exist_ok=True)
    artifact = {'entity': entity, 'scope': 'prospective-generated-claims-' + record_id,
                'unit': unit, 'observations': measurement['observations']}
    artifact_path = root / (record_id + '.json')
    with artifact_path.open('x', encoding='utf-8') as stream:
        json.dump(artifact, stream, indent=2)
        stream.write('\n')
    contract = {
        'claim_id': record_id + '-generated-pair-at-least', 'entity': entity,
        'scope': artifact['scope'],
        'criterion': {'id': record_id + '-generated-minimum', 'operator': 'at_least',
                      'unit': unit, 'minimum': minimum['value']},
        'evidence': {'path': artifact_path.name, 'sha256': _sha(artifact_path)},
    }
    receipt = checker.assess(contract, root)
    out.update(contract=contract, receipt=receipt, artifact_path=str(artifact_path),
               stage=receipt['stage'],
               action={'supported': 'YES', 'contradicted': 'NO', 'unresolved': 'UNKNOWN'}[receipt['verdict']],
               reason='Conditional result from generated structured claims; original source facts not checked.')
    return out
