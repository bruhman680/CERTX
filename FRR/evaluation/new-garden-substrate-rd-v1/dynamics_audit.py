"""Detached exact enumeration; no model, filesystem world, or learning claims."""
import json
from collections import Counter
from pathlib import Path

MASK = 255

def rule90(x):
    return (((x << 1) | (x >> 7)) ^ ((x >> 1) | (x << 7))) & MASK

def advance(pair):
    a, b = pair
    return b, a ^ rule90(b)

def inverse(pair):
    a, b = pair
    return b ^ rule90(a), a

def audit():
    collapse = Counter()
    for initial in range(256):
        x, elapsed = initial, 0
        while x and elapsed <= 4:
            x = rule90(x)
            elapsed += 1
        assert x == 0 and elapsed <= 4
        collapse[elapsed] += 1
    periods = Counter()
    successors = set()
    for a in range(256):
        for b in range(256):
            initial = (a, b)
            nxt = advance(initial)
            assert inverse(nxt) == initial
            assert advance(inverse(initial)) == initial
            successors.add(nxt)
            state, period = nxt, 1
            while state != initial and period <= 8:
                state = advance(state)
                period += 1
            assert state == initial and period <= 8 and 8 % period == 0
            periods[period] += 1
    assert len(successors) == 65536
    return {
        'kind': 'exact finite-state dynamics enumeration; not model evaluation',
        'rule90_periodic_8bit': {'states': 256, 'first_zero_tick_counts': dict(sorted(collapse.items())), 'all_zero_by_tick': 4},
        'second_order_rule90_8bit': {'states': 65536, 'unique_successors': len(successors), 'inverse_checked_every_state': True, 'exact_period_state_counts': dict(sorted(periods.items())), 'maximum_period': max(periods)},
        'model_calls': 0, 'candidate_world_actions': 0,
    }

if __name__ == '__main__':
    result = audit()
    destination = Path(__file__).with_name('RESULTS.json')
    destination.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
