import json, runpy
from pathlib import Path
p=Path(__file__).resolve().parents[1]
module=runpy.run_path(str(p/'tools/check_package.py'))
schema=json.loads((p/'state/schema.json').read_text())
record=json.loads((p/'state/empty.json').read_text())
results=[]
for name,change in [('missing_seed',lambda r:r.pop('seed')),('wrong_version',lambda r:r.update(version='9')),('unexpected_field',lambda r:r.update(hidden_reasoning='x')),('wrong_claim_type',lambda r:r.update(claims='invalid'))]:
 r=json.loads(json.dumps(record));change(r)
 try:
  module['check'](r,schema,name)
  raise RuntimeError(f'Invalid record accepted: {name}')
 except AssertionError: results.append({'test':name,'outcome':'rejected as expected'})
# Pointwise convergence does not imply uniform convergence on positive integers.
for n in [10,100,1000]:
 values=[int(k==n) for k in [1,2,3]]
 assert values==[0,0,0]
 assert int(n==n)==1
results.append({'test':'moving_spike','outcome':'fixed k in {1,2,3} vanish; supremum remains 1','scope':'exact constructed counterexample, not an empirical result'})
# Escaping minimizer: f_n(x)=(x-n)^2/n^2, min at x=n.
rows=[]
for n in [10,100,1000]:
 f=lambda x:(x-n)**2/n**2
 assert f(n)==0
 rows.append({'n':n,'f_n(2)':f(2),'minimum':f(n),'minimizer':n})
results.append({'test':'escaping_minimizer','outcome':rows,'scope':'numeric illustration; exact formulas establish the counterexample'})
# Omitted battery distinguishes future starting behavior under the same READY display.
states=[{'display':'READY','charged':True},{'display':'READY','charged':False}]
assert states[0]['display']==states[1]['display']
assert [s['charged'] for s in states]==[True,False]
results.append({'test':'compression_start','outcome':'same displayed macrostate, different start outcomes','scope':'constructed deterministic model'})
# Untreated probabilities agree, intervention responses differ.
groups={'A':{'untreated':0.5,'treated':0.9},'B':{'untreated':0.5,'treated':0.1}}
assert groups['A']['untreated']==groups['B']['untreated']
assert groups['A']['treated']!=groups['B']['treated']
results.append({'test':'prediction_vs_intervention','outcome':groups,'scope':'constructed probabilities; no clinical evidence'})
(p/'evaluation/results').mkdir(exist_ok=True)
(p/'evaluation/results/local-contact.json').write_text(json.dumps({'kind':'local structural checks and constructed mathematical contact','model_comparison':False,'results':results},indent=2)+'\n')
print(json.dumps(results,indent=2))
