from pathlib import Path
import json,hashlib,collections,sys,re
R=Path(__file__).resolve().parent;G=R.parent/'source-access-three-cycle-v1';ENV=G/'cycle3/environment';j=lambda p:json.loads(p.read_text());sha=lambda b:hashlib.sha256(b).hexdigest()
def main(expected):
 sys.path.insert(0,str(G));import routine
 routine.freeze_check();state=j(ENV/'STATE.json');v=j(G/'cycle3/CURRENT_VERIFY.json');checks=j(G/'cycle3'/v['checks']);assert checks['status']=='pass' and state['next_step']==v['next_step']==expected
 base=j(R/'before/primary/cycle3/environment/STATE.json') if expected==80 else j(R/'checkpoints'/f'{expected-5:04d}.json');oldhashes=base['event_sha256'];assert all(state['event_sha256'][k]==h for k,h in oldhashes.items())
 b=(ENV/'NOTEBOOK.jsonl').read_bytes();before=(R/'before/primary/cycle3/environment/NOTEBOOK.jsonl').read_bytes();assert b.startswith(before)
 if expected>80:assert sha(b[:base['notebook_bytes']])==base['notebook_sha256']
 assert (ENV/'PAUSE').exists() and not (ENV/'RUN.lock').exists()
 rows=[j(p) for p in sorted((ENV/'events').glob('*.json')) if expected-5<=int(p.stem)<expected];assert len(rows)==5
 for x in rows:assert x['environment_version']=='archive-view-v1' and x['history_steps']==list(range(x['step']-12,x['step'])) and x['archive_available_range']==[0,x['step']] and x['task_score'] is None
 (R/'checkpoints').mkdir(exist_ok=True)
 result=dict(status='pass',checkpoint_entries=expected,start_step=expected-5,calls=5,verification=v['verification'],prior_event_hashes_preserved=True,whole_initial75_entry_bytes_preserved=True,prior_checkpoint_byte_prefix_preserved=True,event_sha256=state['event_sha256'],notebook_bytes=len(b),notebook_sha256=sha(b),host_kinds=dict(collections.Counter(x['host_result']['kind'] for x in rows)),output_tokens=sum(len(x['generated_token_ids']) for x in rows),cap_stops=sum(x['stop']=='token_limit' for x in rows),max_input_tokens=max(len(x['input_token_ids']) for x in rows),generation_seconds=sum(x['seconds'] for x in rows),seed_ids=sorted({s for x in rows for s in ('P1','W1','C1') if re.search(r'\b'+s+r'\b',x['text'])}),paused=True)
 p=R/'checkpoints'/f'{expected:04d}.json'
 with p.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
 index=[dict(run_id=x['run_id'],step=x['step'],visible_steps=x['history_steps'],archive_available_range=x['archive_available_range'],host_kind=x['host_result']['kind'],input_tokens=len(x['input_token_ids']),output_tokens=len(x['generated_token_ids']),stop=x['stop']) for x in rows]
 (R/'checkpoints'/f'{expected:04d}_INDEX.json').write_text(json.dumps(index,indent=2)+'\n')
 sample=[dict(run_id=x['run_id'],text=x['text'][:650],text_excerpted=len(x['text'])>650,host_kind=x['host_result']['kind'],host_result_value=x['host_result'].get('result'),archive_range=x['host_result'].get('range')) for x in rows]
 (R/'checkpoints'/f'{expected:04d}_REVIEW.json').write_text(json.dumps(sample,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k!='event_sha256'},indent=2));print(json.dumps(sample,indent=2))
if __name__=='__main__':main(int(sys.argv[1]))
