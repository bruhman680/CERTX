"""External observer for the100-entry authorised block, not model-facing."""
from pathlib import Path
import sys,json,hashlib,collections,subprocess
R=Path(__file__).resolve().parent;ROOT=R.parent.parent;G=ROOT/'evaluation/source-access-three-cycle-v1';E=G/'cycle3/environment';PY='/workspace/cache_backend_venv/bin/python'
SEGMENTS={215:205,225:215,245:225,265:245,285:265,305:285}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check_old():
 mutable={'evaluation/source-access-three-cycle-v1/cycle3/environment/NOTEBOOK.jsonl','evaluation/source-access-three-cycle-v1/cycle3/environment/STATE.json','evaluation/source-access-three-cycle-v1/cycle3/CURRENT_VERIFY.json','evaluation/source-access-three-cycle-v1/cycle3/environment/PAUSE'}
 for p,h in json.loads((R/'PRIMARY_BEFORE.json').read_text()).items():
  if p not in mutable:assert sha(ROOT/p)==h,p
 assert (E/'NOTEBOOK.jsonl').read_bytes().startswith((R/'before/evaluation/source-access-three-cycle-v1/cycle3/environment/NOTEBOOK.jsonl').read_bytes())
def action(args,stem):
 with (R/(stem+'.stdout')).open('x') as out,(R/(stem+'.stderr')).open('x') as err:subprocess.run([PY,'fundamental_routine.py']+args,cwd=G,stdout=out,stderr=err,check=True)
def run(end):
 start=SEGMENTS[end];check_old();assert json.loads((E/'STATE.json').read_text())['next_step']==start and (E/'PAUSE').exists()
 for cursor in range(start,end,5):
  v=json.loads((G/'cycle3/CURRENT_VERIFY.json').read_text());assert v['next_step']==cursor and json.loads((G/'cycle3'/v['checks']).read_text())['status']=='pass'
  action(['resume'],f'{cursor:03}_resume');action(['run','--steps','5'],f'{cursor:03}_run');action(['verify'],f'{cursor:03}_verify');check_old();assert json.loads((E/'STATE.json').read_text())['next_step']==cursor+5 and (E/'PAUSE').exists();print(json.dumps(dict(verified_cursor=cursor+5)),flush=True)
 rows=[json.loads((E/'events'/f'{i:06d}.json').read_text()) for i in range(start,end)];flags=[x for x in rows if x['host_result']['kind']!='record_receipt'];selected={start,start+(end-start)//2-1,end-1}|{x['step'] for x in flags}
 summary=dict(start=start,end=end,calls=end-start,host_kinds=dict(collections.Counter(x['host_result']['kind'] for x in rows)),calculator_expressions=dict(collections.Counter(x['host_result']['expression'] for x in rows if x['host_result']['kind']=='calculation')),caps=sum(x['stop']=='token_limit' for x in rows),output_tokens=sum(len(x['generated_token_ids']) for x in rows),max_input_tokens=max(len(x['input_token_ids']) for x in rows),distinct_exact_replies=len({x['text'] for x in rows}),generation_seconds=sum(x['seconds'] for x in rows),checkpoints=list(range(start+5,end+1,5)))
 packet=[dict(step=x['step'],text=x['text'][:700],excerpted=len(x['text'])>700,host_result=x['host_result'],stop=x['stop']) for x in rows if x['step'] in selected]
 index=[dict(step=x['step'],host_kind=x['host_result']['kind'],input_tokens=len(x['input_token_ids']),output_tokens=len(x['generated_token_ids']),stop=x['stop']) for x in rows]
 for name,data in [('SUMMARY',summary),('PACKET',packet),('INDEX',index)]:
  with (R/f'{end:03}_{name}.json').open('x') as f:json.dump(data,f,indent=2);f.write('\n')
 print(json.dumps(summary),flush=True)
if __name__=='__main__':run(int(sys.argv[1]))
