"""Execute a prospectively frozen pipeline; no task-gold scoring or input repair."""
from pathlib import Path
import json,hashlib
from pipeline import compute_pair
P=Path(__file__).resolve().parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
 assert not(P/'PIPELINE_ACTIONS.json').exists(),'No silent action rerun'
 for n,h in json.loads((P/'FREEZE.json').read_text())['sha256'].items():assert sha(P/n)==h,n
 rows={x['run_id']:x for x in map(json.loads,(P/'RAW_OUTPUTS.jsonl').read_text().splitlines())}
 records=json.loads((P/'RECORDS.json').read_text());results=[]
 for r in records:
  m=rows[r['id']+'_measurements'];c=rows[r['id']+'_minimum']
  # Do NOT use actual minimum, observations, gold_action or gold_reason to compute.
  action=compute_pair(m['text'],c['text'],r['entity'],r['unit'],r['id'],P/'pipeline_evidence')
  action.update(source_run_ids=[m['run_id'],c['run_id']],input_tokens=m['input_tokens']+c['input_tokens'],output_tokens=m['output_tokens']+c['output_tokens'],inference_seconds=m['inference_seconds_excluding_serialization']+c['inference_seconds_excluding_serialization'])
  results.append(action)
 (P/'PIPELINE_ACTIONS.json').write_text(json.dumps(results,indent=2)+'\n')
 (P/'ACTIONS_FREEZE.json').write_text(json.dumps({'phase':'before scoring source agreement/task outcome','sha256':{'PIPELINE_ACTIONS.json':sha(P/'PIPELINE_ACTIONS.json')}},indent=2)+'\n')
if __name__=='__main__':main()
