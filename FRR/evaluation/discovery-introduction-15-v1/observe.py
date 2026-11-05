"""Read-only primary observation; writes only this contact's derived records."""
from pathlib import Path
from collections import Counter
import hashlib,json,sys
R=Path(__file__).resolve().parent;ROOT=R.parent.parent;G=ROOT/'evaluation/source-access-three-cycle-v1';ENV=G/'cycle3/environment'
sys.path.insert(0,str(G));sys.path.insert(0,str(ROOT/'evaluation/discovery-play-patch-v1'))
import world_routine as runner
from primary_adapter import Binding

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def observe(target):
 state=json.loads((ENV/'STATE.json').read_text());assert state['next_step']==target;assert (ENV/'PAUSE').exists() and not (ENV/'RUN.lock').exists()
 pointer=json.loads((ENV.parent/'CURRENT_VERIFY.json').read_text());check=json.loads((ENV.parent/pointer['checks']).read_text());assert pointer['next_step']==target and check['status']=='pass'
 _,events,allrows=runner.Journal(ENV).state();rows=[x for x in allrows if x['step']>=305];assert len(rows)==target-305
 binding=Binding(305);value=binding.replay(events);world=[x for x in rows if x['host_result']['kind']=='play_patch_receipt']
 notes=[]
 for x in rows:
  text=x['text'];notes.append(dict(step=x['step'],entry_after=x['step']+1,text=text,stop=x['stop'],input_tokens=len(x['input_token_ids']),output_tokens=len(x['generated_token_ids']),host_result=x['host_result'],exact_reply_in_input=bool(text.strip()) and text.strip() in x['prompt'],world_word_mention=any(w in text.upper() for w in ('TOUCH A','TOUCH B','LOOK'))))
 before=json.loads((R/'PRIMARY_BEFORE.json').read_text());mutable={'evaluation/source-access-three-cycle-v1/cycle3/environment/STATE.json','evaluation/source-access-three-cycle-v1/cycle3/environment/NOTEBOOK.jsonl','evaluation/source-access-three-cycle-v1/cycle3/CURRENT_VERIFY.json'}
 old_notebook_key='evaluation/source-access-three-cycle-v1/cycle3/environment/NOTEBOOK.jsonl';prefix=b''.join((ENV/'NOTEBOOK.jsonl').read_bytes().splitlines(keepends=True)[:305]);assert hashlib.sha256(prefix).hexdigest()==before[old_notebook_key]
 changed=[p for p,h in before.items() if p not in mutable and (not (ROOT/p).is_file() or sha(ROOT/p)!=h)];assert not changed,changed
 result=dict(status='pass',scope='Descriptive observation, not model understanding/performance proof',start=305,next_step=target,new_model_calls=len(rows),verification=pointer['verification'],paused=True,active_version=runner.NEW_VERSION,host_kinds=dict(Counter(x['host_result']['kind'] for x in rows)),stop_kinds=dict(Counter(x['stop'] for x in rows)),generated_tokens=sum(len(x['generated_token_ids']) for x in rows),world_commands=len(world),world_action_statuses=dict(Counter(x['host_result']['status'] for x in world)),world_number=value,training_updates=0,old_files_checked_excluding_three_projections=len(before)-len(mutable),old_source_files_unchanged=True,old_notebook_exact_prefix_preserved=True,events=notes)
 (R/f'CHECKPOINT_{target}.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='events'},indent=2));print(json.dumps(notes[-5:],indent=2))
if __name__=='__main__':observe(int(sys.argv[1]))
