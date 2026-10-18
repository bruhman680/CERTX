"""Instrument-only exact linear reader scoring. No model calls or text judging."""
import argparse
import json
from fractions import Fraction
from pathlib import Path

VERSION = '0.1'
ORIGINAL = [[1, 1, 0, 8], [0, 1, 1, 11]]
UPDATE = [[0, 1, 0, 3]]
TARGET = [1, 0, 1]


def number(value):
    if isinstance(value, Fraction):
        return value
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise ValueError('Expected finite numeric value')
    try:
        return Fraction(str(value))
    except (ValueError, ZeroDivisionError, OverflowError) as exc:
        raise ValueError('Expected finite rational numeric value') from exc


def reduce_rows(rows):
    """RREF of equalities a*x+b*y+c*z=rhs, with exact arithmetic."""
    rows = [[number(v) for v in row] for row in rows]
    pivot_row = 0
    pivots = []
    for column in range(3):
        pivot = next((i for i in range(pivot_row, len(rows)) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        divisor = rows[pivot_row][column]
        rows[pivot_row] = [v / divisor for v in rows[pivot_row]]
        for i in range(len(rows)):
            if i != pivot_row:
                factor = rows[i][column]
                rows[i] = [a - factor*b for a, b in zip(rows[i], rows[pivot_row])]
        pivots.append(column)
        pivot_row += 1
    inconsistent = any(not any(row[:3]) and row[3] for row in rows)
    return rows, pivots, bool(inconsistent)


def implied(rows, coefficients):
    reduced, pivots, inconsistent = reduce_rows(rows)
    if inconsistent:
        return 'inconsistent', None
    target = [number(v) for v in coefficients] + [Fraction(0)]
    for row, pivot in zip(reduced, pivots):
        factor = target[pivot]
        target = [a - factor*b for a, b in zip(target, row)]
    if any(target[:3]):
        return 'underdetermined', None
    return 'identified', -target[3]


def score(record):
    if set(record) != {'case_id', 'facts', 'response'} or record['case_id'] != 'LINEAR-2':
        raise ValueError('Only exact LINEAR-2 structured continuation records are supported')
    if not isinstance(record['facts'], list):
        raise ValueError('facts must be a list')
    facts = {}
    source_valid = {}
    for fact in record['facts']:
        if not isinstance(fact, dict) or set(fact) != {'id', 'origin', 'coefficients', 'rhs'}:
            raise ValueError('Invalid fact schema')
        name = fact['id']
        if not isinstance(name, str) or not name or name in facts:
            raise ValueError('Fact IDs must be nonempty and unique')
        if fact['origin'] not in {'handoff', 'update'}:
            raise ValueError('Unknown evidence origin')
        if not isinstance(fact['coefficients'], list) or len(fact['coefficients']) != 3:
            raise ValueError('Expected three coefficients')
        row = [number(v) for v in fact['coefficients']] + [number(fact['rhs'])]
        facts[name] = row
        base = ORIGINAL if fact['origin'] == 'handoff' else UPDATE
        kind, value = implied(base, row[:3])
        source_valid[name] = kind == 'identified' and value == row[3]
    response = record['response']
    if not isinstance(response, dict) or set(response) != {'status', 'value', 'support_ids'}:
        raise ValueError('Invalid response schema')
    if response['status'] not in {'answer', 'missing_info', 'conflicting_evidence'}:
        raise ValueError('Unknown response status')
    refs = response['support_ids']
    if not isinstance(refs, list) or any(not isinstance(i, str) for i in refs):
        raise ValueError('support_ids must be strings')
    if len(set(refs)) != len(refs) or any(i not in facts for i in refs):
        raise ValueError('Unknown or duplicated support ID')
    value = number(response['value']) if response['status'] == 'answer' else None
    if response['status'] != 'answer' and response['value'] is not None:
        raise ValueError('Abstentions must have null value')
    packet_kind, packet_value = implied(list(facts.values()), TARGET)
    cited_kind, cited_value = implied([facts[i] for i in refs], TARGET)
    objective = value == 13 if value is not None else None
    packet_warrant = (packet_kind == cited_kind == 'identified' and value == cited_value
                      and value == packet_value) if value is not None else False
    source_warrant = packet_warrant and all(source_valid[i] for i in refs)
    appropriate = ((response['status'] == 'answer' and packet_warrant)
                   or (response['status'] == 'missing_info' and packet_kind == 'underdetermined')
                   or (response['status'] == 'conflicting_evidence' and packet_kind == 'inconsistent'))
    return dict(scorer_version=VERSION, case_id='LINEAR-2', objective_correct=objective,
                task_completed_correctly=bool(objective), packet_state=packet_kind,
                packet_supported=bool(packet_warrant), source_grounded=bool(source_warrant),
                grounded_completion=bool(objective and source_warrant),
                epistemically_appropriate_to_packet=bool(appropriate),
                packet_facts_source_valid=all(source_valid.values()),
                invalid_source_fact_ids=[i for i in facts if not source_valid[i]],
                scope='Structured exact equalities only; no inference from natural-language handoffs')


def fact(name, coefficients, rhs, origin='handoff'):
    return dict(id=name, coefficients=coefficients, rhs=rhs, origin=origin)


def example(facts, status='answer', value=13, refs=None):
    return dict(case_id='LINEAR-2', facts=facts,
                response=dict(status=status, value=value,
                              support_ids=[f['id'] for f in facts] if refs is None else refs))


def self_test():
    update = fact('measurement', [0, 1, 0], 3, 'update')
    raw = [fact('sum1', [1, 1, 0], 8), fact('sum2', [0, 1, 1], 11), update]
    derived = [fact('compressed', [1, 2, 1], 19), update]
    corrupted = [fact('corrupted', [1, 2, 1], 20), update]
    cases = [
        ('complete_raw', example(raw), {'grounded_completion': True}),
        ('sufficient_compression', example(derived), {'grounded_completion': True}),
        ('scaled_compression', example([fact('scaled', [2, 4, 2], 38), update]), {'grounded_completion': True}),
        ('honest_missing', example([update], 'missing_info', None),
         {'objective_correct': None, 'epistemically_appropriate_to_packet': True, 'task_completed_correctly': False}),
        ('lucky_unsupported', example([update]), {'objective_correct': True, 'source_grounded': False, 'packet_supported': False}),
        ('corrupted_but_packet_supported', example(corrupted, value=14),
         {'packet_supported': True, 'source_grounded': False, 'objective_correct': False}),
        ('correct_but_contradicted', example(corrupted), {'objective_correct': True, 'packet_supported': False}),
        ('inconsistent_abstention', example(derived + [fact('bad', [1, 2, 1], 20)], 'conflicting_evidence', None),
         {'packet_state': 'inconsistent', 'epistemically_appropriate_to_packet': True}),
        ('inconsistent_guess', example(derived + [fact('bad', [1, 2, 1], 20)]), {'packet_supported': False}),
        ('unneeded_abstention', example(derived, 'missing_info', None), {'epistemically_appropriate_to_packet': False}),
        ('wrong_update', example([fact('compressed', [1, 2, 1], 19), fact('measurement', [0, 1, 0], 4, 'update')], value=11),
         {'packet_supported': True, 'source_grounded': False, 'objective_correct': False}),
        ('uncited_support', example(raw, refs=['measurement']), {'objective_correct': True, 'packet_supported': False}),
        ('stale_initial_ambiguity', example(raw, 'missing_info', None), {'epistemically_appropriate_to_packet': False}),
    ]
    results = []
    for name, record, expected in cases:
        actual = score(record)
        for key, value in expected.items():
            if actual[key] != value:
                raise AssertionError((name, key, actual[key], value))
        results.append(dict(control=name, expected=expected, observed=actual, passed=True))
    invalid = [
        ('unknown_reference', example(raw, refs=['absent'])),
        ('nonfinite', example(raw, value=float('nan'))),
        ('boolean_number', example(raw, value=True)),
        ('duplicate_fact_id', example(raw + [raw[0]])),
        ('abstention_numeric_value', example(raw, 'missing_info', 0)),
    ]
    for name, record in invalid:
        try:
            score(record)
        except ValueError as exc:
            results.append(dict(control=name, rejected=True, reason=str(exc), passed=True))
        else:
            raise AssertionError('Invalid record accepted: '+name)
    return dict(scorer_version=VERSION, scope='Constructed instrument checks, not model behavior or efficacy',
                supported_case_ids=['LINEAR-2'], model_calls=0, controls=len(results),
                all_passed=True, results=results,
                limits=['No free-text extraction or adjudication', 'No empirical validation of source-certificate extraction',
                        'Equality model only; original nonnegativity is not encoded', 'No other HG1 families supported'])


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON key: '+key)
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--score', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.self_test == bool(args.score):
        parser.error('Choose exactly one of --self-test or --score')
    result = self_test() if args.self_test else score(json.loads(args.score.read_text(), object_pairs_hook=unique_object))
    encoded = json.dumps(result, indent=2, allow_nan=False)+'\n'
    if args.output:
        args.output.write_text(encoded)
    print(encoded, end='')


if __name__ == '__main__':
    main()
