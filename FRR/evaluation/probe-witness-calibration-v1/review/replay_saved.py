#!/usr/bin/env python3
"""Independent PW-C replay from SCHEMA.md; no experiment imports/source inspection."""
import os
for v in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'): os.environ[v]='1'
import hashlib,json
from pathlib import Path
import numpy as np
BASE=Path(__file__).resolve().parent.parent
RUN=BASE/'run'
TOL=1e-10
failures=[]; maxima={}; counts={}; strict=[]; membership=[]; category=[]
def check(ok,where):
 if not bool(ok): failures.append(where)
def near(a,b,where):
 a=np.asarray(a); b=np.asarray(b)
 if a.shape!=b.shape: failures.append(where+':shape');return
 e=float(np.max(np.abs(a-b))) if a.size else 0.; maxima[where.split(':')[0]]=max(maxima.get(where.split(':')[0],0),e)
 check(np.allclose(a,b,atol=2e-12,rtol=2e-12,equal_nan=True),where)
def rows(path): return [json.loads(s) for s in path.read_text().splitlines() if s.strip()]
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def digest(a):
 a=np.asarray(a);return hashlib.sha256(a.dtype.str.encode()+json.dumps(a.shape).encode()+a.tobytes(order='C')).hexdigest()
def apply(x,p):
 p=p.T
 return x.real@p.real-x.imag@p.imag+1j*(x.real@p.imag+x.imag@p.real)
def inner(q,c): return q.real@c.real.T+q.imag@c.imag.T+1j*(q.real@c.imag.T-q.imag@c.real.T)
def product(q,c):
 qn=np.linalg.norm(q,axis=1);cn=np.linalg.norm(c,axis=1)
 qu=np.divide(q,qn[:,None],out=np.zeros_like(q),where=qn[:,None]>TOL);cu=np.divide(c,cn[:,None],out=np.zeros_like(c),where=cn[:,None]>TOL)
 z=inner(qu,cu)
 valid=(qn[:,None]>TOL)&(cn[None,:]>TOL)&(np.abs(z)>TOL)
 return z,valid,qn,cn
def decode(z,valid,centres,available):
 lab=np.full(z.shape,'ABSTAIN',dtype='<U7');why=np.full(z.shape,'calibration_unavailable',dtype='<U23')
 if np.all(available):
  why[:]='zero_product'
  for ix in np.ndindex(z.shape):
   if valid[ix]:
    d=np.abs(np.angle(np.exp(1j*(np.angle(z[ix])-np.angle(centres)))))
    order=np.argsort(d,kind='stable')
    if d[order[1]]-d[order[0]]<=TOL: why[ix]='ambiguous_centre'
    else: lab[ix]=('A','N','U')[order[0]];why[ix]='ok'
 return lab,why

