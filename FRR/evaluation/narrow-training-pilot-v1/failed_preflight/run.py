"""Frozen bounded local SFT pilot, separate checkpoint, no network or gold eval-key parsing."""
from pathlib import Path
import os,json,time,hashlib,random,gc,resource,platform
os.environ['HF_HUB_OFFLINE']='1'
os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'
import torch,transformers
import torch.nn.functional as F
from transformers import AutoTokenizer,AutoModelForCausalLM
from safetensors.torch import save_file
P=Path(__file__).resolve().parent
MODEL=Path('/workspace/cache_backend_models/smollm2-135m')
CHECKPOINT=Path('/workspace/narrow_training_checkpoint_v1')
STATES=Path('/workspace/smollm_narrow_training_states_v1')

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def dump(p,v):
 with p.open('x') as f:f.write(json.dumps(v,indent=2)+'\n')
def load(path):
 return AutoModelForCausalLM.from_pretrained(path,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
def run():
 assert not (P/'RAW_OUTPUTS.jsonl').exists() and not CHECKPOINT.exists() and not STATES.exists()
 for n,h in json.loads((P/'FREEZE.json').read_text())['sha256'].items():assert sha(P/n)==h,n
 old=json.loads((P/'PRESERVATION_BEFORE.json').read_text())
 for name,h in old['model_and_cache_sha256'].items():assert sha(Path(name))==h,name
 torch.set_num_threads(2);torch.manual_seed(20261030)
 tok=AutoTokenizer.from_pretrained(MODEL,local_files_only=True,trust_remote_code=False)
 guidance=json.loads((P/'GUIDANCE.json').read_text())
 cases=json.loads((P/'EVAL_CASES.json').read_text()) # Contains no evaluation labels/target values.
 train=json.loads((P/'TRAIN.json').read_text())
 STATES.mkdir();rows=[]
 def prompt(case):
  return [{'role':'user','content':guidance['instruction']+'\n\nRecord:\n'+case['source']+'\n\n'+guidance['question']}]
 def evaluate(model,chosen,arm):
  model.eval()
  with torch.inference_mode():
   for c in chosen:
    messages=prompt(c);rendered=tok.apply_chat_template(messages,tokenize=False,add_generation_prompt=True)
    ids=tok.apply_chat_template(messages,tokenize=True,add_generation_prompt=True,return_tensors='pt')
    begin=time.perf_counter();o=model(input_ids=ids,attention_mask=torch.ones_like(ids),use_cache=True)
    cache=o.past_key_values;logits=o.logits[:,-1,:];new=[];stop='token_limit'
    for step in range(8):
     nxt=int(logits.argmax(-1).item());new.append(nxt)
     if nxt==tok.eos_token_id:stop='eos';break
     if step==7:break
     o=model(input_ids=torch.tensor([[nxt]]),past_key_values=cache,use_cache=True,attention_mask=torch.ones((1,cache.get_seq_length()+1),dtype=torch.long));cache=o.past_key_values;logits=o.logits[:,-1,:]
    elapsed=time.perf_counter()-begin;text=tok.decode(new,skip_special_tokens=True)
    rid=c['id']+'__'+arm;f=STATES/(rid+'.safetensors');full=ids[0].tolist()+new;count=int(cache.get_seq_length())
    arrays={f'layer{i}_{kind}':v.detach().cpu().contiguous() for i,pair in enumerate(cache.to_legacy_cache()) for kind,v in zip(('k','v'),pair)}
    sb=time.perf_counter();save_file(arrays,str(f));ser=time.perf_counter()-sb
    row={'run_id':rid,'record_id':c['id'],'family':'narrow_source_state','facet':'state_label','cycle':'NT1','arm':arm,'structure_family':c['structure_family'],'messages':messages,'rendered_prompt':rendered,'input_token_ids':ids[0].tolist(),'generated_token_ids':new,'text':text,'stop':stop,'input_tokens':int(ids.shape[1]),'output_tokens':len(new),'inference_seconds_excluding_serialization':elapsed,'serialization_seconds':ser,'checkpoint_kind':'original' if arm.startswith('original') else 'adapted','cache_artifact':{'local_path':str(f),'sha256':sha(f),'bytes':f.stat().st_size,'cache_token_count':count,'all_sequence_token_ids':full,'cached_token_prefix_sha256':hashlib.sha256(json.dumps(full[:count],separators=(',',':')).encode()).hexdigest()}}
    with (P/'RAW_OUTPUTS.jsonl').open('a') as stream:stream.write(json.dumps(row)+'\n')
    rows.append(row);print(json.dumps({'run':rid,'text':text,'stop':stop}),flush=True)
 model=load(MODEL)
 evaluate(model,[c for c in cases if c['split']=='dev'],'original_dev')
 batches=[]
 for c in train:
  inp=tok.apply_chat_template(prompt(c),tokenize=True,add_generation_prompt=True)
  target=tok.encode(c['label'],add_special_tokens=False)+[tok.eos_token_id]
  batches.append((inp+target,[-100]*len(inp)+target))
 assert max(len(a) for a,b in batches)<=160,'No silent truncation'
 order=list(range(len(train)));random.Random(20261030).shuffle(order)
 optimizer=torch.optim.AdamW(model.parameters(),lr=1e-4,weight_decay=.01,foreach=False)
 model.train();start=time.perf_counter();completed=0;stop='fixed_48_steps';losses=[]
 for step in range(48):
  if time.perf_counter()-start>=240:stop='wall_time_cap';break
  current=int(Path('/sys/fs/cgroup/memory.current').read_text())
  memstat=dict(line.split() for line in Path('/sys/fs/cgroup/memory.stat').read_text().splitlines())
  working=current-int(memstat.get('inactive_file',0))
  if working>.6*8589934592:stop='memory_headroom';break
  batch=[batches[i] for i in order[2*step:2*step+2]];length=max(len(x[0]) for x in batch)
  x=torch.full((2,length),tok.eos_token_id,dtype=torch.long);y=torch.full_like(x,-100);mask=torch.zeros_like(x)
  for j,(a,b) in enumerate(batch):x[j,:len(a)]=torch.tensor(a);y[j,:len(b)]=torch.tensor(b);mask[j,:len(a)]=1
  begin=time.perf_counter();optimizer.zero_grad(set_to_none=True)
  logits=model(input_ids=x,attention_mask=mask,use_cache=False).logits[:,:-1,:]
  shifted=y[:,1:];per=F.cross_entropy(logits.reshape(-1,logits.shape[-1]),shifted.reshape(-1),ignore_index=-100,reduction='none').reshape(2,-1)
  loss=(per.sum(1)/(shifted!=-100).sum(1)).mean()
  if not torch.isfinite(loss):stop='nonfinite_loss';break
  loss.backward();grad=torch.nn.utils.clip_grad_norm_(model.parameters(),1.,foreach=False)
  if not torch.isfinite(grad):stop='nonfinite_gradient';break
  optimizer.step();completed+=1
  item={'step':completed,'loss':float(loss.detach()),'preclip_gradient_norm':float(grad),'seconds':time.perf_counter()-begin,'training_example_ids':[train[i]['id'] for i in order[2*step:2*step+2]],'cgroup_memory_before_step':current,'cgroup_working_estimate_before_step':working}
  with (P/'TRAINING_LOG.jsonl').open('a') as f:f.write(json.dumps(item)+'\n')
  losses.append(item['loss'])
  if completed%8==0:print(json.dumps({'training_step':completed,'loss':item['loss']}),flush=True)
 training_seconds=time.perf_counter()-start
 CHECKPOINT.mkdir();model.save_pretrained(CHECKPOINT,safe_serialization=True);tok.save_pretrained(CHECKPOINT)
 torch.save({'optimizer':optimizer.state_dict(),'completed_steps':completed,'seed':20261030,'training_order':order},CHECKPOINT/'optimizer_state.pt')
 checkpoint_hashes={f.name:sha(f) for f in CHECKPOINT.iterdir() if f.is_file()}
 dump(P/'TRAINING_MANIFEST.json',{'base_model':'HuggingFaceTB/SmolLM2-135M-Instruct','revision':'12fd25f77366fa6b3b4b768ec3050bf629380bac','completed_steps':completed,'stop':stop,'training_seconds':training_seconds,'peak_process_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,'max_training_sequence_tokens':max(len(x[0]) for x in batches),'checkpoint_directory':str(CHECKPOINT),'checkpoint_sha256':checkpoint_hashes,'first_loss':losses[0] if losses else None,'last_loss':losses[-1] if losses else None,'optimizer_state_preserved':True,'torch':torch.__version__,'transformers':transformers.__version__,'python':platform.python_version(),'scope':'one fixed full-weight fine-tuning pilot, no original disk-weight overwrite; no hyperparameter selection'})
 optimizer.zero_grad(set_to_none=True);del optimizer;gc.collect();model.eval()
 # The first held-out test forward pass occurs only after training and checkpoint save.
 evaluate(model,[c for c in cases if c['split']=='dev'],'adapted_dev')
 evaluate(model,[c for c in cases if c['split']=='test'],'adapted_test')
 del model;gc.collect();model=load(MODEL)
 evaluate(model,[c for c in cases if c['split']=='test'],'original_test')
 dump(P/'RUN_MANIFEST.json',{'calls':len(rows),'test_not_forwarded_before_training_complete':True,'eval_keys_hashed_but_not_parsed_or_prompted':True,'training_labels_used_for_supervised_updates':True,'generation_cap':8,'actual_training_steps':completed,'network':False,'training_checkpoint_separate':True})
if __name__=='__main__':run()
