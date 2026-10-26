import os
for n in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[n]='1'
import numpy as np,json,hashlib,re
from pathlib import Path
P=Path(__file__).resolve().parents[1];R=P/'run';O=P/'review';T=1e-10;A=2e-12
S=np.load(R/'source_inputs.npz');D=np.load(R/'selected_training.npz');B=np.load(R/'probe_inputs.npz');C=np.load(R/'structures_centres.npz');POOL=np.load(R/'outcomes.npz')
load=lambda f:json.load(open(R/f));M=load('OUTCOME_MAP.json');SS=load('STRUCTURAL_DIAGNOSTICS.json');CC=load('CALIBRATION_CONFIGS.json');err=[];mx={};checks=0;Ps={};fits={};cal={};sel=[]
def check(k,a,b):
 global checks
 checks+=1;a=np.asarray(a);b=np.asarray(b)
 if a.shape!=b.shape:err.append([k,'shape',str(a.shape),str(b.shape)]);return
 if a.dtype.kind in 'USbiu':
  n=int(np.count_nonzero(a!=b))
  if n:err.append([k,'discrete',n,np.argwhere(a!=b).tolist()[:3]])
 else:
  d=float(np.max(np.abs(a-b),initial=0));f=k.split(':')[-1];mx[f]=max(mx.get(f,0),d)
  if not np.allclose(a,b,atol=A,rtol=A,equal_nan=True):err.append([k,'numeric',d])
def fit(x):
 u,s,v=np.linalg.svd(x.T,full_matrices=False);n=int(np.sum(s>T));k=min(n,12);return (u[:,:k]@u[:,:k].T if k else np.zeros((24,24))),s,n,k
nd=lambda a,b:np.linalg.norm(a-b)/np.sqrt(24)
probes={'COPY':(1,1),'CONTEXT_FLIP':(-1,1),'PARTIAL_CONTEXT':(-.5,1),'SIGNAL_FLIP':(1,-1),'GLOBAL_FLIP':(-1,-1)}
check('map:conditions',len(M['conditions']),960);check('map:logical_arrays',sum(map(len,M['conditions'].values())),7680);check('map:unique',len(POOL.files),M['unique_arrays'])
for k in POOL.files:
 a=POOL[k];check('hash:'+k,k,'h'+hashlib.sha256(a.dtype.str.encode()+json.dumps(a.shape).encode()+a.tobytes()).hexdigest())
for row in SS:
 seed,ai,m,probe=row['seed'],3 if row['delta']==.5 else 4,row['m'],row['probe'];prefix=f's{seed}_a{ai}_{probe}';stem=row['stem'];q=S[f's{seed}_Q'][1];x=D[f's{seed}_a{ai}_differences'];alpha,beta=probes[probe]
 check(stem+':source_difference',x,np.diff(D[f's{seed}_a{ai}_pairs'][:,::-1],axis=1)[:,0]/2)
 first=x@q.T;second=(x*np.r_[np.full(12,alpha),np.full(12,beta)])@q.T;av=(first+second)/2;identified=abs(beta-alpha)>T;sol=(second-alpha*first)/(beta-alpha) if identified else np.zeros_like(first)
 pb=q@np.diag(np.r_[np.zeros(12),np.ones(12)])@q.T
 if probe=='GLOBAL_FLIP':target=np.zeros((24,24))
 elif probe=='SIGNAL_FLIP':target=q@np.diag(np.r_[np.ones(12),np.zeros(12)])@q.T
 else:
  t=row['delta']*{'COPY':1,'CONTEXT_FLIP':0,'PARTIAL_CONTEXT':.25}[probe];I=np.eye(12);target=q@np.block([[t*t*I,t*I],[t*I,I]])@q.T/(1+t*t)
 check(stem+':analytic_target',target,C[stem+'_analytic_target']);check(stem+':identified',identified,row['identified_operator']);ff={}
 for field,v in {'first':first,'second':second,'average':av,'solved':sol}.items():
  check(stem+':raw_'+field,v,B[prefix+'_'+field]);p,s,n,k=fit(v[:m]);ff[field]=p;check(stem+':'+field+'_projector',p,C[stem+'_'+field+'_projector']);check(stem+':'+field+'_singular_values',s,C[stem+'_'+field+'_singular_values']);saved=row['fit'][field]
  for key,value in {'numerical_rank':n,'retained_rank':k,'normalized_singular_values':s/s[0] if s[0] else np.zeros_like(s),'hermitian_error':np.linalg.norm(p-p.T),'idempotent_error':np.linalg.norm(p@p-p)}.items():check(stem+':'+field+'_'+key,value,saved[key])
 p0,pp,pa,ps=[ff[k] for k in ('first','second','average','solved')]
 for f,v in {'ambient_relative_change':np.linalg.norm(second[:m]-first[:m])/np.linalg.norm(first[:m]),'base_probe_distance':nd(p0,pp),'average_base_distance':nd(pa,p0),'average_binding_distance':nd(pa,pb),'average_target_distance':nd(pa,target)}.items():check(stem+':'+f,v,row[f])
 if identified:
  for f in ('solved_target_distance','solved_binding_distance'):check(stem+':'+f,nd(ps,pb),row[f])
 else:check(stem+':solved_zero',nd(ps,np.zeros_like(ps)),row['solved_zero_placeholder_distance'])
 fits[stem]=ff
 for method,p in {'full':np.eye(24),'oracle':pb,'repaired':pa,'solved':ps}.items():Ps[stem+'_'+method+'_projector']=p;check(stem+':'+method+'_projector',p,C[stem+'_'+method+'_projector'])
