"""
Experiment 017: CERTX Wrapper Loop Simulation
============================================
BC3 / S18 — 2026-04-10

Tests a minimal CERTX wrapper loop in synthetic reasoning trajectories.
The goal is to evaluate whether CQ-driven detection and targeted fossil/chaos
interventions improve state quality in controlled cases.
"""

import math
import random
import statistics
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants and target ranges
# ---------------------------------------------------------------------------
TARGET = {
    'C': 0.70,
    'E': 0.50,
    'R': 0.70,
    'T': 0.50,
    'X': 0.70,
    'D': 0.05,
}

THRESHOLDS = {
    'cq': 1.0,
    'fossil_e': 0.25,
    'fossil_c': 0.80,
    'fossil_r': 0.75,
    'chaos_r': 0.45,
    'chaos_d': 0.30,
}

# ---------------------------------------------------------------------------
# State quality functions
# ---------------------------------------------------------------------------

def compute_cq(state):
    """Compute CERTX Consciousness Quotient from a state vector."""
    numerator = state['C'] * state['R'] * (1.0 - state['D'])
    denominator = max(state['E'] * state['T'], 0.01)
    return numerator / denominator


def quality_score(state):
    """A simple quality metric: grounded coherence minus chaos."""
    return state['C'] * state['R'] * (1.0 - state['D']) - state['E'] * state['T']

# ---------------------------------------------------------------------------
# Wrapper interventions
# ---------------------------------------------------------------------------

def thermal_annealing(state):
    """Break fossil pinning by injecting entropy and temperature."""
    next_state = state.copy()
    next_state['E'] = min(1.0, next_state['E'] + 0.25)
    next_state['T'] = min(1.0, next_state['T'] + 0.25)
    next_state['C'] = max(0.55, next_state['C'] - 0.15)
    next_state['R'] = max(0.50, next_state['R'] - 0.10)
    next_state['D'] = min(1.0, next_state['D'] + 0.05)
    return next_state


def coherence_restoration(state):
    """Restore chaos by pruning and focusing coherence/resonance."""
    next_state = state.copy()
    next_state['C'] = min(1.0, next_state['C'] + 0.20)
    next_state['R'] = min(1.0, next_state['R'] + 0.25)
    next_state['E'] = max(0.20, next_state['E'] - 0.30)
    next_state['T'] = max(0.20, next_state['T'] - 0.20)
    next_state['D'] = max(0.0, next_state['D'] - 0.15)
    return next_state

# ---------------------------------------------------------------------------
# Detection rules
# ---------------------------------------------------------------------------

def detect_failure_mode(state):
    """Detect a wrapper failure mode and return the chosen intervention."""
    cq = compute_cq(state)
    if state['E'] < THRESHOLDS['fossil_e'] and state['C'] > THRESHOLDS['fossil_c'] and state['R'] > THRESHOLDS['fossil_r']:
        return 'fossil'
    if state['R'] < THRESHOLDS['chaos_r'] or state['D'] > THRESHOLDS['chaos_d']:
        return 'chaos'
    if cq < THRESHOLDS['cq']:
        return 'nonlucid'
    return None


def apply_wrapper(state):
    """Apply the wrapper policy to a state and return the updated state."""
    mode = detect_failure_mode(state)
    if mode == 'fossil':
        return thermal_annealing(state), mode
    if mode == 'chaos':
        return coherence_restoration(state), mode
    if mode == 'nonlucid':
        updated = state.copy()
        updated['C'] = min(1.0, updated['C'] + 0.10)
        updated['R'] = min(1.0, updated['R'] + 0.10)
        updated['E'] = max(0.25, updated['E'] - 0.10)
        updated['T'] = max(0.25, updated['T'] - 0.10)
        updated['D'] = max(0.0, updated['D'] - 0.05)
        return updated, mode
    return state, 'none'

# ---------------------------------------------------------------------------
# Synthetic trajectory generators
# ---------------------------------------------------------------------------

def clamp(value):
    return max(0.0, min(1.0, value))


