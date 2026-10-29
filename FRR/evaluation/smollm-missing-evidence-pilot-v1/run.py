"""One frozen paired guidance pilot. Preserve all branch outputs and actual caches."""
from pathlib import Path
import json,hashlib,time,sys,platform,os
os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'
import torch,transformers
from transformers import AutoTokenizer,AutoModelForCausalLM
from safetensors.torch import save_file
P=Path(__file__).resolve().parent

def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def run():
 frozen=json.loads((P/'FREEZE.json').read_text())['sha256']
 for name,h in frozen.items():assert sha(P/name)==h,name
 torch.set_num_threads(2);torch.manual_seed(0)
 path=Path('/workspace/cache_backend_models/smollm2-135m')
 tok=AutoTokenizer.from_pretrained(path,local_files_only=True,trust_remote_code=False)
 model=AutoModelForCausalLM.from_pretrained(path,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager').eval()
 guidance=json.loads((P/'GUIDANCE.json').read_text());cases=json.loads((P/'CASES.json').read_text())
 states=Path('/workspace/smollm_missing_evidence_states_v1');states.mkdir(exist_ok=True)
 rows=[]
 with torch.inference_mode():
  for i,case in enumerate(cases):
   arms=['ordinary','single_rule'] if i%2==0 else ['single_rule','ordinary']
   for order,arm in enumerate(arms):
    run_id=case['id']+'_'+arm
    user=guidance[arm]+'\n\nRecords:\n'+case['records']+'\n\nQuestion: '+case['question']+"\nAnswer in one short sentence. If information is missing, say 'Cannot determine from these records.'"
    messages=[{'role':'user','content':user}]
    rendered=tok.apply_chat_template(messages,tokenize=False,add_generation_prompt=True)
    ids=tok.apply_chat_template(messages,tokenize=True,add_generation_prompt=True,return_tensors='pt')
    begin=time.perf_counter();out=model(input_ids=ids,attention_mask=torch.ones_like(ids),use_cache=True)
    cache=out.past_key_values;logits=out.logits[:,-1,:];new=[];end='token_limit'
    for step in range(96):
     nxt=int(logits.argmax(-1).item());new.append(nxt)
     if nxt==tok.eos_token_id:end='eos';break
     if step==95:break
     out=model(input_ids=torch.tensor([[nxt]]),past_key_values=cache,use_cache=True,attention_mask=torch.ones((1,cache.get_seq_length()+1),dtype=torch.long))
     cache=out.past_key_values;logits=out.logits[:,-1,:]
    inference_seconds=time.perf_counter()-begin
    text=tok.decode(new,skip_special_tokens=True)
    all_ids=ids[0].tolist()+new;cached_count=int(cache.get_seq_length())
    file=states/(run_id+'.safetensors');assert not file.exists(),run_id
    arrays={f'layer{layer}_{kind}':value.detach().cpu().contiguous() for layer,pair in enumerate(cache.to_legacy_cache()) for kind,value in zip(['k','v'],pair)}
    save_file(arrays,str(file))
    row={'run_id':run_id,'case_id':case['id'],'condition':arm,'order_within_case':order,'messages':messages,'rendered_prompt':rendered,'input_token_ids':ids[0].tolist(),'generated_token_ids':new,'text':text,'stop':end,'input_tokens':ids.shape[1],'output_tokens':len(new),'inference_seconds_excluding_serialization':inference_seconds,'cache_artifact':{'local_path':str(file),'sha256':sha(file),'bytes':file.stat().st_size,'cache_token_count':cached_count,'all_sequence_token_ids':all_ids,'cached_token_prefix_sha256':hashlib.sha256(json.dumps(all_ids[:cached_count],separators=(',',':')).encode()).hexdigest(),'note':'Terminal KV cache excludes last generated token if not forwarded. Full token sequence retained for reconstruction; no original cache branch was overwritten.'}}
    rows.append(row)
    with (P/'RAW_OUTPUTS.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
    print(json.dumps({'run':run_id,'stop':end,'tokens':len(new),'text':text}),flush=True)
 manifest={'torch':torch.__version__,'transformers':transformers.__version__,'python':platform.python_version(),'model_pin':json.loads((P/'MODEL_PIN.json').read_text()),'generations':len(rows),'gold_not_in_messages':True,'scope':'Single greedy paired authored development run, not independent contexts in a statistical sense; same model weights.'}
 (P/'RUN_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
 (P/'RAW_FREEZE.json').write_text(json.dumps({'phase':'before manual scoring','sha256':{name:sha(P/name) for name in ['RAW_OUTPUTS.jsonl','RUN_MANIFEST.json','RUN.log']}},indent=2)+'\n')

if __name__=='__main__':run()
