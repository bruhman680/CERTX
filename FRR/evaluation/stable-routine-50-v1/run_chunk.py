"""External pacing/observation only. Does not edit model-facing policy."""
from pathlib import Path
import sys,json,hashlib,subprocess,collections
R=Path(__file__).resolve().parent;ROOT=R.parent.parent;G=ROOT/'evaluation/source-access-three-cycle-v1';E=G/'cycle3/environment';PY='/workspace/cache_backend_venv/bin/python'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check_old():
 mutable={'evaluation/source-access-three-cycle-v1/cycle3/environment/NOTEBOOK.jsonl','evaluation/source-access-three-cycle-v1/cycle3/environment/STATE.json','evaluation/source-access-three-cycle-v1/cycle3/CURRENT_VERIFY.json'}
 for p,h in json.loads((R/'PRIMARY_BEFORE.json').read_text()).items():
  if p not in mutable:assert sha(ROOT/p)==h,p
 for p,h in json.loads((R/'FREEZE.json').read_text())['files'].items():assert sha(ROOT/p)==h,p
 assert (E/'NOTEBOOK.jsonl').read_bytes().startswith((R/'before/evaluation/source-access-three-cycle-v1/cycle3/environment/NOTEBOOK.jsonl').read_bytes())
def action(args,stem):
 with (R/(stem+'.stdout')).open('x') as out,(R/(stem+'.stderr')).open('x') as err:subprocess.run([PY,'routine.py']+args,cwd=G,stdout=out,stderr=err,check=True)
def run(end):
 start=end-10;assert end in (115,125,135,145,155);check_old();assert json.loads((E/'STATE.json').read_text())['next_step']==start and (E/'PAUSE').exists()
 for cursor in (start,start+5):
  v=json.loads((G/'cycle3/CURRENT_VERIFY.json').read_text());assert v['next_step']==cursor and json.loads((G/'cycle3'/v['checks']).read_text())['status']=='pass'
  action(['resume'],f'{cursor:03}_resume');action(['run','--steps','5'],f'{cursor:03}_run');action(['verify'],f'{cursor:03}_verify');check_old()
  assert json.loads((E/'STATE.json').read_text())['next_step']==cursor+5 and (E/'PAUSE').exists()
  print(json.dumps(dict(verified_cursor=cursor+5)),flush=True)
 rows=[json.loads((E/'events'/f'{i:06}.json').read_text()) for i in range(start,end)];index=[dict(step=x['step'],host_kind=x['host_result']['kind'],input_tokens=len(x['input_token_ids']),output_tokens=len(x['generated_token_ids']),stop=x['stop']) for x in rows];flagged=[x for x in rows if x['host_result']['kind']!='record_receipt'];selected={start,start+4,end-1}|{x['step'] for x in flagged}
 packet=[dict(step=x['step'],text=x['text'][:650],excerpted=len(x['text'])>650,host_result=x['host_result']) for x in rows if x['step'] in selected];s=dict(start=start,end=end,calls=10,host_kinds=dict(collections.Counter(x['host_result']['kind'] for x in rows)),output_tokens=sum(len(x['generated_token_ids']) for x in rows),caps=sum(x['stop']=='token_limit' for x in rows),max_input_tokens=max(len(x['input_token_ids']) for x in rows),generation_seconds=sum(x['seconds'] for x in rows),distinct_exact_replies=len({x['text'] for x in rows}),nonordinary_host_steps=[x['step'] for x in flagged],checkpoints=[start+5,end])
 for name,value in [('SUMMARY',s),('INDEX',index),('PACKET',packet)]:
  with (R/f'{end:03}_{name}.json').open('x') as f:json.dump(value,f,indent=2);f.write('\n')
 print(json.dumps(s),flush=True)
if __name__=='__main__':run(int(sys.argv[1]))
