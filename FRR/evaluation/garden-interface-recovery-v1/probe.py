"""Prospective minimal-interface diagnostics; canonical garden is read-only."""
from pathlib import Path
import hashlib, json, os, shlex, sys, time
for k,v in {'HF_HUB_OFFLINE':'1','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'2'}.items(): os.environ[k]=v
H=Path(__file__).resolve().parent;P=H.parent/'final-garden-contract-v1'
sys.path[:0]=[str(P),str(P.parent/'source-access-three-cycle-v1')]
import runner
from world import World,action
from runtime_reference import Guard,parameter_digest

REQUESTS={
 'json_copy':'Return exactly this JSON object and nothing else:\n{"action":"shell","source":"pwd"}',
 'json_formulate':'Run pwd using a shell action. Return only a JSON object with exactly action="shell" and source set to the command string. No Markdown or explanation.',
 'shell_source':'Write only the shell command that prints the current working directory. No Markdown, code fences, or explanation.',
 'python_source':'Write only Python source code that prints the current working directory. No Markdown, code fences, or explanation.',
 'word_copy':'Repeat exactly this word and nothing else: pwd',
}

def save(name,value):
 p=H/name;p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x') as f:json.dump(value,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')

def main():
 import torch
 from transformers import AutoTokenizer,AutoModelForCausalLM
 before=runner.file_inventory(P);assert before==runner.read(P.parent/'detached-action-interface-control-v1/CANONICAL_BEFORE.json')
 runner.verify_pins();assert runner.state()['paused'] and runner.state()['next_entry']==1550
 conditions=[]
 for task in REQUESTS:
  for frame in ['empty','factory']:
   conditions.append(dict(id=task+'_'+frame+'_greedy',task=task,frame=frame,decode='greedy',seed=None))
 for frame in ['empty','factory']:
  conditions.append(dict(id='json_copy_'+frame+'_sampled',task='json_copy',frame=frame,decode='full_softmax',seed=121605))
 save('PLAN.json',dict(max_primary_calls=12,max_total_authorized_calls=24,conditions=conditions,requests=REQUESTS,scope='Minimal presentation/decoding exploration. Twelve declared primary one-step calls; potential second stage requires separate prospective plan. No behavioral framework, no training, no network/download, no canonical contact.',budget=96))
 save('CANONICAL_BEFORE.json',before)
 torch.set_num_threads(2);guard=Guard(5153960755,H/'RESOURCE.jsonl');guard.read('before_load')
 tok=AutoTokenizer.from_pretrained(runner.BASE,local_files_only=True,trust_remote_code=False)
 model=AutoModelForCausalLM.from_pretrained(runner.BASE,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
 model.requires_grad_(False);model.eval();pin=runner.read(runner.R/'MODEL_CONDITION.json')['tensor_digest'];assert parameter_digest(model,False)==pin
 save('PROVENANCE.json',dict(model_weights_sha256=runner.WEIGHTS,tensor_digest=pin,config=runner.read(runner.BASE/'config.json'),tokenizer_sha256=runner.digest(runner.BASE/'tokenizer.json'),tokenizer_config=runner.read(runner.BASE/'tokenizer_config.json')))
 checkpoint=runner.read(runner.R/'bundles/001550.json');results=[]
 for c in conditions:
  messages=([{'role':'system','content':''}] if c['frame']=='empty' else [])+[{'role':'user','content':REQUESTS[c['task']]}]
  ids=tok.apply_chat_template(messages,tokenize=True,add_generation_prompt=True);new=[];stop='token_limit';rng=torch.Generator(device='cpu');rng.manual_seed(c['seed'] or 0)
  guard.read('before_generate',condition=c['id']);start=time.perf_counter()
  with torch.inference_mode():
   x=torch.tensor([ids]);out=model(input_ids=x,attention_mask=torch.ones_like(x),use_cache=True,logits_to_keep=1);cache,logits=out.past_key_values,out.logits[0,-1]
   for i in range(96):
    if c['decode']=='greedy':t=int(logits.argmax())
    else:
     v,ix=torch.sort(logits.float()/.8,descending=True);pick=int(torch.multinomial(torch.softmax(v,0),1,generator=rng));t=int(ix[pick])
    new.append(t)
    if t==tok.eos_token_id:stop='eos';break
    if i<95:
     out=model(input_ids=torch.tensor([[t]]),past_key_values=cache,attention_mask=torch.ones((1,cache.get_seq_length()+1),dtype=torch.long),use_cache=True,logits_to_keep=1);cache,logits=out.past_key_values,out.logits[0,-1]
  text=tok.decode(new,skip_special_tokens=True)
  raw=dict(condition=c,messages=messages,rendered=tok.apply_chat_template(messages,tokenize=False,add_generation_prompt=True),input_token_ids=ids,generated_token_ids=new,text=text,stop=stop,seconds=time.perf_counter()-start)
  save('raw/'+c['id']+'.json',raw)
  source=None;dispatch=None
  if c['task'].startswith('json_'):
   source=action(text);dispatch='shell' if source is not None else None
  elif c['task']=='shell_source' or c['task']=='word_copy':
   # Raw declared source channel. Fences/prose are never stripped.
   source=text;dispatch='shell'
  elif c['task']=='python_source':
   source='python3 -I -S -c '+shlex.quote(text);dispatch='python'
  receipt=None;after=None
  if source is not None:
   w=World()
   try:
    w.restore(checkpoint,runner.R/'objects');receipt=w.execute(source);after=w.capture(H/'objects')
   finally:w.close()
  success=bool(receipt is not None and receipt['exit_code']==0 and receipt['boundary'] is None and receipt['stdout']=='/world\n')
  row=dict(condition=c['id'],task=c['task'],frame=c['frame'],decode=c['decode'],text=text,stop=stop,dispatch=dispatch,receipt=receipt,printed_actual_cwd=success,after=after)
  save('results/'+c['id']+'.json',row);results.append(row)
  assert runner.file_inventory(P)==before
  print(json.dumps(row,ensure_ascii=False),flush=True)
 assert parameter_digest(model,False)==pin and runner.file_inventory(P)==before
 save('COMPLETED.json',dict(status='pass',calls=len(conditions),canonical_calls=0,canonical_unchanged=True,results=results))
 print(json.dumps({'completed_calls':len(conditions),'successful_conditions':[r['condition'] for r in results if r['printed_actual_cwd']]}),flush=True)

if __name__=='__main__':main()