for seed in (92501,92507,92509):
 for ai in (3,4):
  for m in (12,48):
   f=lambda p:fits[f's{seed}_a{ai}_{p}_m{m}'];k=f'{seed}/{ai}/{m}'
   check(k+':context_signal_span',f('CONTEXT_FLIP')['second'],f('SIGNAL_FLIP')['second']);check(k+':global_base_span',f('GLOBAL_FLIP')['second'],f('GLOBAL_FLIP')['first']);check(k+':global_zero',f('GLOBAL_FLIP')['average'],np.zeros((24,24)))
def products(queries,records,p):
 a=queries@p.T;b=records@p.T;an=np.linalg.norm(a,axis=1);bn=np.linalg.norm(b,axis=1);aa=np.zeros_like(a);bb=np.zeros_like(b);va=an>T;vb=bn>T;aa[va]=a[va]/an[va,None];bb[vb]=b[vb]/bn[vb,None];z=aa.conj()@bb.T
 return z,va[:,None]&vb[None,:]&(np.abs(z)>T),an,bn
Ps={k:C[k] for k in Ps} # Supplemental diagnostic: saved-projector readout, not independent fit claim.
for cfg in CC:
 k=cfg['key'];seed,ri=cfg['seed'],cfg['ri'];q=S[f's{seed}_Q'][1];records=S[f's{seed}_cal_records_r{ri}']@q.T;z,v,an,bn=products(records[::3],records,Ps[cfg['projector_key']]);ix=np.arange(8)[:,None]*3+np.arange(3);z=z[np.arange(8)[:,None],ix];v=v[np.arange(8)[:,None],ix];count=v.sum(0);cent=np.array([np.mean(z[v[:,j],j]/np.abs(z[v[:,j],j])) if count[j] else 0j for j in range(3)]);available=(count>0)&(np.abs(cent)>T)
 for f,a in {'centres':cent,'available':available,'calibration_products':z,'calibration_valid':v,'calibration_valid_counts':count,'calibration_query_norms':an,'calibration_record_norms':bn}.items():check(k+':'+f,a,C[k+'_'+f])
 cal[k]=(cent,available)
def decode(z,v,c,available):
 lab=np.full(z.shape,'ABSTAIN',dtype='<U7');why=np.full(z.shape,'calibration_unavailable',dtype='<U23')
 if not np.all(available):return lab,why
 why[:]='zero_product';dist=np.abs(np.angle(np.exp(1j*(np.angle(z)[...,None]-np.angle(c)))));order=np.argsort(dist,axis=-1,kind='stable');sd=np.take_along_axis(dist,order,-1);tie=sd[...,1]-sd[...,0]<=T;why[v&tie]='ambiguous_centre';good=v&~tie;lab[good]=np.array(['A','N','U'])[order[...,0][good]];why[good]='ok';return lab,why
