"""Paired source-pipeline control; read PROTOCOL.md before interpreting results."""
import ast
from fractions import Fraction as F
import hashlib
import json
import pathlib
import platform
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
SOURCE = HERE.parent / 'claude-open-world-intake-v1/sources/FRR/lineage/sources/claude-open-world-guard-2026-11-02/open_world_guard.py'
ROOT_SEED = 202611021937
WORLDS = ('IND', 'DIFF', 'COMMON', 'UPSTREAM', 'ANTI', 'LAG', 'DRIFT', 'PARTIAL', 'SWAP')
CLASSES = ('IND', 'DIFF', 'SHARED')
TRUTH = {'IND': 'IND', 'DIFF': 'DIFF', 'COMMON': 'SHARED', 'UPSTREAM': 'SHARED'}
N_FIT = N_CAL = 800
N_EVAL = 1000

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    pins = json.loads((HERE / 'INPUT_PINS.json').read_text())
    assert sha(SOURCE) == pins['source_sha256']
    assert sha(pathlib.Path(__file__)) == pins['runner_sha256']
    assert sha(HERE / 'PROTOCOL.md') == pins['protocol_sha256']
    prefix = SOURCE.read_text().split('# ---------------- PHASE 1')[0]
    tree = ast.parse(prefix)
    assert all(isinstance(n, (ast.Import, ast.ImportFrom, ast.Assign, ast.FunctionDef)) for n in tree.body if not isinstance(n, ast.Expr))
    # The only Expr allowed here is the source's inert module docstring.
    assert all(isinstance(n.value, ast.Constant) and isinstance(n.value.value, str) for n in tree.body if isinstance(n, ast.Expr))
    ns = {}
    exec(compile(tree, str(SOURCE), 'exec'), ns)
    gen, feats, care = ns['gen'], ns['feats'], ns['care_claim_world']
    q = F(23, 100)
    joint = F(81, 100) * F(2, 25) + F(9, 500) + F(1, 400)
    phi = (joint - q*q)/(q*(1-q))
    assert joint == F(853, 10000)
    assert phi == F(324, 1771) and phi < F(1, 4)
    assert joint/q == F(853, 2300) < F(3, 5)
    root = np.random.SeedSequence(ROOT_SEED)
    rows, parameters, seed_records, raw = [], {}, {}, {}
    with (HERE / 'evaluations.jsonl').open('w') as out:
        for M, mseed in zip((100, 400, 1600), root.spawn(3)):
            children = mseed.spawn(6 + 2*len(WORLDS))
            refs = []
            parameters[str(M)] = {}
            for k, (label, world) in enumerate(zip(CLASSES, ('IND', 'DIFF', 'COMMON'))):
                fit_seed, cal_seed = children[2*k:2*k+2]
                f1 = feats(*gen(world, M, N_FIT, np.random.default_rng(fit_seed)))[0]
                mu, sd = f1.mean(0), np.maximum(f1.std(0), .001)
                f2 = feats(*gen(world, M, N_CAL, np.random.default_rng(cal_seed)))[0]
                threshold = float(np.quantile((((f2-mu)/sd)**2).mean(1), .99))
                refs.append((mu, sd, threshold))
                parameters[str(M)][label] = dict(mu=mu.tolist(), sd=sd.tolist(), threshold=threshold,
                    fit_seed_spawn_key=list(fit_seed.spawn_key), calibration_seed_spawn_key=list(cal_seed.spawn_key))
            for j, world in enumerate(WORLDS):
                eval_seed, care_seed = children[6+2*j:8+2*j]
                seed_records[f'{M}_{world}'] = dict(eval_spawn_key=list(eval_seed.spawn_key), care_spawn_key=list(care_seed.spawn_key))
                a, b = gen(world, M, N_EVAL, np.random.default_rng(eval_seed))
                seed_records[f'{M}_{world}']['observed_A_B_sha256'] = hashlib.sha256(a.tobytes(order='C')+b.tobytes(order='C')).hexdigest()
                raw[f'M{M}_{world}_A'], raw[f'M{M}_{world}_B'] = a, b
                features = feats(a, b)[0]
                distances = np.stack([(((features-mu)/sd)**2).mean(1)/threshold for mu,sd,threshold in refs], 1)
                compatible = distances <= 1
                counts = compatible.sum(1)
                sets = np.full(N_EVAL, 'UNRESOLVED', dtype='<U16')
                sets[counts == 0] = 'UNKNOWN'
                single = counts == 1
                sets[single] = np.array(CLASSES)[compatible[single].argmax(1)]
                original = care(world, a, b, M, np.random.default_rng(care_seed)).astype('<U16')
                mapped = original.copy()
                mapped[np.isin(original, ['COMMON', 'COPY'])] = 'SHARED'
                mapped[original == 'UNRES_INDDIFF'] = 'UNRESOLVED'
                masks = (compatible.astype(np.uint8) * np.array([1,2,4], dtype=np.uint8)).sum(1).astype(np.uint8)
                assert np.all((sets == 'UNKNOWN') == (counts == 0))
                assert np.all((sets == 'UNRESOLVED') == (counts > 1))
                key = f'M{M}_{world}'
                raw[key+'_features'], raw[key+'_distances'], raw[key+'_mask'] = features, distances, masks
                raw[key+'_care_original'], raw[key+'_care'], raw[key+'_set'] = original, mapped, sets
                truth = TRUTH.get(world)
                summary = dict(M=M, world=world, truth=truth, n=N_EVAL,
                    mean_phi=float(features[:,0].mean()), mean_OR_trend=float(features[:,5].mean()),
                    multiple_candidates=float((counts > 1).mean()))
                for method, labels in [('care', mapped), ('compatibility', sets)]:
                    specific = np.isin(labels, CLASSES)
                    summary[method] = dict(fractions={str(v):float((labels == v).mean()) for v in (*CLASSES, 'UNKNOWN', 'UNRESOLVED')},
                        correct_specific=None if truth is None else float((labels == truth).mean()),
                        wrong_specific=float((specific & (labels != truth)).mean()))
                # Paired differences use identical runs, not independent-arm samples.
                wrong_care = np.isin(mapped, CLASSES) & (mapped != truth)
                wrong_set = np.isin(sets, CLASSES) & (sets != truth)
                summary['paired_wrong_counts'] = {'care_only':int((wrong_care & ~wrong_set).sum()),
                    'compatibility_only':int((wrong_set & ~wrong_care).sum()), 'both':int((wrong_care & wrong_set).sum())}
                rows.append(summary)
                for i in range(N_EVAL):
                    out.write(json.dumps(dict(M=M, world=world, run=i,
                        min_normalized_distance=float(distances[i].min()), candidate_mask=int(masks[i]),
                        care_original=str(original[i]), care=str(mapped[i]), compatibility=str(sets[i])), separators=(',',':'))+'\n')
    np.savez_compressed(HERE / 'evaluations.npz', **raw)
    result = dict(scope='Source reuse, paired CPU toy; no empirical coverage guarantee', root_seed=ROOT_SEED,
        python=platform.python_version(), numpy=np.__version__, classes=list(CLASSES),
        mask_bits={'IND':1,'DIFF':2,'SHARED':4}, source_sha256=sha(SOURCE),
        exact_checks={'DIFF_joint':str(joint), 'DIFF_phi':str(phi), 'DIFF_conditional':str(joint/q)}, rows=rows)
    by = {(r['M'], r['world']):r for r in rows}
    result['prediction_checks'] = {
        'P1_DIFF_care_wrong_increases':by[1600,'DIFF']['care']['wrong_specific'] > by[100,'DIFF']['care']['wrong_specific'],
        'P2_DIFF_set_wrong_at_most_05_and_lower':by[1600,'DIFF']['compatibility']['wrong_specific'] <= .05 and by[1600,'DIFF']['compatibility']['wrong_specific'] < by[1600,'DIFF']['care']['wrong_specific'],
        'P3_some_multiple_at_M100':any(r['multiple_candidates'] > 0 for r in rows if r['M']==100),
        'P4_SWAP_unknown_increases':by[1600,'SWAP']['compatibility']['fractions']['UNKNOWN'] > by[400,'SWAP']['compatibility']['fractions']['UNKNOWN']}
    (HERE / 'PARAMETERS.json').write_text(json.dumps(dict(root_seed=ROOT_SEED, classes=parameters, evaluation_seeds=seed_records), indent=2)+'\n')
    (HERE / 'SUMMARY.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
