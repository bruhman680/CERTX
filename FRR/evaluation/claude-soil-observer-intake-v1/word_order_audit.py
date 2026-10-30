"""Exact word-order audit: original reversible examples plus a chiral cycle rival."""
from pathlib import Path
import io,contextlib,builtins,itertools,json,hashlib,os
import numpy as np
P=Path(__file__).resolve().parent;O=P/'originals'
old='/tmp/claude-0/-home-claude/ed722431-0b93-5ef2-81ce-e6127e458ac9/scratchpad/soil_relay/soil_toy.py'
real=builtins.open

def op(file,*a,**kw):return real(O/'soil_toy.py' if str(file)==old else file,*a,**kw)
# Prefix-only load: neither PartA MonteCarlo nor PartB trajectory trial loop runs.
ns={};src=(O/'soil_finite_sample.py').read_text().split('# ---------------- PART A')[0]
builtins.open=op
try:
 with contextlib.redirect_stdout(io.StringIO()):exec(compile(src,str(O/'soil_finite_sample.py'),'exec'),ns)
finally:builtins.open=real

def table(M,pi,n):
 cur=pi[None,:]
 for _ in range(n):cur=np.concatenate([cur@M[0],cur@M[1]])
 return cur.sum(1)
def check(M,pi,n):
 t=table(M,pi,n);lsberr=msberr=0.
 for word in itertools.product([0,1],repeat=n):
  v=pi.copy()
  for bit in word:v=v@M[bit]
  direct=v.sum();lsb=sum(bit<<i for i,bit in enumerate(word));msb=sum(bit<<(n-1-i) for i,bit in enumerate(word));lsberr=max(lsberr,abs(t[lsb]-direct));msberr=max(msberr,abs(t[msb]-direct))
 return {'n':n,'max_lsb_index_error':float(lsberr),'max_msb_index_error':float(msberr)}
rows=[]
for name,kw in ns['W'].items():
 M,_,_=ns['build'](name,**kw);pi=ns['stationary'](M[0]+M[1]);rows.append({'world':name,**check(M,pi,5)})
cycle=[0,0,1,0,1,1];M=[np.zeros((6,6)),np.zeros((6,6))]
for i,bit in enumerate(cycle):M[bit][i,(i+1)%6]=1
rival=check(M,np.ones(6)/6,5)
result={'scope':'Exact prefix/code audit, not fullfinite-sample rerun or new agentexperiment','original_worlds':rows,'nonreversible_cycle':cycle,'rival':rival,'all_original_lsb_correct':all(x['max_lsb_index_error']<1e-12 for x in rows),'original_msb_also_matches_by_reversal_symmetry':all(x['max_msb_index_error']<1e-12 for x in rows),'rival_lsb_correct':rival['max_lsb_index_error']<1e-12,'rival_exposes_msb_mismatch':rival['max_msb_index_error']>.1,'original_code_changed':False}
assert all(result[k] for k in ['all_original_lsb_correct','original_msb_also_matches_by_reversal_symmetry','rival_lsb_correct','rival_exposes_msb_mismatch'])
assert not(P/'WORD_ORDER_AUDIT.json').exists();(P/'WORD_ORDER_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
