"""Optional complete conditional path for one declared soil-count source grammar.

Source bytes -> role/state binding -> model/domain checks -> exact variance ->
at-most answer. Neither source authenticity nor statistical assumptions are
established by this program. Trusted local workspace, not a hardened service.
"""
from __future__ import annotations
import argparse
from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import evidence_threshold as strict_json

RULESET = 'source-calculation-path-0.1'
MAX_BYTES = 65_536
ASSUMPTIONS = ['independent_soil_draws', 'equal_observations_per_soil', 'conditional_iid_emissions']
TOKEN = r'(?:[0-9]{1,9}|[A-Za-z]+(?:-[A-Za-z]+)?)'
IDENT = r'[A-Za-z][A-Za-z0-9_-]{0,63}'
TOOL_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
LOADER_SHA256 = hashlib.sha256(Path(strict_json.__file__).read_bytes()).hexdigest()
_NO_PROPOSAL = object()
LIMITATIONS = [
    'Full declared source grammar only; unsupported content withholds.',
    'Hashes bind bytes, not source authenticity, truth, or real independence.',
    'Model assumptions are caller-declared, not empirically verified.',
    'Exact arithmetic does not establish source extraction beyond the declared grammar.',
    'Local trusted workspace only; source hashes are not runtime/bytecode authentication.',
]


def _keys(x, names):
    return isinstance(x, dict) and set(x) == set(names)


def _count(token):
    if re.fullmatch(r'[0-9]{1,9}', token):
        return str(int(token))
    small = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
             'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
    tens = {'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50, 'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90}
    t = token.lower()
    if t in small:
        return str(small.index(t))
    if t in tens:
        return str(tens[t])
    parts = t.split('-')
    if len(parts) == 2 and parts[0] in tens and parts[1] in small[1:10]:
        return str(tens[parts[0]] + small.index(parts[1]))
    raise ValueError('Unsupported count token.')


def _decimal(x):
    if not isinstance(x, str) or not re.fullmatch(r'[0-9]{1,16}(?:\.[0-9]{1,16})?', x):
        raise ValueError('Expected bounded nonnegative ordinary decimal string.')
    return Fraction(x)


def _field(state, value, quote):
    return {'state': state, 'value': value, 'quote': quote}


def _parse_body(body):
    firsts = [
        (r'There are (?P<n>' + TOKEN + r') independently sampled soils\.', 'known'),
        (r'(?P<n>' + TOKEN + r') soils were sampled independently\.', 'known'),
        (r'There are independently sampled soils, but their number was not recorded\.', 'missing'),
        (r'Some soils were sampled independently, but their number was not recorded\.', 'missing'),
    ]
    match = None
    for pattern, state in firsts:
        m = re.match(pattern, body)
        if m:
            match = m
            k = _field(state, _count(m['n']) if state == 'known' else None, m.group(0))
            break
    if match is None:
        raise ValueError('Independent-soil clause unsupported.')
    rest = body[match.end():]
    if not rest:
        return {'soil_count': k, 'per_soil_observations': _field('absent', None, None)}
    if not re.match(r'[ \t]+', rest):
        raise ValueError('Unexpected clause boundary.')
    clause = rest.lstrip(' \t')
    seconds = [
        (r'Each soil supplies (?P<n>' + TOKEN + r') observations\.', 'observed'),
        (r'Each soil supplied (?P<n>' + TOKEN + r') observations\.', 'observed'),
        (r'Observations per soil were not recorded\.', 'missing'),
        (r'(?P<n>' + TOKEN + r') observations per soil were planned, but none were collected\.', 'planned'),
    ]
    for pattern, state in seconds:
        m = re.fullmatch(pattern, clause)
        if m:
            obs = _field(state, _count(m['n']) if state != 'missing' else None, m.group(0))
            return {'soil_count': k, 'per_soil_observations': obs}
    raise ValueError('Observation clause unsupported or extra content present.')