def main():
 global RUN
 import argparse
 pa=argparse.ArgumentParser();pa.add_argument('--run-dir',type=Path,default=RUN);args=pa.parse_args();RUN=args.run_dir
 manifest=json.loads((RUN/'CRSTATE_ARCHIVE_MANIFEST.json').read_text())
 for name in ('source_inputs.npz','selected_training.npz'):
  m=manifest['files']['run/'+name]; expected=m['sha256'];check(sha(RUN/name)==expected,'source_hash:'+name)
 source=np.load(RUN/'source_inputs.npz',allow_pickle=False);training=np.load(RUN/'selected_training.npz',allow_pickle=False)
 probes=np.load(RUN/'probe_inputs.npz',allow_pickle=False);w=np.load(RUN/'witness_inputs.npz',allow_pickle=False);fit=np.load(RUN/'fitted_calibration.npz',allow_pickle=False)
 outcome=np.load(RUN/'outcomes.npz',allow_pickle=False);mapping=json.loads((RUN/'OUTCOME_MAP.json').read_text())
 for key in outcome.files: check(key=='h'+digest(outcome[key]),'pool_hash:'+key)
 refs=[v for fields in mapping['conditions'].values() for v in fields.values()]
 check(set(refs)==set(outcome.files),'pool_exact_references');check(len(refs)==mapping['logical_arrays']==15360,'pool_logical_count');check(len(outcome.files)==mapping['unique_arrays'],'pool_unique_count')
 check(sum(outcome[k].nbytes for k in refs)==mapping['logical_array_bytes'],'pool_logical_bytes');check(sum(outcome[k].nbytes for k in outcome.files)==mapping['unique_array_bytes'],'pool_unique_bytes')
 check((RUN/'outcomes.npz').stat().st_size==mapping['artifact_bytes'],'pool_artifact_bytes');check(sha(RUN/'outcomes.npz')==mapping['artifact_sha256'],'pool_artifact_sha256')
 structures=rows(RUN/'STRUCTURAL_DIAGNOSTICS.jsonl');calibs=rows(RUN/'CALIBRATION_CONFIGS.jsonl')
 reconstructed={};raws={};expected_centres={};expected_available={}
 for d in structures:
  stem=d['key']
  seed=d['seed'];ai=stem.split('_')[1];probe=d['probe'];mode=d['witness_mode'];pst=f's{seed}_{ai}_{probe}';ws=f's{seed}_{probe}_{mode}'
  Q=source[f's{seed}_Q'][1];Dbase=training[f's{seed}_{ai}_differences'];nb=Dbase.copy();nb[:,12:]=0;sb=Dbase.copy();sb[:,:12]=0
  near(Dbase,(training[f's{seed}_{ai}_pairs'][:,0]-training[f's{seed}_{ai}_pairs'][:,1])/2,'source_aligned_difference:'+pst)
  near(Dbase[:,:12],(.5 if ai=='a3' else 1.5)*Dbase[:,12:],'source_aligned_blocks:'+pst)
  n=nb@Q.T;s=sb@Q.T;D=Dbase@Q.T;alpha,beta=probes[pst+'_coefficients'];Dp=(alpha*nb+beta*sb)@Q.T
  for tag,val in [('D',D),('n',n),('s',s),('Dprime',Dp)]:near(probes[pst+'_'+tag],val,'probe:'+pst+tag)
  anchor=np.eye(24)[[0,1,2,3,12,13,14,15]]@Q.T;near(w[ws+'_anchors'],anchor,'witness_anchor:'+ws)
  reading=w[ws+'_readings'];response=w[ws+'_responses'];near(np.sum(response*anchor,axis=1)/np.sum(anchor*anchor,axis=1),reading,'witness_scalar:'+ws)
  ah,bh=np.mean(reading[:4]),np.mean(reading[4:]);eps=w[ws+'_eps'];lo=np.array([max(reading[:4]-eps[0]),max(reading[4:]-eps[1])]);hi=np.array([min(reading[:4]+eps[0]),min(reading[4:]+eps[1])]);glo=lo[1]-hi[0];ghi=hi[1]-lo[0];gate=bool(np.all(lo<=hi) and (glo>TOL or ghi<-TOL))
  PB=Q[:,12:]@Q[:,12:].T
  for method,md in d['methods'].items():
   ms=stem+'_'+method
   if method=='BINDING_ORACLE': available=True;raw=s;p=PB
   else:
    a,b={'COEFF_ORACLE':(alpha,beta),'ADVERTISED':(-1.,1.),'POINT':(ah,bh),'GATED':(ah,bh)}[method]
    available=abs(b-a)>TOL and (method!='GATED' or gate)
    raw=(Dp-a*D)/(b-a) if available else None
    if available:
     u,sv,vh=np.linalg.svd(raw,full_matrices=False);rank=min(12,int(np.sum(sv>TOL)));basis=vh[:rank].T;p=basis@basis.conj().T
    else:p=np.zeros((24,24))
   check(md['available']==available,'available:'+ms);near(fit[ms+'_projector'],p,'projector:'+ms);reconstructed[ms]=p
   if available:
    sv_check=np.linalg.svd(raw,compute_uv=False);numeric_rank=int(np.sum(sv_check>TOL));retained=min(12,numeric_rank)
    near(md['singular_values'],sv_check,'singular_values:'+ms);check(md['numeric_rank']==numeric_rank,'numeric_rank:'+ms);check(md['retained_rank']==retained,'retained_rank:'+ms);check(md['available_rank_zero']==(retained==0),'available_rank_zero:'+ms)
    near(md['hermitian_residual'],np.linalg.norm(p-p.conj().T),'hermitian:'+ms);near(md['idempotent_residual'],np.linalg.norm(p@p-p),'idempotent:'+ms)
    near(fit[ms+'_raw_signal'],raw,'raw:'+ms);near(md['raw_relative_frobenius_error'],np.linalg.norm(raw-s)/np.linalg.norm(s),'raw_error:'+ms);near(md['raw_reconstructed_norm'],np.linalg.norm(raw),'raw_norm:'+ms);near(md['projector_binding_distance'],np.linalg.norm(p-PB)/np.sqrt(24),'Pdistance:'+ms)
    if method!='BINDING_ORACLE':
     near(md['raw_nuisance_coefficient'],(alpha-a)/(b-a),'nuisance_gain:'+ms);near(md['raw_signal_gain'],(beta-a)/(b-a),'signal_gain:'+ms)
   else:
    for field in ('raw_signal_key','raw_relative_frobenius_error','raw_reconstructed_norm','projector_binding_distance'):check(md[field] is None,'unavailable_null:'+ms+field)
    check(md['placeholder_rank']==0,'placeholder:'+ms)
 counts['structures']=len(structures)
 for c in calibs:
  stem=c['key'];ms=c['structure_key']+'_'+c['method'];seed=c['seed'];ri=0 if c['r']==.5 else 1;p=reconstructed[ms]
  rec=apply(source[f's{seed}_cal_records_r{ri}']@source[f's{seed}_Q'][1].T,p);q=rec[::3];allz,allv,qn,rn=product(q,rec);z=np.stack([allz[i,3*i:3*i+3] for i in range(8)]);valid=np.stack([allv[i,3*i:3*i+3] for i in range(8)])
  centres=np.zeros(3,complex);available=np.zeros(3,bool);cc=np.sum(valid,axis=0)
  for j in range(3):
   phases=z[valid[:,j],j];mean=np.mean(phases/np.abs(phases)) if len(phases) else 0j
   available[j]=bool(len(phases) and abs(mean)>TOL);centres[j]=mean
  expected_centres[stem]=centres;expected_available[stem]=available
  for tag,val in [('products',z),('query_norms',qn),('record_norms',rn)]:near(fit[stem+'_'+tag],val,'calibration_'+tag+':'+stem)
  for tag,val in [('valid',valid),('available',available),('counts',cc)]:check(np.array_equal(fit[stem+'_'+tag],val),'calibration_'+tag+':'+stem)
  near(fit[stem+'_centres'],centres,'calibration_centres:'+stem)
 counts['calibrations']=len(calibs)
 for condition,fields in mapping['conditions'].items():
  parts=condition.split('_');seed=int(parts[0][1:]);ri=int(parts[-2][1:]);ei=int(parts[-1][1:]);calstem='_'.join(parts[:-1]);ms='_'.join(parts[:-2]);p=reconstructed[ms]
  saved={k:outcome[v] for k,v in fields.items()}
  check(set(saved)=={'products','valid','scores','labels','reasons','top','query_norms','record_norms'},'mapping_fields:'+condition)
  for qi in range(32):check(np.array_equal(saved['top'][qi],np.argsort(-saved['scores'][qi],kind='stable')[:3]),'saved_stable_sort:'+condition+str(qi))
  queries=apply(source[f's{seed}_queries_r{ri}_e{ei}'][[0,31]]@source[f's{seed}_Q'][1].T,p);records=apply(source[f's{seed}_eval_records_r{ri}']@source[f's{seed}_Q'][1].T,p);z,valid,qn,rn=product(queries,records);scores=abs(z);lab,why=decode(z,valid,expected_centres[calstem],expected_available[calstem]);top=np.argsort(-scores,axis=1,kind='stable')[:,:3]
  for tag,val in [('products',z),('scores',scores),('query_norms',qn)]:near(saved[tag][[0,31]],val,'candidate_'+tag+':'+condition)
  near(saved['record_norms'],rn,'candidate_record_norms:'+condition)
  for tag,val in [('valid',valid),('labels',lab),('reasons',why)]:
   if not np.array_equal(saved[tag][[0,31]],val):category.append({'condition':condition,'field':tag,'mismatch_count':int(np.sum(saved[tag][[0,31]]!=val))})
  for ix,qi in enumerate((0,31)):
   got=saved['top'][qi]
   if not np.array_equal(got,top[ix]):
    ids=np.unique(np.concatenate([got,top[ix]]));strict.append({'condition':condition,'query':qi,'saved':got.tolist(),'replay':top[ix].tolist(),'candidate_scores':{str(int(i)):float(scores[ix,i]) for i in ids},'saved_scores':{str(int(i)):float(saved['scores'][qi,i]) for i in ids}})
   if set(got)!=set(top[ix]):membership.append({'condition':condition,'query':qi,'saved':got.tolist(),'replay':top[ix].tolist()})
 counts['method_conditions']=len(mapping['conditions']);counts['method_records']=2*counts['method_conditions'];counts['candidate_readouts']=48*counts['method_records'];counts['pool_arrays']=len(outcome.files)
 for name,want in [('structures',96),('calibrations',960),('method_conditions',1920),('method_records',3840),('candidate_readouts',184320)]:check(counts[name]==want,'count:'+name)
 report={'inspection':'Protocol, SCHEMA.md, original and copied saved arrays only; no experiment implementation/predecessor source inspected or imported.','counts':counts,'numeric_atol':2e-12,'numeric_rtol':2e-12,'decoder_tol':TOL,'failures':failures,'max_abs_errors':maxima,'strict_order_result':'PASS' if not strict else 'FAIL','strict_order_mismatches':strict,'membership_result':'PASS' if not membership else 'FAIL','membership_mismatches':membership,'fixed_id_categories_result':'PASS' if not category else 'FAIL','fixed_id_category_mismatches':category,'overall':'PASS' if not(failures or strict or membership or category) else 'FAIL'}
 (BASE/'review'/'REPLAY_REPORT.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'counts':counts,'failures':len(failures),'strict_order_mismatches':len(strict),'membership_mismatches':len(membership),'fixed_id_category_mismatches':len(category),'overall':report['overall']},indent=2))
if __name__=='__main__':main()
