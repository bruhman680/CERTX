"""External read-only primary audit and derived descriptive metrics after205; no inference."""
from pathlib import Path
import json,hashlib,collections,re
R=Path(__file__).resolve().parent;ROOT=R.parent.parent;G=ROOT/'evaluation/source-access-three-cycle-v1';E=G/'cycle3/environment'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 mutable={'evaluation/source-access-three-cycle-v1/cycle3/environment/NOTEBOOK.jsonl','evaluation/source-access-three-cycle-v1/cycle3/environment/STATE.json','evaluation/source-access-three-cycle-v1/cycle3/CURRENT_VERIFY.json'}
 for p,h in json.loads((R/'PRIMARY_BEFORE.json').read_text()).items():
  if p not in mutable:assert sha(ROOT/p)==h,p
 for p,h in json.loads((R/'FREEZE.json').read_text())['files'].items():assert sha(ROOT/p)==h,p
 assert (E/'NOTEBOOK.jsonl').read_bytes().startswith((R/'before/evaluation/source-access-three-cycle-v1/cycle3/environment/NOTEBOOK.jsonl').read_bytes())
 v=json.loads((G/'cycle3/CURRENT_VERIFY.json').read_text());assert json.loads((E/'STATE.json').read_text())['next_step']==v['next_step']==205 and (E/'PAUSE').exists() and not (E/'RUN.lock').exists();assert json.loads((G/'cycle3'/v['checks']).read_text())['status']=='pass'
 rows=[json.loads((E/'events'/f'{i:06d}.json').read_text()) for i in range(155,205)];blocks=[json.loads((R/f'{n}_SUMMARY.json').read_text()) for n in (165,175,185,195,205)];obs=[json.loads(x) for x in (R/'ROOT_OBSERVATIONS.jsonl').read_text().splitlines()];assert [x['end'] for x in obs]==[165,175,185,195,205]
 sessions=[json.loads(p.read_text()) for p in (E/'sessions').glob('*.json') if 155<=json.loads(p.read_text())['start_step']<205];assert len(sessions)==10 and sum(x['calls'] for x in sessions)==50 and all(x['weights_unchanged'] and x['training_updates']==0 for x in sessions)
 es=[json.loads(x) for x in (E/'NOTEBOOK.jsonl').read_text().splitlines()];old_calcs=[dict(step=e['step'],host_result=e['host_result']) for e in es[:155] if e.get('host_result',{}).get('kind')=='calculation'];calcs=[dict(step=x['step'],text=x['text'],host_result=x['host_result'],history_steps=x['history_steps']) for x in rows if x['host_result']['kind']=='calculation'];candidates=[];metrics=[]
 for x in rows:
  lines=[l.strip() for l in x['text'].splitlines() if l.strip() and any(c.isalnum() for c in l)];lc=collections.Counter(lines);q=x['prompt'];i=x['step'];h=x['host_result'];metrics.append(dict(step=i,host_kind=h['kind'],input_tokens=len(x['input_token_ids']),output_tokens=len(x['generated_token_ids']),stop=x['stop'],max_repeated_content_line=max(lc.values(),default=0),punctuation_only_reply=bool(x['text'].strip()) and not any(c.isalnum() for c in x['text']),exact_your_f_lines=lc['YOUR F']))
  if lines and re.fullmatch(r'\d+',lines[0]):
   n=int(lines[0]);pos=q.rfind('ARCHIVE ACCESS');candidates.append(dict(step=i,first_content_line=lines[0],whole_reply_integer=bool(re.fullmatch(r'\s*\d+\s*',x['text'])),matches_visible_start=n==min(x['history_steps']),matches_archive_lower_bound=n==0,visible_start=min(x['history_steps']),actual_metadata=q[pos:pos+500],text=x['text']))
 summary=dict(start_entries=155,end_entries=205,calls=50,host_kinds=dict(collections.Counter(x['host_result']['kind'] for x in rows)),calculator_expressions=dict(collections.Counter(x['host_result']['expression'] for x in rows if x['host_result']['kind']=='calculation')),output_tokens=sum(len(x['generated_token_ids']) for x in rows),caps=sum(x['stop']=='token_limit' for x in rows),max_input_tokens=max(len(x['input_token_ids']) for x in rows),generation_seconds=sum(x['seconds'] for x in rows),unique_exact_replies=len({x['text'] for x in rows}),verification=v['verification'],checkpoints=[i for b in blocks for i in b['checkpoints']],blocks=blocks)
 for name,data in [('SUMMARY',summary),('EVENT_INDEX',metrics),('ACTION_TRACE',dict(historical_before155=old_calcs,current=calcs,scope='Actual dispatched operations; no goal or learning score')),('INDEX_CANDIDATES',dict(scope='Posthoc first-content-line integers, punctuation wrappers ignored, all matches/nonmatches retained; no task requested, so these are not correctness scores or proof of grounding',rows=candidates)),('CHECKS',dict(status='pass',all_prior_immutable_primary_files_exact=True,old155_notebook_exact_prefix=True,policy_freeze_unchanged=True,ten_sessions_fifty_calls_fixed_weights=True,primary_verification=v,paused_at205=True))]:
  with (R/(name+'.json')).open('x') as f:json.dump(data,f,indent=2);f.write('\n')
 print(json.dumps({k:v for k,v in summary.items() if k!='blocks'},indent=2));print(json.dumps(dict(integer_candidates=len(candidates),visible_start_matches=sum(x['matches_visible_start'] for x in candidates)),indent=2))
if __name__=='__main__':main()
