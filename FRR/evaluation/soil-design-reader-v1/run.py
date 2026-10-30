"""Frozen local reader probe; no optimizer, network, or implicit continuation."""
from pathlib import Path
import json,hashlib,time,platform,os
os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'
os.environ['HF_HUB_OFFLINE']='1'
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
    assert not (P/'RAW_OUTPUTS.jsonl').exists(),'No silent reruns/appends'
    for n,h in json.loads((P/'FREEZE.json').read_text())['sha256'].items():
        assert sha(P/n)==h,n
    old=json.loads((P/'PRESERVATION_BEFORE.json').read_text())
    for name,h in old['model_and_cache_sha256'].items():assert sha(Path(name))==h,name
    torch.set_num_threads(2);torch.manual_seed(0)
    path=Path('/workspace/cache_backend_models/smollm2-135m')
    load_start=time.perf_counter()
    tok=AutoTokenizer.from_pretrained(path,local_files_only=True,trust_remote_code=False)
    model=AutoModelForCausalLM.from_pretrained(path,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager').eval()
    load_seconds=time.perf_counter()-load_start
    cases=json.loads((P/'CASES.json').read_text())
    guidance=json.loads((P/'GUIDANCE.json').read_text())['instruction']
    states=Path('/workspace/smollm_soil_reader_states_v1');states.mkdir(exist_ok=False)
    rows=[]
    with torch.inference_mode():
        for case in cases:
            user=guidance+'\n\nRecord:\n'+case['source']+'\n\nQuestion: '+case['question']
            messages=[{'role':'user','content':user}]
            rendered=tok.apply_chat_template(messages,tokenize=False,add_generation_prompt=True)
            ids=tok.apply_chat_template(messages,tokenize=True,add_generation_prompt=True,return_tensors='pt')
            begin=time.perf_counter()
            out=model(input_ids=ids,attention_mask=torch.ones_like(ids),use_cache=True)
            cache=out.past_key_values; logits=out.logits[:,-1,:];new=[];stop='token_limit'
            for step in range(64):
                nxt=int(logits.argmax(-1).item());new.append(nxt)
                if nxt==tok.eos_token_id:stop='eos';break
                if step==63:break
                out=model(input_ids=torch.tensor([[nxt]]),past_key_values=cache,use_cache=True,attention_mask=torch.ones((1,cache.get_seq_length()+1),dtype=torch.long))
                cache=out.past_key_values;logits=out.logits[:,-1,:]
            seconds=time.perf_counter()-begin
            text=tok.decode(new,skip_special_tokens=True)
            allids=ids[0].tolist()+new; cached_count=int(cache.get_seq_length())
            file=states/(case['id']+'.safetensors')
            assert not file.exists()
            arrays={f'layer{layer}_{kind}':value.detach().cpu().contiguous() for layer,pair in enumerate(cache.to_legacy_cache()) for kind,value in zip(['k','v'],pair)}
            serbegin=time.perf_counter();save_file(arrays,str(file));ser_seconds=time.perf_counter()-serbegin
            row={'run_id':case['id'],'record_id':case['record_id'],'family':case['family'],'facet':case['facet'],'messages':messages,'rendered_prompt':rendered,'input_token_ids':ids[0].tolist(),'generated_token_ids':new,'text':text,'stop':stop,'input_tokens':int(ids.shape[1]),'output_tokens':len(new),'inference_seconds_excluding_serialization':seconds,'serialization_seconds':ser_seconds,'cache_artifact':{'local_path':str(file),'sha256':sha(file),'bytes':file.stat().st_size,'cache_token_count':cached_count,'all_sequence_token_ids':allids,'cached_token_prefix_sha256':hashlib.sha256(json.dumps(allids[:cached_count],separators=(',',':')).encode()).hexdigest(),'note':'Terminal cache excludes last emitted token if not forwarded. Token IDs preserve the full sequence; no old branch overwritten.'}}
            with (P/'RAW_OUTPUTS.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
            rows.append(row)
            print(json.dumps({'run':case['id'],'stop':stop,'tokens':len(new),'text':text}),flush=True)
    manifest={'model_pin':json.loads((P/'MODEL_PIN.json').read_text()),'torch':torch.__version__,'transformers':transformers.__version__,'python':platform.python_version(),'model_load_seconds':load_seconds,'generations':len(rows),'gold_keys_not_loaded_by_runner':True,'max_new_tokens':64,'scope':'Eight authored records, three fresh contexts each, no comparison arm or training. Independent calls are not independent model replications.'}
    (P/'RUN_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
if __name__=='__main__':run()
