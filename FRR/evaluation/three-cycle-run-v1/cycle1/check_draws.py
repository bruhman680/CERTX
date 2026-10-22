"""Deterministic provenance replay: expose absolute outcome samples, no retuning."""
from pathlib import Path
import json,hashlib
import numpy as np
D=Path(__file__).resolve().parent
src=D.parents[1]/'soil-reset-robustness-v1'/'RESULTS.json'
j=json.loads(src.read_text());saved=json.loads((D/'RESULTS.json').read_text());lookup={(x['design'],x['n'],x['world'],x['rep']):x for x in saved['replicates'] if x['mode']=='known'}
rng=np.random.default_rng(2026102201);out=[];maxerr=0
for design,arms in [('diverse',['sham','agent','soil']),('redundant',['sham','shared','shared'])]:
 X=np.array([[1-j['resets'][a]['rates'][0],1-j['resets'][a]['rates'][1]] for a in arms])
 for n in (100,1000,10000):
  for kind in ('shadow','echo','wake','mixed'):
   model=j['models'][kind+'_additive']; means=np.array([[model['responses'][a]['baseline_error'][0]+model['responses'][a][f'forced{y}_minus_no_probe'][0] for y in (0,1)] for a in arms]);base=np.array([model['responses'][a]['baseline_error'][0] for a in arms])
   for rep in range(200):
    counts=rng.binomial(n,means);witness=rng.binomial(n,X);xh=witness/n
    if design=='redundant':xh[1:]=xh[1:].mean(0)
    row=lookup[design,n,kind,rep];maxerr=max(maxerr,float(np.max(abs(counts[:,1]/n-counts[:,0]/n-np.array(row['observed_contrasts'])))),float(np.max(abs(xh-np.array(row['witness_survival'])))))
    out.append({'design':design,'arms':arms,'n':n,'world':kind,'rep':rep,'population_forced0_forced1_probabilities':means.tolist(),'no_probe_same_reset_probabilities':base.tolist(),'outcome1_counts_for_forced0_forced1':counts.tolist(),'coordinate_survival_counts':witness.tolist()})
with (D/'DRAW_LEDGER.jsonl').open('w') as f:
 for x in out:f.write(json.dumps(x,separators=(',',':'))+'\n')
check={'scope':'Deterministic replay of same seeded synthetic draws; independent bookkeeping check, not independent stochastic replication','draw_groups':len(out),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'max_saved_vs_replayed_error':maxerr,'all_true_candidates_retained':all(x['true_candidate_retained'] for x in saved['replicates']),'all_continuous_intervals_cover_truth':all(x['covered'] for x in saved['replicates'] if x['covered'] is not None),'checks':{'replay_matches_saved_outputs':maxerr<1e-15,'same_reset_probabilities_valid':all(all(0<=p<=1 for p in x['no_probe_same_reset_probabilities']) for x in out),'groups_4800':len(out)==4800}}
(D/'CHECKS.json').write_text(json.dumps(check,indent=2)+'\n');print(json.dumps(check,indent=2));assert all(check['checks'].values())
