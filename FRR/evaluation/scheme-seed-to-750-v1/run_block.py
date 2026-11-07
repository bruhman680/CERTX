"""Up to ten entries per checked window; pause for review on non-note events."""
from pathlib import Path
import hashlib,json,os,subprocess,sys
H=Path(__file__).resolve().parent;G=H.parent/'source-access-three-cycle-v1';E=G/'cycle3/environment';RUN=H/'seeded_routine.py';PY=Path('/workspace/cache_backend_venv/bin/python')
MUTABLE={'cycle3/CURRENT_VERIFY.json','cycle3/environment/NOTEBOOK.jsonl','cycle3/environment/STATE.json','cycle3/environment/PAUSE','cycle3/environment/ACTIVE_RUNNER.json'}
def read(p):return json.loads(p.read_text())
def checkpoint(expected):
 assert read(E/'STATE.json')['next_step']==expected and (E/'PAUSE').exists() and not (E/'RUN.lock').exists()
 latest=read(E.parent/'CURRENT_VERIFY.json');assert latest['next_step']==expected and read(E.parent/latest['checks'])['status']=='pass'
 for rel,digest in read(H/'before/PRIMARY_INVENTORY.json').items():
  if rel not in MUTABLE:assert hashlib.sha256((G/rel).read_bytes()).hexdigest()==digest,rel
 return latest

def command(action,label,extra=()):
 with (H/f'{label}.stdout').open('xb') as out,(H/f'{label}.stderr').open('xb') as err:r=subprocess.run([str(PY),str(RUN),action,*extra],stdout=out,stderr=err)
 assert r.returncode==0,f'{label} failed: inspect retained records; no automatic retry'
if __name__=='__main__':
 for request in H.glob('ATTENTION_*.json'):
  if request.stem.endswith('_REVIEW'):continue
  assert (H/(request.stem+'_REVIEW.json')).exists(),'Observer review required before continuing'
 lock=H/'BLOCK.lock';fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY);os.write(fd,str(os.getpid()).encode());os.close(fd)
 try:
  start=read(E/'STATE.json')['next_step'];assert 650<=start<750 and (E/'scheme_world/world.sqlite').is_file();checkpoint(start)
  while start<750:
   n=len(list(H.glob('WINDOW_*_SUMMARY.json')))+1;requested=min(10,750-start)
   command('resume',f'WINDOW_{n:03d}_RESUME');command('run',f'WINDOW_{n:03d}_RUN',('--steps',str(requested)))
   end=read(E/'STATE.json')['next_step'];assert start<end<=start+requested
   command('verify',f'WINDOW_{n:03d}_VERIFY');latest=checkpoint(end)
   rows=[read(E/'events'/f'{i:06d}.json') for i in range(start,end)]
   kinds=[r['host_result']['kind'] for r in rows];attention=any(k!='record_receipt' for k in kinds) or end<start+requested
   summary=dict(window=n,start_step=start,next_step=end,calls=end-start,requested=requested,verification=latest['verification'],host_kinds=kinds,stops=[r['stop'] for r in rows],scheme_submissions=sum(k=='scheme_receipt' for k in kinds),max_input_tokens=max(len(r['input_token_ids']) for r in rows),attention_required=attention)
   with (H/f'WINDOW_{n:03d}_SUMMARY.json').open('x') as f:json.dump(summary,f,indent=2);f.write('\n')
   print(json.dumps(summary),flush=True)
   if attention:
    with (H/f'ATTENTION_{n:03d}.json').open('x') as f:json.dump(dict(window=n,next_step=end,steps=[r['step'] for r in rows if r['host_result']['kind']!='record_receipt'],reason='Non-note event or early pause; inspect before resume'),f,indent=2);f.write('\n')
    print('Observer review requested; paused.',flush=True);break
   start=end
  if read(E/'STATE.json')['next_step']==750:
   checkpoint(750)
   with (H/'COMPLETED.json').open('x') as f:json.dump(dict(status='pass',start=650,next_step=750,new_calls=100,windows=len(list(H.glob('WINDOW_*_SUMMARY.json'))),max_checked_window=10,paused=True),f,indent=2);f.write('\n')
 except BaseException:(E/'PAUSE').touch();raise
 finally:lock.unlink()
