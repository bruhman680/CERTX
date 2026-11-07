"""Three-call connection pilot; deliberately not activation of the primary history."""
from pathlib import Path
import hashlib,json,os,sys
H=Path(__file__).resolve().parent
G=H.parent/'source-access-three-cycle-v1'
E=G/'cycle3/environment'
sys.path[:0]=[str(G),'/workspace']
from workspace import execute, NOTICE, snapshot

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,v):
 with Path(p).open('x') as f: json.dump(v,f,indent=2);f.write('\n')
def primary():
 return {str(p.relative_to(E)):sha(p) for p in E.rglob('*') if p.is_file()}

def main():
 before=primary();assert (E/'PAUSE').exists();assert json.loads((E/'STATE.json').read_text())['next_step']==750
 out=H/'pilot';out.mkdir();home=out/'world';home.mkdir();records=out/'observer';records.mkdir()
 # Only model-authored replies, not old prompts, feedback or researcher opinions.
 history=[json.loads(l) for l in (E/'NOTEBOOK.jsonl').read_text().splitlines()]
 (home/'prior_replies.jsonl').write_text(''.join(json.dumps({'entry':r['step']+1,'text':r['reply']})+'\n' for r in history))
 material=json.loads((H.parent/'minimal-markov-preparation-v1/TABLE_VIEW_DRAFT.json').read_text())['material']
 (home/'transitions.json').write_text(json.dumps({'states':list(range(8)),'transition_matrices':material}))
 (home/'LAWS.txt').write_text('Each matrix is a separate discrete-time system. States are numbered 0 to 7. Entry [i][j] is the probability of the next state being j given current state i. Rows sum to one. These are data; no simulation advances automatically. prior_replies.jsonl contains earlier model replies under an older environment.\n')
 save(records/'PRIMARY_BEFORE.json',before)
 save(records/'INITIAL_WORLD.json',snapshot(home))
 os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'
 import torch
 from transformers import AutoModelForCausalLM,AutoTokenizer
 from runtime_reference import Guard,parameter_digest
 from generate_capacity import generate
 base=Path('/workspace/cache_backend_models/smollm2-135m')
 weights=sha(base/'model.safetensors');assert weights=='5af571cbf074e6d21a03528d2330792e532ca608f24ac70a143f6b369968ab8c'
 torch.set_num_threads(2);guard=Guard(5153960755,records/'RESOURCE.jsonl');guard.read('load')
 tok=AutoTokenizer.from_pretrained(base,local_files_only=True,trust_remote_code=False)
 model=AutoModelForCausalLM.from_pretrained(base,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');model.eval()
 digest=(parameter_digest(model,False),parameter_digest(model,True))
 save(records/'CONDITION.json',dict(parent_entry=750,role='connection pilot, not primary continuation',model=str(base),weights_sha256=weights,added_adapter=False,training_updates=0,input_limit=8096,output_limit=96,temperature=.8,top_p=.9,notice=NOTICE))
 previous=None
 for n in range(3):
  listing=sorted(p.name for p in home.iterdir())
  prompt=NOTICE+'\nCurrent directory entries: '+json.dumps(listing)
  if previous is not None: prompt+='\nPrevious reply and actual result: '+json.dumps(previous)
  prompt+='\n'
  save(records/f'{n:03d}_PLAN.json',dict(prompt=prompt,before=snapshot(home),rng_seed=120850+n))
  raw=generate(model,tok,prompt,guard,f'workspace_pilot_{n}',120850+n)
  save(records/f'{n:03d}_RAW.json',raw) # preserved before executing anything
  result=execute(home,raw['text']);save(records/f'{n:03d}_RESULT.json',result)
  # Visible history is exactly the immediately prior action and its actual consequence.
  previous={k:result[k] for k in ['source','stdout','stderr','exit_code','boundary']}
  if result['pause_required']: break
 assert digest==(parameter_digest(model,False),parameter_digest(model,True));assert sha(base/'model.safetensors')==weights
 assert primary()==before
 save(records/'CHECKS.json',dict(primary_all_files_unchanged=True,primary_entry=750,paused=True,model_calls=n+1,weights_unchanged=True,training_updates=0,observer_directory_outside_mount=True))
 (out/'PAUSE').touch()
 print(json.dumps({'pilot_calls':n+1,'primary_entry':750,'primary_unchanged':True}))

if __name__=='__main__':main()
