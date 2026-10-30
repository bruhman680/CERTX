"""Retrospective saved-response composition; no new generation or gold input repair."""
from pathlib import Path
import json,hashlib,re,sys,time
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P.parents[1]/'tools'))
import evidence_threshold as instrument

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def parse(text,unit,allow_missing):
 if allow_missing and text.strip().rstrip('.').upper()=='MISSING':return {'state':'missing'}
 # Narrow surface parser, not NL entailment: one nonnegative integer with expected literalunit.
 matches=list(re.finditer(r'(?<![\w.])([0-9]+)\s+(cm|kg)\b',text))
 # Reject another numeric expression rather than silently choosing among numbers.
 nums=re.findall(r'(?<![\w.])[0-9]+(?![\w.])',text)
 if len(matches)!=1 or len(nums)!=1 or matches[0].group(2)!=unit:return None
 return {'state':'measured','value':matches[0].group(1)}

def run():
 assert not (P/'REPLAY_RESULTS.json').exists(),'No silent replay rerun'
 for n,h in json.loads((P/'REPLAY_FREEZE.json').read_text())['sha256'].items():assert sha(P/n)==h,n
 raw={x['run_id']:x for x in map(json.loads,(P/'RAW_OUTPUTS.jsonl').read_text().splitlines())}
 # Gold/scoring are evaluation-only; do not use either to choose the instrument action.
 scores={x['run_id']:x for x in json.loads((P/'ROOT_SCORES.json').read_text())}
 records=json.loads((P/'RECORDS.json').read_text());root=P/'replay_inputs';root.mkdir(exist_ok=False)
 results=[]
 for r in records:
  m=raw[r['id']+'_measurement'];c=raw[r['id']+'_minimum'];measurement=parse(m['text'],r['unit'],True);minimum=parse(c['text'],r['unit'],False)
  entry={'record_id':r['id'],'measurement_text':m['text'],'minimum_text':c['text'],'parsed_measurement':measurement,'parsed_minimum':minimum,'source_run_ids':[m['run_id'],c['run_id']],'input_tokens':m['input_tokens']+c['input_tokens'],'output_tokens':m['output_tokens']+c['output_tokens'],'inference_seconds':m['inference_seconds_excluding_serialization']+c['inference_seconds_excluding_serialization']}
  if measurement is None or minimum is None:
   entry.update(action='UNKNOWN',stage='extraction_unusable',receipt=None)
  else:
   artifact={'entity':r['entity'],'scope':'saved-generated-claims-'+r['id'],'unit':r['unit'],'observations':[measurement]}
   artifact_path=root/(r['id']+'.json');artifact_path.write_text(json.dumps(artifact,indent=2)+'\n')
   contract={'claim_id':r['id']+'-generated-pair-at-least','entity':r['entity'],'scope':artifact['scope'],'criterion':{'id':c['run_id'],'operator':'at_least','unit':r['unit'],'minimum':minimum['value']},'evidence':{'path':artifact_path.name,'sha256':sha(artifact_path)}}
   receipt=instrument.assess(contract,root)
   entry.update(contract=contract,receipt=receipt,stage=receipt['stage'],action={'supported':'YES','contradicted':'NO','unresolved':'UNKNOWN'}[receipt['verdict']])
  # Only now evaluate against originalrecord gold and the deposited extractionwarrants.
  gold='UNKNOWN' if r['value'] is None else 'YES' if r['value']>=r['minimum'] else 'NO'
  entry.update(gold=gold,semantic_match=entry['action']==gold,extracted_fields_warranted=scores[m['run_id']]['fully_warranted'] and scores[c['run_id']]['fully_warranted'],direct_action=scores[r['id']+'_pass']['semantic_answer'],direct_warrant=scores[r['id']+'_pass']['fully_warranted'])
  entry['fully_warranted']=entry['semantic_match'] and entry['extracted_fields_warranted'];results.append(entry)
 summary={'scope':'Post-primary saved-response composition, not an independent model arm. Model-generated criterion and measurement; caller context supplies entity/unit, not gold numeric values. Surface parser is not NL entailment/source authentication; primary extractionwarrants evaluated separately. Two extraction calls vsone direct call, not equalbudget. No prompttraining/newmodelcalls/goldrepair.','checker_sha256':instrument.CHECKER_SHA256,'records':results,'semantic_matches':sum(x['semantic_match'] for x in results),'fully_warranted':sum(x['fully_warranted'] for x in results),'direct_semantic_matches':sum(x['direct_action']==x['gold'] for x in results),'direct_warranted':sum(x['direct_warrant'] for x in results),'input_tokens':sum(x['input_tokens'] for x in results),'output_tokens':sum(x['output_tokens'] for x in results),'inference_seconds_already_counted_in_primary':sum(x['inference_seconds'] for x in results)}
 (P/'REPLAY_RESULTS.json').write_text(json.dumps(summary,indent=2)+'\n')
 (P/'REPLAY_RAW_FREEZE.json').write_text(json.dumps({'sha256':{'REPLAY_RESULTS.json':sha(P/'REPLAY_RESULTS.json')}},indent=2)+'\n')
if __name__=='__main__':run()
