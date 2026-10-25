#!/usr/bin/env python3
"""Prospective UB-C1/2/3 implementation. No outcome-dependent parameters."""
import os
for _key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[_key] = '1'
import argparse
import collections
import datetime
import gzip
import hashlib
import io
import json
from pathlib import Path
import shutil
import time
import numpy as np

SEEDS = (91391, 91397, 91411)
RATIOS = (0.5, 1.0, 2.0)
CAL_NOISE = (0.0, 0.75)
EVAL_NOISE = (0.0, 0.75, 1.5)
MODES = ('GLOBAL', 'SCOPED')
STATUSES = ('A', 'N', 'U')
PHASES = np.array([1 + 0j, -1 + 0j, np.exp(1j * np.pi / 3)])
METHODS = ('full_cos_angle', 'full_mod_angle', 'real_AB_angle', 'binding_mod_angle')
TOL = 1e-10
DIM = 24


def json_dump(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False, sort_keys=True) + '\n')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def array_hash(a):
    a = np.ascontiguousarray(a, dtype='<c16')
    return sha(a.tobytes())


def unit(a):
    return a / np.linalg.norm(a, axis=-1, keepdims=True)


def encode(c, b, ratio, mode):
    # Canonical order: entity, time, status; all records unit norm.
    c = np.repeat(c[:, :, None, :], 3, axis=2) * ratio
    b = b[:, :, None, :] * PHASES[None, None, :, None]
    if mode == 'GLOBAL':
        c = c * PHASES[None, None, :, None]
    return unit(np.concatenate((c, b), axis=-1)).reshape(-1, 48)


def products(q, w, family):
    if family == 'binding':
        q, w = unit(q[..., DIM:]), unit(w[..., DIM:])
    if family == 'real_AB':
        a = q.real @ w.real.T + q.imag @ w.imag.T
        b = q.real @ w.imag.T - q.imag @ w.real.T
        h = a + 1j * b
    else:
        h = q.conj() @ w.T
    return h / (np.linalg.norm(q, axis=-1)[:, None] * np.linalg.norm(w, axis=-1)[None, :])


