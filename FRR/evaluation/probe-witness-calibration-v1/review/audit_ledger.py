#!/usr/bin/env python3
"""Independent exhaustive metric/witness audit; no experiment imports.
Prospective schema/source inspection disclosed in PROSPECTIVE_REVIEW.md.
"""
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent.parent
RUN=ROOT/'run'
TOL=1e-10
PROBES={'CONTEXT':(-1.,1.),'WEAK':(.9,1.),'SIGNAL':(1.,-1.),'COPY':(1.,1.)}
MODES={'EXACT':([0.]*4,[0.]*4,0.,0.),'BOUNDED':([.04,.03,.02,.01],[-.01,-.02,-.03,-.04],.05,.05),'BETA_GAIN_ERROR':([0.]*4,[.1]*4,0.,.12),'INVALID_SHARED_BIAS':([.12]*4,[-.12]*4,.02,.02)}
METHODS={'BINDING_ORACLE','COEFF_ORACLE','ADVERTISED','POINT','GATED'}
LABELS=np.array(['A','N','U'])
def read(name): return json.loads((RUN/name).read_text())
def lines(path): return [json.loads(x) for x in path.read_text().splitlines()]
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def ah(a):
 a=np.ascontiguousarray(a)
 return hashlib.sha256(a.dtype.str.encode()+json.dumps(a.shape).encode()+a.tobytes()).hexdigest()
def near(a,b):
 assert np.allclose(a,b,atol=2e-12,rtol=2e-12),(a,b)
def witness(ya,yb,ea,eb):
 a=(max(ya-ea),min(ya+ea)); b=(max(yb-eb),min(yb+eb)); nonempty=a[0]<=a[1] and b[0]<=b[1]
 gap=(b[0]-a[1],b[1]-a[0]); margin=min(abs(x) for x in gap) if nonempty and (gap[0]>0 or gap[1]<0) else 0.
 gate=nonempty and margin>TOL
 return a,b,gap,margin,gate,'ok' if gate else ('empty_witness_set' if not nonempty else 'witness_set_not_separated')
def expected_metrics(top,labels,reasons,claim):
 hits=top//3==claim; right=hits&(labels[top]==LABELS[top%3]); rel=labels[3*claim:3*claim+3]
 count=int(sum(hits)); joint=int(sum(right)); abstain=labels[top]=='ABSTAIN'
 return {'evidence_count':count,'evidence_recall':count/3,'evidence_complete':count==3,
 'joint_label_count':joint,'joint_label_recall':joint/3,'joint_label_complete':joint==3,
 'wrongscope':3-count,'encoded_U_recall':int(any((top==3*claim+2)&(labels[top]=='U'))),
 'abstain_count':int(sum(abstain)),'abstain_reasons':dict(Counter(reasons[top][abstain].tolist())),
 'oracle_relevant_stance_count':int(sum(rel==LABELS)), 'oracle_relevant_stance_accuracy':float(np.mean(rel==LABELS))}
