"""Source-checked candidate only: no model calls, no live activation, no new controls."""
from pathlib import Path
import ast,hashlib,json,math
import numpy as np
H=Path(__file__).resolve().parent
F=H.parent.parent
SOURCE=F/'lineage/sources/claude-errata-intake-2026-10-22/boltz_check.py'
def kernel(beta):
 states=[(x,e) for x in range(4) for e in range(2)]
 energies=np.array([.5*x+.3*e for x,e in states]);rates=np.zeros((8,8))
 for i,(x,e) in enumerate(states):
  for j,(u,v) in enumerate(states):
   if abs(x-u)+abs(e-v)==1:rates[i,j]=math.exp(-beta*max(energies[j]-energies[i],0))
 z=1.05*max(rates.sum(axis=1));p=rates/z
 for i in range(8):p[i,i]=1-p[i].sum()
 return states,energies,p,z

def check():
 # Import only the retained data/rates definitions, excluding the script's
 # printing and experiments. Archived original is never edited.
 tree=ast.parse(SOURCE.read_text());body=[]
 for node in tree.body:
  if isinstance(node,ast.Expr) and isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Name) and node.value.func.id=='print':break
  body.append(node)
 scope={};exec(compile(ast.Module(body=body,type_ignores=[]),str(SOURCE),'exec'),scope)
 checks=[]
 for beta in (.5,1.,2.,5.):
  states,energies,p,z=kernel(beta)
  k=scope['rates'](beta);ref=k/(1.05*k.sum(axis=1).max());ref[np.diag_indices(8)]=1-ref.sum(axis=1)
  assert np.allclose(p,ref,rtol=0,atol=3e-16)
  assert np.all(np.isfinite(p)) and np.all(p>=0) and np.max(np.abs(p.sum(1)-1))<3e-16
  pi=np.exp(-beta*energies);pi/=pi.sum();flux=pi[:,None]*p
  assert np.max(np.abs(pi@p-pi))<3e-16 and np.max(np.abs(flux-flux.T))<3e-16
  A=p.T-np.eye(8);A[-1]=1;b=np.zeros(8);b[-1]=1;sol=np.linalg.solve(A,b)
  assert np.max(np.abs(sol-pi))<2e-15
  checks.append(dict(beta=beta,row_sum_error=float(np.max(np.abs(p.sum(1)-1))),stationary_error=float(np.max(np.abs(sol-pi))),detailed_balance_error=float(np.max(np.abs(flux-flux.T))),shared_normalizer=float(z)))
 result=dict(status='pass',candidate='Archived eight-state four-by-two thermal ladder; user identity clarification pending',source=str(SOURCE.relative_to(F)),source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),states=states,checks=checks,agent_controls_in_source=False,transition_matrix_exposed_to_model=False,model_calls=0,live_cursor=750,live_activated=False)
 (H/'CANDIDATE_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':check()
