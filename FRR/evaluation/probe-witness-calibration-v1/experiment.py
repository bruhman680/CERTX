#!/usr/bin/env python3
"""Independent prospective PW implementation. No predecessor imports."""
import os
for name in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'): os.environ[name]='1'
import argparse, hashlib, json, shutil
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'context-perturbation-repair-v1'
SEEDS=(92501,92507,92509)
PROBES={'CONTEXT':(-1.,1.),'WEAK':(.9,1.),'SIGNAL':(1.,-1.),'COPY':(1.,1.)}
MODES={'EXACT':([0.]*4,[0.]*4,0.,0.),'BOUNDED':([.04,.03,.02,.01],[-.01,-.02,-.03,-.04],.05,.05),'BETA_GAIN_ERROR':([0.]*4,[.1]*4,0.,.12),'INVALID_SHARED_BIAS':([.12]*4,[-.12]*4,.02,.02)}
METHODS=('BINDING_ORACLE','COEFF_ORACLE','ADVERTISED','POINT','GATED')
TOL=1e-10
LABELS=np.array(['A','N','U'])
def filehash(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ah(a):
 a=np.ascontiguousarray(a); return hashlib.sha256(a.dtype.str.encode()+json.dumps(a.shape).encode()+a.tobytes()).hexdigest()
def meta(a): return {'dtype':a.dtype.str,'shape':list(a.shape),'sha256_dtype_shape_bytes':ah(a)}
def savejson(path,obj): Path(path).write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n')
def writejsonl(path,rows):
 with Path(path).open('w') as f:
  for row in rows: f.write(json.dumps(row,allow_nan=False,separators=(',',':'))+'\n')
def verify_sources():
 manifest=json.loads((SOURCE/'STATE_ARCHIVE_MANIFEST.json').read_text()); result={}
 for name in ('source_inputs.npz','selected_training.npz'):
  p=SOURCE/'run'/name; expected=manifest['files']['run/'+name]
  assert filehash(p)==expected['sha256'],name
  assert p.stat().st_size==expected['bytes'],name
  result[name]={'sha256':filehash(p),'bytes':p.stat().st_size,'manifest_entry':'run/'+name}
 return result

def interval(y,eps):
 lo=float(np.max(y-eps)); hi=float(np.min(y+eps)); mean=float(np.mean(y))
 return {'lower':lo,'upper':hi,'nonempty':lo<=hi,'mean':mean,'mean_in_interval':lo<=mean<=hi}
def witness_inference(ya,yb,ea,eb):
 A=interval(ya,ea); B=interval(yb,eb); nonempty=A['nonempty'] and B['nonempty']
 lo=B['lower']-A['upper']; hi=B['upper']-A['lower']; margin=min(abs(lo),abs(hi)) if nonempty and (lo>0 or hi<0) else 0.; gate=nonempty and margin>TOL
 return {'alpha_interval':A,'beta_interval':B,'a_hat':A['mean'],'b_hat':B['mean'],'point_gap':B['mean']-A['mean'],'compatible_gap_range':[lo,hi],'min_absolute_gap':margin,'gate_passed':gate,'gate_reason':'ok' if gate else ('empty_witness_set' if not nonempty else 'witness_set_not_separated')}
def fit(raw):
 _,s,vh=np.linalg.svd(raw,full_matrices=False); numeric=int(np.sum(s>TOL)); rank=min(12,numeric)
 P=vh[:rank].T@vh[:rank].conj() if rank else np.zeros((24,24),complex)
 return P,{'numeric_rank':numeric,'retained_rank':rank,'singular_values':s.tolist(),'rank_cutoff':TOL,'hermitian_residual':float(np.linalg.norm(P-P.conj().T)),'idempotent_residual':float(np.linalg.norm(P@P-P))}
def products(queries,records,P):
 q=queries@P.T; r=records@P.T; qn=np.linalg.norm(q,axis=1); rn=np.linalg.norm(r,axis=1)
 q=np.divide(q,qn[:,None],out=np.zeros_like(q),where=qn[:,None]>TOL)
 r=np.divide(r,rn[:,None],out=np.zeros_like(r),where=rn[:,None]>TOL)
 z=q.conj()@r.T
 real=q.real@r.real.T+q.imag@r.imag.T+1j*(q.real@r.imag.T-q.imag@r.real.T); err=float(np.max(abs(z-real)))
 valid=(qn[:,None]>TOL)&(rn[None,:]>TOL)&(abs(z)>TOL)
 return z,valid,qn,rn,err

def calibrate(records,P):
 z,valid,qn,rn,err=products(records[::3],records,P); ix=np.arange(8)[:,None]*3+np.arange(3)[None,:]
 zz=np.take_along_axis(z,ix,axis=1); vv=np.take_along_axis(valid,ix,axis=1); phases=np.divide(zz,abs(zz),out=np.zeros_like(zz),where=vv); counts=vv.sum(axis=0)
 centres=np.divide(phases.sum(axis=0),counts,out=np.zeros(3,complex),where=counts>0); available=(counts>0)&(abs(centres)>TOL)
 return {'centres':centres,'available':available,'counts':counts,'products':zz,'valid':vv,'query_norms':qn,'record_norms':rn},err
def decode(z,valid,cal):
 labels=np.full(z.shape,'ABSTAIN',dtype='<U7'); reasons=np.full(z.shape,'zero_product',dtype='<U24')
 if not np.all(cal['available']): reasons[:]='calibration_unavailable'; return labels,reasons
 distance=abs(np.angle(np.exp(1j*(np.angle(z)[:,:,None]-np.angle(cal['centres']))))); order=np.argsort(distance,axis=2,kind='stable'); best=np.take_along_axis(distance,order,axis=2); ambiguous=best[:,:,1]-best[:,:,0]<=TOL; good=valid&~ambiguous
 labels[good]=LABELS[order[:,:,0][good]]; reasons[good]='ok'; reasons[valid&ambiguous]='ambiguous_centre'; return labels,reasons
def metrics(top,labels,reasons,claim):
 relevant=np.arange(3)+claim*3; hit=top//3==claim; correct=labels[top]==LABELS[top%3]; joint=hit&correct; rc=labels[relevant]==LABELS; why,counts=np.unique(reasons[top][labels[top]=='ABSTAIN'],return_counts=True)
 return {'evidence_count':int(hit.sum()),'evidence_recall':float(hit.sum()/3),'evidence_complete':bool(hit.all()),'joint_label_count':int(joint.sum()),'joint_label_recall':float(joint.sum()/3),'joint_label_complete':bool(joint.all()),'wrongscope':int((~hit).sum()),'encoded_U_recall':int(np.any((top==relevant[2])&correct)),'abstain_count':int(np.sum(labels[top]=='ABSTAIN')),'abstain_reasons':dict(zip(why.tolist(),counts.tolist())),'oracle_relevant_stance_count':int(rc.sum()),'oracle_relevant_stance_accuracy':float(rc.mean())}
class Pool:
 def __init__(self): self.arrays={}; self.logical=0; self.logical_bytes=0
 def add(self,a):
  a=np.ascontiguousarray(a); key='h'+ah(a)
  if key in self.arrays:
   old=self.arrays[key]; assert old.dtype==a.dtype and old.shape==a.shape and old.tobytes()==a.tobytes()
  else: self.arrays[key]=a.copy()
  self.logical+=1; self.logical_bytes+=a.nbytes; return key

def fixture_checks():
 assert not interval(np.array([0.,1.]),.1)['nonempty']
 assert witness_inference(np.zeros(4),np.ones(4),0.,0.)['gate_passed']
 assert not witness_inference(np.zeros(4),np.zeros(4),0.,0.)['gate_passed']
 P,d=fit(np.zeros((48,24))); assert d['retained_rank']==0 and np.count_nonzero(P)==0
 print(json.dumps({'independent_nonexperimental_fixtures':'PASS','source_fit':False}))

def main(out):
 if out.exists(): raise FileExistsError('Output must be fresh; preserve every attempt')
 out.mkdir(parents=True); verified=verify_sources()
 for name in verified: shutil.copyfile(SOURCE/'run'/name,out/name)
 shutil.copyfile(SOURCE/'STATE_ARCHIVE_MANIFEST.json',out/'CRSTATE_ARCHIVE_MANIFEST.json')
 source=np.load(out/'source_inputs.npz',allow_pickle=False); train=np.load(out/'selected_training.npz',allow_pickle=False)
 savejson(out/'INPUT_MANIFEST.json',{'source_commit':'fe043657d412ea8626e975182fe19b97df0d44f5','files':verified,'array_hash_scheme':'SHA256(dtype.str UTF8 + json.dumps(shape) UTF8 + contiguous C bytes); distinct from predecessor original str(dtype)+str(shape)+bytes and local rawbytes schemes','source_arrays':{k:meta(source[k]) for k in source.files},'training_arrays':{k:meta(train[k]) for k in train.files}})
 probes={}; witnesses={}; witness_rows=[]; structural=[]; fitted={}; cals={}; calrows=[]; querymanifest={}
 for seed in SEEDS:
  Q=source[f's{seed}_Q'][1]; assert np.max(abs(Q.T@Q-np.eye(24)))<1e-12; anchors=np.eye(24)[[0,1,2,3,12,13,14,15]]@Q.T
  for probe,(alpha,beta) in PROBES.items():
   for mode,(ae,be,ea,eb) in MODES.items():
    key=f's{seed}_{probe}_{mode}'; ya=alpha+np.array(ae); yb=beta+np.array(be); y=np.r_[ya,yb]; responses=y[:,None]*anchors; dot=np.sum(responses*anchors.conj(),axis=1)/np.sum(anchors*anchors.conj(),axis=1); assert np.max(abs(dot-y))<1e-12
    witnesses[key+'_anchors']=anchors; witnesses[key+'_responses']=responses; witnesses[key+'_readings']=y; witnesses[key+'_errors']=np.r_[ae,be]; witnesses[key+'_eps']=np.array([ea,eb]); w=witness_inference(ya,yb,ea,eb); A=w['alpha_interval']; B=w['beta_interval']; coverage=A['lower']<=alpha<=A['upper'] and B['lower']<=beta<=B['upper']
    w.update({'key':key,'seed':seed,'probe':probe,'witness_mode':mode,'true_alpha':alpha,'true_beta':beta,'true_gap':beta-alpha,'true_pair_covered':bool(coverage),'individual_bound_coverage':((y-np.r_[np.full(4,ea),np.full(4,eb)]<=np.r_[np.full(4,alpha),np.full(4,beta)])&(np.r_[np.full(4,alpha),np.full(4,beta)]<=y+np.r_[np.full(4,ea),np.full(4,eb)])).tolist(),'scalar_anchor_max_error':float(np.max(abs(dot-y))),'false_identification_under_actual_model':bool(w['gate_passed'] and abs(beta-alpha)<=TOL),'oracle_relative_withholding':bool(not w['gate_passed'] and abs(beta-alpha)>TOL),'inversion_amplification':1/abs(w['point_gap']) if abs(w['point_gap'])>TOL else None}); witness_rows.append(w)
    direct_gate=A['nonempty'] and B['nonempty'] and (B['lower']-A['upper']>TOL or A['lower']-B['upper']>TOL)
    assert w['gate_passed']==direct_gate
    assert w['true_pair_covered']==(mode!='INVALID_SHARED_BIAS')
  for ai,delta in ((3,.5),(4,1.5)):
   base=train[f's{seed}_a{ai}_differences']; pairs=train[f's{seed}_a{ai}_pairs']; assert base.shape==(48,24) and np.max(abs((pairs[:,0]-pairs[:,1])/2-base))<1e-12
   assert np.max(abs(base[:,:12]-delta*base[:,12:]))<1e-12
   assert np.max(abs(np.linalg.norm(base[:,12:],axis=1)-1/np.sqrt(2)))<1e-12
   n=base.copy(); n[:,12:]=0; s=base.copy(); s[:,:12]=0
   for probe,(alpha,beta) in PROBES.items():
    stem=f's{seed}_a{ai}_{probe}'; probes[stem+'_D']=base@Q.T; probes[stem+'_n']=n@Q.T; probes[stem+'_s']=s@Q.T; probes[stem+'_Dprime']=(alpha*n+beta*s)@Q.T; probes[stem+'_coefficients']=np.array([alpha,beta])
 np.savez_compressed(out/'probe_inputs.npz',**probes); np.savez_compressed(out/'witness_inputs.npz',**witnesses); writejsonl(out/'WITNESS_DIAGNOSTICS.jsonl',witness_rows)
 savejson(out/'PRE_FIT_CHECKPOINT.json',{'phase':'before_any_source_fit','files':{n:filehash(out/n) for n in ('source_inputs.npz','selected_training.npz','CRSTATE_ARCHIVE_MANIFEST.json','INPUT_MANIFEST.json','probe_inputs.npz','witness_inputs.npz','WITNESS_DIAGNOSTICS.jsonl')},'probe_arrays':{k:meta(v) for k,v in probes.items()},'witness_arrays':{k:meta(v) for k,v in witnesses.items()}})
 wlookup={(w['seed'],w['probe'],w['witness_mode']):w for w in witness_rows}; methodinfo={}; productchecks=[]
 for seed in SEEDS:
  Q=source[f's{seed}_Q'][1]; PB=Q[:,12:]@Q[:,12:].T
  for ai,delta in ((3,.5),(4,1.5)):
   for probe,(alpha,beta) in PROBES.items():
    pkey=f's{seed}_a{ai}_{probe}'; D=probes[pkey+'_D']; Dp=probes[pkey+'_Dprime']; true=probes[pkey+'_s']; n=probes[pkey+'_n']
    for mode in MODES:
     key=pkey+'_'+mode; w=wlookup[seed,probe,mode]; diag={'key':key,'seed':seed,'delta':delta,'probe':probe,'witness_mode':mode,'methods':{}}
     for method in METHODS:
      mk=key+'_'+method; reason='ok'; a=b=None; raw=None
      if method=='BINDING_ORACLE': P=PB.copy(); raw=true.copy(); _,info=fit(raw)
      else:
       a,b=((alpha,beta) if method=='COEFF_ORACLE' else ((-1.,1.) if method=='ADVERTISED' else (w['a_hat'],w['b_hat'])))
       if method=='GATED' and not w['gate_passed']: reason=w['gate_reason']
       elif abs(b-a)<=TOL: reason='true_operator_singular' if method=='COEFF_ORACLE' else 'estimated_operator_singular'
       if reason=='ok': raw=(Dp-a*D)/(b-a); P,info=fit(raw)
       else: P=np.zeros((24,24),complex); _,info=fit(np.zeros((48,24)))
      available=reason=='ok'; fitted[mk+'_projector']=P
      if available: fitted[mk+'_raw_signal']=raw
      fitted[mk+'_singular_values']=np.array(info['singular_values']); nc=0. if method=='BINDING_ORACLE' else ((alpha-a)/(b-a) if available else None); sc=1. if method=='BINDING_ORACLE' else ((beta-a)/(b-a) if available else None); identity=float(np.max(abs(raw-(nc*n+sc*true)))) if available else None
      if available: assert identity<1e-12
      info.update({'available':available,'availability_reason':reason,'placeholder_rank':None if available else 0,'raw_signal_key':mk+'_raw_signal' if available else None,'raw_relative_frobenius_error':float(np.linalg.norm(raw-true)/np.linalg.norm(true)) if available else None,'raw_reconstructed_norm':float(np.linalg.norm(raw)) if available else None,'raw_nuisance_coefficient':nc,'raw_signal_gain':sc,'coefficient_identity_error':identity,'projector_binding_distance':float(np.linalg.norm(P-PB)/np.sqrt(24)) if available else None,'available_rank_zero':bool(available and info['retained_rank']==0),'a_used':a,'b_used':b}); diag['methods'][method]=info; methodinfo[mk]=info
      if mode=='BETA_GAIN_ERROR' and method in ('POINT','GATED') and abs(beta-alpha)>TOL:
       info['beta_gain_span_check']=bool(info['projector_binding_distance']<1e-12 and abs(nc)<1e-12 and abs(sc-1)>1e-12)
       assert info['beta_gain_span_check']
      for ri in (0,1):
       ck=mk+f'_r{ri}'; records=source[f's{seed}_cal_records_r{ri}']@Q.T; cal,err=calibrate(records,P); cals[ck]=cal
       for field,val in cal.items(): fitted[ck+'_'+field]=val
       calrows.append({'key':ck,'structure_key':key,'method':method,'seed':seed,'delta':delta,'probe':probe,'witness_mode':mode,'r':(.5,2)[ri],'available':cal['available'].tolist(),'counts':cal['counts'].tolist(),'complex_vs_real_error':err})
     structural.append(diag)
 np.savez_compressed(out/'fitted_calibration.npz',**fitted); writejsonl(out/'STRUCTURAL_DIAGNOSTICS.jsonl',structural); writejsonl(out/'CALIBRATION_CONFIGS.jsonl',calrows)
 savejson(out/'PRE_SCORING_CHECKPOINT.json',{'phase':'all_fits_and_calibration_saved_before_scoring','files':{n:filehash(out/n) for n in ('fitted_calibration.npz','STRUCTURAL_DIAGNOSTICS.jsonl','CALIBRATION_CONFIGS.jsonl')},'structures':len(structural),'calibrations':len(calrows)})
 pool=Pool(); mapping={}; ledger=[]; paired={}; aggregates=[]; controls={}
 for seed in SEEDS:
  Q=source[f's{seed}_Q'][1]; claims=source[f's{seed}_query_claim_index']; repetitions=source[f's{seed}_query_repetition']
  for ai,delta in ((3,.5),(4,1.5)):
   for probe in PROBES:
    for mode in MODES:
     for method in METHODS:
      mk=f's{seed}_a{ai}_{probe}_{mode}_{method}'; info=methodinfo[mk]; P=fitted[mk+'_projector']; w=wlookup[seed,probe,mode]
      for ri in (0,1):
       ck=mk+f'_r{ri}'; records=source[f's{seed}_eval_records_r{ri}']@Q.T
       for ei in (0,1):
        condition=ck+f'_e{ei}'; queries=source[f's{seed}_queries_r{ri}_e{ei}']@Q.T; z,valid,qn,rn,err=products(queries,records,P); labels,reasons=decode(z,valid,cals[ck]); scores=abs(z); top=np.argsort(-scores,axis=1,kind='stable')[:,:3]; arrays={'products':z,'valid':valid,'scores':scores,'labels':labels,'reasons':reasons,'top':top,'query_norms':qn,'record_norms':rn}; mapping[condition]={field:pool.add(value) for field,value in arrays.items()}; productchecks.append({'condition':condition,'complex_vs_real_error':err}); assert err<1e-12; metricrows=[]
        for qi in range(32):
         claim=int(claims[qi]); tt=top[qi]; relevant=np.arange(3)+claim*3; order=np.argsort(-scores[qi],kind='stable'); gap=float(scores[qi,order[2]]-scores[qi,order[3]]); qid=f's{seed}_r{ri}_e{ei}_q{qi}'
         if qid not in querymanifest: querymanifest[qid]={'query_id':qid,'seed':seed,'r_index':ri,'noise_index':ei,'claim_index':claim,'entity_index':claim//2,'time_index':claim%2,'repetition':int(repetitions[qi]),'base_array_hash':ah(source[f's{seed}_queries_r{ri}_e{ei}'][qi]),'paired_uses':0,'method_uses':0}
         querymanifest[qid]['method_uses']+=1; mt=metrics(tt,labels[qi],reasons[qi],claim); metricrows.append(mt)
         row={'index':len(ledger),'condition':condition,'outcome_key':condition,'seed':seed,'delta':delta,'probe':probe,'witness_mode':mode,'method':method,'r':(.5,2)[ri],'eval_noise':(0.,1.5)[ei],'query_index':qi,'query_id':qid,'claim_index':claim,'query_repetition':int(repetitions[qi]),'available':info['available'],'availability_reason':info['availability_reason'],'placeholder_rank':info['placeholder_rank'],'numeric_rank':info['numeric_rank'],'retained_rank':info['retained_rank'],'gate_passed':w['gate_passed'],'true_pair_covered':w['true_pair_covered'],'false_identification_under_actual_model':w['false_identification_under_actual_model'],'oracle_relative_withholding':w['oracle_relative_withholding'],'returned_indices':tt.tolist(),'returned_record_ids':[f's{seed}_claim{int(i)//3}_{LABELS[int(i)%3]}' for i in tt],'returned_products':[[float(x.real),float(x.imag)] for x in z[qi,tt]],'returned_scores':scores[qi,tt].tolist(),'predictions':labels[qi,tt].tolist(),'reasons':reasons[qi,tt].tolist(),'oracle_relevant_predictions':labels[qi,relevant].tolist(),'oracle_relevant_reasons':reasons[qi,relevant].tolist(),'third_fourth_gap':gap,'exact_boundary_tie':gap==0.,'near_boundary':gap<=TOL,'within_top3_gaps':np.diff(-scores[qi,tt]).tolist(),'metrics':mt}; ledger.append(row)
         pk=f's{seed}_a{ai}_{probe}_{mode}_r{ri}_e{ei}_q{qi}'
         if pk not in paired: paired[pk]={'key':pk,'query_id':qid,'method_indices':{}}; querymanifest[qid]['paired_uses']+=1
         paired[pk]['method_indices'][method]=row['index']
         if method in ('BINDING_ORACLE','COEFF_ORACLE'):
          controlkey=(seed,ai,probe,ri,ei,qi,method); payload={k:row[k] for k in ('returned_indices','predictions','reasons','oracle_relevant_predictions','oracle_relevant_reasons','metrics')}
          if controlkey in controls: assert payload==controls[controlkey]
          else: controls[controlkey]=payload
        numeric=[k for k in metricrows[0] if k!='abstain_reasons']; ag={'condition':condition,'count':32,'sums':{k:sum(x[k] for x in metricrows) for k in numeric},'means':{k:sum(x[k] for x in metricrows)/32 for k in numeric}}; ag['abstain_reasons']={reason:sum(x['abstain_reasons'].get(reason,0) for x in metricrows) for reason in ('calibration_unavailable','ambiguous_centre','zero_product')}; aggregates.append(ag)
 np.savez_compressed(out/'outcomes.npz',**pool.arrays)
 savejson(out/'OUTCOME_MAP.json',{'conditions':mapping,'hash_encoding':'SHA256(dtype.str + json.dumps(shape) + C-order bytes)','logical_arrays':pool.logical,'unique_arrays':len(pool.arrays),'logical_array_bytes':pool.logical_bytes,'unique_array_bytes':sum(a.nbytes for a in pool.arrays.values()),'artifact_bytes':(out/'outcomes.npz').stat().st_size,'artifact_sha256':filehash(out/'outcomes.npz')})
 writejsonl(out/'LEDGER.jsonl',ledger); writejsonl(out/'PAIRED_ROWS.jsonl',paired.values()); savejson(out/'AGGREGATES.json',aggregates); savejson(out/'QUERY_MANIFEST.json',list(querymanifest.values())); savejson(out/'PRODUCT_CHECKS.json',productchecks)
 counts={'paired_rows':len(paired),'method_records':len(ledger),'method_conditions':len(mapping),'structures':len(structural),'calibrations':len(calrows),'query_ids':len(querymanifest),'unique_base_query_arrays':len(set(q['base_array_hash'] for q in querymanifest.values())),'underlying_source_claims':48,'witness_configs':len(witness_rows),'nominal_anchor_readings_per_config':8,'nominal_anchor_readings':len(witness_rows)*8,'unique_anchor_arrays':len({ah(witnesses[k]) for k in witnesses if k.endswith('_anchors')}),'unique_reading_arrays':len({ah(witnesses[k]) for k in witnesses if k.endswith('_readings')})}
 for k,v in {'paired_rows':12288,'method_records':61440,'method_conditions':1920,'structures':96,'calibrations':960,'query_ids':384,'unique_base_query_arrays':288}.items(): assert counts[k]==v,(k,counts[k])
 assert all(q['paired_uses']==32 and q['method_uses']==160 for q in querymanifest.values())
 savejson(out/'SUMMARY.json',{'counts':counts,'repeated_oracle_across_witness_modes':'PASS exact indices, categories, metrics','historical_CR_strict_ordered_replay':'FAIL; historical unchanged','statistical_independence_claim':False,'pool':{'logical_arrays':pool.logical,'unique_arrays':len(pool.arrays),'logical_array_bytes':pool.logical_bytes,'unique_array_bytes':sum(a.nbytes for a in pool.arrays.values()),'artifact_bytes':(out/'outcomes.npz').stat().st_size}})
 savejson(out/'OUTPUT_HASHES.json',{p.name:{'sha256':filehash(p),'bytes':p.stat().st_size} for p in sorted(out.iterdir()) if p.is_file()}); print(json.dumps(counts))
if __name__=='__main__':
 parser=argparse.ArgumentParser(); parser.add_argument('--out',type=Path,default=ROOT/'run'); parser.add_argument('--source-hash-only',action='store_true'); parser.add_argument('--fixtures',action='store_true'); args=parser.parse_args()
 if args.source_hash_only: print(json.dumps(verify_sources(),indent=2))
 elif args.fixtures: fixture_checks()
 else: main(args.out)
