from pathlib import Path
import json,hashlib,ast
import numpy as np
BASE=Path(__file__).resolve().parent.parent;source=BASE/'claude-open-world-intake-v1/sources/FRR/lineage/sources/claude-open-world-guard-2026-11-02/open_world_guard.py';ns={};exec(compile(ast.parse(source.read_text().split('# ---------------- PHASE 1')[0]),str(source),'exec'),ns)
def intervals(k,n):
 p=k/n;z=1.96;den=2*(n+z*z);mid=2*n*p+z*z;half=z*np.sqrt(z*z+4*n*p*(1-p));return (mid-half)/den,(mid+half)/den
for study in ['joint-noise-candidates-v1','offgrid-calibration-v1']:
 r=BASE/study
 if not (r/'SUMMARY.json').exists():continue
 raw=json.loads((r/'RAW.json').read_text());grid=np.array(raw['grid']);L=len(grid);params=json.loads((r/'PARAMETERS.json').read_text());lookup={(x['seed'],x['M'],x.get('cls',x.get('class')),x['noise']):x for x in params};summary=json.loads((r/'SUMMARY.json').read_text())['rows'];by={(x['seed'],x['M'],x['world'],x['noise'],x['arm']):x for x in summary};counts=0
 for c in raw['cells']:
  a,b=ns['gen'](c['world'],c['M'],300,np.random.default_rng(np.random.SeedSequence(c['eval_seed'])),c['noise']);assert hashlib.sha256(a.tobytes()+b.tobytes()).hexdigest()==c['observed_A_B_sha256'];F=ns['feats'](a,b)[0];Ds=[]
  for label in ['IND','DIFF','SHARED']:
   for noise in grid:
    par=lookup[c['seed'],c['M'],label,float(noise)];Ds.append((((F-np.array(par['mean']))/np.array(par['sd']))**2).mean(1)/par['threshold'])
  pair=np.stack(Ds,1)<=1;assert np.array_equal((pair*(1<<np.arange(3*L))).sum(1),c['pair_masks']);j={'IND':0,'DIFF':1,'COMMON':2}[c['world']];g=int(np.flatnonzero(grid==c['noise'])[0])
  for arm,d in c['arms'].items():
   if arm in ('union','dense_union'):allow=np.ones((300,L),bool)
   elif arm=='fixed':allow=np.tile(grid==.05,(300,1))
   elif arm=='oracle':allow=np.tile(grid==c['noise'],(300,1))
   elif arm=='coarse_union':allow=np.tile(np.isin(grid,[.025,.05,.1]),(300,1))
   else:
    n=40 if arm=='gold40' else 400 if arm=='gold400' else 4000;k=np.array(c['gold'+str(n)]);lo,hi=intervals(k,n);allow=(grid[None,:]>=lo[:,None])&(grid[None,:]<=hi[:,None])
    if arm=='coarse_gold4000':allow&=np.isin(grid,[.025,.05,.1])
   expectedallow=(allow*(1<<np.arange(L))).sum(1);stored=d.get('allowed_noise_masks',d.get('noise_masks'));assert np.array_equal(expectedallow,stored)
   filtered=pair&np.tile(allow,(1,3));bits=(filtered.reshape(-1,3,L).any(2)*np.array([1,2,4])).sum(1);assert np.array_equal(bits,d['class_masks']);lab=np.full(300,4);lab[bits==0]=3
   for bit,label in [(1,0),(2,1),(4,2)]:lab[bits==bit]=label
   assert np.array_equal(lab,d['labels']);row=by[c['seed'],c['M'],c['world'],c['noise'],arm]
   fields={'true_pair_compatible':filtered[:,j*L+g].mean(),'correct_singleton':(lab==j).mean(),'wrong_singleton':((lab<3)&(lab!=j)).mean(),'UNKNOWN':(lab==3).mean(),'UNRESOLVED':(lab==4).mean(),'calibration_grid_empty':(~allow.any(1)).mean(),'true_noise_retained':allow[:,g].mean()}
   for key,value in fields.items():assert abs(value-row[key])<1e-12
   counts+=300
  if study.startswith('joint'):assert np.all(np.array(c['gold400'])>=np.array(c['gold40']))
 if study.startswith('offgrid'):
  old=json.loads((BASE/'joint-noise-candidates-v1/PARAMETERS.json').read_text());old={(x['seed'],x['M'],x['cls'],x['noise']):x for x in old}
  for key,x in lookup.items():
   if key in old:
    for field in ['mean','sd','threshold']:assert x[field]==old[key][field]
 checks={'status':'pass','input_hashes_and_pair_masks_recomputed':len(raw['cells']),'arm_evaluations_reconstructed':counts,'gold_intervals_recomputed_with_equivalent_formula':True,'all_summary_metrics_recomputed':True,'parent_coarse_pairs_preserved':study.startswith('offgrid')}
 with (r/'AUDIT.json').open('x') as f:json.dump(checks,f,indent=2);f.write('\n')
 print(study,json.dumps(checks))
