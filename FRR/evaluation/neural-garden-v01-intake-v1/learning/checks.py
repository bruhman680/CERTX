"""Bounded audit of inspected pinned source and retained JSON. No checkpoints loaded."""
from pathlib import Path
import hashlib,json,sys,time
import numpy as np
H=Path(__file__).resolve().parent; S=H/'sources';sys.path.insert(0,str(S))
def read(n):return json.loads((S/n).read_text())
def dump(n,d):
 with (H/n).open('x') as f:json.dump(d,f,indent=2,allow_nan=False);f.write('\n')
online=read('NEXT_ONLINE_AUDIT_results.json')
stability=read('STABILITY2_holdout_results.json')
memory=read('MEMORY2_SAFETY_results.json')
print({n:list(d) for n,d in [('online',online),('stability',stability),('memory',memory)]},flush=True)
from NEXT_ONLINE_probe import summarize,one_seed
from STABILITY2_probe import one
computed=summarize(online['rows'])
assert computed==online['summary']
assert len(online['rows'])==12 and all(r['paired_online_minus_frozen_energy']<0 for r in online['rows'])
assert len(stability['rows'])==8
for name,stats in stability['summary'].items():
 values=[r['conditions'][name]['energy'] for r in stability['rows']]
 assert abs(float(np.mean(values))-stats['energy'])<1e-14
 if name!='frozen':assert all(r['conditions'][name]['energy']<r['conditions']['frozen']['energy'] for r in stability['rows'])
ms={}
for regime in ('stable','mild'):
 ms[regime]={}
 for mode in ('protected','latest','composite','safety'):
  vals=[];scores=[]
  for row in memory['rows']:
   key={'protected':'protected','latest':'1600','composite':row['selected_composite'],'safety':row['selected_safety']}[mode]
   arr=row['testing'][regime][key];vals.extend(arr);scores.append(float(np.mean([v['score'] for v in arr])))
  m={k:float(np.mean([v[k] for v in vals])) for k in ('energy','floor','score')}
  for k,v in m.items():assert abs(v-memory['summary'][regime][mode][k])<1e-14
  ms[regime][mode]=m
source_checks={}
for key,expected in online.get('source_sha256',{}).items():
 if (S/key).exists():source_checks[key]=hashlib.sha256((S/key).read_bytes()).hexdigest()==expected
assert all(source_checks.values())
dump('ROW_AUDIT.json',{'status':'pass','online_summary_exact':True,'online_seed_count':12,
 'online_energy_wins':computed['online_energy_paired_wins'],'online_energy_delta':computed['online_minus_frozen_energy_mean'],
 'stability_holdout_seeds':8,'all_radius_arms_lose_to_frozen_each_seed':True,
 'memory_safety_recomputed':ms,'available_source_hash_checks':source_checks,
 'scope':'Arithmetic/source checks of supplied rows, not independent replication of all simulations.'})
started=time.perf_counter()
seed=online['rows'][0]['seed']
rep=one_seed(seed)
old=next(r for r in online['rows'] if r['seed']==seed)
def maxdiff(a,b):
 if isinstance(a,dict):
  assert a.keys()==b.keys();return max((maxdiff(a[k],b[k]) for k in a),default=0.)
 if isinstance(a,list):
  assert len(a)==len(b);return max((maxdiff(x,y) for x,y in zip(a,b)),default=0.)
 if isinstance(a,(float,int)) and not isinstance(a,bool):return abs(a-b)
 assert a==b;return 0.
d=maxdiff(rep,old);assert d<1e-12,d
ss=stability['rows'][0]['seed']; sr=one(ss);so=next(r for r in stability['rows'] if r['seed']==ss)
sd=maxdiff(sr,so);assert sd<1e-12,sd
dump('BOUNDED_REPRODUCTION.json',{'status':'pass','online_audit_seed':seed,'online_max_absolute_row_difference':d,
 'stability_holdout_seed':ss,'stability_max_absolute_row_difference':sd,
 'elapsed_seconds':time.perf_counter()-started,'online_row':rep,'stability_row':sr,
 'scope':'One previously published seed reproduced per protocol with inspected code and fresh synthetic worlds. Not new heldout confirmatory evidence, no remote pickle load or canonical run used.'})
print({'reproduction':'pass','online_seed':seed,'stability_seed':ss,'online_diff':d,'stability_diff':sd},flush=True)
