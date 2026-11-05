"""Replay old history in disposable clone; no model generation and no real-primary writes."""
import hashlib,json,shutil,tempfile,sys
from pathlib import Path
PACKAGE=Path(__file__).resolve().parent;sys.path.insert(0,str(PACKAGE))
from prepare_primary import G,DEFAULT_ENV,candidate_source,plan,activate
from world import Rules
from journal import Journal
from primary_adapter import Binding

def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 before={p:h(p) for p in G.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
 prepared=plan();(PACKAGE/'prepared_world_routine.py').write_text(candidate_source(DEFAULT_ENV))
 with tempfile.TemporaryDirectory(prefix='frr-world-fixture-') as td:
  root=Path(td);cycle=root/'cycle3';cycle.mkdir();env=cycle/'environment'
  shutil.copytree(DEFAULT_ENV,env);shutil.copytree(G/'cycle3/verification',cycle/'verification');shutil.copy2(G/'cycle3/CURRENT_VERIFY.json',cycle/'CURRENT_VERIFY.json')
  result=activate(env,root/'world_routine.py')
  checks=json.loads((cycle/'verification'/f"{result['verification']}_CHECKS.json").read_text());assert checks['status']=='pass';assert result['next_step']==305
  try:activate(env,root/'world_routine.py')
  except (FileExistsError,ValueError):pass
  else:raise AssertionError('Repeated activation must refuse reset')
  clone_result=dict(status='pass',next_step=305,calls_replayed=checks['calls'],verification=result['verification'],source_events_equal=all(p.read_bytes()==(env/'events'/p.name).read_bytes() for p in (DEFAULT_ENV/'events').glob('*.json')),repeat_activation_refused=True)
  assert clone_result['source_events_equal']
 # Read actual primary through old runner only; do not call project/verify/run.
 sys.path.insert(0,str(G));import boundary_routine as old
 _,events,_=old.Journal(DEFAULT_ENV).state();binding=Binding(305);preview=binding.render(old.boundary_view_render(events),events)
 from transformers import AutoTokenizer
 tok=AutoTokenizer.from_pretrained(old.parent.BASE,local_files_only=True,trust_remote_code=False)
 tokens=tok.apply_chat_template([{'role':'user','content':preview}],tokenize=True,add_generation_prompt=True);assert len(tokens)<=8096;assert binding.replay(events)==0
 (PACKAGE/'PREPARED_INPUT_PREVIEW.txt').write_text(preview)
 after={p:h(p) for p in G.rglob('*') if p.is_file() and '__pycache__' not in p.parts};assert before==after
 evidence=dict(status='pass',scope='Host integration, replay and tokenizer-only preview; no model generation',prepared_plan=prepared,clone_replay=clone_result,preview_input_tokens=len(tokens),input_limit=8096,primary_files_checked=len(before),primary_bytes_unchanged=True,primary_cursor=305,primary_verification=json.loads((G/'cycle3/CURRENT_VERIFY.json').read_text())['verification'],primary_paused=(DEFAULT_ENV/'PAUSE').exists(),new_world_active_in_primary=False)
 (PACKAGE/'INTEGRATION_CHECKS.json').write_text(json.dumps(evidence,indent=2)+'\n');print(json.dumps(evidence,indent=2))
if __name__=='__main__':main()
