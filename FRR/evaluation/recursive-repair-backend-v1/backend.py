"""Pinned public CPU model: full inference vs cropped-cache replay; not SwaT."""
from pathlib import Path
import os,json,hashlib,sys,copy,re,platform
os.environ['HF_HUB_DISABLE_XET']='1'
os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'
import torch,transformers
from huggingface_hub import snapshot_download
from safetensors.torch import save_file,load_file
from transformers import AutoTokenizer,AutoModelForCausalLM,DynamicCache
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parents[1]/'tools'))
from cache_replay_plan import plan,token_digest

def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def prompt(tok,context,question):
 return tok.apply_chat_template([{'role':'user','content':'Use only the records below. Answer with exactly PASS if the stated condition is met, FAIL if the records establish it is not met, or UNKNOWN if the evidence is insufficient. Do not add explanation.\nRecords: '+context+'\nQuestion: '+question}],tokenize=True,add_generation_prompt=True,return_tensors='pt')

def greedy(model,tok,last,cache,limit=8):
 ids=[]
 for _ in range(limit):
  nxt=int(last.argmax(-1).item());ids.append(nxt)
  if nxt==tok.eos_token_id:break
  t=torch.tensor([[nxt]])
  out=model(input_ids=t,past_key_values=cache,use_cache=True,
            attention_mask=torch.ones((1,cache.get_seq_length()+1),dtype=torch.long))
  cache=out.past_key_values;last=out.logits[:,-1,:]
 return ids,tok.decode(ids,skip_special_tokens=True)

def label(s):
 m=re.match(r'^\s*(PASS|FAIL|UNKNOWN)\b',s)
 return m.group(1) if m else 'FORMAT_FAILURE'

def run():
 torch.set_num_threads(2);torch.manual_seed(0)
 pin=json.loads((P/'MODEL_PIN.json').read_text())
 target='/workspace/cache_backend_models/smollm2-135m'
 snapshot_download(repo_id=pin['model_id'],revision=pin['revision'],local_dir=target,
                   allow_patterns=['*.json','*.safetensors','*.txt'],token=False)
 path=Path(target)
 hashes={str(x.relative_to(path)):sha(x) for x in sorted(path.rglob('*')) if x.is_file() and '.cache' not in x.parts}
 (P/'DOWNLOADED_FILES.json').write_text(json.dumps(hashes,indent=2)+'\n')
 tok=AutoTokenizer.from_pretrained(path,local_files_only=True,trust_remote_code=False)
 model=AutoModelForCausalLM.from_pretrained(path,local_files_only=True,trust_remote_code=False,
                                         use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager').eval()
 identity={'model_revision':pin['revision']+':'+hashes['model.safetensors'],
           'tokenizer_revision':hashes['tokenizer.json'],'position_config':'model-config:'+hashes['config.json'],
           'attention_policy':'causal_full','kv_layout':'transformers4.57.1-DynamicCache-Llama-batch1',
           'dtype':'float32','adapter_identity':'none','multimodal_identity':'none','namespace':'local-authored-backend-test'}
 artifact_root=Path('/workspace/cache_backend_artifacts');artifact_root.mkdir(exist_ok=True)
 rows=[]
 with torch.inference_mode():
  for case in json.loads((P/'BACKEND_CASES.json').read_text()):
   old=prompt(tok,case['old'],case['question']);new=prompt(tok,case['new'],case['question'])
   original=model(input_ids=old,use_cache=True,attention_mask=torch.ones_like(old))
   oldcache=original.past_key_values
   legacy=oldcache.to_legacy_cache()
   arrays={f'layer{i}_{which}':v.detach().cpu().contiguous() for i,pair in enumerate(legacy) for which,v in zip(['k','v'],pair)}
   file=artifact_root/(case['id']+'.safetensors');save_file(arrays,str(file));expected_sha=sha(file)
   manifest={'token_ids':old[0].tolist(),'cache_token_count':old.shape[1],
             'prefix_sha256':token_digest(old[0].tolist()),'execution_identity':identity}
   decision=plan(manifest,{'token_ids':new[0].tolist(),'execution_identity':identity})
   # Gate actual artifact load on the recorded file binding.
   assert sha(file)==expected_sha
   restored=load_file(str(file));nlayer=len(legacy)
   cache=DynamicCache.from_legacy_cache(tuple((restored[f'layer{i}_k'],restored[f'layer{i}_v']) for i in range(nlayer)))
   keep=decision['reuse_prefix_tokens'];cache.crop(keep)
   suffix=new[:,keep:];assert suffix.shape[1]>0
   replay=model(input_ids=suffix,past_key_values=cache,use_cache=True,attention_mask=torch.ones_like(new))
   full=model(input_ids=new,use_cache=True,attention_mask=torch.ones_like(new))
   error=float((replay.logits[:,-1,:]-full.logits[:,-1,:]).abs().max().item())
   rid,rtxt=greedy(model,tok,replay.logits[:,-1,:],replay.past_key_values)
   fid,ftxt=greedy(model,tok,full.logits[:,-1,:],full.past_key_values)
   row={'id':case['id'],'gold':case['gold'],'old_tokens':old.shape[1],'new_tokens':new.shape[1],
        'plan':decision,'artifact_sha256':expected_sha,'artifact_bytes':file.stat().st_size,
        'last_prompt_max_logit_error':error,'logits_within_1e_4':error<=1e-4,
        'full_greedy_token_ids':fid,'replay_greedy_token_ids':rid,'greedy_tokens_match':fid==rid,
        'full_text':ftxt,'replay_text':rtxt,'full_label':label(ftxt),'replay_label':label(rtxt),
        'gold_label_match':label(ftxt)==case['gold']}
   rows.append(row)
   (P/'BACKEND_PARTIAL.json').write_text(json.dumps(rows,indent=2)+'\n')
   print(json.dumps({'id':case['id'],'logit_error':error,'greedy_match':fid==rid,'full_text':ftxt,'gold':case['gold']}),flush=True)
  first=artifact_root/'B1.safetensors';tampered=artifact_root/'B1.tampered.safetensors'
  b=bytearray(first.read_bytes());b[-1]^=1;tampered.write_bytes(b)
  binding={'original_sha256':sha(first),'tampered_sha256':sha(tampered),'refused_before_load':sha(first)!=sha(tampered)}
 result={'model':pin,'torch':torch.__version__,'transformers':transformers.__version__,'python':platform.python_version(),
         'identity':identity,'cases':rows,'binding_diagnostic':binding,'scope':'Six authored greedy CPU cases, same-model cache equivalence; no general semantic benefit or SwaT transfer.',
         'all_cache_logits_match':all(x['logits_within_1e_4'] for x in rows),'all_greedy_tokens_match':all(x['greedy_tokens_match'] for x in rows),
         'semantic_gold_matches':sum(x['gold_label_match'] for x in rows)}
 (P/'BACKEND_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
 return result

if __name__=='__main__':
 result=run();sys.exit(0 if result['all_cache_logits_match'] and result['all_greedy_tokens_match'] else 1)