def main():
 rows=lines(RUN/'LEDGER.jsonl'); pairs=lines(RUN/'PAIRED_ROWS.jsonl'); aggs=read('AGGREGATES.json'); mapping=read('OUTCOME_MAP.json')['conditions']
 src=np.load(RUN/'source_inputs.npz',allow_pickle=False); obs=np.load(RUN/'witness_inputs.npz',allow_pickle=False); pool=np.load(RUN/'outcomes.npz',allow_pickle=False)
 ws=lines(RUN/'WITNESS_DIAGNOSTICS.jsonl'); structs=lines(RUN/'STRUCTURAL_DIAGNOSTICS.jsonl')
 assert len(rows)==61440 and len(pairs)==12288 and len(aggs)==len(mapping)==1920 and len(ws)==48 and len(structs)==96
 wlookup={}; witness_flags=Counter()
 for w in ws:
  k=w['key']; alpha,beta=PROBES[w['probe']]; ae,be,ea,eb=MODES[w['witness_mode']]; y=obs[k+'_readings']; near(y,np.r_[alpha+np.array(ae),beta+np.array(be)]); near(obs[k+'_eps'],[ea,eb]); near(obs[k+'_errors'],ae+be)
  a,b,gap,margin,gate,reason=witness(y[:4],y[4:],ea,eb)
  for role,interval,yy in [('alpha',a,y[:4]),('beta',b,y[4:])]:
   d=w[role+'_interval']; near([d['lower'],d['upper']],interval); assert d['nonempty']==(interval[0]<=interval[1]); near(d['mean'],np.mean(yy)); assert d['mean_in_interval']==(interval[0]<=np.mean(yy)<=interval[1])
  near([w['a_hat'],w['b_hat']],[np.mean(y[:4]),np.mean(y[4:])]); near(w['point_gap'],np.mean(y[4:])-np.mean(y[:4])); near(w['compatible_gap_range'],gap); near(w['min_absolute_gap'],margin)
  assert w['gate_passed']==gate and w['gate_reason']==reason
  covered=a[0]<=alpha<=a[1] and b[0]<=beta<=b[1]; assert covered==w['true_pair_covered']
  radii=np.r_[np.full(4,ea),np.full(4,eb)]; truth=np.r_[np.full(4,alpha),np.full(4,beta)]
  assert w['individual_bound_coverage']==((y-radii<=truth)&(truth<=y+radii)).tolist()
  assert w['false_identification_under_actual_model']==(gate and abs(beta-alpha)<=TOL)
  assert w['oracle_relative_withholding']==(not gate and abs(beta-alpha)>TOL)
  near([w['true_alpha'],w['true_beta'],w['true_gap']],[alpha,beta,beta-alpha])
  if abs(w['point_gap'])>TOL: near(w['inversion_amplification'],1/abs(w['point_gap']))
  else: assert w['inversion_amplification'] is None
  witness_flags[(w['witness_mode'],gate,covered)]+=1; wlookup[w['seed'],w['probe'],w['witness_mode']]=w
 structure={}
 for s in structs:
  w=wlookup[s['seed'],s['probe'],s['witness_mode']]; alpha,beta=PROBES[s['probe']]
  assert set(s['methods'])==METHODS
  for method,d in s['methods'].items():
   reason='ok'
   if method=='GATED' and not w['gate_passed']: reason=w['gate_reason']
   elif method=='COEFF_ORACLE' and abs(beta-alpha)<=TOL: reason='true_operator_singular'
   elif method in ('POINT','GATED') and abs(w['point_gap'])<=TOL: reason='estimated_operator_singular'
   available=reason=='ok'; assert d['available']==available and d['availability_reason']==reason
   assert d['placeholder_rank']==(None if available else 0)
   assert d['retained_rank']==min(12,d['numeric_rank'])
   assert d['available_rank_zero']==(available and d['retained_rank']==0)
   if not available:
    assert d['retained_rank']==0
    assert all(d[k] is None for k in ('raw_signal_key','raw_relative_frobenius_error','raw_reconstructed_norm','raw_nuisance_coefficient','raw_signal_gain','coefficient_identity_error','projector_binding_distance'))
   if method in ('POINT','GATED'): near([d['a_used'],d['b_used']],[w['a_hat'],w['b_hat']])
   elif method=='ADVERTISED': near([d['a_used'],d['b_used']],[-1,1])
   elif method=='COEFF_ORACLE': near([d['a_used'],d['b_used']],[alpha,beta])
   else: assert d['a_used'] is None and d['b_used'] is None
   structure[s['key']+'_'+method]=d
 bycondition=defaultdict(list); byquery=defaultdict(list); repeated={}; repeat_checks=0; unavailable=Counter(); returned_reasons=Counter(); prior_control_differences=[]
 prior={}
 for p in lines(ROOT.parent/'context-perturbation-repair-v1/run/LEDGER.jsonl'):
  if p['method']=='oracle': prior[(p['seed'],p['r'],p['eval_eta'],p['query_index'])]=p
 for i,row in enumerate(rows):
  assert row['index']==i and row['condition']==row['outcome_key']; fields={k:pool[v] for k,v in mapping[row['condition']].items()}; j=row['query_index']; assert 0<=j<32
  seed=row['seed']; claim=int(src[f's{seed}_query_claim_index'][j]); assert row['claim_index']==claim and row['query_repetition']==int(src[f's{seed}_query_repetition'][j])
  ri=(0 if row['r']==.5 else 1); ei=(0 if row['eval_noise']==0 else 1); assert row['query_id']==f's{seed}_r{ri}_e{ei}_q{j}'
  top=np.asarray(row['returned_indices']); assert len(top)==3 and len(set(top))==3 and np.all((0<=top)&(top<48)); assert np.array_equal(top,fields['top'][j]); order=np.argsort(-fields['scores'][j],kind='stable'); assert np.array_equal(top,order[:3])
  labels=fields['labels'][j]; reasons=fields['reasons'][j]; assert row['predictions']==labels[top].tolist() and row['reasons']==reasons[top].tolist()
  assert row['returned_record_ids']==[f's{seed}_claim{x//3}_{LABELS[x%3]}' for x in top]
  assert row['returned_products']==[[float(z.real),float(z.imag)] for z in fields['products'][j,top]]
  assert row['returned_scores']==fields['scores'][j,top].tolist()
  assert row['oracle_relevant_predictions']==labels[3*claim:3*claim+3].tolist() and row['oracle_relevant_reasons']==reasons[3*claim:3*claim+3].tolist()
  gap=float(fields['scores'][j,order[2]]-fields['scores'][j,order[3]]); assert row['third_fourth_gap']==gap and row['exact_boundary_tie']==(gap==0.) and row['near_boundary']==(gap<=TOL)
  assert row['within_top3_gaps']==np.diff(-fields['scores'][j,top]).tolist()
  expected=expected_metrics(top,labels,reasons,claim); assert row['metrics']==expected,(i,row['metrics'],expected)
  assert sum(expected['abstain_reasons'].values())==expected['abstain_count']; returned_reasons.update(expected['abstain_reasons'])
  w=wlookup[seed,row['probe'],row['witness_mode']]
  for k in ('gate_passed','true_pair_covered','false_identification_under_actual_model','oracle_relative_withholding'): assert row[k]==w[k]
  mk=row['condition'].rsplit('_r',1)[0]; d=structure[mk]
  for k in ('available','availability_reason','placeholder_rank','numeric_rank','retained_rank'): assert row[k]==d[k]
  unavailable[(row['method'],row['availability_reason'])]+=1; bycondition[row['condition']].append(row); byquery[row['query_id']].append(i)
  payload={k:row[k] for k in ('returned_indices','predictions','reasons','oracle_relevant_predictions','oracle_relevant_reasons','metrics')}
  if row['method'] in ('BINDING_ORACLE','COEFF_ORACLE'):
   key=(seed,row['delta'],row['probe'],ri,ei,j,row['method'])
   if key in repeated: assert payload==repeated[key]; repeat_checks+=1
   else: repeated[key]=payload
  if row['method']=='BINDING_ORACLE':
   p=prior[seed,row['r'],row['eval_noise'],j]
   flags={k:row[k]!=p[k] for k in ('returned_indices','predictions','reasons','oracle_relevant_predictions','oracle_relevant_reasons')}
   if any(flags.values()): prior_control_differences.append({'row':i,'differences':flags,'same_membership':set(row['returned_indices'])==set(p['returned_indices'])})
 assert len(byquery)==384 and set(map(len,byquery.values()))=={160}
 max_aggregate_error=0.
 for ag in aggs:
  rr=bycondition[ag['condition']]; assert len(rr)==ag['count']==32 and {r['query_index'] for r in rr}==set(range(32)); numeric=set(rr[0]['metrics'])-{'abstain_reasons'}; assert set(ag['sums'])==set(ag['means'])==numeric
  for k in numeric:
   val=sum(r['metrics'][k] for r in rr); err=abs(val-ag['sums'][k]); meanerr=abs(val/32-ag['means'][k]); max_aggregate_error=max(max_aggregate_error,err,meanerr)
   if all(isinstance(r['metrics'][k],(bool,int)) for r in rr): assert err==meanerr==0.
   else: assert err<=1e-11 and meanerr<=1e-11
  for reason in ('calibration_unavailable','ambiguous_centre','zero_product'): assert ag['abstain_reasons'][reason]==sum(r['metrics']['abstain_reasons'].get(reason,0) for r in rr)
 seen=set()
 for p in pairs:
  indices=p['method_indices']; assert set(indices)==METHODS; rr=[rows[i] for i in indices.values()]; assert all(r['query_id']==p['query_id'] for r in rr)
  for k in ('seed','delta','probe','witness_mode','r','eval_noise','query_index'): assert len({r[k] for r in rr})==1
  assert all(rows[i]['method']==m for m,i in indices.items()); assert seen.isdisjoint(indices.values()); seen.update(indices.values())
 assert seen==set(range(61440))
 manifest=read('QUERY_MANIFEST.json'); hashes=[]
 for q in manifest:
  qid=q['query_id']; assert qid in byquery; arr=src[f"s{q['seed']}_queries_r{q['r_index']}_e{q['noise_index']}"][rows[byquery[qid][0]]['query_index']]
  h=ah(arr); hashes.append(h); assert h==q['base_array_hash'] and q['paired_uses']==32 and q['method_uses']==160
 assert len(manifest)==384 and len(set(hashes))==288
 result={'passed':True,'method_records':61440,'paired_rows':12288,'aggregates':1920,'witness_configs':48,'structures':96,'query_ids':384,'unique_base_arrays':288,'per_query_method_uses':160,'repeated_oracle_checks':repeat_checks,'max_aggregate_arithmetic_error':max_aggregate_error,'returned_abstain_reasons':dict(returned_reasons),'availability_reason_counts':{str(k):v for k,v in unavailable.items()},'witness_gate_coverage_counts':{str(k):v for k,v in witness_flags.items()},'historical_binding_control_rows':12288,'historical_binding_control_difference_rows':len(prior_control_differences),'historical_binding_control_membership_changes':sum(not d['same_membership'] for d in prior_control_differences),'source_inspection':'Current protocol/schema/experiment and predecessor experiment/independent auditor inspected; no implementation imports','audit_sha256':digest(Path(__file__)),'ledger_sha256':digest(RUN/'LEDGER.jsonl')}
 (ROOT/'review/LEDGER_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n'); (ROOT/'review/HISTORICAL_BINDING_CONTROL_DIFFERENCES.json').write_text(json.dumps(prior_control_differences,indent=2)+'\n'); print(json.dumps(result))
if __name__=='__main__': main()
