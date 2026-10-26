#!/usr/bin/env python3
"""Standalone prospective CR-C1/2/3 implementation. Never imports prior code."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import time
# Set before NumPy imports/initializes any BLAS runtime.
for _thread_variable in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
                         'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
    os.environ[_thread_variable] = '1'
import numpy as np

HERE = Path(__file__).resolve().parent
EVAL = HERE.parent
SA = EVAL / 'structural-access-three-cycle-v1'
PC = EVAL / 'paired-context-mismatch-v1'
SEEDS = (92501, 92507, 92509)
PROBES = {'COPY': (1., 1.), 'CONTEXT_FLIP': (-1., 1.),
          'PARTIAL_CONTEXT': (-.5, 1.), 'SIGNAL_FLIP': (1., -1.),
          'GLOBAL_FLIP': (-1., -1.)}
METHODS = ('full', 'oracle', 'repaired', 'solved')
LABELS = np.array(['A', 'N', 'U'])
TOL = 1e-10


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1048576), b''):
            h.update(block)
    return h.hexdigest()


def ah(a):
    return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()


def meta(a):
    return {'dtype': str(a.dtype), 'shape': list(a.shape), 'sha256': ah(a)}


def dump(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + '\n')


def source_meta(a):
    # Original SA/PC manifests bind dtype and shape before contiguous bytes.
    h = hashlib.sha256()
    h.update(str(a.dtype).encode())
    h.update(str(a.shape).encode())
    h.update(np.ascontiguousarray(a).tobytes())
    return {'dtype': str(a.dtype), 'shape': list(a.shape), 'sha256': h.hexdigest()}


def check(a, expected):
    assert source_meta(a) == expected, ('array source mismatch', source_meta(a), expected)


class Pool:
    """Exact content address includes dtype, shape and C-contiguous bytes."""
    def __init__(self):
        self.arrays = {}
        self.fields = {}
        self.logical_bytes = 0

    def add(self, condition, fields):
        mapping = {}
        for field, value in fields.items():
            a = np.ascontiguousarray(value)
            digest = hashlib.sha256()
            digest.update(a.dtype.str.encode())
            digest.update(json.dumps(a.shape).encode())
            digest.update(a.tobytes())
            key = 'h' + digest.hexdigest()
            if key in self.arrays:
                old = self.arrays[key]
                assert old.dtype == a.dtype and old.shape == a.shape and old.tobytes() == a.tobytes()
            else:
                self.arrays[key] = a
            mapping[field] = key
            self.logical_bytes += a.nbytes
        self.fields[condition] = mapping

    def save(self, out):
        np.savez_compressed(out / 'outcomes.npz', **self.arrays)
        dump(out / 'OUTCOME_MAP.json', {'conditions': self.fields,
             'logical_arrays': sum(map(len, self.fields.values())),
             'unique_arrays': len(self.arrays), 'logical_bytes': self.logical_bytes,
             'unique_bytes': sum(a.nbytes for a in self.arrays.values()),
             'address': 'SHA256(dtype.str UTF8 + JSON shape UTF8 + contiguous C bytes)',
             'arrays': {k: meta(a) for k, a in self.arrays.items()}})


def fit(d):
    _, s, vh = np.linalg.svd(d, full_matrices=False)
    numeric = int(np.count_nonzero(s > TOL))
    rank = min(numeric, 12)
    basis = vh[:rank].conj().T
    p = basis @ basis.conj().T if rank else np.zeros((24, 24), dtype=d.dtype)
    gap = float(s[rank-1] - s[rank]) if rank and rank < len(s) else None
    return p, {'numerical_rank': numeric, 'retained_rank': rank,
        'rank_tolerance': TOL, 'singular_values': s.tolist(),
        'normalized_singular_values': (s / s[0] if s[0] > TOL else np.zeros_like(s)).tolist(),
        'rank_cutoff_gap': gap, 'rank_cutoff_near_tie': gap is not None and abs(gap) <= TOL,
        'hermitian_error': float(np.linalg.norm(p-p.conj().T)),
        'idempotent_error': float(np.linalg.norm(p@p-p))}


def dist(a, b):
    return float(np.linalg.norm(a-b) / np.sqrt(24))


def target(delta, alpha, beta):
    c, b = delta*(1+alpha)/2, (1+beta)/2
    if c == 0 and b == 0:
        return np.zeros((24, 24))
    i = np.eye(12)
    return np.block([[c*c*i, c*b*i], [c*b*i, b*b*i]])/(c*c+b*b)


def products(queries, records, p):
    q, x = queries @ p.T, records @ p.T
    qn, xn = np.linalg.norm(q, axis=1), np.linalg.norm(x, axis=1)
    q = np.divide(q, qn[:, None], out=np.zeros_like(q), where=qn[:, None] > TOL)
    x = np.divide(x, xn[:, None], out=np.zeros_like(x), where=xn[:, None] > TOL)
    z = q.conj() @ x.T
    valid = (qn[:, None] > TOL) & (xn[None, :] > TOL) & (np.abs(z) > TOL)
    # Algebraic real A+iB replay of actual normalized query/record arrays.
    real = q.real @ x.real.T + q.imag @ x.imag.T
    imag = q.real @ x.imag.T - q.imag @ x.real.T
    err = float(np.max(np.abs(z-(real+1j*imag))))
    assert err < 1e-12
    return z, valid, qn, xn, err


def calibrate(records, p):
    z, valid, qn, xn, err = products(records[::3], records, p)
    idx = np.arange(8)[:, None]*3 + np.arange(3)
    matched, v = np.take_along_axis(z, idx, 1), np.take_along_axis(valid, idx, 1)
    units = np.divide(matched, np.abs(matched), out=np.zeros_like(matched), where=v)
    counts = np.sum(v, axis=0)
    centres = np.divide(np.sum(units, axis=0), counts, out=np.zeros(3, dtype=complex), where=counts > 0)
    available = (counts > 0) & (np.abs(centres) > TOL)
    return {'centres': centres, 'available': available, 'calibration_products': matched,
            'calibration_valid': v, 'calibration_valid_counts': counts, 'calibration_query_norms': qn, 'calibration_record_norms': xn}, err


def decode(z, valid, cal):
    labels = np.full(z.shape, 'ABSTAIN', dtype='<U7')
    reasons = np.full(z.shape, 'calibration_unavailable', dtype='<U23')
    if not np.all(cal['available']):
        return labels, reasons
    reasons[:] = 'zero_product'
    centres = cal['centres']/np.abs(cal['centres'])
    distances = np.abs(np.angle(z[..., None]*np.conj(centres)))
    order = np.argsort(distances, axis=-1, kind='stable')
    ds = np.take_along_axis(distances, order, -1)
    ambiguous = ds[..., 1]-ds[..., 0] <= TOL
    good = valid & ~ambiguous
    labels[good] = LABELS[order[..., 0][good]]
    reasons[good] = 'ok'
    reasons[valid & ambiguous] = 'ambiguous_centre'
    return labels, reasons


def metrics(top, predictions, reasons, claim, all_labels):
    relevant = top//3 == claim
    correct = relevant & (predictions == LABELS[top%3])
    count, joint = int(relevant.sum()), int(correct.sum())
    result = {'evidence_count': count, 'evidence_recall': count/3,
        'evidence_complete': int(count == 3), 'joint_label_count': joint,
        'joint_label_recall': joint/3, 'joint_complete': int(joint == 3),
        'wrong_scope_count': 3-count,
        'encoded_U_recall': int(np.any(relevant & (top%3 == 2) & (predictions == 'U'))),
        'abstain_count': int(np.sum(predictions == 'ABSTAIN')),
        'oracle_relevant_stance_accuracy': float(np.mean(all_labels[claim*3:claim*3+3] == LABELS))}
    for reason in ('calibration_unavailable', 'ambiguous_centre', 'zero_product'):
        result['abstain_'+reason] = int(np.sum(reasons == reason))
    return result


def source(out):
    sm = json.loads((SA/'run/INPUT_MANIFEST.json').read_text())
    pm = json.loads((PC/'run/INPUT_MANIFEST.json').read_text())
    sam = json.loads((SA/'ARCHIVE_MANIFEST.json').read_text())
    pam = json.loads((PC/'ARCHIVE_MANIFEST.json').read_text())
    assert sha(SA/'run/inputs.npz') == sm['file_sha256'] == sam['files']['run/inputs.npz']['sha256']
    assert sha(PC/'run/training_inputs.npz') == pm['training_file_sha256'] == pam['files']['run/training_inputs.npz']['sha256']
    assert sha(SA/'run/INPUT_MANIFEST.json') == sam['files']['run/INPUT_MANIFEST.json']['sha256']
    assert sha(PC/'run/INPUT_MANIFEST.json') == pam['files']['run/INPUT_MANIFEST.json']['sha256']
    # Bind the existing source archives too; do not copy the large PC archive.
    assert sha(SA/'run.tar.xz') == sam['sha256']
    assert sha(PC/'run.tar.xz') == pam['sha256']
    shutil.copyfile(SA/'run/inputs.npz', out/'source_inputs.npz')
    for prefix, root in [('SA', SA), ('PC', PC)]:
        shutil.copyfile(root/'ARCHIVE_MANIFEST.json', out/(prefix+'_ARCHIVE_MANIFEST.json'))
        shutil.copyfile(root/'run/INPUT_MANIFEST.json', out/(prefix+'_INPUT_MANIFEST.json'))
    with np.load(out/'source_inputs.npz', allow_pickle=False) as archive:
        inputs = {k: archive[k] for k in archive.files}
    for k, a in inputs.items():
        check(a, sm['arrays'][k])
    selected, provenance = {}, {}
    with np.load(PC/'run/training_inputs.npz', allow_pickle=False) as archive:
        for seed in SEEDS:
            for ai in (3, 4):
                for suffix in ('pairs', 'differences'):
                    k = f's{seed}_a{ai}_{suffix}'
                    a = archive[k]
                    check(a, pm['training_arrays'][k])
                    selected[k] = a[:48].copy()
                    provenance[k] = {'full_array': source_meta(a), 'full_array_local_rawbytes': meta(a), 'slice': '[0:48, ...]', 'selected': meta(selected[k])}
    np.savez_compressed(out/'selected_training.npz', **selected)
    dump(out/'INPUT_MANIFEST.json', {'source_commits': {'SA': '8560969b84f0eed0c4b81f1fbc87febe959aa3ac',
        'PC': 'cc413eca895131bfe81c3fc6f38dc81f21a26143'},
        'hash_schemes': {'source_array': 'SHA256(str(dtype) UTF8 + str(shape tuple) UTF8 + contiguous C bytes)',
                        'local_array': 'SHA256(contiguous C bytes)',
                        'outcome_pool': 'SHA256(dtype.str UTF8 + JSON shape UTF8 + contiguous C bytes)'},
        'source_file_sha256': sha(out/'source_inputs.npz'), 'training_full_file_sha256': pm['training_file_sha256'],
        'selected_file_sha256': sha(out/'selected_training.npz'), 'selected_arrays': provenance,
        'source_arrays': {k: meta(a) for k, a in inputs.items()}, 'time_unix': time.time()})
    return inputs, selected


def main(out):
    out.mkdir(parents=True, exist_ok=False)
    dump(out/'ATTEMPT.json', {'status': 'started', 'time_unix': time.time()})
    for name in ('experiment.py', 'PROTOCOL.md', 'SCHEMA.md', 'IMPLEMENTATION.md'):
        shutil.copyfile(HERE/name, out/name)
    inputs, training = source(out)
    raw, specifications, query_manifest = {}, [], []
    for seed in SEEDS:
        q = inputs[f's{seed}_Q'][1]
        assert np.linalg.norm(q.T@q-np.eye(24)) < 1e-12
        for ri in range(2):
            for ei in range(2):
                queries = inputs[f's{seed}_queries_r{ri}_e{ei}']
                for j, a in enumerate(queries):
                    query_manifest.append({'query_id': f'{seed}-r{ri}-e{ei}-q{j:02d}', 'array_sha256': ah(a),
                        'claim': int(inputs[f's{seed}_query_claim_index'][j]),
                        'repetition': int(inputs[f's{seed}_query_repetition'][j]),
                        'paired_reuses': 20, 'method_reuses': 80})
        for ai, delta in ((3, .5), (4, 1.5)):
            base = training[f's{seed}_a{ai}_differences']
            pairs = training[f's{seed}_a{ai}_pairs']
            pair_error = float(np.max(np.abs(base-(pairs[:, 0]-pairs[:, 1])/2)))
            # Source pair convention checked explicitly; difference is A-N divided by two.
            assert pair_error < 1e-12, pair_error
            assert np.max(np.abs(base[:, :12]-delta*base[:, 12:])) < 1e-12
            for probe, (alpha, beta) in PROBES.items():
                stem = f's{seed}_a{ai}_{probe}'
                probe_base = base*np.r_[np.full(12, alpha), np.full(12, beta)]
                first, second = base@q.T, probe_base@q.T
                average = (first+second)/2
                identified = abs(beta-alpha) > TOL
                solved = (second-alpha*first)/(beta-alpha) if identified else np.zeros_like(first)
                raw.update({stem+'_solved': solved, stem+'_solved_available': np.array(identified),
                            stem+'_solved_reason': np.array('ok' if identified else 'unidentified_operator'),
                            stem+'_identified_operator': np.array(identified), stem+'_first': first, stem+'_second': second, stem+'_average': average,
                            stem+'_intervention': np.array([alpha, beta])})
                for m in (12, 48):
                    specifications.append((seed, ai, delta, probe, alpha, beta, m, stem, pair_error))
    np.savez_compressed(out/'probe_inputs.npz', **raw)
    dump(out/'QUERY_MANIFEST.json', {'queries': query_manifest, 'query_ids': len(query_manifest),
        'unique_base_arrays': len({x['array_sha256'] for x in query_manifest}), 'underlying_claims': 48,
        'note': 'Same evaluation data control; nominal contrasts have arm-dependent information.'})
    dump(out/'PRE_FIT_CHECKPOINT.json', {'time_unix': time.time(), 'files': {n: sha(out/n) for n in
        ('source_inputs.npz', 'selected_training.npz', 'INPUT_MANIFEST.json', 'probe_inputs.npz', 'QUERY_MANIFEST.json')},
        'arrays': {k: meta(a) for k, a in raw.items()}})
    structures, diagnostics, calibrations, configs, checks = {}, [], {}, [], []
    for seed, ai, delta, probe, alpha, beta, m, rawstem, pair_error in specifications:
        q = inputs[f's{seed}_Q'][1]
        pb = q@np.diag(np.r_[np.zeros(12), np.ones(12)])@q.T
        stem = rawstem+f'_m{m}'
        projections = {}
        fitinfo = {}
        for name in ('first', 'second', 'average', 'solved'):
            projections[name], fitinfo[name] = fit(raw[rawstem+'_'+name][:m])
            structures[stem+'_'+name+'_projector'] = projections[name]
            structures[stem+'_'+name+'_singular_values'] = np.asarray(fitinfo[name]['singular_values'])
        p = projections['average']
        intended = q@target(delta, alpha, beta)@q.T
        structures[stem+'_analytic_target'] = intended
        diag = {'seed': seed, 'delta': delta, 'probe': probe, 'm': m, 'stem': stem,
            'alpha': alpha, 'beta': beta, 'identified_operator': abs(beta-alpha) > TOL,
            'solved_available': abs(beta-alpha) > TOL,
            'solved_reason': 'ok' if abs(beta-alpha) > TOL else 'unidentified_operator',
            'solved_target_distance': dist(projections['solved'], pb) if abs(beta-alpha) > TOL else None,
            'solved_binding_distance': dist(projections['solved'], pb) if abs(beta-alpha) > TOL else None,
            'solved_zero_placeholder_distance': None if abs(beta-alpha) > TOL else dist(projections['solved'], np.zeros((24, 24))), 'fit': fitinfo, 'source_pair_roundoff': pair_error,
            'ambient_relative_change': float(np.linalg.norm(raw[rawstem+'_second'][:m]-raw[rawstem+'_first'][:m])/np.linalg.norm(raw[rawstem+'_first'][:m])),
            'base_probe_distance': dist(projections['first'], projections['second']),
            'average_base_distance': dist(p, projections['first']), 'average_binding_distance': dist(p, pb),
            'average_target_distance': dist(p, intended), 'target_rank': int(np.linalg.matrix_rank(intended, tol=TOL)),
            'fixed_rank_predecessor_difference': 'Previous estimator always retained 12; this estimator guards numerical rank and returns zero for empty average.'}
        assert diag['average_target_distance'] < 1e-9
        assert diag['solved_target_distance'] is None or diag['solved_target_distance'] < 1e-9
        diagnostics.append(diag)
        for method, projector in [('full', np.eye(24)), ('oracle', pb), ('repaired', p), ('solved', projections['solved'])]:
            structures[stem+'_'+method+'_projector'] = projector
            for ri in range(2):
                cstem = stem+f'_r{ri}_{method}'
                records = inputs[f's{seed}_cal_records_r{ri}']@q.T
                cal, error = calibrate(records, projector)
                calibrations[cstem] = cal
                structures.update({cstem+'_'+k: v for k, v in cal.items()})
                configs.append({'key': cstem, 'seed': seed, 'ai': ai, 'delta': delta, 'probe': probe,
                                'm': m, 'ri': ri, 'r': (.5, 2.)[ri], 'method': method, 'projector_key': stem+'_'+method+'_projector',
                                'identified_operator': abs(beta-alpha) > TOL if method == 'solved' else None})
                checks.append({'calibration': cstem, 'complex_real_error': error})
    # Span equivalence controls on actual data/projectors.
    controls = []
    for seed in SEEDS:
        for ai in (3, 4):
            for m in (12, 48):
                prefix = f's{seed}_a{ai}_'
                cf = structures[prefix+f'CONTEXT_FLIP_m{m}_second_projector']
                sf = structures[prefix+f'SIGNAL_FLIP_m{m}_second_projector']
                gf = structures[prefix+f'GLOBAL_FLIP_m{m}_second_projector']
                base = structures[prefix+f'GLOBAL_FLIP_m{m}_first_projector']
                zero = raw[prefix+'GLOBAL_FLIP_average'][:m]
                row = {'seed': seed, 'ai': ai, 'm': m, 'context_signal_probe_span_distance': dist(cf, sf),
                       'global_base_probe_span_distance': dist(gf, base), 'global_average_norm': float(np.linalg.norm(zero))}
                assert max(row[k] for k in ('context_signal_probe_span_distance', 'global_base_probe_span_distance', 'global_average_norm')) < 1e-12
                controls.append(row)
    assert len(diagnostics) == 60 and len(configs) == 480
    np.savez_compressed(out/'structures_centres.npz', **structures)
    dump(out/'STRUCTURAL_DIAGNOSTICS.json', diagnostics)
    dump(out/'CALIBRATION_CONFIGS.json', configs)
    dump(out/'ALGEBRA_DIAGNOSTICS.json', {'controls': controls, 'calibrations': checks})
    dump(out/'PRE_SCORING_CHECKPOINT.json', {'time_unix': time.time(), 'files': {n: sha(out/n) for n in
        ('PRE_FIT_CHECKPOINT.json', 'structures_centres.npz', 'STRUCTURAL_DIAGNOSTICS.json', 'CALIBRATION_CONFIGS.json', 'ALGEBRA_DIAGNOSTICS.json')}})
    pool, aggregates, product_checks = Pool(), [], []
    ledger, paired, repeated = [], {}, {}
    prior = {}
    # Read source ledger only after the fitted checkpoint, solely for frozen FULL/ORACLE controls.
    assert sha(PC/'run/LEDGER.jsonl') == json.loads((out/'PC_ARCHIVE_MANIFEST.json').read_text())['files']['run/LEDGER.jsonl']['sha256']
    with open(PC/'run/LEDGER.jsonl') as f:
        for line in f:
            row = json.loads(line)
            if row['method'] in ('full', 'oracle'):
                key = (row['query_id'], row['method'])
                reference = {k: row[k] for k in ('returned_indices', 'predictions', 'reasons', 'oracle_relevant_predictions', 'oracle_relevant_reasons', 'metrics')}
                if key in prior:
                    assert prior[key] == reference
                prior[key] = reference
    predecessor_checks, repeat_checks = [], []
    for cfg in configs:
        seed, ri, method = cfg['seed'], cfg['ri'], cfg['method']
        q = inputs[f's{seed}_Q'][1]
        p = structures[cfg['projector_key']]
        records = inputs[f's{seed}_eval_records_r{ri}']@q.T
        for ei in range(2):
            key = cfg['key']+f'_e{ei}'
            queries = inputs[f's{seed}_queries_r{ri}_e{ei}']@q.T
            z, valid, qn, xn, error = products(queries, records, p)
            labels, reasons = decode(z, valid, calibrations[cfg['key']])
            scores = np.abs(z)
            order = np.argsort(-scores, axis=1, kind='stable')
            top = order[:, :3]
            fields = {'products': z, 'valid': valid, 'labels': labels, 'reasons': reasons,
                      'scores': scores, 'top': top, 'query_norms': qn, 'record_norms': xn}
            pool.add(key, fields)
            product_checks.append({'key': key, 'complex_real_error': error})
            condition = {k: cfg[k] for k in ('seed', 'delta', 'probe', 'm', 'r', 'method')}
            condition.update(Q='dense', eval_eta=(0., 1.5)[ei],
                             solved_available=cfg['identified_operator'] if method == 'solved' else None,
                             solved_reason=('ok' if cfg['identified_operator'] else 'unidentified_operator') if method == 'solved' else None,
                             unidentified_operator=method == 'solved' and not cfg['identified_operator'])
            sums = {}
            for j in range(32):
                claim = int(inputs[f's{seed}_query_claim_index'][j])
                ix = top[j]
                pred, reason = labels[j, ix], reasons[j, ix]
                met = metrics(ix, pred, reason, claim, labels[j])
                for name, value in met.items():
                    sums[name] = sums.get(name, 0)+value
                qid = f'{seed}-r{ri}-e{ei}-q{j:02d}'
                gap = float(scores[j, order[j, 2]]-scores[j, order[j, 3]])
                row = dict(condition, query_id=qid, query_index=j, claim=claim,
                    repetition=int(inputs[f's{seed}_query_repetition'][j]), outcome_key=key,
                    returned_indices=ix.tolist(), returned_record_ids=[f'eval-e{x//6}-t{(x//3)%2}-{LABELS[x%3]}' for x in ix],
                    products_real=z[j, ix].real.tolist(), products_imag=z[j, ix].imag.tolist(),
                    scores=scores[j, ix].tolist(), angles=np.angle(z[j, ix]).tolist(),
                    predictions=pred.tolist(), reasons=reason.tolist(), boundary_gap=gap, near_boundary_tie=gap <= TOL,
                    within_top3_score_differences=np.diff(scores[j, ix]).tolist(),
                    oracle_relevant_predictions=labels[j, claim*3:claim*3+3].tolist(),
                    oracle_relevant_reasons=reasons[j, claim*3:claim*3+3].tolist(), metrics=met)
                pair_key = f'{seed}-a{cfg["ai"]}-{cfg["probe"]}-m{cfg["m"]}-r{ri}-e{ei}-q{j:02d}'
                if pair_key not in paired:
                    paired[pair_key] = {'pair_id': pair_key, 'query_id': qid, 'method_record_indices': {}}
                paired[pair_key]['method_record_indices'][method] = len(ledger)
                ledger.append(row)
                if method in ('full', 'oracle'):
                    ref = {k: row[k] for k in ('returned_indices', 'predictions', 'reasons', 'oracle_relevant_predictions', 'oracle_relevant_reasons', 'metrics')}
                    reference = prior[(qid, method)]
                    differing = {k: {'old': reference[k], 'new': ref[k]} for k in ref if reference[k] != ref[k]}
                    predecessor_checks.append({'key': key, 'query_id': qid, 'differences': differing})
                    assert not differing, ('predecessor control changed', qid, method, differing)
                    rkey = (qid, method)
                    if rkey in repeated:
                        assert ref == repeated[rkey]
                        repeat_checks.append({'key': key, 'query_id': qid, 'equal': True})
                    else:
                        repeated[rkey] = ref
            aggregates.append(dict(condition, outcome_key=key, count=32, metric_sums=sums,
                                   metric_means={k: v/32 for k, v in sums.items()}))
    assert len(ledger) == 30720 and len(paired) == 7680 and len(aggregates) == 960
    assert len(query_manifest) == 384 and len({x['array_sha256'] for x in query_manifest}) == 288
    pool.save(out)
    with open(out/'LEDGER.jsonl', 'w') as f:
        for row in ledger:
            f.write(json.dumps(row, allow_nan=False)+'\n')
    with open(out/'PAIRED_ROWS.jsonl', 'w') as f:
        for row in paired.values():
            f.write(json.dumps(row)+'\n')
    dump(out/'AGGREGATES.json', aggregates)
    dump(out/'PRODUCT_CHECKS.json', product_checks)
    dump(out/'PREDECESSOR_CONTROL_CHECKS.json', predecessor_checks)
    dump(out/'REPEATED_CONTROL_CHECKS.json', repeat_checks)
    dump(out/'SUMMARY.json', {'structural_rows': len(diagnostics), 'calibration_conditions': len(configs),
        'method_conditions': len(aggregates), 'paired_rows': len(paired), 'method_records': len(ledger),
        'query_ids': 384, 'unique_base_queries': 288, 'underlying_claims': 48,
        'logical_output_arrays': sum(map(len, pool.fields.values())), 'unique_output_arrays': len(pool.arrays)})
    dump(out/'ATTEMPT.json', {'status': 'complete', 'time_unix': time.time()})
    dump(out/'OUTPUT_HASHES.json', {p.name: sha(p) for p in sorted(out.iterdir()) if p.is_file() and p.name != 'OUTPUT_HASHES.json'})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, default=HERE/'run')
    args = parser.parse_args()
    main(args.out)
