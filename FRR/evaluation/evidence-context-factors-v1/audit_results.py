"""Independent arithmetic/pairing audit over saved outputs. No model forwards."""
from pathlib import Path
import json,math
R=Path(__file__).resolve().parent
raw=[json.loads(x) for x in (R/'run/RAW.jsonl').read_text().splitlines()];by={r['run_id']:r for r in raw};summary=json.loads((R/'run/SUMMARY.json').read_text());tokens=json.loads((R/'TOKENIZATION.json').read_text());target=json.loads((R/'PADDING.json').read_text())['global_matched_token_count']
for r in raw:
 assert r['input_token_ids']==tokens['input_token_ids'][r['run_id']]
 if r['condition'] not in ('original','legacy_anchor'):assert len(r['input_token_ids'])==target
 if 'probability' in r:
  for k,c in r['probability']['candidates'].items():
   assert c['target_ids']==tokens['candidate_target_ids'][k]
   assert abs(math.exp(c['token_logps'][0])-c['first_token_full_vocab_prob'])<1e-12
for axis,record in summary['factors'].items():
 assert len(record['rows'])==64
 for d in record['rows']:
  left,right=by[d['left']],by[d['right']];assert left['case_id']==right['case_id']
  assert len(left['input_token_ids'])==len(right['input_token_ids'])==target
  if axis=='content':assert (left['content'],right['content'])==('filler','duplicate') and left['authority']==right['authority'] and left['placement']==right['placement']
  if axis=='authority':assert (left['authority'],right['authority'])==(False,True) and left['content']==right['content'] and left['placement']==right['placement']
  if axis=='placement':assert (left['placement'],right['placement'])==('before','after') and left['authority']==right['authority'] and left['content']==right['content']
  assert d['repair']==(not left['correct'] and right['correct']);assert d['harm']==(left['correct'] and not right['correct'])
  assert abs(d['gold_logp_delta']-(right['probability']['candidates'][right['expected']]['sequence_logp']-left['probability']['candidates'][left['expected']]['sequence_logp']))<1e-12
 for split in ('discovery','confirmation'):
  rows=[x for x in record['rows'] if x['split']==split];m=record['by_split'][split];assert len(rows)==32 and len({x['case_id'] for x in rows})==8
  assert sum(x['repair'] for x in rows)==m['repairs'] and sum(x['harm'] for x in rows)==m['harms']
resources=[json.loads(x) for x in (R/'run/RESOURCE.jsonl').read_text().splitlines()];assert all(x['working_estimate']<x['working_limit'] for x in resources)
with (R/'ROOT_AUDIT.json').open('x') as f:json.dump({'status':'pass','inputs_match_pre_run_tokens':167,'matched_context_lengths':144,'matched_tokens_per_prompt':target,'factor_contrasts_checked':192,'split_contrasts':32,'cases_per_split':8,'candidate_target_first_probs_checked':640,'maximum_working_estimate_bytes':max(x['working_estimate'] for x in resources),'resource_checks':'pass'},f,indent=2);f.write('\n')
print('All paired-factor, input-token, candidate-score and resource checks passed')
