"""Independent stationary solve/path sum and scope tests for archived thermo2.

Predictions before this audit: stationary solve agrees with power method; an
identity observer gives D_n=(n-1)*sigma; binary boundary aggregation disproves
the general equality of boundary-edge and lumped dissipation. No physical-unit
or real-system inference is made. Uses NumPy only, no provider calls.
"""
import contextlib
import importlib.util
import io
import itertools
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'lineage/sources/claude-relay-2026-10-15/thermo2.py'
spec = importlib.util.spec_from_file_location('archived_thermo', SOURCE)
T = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(T)


def stationary_solve(P):
    a = P.T - np.eye(len(P))
    a[-1] = 1
    b = np.zeros(len(P)); b[-1] = 1
    return np.linalg.solve(a, b)


def direct_word_D(P, pi, labels, n):
    """Sum microscopic paths directly; independent of forward/filter routine."""
    law = {}
    for path in itertools.product(range(len(P)), repeat=n):
        probability = pi[path[0]]
        for i, j in zip(path, path[1:]):
            probability *= P[i, j]
        word = tuple(labels[i] for i in path)
        law[word] = law.get(word, 0.) + probability
    return float(sum(p * np.log(p/law[w[::-1]]) for w, p in law.items() if p > 0))


rows = []
for N, E, labels, m in [
    (3, T.E3, [0, 0, 1], 2),
    (4, T.E4, [0, 0, 1, 1], 2),
    (6, T.E6, [0, 0, 0, 1, 1, 1], 2),
    (6, T.E6, [0, 1, 0, 1, 0, 1], 2),
    (6, T.E6, [0, 0, 1, 1, 2, 2], 3),
    (6, T.E6, [0, 1, 1, 1, 1, 2], 3),
]:
    P = T.ring_chain(N, E, 1., 2.)
    pi = stationary_solve(P)
    sigma = T.epr(P, pi)
    D = T.word_D(P, pi, labels, m, 14 if m == 2 else 9)
    edges = []
    for i in range(N):
        j = (i+1) % N
        f, r = pi[i]*P[i, j], pi[j]*P[j, i]
        edges.append((f-r)*np.log(f/r))
    boundary = sum(edges[i] for i in range(N) if labels[i] != labels[(i+1) % N])
    lumped = T.lumped_epr(P, pi, labels, m)
    direct_errors = [abs(D[n]-direct_word_D(P, pi, labels, n)) for n in (2, 3, 5)]
    identity = T.word_D(P, pi, list(range(N)), N, 5)
    d = {n: D[n]-D[n-1] for n in range(2, max(D)+1)}
    row = dict(N=N, labels=labels, sigma=sigma, boundary_sigma=boundary,
               lumped_sigma=lumped, boundary_minus_lumped=boundary-lumped,
               power_solve_difference=float(abs(pi-T.stat(P)).max()),
               stationary_residual=float(abs(pi@P-pi).max()),
               direct_path_word_max_error=max(direct_errors),
               identity_DPI_equality_max_error=max(abs(identity[n]-(n-1)*sigma) for n in identity),
               d2_lumped_error=abs(d[2]-lumped),
               minimum_increment=min(d.values()),
               max_increment_over_sigma=max(d.values())/sigma,
               max_block_bound_excess=max(D[n]-(n-1)*sigma for n in D),
               increments=d)
    assert row['stationary_residual'] < 1e-12
    assert row['direct_path_word_max_error'] < 1e-11
    assert row['identity_DPI_equality_max_error'] < 1e-10
    assert row['d2_lumped_error'] < 1e-11
    assert row['minimum_increment'] > -1e-11
    assert row['max_block_bound_excess'] < 1e-10
    assert boundary-lumped > -1e-12
    rows.append(row)

zero = []
for N, E in ((3, T.E3), (4, T.E4), (6, T.E6)):
    P = T.ring_chain(N, E, 1., 0.)
    pi = stationary_solve(P)
    boltz = np.exp(-np.asarray(E)); boltz /= boltz.sum()
    result = dict(N=N, boltzmann_error=float(abs(pi-boltz).max()), sigma=T.epr(P, pi))
    assert result['boltzmann_error'] < 1e-12
    assert abs(result['sigma']) < 1e-12
    zero.append(result)

out = dict(scope='Stationary bidirectionally supported discrete-time ring chains, N>=3; n<=14 binary/n<=9 ternary. EPR nats per uniformized step.',
           archived_module=str(SOURCE), zero_affinity=zero, cases=rows,
           tests='All assertions passed; finite enumeration is not proof of all horizons.',
           nonclaims=['Not physical entropy in joules/K without a local-detailed-balance interpretation and units.',
                      'Finite increment overshoot does not violate the block data-processing bound.',
                      'Boundary/lumped equality requires channel-identification conditions.'])
destination = ROOT / 'evaluation/results/relay-thermo-audit.json'
destination.write_text(json.dumps(out, indent=2)+'\n')
print(destination)
for r in rows:
    print(f"N={r['N']} labels={r['labels']} sigma={r['sigma']:.8f} boundary={r['boundary_sigma']:.8f} lump={r['lumped_sigma']:.8f} max(d)/sigma={r['max_increment_over_sigma']:.5f}")
