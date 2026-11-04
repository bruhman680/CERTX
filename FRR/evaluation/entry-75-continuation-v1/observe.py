"""External descriptive attention packet; never changes the garden's inputs."""
from pathlib import Path
import json,re,hashlib,collections
R=Path(__file__).resolve().parent;G=R.parent/'source-access-three-cycle-v1';ENV=G/'cycle3/environment'
def main():
 allrows=[json.loads(p.read_text()) for p in sorted((ENV/'events').glob('*.json'))];old=[x for x in allrows if x['step']<65];new=[x for x in allrows if x['step']>=65]
 kinds={x['host_result']['kind'] for x in old};expr={x['host_result'].get('expression') for x in old if x['host_result']['kind'].startswith('calculation')};out=[]
 for x in new:
  h=x['host_result'];ids=[s for s in ('P1','W1','C1') if re.search(r'\b'+s+r'\b',x['text'])];flags=[]
  if h['executed'] and h['kind'] not in kinds:flags.append('new_actual_action_kind')
  if h['kind'].startswith('calculation') and h.get('expression') not in expr:flags.append('different_calculator_expression')
  if ids:flags.append('literal_seed_reference')
  if len(x['generated_token_ids'])>=32:flags.append('long_reply')
  if x['stop']=='token_limit':flags.append('output_cap')
  out.append(dict(run_id=x['run_id'],step=x['step'],host_kind=h['kind'],host_executed=h['executed'],seed_ids=ids,input_tokens=len(x['input_token_ids']),output_tokens=len(x['generated_token_ids']),stop=x['stop'],flags=flags))
 rank={'new_actual_action_kind':0,'different_calculator_expression':1,'literal_seed_reference':2,'long_reply':3,'output_cap':4};flagged=sorted([x for x in out if x['flags']],key=lambda x:(min(rank[f] for f in x['flags']),x['step']));quiet=[x for x in out if not x['flags']];sample=min(quiet,key=lambda x:hashlib.sha256(('e75quiet:'+x['run_id']).encode()).hexdigest()) if quiet else None
 selected=flagged[:5 if sample else 6]+([sample] if sample else []);ids={x['run_id'] for x in selected}
 index=dict(policy='External posthoc heuristic attention, broad priority categories declared before run; exact thresholds are descriptive, not calibrated phase/semantic success criteria',rows=out,selected_ids=[x['run_id'] for x in selected],flagged_total=len(flagged),flagged_not_selected=len([x for x in flagged if x['run_id'] not in ids]),quiet_sample_id=sample['run_id'] if sample else None)
 (R/'EVENT_INDEX.json').write_text(json.dumps(index,indent=2)+'\n');(R/'REVIEW_SAMPLE.json').write_text(json.dumps([dict(run_id=x['run_id'],text=x['text'],host_result=x['host_result'],stop=x['stop']) for x in new if x['run_id'] in ids],indent=2)+'\n')
 summary=dict(calls=len(new),next_step=len((ENV/'NOTEBOOK.jsonl').read_text().splitlines()),host_kinds=dict(collections.Counter(x['host_result']['kind'] for x in new)),seed_reference_replies=sum(bool(x['seed_ids']) for x in out),output_tokens=sum(len(x['generated_token_ids']) for x in new),cap_stops=sum(x['stop']=='token_limit' for x in new),max_input_tokens=max((len(x['input_token_ids']) for x in new),default=0),crossed_old_6144=sum(len(x['input_token_ids'])>6144 for x in new),generation_seconds=sum(x['seconds'] for x in new),selected_examples=len(selected),flagged_overflow=index['flagged_not_selected'])
 (R/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2));print(json.dumps(index['selected_ids']))
if __name__=='__main__':main()
