"""Boundary diagnostics after the original numeric run. No semantics test."""
from pathlib import Path
import sys,json,copy,subprocess
import numpy as np
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P));from experiment import weights,incremental,full,ident
sys.path.insert(0,str(P.parents[1]/'tools'))
from cache_replay_plan import plan,token_digest,IDENTITY_FIELDS
base=list(range(1,25));identity=ident(3)
c={'token_ids':base,'cache_token_count':24,'prefix_sha256':token_digest(base),'execution_identity':identity}
r={'token_ids':base+[62],'execution_identity':identity}
checks=[]
for marker in ['unknown',' Unavailable ','UNSPECIFIED','  ']:
 a,b=copy.deepcopy(c),copy.deepcopy(r)
 a['execution_identity']['model_revision']=marker;b['execution_identity']['model_revision']=marker
 d=plan(a,b);checks.append({'case':'unknown_marker:'+repr(marker),'reuse':d['reuse_prefix_tokens'],'pass':d['reuse_prefix_tokens']==0})
for field in IDENTITY_FIELDS:
 a,b=copy.deepcopy(c),copy.deepcopy(r);b['execution_identity'][field]='changed'
 d=plan(a,b);checks.append({'case':'changed_identity:'+field,'reuse':d['reuse_prefix_tokens'],'pass':d['reuse_prefix_tokens']==0})
# A valid token/identity manifest cannot authenticate the actual cache tensors.
w=weights(3);_,cache=incremental(base,w);cache[0][1][0,:]+=5
out,_=incremental([62],w,cache);truth=full(base+[62],w)
error=float(np.max(np.abs(out[-1]-truth[-1])))
d=plan(c,r)
assert d['reuse_prefix_tokens']==24 and error>1e-10
request=P/'CLI_EXAMPLE.json';request.write_text(json.dumps({'cached':c,'requested':r},indent=2)+'\n')
cli=subprocess.run([sys.executable,str(P.parents[1]/'tools/cache_replay_plan.py'),str(request)],capture_output=True,text=True)
assert cli.returncode==0 and json.loads(cli.stdout)==d
checks.append({'case':'cli_matches_library','pass':True})
assert all(x['pass'] for x in checks)
result={'scope':'Post-development boundary diagnostics; not independent model validation','checks':checks,'valid_metadata_wrong_tensor':{'plan_reuses_tokens':24,'max_logit_error':error,'interpretation':'Planner cannot inspect/authenticate tensor state; backend must bind actual cache artifact and verify execution contract.'},'no_new_token_case':'Planner may return an empty replay when everything is already cached. A generation backend must retain last-token logits or replay that token to obtain logits; planner does not supply logits.'}
(P/'SUPPLEMENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checks':len(checks),'all_pass':True,'wrong_tensor_error':error}))
