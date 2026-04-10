"""
Experiment 015b: CERTX Wrapper Prompt Example
============================================

Demonstrates a concrete prompt-level wrapper flow with hidden
Reasoning Trajectory Record (RTR) updates and failure-mode interventions.
"""

import json
from exp_015_wrapper_loop_simulation import compute_cq, detect_failure_mode, apply_wrapper

INITIAL_STATE = {
    'C': 0.66,
    'E': 0.52,
    'R': 0.68,
    'T': 0.50,
    'X': 0.70,
    'D': 0.08,
}

PHASES = ['EXPANSION', 'COMPRESSION', 'STABILIZATION', 'MICRO-BREATH']


def record_rtr(step, phase, state, note, intervention=None):
    return {
        'step': step,
        'phase': phase,
        'C': round(state['C'], 3),
        'E': round(state['E'], 3),
        'R': round(state['R'], 3),
        'T': round(state['T'], 3),
        'X': round(state['X'], 3),
        'D': round(state['D'], 3),
        'CQ': round(compute_cq(state), 3),
        'note': note,
        'intervention': intervention,
    }


def synthesize_output(candidates):
    best = max(candidates, key=lambda c: c['score'])
    return best['response']


def run_wrapper_prompt_example():
    state = INITIAL_STATE.copy()
    rtr = []

    # Phase 1: EXPANSION
    candidates = [
        {'source': 'Logic', 'response': 'Summarize the prompt as a reasoning pipeline.', 'score': 0.72},
        {'source': 'Memory', 'response': 'Link the wrapper to existing CQ and drift diagnostics.', 'score': 0.68},
        {'source': 'KG', 'response': 'Frame the flow as a four-phase breathing loop.', 'score': 0.70},
    ]
    state['E'] = min(1.0, state['E'] + 0.07)
    rtr.append(record_rtr(1, 'EXPANSION', state, 'Generated three candidate perspectives.'))

    # Phase 2: COMPRESSION
    selected = synthesize_output(candidates)
    state['C'] = min(1.0, state['C'] + 0.08)
    state['E'] = max(0.20, state['E'] - 0.12)
    rtr.append(record_rtr(2, 'COMPRESSION', state, 'Pruned to invariant structure and selected the primary synthesis.'))

    # Phase 3: STABILIZATION
    state['R'] = min(1.0, state['R'] + 0.06)
    state['D'] = max(0.0, state['D'] - 0.03)
    failure_mode = detect_failure_mode(state)
    if failure_mode:
        state, intervention = apply_wrapper(state)
        rtr.append(record_rtr(3, 'STABILIZATION', state, 'Applied corrective intervention to preserve reasoning health.', intervention))
    else:
        rtr.append(record_rtr(3, 'STABILIZATION', state, 'No corrective intervention needed.', None))

    # Phase 4: MICRO-BREATH
    state['T'] = max(0.25, min(0.75, state['T']))
    state['X'] = max(0.60, min(1.0, state['X']))
    rtr.append(record_rtr(4, 'MICRO-BREATH', state, 'Confirmed homeostatic bounds and prevented pinning.'))

    polished_output = (
        'Implement the CERTX wrapper as an internal reasoning scout: generate multiple perspectives, '
        'compress to invariant structure, verify coherence, and preserve any failure trace as a learning signal '
        'while only exposing the final synthesized answer.'
    )

    print('=== CERTX Wrapper Prompt Example ===')
    print('\nPOLISHED OUTPUT:')
    print(polished_output)
    print('\nHIDDEN RTR:')
    print(json.dumps(rtr, indent=2))


if __name__ == '__main__':
    run_wrapper_prompt_example()
