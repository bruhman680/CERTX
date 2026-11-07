"""Automatic verified continuation; researcher interpretation is not an approval gate.

Explicit invocation requires a target and fresh recording directory. No inference
runs at import. The existing pinned model-facing runner is not changed.
"""
from pathlib import Path
import argparse,json,subprocess
ROOT=Path('/workspace/frr/evaluation')
ENV=ROOT/'source-access-three-cycle-v1/cycle3/environment'
RUNNER=ROOT/'scheme-seed-to-750-v1/seeded_routine.py'
PY=Path('/workspace/cache_backend_venv/bin/python')
def read(path):return json.loads(Path(path).read_text())
def decision(session,checks):
 if checks.get('status')!='pass':return 'stop_integrity'
 if session.get('stop_reason')=='pause_requested':return 'stop_operator'
 if session.get('stop_reason') not in ('budget_pause','curious_event_pause'):return 'stop_runtime'
 if session.get('weights_unchanged') is not True or session.get('training_updates')!=0:return 'stop_integrity'
 return 'continue'
def command(action,record,label,extra=()):
 with (record/f'{label}.stdout').open('xb') as out,(record/f'{label}.stderr').open('xb') as err:
  result=subprocess.run([str(PY),str(RUNNER),action,*extra],stdout=out,stderr=err)
 if result.returncode:raise RuntimeError(f'{label}: runtime failure; retain records, no automatic retry')
def run(target,record):
 record=Path(record);record.mkdir(parents=True,exist_ok=False)
 start=read(ENV/'STATE.json')['next_step'];assert target>start and (ENV/'PAUSE').exists() and not (ENV/'RUN.lock').exists()
 assert (ENV/'scheme_world/world.sqlite').is_file(),'Restore missing persistent store from checked bundle; never create an empty replacement'
 command('verify',record,'BASELINE_VERIFY')
 current=start;window=0;reason='target_reached'
 while current<target:
  if (record/'STOP').exists():reason='stop_operator';break
  window+=1;before_sessions={p.name for p in (ENV/'sessions').glob('*.json')}
  command('resume',record,f'{window:03d}_RESUME')
  command('run',record,f'{window:03d}_RUN',('--steps',str(min(10,target-current))))
  command('verify',record,f'{window:03d}_VERIFY')
  latest=read(ENV.parent/'CURRENT_VERIFY.json');checks=read(ENV.parent/latest['checks'])
  end=read(ENV/'STATE.json')['next_step'];assert current<end<=target and latest['next_step']==end
  new_sessions=[p for p in (ENV/'sessions').glob('*.json') if p.name not in before_sessions];assert len(new_sessions)==1
  session=read(new_sessions[0]);assert session['start_step']==current and session['next_step']==end
  rows=[read(ENV/'events'/f'{i:06d}.json') for i in range(current,end)]
  # Raw results remain observations. Semantic success, failure, novelty, or
  # researcher approval never decide whether the next reply is allowed.
  observations=[dict(step=r['step'],host_result=r['host_result']) for r in rows]
  choice=decision(session,checks)
  with (record/f'{window:03d}_OBSERVATIONS.json').open('x') as f:
   json.dump(dict(start_step=current,next_step=end,verification=latest['verification'],observations=observations,controller_decision=choice,researcher_approval_required=False),f,indent=2);f.write('\n')
  current=end;print(json.dumps(dict(next_step=end,controller_decision=choice,researcher_approval_required=False)),flush=True)
  if choice!='continue':reason=choice;break
 with (record/'SUMMARY.json').open('x') as f:json.dump(dict(start_step=start,next_step=current,target=target,stop_reason=reason,windows=window,paused=(ENV/'PAUSE').exists(),researcher_approval_required=False),f,indent=2);f.write('\n')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--target',type=int,required=True);p.add_argument('--record-directory',type=Path,required=True);a=p.parse_args();run(a.target,a.record_directory)
