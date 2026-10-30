"""One frozen instrument evaluation; no model inference or input repair."""
from pathlib import Path
import json,hashlib,sys,collections,time
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P.parents[1]/'tools'))
import field_role_guard as guard
import evidence_threshold as checker

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 assert not(P/'RESULTS.json').exists(),'No silent result rerun'
 for name,h in json.loads((P/'FREEZE.json').read_text())['sha256'].items():assert sha(P/name)==h,name
 records={x['id']:x for x in json.loads((P/'RECORDS.json').read_text())};cases=json.loads((P/'CASES.json').read_text());outputs=[];chain=[];start=time.perf_counter()
 for c in cases:
  r=records[c['record_id']];receipt=guard.bind(c['proposal'],P/r['source_path'],c['expected_sha256'],r['entity'],r['unit']);outputs.append({'id':c['id'],'kind':c['kind'],'expected_status':c['expected_status'],'receipt':receipt,'status_matches':receipt['status']==c['expected_status']})
  if c['kind']=='valid' and receipt['status']=='bound':
   d=P/'chain_evidence';d.mkdir(exist_ok=True);artifact=d/(r['id']+'.json');assert not artifact.exists();artifact.write_text(json.dumps({'entity':r['entity'],'scope':r['id'],'unit':r['unit'],'observations':receipt['fields']['observations']},indent=2)+'\n');contract={'claim_id':r['id'],'entity':r['entity'],'scope':r['id'],'criterion':{'id':r['id']+'-min','operator':'at_least','unit':r['unit'],'minimum':receipt['fields']['minimum']},'evidence':{'path':artifact.name,'sha256':sha(artifact)}}
   checked=checker.assess(contract,d);action={'supported':'YES','contradicted':'NO','unresolved':'UNKNOWN'}[checked['verdict']];chain.append({'record_id':r['id'],'contract':contract,'receipt':checked,'action':action,'caller_expected_action':r['conditional_action'],'action_matches':action==r['conditional_action']})
 # Strict interface compatibility of already-preserved outputs, not a new modelarm.
 previous=P.parent/'typed-pipeline-prospective-v1';oldrecords=json.loads((previous/'RECORDS.json').read_text());raw={x['run_id']:x for x in map(json.loads,(previous/'RAW_OUTPUTS.jsonl').read_text().splitlines())};compat=[];d=P/'prior_tp_sources';d.mkdir(exist_ok=False)
 for r in oldrecords:
  path=d/(r['id']+'.txt');path.write_text(r['records']+'\n');proposal={'minimum_text':raw[r['id']+'_minimum']['text'],'measurement_text':raw[r['id']+'_measurements']['text']};receipt=guard.bind(proposal,path,sha(path),r['entity'],r['unit']);action='UNKNOWN' if receipt['status']!='bound' else 'NOT_EVALUATED';compat.append({'record_id':r['id'],'proposal':proposal,'receipt':receipt,'fallback_action':action,'gold_action':r['gold_action'],'label_matches':action==r['gold_action'],'scope':'Oldoutputs were not solicited in this new witnessed schema; rejection is not independent modelperformance or sourcereason recognition.'})
 results={'guard_cases':outputs,'conditional_checker_chain':chain,'previous_output_compatibility':compat,'elapsed_seconds_excluding_tests':time.perf_counter()-start};(P/'RESULTS.json').write_text(json.dumps(results,indent=2)+'\n');(P/'RESULTS_FREEZE.json').write_text(json.dumps({'sha256':{'RESULTS.json':sha(P/'RESULTS.json')}},indent=2)+'\n')
 summary={'instrument_cases':len(outputs),'expected_bound':sum(x['expected_status']=='bound' for x in outputs),'expected_rejected':sum(x['expected_status']!='bound' for x in outputs),'expected_status_matches':sum(x['status_matches'] for x in outputs),'stages':dict(collections.Counter(x['receipt']['stage'] for x in outputs)),'conditional_curated_chain_matches':sum(x['action_matches'] for x in chain),'conditional_curated_chain_total':len(chain),'prior_outputs_tested':len(compat),'prior_output_bound':sum(x['receipt']['status']=='bound' for x in compat),'prior_output_fallback_key_matches':sum(x['label_matches'] for x in compat),'prior_output_source_reason_recognition':0,'new_model_generations':0,'weights_updated':False,'scope':'Authored instrument checks + backward interface compatibility, not general model/harness efficacy.'};(P/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
