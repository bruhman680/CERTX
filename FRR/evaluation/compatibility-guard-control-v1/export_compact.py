"""Post-run publication export; no further simulation or selection."""
import hashlib
import json
import pathlib
import numpy as np

r = pathlib.Path(__file__).resolve().parent
s = json.loads((r/'SUMMARY.json').read_text())
p = json.loads((r/'PARAMETERS.json').read_text())
z = np.load(r/'evaluations.npz', allow_pickle=False)
vocabulary = ['IND', 'DIFF', 'SHARED', 'UNKNOWN', 'UNRESOLVED', 'COMMON', 'COPY', 'UNRES_INDDIFF']
code = {v:i for i,v in enumerate(vocabulary)}
cells = []
for row in s['rows']:
    M, world = row['M'], row['world']
    key = f'M{M}_{world}'
    cells.append(dict(M=M, world=world, observed_A_B_sha256=p['evaluation_seeds'][f'{M}_{world}']['observed_A_B_sha256'],
        candidate_mask=z[key+'_mask'].tolist(), min_normalized_distance=z[key+'_distances'].min(1).tolist(),
        care_original=[code[v] for v in z[key+'_care_original']], care=[code[v] for v in z[key+'_care']],
        compatibility=[code[v] for v in z[key+'_set']]))
out = dict(label_vocabulary=vocabulary, candidate_bits={'IND':1,'DIFF':2,'SHARED':4},
    local_npz_sha256=hashlib.sha256((r/'evaluations.npz').read_bytes()).hexdigest(), cells=cells)
(r/'EVALUATIONS_COMPACT.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
print((r/'EVALUATIONS_COMPACT.json').stat().st_size)
