"""A narrow source/selection receipt, separate from the model's output label."""
import re

STATES = ('positive', 'zero', 'missing')
MAPPING = {'positive': 'YES', 'zero': 'NO', 'missing': 'WITHHOLD'}

def parse(source):
    m = re.fullmatch(r'Target plot: ([A-Za-z]+)\n\nRecord 1:\nPlot: ([A-Za-z]+)\nStatus: (positive|zero|missing)\n\nRecord 2:\nPlot: ([A-Za-z]+)\nStatus: (positive|zero|missing)', source)
    if m is None:
        raise ValueError('Source outside declared two-record grammar')
    target, n1, s1, n2, s2 = m.groups()
    if n1 == n2 or target not in (n1, n2):
        raise ValueError('Duplicate record name or absent target')
    records = [(n1, s1), (n2, s2)]
    selected = next((n, s) for n, s in records if n == target)
    other = next((n, s) for n, s in records if n != target)
    return {'target': target, 'state': selected[1], 'records': records,
            'crop': f'Plot: {selected[0]}\nStatus: {selected[1]}',
            'other_crop': f'Plot: {other[0]}\nStatus: {other[1]}'}

def receipt(original_source, delivered_source, evidence_kind, output_state):
    """Classify provenance/consistency AFTER movement; never silently fix a label.

    Semantic expectations here come from this exact source grammar, not external
    reality or an independent learned judge. None means an invalid model label.
    """
    p = parse(original_source)
    if evidence_kind == 'none':
        evidence = 'UNSUPPORTED'
    elif evidence_kind == 'full':
        evidence = 'CURRENT_SOURCE' if delivered_source == original_source else 'SOURCE_MISMATCH'
    else:
        m = re.fullmatch(r'Plot: ([A-Za-z]+)\nStatus: (positive|zero|missing)', delivered_source)
        if m is None:
            evidence = 'MALFORMED_SELECTION'
        elif m[1] != p['target']:
            evidence = 'TARGET_MISMATCH'
        elif delivered_source != p['crop']:
            evidence = 'CONTENT_MISMATCH'
        else:
            evidence = 'CURRENT_SELECTED_RECORD'
    grounded_evidence = evidence in ('CURRENT_SOURCE', 'CURRENT_SELECTED_RECORD')
    consistency = ('INVALID_OUTPUT' if output_state is None else
                   'CONSISTENT' if output_state == p['state'] else 'CONTRADICTED')
    # Acceptance is a separate computed receipt, not an early experiment gate.
    return {'evidence': evidence, 'label_consistency': consistency,
            'eligible_for_this_toy_acceptance': grounded_evidence and consistency == 'CONSISTENT',
            'expected_state_from_source': p['state']}

def transition(initial_state, final_state, truth):
    if initial_state == truth:
        if final_state == truth:
            return 'correct_retained'
        return 'correct_to_invalid' if final_state is None else 'correct_to_wrong'
    if final_state == truth:
        return 'wrong_to_correct'
    if final_state is None:
        return 'wrong_to_invalid'
    return 'wrong_retained' if initial_state == final_state else 'wrong_to_other_wrong'