def fit_centres(q, w, family):
    h = products(q, w, family)
    # Two repetitions per entity/time, against that scope's three records only.
    same = h[np.arange(16)[:, None], (np.arange(16) // 2 * 3)[:, None] + np.arange(3)]
    centres, diagnostics = [], []
    for s in range(3):
        values = same[:, s]
        valid = np.abs(values) > TOL
        n = int(valid.sum())
        mean = np.mean(values[valid] / np.abs(values[valid])) if n else 0j
        resultant = float(abs(mean))
        missing = n == 0 or resultant <= TOL
        centres.append(None if missing else float(np.angle(mean)))
        diagnostics.append({'status': STATUSES[s], 'centre': centres[-1], 'resultant_length': resultant,
                            'valid_angle_count': n, 'flag': 'missing_centre' if missing else 'available'})
    return centres, diagnostics


def decode(h, centres):
    # No entity, time, relevance, or source status is accepted by this decoder.
    shape = h.shape
    pred = np.full(shape, 3, dtype=np.int64)
    reasons = np.full(shape, '', dtype='<U24')
    if any(c is None for c in centres):
        reasons[:] = 'calibration_unavailable'
        return pred, reasons
    valid = np.abs(h) > TOL
    distance = np.abs(np.angle(np.exp(1j * (np.angle(h)[..., None] - np.array(centres)))))
    order = np.argsort(distance, axis=-1, kind='stable')
    nearest = np.take_along_axis(distance, order, axis=-1)
    ambiguous = (nearest[..., 1] - nearest[..., 0]) <= TOL
    pred[valid & ~ambiguous] = order[..., 0][valid & ~ambiguous]
    reasons[~valid] = 'zero_product'
    reasons[valid & ambiguous] = 'ambiguous_centre'
    return pred, reasons


def rank(scores):
    return np.argsort(-scores, axis=-1, kind='stable')


def metric(retrieved, pred, scope, oracle_pred):
    relevant = retrieved // 3 == scope
    correct = relevant & (pred == retrieved % 3)
    top_relevant = bool(relevant[0])
    return {'evidence_recall': float(relevant.sum() / 3), 'evidence_complete': bool(relevant.all()),
            'joint_label_recall': float(correct.sum() / 3), 'joint_complete': bool(correct.all()),
            'wrong_scope_count': int((~relevant).sum()), 'abstain_count': int((pred == 3).sum()),
            'encoded_U_recall': int(np.any(correct & (retrieved % 3 == 2))),
            'A_reference_agreement_at_1': bool(top_relevant and retrieved[0] % 3 == 0),
            'decoded_A_at_1_if_relevant': bool(pred[0] == 0) if top_relevant else None,
            'top1_relevant': top_relevant, 'top1_source_A': bool(retrieved[0] % 3 == 0) if top_relevant else None,
            'oracle_relevant_stance_accuracy': float(np.mean(oracle_pred == np.arange(3)))}


def prepare_inputs():
    latent, queries = {}, {}
    for seed in SEEDS:
        streams = np.random.SeedSequence(seed).spawn(3)
        rng, cal_rng, eval_rng = [np.random.default_rng(s) for s in streams]
        entity = unit(rng.normal(size=(12, DIM))); times = unit(rng.normal(size=(2, DIM)))
        predicate = unit(rng.normal(size=(1, DIM)))[0]
        c = unit(entity[:, None, :] + times[None, :, :] + predicate)
        b = unit(rng.normal(size=(12, 2, DIM)))
        cal_noise = unit(cal_rng.normal(size=(16, 48)) + 1j * cal_rng.normal(size=(16, 48)))
        eval_noise = unit(eval_rng.normal(size=(32, 48)) + 1j * eval_rng.normal(size=(32, 48)))
        for key, val in [('entity', entity), ('time', times), ('predicate', predicate), ('context', c), ('binding', b), ('cal_noise', cal_noise), ('eval_noise', eval_noise)]:
            latent[f's{seed}_{key}'] = val
        for mode in MODES:
            for ratio in RATIOS:
                for role, cs, bs, noise, etas in [('cal', c[8:], b[8:], cal_noise, CAL_NOISE), ('eval', c[:8], b[:8], eval_noise, EVAL_NOISE)]:
                    records = encode(cs, bs, ratio, mode)
                    latent[f'{role}_s{seed}_{mode}_r{ratio}_records'] = records
                    for eta in etas:
                        queries[f'{role}_s{seed}_{mode}_r{ratio}_eta{eta}'] = unit(np.repeat(records[::3], 2, axis=0) + eta * noise)
    return latent, queries


def main(output_dir=None):
    start = time.monotonic()
    here = Path(__file__).resolve().parent
    out = Path(output_dir) if output_dir else here / 'runs' / datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    out.mkdir(parents=True, exist_ok=False)
    shutil.copy2(__file__, out / 'experiment.py')
    shutil.copy2(here / 'PROTOCOL.md', out / 'PROTOCOL.md')
    json_dump(out / 'frozen_manifest.json', {'source_sha256': sha(Path(__file__).read_bytes()),
        'protocol_sha256': sha((here / 'PROTOCOL.md').read_bytes()), 'seeds': SEEDS,
        'tolerance': TOL, 'numpy_version': np.__version__, 'blas_threads': {k: os.environ[k] for k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS')},
        'candidate_order': 'entity-major, time-major, status A/N/U',
        'noise': 'unit isotropic complex Gaussian direction scaled by eta before query normalization',
        'rng': 'SeedSequence(master).spawn(3): latent, calibration_noise, evaluation_noise; PCG64 default_rng',
        'S_definition': '.5*norm(q+w)^2/(Eq+Ew) * 2*sqrt(Eq*Ew)/(Eq+Ew); zero energy: 0'})
    latent, query_cache = prepare_inputs()
    np.savez_compressed(out / 'latent_noise_records.npz', **latent)
    np.savez_compressed(out / 'queries.npz', **query_cache)
    json_dump(out / 'frozen_query_hashes.json', {f'{key}_q{i}': array_hash(row) for key, a in query_cache.items() for i, row in enumerate(a)})
    json_dump(out / 'frozen_input_hashes.json', {name: sha((out / name).read_bytes()) for name in ('latent_noise_records.npz', 'queries.npz', 'frozen_query_hashes.json')})
    centres_log = []; aggregates = {}; controls = collections.Counter()
    controls['max_unit_norm_error'] = max(float(np.max(abs(np.linalg.norm(a, axis=-1) - 1))) for k, a in {**latent, **query_cache}.items() if k.endswith('_records') or k.endswith('_noise') or k.startswith(('cal_', 'eval_')))
    controls['max_complex_real_AB_error'] = 0.0
    controls['max_modulus_error'] = 0.0
    controls['max_angle_error'] = 0.0
    controls['max_S_cos_error'] = 0.0
    mismatch_details = []; query_uses = collections.Counter(); id_uses = collections.Counter()
    candidate_meta = [{'index': i, 'entity': i // 6, 'time': i // 3 % 2, 'status': STATUSES[i % 3]} for i in range(48)]
    json_dump(out / 'candidate_metadata.json', candidate_meta)
    with open(out / 'ledger.jsonl.gz', 'wb') as raw:
      with gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0) as gz:
       with io.TextIOWrapper(gz, encoding='utf-8', newline='\n') as ledger:
        for seed in SEEDS:
            for mode in MODES:
                cal_fits = {}
                for cr in RATIOS:
                    cw = latent[f'cal_s{seed}_{mode}_r{cr}_records']
                    for ce in CAL_NOISE:
                        cq = query_cache[f'cal_s{seed}_{mode}_r{cr}_eta{ce}']
                        for family in ('full', 'real_AB', 'binding'):
                            centres, diagnostics = fit_centres(cq, cw, family)
                            cal_fits[cr, ce, family] = centres
                            centres_log.append({'seed': seed, 'mode': mode, 'cal_ratio': cr, 'cal_noise': ce, 'family': family, 'diagnostics': diagnostics,
                                                'calibration_entities': [8, 9, 10, 11]})
                for er in RATIOS:
                    w = latent[f'eval_s{seed}_{mode}_r{er}_records']
                    for ee in EVAL_NOISE:
                        qkey = f'eval_s{seed}_{mode}_r{er}_eta{ee}'
                        q = query_cache[qkey]
                        norms = np.concatenate((np.linalg.norm(w, axis=1), np.linalg.norm(q, axis=1)))
                        controls['max_unit_norm_error'] = max(controls['max_unit_norm_error'], float(np.max(abs(norms - 1))))
                        h = products(q, w, 'full'); hab = products(q, w, 'real_AB'); hb = products(q, w, 'binding')
                        raw_h = q.conj() @ w.T
                        raw_ab = (q.real @ w.real.T + q.imag @ w.imag.T) + 1j * (q.real @ w.imag.T - q.imag @ w.real.T)
                        eq = np.sum(abs(q) ** 2, axis=-1)[:, None]
                        ew = np.sum(abs(w) ** 2, axis=-1)[None, :]
                        energy = eq + ew
                        factor_r = np.divide(2 * np.sqrt(eq * ew), energy, out=np.zeros_like(energy), where=energy > 0)
                        s_direct = np.divide(.5 * np.sum(abs(q[:, None, :] + w[None, :, :]) ** 2, axis=-1), energy, out=np.zeros_like(energy), where=energy > 0) * factor_r
                        s_cos = (1 + h.real) / 2
                        valid = (abs(h) > TOL) & (abs(hab) > TOL)
                        discrepancies = {'raw_complex_real_AB': abs(raw_h - raw_ab), 'complex_real_AB': abs(h - hab), 'modulus': abs(abs(h) - abs(hab)),
                                         'angle': abs(np.angle(h[valid] * np.conj(hab[valid]))), 'S_cos': abs(s_direct - s_cos)}
                        for key, values in discrepancies.items():
                            maximum = float(np.max(values)) if values.size else 0.0
                            controls[f'max_{key}_error'] = max(controls[f'max_{key}_error'], maximum)
                            controls[f'{key}_discrepancies_gt_tol'] += int(np.sum(values > TOL))
                        hs = {'full_cos_angle': h, 'full_mod_angle': h, 'real_AB_angle': hab, 'binding_mod_angle': hb}
                        ranks = {'full_cos_angle': rank(h.real), 'full_mod_angle': rank(abs(h)), 'real_AB_angle': rank(abs(hab)), 'binding_mod_angle': rank(abs(hb))}
                        for label, a, d, sa, sd in [('complex_vs_real_modulus', ranks['full_mod_angle'], ranks['real_AB_angle'], abs(h), abs(hab)), ('cosine_vs_S', ranks['full_cos_angle'], rank(s_direct), h.real, s_direct)]:
                            for qi in range(32):
                                gap_a = float(sa[qi, a[qi, 2]] - sa[qi, a[qi, 3]])
                                gap_d = float(sd[qi, d[qi, 2]] - sd[qi, d[qi, 3]])
                                mismatch = set(a[qi, :3]) != set(d[qi, :3])
                                controls[f'{label}_comparisons'] += 1
                                controls[f'{label}_near_boundary_count'] += int(min(gap_a, gap_d) <= TOL)
                                controls[f'{label}_top3_set_mismatches'] += int(mismatch)
                                if mismatch:
                                    mismatch_details.append({'comparison': label, 'query_id': f'{qkey}_q{qi}', 'top3_a': a[qi, :3].tolist(), 'top3_b': d[qi, :3].tolist(), 'boundary_gap_a': gap_a, 'boundary_gap_b': gap_d})
                        for cr in RATIOS:
                         for ce in CAL_NOISE:
                            condition = {'seed': seed, 'mode': mode, 'cal_ratio': cr, 'eval_ratio': er, 'cal_noise': ce, 'eval_noise': ee,
                                         'ratio_match': cr == er, 'noise_match': ce == ee}
                            decoded = {}
                            for method in METHODS:
                                family = 'binding' if method == 'binding_mod_angle' else 'real_AB' if method == 'real_AB_angle' else 'full'
                                decoded[method] = decode(hs[method], cal_fits[cr, ce, family])
                            for qi in range(32):
                                qid = f'{qkey}_q{qi}'; qhash = array_hash(q[qi]); scope = qi // 2
                                id_uses[qid] += 1; query_uses[qhash] += 1
                                row = {'evaluation_record_key': f's{seed}_{mode}_cr{cr}_er{er}_ce{ce}_ee{ee}_q{qi}',
                                       'query_id': qid, 'query_sha256': qhash, 'condition': condition, 'entity': scope // 2, 'time': scope % 2, 'repetition': qi % 2, 'methods': {}}
                                for method in METHODS:
                                    idx = ranks[method][qi, :3]; pred_all, reasons_all = decoded[method]
                                    predictions = pred_all[qi, idx]
                                    metrics = metric(idx, predictions, scope, pred_all[qi, scope * 3:scope * 3 + 3])
                                    row['methods'][method] = {'retrieved_indices': idx.tolist(), 'predictions': [STATUSES[p] if p < 3 else 'ABSTAIN' for p in predictions],
                                        'reasons': reasons_all[qi, idx].tolist(), 'relevant': (idx // 3 == scope).tolist(), 'metrics': metrics,
                                        'oracle_relevant_diagnostic': {'indices': list(range(scope * 3, scope * 3 + 3)), 'predictions': [STATUSES[p] if p < 3 else 'ABSTAIN' for p in pred_all[qi, scope * 3:scope * 3 + 3]], 'reasons': reasons_all[qi, scope * 3:scope * 3 + 3].tolist()}}
                                    key = tuple(condition[k] for k in ('seed', 'mode', 'cal_ratio', 'eval_ratio', 'cal_noise', 'eval_noise')) + (method,)
                                    acc = aggregates.setdefault(key, {'condition': dict(condition), 'method': method, 'n': 0, 'sums': collections.Counter(), 'denominators': collections.Counter()})
                                    acc['n'] += 1
                                    for name, value in metrics.items():
                                        if value is not None:
                                            acc['sums'][name] += value; acc['denominators'][name] += 1
                                ledger.write(json.dumps(row, allow_nan=False, separators=(',', ':')) + '\n')
                                controls['ledger_rows'] += 1
    assert controls['ledger_rows'] == 10368
    json_dump(out / 'centres.json', centres_log)
    full = []
    for value in aggregates.values():
        value['means'] = {k: value['sums'][k] / n for k, n in value['denominators'].items()}
        full.append(value)
    json_dump(out / 'aggregates_full_condition.json', full)
    summaries = []
    for fields in [('mode', 'cal_ratio', 'eval_ratio', 'cal_noise', 'eval_noise'), ('mode', 'ratio_match', 'noise_match'), ('mode',)]:
        grouped = {}
        for item in full:
            key = tuple(item['condition'][f] for f in fields) + (item['method'],)
            acc = grouped.setdefault(key, {'group_by': list(fields), 'condition': {f: item['condition'][f] for f in fields}, 'method': item['method'], 'n': 0, 'sums': collections.Counter(), 'denominators': collections.Counter()})
            acc['n'] += item['n']; acc['sums'].update(item['sums']); acc['denominators'].update(item['denominators'])
        for acc in grouped.values():
            acc['means'] = {k: acc['sums'][k] / n for k, n in acc['denominators'].items()}
            summaries.append(acc)
    json_dump(out / 'aggregates_summaries.json', {'caveat': 'Repeated paired constructed observations; 48 latent entity/time claims across seeds. No significance tests or population confidence intervals. Means are descriptive; full conditions and missing-centre diagnostics remain authoritative.', 'summaries': summaries})
    # Unique generated IDs exclude all calibration-condition duplication; hashes test actual bytes.
    eval_arrays = [(k, v) for k, v in query_cache.items() if k.startswith('eval_')]
    generated_hashes = collections.Counter(array_hash(row) for _, a in eval_arrays for row in a)
    cal_hashes = collections.Counter(array_hash(row) for k, a in query_cache.items() if k.startswith('cal_') for row in a)
    json_dump(out / 'query_reuse.json', {'generated_evaluation_query_ids': len(id_uses), 'ledger_query_uses': sum(id_uses.values()),
        'unique_evaluation_array_hashes': len(generated_hashes), 'generated_id_use_histogram': dict(collections.Counter(id_uses.values())),
        'generated_array_hash_multiplicity_histogram': dict(collections.Counter(generated_hashes.values())),
        'ledger_array_hash_use_histogram': dict(collections.Counter(query_uses.values())),
        'calibration_query_array_count': sum(cal_hashes.values()), 'unique_calibration_array_hashes': len(cal_hashes),
        'calibration_evaluation_hash_overlap': len(set(cal_hashes) & set(generated_hashes)),
        'query_id_uses': dict(id_uses), 'evaluation_array_hash_uses': dict(query_uses)})
    controls['calibration_entities'] = [8, 9, 10, 11]; controls['evaluation_entities'] = list(range(8))
    controls['calibration_evaluation_entity_overlap'] = 0
    controls['method_records'] = controls['ledger_rows'] * 4
    controls['top3_mismatch_details'] = mismatch_details
    controls['elapsed_seconds'] = time.monotonic() - start
    controls['runtime_cap_seconds'] = 180
    controls['runtime_cap_passed'] = controls['elapsed_seconds'] < 180
    json_dump(out / 'numerical_controls.json', dict(controls))
    json_dump(out / 'artifact_hashes.json', {p.name: sha(p.read_bytes()) for p in sorted(out.iterdir()) if p.is_file()})
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', help='New directory; default timestamped directory beside script under runs/')
    args = parser.parse_args()
    print(main(args.output_dir))