def _base(mode):
    return {'ruleset': RULESET, 'tool_sha256': TOOL_SHA256, 'json_loader_sha256': LOADER_SHA256,
            'mode': mode, 'status': 'withheld', 'stage': 'invalid_contract', 'answer': None,
            'reason_codes': [], 'limitations': LIMITATIONS[:]}


def evaluate(contract, root, proposal=_NO_PROPOSAL):
    out = _base('deterministic_source' if proposal is _NO_PROPOSAL else 'witnessed_proposal')

    def stop(stage, *reasons):
        out.update(stage=stage, reason_codes=list(reasons))
        return out

    try:
        if hashlib.sha256(Path(__file__).read_bytes()).hexdigest() != TOOL_SHA256 or hashlib.sha256(Path(strict_json.__file__).read_bytes()).hexdigest() != LOADER_SHA256:
            return stop('implementation_changed', 'loaded_source_snapshot_changed')
    except OSError:
        return stop('implementation_changed', 'implementation_source_unavailable')
    if not _keys(contract, ['claim_id', 'entity', 'scope', 'source', 'model', 'criterion']):
        return stop('invalid_contract', 'contract_schema')
    if not isinstance(contract['claim_id'], str) or not contract['claim_id'].strip() or len(contract['claim_id']) > 128:
        return stop('invalid_contract', 'claim_id')
    if any(not isinstance(contract[k], str) or re.fullmatch(IDENT, contract[k]) is None for k in ['entity', 'scope']):
        return stop('invalid_contract', 'entity_or_scope')
    src, model, criterion = contract['source'], contract['model'], contract['criterion']
    if not _keys(src, ['path', 'sha256']) or not isinstance(src['path'], str) or not src['path'] or len(src['path']) > 512 or not isinstance(src['sha256'], str) or not re.fullmatch(r'[0-9a-f]{64}', src['sha256']):
        return stop('invalid_contract', 'source_binding_schema')
    if not _keys(model, ['name', 'mean', 'between', 'within', 'assumptions']) or model['name'] != 'equal_cluster_bernoulli_mixture' or model['assumptions'] != ASSUMPTIONS:
        return stop('invalid_model', 'model_or_assumption_declaration')
    if not _keys(criterion, ['operator', 'threshold']) or criterion['operator'] != 'at_most':
        return stop('invalid_contract', 'criterion_schema')
    try:
        mean, between, within = (_decimal(model[k]) for k in ['mean', 'between', 'within'])
        threshold = _decimal(criterion['threshold'])
    except (ValueError, TypeError, ZeroDivisionError):
        return stop('invalid_contract', 'numeric_contract_value')
    if not 0 <= mean <= 1 or between + within != mean * (1 - mean):
        return stop('invalid_model', 'bernoulli_variance_decomposition')
    out.update(claim_id=contract['claim_id'], entity=contract['entity'], scope=contract['scope'],
               contract_canonical_sha256=hashlib.sha256(json.dumps(contract, sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
               declared_model=model.copy(), criterion=criterion.copy())
    try:
        base = Path(root).resolve()
        relative = Path(src['path'])
        if not base.is_dir() or relative.is_absolute():
            return stop('source_unavailable', 'artifact_root_or_relative_path')
        path = (base / relative).resolve()
        if not path.is_relative_to(base):
            return stop('source_unavailable', 'source_path_outside_root')
        with path.open('rb') as stream:
            data = stream.read(MAX_BYTES + 1)
    except (OSError, TypeError, ValueError, RuntimeError):
        return stop('source_unavailable', 'source_read_failed')
    if len(data) > MAX_BYTES:
        return stop('unsupported_source', 'source_size_limit')
    actual = hashlib.sha256(data).hexdigest()
    out['source_sha256'] = actual
    if actual != src['sha256']:
        return stop('source_hash_mismatch', 'expected_source_bytes_differ')
    try:
        text = data.decode('utf-8').strip()
    except UnicodeDecodeError:
        return stop('unsupported_source', 'source_not_utf8')
    header = re.fullmatch(r'Record (?P<entity>' + IDENT + r') / (?P<scope>' + IDENT + r')\.\r?\n(?P<body>.+)', text, re.S)
    if header is None:
        return stop('unsupported_source', 'record_header_or_complete_source_grammar')
    if (header['entity'], header['scope']) != (contract['entity'], contract['scope']):
        return stop('identity_mismatch', 'source_entity_or_scope_differs')
    try:
        fields = _parse_body(header['body'])
    except ValueError:
        return stop('unsupported_source', 'complete_count_grammar_not_supported')
    out['bound_fields'] = fields
    if proposal is not _NO_PROPOSAL:
        if not _keys(proposal, ['entity', 'scope', 'source_sha256', 'fields']):
            return stop('invalid_proposal', 'proposal_schema')
        if (proposal['entity'], proposal['scope'], proposal['source_sha256']) != (contract['entity'], contract['scope'], actual):
            return stop('proposal_binding_mismatch', 'proposal_identity_or_source')
        if not _keys(proposal['fields'], ['soil_count', 'per_soil_observations']):
            return stop('invalid_proposal', 'proposal_field_schema')
        for key in fields:
            if not _keys(proposal['fields'][key], ['state', 'value', 'quote']) or proposal['fields'][key] != fields[key]:
                return stop('proposal_binding_mismatch', 'proposed_role_state_value_or_quote_' + key)
    missing = [key for key, f in fields.items() if f['state'] in ['missing', 'absent']]
    if missing:
        return stop('source_missing', *['missing_' + key for key in missing])
    k, m = int(fields['soil_count']['value']), int(fields['per_soil_observations']['value'])
    domain = []
    if k == 0:
        domain.append('zero_soil_count')
    if m == 0:
        domain.append('zero_observations_per_soil')
    if fields['per_soil_observations']['state'] == 'planned':
        domain.append('planned_not_observed')
    if domain:
        return stop('outside_domain', *domain)
    value = between / k + within / (k * m)
    with localcontext() as ctx:
        ctx.prec = 32
        display = str(Decimal(value.numerator) / Decimal(value.denominator))
    out.update(status='computed', stage='conditional_answer', answer='YES' if value <= threshold else 'NO',
               reason_codes=['source_roles_bound', 'declared_model_and_positive_count_domain', 'exact_at_most_comparison'],
               formula='between/k + within/(k*m)',
               variance={'numerator': str(value.numerator), 'denominator': str(value.denominator), 'decimal_approximation': display, 'display_precision_digits': 32},
               count_product=str(k * m),
               interpretation='Answer conditional on the supplied model, source grammar and declared assumptions; not empirical truth verification.')
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('contract', type=Path)
    p.add_argument('--root', type=Path, required=True)
    p.add_argument('--proposal', type=Path)
    args = p.parse_args()
    try:
        with args.contract.open('rb') as stream:
            data = stream.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise ValueError('Contract exceeds size limit.')
        contract = strict_json.load_json(data)
    except (OSError, UnicodeDecodeError, ValueError):
        out = _base('deterministic_source')
        out.update(stage='invalid_contract', reason_codes=['contract_file_not_strict_bounded_json'])
        print(json.dumps(out, indent=2))
        return
    kwargs = {}
    if args.proposal is not None:
        try:
            with args.proposal.open('rb') as stream:
                proposal_data = stream.read(MAX_BYTES + 1)
            if len(proposal_data) > MAX_BYTES:
                raise ValueError('Proposal exceeds size limit.')
            kwargs['proposal'] = strict_json.load_json(proposal_data)
        except (OSError, UnicodeDecodeError, ValueError):
            out = _base('witnessed_proposal')
            out.update(stage='invalid_proposal', reason_codes=['proposal_file_not_strict_bounded_json'])
            print(json.dumps(out, indent=2))
            return
    out = evaluate(contract, args.root, **kwargs)
    out['contract_input_sha256'] = hashlib.sha256(data).hexdigest()
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
