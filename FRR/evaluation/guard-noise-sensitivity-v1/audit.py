"""Check candidate decisions and regenerate paired-noise inputs; no model calls."""
from pathlib import Path
import ast,json,hashlib
import numpy as np
R=Path(__file__).resolve().parent
source=R.parent/'claude-open-world-intake-v1/sources/FRR/lineage/sources/claude-open-world-guard-2026-11-02/open_world_guard.py'
ns={};exec(compile(ast.parse(source.read_text().split('# ---------------- PHASE 1')[0]),str(source),'exec'),ns)
v=json.loads((R/'RAW_COMPACT.json').read_text());s=json.loads((R/'SUMMARY.json').read_text());by={(x['seed'],x['M'],x['world'],x['noise'],x['quantile']):x for x in s['rows']};inputs={};count=0
for c in v['rows']:
 key=(c['seed'],c['M'],c['world'],c['noise']);row=by[(*key,c['quantile'])];D=np.array(c['normalized_distances']);bits=((D<=1)*np.array([1,2,4])).sum(1);assert np.array_equal(bits,c['candidate_masks'])
 expected=np.full(500,4);expected[bits==0]=3
 for bit,label in [(1,0),(2,1),(4,2)]:expected[bits==bit]=label
 assert np.array_equal(expected,c['labels']);j={'IND':0,'DIFF':1,'COMMON':2}[c['world']]
 for k,val in [('true_class_compatible',float(((bits&(1<<j))!=0).mean())),('correct_singleton',float((expected==j).mean())),('wrong_singleton',float(((expected<3)&(expected!=j)).mean())),('UNKNOWN',float((expected==3).mean())),('UNRESOLVED',float((expected==4).mean()))]:assert val==row[k]
 if key not in inputs:
  a,b=ns['gen'](c['world'],c['M'],500,np.random.default_rng(np.random.SeedSequence(c['evaluation_seed'])),c['noise']);assert hashlib.sha256(a.tobytes()+b.tobytes()).hexdigest()==c['observed_A_B_sha256'];inputs[key]=(a,b)
 count+=500
nested=0
for seed in (2026110301,2026110302):
 for M in (400,1600):
  for world,j in [('IND',0),('DIFF',1),('COMMON',2)]:
   latent=ns['gen'](world,M,500,np.random.default_rng(np.random.SeedSequence([seed,M,j,3])),0)
   previous=[np.zeros_like(latent[0]),np.zeros_like(latent[1])]
   for eps in (.025,.05,.10):
    pair=inputs[seed,M,world,eps]
    for side in (0,1):
     flips=pair[side]^latent[side];assert not np.any(previous[side]&~flips);previous[side]=flips
   nested+=1
result={'status':'pass','threshold_decisions_checked':count,'observed_input_hashes_regenerated':len(inputs),'nested_noise_flip_sets_checked':nested,'scope':'36 input cells regenerate in recorded NumPy runtime; cross-version regeneration remains unverified'}
with (R/'AUDIT.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(result))
