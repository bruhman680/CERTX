"""Nine checked five-reply windows. No prompt/policy changes or automatic retries."""
from pathlib import Path
import hashlib,json,os,subprocess,sys
D=Path(__file__).resolve().parent
G=D.parent/'source-access-three-cycle-v1';E=G/'cycle3/environment'
RUN=D.parent/'scheme-primary-integration-v1/connected_routine_v2.py'
PY=Path('/workspace/cache_backend_venv/bin/python')
MUTABLE={'cycle3/CURRENT_VERIFY.json','cycle3/environment/NOTEBOOK.jsonl','cycle3/environment/STATE.json','cycle3/environment/PAUSE'}
def read(p):return json.loads(p.read_text())
def checkpoint(expected):
 assert read(E/'STATE.json')['next_step']==expected
 assert (E/'PAUSE').exists() and not (E/'RUN.lock').exists()
 latest=read(E.parent/'CURRENT_VERIFY.json');assert latest['next_step']==expected
 assert read(E.parent/latest['checks'])['status']=='pass'
 for rel,digest in read(D/'before/PRIMARY_INVENTORY.json').items():
  if rel not in MUTABLE:assert hashlib.sha256((G/rel).read_bytes()).hexdigest()==digest,rel
 return latest

def command(action,label,extra=()):
 with (D/f'{label}.stdout').open('xb') as out,(D/f'{label}.stderr').open('xb') as err:
  result=subprocess.run([str(PY),str(RUN),action,*extra],stdout=out,stderr=err)
 assert result.returncode==0,f'{label} failed; stop and inspect, no retry'

if __name__=='__main__':
 lock=D/'BLOCK.lock';fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY);os.write(fd,str(os.getpid()).encode());os.close(fd)
 try:
  assert read(E/'STATE.json')['next_step']==505 and (E/'scheme_world/world.sqlite').is_file()
  command('verify','BASELINE_VERIFY');checkpoint(505)
  for n,start in enumerate(range(505,550,5),1):
   checkpoint(start);command('resume',f'WINDOW_{n:02d}_RESUME')
   command('run',f'WINDOW_{n:02d}_RUN',('--steps','5'))
   command('verify',f'WINDOW_{n:02d}_VERIFY');latest=checkpoint(start+5)
   rows=[read(E/'events'/f'{i:06d}.json') for i in range(start,start+5)]
   summary=dict(window=n,start_step=start,next_step=start+5,verification=latest['verification'],
    host_kinds=[r['host_result']['kind'] for r in rows],stops=[r['stop'] for r in rows],
    scheme_actions=sum(r['host_result']['kind']=='scheme_receipt' for r in rows),
    max_input_tokens=max(len(r['input_token_ids']) for r in rows))
   with (D/f'WINDOW_{n:02d}_SUMMARY.json').open('x') as f:json.dump(summary,f,indent=2);f.write('\n')
   print(json.dumps(summary),flush=True)
  checkpoint(550)
  with (D/'COMPLETED.json').open('x') as f:json.dump(dict(status='pass',start=505,next_step=550,new_calls=45,windows=9,paused=True),f,indent=2);f.write('\n')
 except BaseException:
  (E/'PAUSE').touch();raise
 finally:lock.unlink()
