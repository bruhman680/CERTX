"""Run exactly the authorized 320→370 continuation, in checked five-entry windows."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json,os,subprocess,sys,traceback
R=Path(__file__).resolve().parent;ROOT=R.parent.parent;G=ROOT/'evaluation/source-access-three-cycle-v1';ENV=G/'cycle3/environment';PYTHON='/workspace/cache_backend_venv/bin/python'
sys.path.insert(0,str(G));sys.path.insert(0,str(ROOT/'evaluation/discovery-play-patch-v1'))
import world_routine as runner
from primary_adapter import Binding

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot(target):
 state=json.loads((ENV/'STATE.json').read_text());pointer=json.loads((ENV.parent/'CURRENT_VERIFY.json').read_text());assert state['next_step']==target==pointer['next_step'];assert (ENV/'PAUSE').exists() and not (ENV/'RUN.lock').exists();assert json.loads((ENV.parent/pointer['checks']).read_text())['status']=='pass'
 _,events,allrows=runner.Journal(ENV).state();rows=[x for x in allrows if x['step']>=320];assert len(rows)==target-320;value=Binding(305).replay(events)
 before=json.loads((R/'PRIMARY_BEFORE.json').read_text());mutable={'evaluation/source-access-three-cycle-v1/cycle3/environment/STATE.json','evaluation/source-access-three-cycle-v1/cycle3/environment/NOTEBOOK.jsonl','evaluation/source-access-three-cycle-v1/cycle3/CURRENT_VERIFY.json'}
 assert all((ROOT/p).is_file() and sha(ROOT/p)==h for p,h in before.items() if p not in mutable)
 prefix=b''.join((ENV/'NOTEBOOK.jsonl').read_bytes().splitlines(keepends=True)[:320]);assert hashlib.sha256(prefix).hexdigest()==before['evaluation/source-access-three-cycle-v1/cycle3/environment/NOTEBOOK.jsonl']
 notes=[dict(step=x['step'],text=x['text'],stop=x['stop'],input_tokens=len(x['input_token_ids']),output_tokens=len(x['generated_token_ids']),host_result=x['host_result'],exact_reply_in_input=bool(x['text'].strip()) and x['text'].strip() in x['prompt']) for x in rows]
 recent=rows[-5:];world=[x for x in rows if x['host_result']['kind']=='play_patch_receipt'];old=rows[:-5];novel_kinds=sorted(set(x['host_result']['kind'] for x in recent)-set(['record_receipt']+[x['host_result']['kind'] for x in old]))
 result=dict(status='pass',start=320,next_step=target,calls=len(rows),verification=pointer['verification'],paused=True,world_number=value,world_commands=len(world),world_statuses=dict(Counter(x['host_result']['status'] for x in world)),host_kinds=dict(Counter(x['host_result']['kind'] for x in rows)),stop_kinds=dict(Counter(x['stop'] for x in rows)),generated_tokens=sum(len(x['generated_token_ids']) for x in rows),new_host_kinds_this_window=novel_kinds,old_immutable_files_checked=len(before)-3,old_immutable_files_unchanged=True,old_320_notebook_exact_prefix=True,events=notes)
 p=R/f'CHECKPOINT_{target}.json'
 with p.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
 public={k:v for k,v in result.items() if k!='events'};print(json.dumps(public),flush=True)
 (R/'STATUS.json').write_text(json.dumps(public,indent=2)+'\n')
 if target in (340,360,370):
  (R/f'SUMMARY_{target}.md').write_text(f'# Continuation to {target}\n\n{len(rows)} new entries since320; verifier{pointer["verification"]}passes. Host kinds: {dict(Counter(x["host_result"]["kind"] for x in rows))}. World commands:{len(world)}, current number:{value}. Stop kinds:{dict(Counter(x["stop"] for x in rows))}. This is descriptive; no model understanding or phase change is inferred. Raw outputs are retained in the primary and checkpoint.\n')
 return result

def invoke(action,target,extra=()):
 with (R/f'WINDOW_{target}_{action.upper()}.log').open('x') as log:
  subprocess.run([PYTHON,str(G/'world_routine.py'),action,*extra],check=True,stdout=log,stderr=subprocess.STDOUT)
def main():
 p=argparse.ArgumentParser();p.add_argument('--until',type=int,default=370);a=p.parse_args();assert a.until in range(325,371,5)
 lock=R/'BLOCK.lock';fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY);os.write(fd,str(os.getpid()).encode());os.close(fd)
 try:
  current=json.loads((ENV/'STATE.json').read_text())['next_step'];assert current in range(320,371,5) and current<a.until;assert (ENV/'PAUSE').exists() and not (ENV/'RUN.lock').exists()
  if current!=320:assert json.loads((R/f'CHECKPOINT_{current}.json').read_text())['status']=='pass'
  runner.freeze_check()
  for target in range(current+5,a.until+1,5):
   invoke('resume',target);invoke('run',target,('--steps','5'));invoke('verify',target);snapshot(target)
  print('Authorized block boundary reached; primary paused.',flush=True)
 except BaseException as exc:
  (ENV/'PAUSE').touch();(R/'ERROR.json').write_text(json.dumps(dict(error=repr(exc),traceback=traceback.format_exc(),instruction='Inspect logs, plans and events; no silent retry'),indent=2)+'\n');raise
 finally:lock.unlink(missing_ok=True)
if __name__=='__main__':main()
