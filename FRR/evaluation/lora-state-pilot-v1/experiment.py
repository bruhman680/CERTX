"""Fixed local LoRA probe/pilot primitives. No networking or gold evaluation parsing."""
from pathlib import Path
import os,json,time,hashlib,resource
os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer,AutoModelForCausalLM
from safetensors.torch import save_file
from lora_cpu import inject_lora,save_adapter,load_adapter
P=Path(__file__).resolve().parent;BASE=Path('/workspace/cache_backend_models/smollm2-135m');LIMIT=8589934592
class Stop(Exception):pass

def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def dump(p,v):
 with Path(p).open('x') as f:f.write(json.dumps(v,indent=2)+'\n')
def mem(stage):
 stat=dict(line.split() for line in Path('/sys/fs/cgroup/memory.stat').read_text().splitlines());current=int(Path('/sys/fs/cgroup/memory.current').read_text());status=dict(line.split(':',1) for line in Path('/proc/self/status').read_text().splitlines() if ':' in line)
 return {'phase':stage,'cgroup_current':current,'inactive_file':int(stat.get('inactive_file',0)),'working_estimate':current-int(stat.get('inactive_file',0)),'process_rss':int(status['VmRSS'].split()[0])*1024,'process_peak_rss':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,'working_limit':int(.6*LIMIT)}
def check(point):
 if point['working_estimate']>=point['working_limit']:raise Stop('memory_headroom')
def base_digest(m):
 h=hashlib.sha256()
 for n,p in m.named_parameters():
  if not p.requires_grad:h.update(n.encode()+b'\0');h.update(p.detach().cpu().contiguous().numpy().tobytes())
 return h.hexdigest()
def setup(seed):
 torch.set_num_threads(2);torch.manual_seed(seed)
 tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False)
 m=AutoModelForCausalLM.from_pretrained(BASE,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
 return m,tok
G=json.loads((P/'GUIDANCE.json').read_text())
def prompt(c):return [{'role':'user','content':G['instruction']+'\n\nRecord:\n'+c['source']+'\n\n'+G['question']}]
def encode(tok,c,training=False):
 ids=tok.apply_chat_template(prompt(c),tokenize=True,add_generation_prompt=True)
 if not training:return ids
 target=tok.encode(c['label'],add_special_tokens=False)+[tok.eos_token_id]
 return ids+target,[-100]*len(ids)+target

def balanced_step(m,tok,opt,examples):
 points=[];losses=[];points.append(mem('before_update'));check(points[-1]);opt.zero_grad(set_to_none=True);m.train();start=time.perf_counter()
 try:
  for i,c in enumerate(examples):
   ids,labels=encode(tok,c,True);assert len(ids)<=256,'No truncation';x=torch.tensor([ids]);y=torch.tensor([labels])
   o=m(input_ids=x,attention_mask=torch.ones_like(x),use_cache=False)
   loss=F.cross_entropy(o.logits[:,:-1,:].reshape(-1,o.logits.shape[-1]),y[:,1:].reshape(-1),ignore_index=-100)
   points.append(mem(f'after_forward_{i}'));check(points[-1])
   if not torch.isfinite(loss):raise Stop('nonfinite_loss')
   (loss/len(examples)).backward();losses.append(float(loss.detach()));points.append(mem(f'after_backward_{i}'));check(points[-1])
  params=[p for p in m.parameters() if p.requires_grad];norm=torch.nn.utils.clip_grad_norm_(params,1.,foreach=False)
  if not torch.isfinite(norm):raise Stop('nonfinite_gradient')
  opt.step();points.append(mem('after_optimizer'))
  if not all(torch.isfinite(p).all() for p in params):raise Stop('nonfinite_adapter')
  return {'completed':True,'loss':sum(losses)/len(losses),'gradient_norm':float(norm),'seconds':time.perf_counter()-start,'points':points,'example_ids':[c['id'] for c in examples]}
 except Stop as exc:
  return {'completed':False,'stop':str(exc),'seconds':time.perf_counter()-start,'points':points,'example_ids':[c['id'] for c in examples],'micro_losses':losses}

def pin():return {'model_id':'HuggingFaceTB/SmolLM2-135M-Instruct','revision':'12fd25f77366fa6b3b4b768ec3050bf629380bac','weights_sha256':sha(BASE/'model.safetensors')}
def generate(m,tok,c,arm,state_root):
 m.eval();messages=prompt(c);ids=torch.tensor([encode(tok,c)]);start=time.perf_counter()
 with torch.inference_mode():
  o=m(input_ids=ids,attention_mask=torch.ones_like(ids),use_cache=True);cache=o.past_key_values;logits=o.logits[:,-1,:];new=[];stop='token_limit'
  for i in range(8):
   n=int(logits.argmax(-1).item());new.append(n)
   if n==tok.eos_token_id:stop='eos';break
   if i==7:break
   o=m(input_ids=torch.tensor([[n]]),past_key_values=cache,attention_mask=torch.ones((1,cache.get_seq_length()+1),dtype=torch.long),use_cache=True);cache=o.past_key_values;logits=o.logits[:,-1,:]
 elapsed=time.perf_counter()-start;rid=c['id']+'__'+arm;f=state_root/(rid+'.safetensors');assert not f.exists()
 tensors={f'layer{j}_{kind}':v.detach().cpu().contiguous() for j,pair in enumerate(cache.to_legacy_cache()) for kind,v in zip(('k','v'),pair)};sb=time.perf_counter();save_file(tensors,str(f));ser=time.perf_counter()-sb
 allids=ids[0].tolist()+new;count=int(cache.get_seq_length())
 return {'run_id':rid,'record_id':c['id'],'family':'lora_source_state','facet':'state_label','cycle':'LS1','arm':arm,'structure_family':c['structure_family'],'messages':messages,'rendered_prompt':tok.apply_chat_template(messages,tokenize=False,add_generation_prompt=True),'input_token_ids':ids[0].tolist(),'generated_token_ids':new,'text':tok.decode(new,skip_special_tokens=True),'stop':stop,'input_tokens':int(ids.shape[1]),'output_tokens':len(new),'inference_seconds_excluding_serialization':elapsed,'serialization_seconds':ser,'cache_artifact':{'local_path':str(f),'sha256':sha(f),'bytes':f.stat().st_size,'cache_token_count':count,'all_sequence_token_ids':allids,'cached_token_prefix_sha256':hashlib.sha256(json.dumps(allids[:count],separators=(',',':')).encode()).hexdigest()}}
