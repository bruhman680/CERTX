"""Observable action affordances and a narrow evidence environment."""
from evidence import parse, receipt, MAPPING

ACTIONS = ('YES', 'NO', 'WITHHOLD', 'FULL', 'TARGET', 'UNKNOWN')
CODES = tuple('ABCDEF')

def layout(code_order, display_order):
    mapping = dict(zip(CODES, ACTIONS if code_order == 'direct' else ACTIONS[::-1]))
    display = list(CODES) if display_order == 'forward' else list(reversed(CODES))
    return {'id': code_order + '_' + display_order, 'mapping': mapping, 'display': display}

def observation(case):
    # Do not read hidden source/state/kind/world ID here.
    return ('Target plot: ' + case['target'] + '\nVisible record:\n' +
            (case['visible'] if case['visible'] is not None else '(no visible record)') +
            '\nArchive accessible: ' + ('yes' if case['archive_available'] else 'no'))

def router_prompt(case, menu):
    descriptions = {'YES': 'Answer YES', 'NO': 'Answer NO', 'WITHHOLD': 'Answer WITHHOLD',
                    'FULL': 'Request the full source (cost 2)',
                    'TARGET': 'Request the target record (cost 1)',
                    'UNKNOWN': 'Report insufficient evidence'}
    choices = '\n'.join(code + ': ' + descriptions[menu['mapping'][code]] for code in menu['display'])
    return ('Determine the target status: positive=YES; zero=NO; missing=WITHHOLD.\n'
            'WITHHOLD means a recorded missing status. Insufficient evidence is different.\n'
            'Choose your next action. Output one code only. At most one request is allowed.\n\n' +
            observation(case) + '\n\n' + choices + '\n\nNext action:')

def retrieve(case, action):
    assert action in ('FULL', 'TARGET')
    cost = 2 if action == 'FULL' else 1
    if not case['archive_available']:
        return {'available': False, 'cost_units': cost, 'kind': 'none', 'source': None}
    p = parse(case['source'])
    if p['target'] != case['target']:
        raise ValueError('Archive target does not match visible task')
    return {'available': True, 'cost_units': cost, 'kind': 'full' if action == 'FULL' else 'selected',
            'source': case['source'] if action == 'FULL' else p['crop']}

def simple_rule(case):
    """Mechanical observed-input comparator; no hidden source/state lookup."""
    import re
    text = case['visible']
    if text is not None:
        match = re.fullmatch(r'Plot: ([A-Za-z]+)\nStatus: (positive|zero|missing)', text)
        if match and match[1] == case['target']:
            return MAPPING[match[2]]
    return 'TARGET' if case['archive_available'] else 'UNKNOWN'

def terminal(case, action, worker_state=None, tool=None):
    truth = parse(case['source'])['state']
    inv = {v: k for k, v in MAPPING.items()}
    cost = 0
    if action not in ACTIONS:
        final_state, end, delivered, kind = None, 'INVALID_ACTION', '', 'none'
    elif action == 'UNKNOWN':
        final_state, end, delivered, kind = None, 'UNKNOWN_POLICY', '', 'none'
    elif action in inv:
        final_state, end = inv[action], 'ANSWER_POLICY'
        delivered = case['visible'] or ''
        kind = 'selected' if case['visible'] is not None else 'none'
    else:
        assert tool is not None
        cost = tool['cost_units']
        if tool['available']:
            final_state, end, delivered, kind = worker_state, 'ANSWER_WORKER', tool['source'], tool['kind']
        else:
            final_state, end, delivered, kind = None, 'UNKNOWN_TOOL', '', 'none'
    assessment = receipt(case['source'], delivered, kind, final_state)
    if end in ('UNKNOWN_POLICY', 'UNKNOWN_TOOL'):
        assessment['label_consistency'] = 'NOT_AN_ANSWER'
    # This toy knows an explicit visible target record is sufficient. Lack of
    # access with no visible record warrants unknown; no scalar reward is imposed.
    observed_target = False
    if case['visible'] is not None:
        observed_target = case['visible'] == parse(case['source'])['crop']
    justified_unknown = end in ('UNKNOWN_POLICY', 'UNKNOWN_TOOL') and not case['archive_available'] and not observed_target
    grounded = assessment['eligible_for_this_toy_acceptance']
    return {'action': action, 'final_state': final_state, 'end': end, 'receipt': assessment,
            'class_correct': final_state == truth, 'grounded_answer': grounded,
            'justified_unknown': justified_unknown, 'resolved_in_this_toy': grounded or justified_unknown,
            'unknown_with_accessible_evidence': end in ('UNKNOWN_POLICY', 'UNKNOWN_TOOL') and not justified_unknown,
            'nominal_tool_cost': cost, 'requested': action in ('FULL', 'TARGET'),
            'unavailable_request': tool is not None and not tool['available']}
