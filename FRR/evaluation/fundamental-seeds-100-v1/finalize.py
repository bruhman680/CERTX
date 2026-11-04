"""External final audit/derived summaries; no model calls or primary writes."""
from pathlib import Path
import json,hashlib,collections,re
R=Path(__file__).resolve().parent;ROOT=R.parent.parent;G=ROOT/'evaluation/source-access-three-cycle-v1';E=G/'cycle3/environment'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 mutable={'evaluation/source-access-three-cycle-v1/cycle3/environment/NOTEBOOK.jsonl','evaluation/source-access-three-cycle-v1/cycle3/environment/STATE.json','evaluation/source-access-three-cycle-v1/cycle3/CURRENT_VERIFY.json'}
 for p,h in json.loads((R/'PRIMARY_BEFORE.json').read_text()).items():
  if p not in mutable:assert sha(ROOT/p)==h,p
 for p,h in json.loads((G/'FREEZE_FUNDAMENTAL.json').read_text())['files'].items():assert sha(Path(p))==h,p
 assert (E/'NOTEBOOK.jsonl').read_bytes().startswith((R/'before/evaluation/source-access-three-cycle-v1/cycle3/environment/NOTEBOOK.jsonl').read_bytes())
 v=json.loads((G/'cycle3/CURRENT_VERIFY.json').read_text());state=json.loads((E/'STATE.json').read_text());assert state['next_step']==v['next_step']==305 and (E/'PAUSE').exists() and not (E/'RUN.lock').exists();assert json.loads((G/'cycle3'/v['checks']).read_text())['status']=='pass';assert state['manifest_sha256']==sha(E/'ENVIRONMENT_FUNDAMENTAL_V1.json')
 rows=[json.loads((E/'events'/f'{i:06d}.json').read_text()) for i in range(205,305)];assert all(x['environment_version']=='fundamental-seed-view-v1' and x['task_score'] is None for x in rows)
 obs=[json.loads(x) for x in (R/'ROOT_OBSERVATIONS.jsonl').read_text().splitlines()];assert [x['end'] for x in obs]==[215,225,245,265,285,305]
 sessions=[json.loads(p.read_text()) for p in (E/'sessions').glob('*.json') if 205<=json.loads(p.read_text())['start_step']<305];assert len(sessions)==20 and sum(x['calls'] for x in sessions)==100 and all(x['weights_unchanged'] and x['training_updates']==0 for x in sessions)
 shelf=json.loads((E/'seed_shelf/0002.json').read_text());material={'F1_sequence':'0,1,2','F2_expressions':'0+1;1+0;1+1','F3_relations':'sameanddifferent;partandwhole','curiosity_clause':'followwhatmakesyoucurious'};index=[]
 for x in rows:
  canonical=re.sub(r'\s+','',x['text'].casefold());lines=[z.strip() for z in x['text'].splitlines() if z.strip() and any(c.isalnum() for c in z)];lc=collections.Counter(lines)
  index.append(dict(step=x['step'],host_kind=x['host_result']['kind'],input_tokens=len(x['input_token_ids']),output_tokens=len(x['generated_token_ids']),stop=x['stop'],literal_material_hits=[k for k,m in material.items() if m in canonical],exact_F_ids=[f for f in ('F1','F2','F3') if re.search(r'\b'+f+r'\b',x['text'])],max_repeated_content_line=max(lc.values(),default=0),punctuation_only=bool(x['text'].strip()) and not any(c.isalnum() for c in x['text'])))
 blocks=[]
 for start in range(205,305,20):
  rs=[x for x in rows if start<=x['step']<start+20];ix=[x for x in index if start<=x['step']<start+20];counts=collections.Counter(x['text'] for x in rs)
  blocks.append(dict(start=start,end=start+20,calls=20,host_kinds=dict(collections.Counter(x['host_result']['kind'] for x in rs)),calculator_expressions=dict(collections.Counter(x['host_result']['expression'] for x in rs if x['host_result']['kind']=='calculation')),caps=sum(x['stop']=='token_limit' for x in rs),output_tokens=sum(len(x['generated_token_ids']) for x in rs),distinct_exact_replies=len(counts),modal_exact_reply_count=max(counts.values()),literal_material_reply_counts={k:sum(k in x['literal_material_hits'] for x in ix) for k in material},replies_with_repeated_content_line_ge3=sum(x['max_repeated_content_line']>=3 for x in ix)))
 summary=dict(start_entries=205,end_entries=305,calls=100,host_kinds=dict(collections.Counter(x['host_result']['kind'] for x in rows)),calculator_expressions=dict(collections.Counter(x['host_result']['expression'] for x in rows if x['host_result']['kind']=='calculation')),caps=sum(x['stop']=='token_limit' for x in rows),output_tokens=sum(len(x['generated_token_ids']) for x in rows),max_input_tokens=max(len(x['input_token_ids']) for x in rows),unique_exact_replies=len({x['text'] for x in rows}),generation_seconds=sum(x['seconds'] for x in rows),verification=v['verification'],checkpoints=list(range(210,306,5)),blocks=blocks,interpretation='Descriptive combined shelf+sentence trajectory; literal hits/variety/repetition are not novelty,understanding or causal effect scores.')
 preview=json.loads((R/'FIRST_VIEW_205.json').read_text());assert rows[0]['prompt']==preview['prompt'] and rows[0]['input_token_ids']==preview['input_token_ids']
 checks=dict(status='pass',primary_at_paused305=True,old205_notebook_exact_byte_prefix=True,all_prior_immutable_files_exact=True,legacy_and_new_policy_replay=v,transition_replay=json.loads((R/'TRANSITION_CHECKS.json').read_text()),twenty_sessions_hundred_calls_fixed_weights=True,policy_freeze_unchanged=True)
 for name,data in [('SUMMARY',summary),('EVENT_INDEX',index),('TWENTY_ENTRY_SUMMARIES',blocks),('CHECKS',checks)]:
  with (R/(name+'.json')).open('x') as f:json.dump(data,f,indent=2);f.write('\n')
 print(json.dumps({k:v for k,v in summary.items() if k!='blocks'},indent=2));print(json.dumps(blocks,indent=2))
if __name__=='__main__':main()