ledger={}
with open(R/'LEDGER.jsonl') as fh:
 for line in fh:
  row=json.loads(line)
  if row['query_index'] in (0,31):ledger[(row['outcome_key'],row['query_index'])]=row
for k,fields in M['conditions'].items():
 match=re.fullmatch(r's(\d+)_a([34])_(.+)_m(12|48)_r([01])_(full|oracle|repaired|solved)_e([01])',k);seed,ai,probe,m,ri,method,ei=match.groups();seed=int(seed);base=k.rsplit('_e',1)[0];stem=f's{seed}_a{ai}_{probe}_m{m}';q=S[f's{seed}_Q'][1];p=Ps[stem+'_'+method+'_projector'];queries=S[f's{seed}_queries_r{ri}_e{ei}']@q.T;records=S[f's{seed}_eval_records_r{ri}']@q.T;z,v,an,bn=products(queries,records,p);labels,reasons=decode(z,v,*cal[base]);scores=np.abs(z);top=np.argsort(-scores,axis=1,kind='stable')[:,:3];ix=[0,31]
 for f,a in {'products':z[ix],'valid':v[ix],'scores':scores[ix],'labels':labels[ix],'reasons':reasons[ix],'top':top[ix],'query_norms':an[ix],'record_norms':bn}.items():
  saved=POOL[fields[f]];check(k+':'+f,a,saved if f=='record_norms' else saved[ix])
 for qi in ix:
  row=ledger[(k,qi)];sel.append({'condition':k,'query_index':qi,'query_id':row['query_id']});key=k+f'/q{qi}';check(key+':query_identity',row['query_id'],f'{seed}-r{ri}-e{ei}-q{qi:02d}');t=top[qi];check(key+':returned_indices',t,row['returned_indices']);check(key+':returned_labels',labels[qi,t],row['predictions']);check(key+':returned_reasons',reasons[qi,t],row['reasons']);ids=[f'eval-e{int(j)//6}-t{(int(j)//3)%2}-{["A","N","U"][int(j)%3]}' for j in t];check(key+':returned_record_ids',ids,row['returned_record_ids']);rel=3*int(S[f's{seed}_query_claim_index'][qi])+np.arange(3);check(key+':oracle_relevant_predictions',labels[qi,rel],row['oracle_relevant_predictions']);check(key+':oracle_relevant_reasons',reasons[qi,rel],row['oracle_relevant_reasons']);order=np.argsort(-scores[qi],kind='stable');gap=float(scores[qi,order[2]]-scores[qi,order[3]]);check(key+':boundary_gap',gap,row['boundary_gap']);check(key+':near_boundary_tie',gap<=T,row['near_boundary_tie'])
check('coverage:selected',len(sel),1920);check('coverage:ledger',len(ledger),1920)
report={'status':'PASS' if not err else 'FAIL','coverage':{'structural':len(SS),'calibration':len(CC),'method_conditions':len(M['conditions']),'selected_method_records':len(sel),'candidate_readouts':len(sel)*48,'content_addressed_arrays':len(POOL.files)},'checks':checks,'atol':A,'rtol':A,'decision_threshold':T,'max_abs_by_field':mx,'errors':err,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'implementation_source_read':False,'implementation_imports':False,'inspection_disclosure':'Read initial/updated declarative SCHEMA.md and PROTOCOL.md; read raw source/training/probe/structure/outcome NPZ, structural/calibration JSON, output map and selected ledger records. No experiment.py or predecessor implementation read/import.'}
(O/'REPLAY_SELECTION_SUPPLEMENT.json').write_text(json.dumps(sel,indent=2)+'\n');(O/'REPLAY_SAVED_PROJECTOR_RESULT.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('errors','max_abs_by_field')},indent=2));print('errors',len(err),json.dumps(err[:15],indent=2))
