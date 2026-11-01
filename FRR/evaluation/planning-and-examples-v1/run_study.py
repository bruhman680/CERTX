"""One fixed reader, finite public planning allowance, real one-request routes."""
from pathlib import Path
import hashlib
import json
import os
import time

os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'
import torch
from task import decode_action,observed_rule,finish_route
from routing_reference import retrieve
from generate import generate
from runtime_reference import sha,dump_new,append_json,Guard,parameter_digest
from lora_cpu import inject_lora,load_adapter

ROOT=Path(__file__).resolve().parent
ACQ=ROOT.parent/'simple-readout-acquisition-v1/run/canonical'

def main():
    from transformers import AutoTokenizer,AutoModelForCausalLM
    freeze=json.loads((ROOT/'FREEZE.json').read_text())
    assert all(sha(ROOT/n)==h for n,h in freeze['sha256'].items())
    assert all(sha(Path(n))==h for n,h in freeze['dependencies'].items())
    cases={c['id']:c for c in json.loads((ROOT/'DATA.json').read_text())}
    queries=json.loads((ROOT/'QUERIES.json').read_text());links=json.loads((ROOT/'LINKS.json').read_text())
    out=ROOT/'run';out.mkdir();guard=Guard(5153960755,out/'RESOURCE.jsonl')
    manifest=json.loads((ACQ/'MANIFEST.json').read_text());base=Path('/workspace/cache_backend_models/smollm2-135m')
    assert sha(base/'model.safetensors')==manifest['base_pin']['weights_sha256']
    torch.set_num_threads(2);torch.manual_seed(73103)
    tok=AutoTokenizer.from_pretrained(base,local_files_only=True,trust_remote_code=False)
    lengths={q['id']:len(tok.apply_chat_template([{'role':'user','content':q['prompt']}],tokenize=True,add_generation_prompt=True)) for q in queries}
    assert max(lengths.values())<=768
    dump_new(out/'TOKENIZATION.json',{'prompt_lengths':lengths,'max_prompt_tokens':max(lengths.values()),'no_truncation':True})
    guard.read('before_model_load')
    model=AutoModelForCausalLM.from_pretrained(base,local_files_only=True,trust_remote_code=False,
        use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
    inject_lora(model,rank=4,alpha=8,dropout=0.);load_adapter(model,ACQ/'final',base_pin=manifest['base_pin'])
    assert parameter_digest(model,True)==manifest['final_digest']
    model.eval()
    # Validate last-logit-only head against full head on six explicit-action
    # calibration inputs. This optimization does not mask actions or change weights.
    checks=[]
    with torch.inference_mode():
        for word in ('YES','NO','WITHHOLD','FULL','TARGET','UNKNOWN'):
            ids=tok.apply_chat_template([{'role':'user','content':'Return only this action word: '+word}],tokenize=True,add_generation_prompt=True)
            x=torch.tensor([ids]);mask=torch.ones_like(x)
            full=model(input_ids=x,attention_mask=mask,use_cache=False).logits[0,-1]
            last=model(input_ids=x,attention_mask=mask,use_cache=False,logits_to_keep=1).logits[0,-1]
            delta=float((full-last).abs().max());same=int(full.argmax())==int(last.argmax())
            checks.append({'word':word,'max_abs_delta':delta,'same_argmax':same})
            assert same and delta<=1e-4
    dump_new(out/'LOGIT_HEAD_CHECK.json',{'calibration':checks,'scope':'six calibration contexts,not all possible inputs','new_generation_probes':0,'prefill_forwards':12})
    probes={};began=time.perf_counter()
    for i,q in enumerate(queries,1):
        if time.perf_counter()-began>1200:raise TimeoutError('Bounded study wall cap reached;retain partial,no retry')
        row=generate(model,tok,q['prompt'],q['cap'],guard,q['id'])
        row.update({'examples':q['examples'],'response':q['response'],'decision':decode_action(row['text'])})
        append_json(out/'ROUTER_RAW.jsonl',row);probes[q['id']]=row
        if i%16==0:print(json.dumps({'router_probes':i,'planned':96}),flush=True)
    workers={};routes=[]
    def execute(c,action,meta):
        tool=None;state=None;wid=None;hit=False
        if action in ('FULL','TARGET'):
            tool=retrieve(c,action)
            if tool['available']:
                mapping='missing=WITHHOLD; positive=YES; zero=NO'
                text='Map the status to its answer. '+mapping+'. Return only the answer.\n\n'+tool['source']
                if tool['kind']=='full':text='Read only the record for the target plot.\n'+text
                key=hashlib.sha256(text.encode()).hexdigest();hit=key in workers
                if not hit:
                    w=generate(model,tok,text,8,guard,f'worker_{len(workers):03d}')
                    w['prompt_sha256']=key;w['state']={'YES':'positive','NO':'zero','WITHHOLD':'missing'}.get(w['text'].strip())
                    append_json(out/'WORKER_RAW.jsonl',w);workers[key]=w
                w=workers[key];state=w['state'];wid=w['run_id']
        result=finish_route(c,action,state,tool)
        row={'route_id':f'route_{len(routes):04d}','case_id':c['id'],'style':c['style'],'kind':c['kind'],
             **meta,**result,'tool':tool,'worker_id':wid,'worker_cache_hit':hit}
        append_json(out/'ROUTES.jsonl',row);routes.append(row)
    for link in links:
        p=probes[link['query_id']]
        execute(cases[link['case_id']],p['decision']['action'],{'policy':('examples' if link['examples'] else 'none')+'__'+link['response'],
            'query_id':link['query_id'],'examples':link['examples'],'response':link['response']})
    for policy in ('always_target','always_full','always_unknown','observed_rule'):
        for c in cases.values():
            action={'always_target':'TARGET','always_full':'FULL','always_unknown':'UNKNOWN'}.get(policy)
            if policy=='observed_rule':action=observed_rule(c)
            execute(c,action,{'policy':policy,'query_id':None,'examples':None,'response':None})
    assert len(routes)==480 and len(workers)==18
    assert parameter_digest(model,True)==manifest['final_digest']
    assert parameter_digest(model,False)==manifest['base_digest_after']
    assert sha(base/'model.safetensors')==manifest['base_pin']['weights_sha256']
    assert all(sha(Path(n))==h for n,h in freeze['dependencies'].items())
    dump_new(out/'RUN_MANIFEST.json',{'status':'complete','actual_router_generations':96,'actual_worker_generations':18,
        'logical_routes':480,'new_weight_updates':0,'candidate_scoring_forwards':0,'calibration_prefill_forwards':12,
        'saved_base_and_adapter_unchanged':True,'query_cache_fresh_per_probe':True})
    print(json.dumps({'complete':True,'router':96,'worker':18,'routes':480}),flush=True)

if __name__=='__main__':main()