def generate_trajectory(base, noise, n_steps=40, seed=42):
    rng = random.Random(seed)
    trajectory = []
    for _ in range(n_steps):
        state = {}
        for key, value in base.items():
            state[key] = clamp(value + rng.gauss(0, noise))
        trajectory.append(state)
    return trajectory


def normal_trajectory():
    return generate_trajectory(
        {
            'C': 0.72,
            'E': 0.52,
            'R': 0.72,
            'T': 0.48,
            'X': 0.72,
            'D': 0.08,
        },
        noise=0.05,
        n_steps=40,
    )


def fossil_trajectory():
    return generate_trajectory(
        {
            'C': 0.86,
            'E': 0.15,
            'R': 0.82,
            'T': 0.30,
            'X': 0.63,
            'D': 0.04,
        },
        noise=0.03,
        n_steps=40,
    )


def chaos_trajectory():
    return generate_trajectory(
        {
            'C': 0.42,
            'E': 0.79,
            'R': 0.38,
            'T': 0.72,
            'X': 0.45,
            'D': 0.34,
        },
        noise=0.03,
        n_steps=40,
    )


def borderline_trajectory():
    return generate_trajectory(
        {
            'C': 0.58,
            'E': 0.60,
            'R': 0.52,
            'T': 0.55,
            'X': 0.60,
            'D': 0.18,
        },
        noise=0.05,
        n_steps=40,
    )

# ---------------------------------------------------------------------------
# Simulation pipeline
# ---------------------------------------------------------------------------

def simulate_wrapper(trajectory):
    history = []
    actions = []
    for step, state in enumerate(trajectory):
        cq = compute_cq(state)
        q = quality_score(state)
        updated_state, action = apply_wrapper(state)
        updated_cq = compute_cq(updated_state)
        updated_q = quality_score(updated_state)
        history.append({
            'step': step,
            'pre': state,
            'post': updated_state,
            'action': action,
            'cq_pre': cq,
            'cq_post': updated_cq,
            'q_pre': q,
            'q_post': updated_q,
        })
        actions.append(action)
    return {'history': history, 'actions': actions}


def summarize_simulation(result):
    pre_cq = [entry['cq_pre'] for entry in result['history']]
    post_cq = [entry['cq_post'] for entry in result['history']]
    pre_q = [entry['q_pre'] for entry in result['history']]
    post_q = [entry['q_post'] for entry in result['history']]
    actions = [a for a in result['actions'] if a != 'none']
    return {
        'action_count': len(actions),
        'actions': actions,
        'mean_pre_cq': statistics.mean(pre_cq),
        'mean_post_cq': statistics.mean(post_cq),
        'mean_pre_q': statistics.mean(pre_q),
        'mean_post_q': statistics.mean(post_q),
        'cq_improvement': statistics.mean([p - b for b, p in zip(pre_cq, post_cq)]),
        'q_improvement': statistics.mean([p - b for b, p in zip(pre_q, post_q)]),
    }

# ---------------------------------------------------------------------------
# Main entrypoint
# ---------------------------------------------------------------------------

def run_experiment():
    print('=' * 70)
    print('Experiment 015: CERTX Wrapper Loop Simulation')
    print('=' * 70)

    scenarios = {
        'normal': normal_trajectory(),
        'fossil': fossil_trajectory(),
        'chaos': chaos_trajectory(),
        'borderline': borderline_trajectory(),
    }

    for name, trajectory in scenarios.items():
        print(f"\n--- Scenario: {name.upper()} ---")
        result = simulate_wrapper(trajectory)
        summary = summarize_simulation(result)

        print(f"Actions triggered: {summary['action_count']} ({summary['actions']})")
        print(f"Mean CQ before: {summary['mean_pre_cq']:.3f}")
        print(f"Mean CQ after:  {summary['mean_post_cq']:.3f}")
        print(f"CQ improvement: {summary['cq_improvement']:+.3f}")
        print(f"Mean quality before: {summary['mean_pre_q']:.3f}")
        print(f"Mean quality after:  {summary['mean_post_q']:.3f}")
        print(f"Quality improvement: {summary['q_improvement']:+.3f}")

    print('\nExperiment complete. Review scenario summaries for wrapper effectiveness.')


if __name__ == '__main__':
    run_experiment()
