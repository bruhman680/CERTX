"""Constructed transport/retention example; no general memory claim or AI eval.

The deposit mechanism is explicit in the construction. Passive reads are copies;
active probes remove a declared fraction of pulse and retained state at site 20.
"""
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def run(direction=1, rho=.98, deposit=.2, pulse=True, log=False, probe=0., initial_retained=None):
    mobile = np.zeros(31)
    retained = np.zeros(31)
    if initial_retained is not None:
        retained[:] = initial_retained
    mobile[15] = float(pulse)
    records = {}
    for t in range(41):
        if log and t in [0, 5, 16, 40]:
            records[t] = {'mobile': mobile.copy().tolist(),
                          'retained': retained.copy().tolist()}
        if t == 40:
            break
        # A physically consequential probe is distinct from a copied read.
        mobile[20] *= 1 - probe
        retained[20] *= 1 - probe
        retained = rho * retained + deposit * mobile
        shifted = np.zeros_like(mobile)
        if direction == 1:
            shifted[1:] = mobile[:-1]
        else:
            shifted[:-1] = mobile[1:]
        mobile = shifted
    return mobile, retained, records


def summary(mobile, retained):
    return {'mobile_mass': float(mobile.sum()),
            'retained_mass': float(retained.sum()),
            'retained_position_moment': float(retained @ (np.arange(31) - 15)),
            'retained_at_site20': float(retained[20])}


def main():
    plus = run(log=True)
    minus = run(direction=-1, log=True)
    without_log = run()
    assert np.array_equal(plus[0], without_log[0])
    assert np.array_equal(plus[1], without_log[1])
    assert plus[0].sum() == minus[0].sum() == 0
    assert np.isclose(plus[1].sum(), minus[1].sum())
    assert not np.array_equal(plus[1], minus[1])
    assert np.isclose(plus[1] @ (np.arange(31)-15),
                      -minus[1] @ (np.arange(31)-15))
    controls = {}
    for name, settings in [('no_write', {'deposit': 0}),
                           ('fast_erasure', {'rho': 0}),
                           ('no_pulse', {'pulse': False}),
                           ('active_probe', {'probe': .2})]:
        u, r, _ = run(**settings)
        controls[name] = summary(u, r)
    assert all(controls[name]['retained_mass'] == 0
               for name in ['no_write', 'fast_erasure', 'no_pulse'])
    assert controls['active_probe']['retained_mass'] < plus[1].sum()
    # The fresh-reader interface receives only a substrate snapshot.
    fresh_substrate = plus[1].copy()
    erased_substrate = np.zeros_like(fresh_substrate)
    assert erased_substrate.sum() == 0
    # Without a known baseline, a prepared older field can mimic the same trace.
    prepared = fresh_substrate / (.98 ** 40)
    _, mimic, _ = run(pulse=False, initial_retained=prepared)
    assert np.allclose(mimic, fresh_substrate)
    results = {'kind': 'explicitly constructed linear model',
               'settings': {'sites': 31, 'initial_site': 15, 'steps': 40,
                            'rho': .98, 'deposit': .2, 'probe_site': 20},
               'right_history': summary(plus[0], plus[1]),
               'left_history': summary(minus[0], minus[1]),
               'controls': controls, 'passive_read_unchanged': True,
               'fresh_reader_input': fresh_substrate.tolist(),
               'substrate_reset_mass': float(erased_substrate.sum()),
               'no_pulse_prepared_initial_field_matches': bool(np.allclose(mimic, fresh_substrate)),
               'right_witness_snapshots': plus[2],
               'left_witness_snapshots': minus[2],
               'limits': ['Retention and motion are programmed, not discovered.',
                          'No learned or human reader was evaluated.',
                          'Passive reads are noninteracting only by this model definition.',
                          'Position-moment readout is chosen from known toy geometry.',
                          'No guarantee of uncompromised real-world measurement.']}
    out = ROOT / 'evaluation/results/substrate-witness-2026-10-05.json'
    out.write_text(json.dumps(results, indent=2)+'\n')
    print(json.dumps({k: results[k] for k in
                     ['right_history', 'left_history', 'controls',
                      'passive_read_unchanged', 'no_pulse_prepared_initial_field_matches']}, indent=2))


if __name__ == '__main__':
    main()
